package com.zatoona.app

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.media.AudioAttributes
import android.media.AudioFocusRequest
import android.media.AudioManager
import android.media.MediaPlayer
import android.media.RingtoneManager
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.PowerManager
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import kotlin.math.abs

/**
 * AlarmService
 * Foreground service for continuous alarm ringing, looping vibration, and lock-screen dismissal.
 * Complies with Android 14 (API 34) specialUse foreground service policy.
 */
class AlarmService : Service() {

    companion object {
        const val TAG = "ZatoonaAlarmService"

        const val ACTION_START_ALARM = "com.zatoona.app.ACTION_START_ALARM"
        const val ACTION_DISMISS_ALARM = "com.zatoona.app.ACTION_DISMISS_ALARM"

        const val EXTRA_SCHEDULE_ID = "com.zatoona.app.EXTRA_SCHEDULE_ID"
        const val EXTRA_TRIGGER_MS = "com.zatoona.app.EXTRA_TRIGGER_MS"
        const val EXTRA_TITLE = "com.zatoona.app.EXTRA_TITLE"
        const val EXTRA_BODY = "com.zatoona.app.EXTRA_BODY"
        const val EXTRA_MODE = "com.zatoona.app.EXTRA_MODE"
        const val EXTRA_TYPE = "com.zatoona.app.EXTRA_TYPE"

        const val AUTO_SILENCE_TIMEOUT_MS = 10 * 60 * 1000L // 10 minutes auto-silence safety

        // Singleton state for deduplication and active alarm synchronization
        @Volatile
        var isAlarmActive: Boolean = false
            private set

        @Volatile
        var activeScheduleId: String? = null
            private set

        @Volatile
        var activeTriggerMs: Long = 0L
            private set

        var onAlarmDismissed: (() -> Unit)? = null
    }

    private var mediaPlayer: MediaPlayer? = null
    private var vibrator: Vibrator? = null
    private var wakeLock: PowerManager.WakeLock? = null
    private var audioManager: AudioManager? = null
    private var audioFocusRequest: AudioFocusRequest? = null

    private val handler = Handler(Looper.getMainLooper())
    private val autoSilenceRunnable = Runnable {
        Log.w(TAG, "Alarm reached 10-minute auto-silence limit. Silencing...")
        handleAutoSilence()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        audioManager = getSystemService(Context.AUDIO_SERVICE) as? AudioManager
        initVibrator()
        acquireWakeLock()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent == null) {
            stopSelf()
            return START_NOT_STICKY
        }

        when (intent.action) {
            ACTION_START_ALARM -> {
                val scheduleId = intent.getStringExtra(EXTRA_SCHEDULE_ID) ?: ""
                val triggerMs = intent.getLongExtra(EXTRA_TRIGGER_MS, System.currentTimeMillis())
                val title = intent.getStringExtra(EXTRA_TITLE) ?: "تذكير زتونة"
                val body = intent.getStringExtra(EXTRA_BODY) ?: ""
                val mode = intent.getStringExtra(EXTRA_MODE) ?: "home"
                val type = intent.getStringExtra(EXTRA_TYPE) ?: "custom"

                handleStartAlarm(scheduleId, triggerMs, title, body, mode, type)
            }

            ACTION_DISMISS_ALARM -> {
                val scheduleId = intent.getStringExtra(EXTRA_SCHEDULE_ID) ?: activeScheduleId
                Log.i(TAG, "Dismiss action received for schedule: $scheduleId")
                handleDismissAlarm()
            }

            else -> {
                Log.w(TAG, "Unknown action: ${intent.action}")
            }
        }

        return START_NOT_STICKY
    }

    private fun handleStartAlarm(
        scheduleId: String,
        triggerMs: Long,
        title: String,
        body: String,
        mode: String,
        type: String
    ) {
        // Build and display foreground notification immediately (Android requirement)
        val notifId = abs(scheduleId.hashCode())
        val notification = buildForegroundNotification(scheduleId, triggerMs, title, body, mode, type)

        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
                ServiceCompat.startForeground(
                    this,
                    notifId,
                    notification,
                    ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE
                )
            } else {
                startForeground(notifId, notification)
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error starting foreground service: ${e.message}", e)
        }

        // Deduplication: if the exact same schedule and trigger is already sounding, do not restart
        if (isAlarmActive && activeScheduleId == scheduleId && activeTriggerMs == triggerMs) {
            Log.d(TAG, "Alarm $scheduleId at $triggerMs already active. Keeping current playback.")
            return
        }

        activeScheduleId = scheduleId
        activeTriggerMs = triggerMs
        isAlarmActive = true

        // Reset auto-silence countdown
        handler.removeCallbacks(autoSilenceRunnable)
        handler.postDelayed(autoSilenceRunnable, AUTO_SILENCE_TIMEOUT_MS)

        // Request audio focus and start audio playback
        requestAlarmAudioFocus()
        startLoopingAudio()
        startVibration()

        Log.i(TAG, "Alarm started for $scheduleId ($title) at $triggerMs")
    }

    private fun handleDismissAlarm() {
        stopAudioAndVibration()
        releaseWakeLock()
        handler.removeCallbacks(autoSilenceRunnable)

        val scheduleId = activeScheduleId
        isAlarmActive = false
        activeScheduleId = null
        activeTriggerMs = 0L

        // Notify active AlarmActivity to close
        try {
            onAlarmDismissed?.invoke()
        } catch (e: Exception) {
            Log.w(TAG, "Error invoking onAlarmDismissed: ${e.message}")
        }

        // Cancel the notification
        if (!scheduleId.isNullOrBlank()) {
            val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.cancel(abs(scheduleId.hashCode()))
        }

        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    private fun handleAutoSilence() {
        val scheduleId = activeScheduleId
        val notifId = if (!scheduleId.isNullOrBlank()) abs(scheduleId.hashCode()) else 9999

        stopAudioAndVibration()
        releaseWakeLock()

        isAlarmActive = false
        activeScheduleId = null
        activeTriggerMs = 0L

        // Notify active AlarmActivity to close
        try {
            onAlarmDismissed?.invoke()
        } catch (e: Exception) {
            Log.w(TAG, "Error notifying dismiss on auto-silence: ${e.message}")
        }

        // Demote foreground and post missed alarm notice
        stopForeground(STOP_FOREGROUND_REMOVE)

        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val missedNotice = NotificationCompat.Builder(this, ZatoonaNotificationManager.CHANNEL_REMINDERS)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentTitle("منبه فائت")
            .setContentText("تم كتم صوت المنبه تلقائياً بعد 10 دقائق لحماية البطارية.")
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)
            .build()
        notificationManager.notify(notifId, missedNotice)

        stopSelf()
    }

    private fun startLoopingAudio() {
        try {
            if (mediaPlayer?.isPlaying == true) {
                return
            }
            mediaPlayer?.release()

            val alarmUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
                ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
                ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_RINGTONE)

            mediaPlayer = MediaPlayer().apply {
                setDataSource(applicationContext, alarmUri)
                setAudioAttributes(
                    AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_ALARM)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                        .build()
                )
                isLooping = true
                prepare()
                start()
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error starting alarm MediaPlayer: ${e.message}", e)
        }
    }

    private fun requestAlarmAudioFocus() {
        val am = audioManager ?: return
        val audioAttributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_ALARM)
            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            .build()

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            audioFocusRequest = AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_EXCLUSIVE)
                .setAudioAttributes(audioAttributes)
                .setOnAudioFocusChangeListener { focusChange ->
                    Log.d(TAG, "Alarm audio focus changed: $focusChange")
                }
                .build()
            audioFocusRequest?.let { am.requestAudioFocus(it) }
        } else {
            @Suppress("DEPRECATION")
            am.requestAudioFocus(null, AudioManager.STREAM_ALARM, AudioManager.AUDIOFOCUS_GAIN_TRANSIENT)
        }
    }

    private fun releaseAlarmAudioFocus() {
        val am = audioManager ?: return
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            audioFocusRequest?.let { am.abandonAudioFocusRequest(it) }
            audioFocusRequest = null
        } else {
            @Suppress("DEPRECATION")
            am.abandonAudioFocus(null)
        }
    }

    private fun initVibrator() {
        vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val vm = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
            vm?.defaultVibrator
        } else {
            @Suppress("DEPRECATION")
            getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
        }
    }

    private fun startVibration() {
        val vib = vibrator ?: return
        val pattern = longArrayOf(0, 600, 600, 600)
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                vib.vibrate(VibrationEffect.createWaveform(pattern, 0))
            } else {
                @Suppress("DEPRECATION")
                vib.vibrate(pattern, 0)
            }
        } catch (e: Exception) {
            Log.w(TAG, "Failed to start vibration: ${e.message}")
        }
    }

    private fun stopAudioAndVibration() {
        try {
            if (mediaPlayer?.isPlaying == true) {
                mediaPlayer?.stop()
            }
            mediaPlayer?.release()
            mediaPlayer = null
        } catch (e: Exception) {
            Log.w(TAG, "Error stopping MediaPlayer: ${e.message}")
        }

        try {
            vibrator?.cancel()
        } catch (e: Exception) {
            Log.w(TAG, "Error cancelling vibrator: ${e.message}")
        }

        releaseAlarmAudioFocus()
    }

    private fun acquireWakeLock() {
        try {
            val pm = getSystemService(Context.POWER_SERVICE) as? PowerManager
            wakeLock = pm?.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "Zatoona:AlarmServiceWakeLock")
            wakeLock?.acquire(11 * 60 * 1000L) // Safe 11-minute timeout
        } catch (e: Exception) {
            Log.w(TAG, "Error acquiring wake lock: ${e.message}")
        }
    }

    private fun releaseWakeLock() {
        try {
            if (wakeLock?.isHeld == true) {
                wakeLock?.release()
            }
            wakeLock = null
        } catch (e: Exception) {
            Log.w(TAG, "Error releasing wake lock: ${e.message}")
        }
    }

    private fun buildForegroundNotification(
        scheduleId: String,
        triggerMs: Long,
        title: String,
        body: String,
        mode: String,
        type: String
    ): Notification {
        val channelId = ZatoonaNotificationManager.CHANNEL_ALARMS

        // Ensure alarm notification channel exists
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            val channel = NotificationChannel(
                channelId,
                "منبهات زتونة",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "تنبيهات المنبه التفاعلية مع شاشة القفل والصوت المستمر"
                enableVibration(true)
                setBypassDnd(true)
                lockscreenVisibility = Notification.VISIBILITY_PUBLIC
                setSound(null, null) // Silent channel: AlarmService manages looping audio directly
            }
            nm.createNotificationChannel(channel)
        }

        // Full Screen Intent pointing to AlarmActivity
        val fullScreenIntent = Intent(this, AlarmActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or
                    Intent.FLAG_ACTIVITY_NO_USER_ACTION or
                    Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra(EXTRA_SCHEDULE_ID, scheduleId)
            putExtra(EXTRA_TRIGGER_MS, triggerMs)
            putExtra(EXTRA_TITLE, title)
            putExtra(EXTRA_BODY, body)
            putExtra(EXTRA_MODE, mode)
            putExtra(EXTRA_TYPE, type)
        }

        val reqCode = abs(scheduleId.hashCode())
        val fullScreenPendingIntent = PendingIntent.getActivity(
            this,
            reqCode,
            fullScreenIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        // Dismiss action intent
        val dismissIntent = Intent(this, AlarmService::class.java).apply {
            action = ACTION_DISMISS_ALARM
            putExtra(EXTRA_SCHEDULE_ID, scheduleId)
        }
        val dismissPendingIntent = PendingIntent.getService(
            this,
            reqCode + 5000,
            dismissIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val builder = NotificationCompat.Builder(this, channelId)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentTitle(title)
            .setContentText(body.ifBlank { "منبه نشط — اسحب أو اضغط للإيقاف" })
            .setStyle(NotificationCompat.BigTextStyle().bigText(body.ifBlank { "منبه نشط — اسحب أو اضغط للإيقاف" }))
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setOngoing(true)
            .setAutoCancel(false)
            .setContentIntent(fullScreenPendingIntent)
            .addAction(
                android.R.drawable.ic_menu_close_clear_cancel,
                "إيقاف",
                dismissPendingIntent
            )

        // Full-screen intent validation for Android 14+
        val canUseFullScreen = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            nm.canUseFullScreenIntent()
        } else {
            true
        }

        if (canUseFullScreen) {
            builder.setFullScreenIntent(fullScreenPendingIntent, true)
        }

        return builder.build()
    }

    override fun onDestroy() {
        stopAudioAndVibration()
        releaseWakeLock()
        handler.removeCallbacks(autoSilenceRunnable)
        super.onDestroy()
    }
}

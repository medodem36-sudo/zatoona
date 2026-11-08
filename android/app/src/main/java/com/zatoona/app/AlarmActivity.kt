package com.zatoona.app

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.media.RingtoneManager
import android.os.Build
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.Bundle
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.util.Log
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.view.animation.OvershootInterpolator
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * AlarmActivity
 * Native full-screen interactive alarm display over Android lock screen.
 * Provides continuous visual alert, swipe-to-dismiss gesture, and fallback dismiss button.
 */
class AlarmActivity : AppCompatActivity() {

    companion object {
        private const val TAG = "ZatoonaAlarmActivity"
    }

    private var scheduleId: String = ""
    private var triggerMs: Long = 0L
    private var isDismissed = false

    private var localMediaPlayer: MediaPlayer? = null
    private var localVibrator: Vibrator? = null

    // 598. Flip-to-Dismiss / Snooze Physical Sensor Listener
    private var sensorManager: SensorManager? = null
    private var accelerometer: Sensor? = null
    private var isFaceDown = false
    private var lastFlipTime = 0L

    private val sensorListener = object : SensorEventListener {
        override fun onSensorChanged(event: SensorEvent?) {
            if (event?.sensor?.type == Sensor.TYPE_ACCELEROMETER) {
                val z = event.values[2]
                // When phone is placed face-down, Z acceleration is near -9.8 m/s^2
                if (z < -6.5) {
                    val now = System.currentTimeMillis()
                    if (!isFaceDown && (now - lastFlipTime > 1500)) {
                        isFaceDown = true
                        lastFlipTime = now
                        android.util.Log.i(TAG, "Flip-to-Dismiss gesture detected! Dismissing alarm.")
                        runOnUiThread {
                            triggerDismiss()
                        }
                    }
                } else if (z > 2.0) {
                    isFaceDown = false
                }
            }
        }
        override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}
    }

    private lateinit var swipeTrack: FrameLayout
    private lateinit var swipeHandle: FrameLayout
    private lateinit var tvSwipeHint: TextView
    private lateinit var btnDismiss: MaterialButton
    private lateinit var tvAlarmTime: TextView
    private lateinit var tvAlarmTitle: TextView
    private lateinit var tvAlarmBody: TextView
    private lateinit var ivBellLarge: ImageView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        configureLockScreenFlags()
        setContentView(R.layout.activity_alarm)

        initViews()
        unpackIntent(intent)
        setupSwipeToDismiss()
        setupListeners()
        startLocalAudioAndVibration()

        // Register Flip-to-Dismiss accelerometer sensor listener
        try {
            sensorManager = getSystemService(Context.SENSOR_SERVICE) as? SensorManager
            accelerometer = sensorManager?.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
            accelerometer?.let {
                sensorManager?.registerListener(sensorListener, it, SensorManager.SENSOR_DELAY_UI)
            }
        } catch (e: Exception) {
            android.util.Log.w(TAG, "Failed to register accelerometer: ${e.message}")
        }
    }

    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        setIntent(intent)
        intent?.let { unpackIntent(it) }
        startLocalAudioAndVibration()
    }

    private fun configureLockScreenFlags() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1) {
            setShowWhenLocked(true)
            setTurnScreenOn(true)
        } else {
            @Suppress("DEPRECATION")
            window.addFlags(
                WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON
            )
        }
        window.addFlags(
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON or
            WindowManager.LayoutParams.FLAG_ALLOW_LOCK_WHILE_SCREEN_ON
        )
    }

    private fun initViews() {
        swipeTrack = findViewById(R.id.swipeTrack)
        swipeHandle = findViewById(R.id.swipeHandle)
        tvSwipeHint = findViewById(R.id.tvSwipeHint)
        btnDismiss = findViewById(R.id.btnDismiss)
        tvAlarmTime = findViewById(R.id.tvAlarmTime)
        tvAlarmTitle = findViewById(R.id.tvAlarmTitle)
        tvAlarmBody = findViewById(R.id.tvAlarmBody)
        ivBellLarge = findViewById(R.id.ivBellLarge)
    }

    private fun unpackIntent(intent: Intent) {
        scheduleId = intent.getStringExtra(AlarmService.EXTRA_SCHEDULE_ID) ?: ""
        triggerMs = intent.getLongExtra(AlarmService.EXTRA_TRIGGER_MS, System.currentTimeMillis())
        val title = intent.getStringExtra(AlarmService.EXTRA_TITLE) ?: "تذكير زتونة"
        val body = intent.getStringExtra(AlarmService.EXTRA_BODY) ?: ""

        val displayTimeMs = if (triggerMs > 0) triggerMs else System.currentTimeMillis()
        val timeFormat = SimpleDateFormat("hh:mm a", Locale("ar"))
        tvAlarmTime.text = timeFormat.format(Date(displayTimeMs))

        tvAlarmTitle.text = title
        tvAlarmBody.text = if (body.isNotBlank()) body else "حان موعد التذكير المجدول"
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun setupSwipeToDismiss() {
        var startX = 0f

        swipeHandle.setOnTouchListener { view, event ->
            val marginStart = (view.layoutParams as? ViewGroup.MarginLayoutParams)?.marginStart ?: 0
            val maxTravel = (swipeTrack.width - view.width - (marginStart * 2)).coerceAtLeast(1)

            when (event.actionMasked) {
                MotionEvent.ACTION_DOWN -> {
                    startX = event.rawX
                    true
                }

                MotionEvent.ACTION_MOVE -> {
                    if (isDismissed) return@setOnTouchListener true

                    val deltaX = event.rawX - startX
                    val clampedX = deltaX.coerceIn(0f, maxTravel.toFloat())
                    view.translationX = clampedX

                    val progress = clampedX / maxTravel.toFloat()
                    tvSwipeHint.alpha = (1f - progress * 1.5f).coerceAtLeast(0.1f)

                    if (progress >= 0.70f) {
                        isDismissed = true
                        triggerDismiss()
                    }
                    true
                }

                MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                    if (!isDismissed) {
                        view.animate()
                            .translationX(0f)
                            .setDuration(250)
                            .setInterpolator(OvershootInterpolator(1.2f))
                            .start()
                        tvSwipeHint.animate().alpha(1f).setDuration(250).start()
                    }
                    true
                }

                else -> false
            }
        }
    }

    private fun setupListeners() {
        btnDismiss.setOnClickListener {
            if (!isDismissed) {
                isDismissed = true
                triggerDismiss()
            }
        }

        // Listen for dismissal triggered externally (e.g., from notification action button)
        AlarmService.onAlarmDismissed = {
            runOnUiThread {
                if (!isFinishing) {
                    finish()
                }
            }
        }
    }

    private fun startLocalAudioAndVibration() {
        if (AlarmService.isAlarmActive) {
            Log.d(TAG, "AlarmService is already actively handling alarm sound.")
            return
        }

        try {
            if (localMediaPlayer?.isPlaying == true) return
            localMediaPlayer?.release()

            val alarmUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
                ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
                ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_RINGTONE)

            localMediaPlayer = MediaPlayer().apply {
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
            Log.i(TAG, "Started local looping alarm audio fallback in AlarmActivity")
        } catch (e: Exception) {
            Log.w(TAG, "Failed to start local audio fallback: ${e.message}")
        }

        try {
            val pattern = longArrayOf(0, 600, 600, 600)
            localVibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vm = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
                vm?.defaultVibrator
            } else {
                @Suppress("DEPRECATION")
                getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                localVibrator?.vibrate(VibrationEffect.createWaveform(pattern, 0))
            } else {
                @Suppress("DEPRECATION")
                localVibrator?.vibrate(pattern, 0)
            }
            Log.i(TAG, "Started local looping vibration fallback in AlarmActivity")
        } catch (e: Exception) {
            Log.w(TAG, "Failed to start local vibration fallback: ${e.message}")
        }
    }

    private fun stopLocalAudioAndVibration() {
        try {
            if (localMediaPlayer?.isPlaying == true) {
                localMediaPlayer?.stop()
            }
            localMediaPlayer?.release()
            localMediaPlayer = null
        } catch (e: Exception) {
            Log.w(TAG, "Error stopping local MediaPlayer: ${e.message}")
        }

        try {
            localVibrator?.cancel()
            localVibrator = null
        } catch (e: Exception) {
            Log.w(TAG, "Error cancelling local vibrator: ${e.message}")
        }
    }

    private fun triggerDismiss() {
        stopLocalAudioAndVibration()
        performHapticClick()

        // Send dismiss command to AlarmService
        val dismissIntent = Intent(this, AlarmService::class.java).apply {
            action = AlarmService.ACTION_DISMISS_ALARM
            putExtra(AlarmService.EXTRA_SCHEDULE_ID, scheduleId)
        }
        startService(dismissIntent)

        // Mark dismissed in repository to prevent duplicate alerts
        if (scheduleId.isNotBlank()) {
            val repository = ZatoonaScheduleRepository(this)
            repository.markDispatched("$scheduleId:dismissed", System.currentTimeMillis())
        }

        // Finish activity cleanly
        finish()
        overridePendingTransition(0, android.R.anim.fade_out)
    }

    private fun performHapticClick() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vm = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
                vm?.defaultVibrator?.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK))
            } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                @Suppress("DEPRECATION")
                val vib = getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
                vib?.vibrate(VibrationEffect.createOneShot(50, VibrationEffect.DEFAULT_AMPLITUDE))
            }
        } catch (e: Exception) {
            // Ignore haptic error
        }
    }

    override fun onDestroy() {
        stopLocalAudioAndVibration()
        try {
            sensorManager?.unregisterListener(sensorListener)
        } catch (e: Exception) {}
        AlarmService.onAlarmDismissed = null
        super.onDestroy()
    }
}

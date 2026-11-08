package com.zatoona.app

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.PowerManager
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import java.util.Locale

/**
 * WakeWordService
 * Continuous foreground listening service for Coach Zaitouna wake words ("يا كوتش", "يا زتونة").
 * Operates reliably across lock-screen, screen-off, and background states via
 * FOREGROUND_SERVICE_MICROPHONE and a dedicated partial WakeLock.
 */
class WakeWordService : Service() {

    private val mainHandler = Handler(Looper.getMainLooper())
    private var wakeLock: PowerManager.WakeLock? = null
    private var speechRecognizer: SpeechRecognizer? = null
    private var textToSpeech: TextToSpeech? = null
    private var isTtsReady: Boolean = false

    companion object {
        const val TAG = "WakeWordService"
        const val ACTION_START = "com.zatoona.app.ACTION_START_WAKE_WORD"
        const val ACTION_STOP = "com.zatoona.app.ACTION_STOP_WAKE_WORD"
        const val ACTION_PAUSE = "com.zatoona.app.ACTION_PAUSE_WAKE_WORD"
        const val ACTION_RESUME = "com.zatoona.app.ACTION_RESUME_WAKE_WORD"

        private const val NOTIFICATION_ID = 9005
        private const val CHANNEL_ID = "zatoona_wake_word_channel"

        @Volatile
        var isRunning: Boolean = false
            private set

        @Volatile
        var isPausedForExternalInput: Boolean = false
            private set

        @Volatile
        var instance: WakeWordService? = null
            private set

        fun pauseListening() {
            isPausedForExternalInput = true
            instance?.stopRecognizer()
        }

        fun resumeListening() {
            isPausedForExternalInput = false
            instance?.scheduleRecognizerRestart(300L)
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        instance = this
        createNotificationChannel()
        acquireWakeLock()
        initTextToSpeech()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.action ?: ACTION_START

        when (action) {
            ACTION_STOP -> {
                Log.i(TAG, "WakeWordService received STOP action")
                val prefs = getSharedPreferences("zatoona_settings", Context.MODE_PRIVATE)
                prefs.edit().putBoolean("wake_word_continuous_enabled", false).apply()
                stopListeningAndSelf()
                return START_NOT_STICKY
            }
            ACTION_PAUSE -> {
                pauseListening()
                return START_STICKY
            }
            ACTION_RESUME -> {
                resumeListening()
                return START_STICKY
            }
            ACTION_START -> {
                Log.i(TAG, "WakeWordService received START action")
                val notification = buildForegroundNotification()
                try {
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
                        ServiceCompat.startForeground(
                            this,
                            NOTIFICATION_ID,
                            notification,
                            ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE
                        )
                    } else {
                        startForeground(NOTIFICATION_ID, notification)
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "startForeground error: ${e.message}")
                }

                isRunning = true
                isPausedForExternalInput = false
                acquireWakeLock()
                scheduleRecognizerRestart(400L)
            }
        }

        return START_STICKY
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "خدمة النداء الصوتي لكوتش زتونة",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "استماع مستمر لنداء كوتش زتونة للرد الفوري حتى والشاشة مغلقة"
                setShowBadge(false)
            }
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager
            manager?.createNotificationChannel(channel)
        }
    }

    private fun buildForegroundNotification(): Notification {
        val openIntent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra(MainActivity.EXTRA_AUTO_LISTEN, true)
            putExtra(MainActivity.EXTRA_WAKE_TRIGGER, true)
        }
        val openPending = PendingIntent.getActivity(
            this,
            301,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val stopIntent = Intent(this, WakeWordService::class.java).apply {
            action = ACTION_STOP
        }
        val stopPending = PendingIntent.getService(
            this,
            302,
            stopIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("🎙️ كوتش زتونة: سامعك ومستنيك دائماً")
            .setContentText("انده 'يا كوتش' أو 'يا زتونة' في أي وقت وسأرد عليك فوراً")
            .setSmallIcon(R.mipmap.ic_launcher)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setContentIntent(openPending)
            .addAction(R.mipmap.ic_launcher, "تحدث الآن 🗣️", openPending)
            .addAction(R.mipmap.ic_launcher, "إيقاف الاستماع ⏹️", stopPending)
            .build()
    }

    private fun acquireWakeLock() {
        if (wakeLock == null) {
            try {
                val pm = getSystemService(Context.POWER_SERVICE) as? PowerManager
                wakeLock = pm?.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "Zatoona:WakeWordServiceWakeLock")
                wakeLock?.setReferenceCounted(false)
                wakeLock?.acquire()
                Log.d(TAG, "Partial WakeLock acquired for continuous listening")
            } catch (e: Exception) {
                Log.e(TAG, "Failed to acquire WakeLock: ${e.message}")
            }
        }
    }

    private fun releaseWakeLock() {
        try {
            if (wakeLock?.isHeld == true) {
                wakeLock?.release()
                Log.d(TAG, "Partial WakeLock released")
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error releasing WakeLock: ${e.message}")
        }
        wakeLock = null
    }

    private fun initTextToSpeech() {
        try {
            textToSpeech = TextToSpeech(this) { status ->
                if (status == TextToSpeech.SUCCESS) {
                    val egLocale = Locale("ar", "EG")
                    val res = textToSpeech?.setLanguage(egLocale)
                    if (res == TextToSpeech.LANG_MISSING_DATA || res == TextToSpeech.LANG_NOT_SUPPORTED) {
                        textToSpeech?.setLanguage(Locale("ar"))
                    }
                    textToSpeech?.setSpeechRate(1.05f)
                    textToSpeech?.setPitch(1.0f)
                    isTtsReady = true

                    textToSpeech?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                        override fun onStart(utteranceId: String?) {}
                        override fun onDone(utteranceId: String?) {
                            Log.d(TAG, "TTS playback finished: $utteranceId")
                            // Resume listening after coach finishes speaking
                            mainHandler.postDelayed({
                                resumeListening()
                            }, 500L)
                        }
                        override fun onError(utteranceId: String?) {
                            mainHandler.postDelayed({
                                resumeListening()
                            }, 500L)
                        }
                    })
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "initTextToSpeech error: ${e.message}")
        }
    }

    private fun scheduleRecognizerRestart(delayMs: Long) {
        if (!isRunning || isPausedForExternalInput) return
        mainHandler.removeCallbacks(restartRecognizerRunnable)
        mainHandler.postDelayed(restartRecognizerRunnable, delayMs)
    }

    private val restartRecognizerRunnable = Runnable {
        startRecognizer()
    }

    private fun startRecognizer() {
        if (!isRunning || isPausedForExternalInput) return

        try {
            stopRecognizer()

            if (!SpeechRecognizer.isRecognitionAvailable(this)) {
                Log.w(TAG, "Speech recognition not available on this device")
                return
            }

            speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this).apply {
                setRecognitionListener(object : RecognitionListener {
                    override fun onReadyForSpeech(params: Bundle?) {
                        Log.d(TAG, "Listening for wake word...")
                    }

                    override fun onBeginningOfSpeech() {}
                    override fun onRmsChanged(rmsdB: Float) {}
                    override fun onBufferReceived(buffer: ByteArray?) {}
                    override fun onEndOfSpeech() {}

                    override fun onError(error: Int) {
                        Log.d(TAG, "Recognizer error code: $error")
                        if (!isRunning || isPausedForExternalInput) return

                        val delay = when (error) {
                            SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> 600L
                            SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> 2000L
                            SpeechRecognizer.ERROR_AUDIO -> 1000L
                            else -> 250L // Fast loop restart for timeout or no-match
                        }
                        scheduleRecognizerRestart(delay)
                    }

                    override fun onResults(results: Bundle?) {
                        val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION) ?: arrayListOf()
                        Log.d(TAG, "Recognizer onResults: $matches")

                        var matched = false
                        for (raw in matches) {
                            val normalized = normalizeArabic(raw)
                            if (isWakeWordMatch(normalized)) {
                                matched = true
                                handleWakeWordDetected(raw)
                                break
                            }
                        }

                        if (!matched) {
                            // No wake word in this utterance; silently restart continuous listening
                            scheduleRecognizerRestart(200L)
                        }
                    }

                    override fun onPartialResults(partialResults: Bundle?) {
                        val matches = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION) ?: arrayListOf()
                        for (raw in matches) {
                            val normalized = normalizeArabic(raw)
                            if (isWakeWordMatch(normalized)) {
                                Log.i(TAG, "Wake word matched in partial results: $raw")
                                stopRecognizer()
                                handleWakeWordDetected(raw)
                                break
                            }
                        }
                    }

                    override fun onEvent(eventType: Int, params: Bundle?) {}
                })
            }

            val recognizerIntent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                putExtra(RecognizerIntent.EXTRA_LANGUAGE, "ar-EG")
                putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
                putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
                putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, packageName)
            }

            speechRecognizer?.startListening(recognizerIntent)
        } catch (e: Exception) {
            Log.e(TAG, "startRecognizer error: ${e.message}")
            scheduleRecognizerRestart(1000L)
        }
    }

    private fun stopRecognizer() {
        try {
            speechRecognizer?.stopListening()
            speechRecognizer?.cancel()
            speechRecognizer?.destroy()
        } catch (e: Exception) {
            Log.e(TAG, "stopRecognizer error: ${e.message}")
        } finally {
            speechRecognizer = null
        }
    }

    private fun handleWakeWordDetected(rawSpokenText: String) {
        Log.i(TAG, "Wake word detected successfully: '$rawSpokenText'")

        // 1. Pause continuous listener so it doesn't transcribe our own voice or prompt
        isPausedForExternalInput = true
        stopRecognizer()

        // 2. Immediate Haptic Buzz (double pulse)
        triggerWakeHaptic()

        // 3. Wake up screen and acquire screen lock
        turnScreenOn()

        // 4. Extract command if user said something alongside the wake word (e.g. "يا كوتش سجلت كوباية مية")
        val cleanCommand = extractCommand(rawSpokenText)

        // 5. Determine if MainActivity is already running in foreground
        val mainActive = MainActivity.isForeground && MainActivity.instance != null

        if (mainActive) {
            // Already active on screen: forward directly to web UI
            MainActivity.instance?.handleWakeWordFromService(cleanCommand)
            // Schedule resume in 4 seconds
            mainHandler.postDelayed({
                isPausedForExternalInput = false
                scheduleRecognizerRestart(300L)
            }, 4000L)
        } else {
            // Screen locked, screen off, or app in background:
            // Speak instant spoken feedback aloud so user knows Coach heard them
            if (cleanCommand.isNotBlank()) {
                speakCoachAloud("من عينيا يا بطل، بنفذلك حالاً")
            } else {
                speakCoachAloud("أيوه يا وحش! أنا معاك وسامعك، اؤمرني")
            }

            // Launch MainActivity onto lock screen
            launchMainActivityOnLockScreen(cleanCommand)

            // Resume listening safely after speaking/handling
            mainHandler.postDelayed({
                isPausedForExternalInput = false
                scheduleRecognizerRestart(500L)
            }, 5500L)
        }
    }

    private fun triggerWakeHaptic() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vm = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
                val effect = VibrationEffect.createWaveform(longArrayOf(0, 100, 50, 120), -1)
                vm?.defaultVibrator?.vibrate(effect)
            } else {
                @Suppress("DEPRECATION")
                val v = getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    val effect = VibrationEffect.createWaveform(longArrayOf(0, 100, 50, 120), -1)
                    v?.vibrate(effect)
                } else {
                    @Suppress("DEPRECATION")
                    v?.vibrate(longArrayOf(0, 100, 50, 120), -1)
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "triggerWakeHaptic error: ${e.message}")
        }
    }

    private fun turnScreenOn() {
        try {
            val pm = getSystemService(Context.POWER_SERVICE) as? PowerManager
            @Suppress("DEPRECATION")
            val screenWakeLock = pm?.newWakeLock(
                PowerManager.SCREEN_BRIGHT_WAKE_LOCK or
                        PowerManager.ACQUIRE_CAUSES_WAKEUP or
                        PowerManager.ON_AFTER_RELEASE,
                "Zatoona:WakeScreenLock"
            )
            screenWakeLock?.acquire(4500L)
        } catch (e: Exception) {
            Log.e(TAG, "turnScreenOn error: ${e.message}")
        }
    }

    private fun speakCoachAloud(text: String) {
        if (!isTtsReady || textToSpeech == null) return
        try {
            val params = Bundle().apply {
                putFloat(TextToSpeech.Engine.KEY_PARAM_VOLUME, 1.0f)
            }
            textToSpeech?.speak(
                text,
                TextToSpeech.QUEUE_FLUSH,
                params,
                "ZatoonaWakeService_${System.currentTimeMillis()}"
            )
        } catch (e: Exception) {
            Log.e(TAG, "speakCoachAloud error: ${e.message}")
        }
    }

    private fun launchMainActivityOnLockScreen(cleanCommand: String) {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or
                    Intent.FLAG_ACTIVITY_CLEAR_TOP or
                    Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra(MainActivity.EXTRA_AUTO_LISTEN, true)
            putExtra(MainActivity.EXTRA_WAKE_TRIGGER, true)
            putExtra(MainActivity.EXTRA_WAKE_COMMAND, cleanCommand)
        }
        try {
            startActivity(intent)
        } catch (e: Exception) {
            Log.e(TAG, "Error launching MainActivity from WakeWordService: ${e.message}")
        }
    }

    private fun normalizeArabic(raw: String): String {
        return raw.lowercase()
            .replace(Regex("[\\p{Mn}]"), "") // remove tashkeel/diacritics
            .replace("أ", "ا")
            .replace("إ", "ا")
            .replace("آ", "ا")
            .replace("ة", "ه")
            .replace("ى", "ي")
            .trim()
    }

    private fun isWakeWordMatch(normalized: String): Boolean {
        val keywords = listOf(
            "كوتش", "يا كوتش", "ياكوتش",
            "زتونه", "يازتونه", "يا زتونه",
            "زيتونه", "يازيتونه", "يا زيتونه"
        )
        for (kw in keywords) {
            if (normalized.contains(kw)) return true
        }
        return false
    }

    private fun extractCommand(rawText: String): String {
        return rawText.replace(
            Regex("^(يا\\s*كوتش|كوتش|يا\\s*زتون[هة]|زتون[هة]|يا\\s*زيتون[هة]|زيتون[هة]|ياكوتش|يازتون[هة]|يازيتون[هة])\\s*", RegexOption.IGNORE_CASE),
            ""
        ).trim()
    }

    private fun stopListeningAndSelf() {
        isRunning = false
        isPausedForExternalInput = false
        mainHandler.removeCallbacks(restartRecognizerRunnable)
        stopRecognizer()
        releaseWakeLock()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    override fun onDestroy() {
        instance = null
        isRunning = false
        isPausedForExternalInput = false
        mainHandler.removeCallbacks(restartRecognizerRunnable)
        stopRecognizer()
        releaseWakeLock()
        try {
            textToSpeech?.stop()
            textToSpeech?.shutdown()
        } catch (e: Exception) {}
        super.onDestroy()
    }
}

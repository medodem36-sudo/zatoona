package com.zatoona.app



import android.Manifest

import android.content.Context

import android.hardware.Sensor

import android.hardware.SensorEvent

import android.hardware.SensorEventListener

import android.hardware.SensorManager

import android.speech.RecognitionListener

import android.speech.RecognizerIntent

import android.speech.SpeechRecognizer

import android.os.Handler

import android.os.Looper

import android.speech.tts.TextToSpeech

import android.view.WindowManager

import java.util.Locale



import android.util.Log

import android.annotation.SuppressLint

import android.content.Intent

import android.content.pm.PackageManager

import android.media.session.MediaSession

import android.media.session.PlaybackState

import android.net.Uri

import android.view.KeyEvent

import android.app.KeyguardManager
import android.os.Build

import android.os.Bundle

import android.webkit.JsPromptResult

import android.webkit.JsResult

import android.webkit.PermissionRequest

import android.webkit.WebChromeClient

import android.webkit.WebResourceRequest

import android.webkit.WebResourceResponse

import android.webkit.WebSettings

import android.webkit.WebView

import android.webkit.WebViewClient

import android.widget.EditText

import androidx.activity.OnBackPressedCallback

import androidx.activity.result.contract.ActivityResultContracts

import androidx.appcompat.app.AlertDialog

import androidx.appcompat.app.AppCompatActivity

import androidx.core.content.ContextCompat



class MainActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_AUTO_LISTEN = "com.zatoona.app.EXTRA_AUTO_LISTEN"
        const val EXTRA_WAKE_TRIGGER = "com.zatoona.app.EXTRA_WAKE_TRIGGER"
        const val EXTRA_WAKE_COMMAND = "com.zatoona.app.EXTRA_WAKE_COMMAND"

        @Volatile
        var instance: MainActivity? = null
            private set

        @Volatile
        var isForeground: Boolean = false
            private set
    }





    private lateinit var webView: WebView

    private val assetLoader by lazy { ZatoonaAssetLoader.build(this) }

    private val bridge by lazy { ZatoonaBridge(this) }



    private var pendingTargetMode: String? = null

    private var isPageLoaded = false

    private var mediaSession: MediaSession? = null

    private var textToSpeech: TextToSpeech? = null

    private var isTtsReady = false

    private val mainHandler = Handler(Looper.getMainLooper())

    private var isWakeWordListening = false



    private val audioPermissionLauncher = registerForActivityResult(

        ActivityResultContracts.RequestPermission()

    ) { _ -> }



    private fun requestAudioPermissionIfNeeded() {

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)

            != PackageManager.PERMISSION_GRANTED

        ) {

            audioPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO)

        }

    }



    private val notificationPermissionLauncher = registerForActivityResult(

        ActivityResultContracts.RequestPermission()

    ) { isGranted ->

        // Permission result handled gracefully

    }



    @SuppressLint("SetJavaScriptEnabled")

    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        instance = this



        webView = WebView(this)

        webView.isVerticalScrollBarEnabled = false

        webView.isHorizontalScrollBarEnabled = false

        setContentView(webView)



        configureWebSettings(webView.settings)

        configureWebViewClient()

        configureWebChromeClient()

        attachBridge()

        handleBackNavigation()

        requestNotificationPermissionIfNeeded()

        requestAudioPermissionIfNeeded()

        setupMediaSession()

        initTextToSpeech()



        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1) {

            setShowWhenLocked(true)

            setTurnScreenOn(true)

        }



        handleNotificationIntent(intent)



        // Clear web resource cache so updated APK assets are immediately picked up

        webView.clearCache(true)



        // Load trusted local PWA bundle with cache-busting timestamp to bypass stale Service Worker match

        val entryUrl = "${ZatoonaAssetLoader.ENTRY_URL}?v=${System.currentTimeMillis()}"

        webView.loadUrl(entryUrl)

    }



    override fun onNewIntent(intent: Intent?) {

        super.onNewIntent(intent)

        setIntent(intent)

        handleNotificationIntent(intent)

    }



    private fun handleNotificationIntent(intent: Intent?) {

        if (intent == null) return

        val autoListen = intent.getBooleanExtra(EXTRA_AUTO_LISTEN, false)
        val wakeTrigger = intent.getBooleanExtra(EXTRA_WAKE_TRIGGER, false)
        val wakeCommand = intent.getStringExtra(EXTRA_WAKE_COMMAND)

        if (autoListen || wakeTrigger) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1) {
                setShowWhenLocked(true)
                setTurnScreenOn(true)
            }
            window.addFlags(
                WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON or
                WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON
            )
            val km = getSystemService(Context.KEYGUARD_SERVICE) as? KeyguardManager
            km?.requestDismissKeyguard(this, null)

            mainHandler.postDelayed({
                if (!wakeCommand.isNullOrBlank()) {
                    val jsonCmd = org.json.JSONObject.quote(wakeCommand)
                    webView.evaluateJavascript("""
                        (function(){
                            if(typeof openAiFullscreenChat === 'function') openAiFullscreenChat();
                            if(typeof window.onNativeWakeWordTriggered === 'function') {
                                window.onNativeWakeWordTriggered($jsonCmd);
                            } else if(typeof processAiUserPrompt === 'function') {
                                processAiUserPrompt($jsonCmd);
                            }
                        })()
                    """.trimIndent(), null)
                } else {
                    webView.evaluateJavascript("""
                        (function(){
                            if(typeof openAiFullscreenChat === 'function') openAiFullscreenChat();
                            if(typeof window.onNativeWakeWordTriggered === 'function') {
                                window.onNativeWakeWordTriggered('');
                            } else if(typeof toggleAiVoiceInput === 'function') {
                                setTimeout(toggleAiVoiceInput, 300);
                            }
                        })()
                    """.trimIndent(), null)
                }
            }, 350)
        }

        val mode = intent.getStringExtra(ZatoonaNotificationManager.EXTRA_MODE)

        if (!mode.isNullOrBlank() && ZatoonaBridge.ALLOWED_MODES.contains(mode.lowercase())) {

            pendingTargetMode = mode.lowercase()

            if (isPageLoaded) {

                dispatchPendingNavigation()

            }

        }

    }

    fun handleWakeWordFromService(cleanCommand: String) {
        runOnUiThread {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1) {
                setShowWhenLocked(true)
                setTurnScreenOn(true)
            }
            window.addFlags(
                WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON or
                WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON
            )
            val km = getSystemService(Context.KEYGUARD_SERVICE) as? KeyguardManager
            km?.requestDismissKeyguard(this, null)

            if (cleanCommand.isNotBlank()) {
                val jsonCmd = org.json.JSONObject.quote(cleanCommand)
                webView.evaluateJavascript("""
                    (function(){
                        if(typeof openAiFullscreenChat === 'function') openAiFullscreenChat();
                        if(typeof window.onNativeWakeWordTriggered === 'function') {
                            window.onNativeWakeWordTriggered($jsonCmd);
                        } else if(typeof processAiUserPrompt === 'function') {
                            processAiUserPrompt($jsonCmd);
                        }
                    })()
                """.trimIndent(), null)
            } else {
                webView.evaluateJavascript("""
                    (function(){
                        if(typeof openAiFullscreenChat === 'function') openAiFullscreenChat();
                        if(typeof window.onNativeWakeWordTriggered === 'function') {
                            window.onNativeWakeWordTriggered('');
                        } else if(typeof toggleAiVoiceInput === 'function') {
                            setTimeout(toggleAiVoiceInput, 300);
                        }
                    })()
                """.trimIndent(), null)
            }
        }
    }



    private fun dispatchPendingNavigation() {

        val mode = pendingTargetMode ?: return

        pendingTargetMode = null

        val js = "if(typeof routeNotificationClick==='function'){routeNotificationClick({mode:'$mode'});}"

        webView.post {

            webView.evaluateJavascript(js, null)

        }

    }



    private fun requestNotificationPermissionIfNeeded() {

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {

            val status = ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)

            if (status != PackageManager.PERMISSION_GRANTED) {

                notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)

            }

        }

    }



    @SuppressLint("SetJavaScriptEnabled")

    private fun configureWebSettings(settings: WebSettings) {

        settings.apply {

            javaScriptEnabled = true

            domStorageEnabled = true

            databaseEnabled = true



            // Security hardening: strictly disable local file URLs and cross-origin file access

            allowFileAccess = false

            allowContentAccess = false

            allowFileAccessFromFileURLs = false

            allowUniversalAccessFromFileURLs = false



            // Responsive layout defaults

            useWideViewPort = true

            loadWithOverviewMode = true

            builtInZoomControls = false

            displayZoomControls = false



            cacheMode = WebSettings.LOAD_DEFAULT

        }

    }



    private fun configureWebViewClient() {

        webView.webViewClient = object : WebViewClient() {

            override fun shouldInterceptRequest(

                view: WebView?,

                request: WebResourceRequest?

            ): WebResourceResponse? {

                val url = request?.url ?: return null

                return assetLoader.shouldInterceptRequest(url)

            }



            override fun onPageFinished(view: WebView?, url: String?) {

                super.onPageFinished(view, url)

                isPageLoaded = true

                dispatchPendingNavigation()

            }



            override fun shouldOverrideUrlLoading(

                view: WebView?,

                request: WebResourceRequest?

            ): Boolean {

                val url = request?.url?.toString() ?: return false

                if (ZatoonaAssetLoader.isTrustedUrl(url)) {

                    // Internal trusted navigation: allow WebView to handle

                    return false

                }

                // External link: open in system browser, never expose native bridge

                try {

                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))

                    startActivity(intent)

                } catch (e: Exception) {

                    // Gracefully ignore unresolvable intents

                }

                return true

            }

        }

    }



    private fun configureWebChromeClient() {

        webView.webChromeClient = object : WebChromeClient() {

            override fun onPermissionRequest(request: PermissionRequest?) {

                runOnUiThread {

                    request?.grant(request.resources)

                }

            }



            override fun onJsAlert(

                view: WebView?,

                url: String?,

                message: String?,

                result: JsResult?

            ): Boolean {

                if (isFinishing || isDestroyed) {

                    result?.cancel()

                    return true

                }

                AlertDialog.Builder(this@MainActivity)

                    .setTitle(R.string.app_name)

                    .setMessage(message ?: "")

                    .setPositiveButton(android.R.string.ok) { _, _ -> result?.confirm() }

                    .setOnCancelListener { result?.cancel() }

                    .show()

                return true

            }



            override fun onJsConfirm(

                view: WebView?,

                url: String?,

                message: String?,

                result: JsResult?

            ): Boolean {

                if (isFinishing || isDestroyed) {

                    result?.cancel()

                    return true

                }

                AlertDialog.Builder(this@MainActivity)

                    .setTitle(R.string.app_name)

                    .setMessage(message ?: "")

                    .setPositiveButton("نعم") { _, _ -> result?.confirm() }

                    .setNegativeButton("إلغاء") { _, _ -> result?.cancel() }

                    .setOnCancelListener { result?.cancel() }

                    .show()

                return true

            }



            override fun onJsPrompt(

                view: WebView?,

                url: String?,

                message: String?,

                defaultValue: String?,

                result: JsPromptResult?

            ): Boolean {

                if (isFinishing || isDestroyed) {

                    result?.cancel()

                    return true

                }

                val input = EditText(this@MainActivity).apply {

                    setText(defaultValue ?: "")

                    setSelection(text.length)

                }

                AlertDialog.Builder(this@MainActivity)

                    .setTitle(R.string.app_name)

                    .setMessage(message ?: "")

                    .setView(input)

                    .setPositiveButton(android.R.string.ok) { _, _ ->

                        result?.confirm(input.text.toString())

                    }

                    .setNegativeButton(android.R.string.cancel) { _, _ ->

                        result?.cancel()

                    }

                    .setOnCancelListener { result?.cancel() }

                    .show()

                return true

            }

        }

    }



        // 591. Bluetooth Headset Media Button Capture

    private fun setupMediaSession() {

        try {

            mediaSession = MediaSession(this, "ZatoonaMediaSession").apply {

                setCallback(object : MediaSession.Callback() {

                    override fun onMediaButtonEvent(mediaButtonIntent: Intent): Boolean {

                        val keyEvent = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {

                            mediaButtonIntent.getParcelableExtra(Intent.EXTRA_KEY_EVENT, KeyEvent::class.java)

                        } else {

                            @Suppress("DEPRECATION")

                            mediaButtonIntent.getParcelableExtra(Intent.EXTRA_KEY_EVENT)

                        }

                        if (keyEvent?.action == KeyEvent.ACTION_UP) {

                            when (keyEvent.keyCode) {

                                KeyEvent.KEYCODE_HEADSETHOOK,

                                KeyEvent.KEYCODE_MEDIA_PLAY,

                                KeyEvent.KEYCODE_MEDIA_PAUSE,

                                KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE -> {

                                    runOnUiThread {

                                        webView.evaluateJavascript(

                                            "if(typeof window.onNativeMediaButtonPressed === 'function'){ window.onNativeMediaButtonPressed(); }",

                                            null

                                        )

                                    }

                                    return true

                                }

                            }

                        }

                        return super.onMediaButtonEvent(mediaButtonIntent)

                    }

                })

                setFlags(MediaSession.FLAG_HANDLES_MEDIA_BUTTONS or MediaSession.FLAG_HANDLES_TRANSPORT_CONTROLS)

                val state = PlaybackState.Builder()

                    .setActions(PlaybackState.ACTION_PLAY_PAUSE or PlaybackState.ACTION_PLAY)

                    .setState(PlaybackState.STATE_PLAYING, 0, 1.0f)

                    .build()

                setPlaybackState(state)

                isActive = true

            }

        } catch (e: Exception) {

            // Gracefully ignore media session initialization error

        }

    }



    private fun attachBridge() {

        // Expose JavaScript bridge only to the trusted local bundle

        webView.addJavascriptInterface(bridge, ZatoonaBridge.BRIDGE_NAME)

    }



    private fun handleBackNavigation() {

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {

            override fun handleOnBackPressed() {

                val dismissModalJs = """

                    (function(){

                        var modal = document.querySelector('.ai-chat-fullscreen-overlay.open, .theme-modal-overlay.open, .p5-modal-overlay.open, .p4-modal-overlay.open, .gym-modal-overlay.open, .drawer-overlay.open, .img-viewer-overlay.open, .backup-crypto-overlay.open, .battery-guide-overlay.open, .ex-img-modal-overlay.open, .str-modal-overlay.open');

                        if (modal) {

                            modal.classList.remove('open', 'active');

                            return 'closed';

                        }

                        return 'none';

                    })()

                """.trimIndent()



                webView.evaluateJavascript(dismissModalJs) { res ->

                    if (res != null && res.contains("closed")) {

                        return@evaluateJavascript

                    }

                    if (webView.canGoBack()) {

                        webView.goBack()

                    } else {

                        isEnabled = false

                        onBackPressedDispatcher.onBackPressed()

                    }

                }

            }

        })

    }



    private var speechRecognizer: SpeechRecognizer? = null

    private var sensorManager: SensorManager? = null

    private var accelerometer: Sensor? = null

    private var isFaceDown = false

    private var lastFlipTime = 0L



    private val flipSensorListener = object : SensorEventListener {

        override fun onSensorChanged(event: SensorEvent?) {

            if (event?.sensor?.type == Sensor.TYPE_ACCELEROMETER) {

                val z = event.values[2]

                if (z < -6.5) {

                    val now = System.currentTimeMillis()

                    if (!isFaceDown && (now - lastFlipTime > 1500)) {

                        isFaceDown = true

                        lastFlipTime = now

                        runOnUiThread {

                            webView.evaluateJavascript("window.onNativeFlipGesture && window.onNativeFlipGesture();", null)

                        }

                    }

                } else if (z > 2.0) {

                    isFaceDown = false

                }

            }

        }

        override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    }



    override fun onResume() {
        super.onResume()
        isForeground = true

        try {
            if (FloatingStudyBubbleService.isRunning && FloatingStudyBubbleService.isBubbleVisibleOnScreen) {
                val hideIntent = Intent(this, FloatingStudyBubbleService::class.java).apply {
                    action = FloatingStudyBubbleService.ACTION_HIDE_BUBBLE
                }
                startService(hideIntent)
            }
        } catch (e: Exception) {}

        try {

            sensorManager = getSystemService(Context.SENSOR_SERVICE) as? SensorManager

            accelerometer = sensorManager?.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)

            accelerometer?.let {

                sensorManager?.registerListener(flipSensorListener, it, SensorManager.SENSOR_DELAY_UI)

            }

        } catch (e: Exception) {}

    }



    override fun onPause() {
        isForeground = false
        super.onPause()

        try {
            if (FloatingStudyBubbleService.isRunning && !FloatingStudyBubbleService.wasDismissedToBackground) {
                val bubbleIntent = Intent(this, FloatingStudyBubbleService::class.java).apply {
                    action = FloatingStudyBubbleService.ACTION_SHOW_BUBBLE
                }
                startService(bubbleIntent)
            }
        } catch (e: Exception) {}

        try {

            sensorManager?.unregisterListener(flipSensorListener)

        } catch (e: Exception) {}

    }



    private fun initTextToSpeech(onReady: (() -> Unit)? = null) {

        try {

            textToSpeech = TextToSpeech(this) { status ->

                if (status == TextToSpeech.SUCCESS) {

                    val egLocale = Locale("ar", "EG")

                    val res = textToSpeech?.setLanguage(egLocale)

                    if (res == TextToSpeech.LANG_MISSING_DATA || res == TextToSpeech.LANG_NOT_SUPPORTED) {

                        textToSpeech?.setLanguage(Locale("ar"))

                    }

                    textToSpeech?.setSpeechRate(1.0f)

                    textToSpeech?.setPitch(1.0f)

                    isTtsReady = true

                    Log.i("MainActivity", "Native Arabic TTS initialized successfully.")

                    onReady?.invoke()

                }

            }

        } catch (e: Exception) {

            Log.e("MainActivity", "Failed to init TextToSpeech: ${e.message}")

        }

    }



    fun speakTextNative(text: String): Boolean {

        if (!isTtsReady || textToSpeech == null) {

            initTextToSpeech {

                speakTextNative(text)

            }

            return true

        }

        runOnUiThread {

            if (isTtsReady && textToSpeech != null) {

                try {

                    textToSpeech?.stop()

                    val params = Bundle()

                    params.putFloat(TextToSpeech.Engine.KEY_PARAM_VOLUME, 1.0f)

                    textToSpeech?.speak(text, TextToSpeech.QUEUE_FLUSH, params, "ZatoonaCoachUtterance_${System.currentTimeMillis()}")

                } catch (e: Exception) {

                    Log.e("MainActivity", "speakTextNative error: ${e.message}")

                }

            }

        }

        return true

    }



    fun stopSpeakingNative() {

        runOnUiThread {

            try {

                textToSpeech?.stop()

            } catch (e: Exception) {}

        }

    }



    fun setContinuousWakeWord(enabled: Boolean) {

        runOnUiThread {

            isWakeWordListening = enabled

            if (enabled) {

                window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

                startNativeSpeechRecognizer(isWakeWord = true)

            } else {

                window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

                try {

                    speechRecognizer?.stopListening()

                    speechRecognizer?.destroy()

                    speechRecognizer = null

                } catch (e: Exception) {}

                WakeWordService.resumeListening()
                                    webView.evaluateJavascript("window.onNativeSpeechStateChange && window.onNativeSpeechStateChange('idle');", null)

            }

        }

    }



    fun startNativeSpeechRecognizer(isWakeWord: Boolean = false) {

        runOnUiThread {

            if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)

                != PackageManager.PERMISSION_GRANTED) {

                requestAudioPermissionIfNeeded()

                return@runOnUiThread

            }



            if (!SpeechRecognizer.isRecognitionAvailable(this)) {

                return@runOnUiThread

            }



            try {

                speechRecognizer?.destroy()

                speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this).apply {

                    setRecognitionListener(object : RecognitionListener {

                        override fun onReadyForSpeech(params: Bundle?) {

                            if (!isWakeWord) {

                                webView.evaluateJavascript("window.onNativeSpeechStateChange && window.onNativeSpeechStateChange('listening');", null)

                            }

                        }

                        override fun onBeginningOfSpeech() {}

                        override fun onRmsChanged(rmsdB: Float) {}

                        override fun onBufferReceived(buffer: ByteArray?) {}

                        override fun onEndOfSpeech() {

                            if (!isWakeWord) {

                                webView.evaluateJavascript("window.onNativeSpeechStateChange && window.onNativeSpeechStateChange('processing');", null)

                            }

                        }

                        override fun onError(error: Int) {

                            if (isWakeWord && isWakeWordListening && !isFinishing && !isDestroyed) {

                                mainHandler.postDelayed({

                                    if (isWakeWordListening && !isFinishing && !isDestroyed) {

                                        startNativeSpeechRecognizer(isWakeWord = true)

                                    }

                                }, 500)

                            } else {

                                WakeWordService.resumeListening()
                                webView.evaluateJavascript("window.onNativeSpeechStateChange && window.onNativeSpeechStateChange('error');", null)

                            }

                        }

                        override fun onResults(results: Bundle?) {

                            val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)

                            val text = matches?.firstOrNull() ?: ""

                            val cleanText = text.trim()



                            if (isWakeWord) {

                                val lower = cleanText.lowercase()

                                val isWakeMatch = lower.contains("كوتش") || lower.contains("زتونه") || lower.contains("زتونة")

                                if (isWakeMatch) {

                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1) {

                                        setShowWhenLocked(true)

                                        setTurnScreenOn(true)

                                    }

                                    val jsonText = org.json.JSONObject.quote(cleanText)

                                    webView.evaluateJavascript("window.onNativeWakeWordTriggered && window.onNativeWakeWordTriggered($jsonText);", null)

                                } else {

                                    // Silent loop restart for wake-word

                                    mainHandler.postDelayed({

                                        if (isWakeWordListening && !isFinishing && !isDestroyed) {

                                            startNativeSpeechRecognizer(isWakeWord = true)

                                        }

                                    }, 300)

                                }

                            } else {

                                // Explicit mic dictation: ALWAYS forward what the user said directly!

                                if (cleanText.isNotBlank()) {

                                    val jsonText = org.json.JSONObject.quote(cleanText)

                                    webView.evaluateJavascript("window.onNativeSpeechResult && window.onNativeSpeechResult($jsonText);", null)

                                } else {

                                    webView.evaluateJavascript("window.onNativeSpeechStateChange && window.onNativeSpeechStateChange('idle');", null)

                                }

                            }

                        }

                        override fun onPartialResults(partialResults: Bundle?) {}

                        override fun onEvent(eventType: Int, params: Bundle?) {}

                    })

                }



                val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {

                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)

                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, "ar-EG")

                    putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)

                }

                WakeWordService.pauseListening()
                speechRecognizer?.startListening(intent)

            } catch (e: Exception) {

                Log.e("MainActivity", "Speech recognition start failed: ${e.message}")

            }

        }

    }



    override fun onDestroy() {

        try {

            speechRecognizer?.destroy()

        } catch (e: Exception) {}

        try {

            textToSpeech?.stop()

            textToSpeech?.shutdown()

        } catch (e: Exception) {}

        mediaSession?.release()

        mediaSession = null

        webView.removeJavascriptInterface(ZatoonaBridge.BRIDGE_NAME)

        webView.destroy()

        if (instance === this) instance = null
        isForeground = false
        super.onDestroy()

    }

}

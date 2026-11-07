package com.zatoona.app

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.PackageManager
import android.media.session.MediaSession
import android.media.session.PlaybackState
import android.net.Uri
import android.view.KeyEvent
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

    private lateinit var webView: WebView
    private val assetLoader by lazy { ZatoonaAssetLoader.build(this) }
    private val bridge by lazy { ZatoonaBridge(this) }

    private var pendingTargetMode: String? = null
    private var isPageLoaded = false
    private var mediaSession: MediaSession? = null

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
        val mode = intent.getStringExtra(ZatoonaNotificationManager.EXTRA_MODE)
        if (!mode.isNullOrBlank() && ZatoonaBridge.ALLOWED_MODES.contains(mode.lowercase())) {
            pendingTargetMode = mode.lowercase()
            if (isPageLoaded) {
                dispatchPendingNavigation()
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

    override fun onDestroy() {
        mediaSession?.release()
        mediaSession = null
        webView.removeJavascriptInterface(ZatoonaBridge.BRIDGE_NAME)
        webView.destroy()
        super.onDestroy()
    }
}

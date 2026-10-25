package com.zatoona.app

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private val assetLoader by lazy { ZatoonaAssetLoader.build(this) }
    private val bridge by lazy { ZatoonaBridge(this) }

    private var pendingTargetMode: String? = null
    private var isPageLoaded = false

    private val notificationPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        // Permission result handled gracefully
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)
        setContentView(webView)

        configureWebSettings(webView.settings)
        configureWebViewClient()
        attachBridge()
        handleBackNavigation()
        requestNotificationPermissionIfNeeded()

        handleNotificationIntent(intent)

        // Load trusted local PWA bundle
        webView.loadUrl(ZatoonaAssetLoader.ENTRY_URL)
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

    private fun attachBridge() {
        // Expose JavaScript bridge only to the trusted local bundle
        webView.addJavascriptInterface(bridge, ZatoonaBridge.BRIDGE_NAME)
    }

    private fun handleBackNavigation() {
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) {
                    webView.goBack()
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })
    }

    override fun onDestroy() {
        webView.removeJavascriptInterface(ZatoonaBridge.BRIDGE_NAME)
        webView.destroy()
        super.onDestroy()
    }
}

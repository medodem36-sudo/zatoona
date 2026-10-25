package com.zatoona.app

import android.content.Context
import androidx.webkit.WebViewAssetLoader

/**
 * ZatoonaAssetLoader
 * Configures a secure, HTTPS-style virtual domain for local WebView asset resolution
 * using AndroidX WebViewAssetLoader. This prevents mixed-content and CORS errors while
 * avoiding dangerous file:/// URLs.
 */
object ZatoonaAssetLoader {
    const val TRUSTED_DOMAIN = "appassets.androidplatform.net"
    const val TRUSTED_ORIGIN = "https://appassets.androidplatform.net"
    const val ENTRY_URL = "https://appassets.androidplatform.net/assets/index.html"

    fun build(context: Context): WebViewAssetLoader {
        return WebViewAssetLoader.Builder()
            .setDomain(TRUSTED_DOMAIN)
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(context))
            .build()
    }

    fun isTrustedUrl(url: String?): Boolean {
        if (url.isNullOrBlank()) return false
        return url.startsWith(TRUSTED_ORIGIN)
    }
}

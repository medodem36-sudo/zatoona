# -*- coding: utf-8 -*-
"""
Create Phase 13.4B1 Android Scaffold
"""
import os

BASE_DIR = r"C:\Users\Lenovo\Documents\GitHub\zatoona\android"

# List of files to create with their contents
files = {}

# 1. settings.gradle.kts
files["settings.gradle.kts"] = """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "Zatoona"
include(":app")
"""

# 2. build.gradle.kts (root)
files["build.gradle.kts"] = """// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    id("com.android.application") version "8.2.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.22" apply false
}
"""

# 3. gradle.properties
files["gradle.properties"] = """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
kotlin.code.style=official
"""

# 4. gradle-wrapper.properties
files[os.path.join("gradle", "wrapper", "gradle-wrapper.properties")] = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.5-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""

# 5. app/build.gradle.kts
files[os.path.join("app", "build.gradle.kts")] = """plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.zatoona.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.zatoona.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
        debug {
            isMinifyEnabled = false
            applicationIdSuffix = ".debug"
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.webkit:webkit:1.10.0")

    testImplementation("junit:junit:4.13.2")
    testImplementation("org.json:json:20231013")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}
"""

# 6. app/proguard-rules.pro
files[os.path.join("app", "proguard-rules.pro")] = """# Keep JavaScript interface methods from being stripped or obfuscated
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep Zatoona bridge classes
-keep class com.zatoona.app.ZatoonaBridge { *; }
"""

# 7. app/src/main/AndroidManifest.xml
files[os.path.join("app", "src", "main", "AndroidManifest.xml")] = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- Network state check for offline awareness -->
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.Zatoona"
        android:networkSecurityConfig="@xml/network_security_config"
        android:usesCleartextTraffic="false">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|screenLayout|keyboardHidden"
            android:theme="@style/Theme.Zatoona.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>
"""

# 8. app/src/main/res/xml/network_security_config.xml
files[os.path.join("app", "src", "main", "res", "xml", "network_security_config.xml")] = """<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Strictly forbid cleartext (HTTP) traffic -->
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
</network-security-config>
"""

# 9. app/src/main/res/values/strings.xml
files[os.path.join("app", "src", "main", "res", "values", "strings.xml")] = """<resources>
    <string name="app_name">زتونة</string>
</resources>
"""

# 10. app/src/main/res/values/themes.xml
files[os.path.join("app", "src", "main", "res", "values", "themes.xml")] = """<resources>
    <style name="Theme.Zatoona" parent="Theme.MaterialComponents.DayNight">
        <item name="colorPrimary">#2D6A4F</item>
        <item name="android:statusBarColor">#FAF9F6</item>
        <item name="android:windowLightStatusBar">true</item>
    </style>
    <style name="Theme.Zatoona.NoActionBar">
        <item name="windowActionBar">false</item>
        <item name="windowNoTitle">true</item>
        <item name="android:statusBarColor">#FAF9F6</item>
        <item name="android:windowLightStatusBar">true</item>
    </style>
</resources>
"""

# 11. app/src/main/assets/.gitkeep
files[os.path.join("app", "src", "main", "assets", ".gitkeep")] = ""

# 12. app/src/main/java/com/zatoona/app/ZatoonaAssetLoader.kt
files[os.path.join("app", "src", "main", "java", "com", "zatoona", "app", "ZatoonaAssetLoader.kt")] = """package com.zatoona.app

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
"""

# 13. app/src/main/java/com/zatoona/app/ZatoonaBridge.kt
files[os.path.join("app", "src", "main", "java", "com", "zatoona", "app", "ZatoonaBridge.kt")] = """package com.zatoona.app

import android.content.Context
import android.content.SharedPreferences
import android.webkit.JavascriptInterface
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject

/**
 * ZatoonaBridge
 * Secure, versioned JavaScript bridge contract for Zatoona native shell.
 *
 * Responsibilities in Phase 13.4B1:
 * - Accepts upcoming alarm definitions from the PWA.
 * - Performs strict schema validation, length bounds checking, and type whitelisting.
 * - Stores validated alarms in local SharedPreferences for future AlarmManager scheduling.
 * - Provides safe, structured error responses without leaking private user data.
 *
 * Scope Boundary: Does NOT schedule native alarms or show notifications in this phase.
 */
class ZatoonaBridge(private val context: Context) {

    companion object {
        const val BRIDGE_NAME = "ZatoonaNativeBridge"
        const val SCHEMA_VERSION = "v1"
        const val PREFS_NAME = "zatoona_alarms_prefs"
        const val KEY_ALARMS_CACHE = "cached_upcoming_alarms_v1"
        const val MAX_PAYLOAD_LENGTH = 131072 // 128 KB
        const val MAX_ALARM_ITEMS = 60
        const val MAX_TITLE_LENGTH = 120
        const val MAX_BODY_LENGTH = 300
        const val MAX_ID_LENGTH = 80

        val ALLOWED_TYPES = setOf("prayer", "sleep", "activity", "custom")
        val ALLOWED_MODES = setOf(
            "home", "meal", "gym", "sleep", "prayer", "schedule",
            "recovery", "overview", "search", "budget", "notes", "stretches"
        )
        val ID_REGEX = Regex("^[a-zA-Z0-9_\\-:]+$")
    }

    private val prefs: SharedPreferences by lazy {
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }

    @JavascriptInterface
    fun syncUpcomingAlarms(payloadJson: String?): String {
        val result = JSONObject()
        try {
            if (payloadJson == null || payloadJson.isBlank()) {
                return errorResponse("EMPTY_PAYLOAD", "Payload cannot be null or empty.")
            }

            if (payloadJson.length > MAX_PAYLOAD_LENGTH) {
                return errorResponse("PAYLOAD_OVERSIZED", "Payload exceeds maximum allowed size (128 KB).")
            }

            val array = try {
                JSONArray(payloadJson)
            } catch (e: JSONException) {
                return errorResponse("INVALID_JSON", "Payload is not a valid JSON array: \${e.message}")
            }

            if (array.length() > MAX_ALARM_ITEMS) {
                return errorResponse("TOO_MANY_ITEMS", "Alarm count exceeds maximum limit (\${MAX_ALARM_ITEMS}).")
            }

            val validatedList = JSONArray()
            val nowMs = System.currentTimeMillis()
            val maxFutureMs = nowMs + (35L * 24 * 60 * 60 * 1000) // max 35 days in future

            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i)
                    ?: return errorResponse("INVALID_ITEM", "Item at index \$i is not a JSON object.")

                val version = item.optString("schemaVersion", SCHEMA_VERSION)
                if (version != SCHEMA_VERSION) {
                    return errorResponse("UNSUPPORTED_SCHEMA", "Item at index \$i has unsupported schemaVersion: \$version")
                }

                val id = item.optString("id", "").trim()
                if (id.isEmpty() || id.length > MAX_ID_LENGTH || !ID_REGEX.matches(id)) {
                    return errorResponse("INVALID_ID", "Item at index \$i has invalid or missing ID.")
                }

                val type = item.optString("type", "").trim().lowercase()
                if (!ALLOWED_TYPES.contains(type)) {
                    return errorResponse("INVALID_TYPE", "Item at index \$i has disallowed type: \$type")
                }

                val title = item.optString("title", "").trim()
                if (title.isEmpty() || title.length > MAX_TITLE_LENGTH) {
                    return errorResponse("INVALID_TITLE", "Item at index \$i has invalid title length.")
                }

                val body = item.optString("body", "").trim()
                if (body.length > MAX_BODY_LENGTH) {
                    return errorResponse("INVALID_BODY", "Item at index \$i has body exceeding maximum length.")
                }

                val triggerEpochMs = item.optLong("triggerEpochMs", -1L)
                if (triggerEpochMs <= 0 || triggerEpochMs > maxFutureMs) {
                    return errorResponse("INVALID_TIMESTAMP", "Item at index \$i has trigger timestamp out of bounds.")
                }

                val mode = item.optString("mode", "home").trim().lowercase()
                if (!ALLOWED_MODES.contains(mode)) {
                    return errorResponse("INVALID_MODE", "Item at index \$i has disallowed mode route: \$mode")
                }

                val channelId = item.optString("channelId", "zatoona_reminders").trim()

                val cleanItem = JSONObject().apply {
                    put("schemaVersion", SCHEMA_VERSION)
                    put("id", id)
                    put("type", type)
                    put("title", title)
                    put("body", body)
                    put("triggerEpochMs", triggerEpochMs)
                    put("mode", mode)
                    put("channelId", channelId)
                }
                validatedList.put(cleanItem)
            }

            // Save validated alarms cache locally
            prefs.edit().putString(KEY_ALARMS_CACHE, validatedList.toString()).apply()

            result.put("status", "ok")
            result.put("schemaVersion", SCHEMA_VERSION)
            result.put("syncedCount", validatedList.length())
            result.put("timestamp", nowMs)
            return result.toString()

        } catch (t: Throwable) {
            return errorResponse("INTERNAL_ERROR", "Bridge synchronization error occurred.")
        }
    }

    private fun errorResponse(code: String, message: String): String {
        return JSONObject().apply {
            put("status", "error")
            put("code", code)
            put("message", message)
            put("timestamp", System.currentTimeMillis())
        }.toString()
    }
}
"""

# 14. app/src/main/java/com/zatoona/app/MainActivity.kt
files[os.path.join("app", "src", "main", "java", "com", "zatoona", "app", "MainActivity.kt")] = """package com.zatoona.app

import android.annotation.SuppressLint
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private val assetLoader by lazy { ZatoonaAssetLoader.build(this) }
    private val bridge by lazy { ZatoonaBridge(this) }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)
        setContentView(webView)

        configureWebSettings(webView.settings)
        configureWebViewClient()
        attachBridge()
        handleBackNavigation()

        // Load trusted local PWA bundle
        webView.loadUrl(ZatoonaAssetLoader.ENTRY_URL)
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
"""

for rel_path, content in files.items():
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print(f"Created: android/{rel_path}")

print("Phase 13.4B1 Android scaffold created successfully.")

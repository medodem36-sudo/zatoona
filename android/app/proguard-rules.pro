# Keep JavaScript interface methods from being stripped or obfuscated
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep Zatoona bridge classes
-keep class com.zatoona.app.ZatoonaBridge { *; }

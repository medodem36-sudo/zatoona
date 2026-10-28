import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

passed_count = 0
failed_count = 0

def test(name, condition, details=""):
    global passed_count, failed_count
    if condition:
        print(f"  [PASS] {name}")
        passed_count += 1
    else:
        print(f"  [FAIL] {name} - {details}")
        failed_count += 1

def run_tests():
    global passed_count, failed_count
    print("================================================================================")
    print("PHASE 14 ACCEPTANCE TEST SUITE: RELEASE SIGNING CONFIGURATION TEMPLATE")
    print("================================================================================")

    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ANDROID = os.path.join(REPO, 'android')
    APP = os.path.join(ANDROID, 'app')
    GRADLE_KTS = os.path.join(APP, 'build.gradle.kts')
    GITIGNORE = os.path.join(REPO, '.gitignore')
    KS_EXAMPLE = os.path.join(ANDROID, 'keystore.properties.example')
    KS_REAL = os.path.join(ANDROID, 'keystore.properties')
    PROGUARD = os.path.join(APP, 'proguard-rules.pro')

    # ---------------------------------------------------------
    # Group 1: .gitignore Security Guards
    # ---------------------------------------------------------
    print("\n--- Group 1: .gitignore Security Guards ---")
    test(".gitignore file exists", os.path.isfile(GITIGNORE))
    with open(GITIGNORE, 'r', encoding='utf-8') as f:
        gitignore = f.read()

    test(".gitignore blocks *.keystore files", '*.keystore' in gitignore)
    test(".gitignore blocks *.jks files", '*.jks' in gitignore)
    test(".gitignore blocks *.p12 files", '*.p12' in gitignore)
    test(".gitignore blocks keystore.properties", 'keystore.properties' in gitignore)
    test(".gitignore blocks signing.properties", 'signing.properties' in gitignore)

    # ---------------------------------------------------------
    # Group 2: keystore.properties.example Template
    # ---------------------------------------------------------
    print("\n--- Group 2: keystore.properties.example Template ---")
    test("keystore.properties.example exists", os.path.isfile(KS_EXAMPLE))

    with open(KS_EXAMPLE, 'r', encoding='utf-8') as f:
        example = f.read()

    test("Example contains storeFile property", 'storeFile=' in example)
    test("Example contains storePassword property", 'storePassword=' in example)
    test("Example contains keyAlias property", 'keyAlias=' in example)
    test("Example contains keyPassword property", 'keyPassword=' in example)
    test("Example has placeholder values (not real passwords)",
         'YOUR_STORE_PASSWORD_HERE' in example or 'YOUR_PASSWORD' in example or 'PLACEHOLDER' in example)
    test("Example includes keytool generation instructions", 'keytool' in example)
    test("Example warns against committing secrets",
         'NEVER commit' in example or 'never commit' in example.lower() or 'excluded from Git' in example)

    # ---------------------------------------------------------
    # Group 3: No Real keystore.properties Committed
    # ---------------------------------------------------------
    print("\n--- Group 3: Security — No Real Secrets Present ---")
    test("Real keystore.properties does NOT exist in repo (safe)",
         not os.path.isfile(KS_REAL),
         "DANGER: keystore.properties found in repo!")

    # Check no .keystore or .jks files in repo
    keystore_files = []
    for root, dirs, files in os.walk(REPO):
        # Skip .gradle and build directories
        dirs[:] = [d for d in dirs if d not in ['.gradle', 'build', '.git', 'node_modules']]
        for f in files:
            if f.endswith('.keystore') or f.endswith('.jks') or f.endswith('.p12'):
                keystore_files.append(os.path.join(root, f))

    test("No .keystore / .jks / .p12 files found in repo tree",
         len(keystore_files) == 0,
         f"Found: {keystore_files}")

    # ---------------------------------------------------------
    # Group 4: build.gradle.kts signingConfigs Template
    # ---------------------------------------------------------
    print("\n--- Group 4: build.gradle.kts Release Signing Configuration ---")
    test("build.gradle.kts exists", os.path.isfile(GRADLE_KTS))

    with open(GRADLE_KTS, 'r', encoding='utf-8') as f:
        gradle = f.read()

    test("Gradle reads keystore.properties file",
         'keystorePropertiesFile' in gradle and 'keystore.properties' in gradle)
    test("Gradle uses java.util.Properties to load config",
         'java.util.Properties' in gradle)
    test("Gradle conditionally checks if keystore.properties exists",
         'keystorePropertiesFile.exists()' in gradle or 'hasReleaseSigningConfig' in gradle)
    test("Gradle defines signingConfigs.release block",
         'signingConfigs' in gradle and 'create("release")' in gradle)
    test("signingConfigs reads storeFile from properties",
         'getProperty("storeFile"' in gradle or "storeFile" in gradle)
    test("signingConfigs reads storePassword from properties",
         'getProperty("storePassword"' in gradle)
    test("signingConfigs reads keyAlias from properties",
         'getProperty("keyAlias"' in gradle)
    test("signingConfigs reads keyPassword from properties",
         'getProperty("keyPassword"' in gradle)
    test("Release buildType references signingConfig when available",
         'signingConfig = signingConfigs.getByName("release")' in gradle or
         'signingConfig = signingConfigs' in gradle)
    test("Release signing is CONDITIONAL (guarded by file existence check)",
         'hasReleaseSigningConfig' in gradle and
         gradle.count('hasReleaseSigningConfig') >= 2)
    test("Debug buildType is NOT affected by release signing",
         'applicationIdSuffix = ".debug"' in gradle)

    # ---------------------------------------------------------
    # Group 5: Gradle Build Integrity (Debug APK Still Works)
    # ---------------------------------------------------------
    print("\n--- Group 5: Gradle Build Integrity ---")
    debug_apk = os.path.join(APP, 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
    test("Debug APK exists (build not broken by signing config changes)",
         os.path.isfile(debug_apk))
    if os.path.isfile(debug_apk):
        size = os.path.getsize(debug_apk)
        test(f"Debug APK size is healthy ({size:,} bytes > 2 MB)", size > 2_000_000)

    # ---------------------------------------------------------
    # Group 6: ProGuard / R8 Protection Integrity
    # ---------------------------------------------------------
    print("\n--- Group 6: ProGuard / R8 Protection ---")
    test("proguard-rules.pro exists", os.path.isfile(PROGUARD))
    with open(PROGUARD, 'r', encoding='utf-8') as f:
        proguard = f.read()

    test("ProGuard keeps @JavascriptInterface methods",
         '@android.webkit.JavascriptInterface' in proguard)
    test("ProGuard keeps ZatoonaBridge class",
         'com.zatoona.app.ZatoonaBridge' in proguard)
    test("Release build has isMinifyEnabled = true",
         'isMinifyEnabled = true' in gradle)

    # ---------------------------------------------------------
    # Group 7: Version & Identification
    # ---------------------------------------------------------
    print("\n--- Group 7: App Version & Identity ---")
    test("applicationId is com.zatoona.app", 'applicationId = "com.zatoona.app"' in gradle)
    test("versionCode is set", 'versionCode = ' in gradle)
    test("versionName is set", 'versionName = ' in gradle)
    test("compileSdk = 34", 'compileSdk = 34' in gradle)
    test("minSdk = 26", 'minSdk = 26' in gradle)
    test("targetSdk = 34", 'targetSdk = 34' in gradle)

    print("\n================================================================================")
    print(f"RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("================================================================================")
    return failed_count == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

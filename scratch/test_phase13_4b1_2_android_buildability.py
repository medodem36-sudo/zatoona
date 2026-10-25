# -*- coding: utf-8 -*-
"""
Phase 13.4B1.2 Acceptance Test: Android Toolchain Setup & Buildability Verification
Verifies:
1. Toolchain Components & SDK Configuration
2. Real APK Artifact Generation & Structure
3. Packaged PWA Assets Integrity
4. Android Device / Emulator Diagnostics
5. PWA Parity & Invariance
"""
import sys
import os
import json
import zipfile
import subprocess
import filecmp

sys.stdout.reconfigure(encoding='utf-8')

REPO = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
ANDROID_DIR = os.path.join(REPO, "android")
INDEX_PATH = os.path.join(REPO, "index.html")
ZATOONA_PATH = os.path.join(REPO, "zatoona.html")
APK_PATH = os.path.join(ANDROID_DIR, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
METADATA_PATH = os.path.join(ANDROID_DIR, "app", "build", "outputs", "apk", "debug", "output-metadata.json")

passed = 0
failed = 0

def check(desc, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {desc}")
    else:
        failed += 1
        print(f"  [FAIL] {desc}")

print("================================================================================")
print("PHASE 13.4B1.2 ACCEPTANCE TEST: ANDROID TOOLCHAIN & BUILDABILITY")
print("================================================================================")

# --- 1. Toolchain Components & Environment Configuration ---
print("\n--- 1. Toolchain Components & Environment Configuration ---")
jdk_path = r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot"
sdk_path = r"C:\Users\Lenovo\AppData\Local\Android\Sdk"
gradle_bin = r"C:\Users\Lenovo\AppData\Local\Gradle\gradle-8.5\bin\gradle.bat"
adb_path = r"C:\Users\Lenovo\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"

check("JDK 17 home exists", os.path.isdir(jdk_path))
check("JDK 17 javac.exe exists", os.path.isfile(os.path.join(jdk_path, "bin", "javac.exe")))
check("Android SDK directory exists", os.path.isdir(sdk_path))
check("Android SDK platforms/android-34 exists", os.path.isdir(os.path.join(sdk_path, "platforms", "android-34")))
check("Android SDK build-tools directory exists", os.path.isdir(os.path.join(sdk_path, "build-tools")))
check("Gradle 8.5 binary exists", os.path.isfile(gradle_bin))
check("ADB platform-tools binary exists", os.path.isfile(adb_path))

local_props = os.path.join(ANDROID_DIR, "local.properties")
check("android/local.properties exists", os.path.isfile(local_props))
with open(local_props, "r", encoding="utf-8") as f:
    props_content = f.read()
check("android/local.properties specifies sdk.dir correctly", "sdk.dir=" in props_content and "Android" in props_content)

# --- 2. Real APK Artifact Generation & Packaging ---
print("\n--- 2. Real APK Artifact Generation & Packaging ---")
check("Debug APK file generated at expected output path", os.path.isfile(APK_PATH))
apk_size = os.path.getsize(APK_PATH) if os.path.isfile(APK_PATH) else 0
check(f"APK size is realistic for packaged app ({apk_size} bytes, > 2 MB)", apk_size > 2 * 1024 * 1024)

check("output-metadata.json exists", os.path.isfile(METADATA_PATH))
if os.path.isfile(METADATA_PATH):
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)
    check("Metadata applicationId is com.zatoona.app.debug", meta.get("applicationId") == "com.zatoona.app.debug")
    elements = meta.get("elements", [])
    check("Metadata contains output element", len(elements) > 0)
    if elements:
        check("Metadata outputFile is app-debug.apk", elements[0].get("outputFile") == "app-debug.apk")
        check("Metadata versionName is 1.0.0", elements[0].get("versionName") == "1.0.0")

# --- 3. Packaged APK Internal Inspection ---
print("\n--- 3. Packaged APK Internal Inspection ---")
if os.path.isfile(APK_PATH):
    with zipfile.ZipFile(APK_PATH, "r") as z:
        names = set(z.namelist())
        check("APK contains AndroidManifest.xml", "AndroidManifest.xml" in names)
        check("APK contains resources.arsc", "resources.arsc" in names)
        check("APK contains classes.dex", "classes.dex" in names)
        
        # Check bundled PWA assets
        check("APK packages assets/index.html", "assets/index.html" in names)
        check("APK packages assets/manifest.json", "assets/manifest.json" in names)
        check("APK packages assets/sw.js", "assets/sw.js" in names)
        check("APK packages assets/assets/data/exercise-catalog.js", "assets/assets/data/exercise-catalog.js" in names)
        check("APK packages assets/assets/data/stretch-catalog.js", "assets/assets/data/stretch-catalog.js" in names)
        
        # Check launcher mipmaps
        launcher_icons = [n for n in names if "ic_launcher" in n]
        check(f"APK contains mipmap launcher icons ({len(launcher_icons)} entries)", len(launcher_icons) >= 5)

# --- 4. Android Device / Target Diagnostics ---
print("\n--- 4. Android Device / Target Diagnostics ---")
emulator_bin = os.path.join(sdk_path, "emulator", "emulator.exe")
check("Android emulator binary exists in SDK", os.path.isfile(emulator_bin))
try:
    avd_proc = subprocess.run([emulator_bin, "-list-avds"], capture_output=True, text=True, timeout=10)
    avds = [line.strip() for line in avd_proc.stdout.splitlines() if line.strip()]
    check(f"AVD list query successful (found {len(avds)}: {avds})", avd_proc.returncode == 0)
except Exception as e:
    check("AVD query failed", False)

try:
    adb_proc = subprocess.run([adb_path, "devices"], capture_output=True, text=True, timeout=10)
    check("ADB devices query successful", adb_proc.returncode == 0)
except Exception as e:
    check("ADB devices query failed", False)

# --- 5. PWA Invariance & Browser Parity ---
print("\n--- 5. PWA Invariance & Browser Parity ---")
check("index.html exists", os.path.isfile(INDEX_PATH))
check("zatoona.html exists", os.path.isfile(ZATOONA_PATH))
parity = filecmp.cmp(INDEX_PATH, ZATOONA_PATH, shallow=False)
check("index.html and zatoona.html are 100% byte-identical", parity)

print(f"\n================================================================================")
print(f"RESULTS: {passed} PASSED, {failed} FAILED")
print(f"================================================================================")

sys.exit(0 if failed == 0 else 1)

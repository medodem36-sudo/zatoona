import os
import sys
import zipfile
import hashlib

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
    print("PHASE 13.5 EXTENSION ACCEPTANCE TEST: NEXT PRAYER HOME-SCREEN WIDGET (PROPOSAL #8)")
    print("================================================================================")

    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ANDROID = os.path.join(REPO, 'android')
    APP = os.path.join(ANDROID, 'app')
    MAIN = os.path.join(APP, 'src', 'main')
    RES = os.path.join(MAIN, 'res')
    JAVA = os.path.join(MAIN, 'java', 'com', 'zatoona', 'app')

    MANIFEST = os.path.join(MAIN, 'AndroidManifest.xml')
    WIDGET_INFO = os.path.join(RES, 'xml', 'widget_next_prayer_info.xml')
    WIDGET_LAYOUT = os.path.join(RES, 'layout', 'widget_next_prayer.xml')
    WIDGET_PROVIDER = os.path.join(JAVA, 'NextPrayerWidgetProvider.kt')
    BRIDGE = os.path.join(JAVA, 'ZatoonaBridge.kt')
    STRINGS = os.path.join(RES, 'values', 'strings.xml')
    PROGUARD = os.path.join(APP, 'proguard-rules.pro')
    APK_PATH = os.path.join(APP, 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')

    # ---------------------------------------------------------
    # Group 1: Android Manifest Declarations
    # ---------------------------------------------------------
    print("\n--- Group 1: Android Manifest Declarations ---")
    test("AndroidManifest.xml exists", os.path.isfile(MANIFEST))
    with open(MANIFEST, 'r', encoding='utf-8') as f:
        manifest = f.read()

    test("NextPrayerWidgetProvider receiver registered",
         'android:name=".NextPrayerWidgetProvider"' in manifest)
    test("Receiver exported=true",
         'android:name=".NextPrayerWidgetProvider"' in manifest and 'android:exported="true"' in manifest)
    test("Receiver listens for APPWIDGET_UPDATE action",
         'android.appwidget.action.APPWIDGET_UPDATE' in manifest)
    test("Receiver metadata points to @xml/widget_next_prayer_info",
         'android:name="android.appwidget.provider"' in manifest and
         'android:resource="@xml/widget_next_prayer_info"' in manifest)
    test("Receiver label references widget_next_prayer_title",
         'android:label="@string/widget_next_prayer_title"' in manifest)

    # ---------------------------------------------------------
    # Group 2: AppWidgetProvider XML Specification
    # ---------------------------------------------------------
    print("\n--- Group 2: AppWidgetProvider XML Specification ---")
    test("widget_next_prayer_info.xml exists", os.path.isfile(WIDGET_INFO))
    with open(WIDGET_INFO, 'r', encoding='utf-8') as f:
        info_xml = f.read()

    test("appwidget-provider root element present", '<appwidget-provider' in info_xml)
    test("minWidth specified (>= 200dp)", 'android:minWidth="200dp"' in info_xml)
    test("minHeight specified (>= 80dp)", 'android:minHeight="80dp"' in info_xml)
    test("updatePeriodMillis set to 1800000 (30 min)", 'android:updatePeriodMillis="1800000"' in info_xml)
    test("initialLayout references @layout/widget_next_prayer",
         'android:initialLayout="@layout/widget_next_prayer"' in info_xml)
    test("previewImage references @mipmap/ic_launcher",
         'android:previewImage="@mipmap/ic_launcher"' in info_xml)
    test("widgetCategory is home_screen",
         'android:widgetCategory="home_screen"' in info_xml)
    test("description references @string/widget_next_prayer_description",
         'android:description="@string/widget_next_prayer_description"' in info_xml)

    # ---------------------------------------------------------
    # Group 3: Widget Layout Design & RemoteViews Invariants
    # ---------------------------------------------------------
    print("\n--- Group 3: Widget Layout & RemoteViews Invariants ---")
    test("widget_next_prayer.xml exists", os.path.isfile(WIDGET_LAYOUT))
    with open(WIDGET_LAYOUT, 'r', encoding='utf-8') as f:
        layout_xml = f.read()

    test("No disallowed RemoteViews tags (ConstraintLayout forbidden)",
         'ConstraintLayout' not in layout_xml and 'CoordinatorLayout' not in layout_xml)
    test("Root container is LinearLayout", layout_xml.lstrip().startswith('<?xml') and '<LinearLayout' in layout_xml)
    test("Root has id widget_prayer_root", 'android:id="@+id/widget_prayer_root"' in layout_xml)
    test("Header title TextView exists (widget_prayer_header_title)", 'android:id="@+id/widget_prayer_header_title"' in layout_xml)
    test("City badge TextView exists (widget_prayer_city)", 'android:id="@+id/widget_prayer_city"' in layout_xml)
    test("Prayer name TextView exists (widget_prayer_name)", 'android:id="@+id/widget_prayer_name"' in layout_xml)
    test("Prayer time TextView exists (widget_prayer_time)", 'android:id="@+id/widget_prayer_time"' in layout_xml)
    test("Countdown TextView exists (widget_prayer_countdown)", 'android:id="@+id/widget_prayer_countdown"' in layout_xml)

    # ---------------------------------------------------------
    # Group 4: Localized Arabic Strings
    # ---------------------------------------------------------
    print("\n--- Group 4: Localized Arabic Strings ---")
    test("strings.xml exists", os.path.isfile(STRINGS))
    with open(STRINGS, 'r', encoding='utf-8') as f:
        strings = f.read()

    test("String widget_next_prayer_title defined in Arabic",
         '<string name="widget_next_prayer_title">زتونة — الصلاة القادمة</string>' in strings)
    test("String widget_prayer_header defined in Arabic",
         '<string name="widget_prayer_header">الصلاة القادمة</string>' in strings)
    test("String widget_prayer_fallback defined in Arabic",
         '<string name="widget_prayer_fallback">افتح زتونة لمزامنة المواقيت</string>' in strings)

    # ---------------------------------------------------------
    # Group 5: Kotlin Widget Provider Engine
    # ---------------------------------------------------------
    print("\n--- Group 5: Kotlin NextPrayerWidgetProvider Engine ---")
    test("NextPrayerWidgetProvider.kt exists", os.path.isfile(WIDGET_PROVIDER))
    with open(WIDGET_PROVIDER, 'r', encoding='utf-8') as f:
        kt = f.read()

    test("Class extends AppWidgetProvider", 'class NextPrayerWidgetProvider : AppWidgetProvider()' in kt)
    test("Overrides onUpdate", 'override fun onUpdate(' in kt)
    test("Implements updateAppWidget", 'fun updateAppWidget(' in kt)
    test("Implements updateAllWidgets static trigger", 'fun updateAllWidgets(context: Context)' in kt)
    test("Implements findNextPrayer calculation", 'fun findNextPrayer(' in kt)
    test("Implements Arabic countdown formatting", 'fun formatCountdown(' in kt)
    test("Implements 12h Arabic time formatting (ص / م)", 'fun formatTime12h(' in kt)
    test("Sets click PendingIntent on widget_prayer_root targeting prayer mode",
         'views.setOnClickPendingIntent(R.id.widget_prayer_root, pendingIntent)' in kt and
         '"prayer"' in kt)
    test("PendingIntent uses FLAG_ACTIVITY_NEW_TASK or CLEAR_TOP",
         'Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP' in kt)
    test("PendingIntent uses FLAG_IMMUTABLE",
         'PendingIntent.FLAG_IMMUTABLE' in kt)

    # ---------------------------------------------------------
    # Group 6: ZatoonaBridge Synchronization Hook
    # ---------------------------------------------------------
    print("\n--- Group 6: ZatoonaBridge Synchronization Hook ---")
    test("ZatoonaBridge.kt exists", os.path.isfile(BRIDGE))
    with open(BRIDGE, 'r', encoding='utf-8') as f:
        bridge_kt = f.read()

    test("syncSchedules calls NextPrayerWidgetProvider.updateAllWidgets",
         'NextPrayerWidgetProvider.updateAllWidgets(context)' in bridge_kt and
         'fun syncSchedules' in bridge_kt)
    test("updateActivePrayerCity calls NextPrayerWidgetProvider.updateAllWidgets",
         'NextPrayerWidgetProvider.updateAllWidgets(context)' in bridge_kt and
         'fun updateActivePrayerCity' in bridge_kt)

    # ---------------------------------------------------------
    # Group 7: ProGuard / R8 Rules
    # ---------------------------------------------------------
    print("\n--- Group 7: ProGuard / R8 Protection ---")
    test("proguard-rules.pro exists", os.path.isfile(PROGUARD))
    with open(PROGUARD, 'r', encoding='utf-8') as f:
        proguard = f.read()

    test("ProGuard keeps NextPrayerWidgetProvider from shrinking/obfuscation",
         'com.zatoona.app.NextPrayerWidgetProvider' in proguard)

    # ---------------------------------------------------------
    # Group 8: Packaged APK Artifact Packaging
    # ---------------------------------------------------------
    print("\n--- Group 8: Packaged APK Artifact Verification ---")
    test("Debug APK exists", os.path.isfile(APK_PATH))
    if os.path.isfile(APK_PATH):
        with zipfile.ZipFile(APK_PATH, 'r') as z:
            names = z.namelist()
            test("APK packages next prayer widget layout resource",
                 'res/layout/widget_next_prayer.xml' in names)
            test("APK packages next prayer widget info XML metadata",
                 'res/xml/widget_next_prayer_info.xml' in names)

            # DEX inspection
            has_class = False
            for n in names:
                if n.endswith('.dex'):
                    if b'NextPrayerWidgetProvider' in z.read(n):
                        has_class = True
                        break
            test("APK classes.dex contains NextPrayerWidgetProvider byte symbols", has_class)

    # ---------------------------------------------------------
    # Group 9: PWA Invariance & 3-Way Parity
    # ---------------------------------------------------------
    print("\n--- Group 9: PWA Invariance & 3-Way Parity ---")
    pwa_files = [
        os.path.join(REPO, 'index.html'),
        os.path.join(REPO, 'zatoona.html'),
        os.path.join(MAIN, 'assets', 'index.html')
    ]
    hashes = []
    sizes = []
    for p in pwa_files:
        test(f"PWA file exists: {os.path.basename(p)}", os.path.isfile(p))
        if os.path.isfile(p):
            with open(p, 'rb') as f:
                content = f.read()
                hashes.append(hashlib.sha256(content).hexdigest())
                sizes.append(len(content))

    test("All 3 PWA HTML entrypoints have identical size", len(set(sizes)) == 1, f"Sizes: {sizes}")
    test("All 3 PWA HTML entrypoints have 100% identical SHA-256 hash", len(set(hashes)) == 1, f"Hashes: {hashes}")

    print("\n================================================================================")
    print(f"RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("================================================================================")
    return failed_count == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

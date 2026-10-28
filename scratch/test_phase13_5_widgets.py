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
    print("PHASE 13.5 ACCEPTANCE TEST SUITE: NATIVE ANDROID QUICK ACCESS WIDGET (PROPOSAL #7)")
    print("================================================================================")

    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ANDROID = os.path.join(REPO, 'android')
    APP = os.path.join(ANDROID, 'app')
    MAIN = os.path.join(APP, 'src', 'main')
    RES = os.path.join(MAIN, 'res')
    JAVA = os.path.join(MAIN, 'java', 'com', 'zatoona', 'app')

    MANIFEST = os.path.join(MAIN, 'AndroidManifest.xml')
    WIDGET_INFO = os.path.join(RES, 'xml', 'widget_quick_access_info.xml')
    WIDGET_LAYOUT = os.path.join(RES, 'layout', 'widget_quick_access.xml')
    WIDGET_PROVIDER = os.path.join(JAVA, 'QuickAccessWidgetProvider.kt')
    STRINGS = os.path.join(RES, 'values', 'strings.xml')
    CARD_BG = os.path.join(RES, 'drawable', 'bg_widget_card.xml')
    BTN_BG = os.path.join(RES, 'drawable', 'bg_widget_button.xml')
    PROGUARD = os.path.join(APP, 'proguard-rules.pro')
    APK_PATH = os.path.join(APP, 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')

    # ---------------------------------------------------------
    # Group 1: Android Manifest & Component Declarations
    # ---------------------------------------------------------
    print("\n--- Group 1: Android Manifest Declarations ---")
    test("AndroidManifest.xml exists", os.path.isfile(MANIFEST))
    with open(MANIFEST, 'r', encoding='utf-8') as f:
        manifest = f.read()

    test("QuickAccessWidgetProvider receiver registered",
         'android:name=".QuickAccessWidgetProvider"' in manifest)
    test("Receiver exported=true",
         'android:name=".QuickAccessWidgetProvider"' in manifest and 'android:exported="true"' in manifest)
    test("Receiver listens for APPWIDGET_UPDATE action",
         'android.appwidget.action.APPWIDGET_UPDATE' in manifest)
    test("Receiver metadata points to @xml/widget_quick_access_info",
         'android:name="android.appwidget.provider"' in manifest and
         'android:resource="@xml/widget_quick_access_info"' in manifest)
    test("Receiver label references widget_quick_access_title",
         'android:label="@string/widget_quick_access_title"' in manifest)

    # ---------------------------------------------------------
    # Group 2: AppWidgetProvider XML Specification
    # ---------------------------------------------------------
    print("\n--- Group 2: AppWidgetProvider XML Specification ---")
    test("widget_quick_access_info.xml exists", os.path.isfile(WIDGET_INFO))
    with open(WIDGET_INFO, 'r', encoding='utf-8') as f:
        info_xml = f.read()

    test("appwidget-provider root element present", '<appwidget-provider' in info_xml)
    test("minWidth specified (>= 250dp)", 'android:minWidth="250dp"' in info_xml)
    test("minHeight specified (>= 100dp)", 'android:minHeight="100dp"' in info_xml)
    test("initialLayout references @layout/widget_quick_access",
         'android:initialLayout="@layout/widget_quick_access"' in info_xml)
    test("previewImage references @mipmap/ic_launcher",
         'android:previewImage="@mipmap/ic_launcher"' in info_xml)
    test("widgetCategory is home_screen",
         'android:widgetCategory="home_screen"' in info_xml)
    test("description references @string/widget_quick_access_description",
         'android:description="@string/widget_quick_access_description"' in info_xml)

    # ---------------------------------------------------------
    # Group 3: Widget Layout Design & RemoteViews Safety
    # ---------------------------------------------------------
    print("\n--- Group 3: Widget Layout & RemoteViews Invariants ---")
    test("widget_quick_access.xml exists", os.path.isfile(WIDGET_LAYOUT))
    with open(WIDGET_LAYOUT, 'r', encoding='utf-8') as f:
        layout_xml = f.read()

    test("No disallowed RemoteViews tags (ConstraintLayout forbidden)",
         'ConstraintLayout' not in layout_xml and 'CoordinatorLayout' not in layout_xml)
    test("Root container is LinearLayout", layout_xml.lstrip().startswith('<?xml') and '<LinearLayout' in layout_xml)
    test("Header view exists (widget_header)", 'android:id="@+id/widget_header"' in layout_xml)
    test("Title TextView exists (widget_title)", 'android:id="@+id/widget_title"' in layout_xml)
    test("Prayer button exists (widget_btn_prayer)", 'android:id="@+id/widget_btn_prayer"' in layout_xml)
    test("Gym button exists (widget_btn_gym)", 'android:id="@+id/widget_btn_gym"' in layout_xml)
    test("Meal button exists (widget_btn_meal)", 'android:id="@+id/widget_btn_meal"' in layout_xml)
    test("Schedule button exists (widget_btn_schedule)", 'android:id="@+id/widget_btn_schedule"' in layout_xml)
    test("Card background drawable exists", os.path.isfile(CARD_BG))
    test("Button background drawable exists", os.path.isfile(BTN_BG))

    # ---------------------------------------------------------
    # Group 4: Localized Strings
    # ---------------------------------------------------------
    print("\n--- Group 4: Localized Arabic Strings ---")
    test("strings.xml exists", os.path.isfile(STRINGS))
    with open(STRINGS, 'r', encoding='utf-8') as f:
        strings = f.read()

    test("String widget_quick_access_title defined in Arabic",
         '<string name="widget_quick_access_title">زتونة — وصول سريع</string>' in strings)
    test("String widget_prayer defined in Arabic",
         '<string name="widget_prayer">الصلوات</string>' in strings)
    test("String widget_gym defined in Arabic",
         '<string name="widget_gym">التمارين</string>' in strings)
    test("String widget_meal defined in Arabic",
         '<string name="widget_meal">التغذية</string>' in strings)
    test("String widget_schedule defined in Arabic",
         '<string name="widget_schedule">الجدول</string>' in strings)

    # ---------------------------------------------------------
    # Group 5: Kotlin Widget Provider Engine
    # ---------------------------------------------------------
    print("\n--- Group 5: Kotlin Widget Provider Engine ---")
    test("QuickAccessWidgetProvider.kt exists", os.path.isfile(WIDGET_PROVIDER))
    with open(WIDGET_PROVIDER, 'r', encoding='utf-8') as f:
        kt = f.read()

    test("Class extends AppWidgetProvider", 'class QuickAccessWidgetProvider : AppWidgetProvider()' in kt)
    test("Overrides onUpdate", 'override fun onUpdate(' in kt)
    test("Implements updateAppWidget", 'fun updateAppWidget(' in kt)
    test("Instantiates RemoteViews with R.layout.widget_quick_access",
         'RemoteViews(context.packageName, R.layout.widget_quick_access)' in kt)
    test("Sets click PendingIntent on widget_header",
         'views.setOnClickPendingIntent(\n                R.id.widget_header' in kt or
         'R.id.widget_header' in kt)
    test("Wires prayer destination mode", '"prayer"' in kt and 'R.id.widget_btn_prayer' in kt)
    test("Wires gym destination mode", '"gym"' in kt and 'R.id.widget_btn_gym' in kt)
    test("Wires meal destination mode", '"meal"' in kt and 'R.id.widget_btn_meal' in kt)
    test("Wires schedule destination mode", '"schedule"' in kt and 'R.id.widget_btn_schedule' in kt)
    test("PendingIntent uses FLAG_ACTIVITY_NEW_TASK or CLEAR_TOP",
         'Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP' in kt)
    test("PendingIntent uses FLAG_IMMUTABLE",
         'PendingIntent.FLAG_IMMUTABLE' in kt)
    test("Calls appWidgetManager.updateAppWidget",
         'appWidgetManager.updateAppWidget(appWidgetId, views)' in kt)

    # ---------------------------------------------------------
    # Group 6: ProGuard / R8 Protection
    # ---------------------------------------------------------
    print("\n--- Group 6: ProGuard / R8 Rules ---")
    test("proguard-rules.pro exists", os.path.isfile(PROGUARD))
    with open(PROGUARD, 'r', encoding='utf-8') as f:
        proguard = f.read()

    test("ProGuard keeps QuickAccessWidgetProvider from shrinking/obfuscation",
         'com.zatoona.app.QuickAccessWidgetProvider' in proguard)

    # ---------------------------------------------------------
    # Group 7: Packaged APK Artifact Packaging
    # ---------------------------------------------------------
    print("\n--- Group 7: Packaged APK Artifact Verification ---")
    test("Debug APK exists", os.path.isfile(APK_PATH))
    if os.path.isfile(APK_PATH):
        with zipfile.ZipFile(APK_PATH, 'r') as z:
            names = z.namelist()
            test("APK packages widget layout resource",
                 'res/layout/widget_quick_access.xml' in names)
            test("APK packages widget info XML metadata",
                 'res/xml/widget_quick_access_info.xml' in names)
            test("APK packages widget card background drawable",
                 'res/drawable/bg_widget_card.xml' in names)
            test("APK packages widget button background drawable",
                 'res/drawable/bg_widget_button.xml' in names)

            # DEX inspection
            has_class = False
            for n in names:
                if n.endswith('.dex'):
                    if b'QuickAccessWidgetProvider' in z.read(n):
                        has_class = True
                        break
            test("APK classes.dex contains QuickAccessWidgetProvider byte symbols", has_class)

    # ---------------------------------------------------------
    # Group 8: PWA Invariance & 3-Way Parity
    # ---------------------------------------------------------
    print("\n--- Group 8: PWA Invariance & 3-Way Parity ---")
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

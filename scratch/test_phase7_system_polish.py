# -*- coding: utf-8 -*-
"""
test_phase7_system_polish.py
Automated acceptance test suite for Phase 7:
System Polish & Zatoona Wrapped (7 features)
"""
import os
import sys
import json
import time

sys.stdout.reconfigure(encoding='utf-8')

passed_count = 0
failed_count = 0

def check(title, condition, details=""):
    global passed_count, failed_count
    if condition:
        print(f"  [PASS] {title}")
        passed_count += 1
    else:
        print(f"  [FAIL] {title} - {details}")
        failed_count += 1

print("==================================================")
print("Running Phase 7 Test Suite: System Polish & Zatoona Wrapped")
print("==================================================")

# 1. Android Native Study Widget Checks
print("\n--- 1. Android Native Study Widget ---")
study_provider_path = "android/app/src/main/java/com/zatoona/app/StudyWidgetProvider.kt"
study_layout_path = "android/app/src/main/res/layout/widget_study.xml"
study_info_path = "android/app/src/main/res/xml/widget_study_info.xml"
manifest_path = "android/app/src/main/AndroidManifest.xml"

check("StudyWidgetProvider.kt exists", os.path.exists(study_provider_path))
if os.path.exists(study_provider_path):
    with open(study_provider_path, "r", encoding="utf-8") as f:
        src = f.read()
    check("StudyWidgetProvider inherits AppWidgetProvider", "class StudyWidgetProvider : AppWidgetProvider()" in src)
    check("StudyWidgetProvider handles study mode navigation", "mode, \"study\"" in src or "mode: String" in src)
    check("StudyWidgetProvider loads cached data", "KEY_STUDY_CACHE" in src)

check("widget_study.xml exists", os.path.exists(study_layout_path))
if os.path.exists(study_layout_path):
    with open(study_layout_path, "r", encoding="utf-8") as f:
        layout = f.read()
    check("widget_study.xml has root and text views", "widget_study_root" in layout and "widget_study_time_display" in layout)
    check("widget_study.xml has action buttons", "widget_study_btn_start" in layout and "widget_study_btn_review" in layout)

check("widget_study_info.xml exists", os.path.exists(study_info_path))

# 2. Android Quick Settings Tile Services
print("\n--- 2. Android Quick Settings Tile Services ---")
study_tile_path = "android/app/src/main/java/com/zatoona/app/ZatoonaStudyTileService.kt"
gym_tile_path = "android/app/src/main/java/com/zatoona/app/ZatoonaGymTileService.kt"

check("ZatoonaStudyTileService.kt exists", os.path.exists(study_tile_path))
if os.path.exists(study_tile_path):
    with open(study_tile_path, "r", encoding="utf-8") as f:
        tsrc = f.read()
    check("ZatoonaStudyTileService extends TileService", "class ZatoonaStudyTileService : TileService()" in tsrc)
    check("ZatoonaStudyTileService launches study mode", '"study"' in tsrc)

check("ZatoonaGymTileService.kt exists", os.path.exists(gym_tile_path))
if os.path.exists(gym_tile_path):
    with open(gym_tile_path, "r", encoding="utf-8") as f:
        gsrc = f.read()
    check("ZatoonaGymTileService extends TileService", "class ZatoonaGymTileService : TileService()" in gsrc)
    check("ZatoonaGymTileService launches gym mode", '"gym"' in gsrc)

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = f.read()
check("AndroidManifest declares StudyWidgetProvider", "StudyWidgetProvider" in manifest)
check("AndroidManifest declares ZatoonaStudyTileService", "ZatoonaStudyTileService" in manifest and "BIND_QUICK_SETTINGS_TILE" in manifest)
check("AndroidManifest declares ZatoonaGymTileService", "ZatoonaGymTileService" in manifest)

# 3. ZatoonaBridge & ProGuard Updates
print("\n--- 3. ZatoonaBridge & ProGuard Rules ---")
bridge_path = "android/app/src/main/java/com/zatoona/app/ZatoonaBridge.kt"
with open(bridge_path, "r", encoding="utf-8") as f:
    bridge = f.read()
check("ZatoonaBridge ALLOWED_MODES includes 'study'", '"study"' in bridge)
check("ZatoonaBridge defines KEY_STUDY_CACHE", "KEY_STUDY_CACHE" in bridge)
check("ZatoonaBridge defines syncStudyWidget", "fun syncStudyWidget" in bridge)

proguard_path = "android/app/proguard-rules.pro"
with open(proguard_path, "r", encoding="utf-8") as f:
    prog = f.read()
check("ProGuard keeps StudyWidgetProvider", "StudyWidgetProvider" in prog)
check("ProGuard keeps ZatoonaStudyTileService", "ZatoonaStudyTileService" in prog)

# 4. Web PWA Structure & Selenium Integration
print("\n--- 4. Web / PWA Automated Reminders & Zatoona Wrapped ---")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

check("index.html contains #backupReminderBanner", 'id="backupReminderBanner"' in html)
check("index.html contains #backupReminderSettingsRow", 'id="backupReminderSettingsRow"' in html)
check("index.html contains #zatoonaWrappedCard", 'id="zatoonaWrappedCard"' in html)
check("index.html contains #zatoonaWrappedModal", 'id="zatoonaWrappedModal"' in html)
check("index.html contains KNOWN_KEY_PATTERNS with /^zatoona-/", "/^zatoona-/" in html)

# 5. Selenium Headless Chrome Live E2E
print("\n--- 5. Selenium Headless Chrome Live E2E Tests ---")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=opts)
    abs_path = os.path.abspath("index.html")
    driver.get(f"file:///{abs_path.replace(os.sep, '/')}")
    time.sleep(2)

    # Test 5.1: Backup Reminder triggers when overdue
    driver.execute_script("""
        // Set last backup to 10 days ago (overdue for 7-day default)
        var tenDaysAgo = Date.now() - (10 * 86400000);
        localStorage.setItem('zatoona-last-backup-timestamp-v1', tenDaysAgo.toString());
        localStorage.removeItem('zatoona-backup-reminder-dismissed-v1');
        localStorage.setItem('zatoona-backup-reminder-interval-v1', '7');
        // Trigger check
        if (typeof checkBackupReminder === 'function') {
            checkBackupReminder();
        } else {
            // Reload or call via event
            var event = new Event('DOMContentLoaded');
            document.dispatchEvent(event);
        }
    """)
    time.sleep(0.5)
    banner_display = driver.execute_script("return document.getElementById('backupReminderBanner').style.display;")
    check("Backup reminder banner displays when overdue", banner_display == "flex" or banner_display == "")

    # Test 5.2: Dismiss backup reminder hides banner
    driver.execute_script("dismissBackupReminder();")
    time.sleep(0.3)
    banner_hidden = driver.execute_script("return document.getElementById('backupReminderBanner').style.display;")
    check("Dismiss backup reminder hides banner", banner_hidden == "none")

    # Test 5.3: Study widget sync creates valid payload in localStorage
    driver.execute_script("syncStudyToNativeWidget();")
    study_cache_raw = driver.execute_script("return localStorage.getItem('zatoona-study-widget-cache-v1');")
    check("syncStudyToNativeWidget saves valid cache", study_cache_raw is not None and "focusMinutesToday" in study_cache_raw)

    # Test 5.4: Open Zatoona Wrapped Modal
    driver.execute_script("openZatoonaWrappedModal('month');")
    time.sleep(0.5)
    modal_open = driver.execute_script("return document.getElementById('zatoonaWrappedModal').classList.contains('open');")
    check("openZatoonaWrappedModal opens modal (.open class added)", modal_open is True)

    rank_text = driver.execute_script("return document.getElementById('wrappedRankTitle').textContent;")
    check("Wrapped rank title is populated", len(rank_text) > 3)

    metrics_count = driver.execute_script("return document.querySelectorAll('#wrappedMetricsGrid .wrapped-metric-card').length;")
    check("Wrapped metrics grid renders 6 pillar cards", metrics_count == 6)

    # Test 5.5: Switch period to 'year'
    driver.execute_script("switchWrappedPeriod('year');")
    time.sleep(0.3)
    year_active = driver.execute_script("return document.getElementById('btnWrappedYear').classList.contains('active');")
    check("switchWrappedPeriod('year') activates year tab", year_active is True)

    # Test 5.6: Close Zatoona Wrapped Modal
    driver.execute_script("closeZatoonaWrappedModal();")
    time.sleep(0.3)
    modal_closed = driver.execute_script("return !document.getElementById('zatoonaWrappedModal').classList.contains('open');")
    check("closeZatoonaWrappedModal closes modal (.open class removed)", modal_closed is True)

    driver.quit()
except Exception as e:
    check("Selenium E2E suite execution", False, str(e))

print(f"\nPhase 7 Test Summary: {passed_count} Passed, {failed_count} Failed")
if failed_count > 0:
    sys.exit(1)

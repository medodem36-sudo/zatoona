#!/usr/bin/env python3
"""
Acceptance Test Suite for:
- Item #1 (Proposal #9): Native Android Daily Habits Home-Screen Widget
- Item #3 (Phase 13.7): Optional Privacy-Conscious Local AI Assistant ("كوتش زتونة الذكي")
"""

import os
import sys
import json
import re
import hashlib
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    total = 0
    passed = 0
    failed = 0

    def check(name, condition, extra=""):
        nonlocal total, passed, failed
        total += 1
        if condition:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            failed += 1
            print(f"  [FAIL] {name}: {extra}")

    print("\n--- Testing Item #1: Daily Habits Native Android Widget ---")

    # 1. strings.xml
    strings_path = os.path.join(REPO_ROOT, "android/app/src/main/res/values/strings.xml")
    check("strings.xml exists", os.path.isfile(strings_path))
    with open(strings_path, "r", encoding="utf-8") as f:
        strings_content = f.read()
    check("strings.xml has widget_daily_habits_title", "widget_daily_habits_title" in strings_content)
    check("strings.xml has widget_habits_header", "widget_habits_header" in strings_content)
    check("strings.xml has widget_habits_empty", "widget_habits_empty" in strings_content)
    check("strings.xml contains valid Arabic wording for habits", "عادات اليوم" in strings_content)

    # 2. widget_daily_habits.xml
    layout_path = os.path.join(REPO_ROOT, "android/app/src/main/res/layout/widget_daily_habits.xml")
    check("widget_daily_habits.xml exists", os.path.isfile(layout_path))
    if os.path.isfile(layout_path):
        tree = ET.parse(layout_path)
        root = tree.getroot()
        check("layout root is LinearLayout", root.tag == "LinearLayout")
        with open(layout_path, "r", encoding="utf-8") as f:
            layout_content = f.read()
        check("layout has widget_habits_root", "@+id/widget_habits_root" in layout_content)
        check("layout has widget_habits_badge", "@+id/widget_habits_badge" in layout_content)
        check("layout has widget_habits_progress_bar", "@+id/widget_habits_progress_bar" in layout_content)
        check("layout has slot rows 1..3", "@+id/widget_habit_row_1" in layout_content and "@+id/widget_habit_row_3" in layout_content)
        check("layout has status text views 1..3", "@+id/widget_habit_status_1" in layout_content and "@+id/widget_habit_status_3" in layout_content)
        check("layout has streak text views 1..3", "@+id/widget_habit_streak_1" in layout_content and "@+id/widget_habit_streak_3" in layout_content)
        check("layout has widget_habits_empty", "@+id/widget_habits_empty" in layout_content)

    # 3. widget_daily_habits_info.xml
    info_path = os.path.join(REPO_ROOT, "android/app/src/main/res/xml/widget_daily_habits_info.xml")
    check("widget_daily_habits_info.xml exists", os.path.isfile(info_path))
    if os.path.isfile(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            info_content = f.read()
        check("info points to widget_daily_habits", "@layout/widget_daily_habits" in info_content)
        check("info references widget_daily_habits_description", "@string/widget_daily_habits_description" in info_content)
        check("info category is home_screen", 'widgetCategory="home_screen"' in info_content)

    # 4. DailyHabitsWidgetProvider.kt
    provider_path = os.path.join(REPO_ROOT, "android/app/src/main/java/com/zatoona/app/DailyHabitsWidgetProvider.kt")
    check("DailyHabitsWidgetProvider.kt exists", os.path.isfile(provider_path))
    if os.path.isfile(provider_path):
        with open(provider_path, "r", encoding="utf-8") as f:
            prov_content = f.read()
        check("extends AppWidgetProvider", "class DailyHabitsWidgetProvider : AppWidgetProvider()" in prov_content)
        check("has loadWidgetData method", "fun loadWidgetData(" in prov_content)
        check("has updateAppWidget method", "fun updateAppWidget(" in prov_content)
        check("has updateAllWidgets method", "fun updateAllWidgets(" in prov_content)
        check("reads KEY_DAILY_HABITS_CACHE", "KEY_DAILY_HABITS_CACHE" in prov_content)
        check("sets progress bar on RemoteViews", "setProgressBar(R.id.widget_habits_progress_bar" in prov_content)
        check("handles empty state and slots", "widget_habit_row_1" in prov_content and "widget_habits_empty" in prov_content)
        check("creates schedule intent on widget click", 'putExtra(ZatoonaNotificationManager.EXTRA_MODE, "schedule")' in prov_content)

    # 5. ZatoonaBridge.kt methods
    bridge_path = os.path.join(REPO_ROOT, "android/app/src/main/java/com/zatoona/app/ZatoonaBridge.kt")
    with open(bridge_path, "r", encoding="utf-8") as f:
        bridge_content = f.read()
    check("ZatoonaBridge has KEY_DAILY_HABITS_CACHE", "KEY_DAILY_HABITS_CACHE" in bridge_content)
    check("ZatoonaBridge has syncDailyHabits @JavascriptInterface", "fun syncDailyHabits(" in bridge_content)
    check("ZatoonaBridge has getDailyHabitsCache @JavascriptInterface", "fun getDailyHabitsCache(" in bridge_content)
    check("ZatoonaBridge triggers DailyHabitsWidgetProvider.updateAllWidgets", "DailyHabitsWidgetProvider.updateAllWidgets(context)" in bridge_content)
    check("ZatoonaBridge enforces schemaVersion check", 'obj.optString("schemaVersion"' in bridge_content)

    # 6. AndroidManifest.xml & proguard-rules.pro
    manifest_path = os.path.join(REPO_ROOT, "android/app/src/main/AndroidManifest.xml")
    with open(manifest_path, "r", encoding="utf-8") as f:
        man_content = f.read()
    check("AndroidManifest registers DailyHabitsWidgetProvider", "DailyHabitsWidgetProvider" in man_content)
    check("DailyHabitsWidgetProvider filter has APPWIDGET_UPDATE", "android.appwidget.action.APPWIDGET_UPDATE" in man_content)

    proguard_path = os.path.join(REPO_ROOT, "android/app/proguard-rules.pro")
    with open(proguard_path, "r", encoding="utf-8") as f:
        prog_content = f.read()
    check("proguard keeps DailyHabitsWidgetProvider", "DailyHabitsWidgetProvider" in prog_content)

    print("\n--- Testing Item #1 & Item #3 in index.html ---")
    html_path = os.path.join(REPO_ROOT, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Item #1 PWA Bridge sync
    check("index.html has syncDailyHabitsToNativeBridge", "function syncDailyHabitsToNativeBridge(" in html)
    check("addCustomHabit calls syncDailyHabitsToNativeBridge", "saveCustomHabitsList(list);\n  renderCustomHabitsTracker();\n  try { syncDailyHabitsToNativeBridge();" in html)
    check("deleteCustomHabit calls syncDailyHabitsToNativeBridge", "saveCustomHabitsList(list);\n  renderCustomHabitsTracker();\n  try { syncDailyHabitsToNativeBridge();" in html)
    check("toggleCustomHabit calls syncDailyHabitsToNativeBridge", "try { syncDailyHabitsToNativeBridge(iso);" in html)
    check("initNotificationScheduler calls syncDailyHabitsToNativeBridge", "syncDailyHabitsToNativeBridge(); } catch(e){ console.warn('[native-bridge] habits sync error:" in html)
    check("window exports syncDailyHabitsToNativeBridge", "window.syncDailyHabitsToNativeBridge = syncDailyHabitsToNativeBridge" in html)

    # Item #3 Local AI Coach
    check("overviewView has #aiCoachCard", 'id="aiCoachCard"' in html)
    check("KNOWN_KEY_PATTERNS contains ai-coach-settings", "/^ai-coach-settings$/" in html)
    check("has AI_COACH_SETTINGS_DEFAULT with enabled=false (opt-in)", "enabled: false" in html)
    check("has loadAiCoachSettings", "function loadAiCoachSettings(" in html)
    check("has saveAiCoachSettings", "function saveAiCoachSettings(" in html)
    check("has analyzeDailyWellnessStats", "function analyzeDailyWellnessStats(" in html)
    check("analyzeDailyWellnessStats inspects worship", "worship: {" in html and "fardDone" in html)
    check("analyzeDailyWellnessStats inspects nutrition & water", "waterTarget: 8" in html and "proteinTarget:" in html)
    check("analyzeDailyWellnessStats inspects gym & rest days", "isRestDay" in html and "warmupDone" in html)
    check("analyzeDailyWellnessStats inspects sleep & winddown", "sleepH" in html and "winddownDone" in html)
    check("analyzeDailyWellnessStats inspects habits", "doneHabitsCount" in html)
    check("has generateLocalAiAdvice", "function generateLocalAiAdvice(" in html)
    check("generateLocalAiAdvice supports Egyptian Arabic tone", "يا بطل" in html and "عاش يا وحش" in html)
    check("has generateAiCoachAdvice", "async function generateAiCoachAdvice(" in html)
    check("generateAiCoachAdvice supports optional Gemini API with local fallback", "generativelanguage.googleapis.com" in html and "local-fallback" in html)
    check("has renderAiCoachCard", "function renderAiCoachCard(" in html)
    check("renderAiCoachCard includes opt-in privacy explanation", "ضمان الخصوصية والتشغيل المحلي" in html)
    check("renderAiCoachCard supports category chips (all, prayer, gym, nutrition, sleep, habits)", 'data-cat="all"' in html and 'data-cat="prayer"' in html and 'data-cat="gym"' in html and 'data-cat="nutrition"' in html and 'data-cat="sleep"' in html and 'data-cat="habits"' in html)
    check("renderOverview calls renderAiCoachCard", "renderDailySummaryShareCard();\n  renderAiCoachCard();\n  renderReminders();" in html)
    check("window exports AI coach functions", "window.loadAiCoachSettings = loadAiCoachSettings" in html and "window.analyzeDailyWellnessStats = analyzeDailyWellnessStats" in html and "window.generateAiCoachAdvice = generateAiCoachAdvice" in html and "window.renderAiCoachCard = renderAiCoachCard" in html)

    print("\n--- Testing 3-Way HTML Parity ---")
    files = [
        "index.html",
        "zatoona.html",
        "android/app/src/main/assets/index.html"
    ]
    hashes = {}
    sizes = {}
    for p in files:
        full_p = os.path.join(REPO_ROOT, p)
        check(f"Parity file exists: {p}", os.path.isfile(full_p))
        if os.path.isfile(full_p):
            with open(full_p, "rb") as f:
                content = f.read()
            h = hashlib.sha256(content).hexdigest()
            hashes[p] = h
            sizes[p] = len(content)

    all_sizes_match = len(set(sizes.values())) == 1 and len(sizes) == 3
    all_hashes_match = len(set(hashes.values())) == 1 and len(hashes) == 3
    check("All 3 HTML files have identical sizes", all_sizes_match, f"Sizes: {sizes}")
    check("All 3 HTML files have identical SHA-256 hashes", all_hashes_match, f"Hashes: {hashes}")

    print(f"\n==========================================")
    print(f"Results: {passed} / {total} PASS ({failed} failed)")
    print(f"==========================================")

    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

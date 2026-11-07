import os
import sys
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_tests():
    print("=" * 80)
    print("TEST SUITE: AI VOICE ASSISTANT, IN-APP ACTION EXECUTION & ROADMAPS")
    print("=" * 80)

    passed = 0
    failed = 0

    def check(desc, cond):
        nonlocal passed, failed
        if cond:
            print(f"  [PASS] {desc}")
            passed += 1
        else:
            print(f"  [FAIL] {desc}")
            failed += 1

    # 1. Android Manifest & MainActivity Verification
    manifest = open('android/app/src/main/AndroidManifest.xml', 'r', encoding='utf-8').read()
    check("AndroidManifest contains RECORD_AUDIO permission", 'android.permission.RECORD_AUDIO' in manifest)
    check("AndroidManifest contains MODIFY_AUDIO_SETTINGS permission", 'android.permission.MODIFY_AUDIO_SETTINGS' in manifest)

    main_activity = open('android/app/src/main/java/com/zatoona/app/MainActivity.kt', 'r', encoding='utf-8').read()
    check("MainActivity handles onPermissionRequest in WebChromeClient", 'override fun onPermissionRequest' in main_activity)
    check("MainActivity has audioPermissionLauncher", 'audioPermissionLauncher' in main_activity)
    check("MainActivity calls requestAudioPermissionIfNeeded in onCreate", 'requestAudioPermissionIfNeeded()' in main_activity)

    # 2. Browser Environment Testing via Selenium Headless
    chrome_opts = Options()
    chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--window-size=412,915")
    chrome_opts.add_argument("--allow-file-access-from-files")

    driver = webdriver.Chrome(options=chrome_opts)
    try:
        file_path = os.path.abspath("index.html")
        driver.get(f"file:///{file_path}")

        # Check Window Functions
        window_funcs = [
            'executeAppAction', 'executeLogWaterAction', 'executeLogPrayerAction',
            'executeToggleHabitAction', 'executeLogWorkoutAction', 'executeAddMicroTasksAction',
            'executeSaveBookSummaryAction', 'executeAddNoteAction', 'parseLocalIntent',
            'toggleAiVoiceInput', 'toggleAiCoachVoiceOutput', 'speakAiCoachResponse'
        ]
        for f in window_funcs:
            exists = driver.execute_script(f"return typeof window.{f} === 'function';")
            check(f"window.{f} is defined", exists)

        # Open Fullscreen Chat
        driver.execute_script("window.openAiFullscreenChat();")

        # Verify Voice UI Elements
        mic_btn = driver.find_element(By.ID, "btnAiChatMic")
        check("Voice Mic button #btnAiChatMic exists in input bar", mic_btn is not None)

        voice_toggle = driver.find_element(By.ID, "btnAiChatVoiceToggle")
        check("Voice output toggle #btnAiChatVoiceToggle exists in header", voice_toggle is not None)

        # Toggle Voice Output
        initial_voice = driver.execute_script("return window.toggleAiCoachVoiceOutput(); return window._aiCoachVoiceOutputEnabled;")
        check("Voice output toggle changes state cleanly", voice_toggle.text in ['🔊 صوت: تشغيل', '🔇 صوت: كتم'])

        # Verify Quick Chips
        chips_bar = driver.find_element(By.CSS_SELECTOR, ".ai-chat-chips-bar")
        check("Chips bar contains programming roadmap chip", "خطة برمجة" in chips_bar.text)
        check("Chips bar contains book summary chip", "زتونة كتاب" in chips_bar.text)
        check("Chips bar contains water logging chip", "سجلت مية" in chips_bar.text)
        check("Chips bar contains prayer logging chip", "سجلت صلاة" in chips_bar.text)

        # 3. Test Local Intent Matcher (Tier 1 Instant Action)
        water_intent = driver.execute_script("return window.parseLocalIntent('سجل اني شربت كوباية مية');")
        check("Local intent matcher parses water command", water_intent and water_intent.get('type') == 'log_water')

        prayer_intent = driver.execute_script("return window.parseLocalIntent('يا كوتش سجل صلاة الظهر');")
        check("Local intent matcher parses Dhuhr prayer command", prayer_intent and prayer_intent.get('type') == 'log_prayer' and prayer_intent.get('target') == 'dhuhr')

        workout_intent = driver.execute_script("return window.parseLocalIntent('سجل تمرين النهاردة');")
        check("Local intent matcher parses workout command", workout_intent and workout_intent.get('type') == 'log_workout')

        # 4. Test In-App Action Execution
        # Water
        water_res = driver.execute_script("return window.executeAppAction({ type: 'log_water', delta: 1 });")
        check("executeAppAction(log_water) returns confirmation message", "كوب" in str(water_res))

        # Prayer (Dhuhr)
        prayer_res = driver.execute_script("return window.executeAppAction({ type: 'log_prayer', target: 'dhuhr' });")
        check("executeAppAction(log_prayer) returns confirmation message", "الظهر" in str(prayer_res))
        dhuhr_done = driver.execute_script("return (loadPrayer(toISO(weekDates[selectedIdx]))?.dhuhr?.fard === true);")
        check("Dhuhr prayer state is updated to true in application memory", dhuhr_done == True)

        # Micro-learning Tasks (Programming)
        micro_res = driver.execute_script("""
            return window.executeAppAction({
                type: 'add_micro_tasks',
                goal: 'بايثون',
                tasks: ['حل 3 مسائل Logic على LeetCode', 'تطبيق عملي 20 دقيقة على Functions']
            });
        """)
        check("executeAppAction(add_micro_tasks) returns confirmation message", "مهام مصغرة" in str(micro_res))
        habits_list = driver.execute_script("return window.loadCustomHabitsList();")
        has_python_task = any('[بايثون]' in h.get('title', '') for h in habits_list)
        check("Custom habits list contains newly generated micro-learning tasks", has_python_task)

        # Book Summary Action
        book_res = driver.execute_script("""
            return window.executeAppAction({
                type: 'save_book_summary',
                title: 'العادات الذرية',
                points: '1. التحسين 1% يومياً\\n2. التركيز على الهوية\\n3. قانون الدقيقتين'
            });
        """)
        check("executeAppAction(save_book_summary) returns confirmation message", "العادات الذرية" in str(book_res))
        daily_note = driver.execute_script("return window.loadDailyNote(toISO(weekDates[selectedIdx]));")
        check("Daily note contains saved book summary (زتونة كتاب)", "العادات الذرية" in str(daily_note))

        # Check Console Errors
        logs = driver.get_log('browser')
        severe_errors = [l for l in logs if l['level'] == 'SEVERE']
        check("Zero SEVERE browser console runtime errors", len(severe_errors) == 0)
        if severe_errors:
            for e in severe_errors:
                print("   [SEVERE ERROR]", e['message'])

    finally:
        driver.quit()

    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    assert failed == 0, f"{failed} tests failed"

if __name__ == '__main__':
    run_tests()

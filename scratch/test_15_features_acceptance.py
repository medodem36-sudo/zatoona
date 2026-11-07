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
    print("TEST SUITE: 15 HYPER-FRESH FEATURES FULL ACCEPTANCE AUDIT")
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

    # 1. Native Checks in Android
    alarm_code = open('android/app/src/main/java/com/zatoona/app/AlarmActivity.kt', 'r', encoding='utf-8').read()
    check("598. AlarmActivity has Accelerometer SensorEventListener for Flip-to-Snooze", 'sensorListener' in alarm_code and 'Sensor.TYPE_ACCELEROMETER' in alarm_code)

    main_code = open('android/app/src/main/java/com/zatoona/app/MainActivity.kt', 'r', encoding='utf-8').read()
    check("591. MainActivity has MediaSession for Bluetooth headset media buttons", 'MediaSession' in main_code and 'onNativeMediaButtonPressed' in main_code)

    # 2. Browser Environment Verification via Headless Chrome
    chrome_opts = Options()
    chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--window-size=412,915")
    chrome_opts.add_argument("--allow-file-access-from-files")

    driver = webdriver.Chrome(options=chrome_opts)
    try:
        file_path = os.path.abspath("index.html")
        driver.get(f"file:///{file_path}")

        # Check All 15 Feature Functions on window
        feature_funcs = [
            'toggleWakeWordHandsFree',            # 401
            'loadAiCoachProfileMemory',          # 408
            'saveAiCoachProfileMemory',          # 408
            'openAiProfileMemoryModal',          # 408
            'parseLocalIntent',                  # 411
            'openProcrastinationNegotiatorModal',# 412
            'acceptMicroCommitment',             # 412
            'auditAndRepairZatoonaState',        # 413
            'speakAiCoachResponse',              # 414
            'structureVoiceNoteToMarkdown',      # 419
            'loadQadaState',                     # 469
            'saveQadaState',                     # 469
            'logQadaFastingDay',                 # 469
            'logQadaPrayerRepaid',               # 469
            'openWorshipQadaModal',              # 469
            'openGymRecoveryHeatmapModal',        # 481
            'playPinkNoise',                     # 530
            'playAmbientSoundWithTimer',         # 530
            'openMonkMode',                      # 541
            'closeMonkMode',                     # 541
            'toggleMonkTimer',                   # 541
            'openJustStartModal',                # 551
            'toggleJustStartCountdown',          # 551
            'onNativeMediaButtonPressed',        # 591
            'showZatoonaDiagnostics',            # 600
            'exportZatoonaFullBackup',           # 600
            'runSelfHealingAuditUI'              # 600
        ]

        for fn in feature_funcs:
            exists = driver.execute_script(f"return typeof window.{fn} === 'function';")
            check(f"Function window.{fn} exists", exists)

        # 401. Wake Word Toggle in Chat Header
        driver.execute_script("window.openAiFullscreenChat();")
        wake_btn = driver.find_element(By.ID, "btnWakeWordToggle")
        check("401. Wake Word toggle button exists in header", wake_btn is not None)
        driver.execute_script("window.toggleWakeWordHandsFree();")
        check("401. Wake Word state toggled to active", "مفعّل" in wake_btn.text)
        driver.execute_script("window.toggleWakeWordHandsFree();")

        # 408. Long-Term Profile Memory
        initial_mem = driver.execute_script("return window.loadAiCoachProfileMemory();")
        check("408. Profile Memory loads defaults", initial_mem and 'workoutSplit' in initial_mem)
        driver.execute_script("""
            var m = window.loadAiCoachProfileMemory();
            m.injuries = 'ألم طفيف في الكوع الأيمن';
            window.saveAiCoachProfileMemory(m);
        """)
        updated_mem = driver.execute_script("return window.loadAiCoachProfileMemory();")
        check("408. Profile Memory persists custom facts", updated_mem.get('injuries') == 'ألم طفيف في الكوع الأيمن')

        # 411. Bilingual Code-Switching
        intent_monk = driver.execute_script("return window.parseLocalIntent('monk mode');")
        check("411. parseLocalIntent recognizes English tech term 'monk mode'", intent_monk and intent_monk.get('type') == 'open_monk_mode')
        intent_noise = driver.execute_script("return window.parseLocalIntent('pink noise');")
        check("411. parseLocalIntent recognizes 'pink noise'", intent_noise and intent_noise.get('type') == 'play_ambient_noise')
        intent_heatmap = driver.execute_script("return window.parseLocalIntent('muscle heatmap');")
        check("411. parseLocalIntent recognizes 'muscle heatmap'", intent_heatmap is not None)

        # 412. Anti-Procrastination Negotiator
        driver.execute_script("window.openProcrastinationNegotiatorModal('حل مسألة كود 5 دقائق');")
        neg_modal = driver.find_element(By.ID, "procrastinationNegotiatorModal")
        check("412. Negotiator modal opens", neg_modal.is_displayed())
        driver.execute_script("window.acceptMicroCommitment();")
        check("412. Accepting micro-commitment closes modal and logs habit", not neg_modal.is_displayed())

        # 413. Self-Healing State Diagnostic Agent
        heal_res = driver.execute_script("return window.auditAndRepairZatoonaState();")
        check("413. Self-Healing audit runs cleanly", heal_res and heal_res.get('success') == True)
        check("413. Self-Healing scanned localStorage keys", heal_res.get('keysChecked', 0) > 0)

        # 419. Voice Note Structuring
        structured = driver.execute_script("""
            return window.structureVoiceNoteToMarkdown('فكرة تطبيق جديد لمتابعة الأوراد، محتاج أصمم الواجهة، وأكتب الكود، وأشتري دومين');
        """)
        check("419. Voice Note structuring outputs Markdown headers", 'الفكرة الجوهرية' in structured and 'Action Items' in structured)

        # 469. Qada Prayer & Fasting Repayment
        driver.execute_script("window.openWorshipQadaModal();")
        qada_modal = driver.find_element(By.ID, "worshipQadaModal")
        check("469. Qada modal opens", qada_modal.is_displayed())
        driver.execute_script("window.logQadaFastingDay(2);")
        qada_state = driver.execute_script("return window.loadQadaState();")
        check("469. Qada fasting days counter incremented", qada_state.get('fastingDays') >= 2)
        driver.execute_script("window.closeWorshipQadaModal();")

        # 481. Muscle Heatmap Modal
        driver.execute_script("window.openGymRecoveryHeatmapModal();")
        heat_modal = driver.find_element(By.ID, "gymRecoveryHeatmapModal")
        check("481. Gym Recovery Heatmap modal opens", heat_modal.is_displayed())
        driver.execute_script("document.getElementById('gymRecoveryHeatmapModal').classList.remove('open');")

        # 530. Pink Noise & Ambient Sound
        pink_test = driver.execute_script("""
            try {
                window.playPinkNoise();
                return true;
            } catch(e) {
                return false;
            }
        """)
        check("530. playPinkNoise executes without error", pink_test)

        # 541. Monk Mode Fullscreen Isolation
        driver.execute_script("window.openMonkMode('مهمة برمجية مركزة');")
        monk_overlay = driver.find_element(By.ID, "monkModeOverlay")
        check("541. Monk Mode overlay opens fullscreen", monk_overlay.is_displayed())
        monk_title = driver.find_element(By.ID, "monkTaskTitle")
        check("541. Monk Mode reflects priority task", "مهمة برمجية مركزة" in monk_title.text)
        driver.execute_script("window.closeMonkMode();")
        check("541. Monk Mode closes cleanly", not monk_overlay.is_displayed())

        # 551. 1-Minute Just-Start Timer
        driver.execute_script("window.openJustStartModal();")
        just_modal = driver.find_element(By.ID, "justStartModal")
        check("551. 1-Minute Just-Start modal opens", just_modal.is_displayed())
        driver.execute_script("window.closeJustStartModal();")

        # 591. Native Bluetooth Headset Media Button
        media_test = driver.execute_script("""
            try {
                window.onNativeMediaButtonPressed();
                return true;
            } catch(e) {
                return false;
            }
        """)
        check("591. onNativeMediaButtonPressed handles headset click cleanly", media_test)

        # 600. Standalone Diagnostics & Backup
        driver.execute_script("window.showZatoonaDiagnostics();")
        diag_modal = driver.find_element(By.ID, "diagnosticsModal")
        check("600. Standalone Diagnostics modal opens", diag_modal.is_displayed())
        report_text = driver.find_element(By.ID, "diagnosticsReportBody").text
        check("600. Diagnostics report shows zero external dependency status", "مستقل" in report_text and "أوفلاين" in report_text)
        driver.execute_script("window.closeZatoonaDiagnostics();")

        # Zero SEVERE Console Errors
        logs = driver.get_log('browser')
        severe_errors = [l for l in logs if l['level'] == 'SEVERE']
        check("Zero SEVERE browser console runtime errors across all 15 features", len(severe_errors) == 0)
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

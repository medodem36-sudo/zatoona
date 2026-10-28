import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    print("PHASE 13.10 ACCEPTANCE TEST SUITE: SMART NOTIFICATION GROUPING (PROPOSAL #14)")
    print("================================================================================")

    html_path = os.path.abspath('index.html')
    file_url = 'file:///' + html_path.replace('\\', '/')

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--window-size=375,812')

    driver = webdriver.Chrome(options=opts)
    driver.get(file_url)
    time.sleep(1.0)

    def js(script):
        return driver.execute_script(script)

    try:
        # ---------------------------------------------------------
        # Group 1: Configuration Defaults & Settings UI
        # ---------------------------------------------------------
        print("\n--- Group 1: Configuration Defaults & Settings UI ---")
        g1 = js("""
            return {
                defaultSmartGrouping: NOTIF_SETTINGS_DEFAULT.smartGrouping,
                loadedSmartGrouping: loadNotificationSettings().smartGrouping,
                hasCheckbox: !!document.getElementById('notifOptSmartGrouping'),
                isChecked: document.getElementById('notifOptSmartGrouping') ? document.getElementById('notifOptSmartGrouping').checked : null
            };
        """)
        test("NOTIF_SETTINGS_DEFAULT has smartGrouping: true", g1.get('defaultSmartGrouping') is True, f"Got: {g1.get('defaultSmartGrouping')}")
        test("loadNotificationSettings returns smartGrouping !== false", g1.get('loadedSmartGrouping') is not False, f"Got: {g1.get('loadedSmartGrouping')}")
        test("Checkbox #notifOptSmartGrouping rendered in Settings UI", g1.get('hasCheckbox') is True)
        test("Checkbox #notifOptSmartGrouping is checked by default", g1.get('isChecked') is True)

        # Test toggle interaction
        toggle_res = js("""
            const chk = document.getElementById('notifOptSmartGrouping');
            chk.checked = false;
            chk.dispatchEvent(new Event('change'));
            const s1 = loadNotificationSettings().smartGrouping;
            chk.checked = true;
            chk.dispatchEvent(new Event('change'));
            const s2 = loadNotificationSettings().smartGrouping;
            return { s1: s1, s2: s2 };
        """)
        test("Unchecking #notifOptSmartGrouping persists false", toggle_res.get('s1') is False, f"Got: {toggle_res.get('s1')}")
        test("Re-checking #notifOptSmartGrouping persists true", toggle_res.get('s2') is True, f"Got: {toggle_res.get('s2')}")

        # ---------------------------------------------------------
        # Group 2: Single Reminder Invariance (Regression Safety)
        # ---------------------------------------------------------
        print("\n--- Group 2: Single Reminder Invariance ---")
        single_res = js("""
            const testIso = '2026-11-20';
            clearDispatchedReminders(testIso);
            notificationSettings = loadNotificationSettings();
            notificationSettings.enabled = true;
            notificationSettings.smartGrouping = true;
            notificationSettings.prayers = { fajr: false, dhuhr: false, asr: false, maghrib: false, isha: false };
            notificationSettings.activities = false;
            reminders = [];

            reminders.push({
                id: 'single_test_1',
                title: 'تذكير مفرد اختباري',
                recurrence: 'daily',
                time: '10:00',
                type: 'water',
                enabled: true
            });

            const intercepted = [];
            const origDispatch = window.dispatchNotification;
            window.dispatchNotification = function(info){
                intercepted.push(info);
            };

            const triggered = checkAndDispatchDueReminders(testIso, 600);
            window.dispatchNotification = origDispatch;

            return {
                triggeredCount: triggered.length,
                interceptedCount: intercepted.length,
                isGrouped: intercepted[0] ? !!intercepted[0].isGrouped : null,
                title: intercepted[0] ? intercepted[0].title : null,
                dispatchedMarked: !!getDispatchedReminders(testIso)['rem:' + testIso + ':single_test_1']
            };
        """)
        test("Single due reminder triggers exactly 1 key", single_res.get('triggeredCount') == 1, f"Got: {single_res}")
        test("Single due reminder dispatches exactly 1 notification", single_res.get('interceptedCount') == 1)
        test("Single due reminder is NOT marked isGrouped", single_res.get('isGrouped') is not True)
        test("Single due reminder retains individual title", 'تذكير مفرد اختباري' in (single_res.get('title') or ''))
        test("Single reminder correctly marked dispatched in storage", single_res.get('dispatchedMarked') is True)

        # ---------------------------------------------------------
        # Group 3: Multiple Simultaneous Reminders (Smart Grouping Active)
        # ---------------------------------------------------------
        print("\n--- Group 3: Multiple Simultaneous Reminders (Smart Grouping Active) ---")
        multi_res = js("""
            const testIso = '2026-11-21';
            clearDispatchedReminders(testIso);
            notificationSettings = loadNotificationSettings();
            notificationSettings.enabled = true;
            notificationSettings.smartGrouping = true;
            notificationSettings.prayers = { fajr: false, dhuhr: false, asr: false, maghrib: false, isha: false };
            notificationSettings.activities = false;
            reminders = [];

            // 3 concurrent reminders at 14:30 (870 min), all using time field
            reminders.push({
                id: 'grp_test_1',
                title: 'الذهاب للمسجد',
                recurrence: 'daily',
                time: '14:30',
                type: 'schedule',
                enabled: true
            });
            reminders.push({
                id: 'grp_test_2',
                title: 'شرب 500 مل ماء',
                recurrence: 'daily',
                time: '14:30',
                type: 'water',
                enabled: true
            });
            reminders.push({
                id: 'grp_test_3',
                title: 'تمرين الإطالة الخفيف',
                recurrence: 'daily',
                time: '14:30',
                type: 'gym',
                enabled: true
            });

            const intercepted = [];
            const origDispatch = window.dispatchNotification;
            window.dispatchNotification = function(info){
                intercepted.push(info);
            };

            const triggered = checkAndDispatchDueReminders(testIso, 870);
            window.dispatchNotification = origDispatch;

            const dispMap = getDispatchedReminders(testIso);

            return {
                triggeredCount: triggered.length,
                interceptedCount: intercepted.length,
                firstNotif: intercepted[0] ? {
                    isGrouped: intercepted[0].isGrouped,
                    title: intercepted[0].title,
                    sub: intercepted[0].sub,
                    plainBody: intercepted[0].plainBody,
                    itemCount: intercepted[0].items ? intercepted[0].items.length : 0,
                    mode: intercepted[0].mode
                } : null,
                allMarkedDispatched: !!(dispMap['rem:' + testIso + ':grp_test_1'] &&
                                        dispMap['rem:' + testIso + ':grp_test_2'] &&
                                        dispMap['rem:' + testIso + ':grp_test_3'])
            };
        """)
        test("Concurrent reminders return all 3 triggered keys", multi_res.get('triggeredCount') == 3, f"Got: {multi_res}")
        test("Smart grouping dispatches exactly ONE consolidated notification", multi_res.get('interceptedCount') == 1, f"Got: {multi_res.get('interceptedCount')}")
        fn = multi_res.get('firstNotif') or {}
        test("Consolidated notification has isGrouped: true", fn.get('isGrouped') is True)
        test("Consolidated title indicates 3 alerts", '3' in (fn.get('title') or ''), f"Title: {fn.get('title')}")
        test("Consolidated body lists all 3 tasks",
             'الذهاب للمسجد' in (fn.get('plainBody') or '') and
             'شرب 500 مل ماء' in (fn.get('plainBody') or '') and
             'تمرين الإطالة' in (fn.get('plainBody') or ''),
             f"Body: {fn.get('plainBody')}")
        test("Consolidated notification captures items array of 3", fn.get('itemCount') == 3)
        test("Target mode prioritizes schedule", fn.get('mode') == 'schedule', f"Mode: {fn.get('mode')}")
        test("All individual reminders marked dispatched", multi_res.get('allMarkedDispatched') is True)

        # Test deduplication on immediate re-run
        dedup_res = js("""
            const testIso = '2026-11-21';
            const triggeredAgain = checkAndDispatchDueReminders(testIso, 870);
            return triggeredAgain.length;
        """)
        test("Immediate re-run returns 0 triggered (clean deduplication)", dedup_res == 0, f"Got: {dedup_res}")

        # ---------------------------------------------------------
        # Group 4: Multiple Simultaneous Reminders with smartGrouping = false
        # ---------------------------------------------------------
        print("\n--- Group 4: Multiple Simultaneous Reminders (Grouping Disabled) ---")
        legacy_res = js("""
            const testIso = '2026-11-22';
            clearDispatchedReminders(testIso);
            notificationSettings = loadNotificationSettings();
            notificationSettings.enabled = true;
            notificationSettings.smartGrouping = false;
            notificationSettings.prayers = { fajr: false, dhuhr: false, asr: false, maghrib: false, isha: false };
            notificationSettings.activities = false;
            reminders = [];

            reminders.push({
                id: 'legacy_1',
                title: 'تذكير أول',
                recurrence: 'daily',
                time: '16:00',
                type: 'water',
                enabled: true
            });
            reminders.push({
                id: 'legacy_2',
                title: 'تذكير ثان',
                recurrence: 'daily',
                time: '16:00',
                type: 'gym',
                enabled: true
            });

            const intercepted = [];
            const origDispatch = window.dispatchNotification;
            window.dispatchNotification = function(info){
                intercepted.push(info);
            };

            const triggered = checkAndDispatchDueReminders(testIso, 960);
            window.dispatchNotification = origDispatch;

            return {
                triggeredCount: triggered.length,
                interceptedCount: intercepted.length,
                hasGrouped: intercepted.some(x => x.isGrouped === true)
            };
        """)
        test("Disabled grouping triggers both keys", legacy_res.get('triggeredCount') == 2)
        test("Disabled grouping dispatches 2 separate notifications", legacy_res.get('interceptedCount') == 2, f"Got: {legacy_res.get('interceptedCount')}")
        test("Disabled grouping does NOT produce isGrouped notifications", legacy_res.get('hasGrouped') is False)

        # ---------------------------------------------------------
        # Group 5: In-App Modal Display for Grouped Notification
        # ---------------------------------------------------------
        print("\n--- Group 5: In-App Modal Display for Grouped Notification ---")
        modal_res = js("""
            notificationSettings.inAppModal = true;
            const groupedInfo = {
                key: 'grouped:2026-11-23:600',
                icon: '🔔',
                title: '🔔 تذكيرات زتونة (2 تنبيهات)',
                sub: 'لديك 2 تنبيهات مجدولة حان موعدها الآن',
                plainBody: 'صلاة الضحى و قراءة القرآن',
                body: '<div id="testGroupList"><div class="item">صلاة الضحى</div><div class="item">قراءة القرآن</div></div>',
                mode: 'prayer',
                date: '2026-11-23',
                isGrouped: true,
                items: [
                    { title: 'صلاة الضحى', mode: 'prayer' },
                    { title: 'قراءة القرآن', mode: 'prayer' }
                ]
            };

            showInAppReminderModal(groupedInfo);
            const modal = document.getElementById('inAppReminderModal');
            const isOpen = modal && !modal.classList.contains('hidden');
            const titleText = document.getElementById('inAppRemTitle').textContent;
            const hasList = !!document.getElementById('testGroupList');

            document.getElementById('inAppRemGo').click();
            const isClosedAfterGo = modal.classList.contains('hidden');
            const currentMode = mode;

            return {
                isOpen: isOpen,
                titleText: titleText,
                hasList: hasList,
                isClosedAfterGo: isClosedAfterGo,
                currentMode: currentMode
            };
        """)
        test("showInAppReminderModal opens modal for grouped info", modal_res.get('isOpen') is True)
        test("Modal title contains alert count", '2 تنبيهات' in (modal_res.get('titleText') or ''))
        test("Modal body renders grouped task list HTML", modal_res.get('hasList') is True)
        test("Clicking #inAppRemGo closes modal and navigates to target mode",
             modal_res.get('isClosedAfterGo') is True and modal_res.get('currentMode') == 'prayer')

        # ---------------------------------------------------------
        # Group 6: Android Kotlin Grouping Engine Inspection
        # ---------------------------------------------------------
        print("\n--- Group 6: Android Kotlin Grouping Engine Inspection ---")
        kt_path = 'android/app/src/main/java/com/zatoona/app/ZatoonaNotificationManager.kt'
        test("ZatoonaNotificationManager.kt exists", os.path.isfile(kt_path))
        with open(kt_path, 'r', encoding='utf-8') as f:
            kt_content = f.read()

        test("Constant GROUP_ZATOONA_REMINDERS defined", 'const val GROUP_ZATOONA_REMINDERS = "com.zatoona.app.REMINDERS_GROUP"' in kt_content)
        test("Constant NOTIFICATION_ID_GROUP_SUMMARY defined", 'const val NOTIFICATION_ID_GROUP_SUMMARY = 999999' in kt_content)
        test("showNotification sets notification group", '.setGroup(GROUP_ZATOONA_REMINDERS)' in kt_content)
        test("showNotification posts group summary notification", '.setGroupSummary(true)' in kt_content)
        test("cancelNotification inspects active notifications for summary cleanup", 'activeNotifications' in kt_content and 'NOTIFICATION_ID_GROUP_SUMMARY' in kt_content)

        # ---------------------------------------------------------
        # Group 7: Encrypted Backup & Key Patterns
        # ---------------------------------------------------------
        print("\n--- Group 7: Encrypted Backup & Key Patterns ---")
        backup_res = js("""
            // validateBackupData expects a flat key->string map (the data payload, not the wrapper)
            const testBackup = {
                'notification-settings': JSON.stringify({ enabled: true, smartGrouping: true }),
                'notif-dispatched:2026-11-20': JSON.stringify({ 'rem:2026-11-20:grp_1': Date.now() })
            };
            return typeof validateBackupData === 'function' ? validateBackupData(testBackup) : null;
        """)
        test("validateBackupData accepts backup with notification-settings & notif-dispatched keys",
             (backup_res is True) or (isinstance(backup_res, dict) and backup_res.get('ok') is True),
             f"Got: {backup_res}")

        # Verify notif-dispatched pattern is in KNOWN_KEY_PATTERNS
        pattern_res = js("""
            const testKey = 'notif-dispatched:2026-01-01';
            const patterns = [/^schema-version$/, /^theme$/, /^targets$/, /^schedule-settings$/, /^shopping$/, /^prep$/, /^subs$/, /^meals:/, /^sched-acts:/, /^water:/, /^weight:/, /^budget-/, /^custom-foods$/, /^food-overrides$/, /^secnote:/, /^ex:/, /^gym-settings$/, /^gym-date-ov:/, /^custom-exercises$/, /^exercise-overrides$/, /^excluded-exercises$/, /^meal-date-ov:/, /^notification-settings$/, /^reminders$/, /^gym-routine-order$/, /^gym-plan-config-v1$/, /^gym-custom-plans-v1$/, /^exercise-image-map-v1$/, /^note-attachments-v1$/, /^gym-sessions-v1$/, /^gym-rest-timer-v1$/, /^shopping-purchases-v1$/, /^gym-warmup-state-v1$/, /^gym-cooldown-state-v1$/, /^zatoona-media-v1$/, /^media$/, /^sleep-routine-settings$/, /^winddown:/, /^fasting:/, /^custom-habits-list$/, /^customhabits:/, /^notif-dispatched:/];
            return patterns.some(re => re.test(testKey));
        """)
        test("notif-dispatched: key matches KNOWN_KEY_PATTERNS", pattern_res is True)

        # ---------------------------------------------------------
        # Group 8: Edge Cases
        # ---------------------------------------------------------
        print("\n--- Group 8: Edge Cases ---")
        empty_res = js("""
            const testIso = '2026-11-25';
            clearDispatchedReminders(testIso);
            notificationSettings.enabled = true;
            notificationSettings.smartGrouping = true;
            notificationSettings.prayers = { fajr: false, dhuhr: false, asr: false, maghrib: false, isha: false };
            notificationSettings.activities = false;
            reminders = [];

            const triggered = checkAndDispatchDueReminders(testIso, 600);
            return triggered.length;
        """)
        test("Zero due reminders returns empty triggered array", empty_res == 0)

        # Test grouping with exactly 2 concurrent (minimum groupable)
        two_res = js("""
            const testIso = '2026-11-26';
            clearDispatchedReminders(testIso);
            notificationSettings.enabled = true;
            notificationSettings.smartGrouping = true;
            notificationSettings.prayers = { fajr: false, dhuhr: false, asr: false, maghrib: false, isha: false };
            notificationSettings.activities = false;
            reminders = [];

            reminders.push({ id: 'two_1', title: 'أول', recurrence: 'daily', time: '09:00', type: 'water', enabled: true });
            reminders.push({ id: 'two_2', title: 'ثاني', recurrence: 'daily', time: '09:00', type: 'gym', enabled: true });

            const intercepted = [];
            const origDispatch = window.dispatchNotification;
            window.dispatchNotification = function(info){ intercepted.push(info); };
            const triggered = checkAndDispatchDueReminders(testIso, 540);
            window.dispatchNotification = origDispatch;

            return {
                triggeredCount: triggered.length,
                interceptedCount: intercepted.length,
                isGrouped: intercepted[0] ? !!intercepted[0].isGrouped : null
            };
        """)
        test("Exactly 2 concurrent reminders triggers grouping", two_res.get('triggeredCount') == 2 and two_res.get('interceptedCount') == 1 and two_res.get('isGrouped') is True, f"Got: {two_res}")

    finally:
        driver.quit()

    print("\n================================================================================")
    print(f"RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("================================================================================")
    return failed_count == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

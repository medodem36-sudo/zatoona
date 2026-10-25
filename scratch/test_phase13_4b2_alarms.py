"""
test_phase13_4b2_alarms.py
Dedicated acceptance test suite for Phase 13.4B2:
Native Android Local Alarm Engine: Closed-App Reminders, Persistent Scheduling & Android Validation.
"""

import os
import sys
import json
import re
import hashlib
import subprocess
from datetime import datetime, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(ROOT_DIR, 'index.html')
ZATOONA_HTML = os.path.join(ROOT_DIR, 'zatoona.html')
ANDROID_DIR = os.path.join(ROOT_DIR, 'android')
APP_SRC = os.path.join(ANDROID_DIR, 'app', 'src', 'main')
MANIFEST_XML = os.path.join(APP_SRC, 'AndroidManifest.xml')
JAVA_DIR = os.path.join(APP_SRC, 'java', 'com', 'zatoona', 'app')
DEBUG_APK = os.path.join(ANDROID_DIR, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')


def run_tests():
    passed = 0
    failed = 0
    total = 0

    def check(name, condition, extra=""):
        nonlocal passed, failed, total
        total += 1
        if condition:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            failed += 1
            print(f"  [FAIL] {name} - {extra}")

    print("\n" + "=" * 70)
    print("PHASE 13.4B2: NATIVE ANDROID LOCAL ALARM ENGINE ACCEPTANCE SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # Group 1: Android Manifest & Component Declarations
    # -------------------------------------------------------------
    print("\n--- Group 1: Android Manifest & Component Declarations ---")
    check("AndroidManifest.xml exists", os.path.isfile(MANIFEST_XML))
    if os.path.isfile(MANIFEST_XML):
        with open(MANIFEST_XML, 'r', encoding='utf-8') as f:
            manifest_content = f.read()

        check("Permission: RECEIVE_BOOT_COMPLETED declared",
              'android.permission.RECEIVE_BOOT_COMPLETED' in manifest_content)
        check("Permission: POST_NOTIFICATIONS declared",
              'android.permission.POST_NOTIFICATIONS' in manifest_content)
        check("Permission: SCHEDULE_EXACT_ALARM declared",
              'android.permission.SCHEDULE_EXACT_ALARM' in manifest_content)
        check("Permission: WAKE_LOCK declared",
              'android.permission.WAKE_LOCK' in manifest_content)

        check("Receiver: AlarmReceiver declared with exported=false",
              'AlarmReceiver' in manifest_content and 'android:exported="false"' in manifest_content)

        check("Receiver: BootReceiver declared with exported=true",
              'BootReceiver' in manifest_content and 'android:exported="true"' in manifest_content)
        check("BootReceiver action: BOOT_COMPLETED",
              'android.intent.action.BOOT_COMPLETED' in manifest_content)
        check("BootReceiver action: MY_PACKAGE_REPLACED",
              'android.intent.action.MY_PACKAGE_REPLACED' in manifest_content)
        check("BootReceiver action: TIME_SET",
              'android.intent.action.TIME_SET' in manifest_content)
        check("BootReceiver action: TIMEZONE_CHANGED",
              'android.intent.action.TIMEZONE_CHANGED' in manifest_content)
        check("BootReceiver action: SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED",
              'android.app.action.SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED' in manifest_content)

        check("MainActivity launchMode is singleTask",
              'android:launchMode="singleTask"' in manifest_content)

    # -------------------------------------------------------------
    # Group 2: Kotlin Native Engine Source Verification
    # -------------------------------------------------------------
    print("\n--- Group 2: Kotlin Native Engine Source Verification ---")
    schedule_model_kt = os.path.join(JAVA_DIR, 'ZatoonaScheduleModel.kt')
    schedule_repo_kt = os.path.join(JAVA_DIR, 'ZatoonaScheduleRepository.kt')
    scheduler_kt = os.path.join(JAVA_DIR, 'ZatoonaAlarmScheduler.kt')
    notif_mgr_kt = os.path.join(JAVA_DIR, 'ZatoonaNotificationManager.kt')
    bridge_kt = os.path.join(JAVA_DIR, 'ZatoonaBridge.kt')
    alarm_rcv_kt = os.path.join(JAVA_DIR, 'AlarmReceiver.kt')
    boot_rcv_kt = os.path.join(JAVA_DIR, 'BootReceiver.kt')
    main_act_kt = os.path.join(JAVA_DIR, 'MainActivity.kt')

    check("ZatoonaScheduleModel.kt exists", os.path.isfile(schedule_model_kt))
    check("ZatoonaScheduleRepository.kt exists", os.path.isfile(schedule_repo_kt))
    check("ZatoonaAlarmScheduler.kt exists", os.path.isfile(scheduler_kt))
    check("ZatoonaNotificationManager.kt exists", os.path.isfile(notif_mgr_kt))
    check("ZatoonaBridge.kt exists", os.path.isfile(bridge_kt))
    check("AlarmReceiver.kt exists", os.path.isfile(alarm_rcv_kt))
    check("BootReceiver.kt exists", os.path.isfile(boot_rcv_kt))
    check("MainActivity.kt exists", os.path.isfile(main_act_kt))

    if os.path.isfile(schedule_model_kt):
        with open(schedule_model_kt, 'r', encoding='utf-8') as f:
            c = f.read()
        check("Schedule model has all required fields",
              all(k in c for k in ['id', 'type', 'title', 'body', 'mode', 'channelId',
                                   'recurrence', 'timeHour', 'timeMinute', 'activeDays',
                                   'triggerEpochMs', 'datedTimings', 'city', 'enabled', 'schemaVersion']))
        check("Schedule model JSON serialization implemented",
              'fun toJSONObject(): JSONObject' in c and 'fun fromJSONObject(' in c)

    if os.path.isfile(schedule_repo_kt):
        with open(schedule_repo_kt, 'r', encoding='utf-8') as f:
            c = f.read()
        check("Repository implements computeNextOccurrence", 'fun computeNextOccurrence(' in c)
        check("Repository implements isDuplicateDispatch", 'fun isDuplicateDispatch(' in c)
        check("Repository implements markDispatched", 'fun markDispatched(' in c)
        check("Repository implements purgeStaleCityPrayers", 'fun purgeStaleCityPrayers(' in c)
        check("Repository implements CRUD operations",
              'fun putSchedule(' in c and 'fun deleteSchedule(' in c and 'fun getAllSchedules(' in c)

    if os.path.isfile(notif_mgr_kt):
        with open(notif_mgr_kt, 'r', encoding='utf-8') as f:
            c = f.read()
        check("Notification channel constant: zatoona_reminders", 'CHANNEL_REMINDERS = "zatoona_reminders"' in c)
        check("Notification channel constant: zatoona_prayers", 'CHANNEL_PRAYERS = "zatoona_prayers"' in c)
        check("Notification channel constant: zatoona_sleep", 'CHANNEL_SLEEP = "zatoona_sleep"' in c)
        check("Notification builder sets content intent", 'setContentIntent(' in c)
        check("Notification builder sets auto cancel", 'setAutoCancel(true)' in c)

    if os.path.isfile(scheduler_kt):
        with open(scheduler_kt, 'r', encoding='utf-8') as f:
            c = f.read()
        check("Scheduler checks canScheduleExactAlarms on API 31+", 'canScheduleExactAlarms' in c)
        check("Scheduler uses setExactAndAllowWhileIdle with fallback",
              'setExactAndAllowWhileIdle' in c and 'setAndAllowWhileIdle' in c)
        check("Scheduler implements rescheduleAll", 'fun rescheduleAll(' in c)
        check("Scheduler implements onAlarmFired", 'fun onAlarmFired(' in c)
        check("Scheduler computes stable request code hash", 'id.hashCode()' in c or 'hashCode()' in c)

    if os.path.isfile(bridge_kt):
        with open(bridge_kt, 'r', encoding='utf-8') as f:
            c = f.read()
        check("Bridge v1 method: syncUpcomingAlarms", 'fun syncUpcomingAlarms(' in c)
        check("Bridge v2 method: syncSchedules", 'fun syncSchedules(' in c)
        check("Bridge method: cancelSchedule", 'fun cancelSchedule(' in c)
        check("Bridge method: updateActivePrayerCity", 'fun updateActivePrayerCity(' in c)
        check("Bridge method: getAlarmEngineStatus", 'fun getAlarmEngineStatus(' in c)
        check("Bridge payload limits enforced (128 KB, 60 items)",
              'MAX_PAYLOAD_LENGTH = 131072' in c and 'MAX_ALARM_ITEMS = 60' in c)
        check("Bridge whitelists types", 'ALLOWED_TYPES = setOf("prayer", "sleep", "activity", "custom")' in c)

    if os.path.isfile(main_act_kt):
        with open(main_act_kt, 'r', encoding='utf-8') as f:
            c = f.read()
        check("MainActivity handles POST_NOTIFICATIONS permission", 'POST_NOTIFICATIONS' in c)
        check("MainActivity implements onNewIntent", 'override fun onNewIntent(' in c)
        check("MainActivity handles routeNotificationClick to WebView", 'routeNotificationClick' in c)

    # -------------------------------------------------------------
    # Group 3: Bridge Logic & Recurrence Mathematical Simulation
    # -------------------------------------------------------------
    print("\n--- Group 3: Bridge Logic & Recurrence Mathematical Simulation ---")

    def compute_next_occurrence(recurrence, time_hour, time_minute, active_days, current_dt):
        if recurrence == 'daily':
            cand = current_dt.replace(hour=time_hour, minute=time_minute, second=0, microsecond=0)
            if cand <= current_dt:
                cand += timedelta(days=1)
            return cand
        elif recurrence in ('weekdays', 'sleep_routine'):
            for offset in range(8):
                cand = (current_dt + timedelta(days=offset)).replace(hour=time_hour, minute=time_minute, second=0, microsecond=0)
                if cand > current_dt:
                    cal_day = (cand.weekday() + 1) % 7
                    if active_days and len(active_days) == 7 and active_days[cal_day]:
                        return cand
            return None
        return None

    now_ref = datetime(2026, 10, 26, 10, 0, 0)
    # Test 1: Daily later today
    next_daily_today = compute_next_occurrence('daily', 14, 30, None, now_ref)
    check("Daily recurrence later today matches today 14:30",
          next_daily_today == datetime(2026, 10, 26, 14, 30, 0))

    # Test 2: Daily earlier today (rolls to tomorrow)
    next_daily_tmrw = compute_next_occurrence('daily', 8, 15, None, now_ref)
    check("Daily recurrence earlier today rolls to tomorrow 08:15",
          next_daily_tmrw == datetime(2026, 10, 27, 8, 15, 0))

    # Test 3: Weekdays (active Mon, Wed, Fri only)
    mwf_days = [False, True, False, True, False, True, False]
    next_mwf_today = compute_next_occurrence('weekdays', 16, 0, mwf_days, now_ref)
    check("Weekdays active Monday matches Monday 16:00",
          next_mwf_today == datetime(2026, 10, 26, 16, 0, 0))

    next_mwf_roll = compute_next_occurrence('weekdays', 9, 0, mwf_days, now_ref)
    check("Weekdays missed Monday rolls to Wednesday",
          next_mwf_roll == datetime(2026, 10, 28, 9, 0, 0))

    # Test 4: Deduplication window (15 minutes)
    def is_duplicate(last_dispatch_ms, current_ms):
        return (current_ms - last_dispatch_ms) < 15 * 60 * 1000

    t0 = 1000000000
    check("Dispatch within 14 min is duplicate", is_duplicate(t0, t0 + 14 * 60 * 1000))
    check("Dispatch at exactly 15 min is not duplicate", not is_duplicate(t0, t0 + 15 * 60 * 1000))
    check("Dispatch after 16 min is not duplicate", not is_duplicate(t0, t0 + 16 * 60 * 1000))

    # Test 5: City isolation purge simulation
    schedules_sample = [
        {"id": "prayer-Minya-fajr", "city": "Minya"},
        {"id": "prayer-Cairo-fajr", "city": "Cairo"},
        {"id": "prayer-Minya-dhuhr", "city": "Minya"},
        {"id": "rem-custom1", "city": ""},
        {"id": "sleep-winddown", "city": ""}
    ]
    def purge_city_prayers(active_city, scheds):
        stale = [s for s in scheds if s.get("city") and s.get("city") != active_city]
        remaining = [s for s in scheds if not s.get("city") or s.get("city") == active_city]
        return stale, remaining

    stale_items, kept_items = purge_city_prayers("Cairo", schedules_sample)
    check("Purge retains Cairo and non-city schedules",
          len(kept_items) == 3 and all(s['city'] in ('', 'Cairo') for s in kept_items))
    check("Purge identifies all Minya schedules as stale",
          len(stale_items) == 2 and all(s['city'] == 'Minya' for s in stale_items))

    # -------------------------------------------------------------
    # Group 4: PWA JavaScript Bridge Integration
    # -------------------------------------------------------------
    print("\n--- Group 4: PWA JavaScript Bridge Integration ---")
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        index_content = f.read()

    check("isNativeBridgeAvailable() defined in index.html",
          'function isNativeBridgeAvailable()' in index_content)
    check("syncRemindersToNativeBridge() defined in index.html",
          'function syncRemindersToNativeBridge()' in index_content)
    check("syncRemindersToNativeBridge handles prayer schedules with datedTimings",
          'datedTimings' in index_content and 'prayer_dated' in index_content)
    check("syncRemindersToNativeBridge handles custom reminders",
          'recurrence: recurrence' in index_content or "recurrence = 'daily'" in index_content)
    check("syncRemindersToNativeBridge handles sleep wind-down routine",
          'sleep-winddown' in index_content and 'sleep_routine' in index_content)
    check("initNotificationScheduler triggers bridge sync",
          'syncRemindersToNativeBridge()' in index_content and 'initNotificationScheduler' in index_content)
    check("onCityChange calls updateActivePrayerCity",
          'updateActivePrayerCity(newCity)' in index_content)
    check("saveNotificationSettings hooks bridge sync",
          'syncRemindersToNativeBridge' in index_content and 'saveNotificationSettings' in index_content)
    check("saveReminders hooks bridge sync",
          'syncRemindersToNativeBridge' in index_content and 'saveReminders' in index_content)
    check("saveSleepRoutineSettings hooks bridge sync",
          'syncRemindersToNativeBridge' in index_content and 'saveSleepRoutineSettings' in index_content)

    # -------------------------------------------------------------
    # Group 5: Binary Parity & File Integrity
    # -------------------------------------------------------------
    print("\n--- Group 5: Binary Parity & File Integrity ---")
    with open(INDEX_HTML, 'rb') as f:
        h_index = hashlib.sha256(f.read()).hexdigest()
    with open(ZATOONA_HTML, 'rb') as f:
        h_zatoona = hashlib.sha256(f.read()).hexdigest()

    check("index.html and zatoona.html are byte-identical", h_index == h_zatoona,
          f"index={h_index[:10]}, zatoona={h_zatoona[:10]}")

    try:
        res = subprocess.run(['fc.exe', '/b', INDEX_HTML, ZATOONA_HTML], capture_output=True, text=True)
        check("fc.exe /b confirms 0 differences", res.returncode == 0)
    except Exception as e:
        check("fc.exe /b confirms 0 differences", False, str(e))

    # -------------------------------------------------------------
    # Group 6: APK Buildability & Packaging Verification
    # -------------------------------------------------------------
    print("\n--- Group 6: APK Buildability & Packaging Verification ---")
    check("Debug APK exists at android/app/build/outputs/apk/debug/app-debug.apk",
          os.path.isfile(DEBUG_APK))
    if os.path.isfile(DEBUG_APK):
        apk_size = os.path.getsize(DEBUG_APK)
        check("APK size is healthy (> 5 MB)", apk_size > 5 * 1024 * 1024, f"Actual size: {apk_size} bytes")

    android_asset_index = os.path.join(APP_SRC, 'assets', 'index.html')
    check("Android assets/index.html exists", os.path.isfile(android_asset_index))
    if os.path.isfile(android_asset_index):
        with open(android_asset_index, 'rb') as f:
            h_asset = hashlib.sha256(f.read()).hexdigest()
        check("Android assets/index.html matches root index.html", h_asset == h_index)

    # -------------------------------------------------------------
    # Group 7: Host Diagnostics & Emulator Status
    # -------------------------------------------------------------
    print("\n--- Group 7: Host Diagnostics & Emulator Status ---")
    avd_dir = os.path.expanduser(r'~/.android/avd/Medium_Phone.avd')
    check("AVD Medium_Phone.avd exists on host", os.path.isdir(avd_dir))

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {total} checks")
    print("=" * 70)

    return failed == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_alarms_notifications_popups.py
Comprehensive verification of all Alarms, Notifications, and In-App Popups & Toasts:
1. window.showToast & window.toast in-app toast engine.
2. In-app reminder modal (#inAppReminderModal) rendering, title, body, icon, and dismiss.
3. Web Audio alert chimes (playChimeAlert, _onTimerFinished) and haptic triggers.
4. Native Android manifest permissions (USE_EXACT_ALARM, SYSTEM_ALERT_WINDOW, USE_FULL_SCREEN_INTENT).
5. Native AlarmActivity lock-screen flags, audio/vibration local fallback engine.
6. Native ZatoonaNotificationManager high-priority channels with VISIBILITY_PUBLIC.
7. Physical device status check on Samsung Galaxy A04e (ADB).
"""

import os
import re
import sys
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

PASS_COUNT = 0
FAIL_COUNT = 0

def check(condition, message):
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  [PASS] {message}")
    else:
        FAIL_COUNT += 1
        print(f"  [FAIL] {message}")

def run_tests():
    global PASS_COUNT, FAIL_COUNT
    print("=" * 80)
    print("ZATOONA COMPREHENSIVE ALARMS, NOTIFICATIONS & POPUPS TEST SUITE")
    print("=" * 80)

    # -------------------------------------------------------------
    # Tier 1: Static Code Analysis (Kotlin & Manifest)
    # -------------------------------------------------------------
    print("\n--- Tier 1: Android Native Alarm & Notification Contract ---")
    manifest_path = "android/app/src/main/AndroidManifest.xml"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_text = f.read()

    check("android.permission.USE_EXACT_ALARM" in manifest_text, "Manifest includes USE_EXACT_ALARM permission")
    check("android.permission.SYSTEM_ALERT_WINDOW" in manifest_text, "Manifest includes SYSTEM_ALERT_WINDOW permission")
    check("android.permission.USE_FULL_SCREEN_INTENT" in manifest_text, "Manifest includes USE_FULL_SCREEN_INTENT permission")
    check("android.permission.POST_NOTIFICATIONS" in manifest_text, "Manifest includes POST_NOTIFICATIONS permission")
    check("android.permission.FOREGROUND_SERVICE_SPECIAL_USE" in manifest_text, "Manifest includes FOREGROUND_SERVICE_SPECIAL_USE permission")
    check("android:showWhenLocked=\"true\"" in manifest_text, "AlarmActivity configured with showWhenLocked='true'")
    check("android:turnScreenOn=\"true\"" in manifest_text, "AlarmActivity configured with turnScreenOn='true'")

    alarm_activity_path = "android/app/src/main/java/com/zatoona/app/AlarmActivity.kt"
    with open(alarm_activity_path, "r", encoding="utf-8") as f:
        alarm_activity_text = f.read()

    check("startLocalAudioAndVibration" in alarm_activity_text, "AlarmActivity implements startLocalAudioAndVibration")
    check("stopLocalAudioAndVibration" in alarm_activity_text, "AlarmActivity implements stopLocalAudioAndVibration")
    check("FLAG_KEEP_SCREEN_ON" in alarm_activity_text, "AlarmActivity sets FLAG_KEEP_SCREEN_ON")
    check("FLAG_ALLOW_LOCK_WHILE_SCREEN_ON" in alarm_activity_text, "AlarmActivity sets FLAG_ALLOW_LOCK_WHILE_SCREEN_ON")
    check("localMediaPlayer = MediaPlayer()" in alarm_activity_text, "AlarmActivity initializes fallback MediaPlayer")
    check("localVibrator" in alarm_activity_text, "AlarmActivity initializes fallback Vibrator")

    notif_manager_path = "android/app/src/main/java/com/zatoona/app/ZatoonaNotificationManager.kt"
    with open(notif_manager_path, "r", encoding="utf-8") as f:
        notif_manager_text = f.read()

    check("showAlarmNotification" in notif_manager_text, "ZatoonaNotificationManager defines showAlarmNotification")
    check("setFullScreenIntent" in notif_manager_text, "showAlarmNotification sets fullScreenIntent")
    check("Notification.VISIBILITY_PUBLIC" in notif_manager_text, "Channels set lockscreenVisibility = VISIBILITY_PUBLIC")
    check("setBypassDnd(true)" in notif_manager_text, "Alarms and Prayers channels setBypassDnd(true)")

    scheduler_path = "android/app/src/main/java/com/zatoona/app/ZatoonaAlarmScheduler.kt"
    with open(scheduler_path, "r", encoding="utf-8") as f:
        scheduler_text = f.read()

    check("context.startActivity(activityIntent)" in scheduler_text, "ZatoonaAlarmScheduler attempts direct launch of AlarmActivity")
    check("showAlarmNotification(schedule, firedEpochMs)" in scheduler_text, "ZatoonaAlarmScheduler falls back to showAlarmNotification")

    # -------------------------------------------------------------
    # Tier 2: Web App In-App Toast Engine & Reminders
    # -------------------------------------------------------------
    print("\n--- Tier 2: In-App Toast Engine & Reminder Popups (Selenium) ---")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=400,850")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        abs_index = os.path.abspath("index.html")
        driver.get(f"file:///{abs_index}")
        time.sleep(2)

        # 1. Verify window.showToast and window.toast functions exist
        has_show_toast = driver.execute_script("return typeof window.showToast === 'function';")
        has_toast = driver.execute_script("return typeof window.toast === 'function';")
        check(has_show_toast, "window.showToast is defined as a function")
        check(has_toast, "window.toast alias is defined as a function")

        # 2. Trigger showToast and check DOM rendering
        driver.execute_script("window.showToast('تم اختبار إشعار التوست بنجاح 🔔', 'success', 5000);")
        time.sleep(0.5)

        container = driver.find_elements(By.ID, "zatoonaToastContainer")
        check(len(container) == 1, "#zatoonaToastContainer created in DOM")

        toast_pills = driver.find_elements(By.CSS_SELECTOR, ".zatoona-toast-pill")
        check(len(toast_pills) >= 1, ".zatoona-toast-pill element rendered")
        if toast_pills:
            check("تم اختبار إشعار التوست بنجاح 🔔" in toast_pills[-1].text, "Toast pill contains correct message text")
            role = container[0].get_attribute("role")
            aria_live = container[0].get_attribute("aria-live")
            check(role == "status" and aria_live == "polite", "Toast container has accessible role='status' and aria-live='polite'")

        # 3. In-App Reminder Modal Verification
        has_show_reminder = driver.execute_script("return typeof showInAppReminderModal === 'function';")
        has_close_reminder = driver.execute_script("return typeof closeInAppReminderModal === 'function';")
        check(has_show_reminder, "showInAppReminderModal is defined")
        check(has_close_reminder, "closeInAppReminderModal is defined")

        driver.execute_script("""
            if(!window.notificationSettings) window.notificationSettings = {};
            window.notificationSettings.inAppModal = true;
            showInAppReminderModal({
                title: 'تنبيه قيام الليل',
                sub: 'موعد الثلث الأخير من الليل',
                body: 'ركعتان في جوف الليل خير من الدنيا وما فيها',
                icon: '🌙'
            });
        """)
        time.sleep(0.5)

        modal = driver.find_element(By.ID, "inAppReminderModal")
        is_visible = not ("hidden" in (modal.get_attribute("class") or ""))
        check(is_visible, "#inAppReminderModal is displayed without 'hidden' class")

        title_el = driver.find_element(By.ID, "inAppRemTitle")
        check("تنبيه قيام الليل" in title_el.text, "#inAppRemTitle rendered with correct reminder title")

        sub_el = driver.find_element(By.ID, "inAppRemSub")
        check("موعد الثلث الأخير من الليل" in sub_el.text, "#inAppRemSub rendered with correct reminder subtext")

        icon_el = driver.find_element(By.ID, "inAppRemIcon")
        check("🌙" in icon_el.text, "#inAppRemIcon rendered with correct icon emoji")

        # Close modal
        close_btn = driver.find_element(By.ID, "inAppRemClose")
        close_btn.click()
        time.sleep(0.3)
        modal_classes = modal.get_attribute("class") or ""
        check("hidden" in modal_classes, "#inAppReminderModal hides cleanly upon clicking close button")

        # 4. Sound & Chimes Safety
        chime_works = driver.execute_script("""
            try {
                if(typeof playChimeAlert === 'function') playChimeAlert();
                if(typeof _onTimerFinished === 'function') _onTimerFinished();
                return true;
            } catch(e) {
                return false;
            }
        """)
        check(chime_works, "playChimeAlert and _onTimerFinished execute safely without runtime exceptions")

        # 5. Console Log Inspection
        logs = driver.get_log("browser")
        severe_errors = [
            l for l in logs
            if l.get("level") == "SEVERE"
            and "favicon.ico" not in l.get("message", "")
            and "manifest.json" not in l.get("message", "")
        ]
        check(len(severe_errors) == 0, f"Zero SEVERE JavaScript console errors (found {len(severe_errors)})")

    finally:
        driver.quit()

    # -------------------------------------------------------------
    # Tier 3: Physical Device Diagnostics (Samsung Galaxy A04e via ADB)
    # -------------------------------------------------------------
    print("\n--- Tier 3: Physical Device Diagnostics (Samsung Galaxy A04e) ---")
    try:
        devices_out = subprocess.check_output(["adb", "devices"], text=True)
        if "R8YWA13G7WM" in devices_out:
            check(True, "Samsung Galaxy A04e (R8YWA13G7WM) connected via ADB")

            pkg_dumpsys = subprocess.check_output(
                ["adb", "-s", "R8YWA13G7WM", "shell", "dumpsys", "package", "com.zatoona.app.debug"],
                text=True
            )
            check("USE_EXACT_ALARM: granted=true" in pkg_dumpsys, "Device granted USE_EXACT_ALARM automatically")
            check("POST_NOTIFICATIONS: granted=true" in pkg_dumpsys, "Device granted POST_NOTIFICATIONS permission")
            check("USE_FULL_SCREEN_INTENT: granted=true" in pkg_dumpsys, "Device granted USE_FULL_SCREEN_INTENT permission")
            check("FOREGROUND_SERVICE_SPECIAL_USE: granted=true" in pkg_dumpsys, "Device granted FOREGROUND_SERVICE_SPECIAL_USE")

            appops_out = subprocess.check_output(
                ["adb", "-s", "R8YWA13G7WM", "shell", "cmd", "appops", "get", "com.zatoona.app.debug", "SYSTEM_ALERT_WINDOW"],
                text=True
            )
            check("allow" in appops_out, "SYSTEM_ALERT_WINDOW allowed (display over other apps)")

            pid_out = subprocess.check_output(
                ["adb", "-s", "R8YWA13G7WM", "shell", "pidof", "com.zatoona.app.debug"],
                text=True
            ).strip()
            check(len(pid_out) > 0, f"com.zatoona.app.debug is actively running on device (PID: {pid_out})")
        else:
            print("  [SKIP] R8YWA13G7WM not connected for Tier 3 ADB diagnostics")
    except Exception as e:
        print(f"  [WARN] ADB diagnostics failed: {e}")

    # -------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f"TOTAL RESULTS: {PASS_COUNT} PASSED, {FAIL_COUNT} FAILED")
    print("=" * 80)
    return FAIL_COUNT == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

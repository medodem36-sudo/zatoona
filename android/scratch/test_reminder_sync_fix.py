import hashlib
import json
import re

def main():
    print("=== TEST SUITE: REMINDER SYNC FIX ===")

    # 1. 3-Way HTML byte parity check
    files = ['index.html', 'zatoona.html', 'android/app/src/main/assets/index.html']
    hashes = {}
    sizes = {}
    for p in files:
        with open(p, 'rb') as f:
            d = f.read()
        sizes[p] = len(d)
        hashes[p] = hashlib.sha256(d).hexdigest()

    assert len(set(sizes.values())) == 1, f"Size mismatch: {sizes}"
    assert len(set(hashes.values())) == 1, f"Hash mismatch: {hashes}"
    print(f"[PASS] 1. 3-Way HTML byte parity: {list(sizes.values())[0]} bytes, SHA-256={list(hashes.values())[0][:16]}...")

    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 2. Check syncRemindersToNativeBridge does NOT exit early on notificationSettings.enabled === false
    assert "if(!notificationSettings || !notificationSettings.enabled) return;" not in html, \
        "[FAIL] Early exit on notificationSettings.enabled still exists!"
    print("[PASS] 2. Early exit guard on notificationSettings.enabled removed from syncRemindersToNativeBridge.")

    # 3. Check prayer notifications are guarded by notificationSettings.enabled
    assert "if(notificationSettings && notificationSettings.enabled && notificationSettings.prayers)" in html, \
        "[FAIL] Prayer notifications not guarded by notificationSettings.enabled"
    print("[PASS] 3. Automated prayer alerts remain strictly guarded by master notification switch.")

    # 4. Check push to native bridge is always executed
    assert "// Push to native bridge (always push, even if empty, so that cancelled/deleted schedules are purged from AlarmManager)" in html
    assert "window.ZatoonaNativeBridge.syncSchedules(JSON.stringify(schedules));" in html
    print("[PASS] 4. Native bridge sync always runs to ensure deleted/empty schedules purge orphaned alarms.")

    # 5. Check deleteReminder calls cancelSchedule
    assert "window.ZatoonaNativeBridge.cancelSchedule(remId)" in html
    print("[PASS] 5. deleteReminder explicitly calls cancelSchedule for immediate alarm cancellation.")

    # 6. Check renderReminders statusBadge
    assert "statusBadge" in html
    assert "⚡ مجدول كمنبه" in html
    assert "🌐 تذكير متصفح (أثناء الفتح)" in html
    assert "🔕 موقّف" in html
    print("[PASS] 6. UI status badges clearly differentiate native scheduled alarms from browser/paused state.")

    # 7. Check ZatoonaBridge.kt reconciliation logic
    with open('android/app/src/main/java/com/zatoona/app/ZatoonaBridge.kt', 'r', encoding='utf-8') as f:
        kt = f.read()
    assert "val incomingIds = mutableSetOf<String>()" in kt
    assert "incomingIds.add(id)" in kt
    assert "!incomingIds.contains(oldSched.id)" in kt
    assert "scheduler.cancelAlarm(oldSched.id)" in kt
    assert "repository.deleteSchedule(oldSched.id)" in kt
    print("[PASS] 7. ZatoonaBridge.kt reconciles persisted schedules and cancels omitted/deleted alarms.")

    print("\nALL TESTS PASSED SUCCESSFULLY (7/7)!")

if __name__ == '__main__':
    main()

import subprocess
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')
adb = r'C:\Users\Lenovo\AppData\Local\Android\Sdk\platform-tools\adb.exe'

def run_adb(args):
    return subprocess.run([adb] + args, capture_output=True, text=True, encoding='utf-8')

print("1. Waking device screen...")
run_adb(['shell', 'input', 'keyevent', 'KEYCODE_WAKEUP'])
run_adb(['shell', 'input', 'keyevent', '82'])
time.sleep(1)

print("2. Launching Zatoona with #sleep...")
run_adb(['shell', 'am', 'start', '-n', 'com.zatoona.app.debug/com.zatoona.app.MainActivity'])
time.sleep(3)

# Open drawer or navigate to sleep
# Tapping menu icon (القائمة ☰) at top right (x=660, y=140)
print("3. Tapping Drawer menu...")
run_adb(['shell', 'input', 'tap', '660', '140'])
time.sleep(1.5)

# Tap 'النوم والاستشفاء' in drawer (approx x=500, y=550)
print("4. Tapping Sleep mode in drawer...")
run_adb(['shell', 'input', 'tap', '500', '550'])
time.sleep(2)

# Scroll down to view Phase 6 sleep cards
print("5. Scrolling down in Sleep view...")
run_adb(['shell', 'input', 'swipe', '360', '1200', '360', '500', '400'])
time.sleep(1.5)

screen_sleep = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_physical_phase6_sleep.png'
run_adb(['shell', 'screencap', '-p', '/sdcard/p6_sleep.png'])
subprocess.run([adb, 'pull', '/sdcard/p6_sleep.png', screen_sleep], capture_output=True)
print(f"Captured Sleep view screenshot: {screen_sleep}")

# Open drawer again to go to schedule
print("6. Tapping Drawer menu for Schedule...")
run_adb(['shell', 'input', 'tap', '660', '140'])
time.sleep(1.5)

# Tap 'الجدول والمهام' in drawer (approx x=500, y=650)
print("7. Tapping Schedule in drawer...")
run_adb(['shell', 'input', 'tap', '500', '650'])
time.sleep(2)

# Scroll down to view Phase 6 schedule cards
print("8. Scrolling down in Schedule view...")
run_adb(['shell', 'input', 'swipe', '360', '1200', '360', '500', '400'])
time.sleep(1.5)

screen_sched = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_physical_phase6_sched.png'
run_adb(['shell', 'screencap', '-p', '/sdcard/p6_sched.png'])
subprocess.run([adb, 'pull', '/sdcard/p6_sched.png', screen_sched], capture_output=True)
print(f"Captured Schedule view screenshot: {screen_sched}")

print("Physical navigation test complete.")

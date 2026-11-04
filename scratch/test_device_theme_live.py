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

print("2. Launching Zatoona...")
run_adb(['shell', 'am', 'start', '-n', 'com.zatoona.app.debug/com.zatoona.app.MainActivity'])
time.sleep(3)

print("3. Tapping '🎨 المظهر' button at (120, 110)...")
run_adb(['shell', 'input', 'tap', '120', '110'])
time.sleep(1.5)

# Screenshot with modal open
screen_modal = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_phone_modal_open_test.png'
run_adb(['shell', 'screencap', '-p', '/sdcard/modal_open.png'])
subprocess.run([adb, 'pull', '/sdcard/modal_open.png', screen_modal], capture_output=True)
print(f"Modal open screenshot saved to: {screen_modal}")

print("4. Tapping '🌊 أزرق' (Ocean accent) at (420, 1110)...")
run_adb(['shell', 'input', 'tap', '420', '1110'])
time.sleep(1.5)

# Screenshot after selecting blue accent
screen_blue = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_phone_accent_blue.png'
run_adb(['shell', 'screencap', '-p', '/sdcard/accent_blue.png'])
subprocess.run([adb, 'pull', '/sdcard/accent_blue.png', screen_blue], capture_output=True)
print(f"Blue accent screenshot saved to: {screen_blue}")

print("5. Pressing Android hardware Back button (KEYCODE_BACK / keyevent 4)...")
run_adb(['shell', 'input', 'keyevent', '4'])
time.sleep(1.5)

# Screenshot after pressing back button
screen_after_back = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_phone_after_hardware_back.png'
run_adb(['shell', 'screencap', '-p', '/sdcard/after_back.png'])
subprocess.run([adb, 'pull', '/sdcard/after_back.png', screen_after_back], capture_output=True)
print(f"After hardware back screenshot saved to: {screen_after_back}")

print("Device test complete.")

import subprocess
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')
adb = r'C:\Users\Lenovo\AppData\Local\Android\Sdk\platform-tools\adb.exe'

def run_adb(args):
    return subprocess.run([adb] + args, capture_output=True, text=True, encoding='utf-8')

print("1. Clearing logcat...")
run_adb(['logcat', '-c'])

print("2. Performing realistic smooth scrolling gestures on physical device...")
# Swipe down (scroll content up)
for i in range(5):
    run_adb(['shell', 'input', 'swipe', '360', '1100', '360', '400', '300'])
    time.sleep(0.5)

# Swipe back up (scroll content down)
for i in range(5):
    run_adb(['shell', 'input', 'swipe', '360', '400', '360', '1100', '300'])
    time.sleep(0.5)

print("3. Checking logcat for GPU tile memory warnings during scroll...")
log_res = run_adb(['logcat', '-d', '-s', 'chromium:E', 'IMGSRV:E'])
tile_errors = [line for line in log_res.stdout.splitlines() if 'tile memory limits exceeded' in line]
gpu_errors = [line for line in log_res.stdout.splitlines() if 'BufPoolFreeBuffer' in line]

print(f"Total tile memory errors during 10 full-screen scrolls: {len(tile_errors)}")
print(f"Total GPU buffer pool errors during 10 full-screen scrolls: {len(gpu_errors)}")

print("4. Testing Theme Customizer button tap...")
# Coordinates for btnOpenThemeModal: (120, 110)
run_adb(['shell', 'input', 'tap', '120', '110'])
time.sleep(1.5)

# Capture screenshot
screen_modal = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_phone_theme_customizer_opened.png'
run_adb(['shell', 'screencap', '-p', '/sdcard/theme_customizer_opened.png'])
subprocess.run([adb, 'pull', '/sdcard/theme_customizer_opened.png', screen_modal], capture_output=True)
print(f"Captured modal screenshot to: {screen_modal}")

# Check console logs for any errors
console_logs = [line for line in log_res.stdout.splitlines() if 'CONSOLE' in line or 'Uncaught' in line]
print(f"Console errors/warnings: {console_logs}")

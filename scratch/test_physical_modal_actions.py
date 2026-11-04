import subprocess
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')
adb = r'C:\Users\Lenovo\AppData\Local\Android\Sdk\platform-tools\adb.exe'

def run_adb(args):
    return subprocess.run([adb] + args, capture_output=True, text=True, encoding='utf-8')

print("1. Tapping '🌊 أزرق' at (460, 1110)...")
run_adb(['shell', 'input', 'tap', '460', '1110'])
time.sleep(1.5)

screen_blue = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_test_blue_tapped.png'
run_adb(['shell', 'screencap', '-p', '/sdcard/blue_tapped.png'])
subprocess.run([adb, 'pull', '/sdcard/blue_tapped.png', screen_blue], capture_output=True)
print(f"Blue tapped screenshot saved to: {screen_blue}")

print("2. Tapping 'X' close button at (90, 795)...")
run_adb(['shell', 'input', 'tap', '90', '795'])
time.sleep(1.5)

screen_x = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_test_x_tapped.png'
run_adb(['shell', 'screencap', '-p', '/sdcard/x_tapped.png'])
subprocess.run([adb, 'pull', '/sdcard/x_tapped.png', screen_x], capture_output=True)
print(f"X tapped screenshot saved to: {screen_x}")

print("3. Reopening modal by tapping (120, 140)...")
run_adb(['shell', 'input', 'tap', '120', '140'])
time.sleep(1.5)

print("4. Pressing Android hardware Back button (input keyevent 4)...")
run_adb(['shell', 'input', 'keyevent', '4'])
time.sleep(1.5)

screen_back = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_test_hardware_back.png'
run_adb(['shell', 'screencap', '-p', '/sdcard/hardware_back.png'])
subprocess.run([adb, 'pull', '/sdcard/hardware_back.png', screen_back], capture_output=True)
print(f"Hardware back screenshot saved to: {screen_back}")

print("All physical interactions completed.")

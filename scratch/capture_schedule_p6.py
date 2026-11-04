import subprocess
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')
adb = r'C:\Users\Lenovo\AppData\Local\Android\Sdk\platform-tools\adb.exe'

# Open Drawer
print("Opening drawer...")
subprocess.run([adb, 'shell', 'input', 'tap', '660', '140'])
time.sleep(1)

# Tap Schedule in drawer (around y=670)
print("Tapping Schedule...")
subprocess.run([adb, 'shell', 'input', 'tap', '500', '670'])
time.sleep(2)

# Scroll down to Schedule section 2
print("Scrolling down to Schedule section 2...")
subprocess.run([adb, 'shell', 'input', 'swipe', '360', '1300', '360', '400', '400'])
time.sleep(1.5)

screen_sched_p6 = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_physical_schedule_p6.png'
subprocess.run([adb, 'shell', 'screencap', '-p', '/sdcard/sched_p6.png'])
subprocess.run([adb, 'pull', '/sdcard/sched_p6.png', screen_sched_p6], capture_output=True)
print('Pulled Schedule Phase 6 screenshot to:', screen_sched_p6)

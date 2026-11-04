import subprocess
import re
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
adb = r'C:\Users\Lenovo\AppData\Local\Android\Sdk\platform-tools\adb.exe'

def run_adb(args):
    return subprocess.run([adb] + args, capture_output=True, text=True, encoding='utf-8')

print("1. Dumping UI hierarchy...")
run_adb(['shell', 'uiautomator', 'dump', '/sdcard/window_dump.xml'])
run_adb(['pull', '/sdcard/window_dump.xml', 'scratch/window_dump.xml'])

with open('scratch/window_dump.xml', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Dump size: {len(content)} characters.")

# Search for theme button
matches = re.findall(r'text="([^"]*)"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', content)
theme_btn_coords = None

for text, x1, y1, x2, y2 in matches:
    if any(k in text for k in ['مظهر', 'زتونة', 'المظهر']):
        cx = (int(x1) + int(x2)) // 2
        cy = (int(y1) + int(y2)) // 2
        print(f"Found theme target: '{text}' at bounds [{x1},{y1}][{x2},{y2}] -> Center: ({cx}, {cy})")
        theme_btn_coords = (cx, cy)
        break

if not theme_btn_coords:
    # Look for any button in the top bar or header
    print("Theme button not directly found in accessibility text. Listing top bar texts:")
    for text, x1, y1, x2, y2 in matches[:15]:
        print(f"  '{text}' bounds=[{x1},{y1}][{x2},{y2}]")
else:
    print(f"2. Tapping theme button at {theme_btn_coords}...")
    run_adb(['shell', 'input', 'tap', str(theme_btn_coords[0]), str(theme_btn_coords[1])])
    time.sleep(2)
    
    print("3. Capturing screenshot after opening Theme Customizer...")
    modal_screen = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\screen_phone_theme_modal.png'
    run_adb(['shell', 'screencap', '-p', '/sdcard/theme_modal.png'])
    subprocess.run([adb, 'pull', '/sdcard/theme_modal.png', modal_screen], capture_output=True)
    print(f"Theme modal screenshot saved to: {modal_screen}")

    # Check UI dump again to confirm modal is open
    run_adb(['shell', 'uiautomator', 'dump', '/sdcard/modal_dump.xml'])
    run_adb(['pull', '/sdcard/modal_dump.xml', 'scratch/modal_dump.xml'])
    with open('scratch/modal_dump.xml', 'r', encoding='utf-8') as f:
        modal_content = f.read()
    
    modal_matches = re.findall(r'text="([^"]*)"', modal_content)
    theme_options = [t for t in modal_matches if any(w in t for w in ['ألوان', 'خط', 'ثيم', 'تخصيص', 'داكن', 'فاتح', 'إغلاق'])]
    print("Detected modal elements on screen:", theme_options[:10])

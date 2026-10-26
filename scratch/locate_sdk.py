# -*- coding: utf-8 -*-
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("Searching for Android SDK directories...")

search_roots = [
    r"D:\Android apk build",
    r"D:",
    r"C:\Users\Lenovo\AppData\Local\Android",
    r"C:\Users\Lenovo",
    r"C:\Android"
]

found_sdk = []

for root_dir in [r"D:\Android apk build", r"C:\Users\Lenovo\AppData\Local", r"D:"]:
    if not os.path.exists(root_dir):
        continue
    print(f"Scanning {root_dir}...")
    try:
        for item in os.listdir(root_dir):
            p = os.path.join(root_dir, item)
            if 'sdk' in item.lower() or 'android' in item.lower():
                print(f"  Candidate: {p}")
                # check if it has platforms or build-tools
                if os.path.isdir(p):
                    sub = os.listdir(p)
                    print(f"    Subdirs: {sub}")
    except Exception as e:
        print(f"  Error reading {root_dir}: {e}")

# Check user config for Android Studio in AppData/Google
appdata = os.environ.get('APPDATA', '')
localappdata = os.environ.get('LOCALAPPDATA', '')
for base in [appdata, localappdata]:
    google_dir = os.path.join(base, 'Google')
    if os.path.exists(google_dir):
        print(f"\nChecking Google config in {google_dir}:")
        for item in os.listdir(google_dir):
            if 'android' in item.lower():
                print(f"  Found: {item}")
                studio_dir = os.path.join(google_dir, item)
                for root, dirs, files in os.walk(studio_dir):
                    for f in files:
                        if f.endswith('.xml') or f.endswith('.properties'):
                            full_f = os.path.join(root, f)
                            try:
                                with open(full_f, 'r', encoding='utf-8', errors='ignore') as fp:
                                    cnt = fp.read()
                                    if 'sdk' in cnt.lower():
                                        for line in cnt.split('\n'):
                                            if 'sdk' in line.lower() and ('path' in line.lower() or 'dir' in line.lower() or 'home' in line.lower()):
                                                print(f"    [{f}]: {line.strip()[:100]}")
                            except:
                                pass

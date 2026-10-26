# -*- coding: utf-8 -*-
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
print("Scanning repository for Android / native / wrapper artifacts...")

native_patterns = [
    'capacitor', 'cordova', 'twa', 'android', 'gradle', '.java', '.kt', 'bubblewrap',
    'alarmmanager', 'workmanager', 'notificationcompat', 'manifest.xml'
]

found_files = []
for root, dirs, files in os.walk(repo):
    # skip .git and scratch
    if '.git' in root or 'scratch' in root or 'test-results' in root:
        continue
    for f in files:
        f_lower = f.lower()
        if any(pat in f_lower for pat in native_patterns):
            found_files.append(os.path.join(root, f))

print(f"Total matching files in non-scratch repo: {len(found_files)}")
for f in found_files:
    print(f"  {os.path.relpath(f, repo)}")

# Also list top-level files and folders
print("\nTop-level repository contents:")
for item in os.listdir(repo):
    p = os.path.join(repo, item)
    t = "DIR " if os.path.isdir(p) else "FILE"
    print(f"  [{t}] {item}")

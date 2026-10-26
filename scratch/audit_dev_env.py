# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import shutil
sys.stdout.reconfigure(encoding='utf-8')

print("=== LOCAL ENVIRONMENT DISCOVERY ===")

def check_cmd(name, args):
    path = shutil.which(name)
    if path:
        try:
            res = subprocess.run([name] + args, capture_output=True, text=True, timeout=5)
            out = (res.stdout or res.stderr).strip().split('\n')[0]
            print(f"[FOUND] {name}: {path} ({out})")
            return True
        except Exception as e:
            print(f"[FOUND] {name}: {path} (error running: {e})")
            return True
    else:
        print(f"[NOT FOUND] {name}")
        return False

check_cmd("node", ["--version"])
check_cmd("npm", ["--version"])
check_cmd("java", ["-version"])
check_cmd("javac", ["-version"])
check_cmd("gradle", ["--version"])
check_cmd("adb", ["version"])

# Check standard Android SDK locations on Windows
user_home = os.path.expanduser("~")
android_paths = [
    os.path.join(user_home, "AppData", "Local", "Android", "Sdk"),
    os.path.join(user_home, "AppData", "Local", "Android", "android-sdk"),
    r"C:\Android\Sdk",
    r"C:\Program Files\Android\Android Studio"
]
print("\n=== ANDROID SDK / STUDIO LOCATIONS ===")
for p in android_paths:
    exists = os.path.exists(p)
    print(f"  {p}: {'EXISTS' if exists else 'NOT FOUND'}")

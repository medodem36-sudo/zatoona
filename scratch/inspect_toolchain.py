# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import shutil
sys.stdout.reconfigure(encoding='utf-8')

print("================================================================================")
print("PHASE 13.4B1 PREFLIGHT: COMPREHENSIVE TOOLCHAIN INSPECTION")
print("================================================================================")

# 1. Environment Variables
print("\n--- 1. Environment Variables ---")
env_vars = ['ANDROID_HOME', 'ANDROID_SDK_ROOT', 'JAVA_HOME', 'GRADLE_HOME', 'PATH']
for var in env_vars:
    val = os.environ.get(var)
    if val:
        if var == 'PATH':
            print(f"{var}: ({len(val.split(os.pathsep))} entries)")
            for p in val.split(os.pathsep):
                if any(k in p.lower() for k in ['android', 'java', 'jdk', 'gradle', 'git']):
                    print(f"   matching entry: {p}")
        else:
            print(f"{var}: {val}")
    else:
        print(f"{var}: [NOT SET]")

# 2. Executables on PATH
print("\n--- 2. Executables on PATH ---")
tools = ['java', 'javac', 'gradle', 'adb', 'sdkmanager', 'node', 'npm', 'git']
for t in tools:
    loc = shutil.which(t)
    if loc:
        try:
            res = subprocess.run([t, '--version'] if t not in ['java', 'javac'] else [t, '-version'], capture_output=True, text=True, timeout=5)
            first_line = (res.stdout or res.stderr).strip().split('\n')[0]
            print(f"  [FOUND] {t:10s} -> {loc} ({first_line})")
        except Exception as e:
            print(f"  [FOUND] {t:10s} -> {loc} (error executing: {e})")
    else:
        print(f"  [NOT FOUND] {t:10s}")

# 3. Comprehensive Filesystem Search for Android SDK & Android Studio
print("\n--- 3. Filesystem Probing for Android & JDK Installations ---")
user_home = os.path.expanduser("~")
potential_sdk_dirs = [
    os.path.join(user_home, "AppData", "Local", "Android", "Sdk"),
    os.path.join(user_home, "AppData", "Local", "Android", "android-sdk"),
    r"C:\Android\Sdk",
    r"C:\Android\android-sdk",
    r"C:\Program Files\Android\Android Studio",
    r"C:\Program Files (x86)\Android\Android Studio",
    os.path.join(user_home, "AppData", "Local", "Programs", "Android Studio"),
]

for d in potential_sdk_dirs:
    exists = os.path.isdir(d)
    print(f"  Directory: {d:50s} -> {'EXISTS' if exists else 'NOT FOUND'}")
    if exists:
        try:
            contents = os.listdir(d)
            print(f"    Contents: {contents[:10]}")
        except Exception as e:
            print(f"    Error reading: {e}")

# Potential JDK directories
potential_jdk_dirs = [
    r"C:\Program Files\Java",
    r"C:\Program Files (x86)\Java",
    r"C:\Program Files\Eclipse Adoptium",
    r"C:\Program Files\Microsoft\jdk",
    os.path.join(user_home, "AppData", "Local", "Programs", "Eclipse Adoptium"),
    os.path.join(user_home, ".jdks")
]
print("\n--- 4. Filesystem Probing for JDKs ---")
for d in potential_jdk_dirs:
    exists = os.path.isdir(d)
    print(f"  Directory: {d:50s} -> {'EXISTS' if exists else 'NOT FOUND'}")
    if exists:
        try:
            subdirs = os.listdir(d)
            print(f"    Subdirs: {subdirs}")
            for sub in subdirs:
                javac_path = os.path.join(d, sub, "bin", "javac.exe")
                if os.path.exists(javac_path):
                    print(f"      [FOUND javac]: {javac_path}")
        except Exception as e:
            print(f"    Error reading: {e}")

# 5. Git Executable
print("\n--- 5. Git Installation Discovery ---")
git_path = r"C:\Users\Lenovo\AppData\Local\GitHubDesktop\app-3.6.7\resources\app\git\cmd\git.exe"
print(f"  GitHub Desktop Git: {git_path} -> {'EXISTS' if os.path.exists(git_path) else 'NOT FOUND'}")
if os.path.exists(git_path):
    res = subprocess.run([git_path, '--version'], capture_output=True, text=True)
    print(f"  Git Version: {res.stdout.strip()}")

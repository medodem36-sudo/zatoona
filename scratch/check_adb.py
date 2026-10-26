# -*- coding: utf-8 -*-
import os
import subprocess
import glob

user_local = os.environ.get('LOCALAPPDATA', '')
links_dir = os.path.join(user_local, 'Microsoft', 'WinGet', 'Links')
print(f"Links dir: {links_dir}")
if os.path.exists(links_dir):
    print("Contents:", os.listdir(links_dir))

packages_dir = os.path.join(user_local, 'Microsoft', 'WinGet', 'Packages')
print(f"\nPackages dir: {packages_dir}")
if os.path.exists(packages_dir):
    for root, dirs, files in os.walk(packages_dir):
        if 'adb.exe' in files:
            adb_path = os.path.join(root, 'adb.exe')
            print(f"[FOUND ADB]: {adb_path}")
            res = subprocess.run([adb_path, 'version'], capture_output=True, text=True)
            print(res.stdout)
            # check connected devices
            dev_res = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
            print("Connected devices:\n" + dev_res.stdout)

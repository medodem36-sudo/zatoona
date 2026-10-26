# -*- coding: utf-8 -*-
import os
import shutil

backup_dir = r"C:\Users\Lenovo\Documents\Zatoona_Backups\phase13_3_preflight_20261025"
os.makedirs(backup_dir, exist_ok=True)

files_to_backup = [
    "index.html",
    "zatoona.html",
    "sw.js",
    "manifest.json",
    os.path.join("assets", "data", "exercise-catalog.js"),
    os.path.join("scratch", "test_master_regression_gate.py")
]

for rel in files_to_backup:
    src = os.path.join(r"C:\Users\Lenovo\Documents\GitHub\zatoona", rel)
    dst = os.path.join(backup_dir, os.path.basename(rel))
    shutil.copy2(src, dst)
    print(f"Backed up {rel} -> {dst}")

print("Pre-flight backup completed successfully.")

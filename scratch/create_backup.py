import os
import shutil

backup_dir = r"C:\Users\Lenovo\Documents\Zatoona_Backups\phase13_1_preflight_20261025"
os.makedirs(backup_dir, exist_ok=True)

files = [
    'index.html',
    'zatoona.html',
    'sw.js',
    'manifest.json',
    'assets/data/exercise-catalog.js'
]

for f in files:
    dest = os.path.join(backup_dir, os.path.basename(f))
    shutil.copy2(f, dest)
    print(f"Backed up {f} -> {dest} ({os.path.getsize(dest)} bytes)")

print("\nBackup completed successfully!")

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

# Create backup before modification
backup_dir = 'scratch/backups/theme_full_fix_pre_injection'
os.makedirs(backup_dir, exist_ok=True)

files = [
    'index.html',
    'zatoona.html',
    'android/app/src/main/assets/index.html',
    'android/app/src/main/java/com/zatoona/app/MainActivity.kt'
]
for p in files:
    with open(p, 'rb') as f:
        data = f.read()
    dest = os.path.join(backup_dir, os.path.basename(p))
    with open(dest, 'wb') as f:
        f.write(data)
print('Backup created for all 4 files.')

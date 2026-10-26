"""
inspect_apk_provenance.py
Deeply inspects the current debug APK to prove provenance against current source code and assets.
"""
import os
import sys
import zipfile
import hashlib
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APK_PATH = os.path.join(ROOT_DIR, 'android', 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
INDEX_HTML = os.path.join(ROOT_DIR, 'index.html')
ANDROID_ASSET_INDEX = os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'assets', 'index.html')

print("=" * 70)
print("APK PROVENANCE AUDIT")
print("=" * 70)

if not os.path.exists(APK_PATH):
    print(f"FATAL: APK not found at {APK_PATH}")
    sys.exit(1)

# 1. File stats & SHA-256
st = os.stat(APK_PATH)
mtime = datetime.fromtimestamp(st.st_mtime)
size = st.st_size

with open(APK_PATH, 'rb') as f:
    apk_hash = hashlib.sha256(f.read()).hexdigest()

print(f"APK Path           : {APK_PATH}")
print(f"APK File Size      : {size:,} bytes ({size / (1024*1024):.2f} MB)")
print(f"APK Last Modified  : {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"APK SHA-256        : {apk_hash}")

# 2. Inspect ZIP structure
with zipfile.ZipFile(APK_PATH, 'r') as z:
    file_list = z.namelist()
    print(f"\nTotal files in APK : {len(file_list)}")

    # Check dex files
    dex_files = [f for f in file_list if f.endswith('.dex')]
    print(f"DEX files          : {dex_files}")

    # Check manifest
    has_manifest = 'AndroidManifest.xml' in file_list
    print(f"Has Manifest binary: {has_manifest}")

    # Check assets
    assets = [f for f in file_list if f.startswith('assets/')]
    print(f"Total assets in APK: {len(assets)}")

    # Check packaged index.html
    has_index = 'assets/index.html' in file_list
    print(f"Has assets/index.html: {has_index}")

    if has_index:
        info = z.getinfo('assets/index.html')
        content = z.read('assets/index.html')
        content_hash = hashlib.sha256(content).hexdigest()
        
        # Compare with root index.html
        with open(INDEX_HTML, 'rb') as f:
            root_index_bytes = f.read()
            root_hash = hashlib.sha256(root_index_bytes).hexdigest()

        # Compare with android/app/src/main/assets/index.html
        with open(ANDROID_ASSET_INDEX, 'rb') as f:
            android_asset_bytes = f.read()
            android_asset_hash = hashlib.sha256(android_asset_bytes).hexdigest()

        print(f"\n--- index.html Parity & Provenance ---")
        print(f"Packaged index.html SHA-256      : {content_hash}")
        print(f"Root index.html SHA-256          : {root_hash}")
        print(f"Android src asset index SHA-256  : {android_asset_hash}")
        print(f"Packaged matches Root index.html : {content_hash == root_hash}")
        print(f"Packaged matches Android asset   : {content_hash == android_asset_hash}")

        # Check for bridge integration code in packaged index.html
        text = content.decode('utf-8', errors='ignore')
        has_bridge_func = 'function syncRemindersToNativeBridge()' in text
        has_bridge_avail = 'function isNativeBridgeAvailable()' in text
        has_init_call = 'syncRemindersToNativeBridge()' in text
        has_city_hook = 'updateActivePrayerCity(newCity)' in text
        has_notif_hook = 'saveNotificationSettings' in text and 'syncRemindersToNativeBridge' in text

        print(f"\n--- Bridge Hooks in Packaged index.html ---")
        print(f"  syncRemindersToNativeBridge() defined : {has_bridge_func}")
        print(f"  isNativeBridgeAvailable() defined      : {has_bridge_avail}")
        print(f"  initNotificationScheduler sync call   : {has_init_call}")
        print(f"  onCityChange updateActivePrayerCity    : {has_city_hook}")
        print(f"  saveNotificationSettings hook          : {has_notif_hook}")

    # Check native class names in dex files
    print("\n--- DEX String & Class Analysis ---")
    all_dex_content = b"".join([z.read(dex) for dex in dex_files])

    classes_to_check = [
        b"ZatoonaBridge",
        b"ZatoonaScheduleModel",
        b"ZatoonaScheduleRepository",
        b"ZatoonaAlarmScheduler",
        b"ZatoonaNotificationManager",
        b"AlarmReceiver",
        b"BootReceiver",
        b"MainActivity",
        b"syncSchedules",
        b"syncUpcomingAlarms",
        b"updateActivePrayerCity",
        b"getAlarmEngineStatus",
        b"zatoona_reminders",
        b"zatoona_prayers",
        b"zatoona_sleep"
    ]

    for sym in classes_to_check:
        present = sym in all_dex_content
        print(f"  Symbol '{sym.decode()}' in DEX: {present}")

# 3. Source file modification times vs APK modification time
print("\n--- Timestamps: Native Source vs APK ---")
src_files = [
    os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'AndroidManifest.xml'),
    os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'java', 'com', 'zatoona', 'app', 'ZatoonaBridge.kt'),
    os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'java', 'com', 'zatoona', 'app', 'ZatoonaAlarmScheduler.kt'),
    os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'java', 'com', 'zatoona', 'app', 'ZatoonaScheduleRepository.kt'),
    os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'java', 'com', 'zatoona', 'app', 'ZatoonaNotificationManager.kt'),
    os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'java', 'com', 'zatoona', 'app', 'AlarmReceiver.kt'),
    os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'java', 'com', 'zatoona', 'app', 'BootReceiver.kt'),
    os.path.join(ROOT_DIR, 'android', 'app', 'src', 'main', 'java', 'com', 'zatoona', 'app', 'MainActivity.kt'),
    ANDROID_ASSET_INDEX
]

for sf in src_files:
    if os.path.exists(sf):
        sf_mtime = datetime.fromtimestamp(os.stat(sf).st_mtime)
        is_older_than_apk = sf_mtime <= mtime
        print(f"  {os.path.basename(sf):30} : {sf_mtime.strftime('%Y-%m-%d %H:%M:%S')} (Built into APK: {is_older_than_apk})")

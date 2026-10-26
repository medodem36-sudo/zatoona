"""
Register Phase 13.4B2 suite in scratch/test_master_regression_gate.py
"""
import sys

with open('scratch/test_master_regression_gate.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''        "id": "phase13_4b1_2",
        "name": "Phase 13.4B1.2 Android Toolchain & Buildability Verification",
        "category": "Native Android & Build",
        "rel_path": "scratch/test_phase13_4b1_2_android_buildability.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies JDK 17, Android SDK 34, Gradle 8.5, real APK compilation & assembly (app-debug.apk), packaged PWA assets, and device/emulator diagnostics."
    },'''

new_suite = '''        "id": "phase13_4b1_2",
        "name": "Phase 13.4B1.2 Android Toolchain & Buildability Verification",
        "category": "Native Android & Build",
        "rel_path": "scratch/test_phase13_4b1_2_android_buildability.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies JDK 17, Android SDK 34, Gradle 8.5, real APK compilation & assembly (app-debug.apk), packaged PWA assets, and device/emulator diagnostics."
    },
    {
        "id": "phase13_4b2",
        "name": "Phase 13.4B2 Native Android Local Alarm Engine",
        "category": "Native Android & Alarms",
        "rel_path": "scratch/test_phase13_4b2_alarms.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies native AlarmManager scheduling, boot/time receivers, notification channels, ZatoonaBridge v2 sync, recurrence math, city isolation, PWA bridge integration, and debug APK packaging."
    },'''

if target not in content:
    print("ERROR: Target not found in test_master_regression_gate.py")
    sys.exit(1)

content = content.replace(target, new_suite, 1)

with open('scratch/test_master_regression_gate.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully registered Phase 13.4B2 in test_master_regression_gate.py")

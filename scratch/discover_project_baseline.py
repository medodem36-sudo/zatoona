# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
print(f"Total lines in index.html: {len(lines)}")
print(f"File size in bytes: {len(content.encode('utf-8'))}")
print(f"SHA-256 hash: {hashlib.sha256(content.encode('utf-8')).hexdigest()}")

# 1. Views
view_pattern = re.compile(r'id=["\']([a-zA-Z0-9_-]*View)["\']')
views = sorted(list(set(view_pattern.findall(content))))
print(f"\n--- Views ({len(views)}) ---")
for v in views:
    print(f"  - {v}")

# 2. Modals
modal_pattern = re.compile(r'id=["\']([a-zA-Z0-9_-]*Modal)["\']')
modals = sorted(list(set(modal_pattern.findall(content))))
print(f"\n--- Modals ({len(modals)}) ---")
for m in modals:
    print(f"  - {m}")

# 3. NAV_MODES
nav_modes_match = re.search(r'const\s+NAV_MODES\s*=\s*(\[[^\]]+\])', content)
if nav_modes_match:
    print(f"\n--- NAV_MODES ---")
    print(nav_modes_match.group(1))

# 4. KNOWN_KEY_PATTERNS
known_keys_match = re.search(r'const\s+KNOWN_KEY_PATTERNS\s*=\s*(\[[^\]]+\])', content)
if known_keys_match:
    print(f"\n--- KNOWN_KEY_PATTERNS ---")
    print(known_keys_match.group(1))

# 5. Functions exposed on window
window_fn_pattern = re.compile(r'window\.([a-zA-Z0-9_]+)\s*=')
window_fns = sorted(list(set(window_fn_pattern.findall(content))))
print(f"\n--- Window Exposed Functions ({len(window_fns)}) ---")
for fn in window_fns:
    print(f"  - {fn}")

# 6. Android Bridge inspect
bridge_path = os.path.join(ROOT_DIR, "android", "app", "src", "main", "java", "com", "zatoona", "app", "ZatoonaBridge.kt")
if os.path.exists(bridge_path):
    with open(bridge_path, "r", encoding="utf-8") as bf:
        bcontent = bf.read()
    js_interfaces = re.findall(r'@JavascriptInterface\s+fun\s+([a-zA-Z0-9_]+)\s*\(', bcontent)
    print(f"\n--- Android Native Bridge Methods ({len(js_interfaces)}) ---")
    for jm in sorted(js_interfaces):
        print(f"  - {jm}")

# 7. Manifest inspect
manifest_path = os.path.join(ROOT_DIR, "android", "app", "src", "main", "AndroidManifest.xml")
if os.path.exists(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as mf:
        mcontent = mf.read()
    receivers = re.findall(r'<receiver[^>]+android:name=["\']([^"\']+)["\']', mcontent)
    services = re.findall(r'<service[^>]+android:name=["\']([^"\']+)["\']', mcontent)
    activities = re.findall(r'<activity[^>]+android:name=["\']([^"\']+)["\']', mcontent)
    permissions = re.findall(r'<uses-permission[^>]+android:name=["\']([^"\']+)["\']', mcontent)
    print(f"\n--- Android Manifest Structure ---")
    print("Permissions:", permissions)
    print("Activities:", activities)
    print("Services:", services)
    print("Receivers:", receivers)

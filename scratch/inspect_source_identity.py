import os, sys, hashlib, datetime, subprocess

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
os.chdir(base_dir)

files = ['index.html', 'zatoona.html', 'sw.js', 'manifest.json']
file_info = {}

for f in files:
    full_path = os.path.join(base_dir, f)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
        with open(full_path, 'rb') as fp:
            data = fp.read()
            h = hashlib.sha256(data).hexdigest()
        try:
            with open(full_path, 'r', encoding='utf-8') as fp:
                line_count = len(fp.readlines())
        except:
            line_count = 'N/A'
        file_info[f] = {'size': size, 'mtime': mtime, 'sha256': h, 'lines': line_count}

print("=== FILE METADATA ===")
for f, info in file_info.items():
    print(f"{f}:")
    print(f"  Size: {info['size']:,} bytes")
    print(f"  Lines: {info['lines']}")
    print(f"  Modified: {info['mtime']}")
    print(f"  SHA-256: {info['sha256']}")

# Assets inspection
assets_dir = os.path.join(base_dir, 'assets')
actual_assets = []
for root, dirs, fnames in os.walk(assets_dir):
    for fn in fnames:
        rel = os.path.relpath(os.path.join(root, fn), base_dir).replace('\\', '/')
        actual_assets.append(rel)

print(f"\n=== ACTUAL ASSETS IN assets/ ({len(actual_assets)} files) ===")
for a in sorted(actual_assets):
    print(f"  {a}")

# Read sw.js SHELL_ASSETS and CACHE_VERSION
with open('sw.js', 'r', encoding='utf-8') as fp:
    sw_text = fp.read()

import re
ver_m = re.search(r"CACHE_VERSION\s*=\s*['\"]([^'\"]+)['\"]", sw_text)
cache_ver = ver_m.group(1) if ver_m else "unknown"

shell_assets_match = re.search(r"const\s+SHELL_ASSETS\s*=\s*\[(.*?)\];", sw_text, re.DOTALL)
shell_assets = []
if shell_assets_match:
    raw = shell_assets_match.group(1)
    shell_assets = [item.strip().strip("'\"") for item in raw.split(',') if item.strip()]

print(f"\n=== sw.js CACHE_VERSION: {cache_ver} ===")
print(f"=== sw.js SHELL_ASSETS ({len(shell_assets)} items) ===")
for sa in shell_assets:
    print(f"  {sa}")

# Compare assets
print("\n=== ASSET COMPARISON ===")
for sa in shell_assets:
    # normalize path
    norm = sa.lstrip('./')
    exists = os.path.exists(os.path.join(base_dir, norm)) if norm else os.path.exists(base_dir)
    status = "EXISTS" if exists else "MISSING"
    print(f"  {sa} -> {status}")

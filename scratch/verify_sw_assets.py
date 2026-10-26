import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    text = f.read()

m_ver = re.search(r"const\s+CACHE_VERSION\s*=\s*'([^']+)';", text)
print(f"CACHE_VERSION in sw.js: {m_ver.group(1)}")
assert m_ver.group(1) == 'v24', f"Expected v24, got {m_ver.group(1)}"

m = re.search(r'const\s+SHELL_ASSETS\s*=\s*(\[[\s\S]*?\]);', text)
assets = re.findall(r"['\"]([^'\"]+)['\"]", m.group(1))

print(f"Total assets in SHELL_ASSETS: {len(assets)}")

missing = []
for a in assets:
    # normalize relative path
    rel = a.lstrip('./').replace('/', os.sep)
    if not rel:
        continue # root './'
    if not os.path.exists(rel):
        missing.append((a, rel))

if missing:
    print(f"FAILED: {len(missing)} assets missing on disk:")
    for a, rel in missing:
        print(f"  {a} -> {rel}")
    sys.exit(1)
else:
    print(f"ALL {len(assets)} SHELL_ASSETS exist on disk! 100% Verified!")

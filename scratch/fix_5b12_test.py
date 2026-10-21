# -*- coding: utf-8 -*-
"""Fix the two stale expectations in test_phase5b1_2_legacy_images.py"""

with open(r'scratch\test_phase5b1_2_legacy_images.py', 'rb') as f:
    data = f.read()

# Fix 1: CACHE_VERSION line
old1 = b'''check("sw.js CACHE_VERSION is 'v22'", "const CACHE_VERSION = 'v22'" in sw_text)'''
new1 = b'''# CACHE_VERSION must be >= v22 (v22 was Phase 5B.1.2; v23 added Phase 9C.1 stretch assets)\r\ncache_ver_match = re.search(r"const CACHE_VERSION\\s*=\\s*'v(\\d+)'", sw_text)\r\ncache_ver_num = int(cache_ver_match.group(1)) if cache_ver_match else 0\r\ncheck(f"sw.js CACHE_VERSION >= v22 (found v{cache_ver_num})", cache_ver_num >= 22)'''

count1 = data.count(old1)
print(f"Fix 1 target found {count1} time(s)")
data = data.replace(old1, new1)

# Fix 2: SHELL_ASSETS count line + disk check
# Find the exact bytes
old2_start = data.find(b'shell_entries = re.findall')
old2_end = data.find(b'# \xe2\x94\x80\xe2\x94\x80 Group 4')  # "── Group 4"
if old2_start == -1 or old2_end == -1:
    print(f"ERROR: Could not find Fix 2 boundaries: start={old2_start}, end={old2_end}")
else:
    old2 = data[old2_start:old2_end]
    print(f"Fix 2 target block length: {len(old2)} bytes")
    print(f"Fix 2 target starts with: {repr(old2[:80])}")
    print(f"Fix 2 target ends with: {repr(old2[-80:])}")

    new2 = (
        b'shell_entries = re.findall(r"\'(\\./[^\']*)\'", shell_block)\r\n'
        b'\r\n'
        b'# Must have at least 42 assets (original 42 from Phase 5B.1.2; Phase 9C.1 added 34 stretch SVGs + 1 catalog)\r\n'
        b'check(f"SHELL_ASSETS count >= 42 (found {len(shell_entries)})", len(shell_entries) >= 42)\r\n'
        b'\r\n'
        b'# Zero duplicate paths\r\n'
        b'unique_entries = set(shell_entries)\r\n'
        b'check(f"Zero duplicate paths in SHELL_ASSETS (unique={len(unique_entries)}, total={len(shell_entries)})",\r\n'
        b'      len(unique_entries) == len(shell_entries))\r\n'
        b'\r\n'
        b'# Stretch catalog and SVGs are included (Phase 9C.1 assets)\r\n'
        b'check("SHELL_ASSETS includes stretch-catalog.js", "./assets/data/stretch-catalog.js" in shell_entries)\r\n'
        b'stretch_svgs_in_shell = [e for e in shell_entries if \'stretches/\' in e]\r\n'
        b'check(f"SHELL_ASSETS includes 34 stretch SVGs (found {len(stretch_svgs_in_shell)})", len(stretch_svgs_in_shell) == 34)\r\n'
        b'\r\n'
        b'# Verify ALL shell assets actually exist on disk\r\n'
        b'missing_assets = []\r\n'
        b'for entry in shell_entries:\r\n'
        b'    rel = entry.lstrip("./")\r\n'
        b'    full = os.path.join(REPO, rel)\r\n'
        b'    if not os.path.exists(full):\r\n'
        b'        missing_assets.append(rel)\r\n'
        b'check(f"All {len(shell_entries)} SHELL_ASSETS exist on disk (missing: {missing_assets})", len(missing_assets) == 0)\r\n'
        b'\r\n'
    )

    data = data[:old2_start] + new2 + data[old2_end:]

# Also update docstring
data = data.replace(
    b"5. sw.js SHELL_ASSETS includes all 12 exercise SVGs and CACHE_VERSION is v22 (41 shell assets total)",
    b"5. sw.js SHELL_ASSETS includes all 12 exercise SVGs + stretch assets, CACHE_VERSION >= v22"
)

with open(r'scratch\test_phase5b1_2_legacy_images.py', 'wb') as f:
    f.write(data)

# Verify
text = data.decode('utf-8')
checks = [
    ("cache_ver_num >= 22" in text, "Fix 1: version floor check"),
    ("len(shell_entries) >= 42" in text, "Fix 2: minimum count check"),
    ("stretch-catalog.js" in text, "Stretch catalog verification"),
    ("stretch_svgs_in_shell" in text, "Stretch SVGs verification"),
    ("unique_entries" in text, "Dedup check"),
    ("CACHE_VERSION is 'v22'" not in text, "Old v22 removed"),
    ("count is 41" not in text, "Old 41 count removed"),
]
all_ok = True
for cond, desc in checks:
    status = "OK" if cond else "FAIL"
    print(f"  [{status}] {desc}")
    if not cond:
        all_ok = False

print(f"\nAll verifications passed: {all_ok}")

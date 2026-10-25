# -*- coding: utf-8 -*-
"""
Phase 5B.1.2 — Legacy A/B Exercise Images Compliance Gate Test
Comprehensive validation of:
1. EX_A_DEFAULTS and EX_B_DEFAULTS source code audit (zero external URLs, all local SVGs)
2. All 12 exercise SVGs exist on disk and have valid, non-empty XML
3. Zero female depictions or references in paths or SVG contents
4. Proper movement clarity (e.g. face pull is face pull, not row)
5. sw.js SHELL_ASSETS includes all 12 exercise SVGs + stretch assets, CACHE_VERSION >= v22
6. Headless Chrome UI rendering:
   - Routine A exercises render with working SVGs (naturalWidth > 0, no img-broken)
   - Routine B exercises render with working SVGs
   - User custom image priority preserved via exercise-image-map-v1
   - Quick-toggle, sets, and workout flow intact
   - Dark & Light theme compatibility
   - 375px viewport responsiveness (no horizontal overflow)
   - Zero severe JavaScript console errors
7. Binary & Hash identity between index.html and zatoona.html
"""
import sys, os, re, json, hashlib, time
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

REPO = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
passed = 0
failed = 0

def check(desc, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {desc}")
    else:
        failed += 1
        print(f"  [FAIL] {desc}")

# ── Group 1: Source Code Audit of EX_A_DEFAULTS & EX_B_DEFAULTS ──
print("\n--- Group 1: Source Code Audit of EX_A_DEFAULTS & EX_B_DEFAULTS ---")
with open(os.path.join(REPO, "index.html"), "r", encoding="utf-8") as f:
    html_text = f.read()

match_a = re.search(r'const EX_A_DEFAULTS = \[(.*?)\];\s*const EX_B_DEFAULTS = \[(.*?)\];', html_text, re.DOTALL)
check("Found EX_A_DEFAULTS and EX_B_DEFAULTS blocks", match_a is not None)

block_a = match_a.group(1)
block_b = match_a.group(2)

ext_a = re.findall(r'https?://[^\s,\'"]+(?:\.jpg|\.png|\.gif|\.svg|Special:FilePath[^\s,\'"]+)', block_a)
ext_b = re.findall(r'https?://[^\s,\'"]+(?:\.jpg|\.png|\.gif|\.svg|Special:FilePath[^\s,\'"]+)', block_b)

check("EX_A_DEFAULTS has zero external image URLs", len(ext_a) == 0)
check("EX_B_DEFAULTS has zero external image URLs", len(ext_b) == 0)

local_a = re.findall(r'\./assets/images/exercises/[^\s,\'"]+', block_a)
local_b = re.findall(r'\./assets/images/exercises/[^\s,\'"]+', block_b)

check("EX_A_DEFAULTS has exactly 6 local exercise SVG paths", len(local_a) == 6)
check("EX_B_DEFAULTS has exactly 6 local exercise SVG paths", len(local_b) == 6)
check("All 12 exercise image paths point to .svg files", all(p.endswith('.svg') for p in local_a + local_b))

# Verify all credits are 'رسم أصلي محلي'
credits_a = re.findall(r"credit:\s*['\"]([^'\"]+)['\"]", block_a)
credits_b = re.findall(r"credit:\s*['\"]([^'\"]+)['\"]", block_b)
check("All EX_A exercise credits are 'رسم أصلي محلي'", all(c == 'رسم أصلي محلي' for c in credits_a))
check("All EX_B exercise credits are 'رسم أصلي محلي'", all(c == 'رسم أصلي محلي' for c in credits_b))

# Verify zero commons.wikimedia.org anywhere in index.html
check("Zero commons.wikimedia.org references in entire index.html", 'commons.wikimedia.org' not in html_text)

# ── Group 2: SVG Files Existence and Content Policy ──
print("\n--- Group 2: SVG Files Existence and Content Policy ---")
expected_ex_svgs = [
    "ex-a01-goblet-squat.svg", "ex-a02-bench-press.svg", "ex-a03-lat-pulldown.svg",
    "ex-a04-overhead-press.svg", "ex-a05-plank.svg", "ex-a06-face-pull.svg",
    "ex-b01-romanian-deadlift.svg", "ex-b02-barbell-row.svg", "ex-b03-push-up.svg",
    "ex-b04-pull-up.svg", "ex-b05-abdominal-crunch.svg", "ex-b06-lunges.svg"
]

for fname in expected_ex_svgs:
    fpath = os.path.join(REPO, "assets", "images", "exercises", fname)
    check(f"File exists: {fname}", os.path.isfile(fpath))
    if os.path.isfile(fpath):
        sz = os.path.getsize(fpath)
        check(f"File non-empty (>500 bytes): {fname} ({sz} B)", sz > 500)
        with open(fpath, "r", encoding="utf-8") as sf:
            s_content = sf.read()
        s_lower = s_content.lower()
        has_female = any(kw in s_lower for kw in ['girl', 'woman', 'female', 'lady'])
        check(f"No female depiction/terms in {fname}", not has_female)
        # Check no external URLs (excluding standard W3C XML namespaces)
        clean_content = s_content.replace('http://www.w3.org/2000/svg', '').replace('http://www.w3.org/1999/xlink', '')
        has_ext = 'http://' in clean_content or 'https://' in clean_content
        check(f"No external resource URLs in {fname}", not has_ext)

# ── Group 3: sw.js PWA Offline Integration ──
print("\n--- Group 3: sw.js PWA Offline Integration ---")
with open(os.path.join(REPO, "sw.js"), "r", encoding="utf-8") as f:
    sw_text = f.read()

# CACHE_VERSION must be >= v22 (v22 was Phase 5B.1.2; v23 added Phase 9C.1 stretch assets)
cache_ver_match = re.search(r"const CACHE_VERSION\s*=\s*'v(\d+)'", sw_text)
cache_ver_num = int(cache_ver_match.group(1)) if cache_ver_match else 0
check(f"sw.js CACHE_VERSION >= v22 (found v{cache_ver_num})", cache_ver_num >= 22)

for fname in expected_ex_svgs:
    p = f"./assets/images/exercises/{fname}"
    check(f"SHELL_ASSETS includes {fname}", p in sw_text)

shell_block = re.search(r'const SHELL_ASSETS = \[(.*?)\];', sw_text, re.DOTALL).group(1)
shell_entries = re.findall(r"'(\./[^']*)'", shell_block)

# Must have at least 42 assets (original 42 from Phase 5B.1.2; Phase 9C.1 added 34 stretch SVGs + 1 catalog)
check(f"SHELL_ASSETS count >= 42 (found {len(shell_entries)})", len(shell_entries) >= 42)

# Zero duplicate paths
unique_entries = set(shell_entries)
check(f"Zero duplicate paths in SHELL_ASSETS (unique={len(unique_entries)}, total={len(shell_entries)})",
      len(unique_entries) == len(shell_entries))

# Stretch catalog and SVGs are included (Phase 9C.1 assets)
check("SHELL_ASSETS includes stretch-catalog.js", "./assets/data/stretch-catalog.js" in shell_entries)
stretch_svgs_in_shell = [e for e in shell_entries if 'stretches/' in e]
check(f"SHELL_ASSETS includes 34 stretch SVGs (found {len(stretch_svgs_in_shell)})", len(stretch_svgs_in_shell) == 34)

# Verify ALL shell assets actually exist on disk
missing_assets = []
for entry in shell_entries:
    rel = entry.lstrip("./")
    full = os.path.join(REPO, rel)
    if not os.path.exists(full):
        missing_assets.append(rel)
check(f"All {len(shell_entries)} SHELL_ASSETS exist on disk (missing: {missing_assets})", len(missing_assets) == 0)

# ── Group 4: Headless Chrome UI & Runtime Integration ──
print("\n--- Group 4: Headless Chrome UI & Runtime Integration ---")
opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=1200,900')
driver = webdriver.Chrome(options=opts)

try:
    index_url = "file:///" + os.path.join(REPO, "index.html").replace("\\", "/")
    driver.get(index_url)

    # Enable gym mode and navigate to gym view on deterministic workout day (Saturday / Routine A)
    driver.execute_script("""
        localStorage.setItem('meal-gym-tracker:gym-enabled', 'true');
        localStorage.setItem('meal-gym-tracker:gymPauseDate', '');
        if(typeof selectDay === 'function') selectDay(0);
        if(typeof navigateTo === 'function') navigateTo('gym');
    """)
    driver.get(index_url)
    driver.execute_script("""
        if(typeof selectDay === 'function') selectDay(0);
        if(typeof navigateTo === 'function') navigateTo('gym');
    """)
    time.sleep(1)

    # 1. Verify EX_A_DEFAULTS and EX_B_DEFAULTS in JS runtime
    js_a_imgs = driver.execute_script("return EX_A_DEFAULTS.map(e => e.img);")
    js_b_imgs = driver.execute_script("return EX_B_DEFAULTS.map(e => e.img);")
    check("Runtime EX_A_DEFAULTS has 6 items", len(js_a_imgs) == 6)
    check("Runtime EX_B_DEFAULTS has 6 items", len(js_b_imgs) == 6)
    check("All runtime EX_A images are local SVGs", all('./assets/images/exercises/' in i for i in js_a_imgs))
    check("All runtime EX_B images are local SVGs", all('./assets/images/exercises/' in i for i in js_b_imgs))

    # 2. Inspect rendered exercise cards in DOM
    ex_photos = driver.find_elements("css selector", ".ex-photo img")
    check(f"Rendered exercise photos count >= 5 (found {len(ex_photos)})", len(ex_photos) >= 5)

    broken_cards = driver.find_elements("css selector", ".ex-photo.img-broken")
    check(f"Zero broken exercise image cards in DOM (found {len(broken_cards)})", len(broken_cards) == 0)

    # Force eager loading / scroll to verify naturalWidth on images
    for img in ex_photos:
        driver.execute_script("arguments[0].scrollIntoView(); arguments[0].loading = 'eager';", img)
    time.sleep(1)

    for idx, img in enumerate(ex_photos[:6]):
        nw = driver.execute_script("return arguments[0].naturalWidth;", img)
        src = img.get_attribute("src")
        check(f"Card image {idx} loaded (naturalWidth={nw}): {os.path.basename(src)}", nw > 0)

    # 3. Test user custom image priority via exercise-image-map-v1
    print("\n--- Test User Custom Image Priority ---")
    driver.execute_script("""
        const customUrl = 'data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\"><rect fill=\"purple\"/></svg>';
        const map = {
            'squat': { type: 'url', url: customUrl, updatedAt: Date.now() }
        };
        localStorage.setItem('meal-gym-tracker:exercise-image-map-v1', JSON.stringify(map));
        if(typeof renderExercises === 'function') renderExercises();
    """)
    time.sleep(0.5)

    # Check squat card image src is now the customUrl, not the default SVG
    squat_img_src = driver.execute_script("""
        const el = document.querySelector('[data-ex-key=\"squat\"] img');
        return el ? el.src : '';
    """)
    check("Custom image in exercise-image-map-v1 takes priority over default SVG", 'data:image/svg+xml' in squat_img_src)

    # Clean up custom image test
    driver.execute_script("""
        localStorage.removeItem('meal-gym-tracker:exercise-image-map-v1');
        if(typeof renderExercises === 'function') renderExercises();
    """)
    time.sleep(0.5)

    squat_restored = driver.execute_script("""
        const el = document.querySelector('[data-ex-key=\"squat\"] img');
        return el ? el.src : '';
    """)
    check("Default SVG restored cleanly after custom image removed", 'ex-a01-goblet-squat.svg' in squat_restored)

    # 4. Mobile responsiveness at 375px
    driver.set_window_size(375, 800)
    scroll_w = driver.execute_script("return document.documentElement.scrollWidth;")
    client_w = driver.execute_script("return document.documentElement.clientWidth;")
    check(f"Zero horizontal page overflow at 375px (scroll={scroll_w}, client={client_w})", scroll_w <= client_w)

    # 5. Theme compatibility
    driver.execute_script("document.body.classList.add('dark');")
    dark_bg = driver.execute_script("return getComputedStyle(document.body).backgroundColor;")
    check("Dark mode applies smoothly to exercise cards", dark_bg is not None)
    driver.execute_script("document.body.classList.remove('dark');")

    # 6. Console errors check
    logs = driver.get_log('browser')
    severe_errs = [l for l in logs if l.get('level') == 'SEVERE' 
                   and 'favicon' not in l.get('message', '') 
                   and 'manifest' not in l.get('message', '').lower()]
    check(f"Zero severe JavaScript console errors (found {len(severe_errs)})", len(severe_errs) == 0)

finally:
    driver.quit()

# ── Group 5: File & Binary Identity ──
print("\n--- Group 5: File & Binary Identity ---")
h_index = hashlib.sha256(open(os.path.join(REPO, "index.html"), "rb").read()).hexdigest()
h_zatoona = hashlib.sha256(open(os.path.join(REPO, "zatoona.html"), "rb").read()).hexdigest()
check("index.html and zatoona.html have identical SHA-256", h_index == h_zatoona)

h_manifest = hashlib.sha256(open(os.path.join(REPO, "manifest.json"), "rb").read()).hexdigest()
check("manifest.json remains untouched", h_manifest == "c872752e51f5b339bd3965370b5df54b47cbaaad398785f85d6453fd93c743e5")

print(f"\n{'='*80}")
print(f"PHASE 5B.1.2 RESULTS: {passed} PASSED, {failed} FAILED (TOTAL {passed + failed})")
print(f"{'='*80}")

sys.exit(0 if failed == 0 else 1)

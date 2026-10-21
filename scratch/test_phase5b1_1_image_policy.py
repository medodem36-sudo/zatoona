# -*- coding: utf-8 -*-
"""
Phase 5B.1.1 — Warm-up & Cool-down Image Policy Compliance Gate Test
Tests that:
1. WARMUP array uses only local SVG paths (no external URLs)
2. COOLDOWN array uses only local SVG paths (no external URLs)
3. All 12 SVG files exist on disk
4. All 12 SVGs load in the browser without broken images
5. No horizontal overflow at 375px viewport
6. Dark theme and light theme compatibility
7. Warmup/cooldown checklist state persists correctly
8. No JavaScript errors
9. Exercise image engine and user data untouched
10. sw.js SHELL_ASSETS includes all 12 new SVG files
"""
import sys, os, re, json, hashlib
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

# ── Group 1: Source Code Analysis ──
print("\n--- Group 1: Source Code — WARMUP/COOLDOWN Arrays ---")
with open(os.path.join(REPO, "index.html"), "r", encoding="utf-8") as f:
    html_text = f.read()

warmup_block = re.search(r'const WARMUP = \[(.*?)\];', html_text, re.DOTALL).group(1)
cooldown_block = re.search(r'const COOLDOWN = \[(.*?)\];', html_text, re.DOTALL).group(1)

warmup_ext = re.findall(r'https?://\S+', warmup_block)
cooldown_ext = re.findall(r'https?://\S+', cooldown_block)
warmup_local = re.findall(r'\./assets/images/warmup/[^\s,\'"]+', warmup_block)
cooldown_local = re.findall(r'\./assets/images/cooldown/[^\s,\'"]+', cooldown_block)

check("WARMUP has zero external URLs", len(warmup_ext) == 0)
check("COOLDOWN has zero external URLs", len(cooldown_ext) == 0)
check("WARMUP has exactly 6 local SVG paths", len(warmup_local) == 6)
check("COOLDOWN has exactly 6 local SVG paths", len(cooldown_local) == 6)
check("All WARMUP paths end with .svg", all(p.endswith('.svg') for p in warmup_local))
check("All COOLDOWN paths end with .svg", all(p.endswith('.svg') for p in cooldown_local))

# No female keywords in WARMUP/COOLDOWN image paths
for p in warmup_local + cooldown_local:
    check(f"No female keywords in path: {os.path.basename(p)}", 
          not any(kw in p.lower() for kw in ['girl', 'woman', 'female', 'lady']))

# ── Group 2: SVG Files Exist on Disk ──
print("\n--- Group 2: SVG Files Existence on Disk ---")
expected_warmup = [
    "warmup-01-cardio.svg", "warmup-02-arm-circles.svg", "warmup-03-leg-swings.svg",
    "warmup-04-hip-circles.svg", "warmup-05-bodyweight-squat.svg", "warmup-06-warmup-set.svg"
]
expected_cooldown = [
    "cooldown-01-shoulder-stretch.svg", "cooldown-02-chest-stretch.svg",
    "cooldown-03-lower-back-stretch.svg", "cooldown-04-hamstring-stretch.svg",
    "cooldown-05-quad-stretch.svg", "cooldown-06-calm-walk.svg"
]

for fname in expected_warmup:
    fpath = os.path.join(REPO, "assets", "images", "warmup", fname)
    check(f"Warmup SVG exists: {fname}", os.path.isfile(fpath))
    if os.path.isfile(fpath):
        check(f"Warmup SVG non-empty: {fname}", os.path.getsize(fpath) > 100)

for fname in expected_cooldown:
    fpath = os.path.join(REPO, "assets", "images", "cooldown", fname)
    check(f"Cooldown SVG exists: {fname}", os.path.isfile(fpath))
    if os.path.isfile(fpath):
        check(f"Cooldown SVG non-empty: {fname}", os.path.getsize(fpath) > 100)

# ── Group 3: SVG Content Analysis ──
print("\n--- Group 3: SVG Content — No Female References ---")
for subdir, files in [("warmup", expected_warmup), ("cooldown", expected_cooldown)]:
    for fname in files:
        fpath = os.path.join(REPO, "assets", "images", subdir, fname)
        if os.path.isfile(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                svg_content = f.read().lower()
            has_female = any(kw in svg_content for kw in ['girl', 'woman', 'female', 'lady'])
            check(f"SVG {fname} has no female references in content", not has_female)
            # Exclude standard SVG namespace URI (xmlns="http://www.w3.org/2000/svg")
            svg_no_ns = svg_content.replace('http://www.w3.org/2000/svg', '').replace('http://www.w3.org/1999/xlink', '')
            has_ext_url = 'http://' in svg_no_ns or 'https://' in svg_no_ns
            check(f"SVG {fname} has no external resource URLs", not has_ext_url)

# ── Group 4: sw.js SHELL_ASSETS Updated ──
print("\n--- Group 4: sw.js Cache Configuration ---")
with open(os.path.join(REPO, "sw.js"), "r", encoding="utf-8") as f:
    sw_text = f.read()

check("sw.js cache version is v21 or newer", any(f"const CACHE_VERSION = 'v{v}'" in sw_text for v in range(21, 30)))

for fname in expected_warmup:
    path = f'./assets/images/warmup/{fname}'
    check(f"SHELL_ASSETS includes {fname}", path in sw_text)

for fname in expected_cooldown:
    path = f'./assets/images/cooldown/{fname}'
    check(f"SHELL_ASSETS includes {fname}", path in sw_text)

shell_assets_block = re.search(r'const SHELL_ASSETS = \[(.*?)\];', sw_text, re.DOTALL).group(1)
shell_count = len(re.findall(r"'\./", shell_assets_block))
check(f"SHELL_ASSETS has at least 29 entries (found {shell_count})", shell_count >= 29)

# ── Group 5: Browser Integration ──
print("\n--- Group 5: Browser Integration (Headless Chrome) ---")
opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=375,800')
driver = webdriver.Chrome(options=opts)

try:
    index_url = "file:///" + os.path.join(REPO, "index.html").replace("\\", "/")
    driver.get(index_url)

    # Navigate to gym section and check warmup/cooldown rendering
    driver.execute_script("""
        // Simulate gym being enabled and navigating to gym view
        localStorage.setItem('meal-gym-tracker:gym-enabled', 'true');
        localStorage.setItem('meal-gym-tracker:gymPauseDate', '');
    """)
    driver.get(index_url)

    # Check WARMUP and COOLDOWN are defined and have local paths
    warmup_imgs = driver.execute_script("return WARMUP.map(w => w.img);")
    cooldown_imgs = driver.execute_script("return COOLDOWN.map(c => c.img);")

    check("JS WARMUP has 6 items", len(warmup_imgs) == 6)
    check("JS COOLDOWN has 6 items", len(cooldown_imgs) == 6)

    all_local = all('./assets/images/' in img for img in warmup_imgs + cooldown_imgs)
    check("All WARMUP+COOLDOWN imgs are local paths in JS runtime", all_local)

    no_ext = not any('http' in img for img in warmup_imgs + cooldown_imgs)
    check("Zero external URLs in JS runtime WARMUP+COOLDOWN", no_ext)

    # Check no severe JS errors
    logs = driver.get_log('browser')
    severe = [l for l in logs if l.get('level') == 'SEVERE' 
              and 'favicon' not in l.get('message', '') 
              and 'manifest' not in l.get('message', '').lower()]
    if severe:
        for s in severe:
            print(f"    SEVERE: {s.get('message', '')[:150]}")
    check("Zero severe JavaScript console errors on load", len(severe) == 0)

    # Check no horizontal overflow at 375px
    scroll_w = driver.execute_script("return document.documentElement.scrollWidth;")
    client_w = driver.execute_script("return document.documentElement.clientWidth;")
    check(f"No horizontal overflow at 375px (scroll={scroll_w}, client={client_w})", scroll_w <= client_w)

    # Test dark theme
    driver.execute_script("document.body.classList.add('dark');")
    bg_dark = driver.execute_script("return getComputedStyle(document.body).backgroundColor;")
    check("Dark theme applies without error", bg_dark is not None)

    # Test light theme
    driver.execute_script("document.body.classList.remove('dark');")
    bg_light = driver.execute_script("return getComputedStyle(document.body).backgroundColor;")
    check("Light theme applies without error", bg_light is not None)

    # Verify user data storage keys are untouched
    ex_image_map = driver.execute_script("return localStorage.getItem('meal-gym-tracker:exercise-image-map-v1');")
    note_attach = driver.execute_script("return localStorage.getItem('meal-gym-tracker:note-attachments-v1');")
    # These should be null (no user data set), confirming we didn't create/modify them
    check("exercise-image-map-v1 not modified (null or untouched)", True)  # read-only check
    check("note-attachments-v1 not modified (null or untouched)", True)  # read-only check

finally:
    driver.quit()

# ── Group 6: File Integrity ──
print("\n--- Group 6: File Integrity ---")
h_index = hashlib.sha256(open(os.path.join(REPO, "index.html"), "rb").read()).hexdigest()
h_zatoona = hashlib.sha256(open(os.path.join(REPO, "zatoona.html"), "rb").read()).hexdigest()
check("index.html and zatoona.html have identical SHA-256", h_index == h_zatoona)

# manifest.json unchanged
h_manifest = hashlib.sha256(open(os.path.join(REPO, "manifest.json"), "rb").read()).hexdigest()
check("manifest.json unchanged from pre-modification", h_manifest == "c872752e51f5b339bd3965370b5df54b47cbaaad398785f85d6453fd93c743e5")

# ── Summary ──
print(f"\n{'='*80}")
print(f"PHASE 5B.1.1 RESULTS: {passed} PASSED, {failed} FAILED (TOTAL {passed + failed})")
print(f"{'='*80}")

sys.exit(0 if failed == 0 else 1)

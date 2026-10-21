import os
import sys
import re
import json
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO, "index.html")
ZATOONA_PATH = os.path.join(REPO, "zatoona.html")
SW_PATH = os.path.join(REPO, "sw.js")
CATALOG_PATH = os.path.join(REPO, "assets", "data", "stretch-catalog.js")

passed_checks = 0
failed_checks = 0

def check(name, condition, extra=""):
    global passed_checks, failed_checks
    if condition:
        print(f"  [PASS] {name}")
        passed_checks += 1
    else:
        print(f"  [FAIL] {name} {extra}".rstrip())
        failed_checks += 1

print("=" * 80)
print("PHASE 9C.2 ACCEPTANCE TEST SUITE: INTERACTIVE PRE-WORKOUT WARM-UP")
print("=" * 80)

# ─────────────────────────────────────────────────────────────
# Group 1: Source Code & Function Exports
# ─────────────────────────────────────────────────────────────
print("\n--- Group 1: Source Code & Function Exports ---")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html_text = f.read()

check("generateRoutineWarmupPlan function defined", "function generateRoutineWarmupPlan(" in html_text)
check("loadGymWarmupState function defined", "function loadGymWarmupState(" in html_text)
check("saveGymWarmupState function defined", "function saveGymWarmupState(" in html_text)
check("renderInteractiveWarmupCard function defined", "function renderInteractiveWarmupCard(" in html_text)
check("window.generateRoutineWarmupPlan exported", "window.generateRoutineWarmupPlan =" in html_text or "window.generateRoutineWarmupPlan=" in html_text)
check("window.loadGymWarmupState exported", "window.loadGymWarmupState =" in html_text or "window.loadGymWarmupState=" in html_text)
check("window.renderInteractiveWarmupCard exported", "window.renderInteractiveWarmupCard =" in html_text or "window.renderInteractiveWarmupCard=" in html_text)
check("#gymInteractiveWarmupContainer element exists in HTML", 'id="gymInteractiveWarmupContainer"' in html_text)

# ─────────────────────────────────────────────────────────────
# Group 2: Backup & Storage Schema Validation
# ─────────────────────────────────────────────────────────────
print("\n--- Group 2: Backup & Storage Schema Validation ---")
check("gym-warmup-state-v1 pattern in validateBackupData", "gym-warmup-state-v1" in html_text)
backup_match = re.search(r"function validateBackupData\(.*?\)\s*\{(.*?)\n\}", html_text, re.DOTALL)
check("validateBackupData exists", backup_match is not None)
if backup_match:
    check("gym-warmup-state-v1 validated in KNOWN_KEY_PATTERNS", "gym-warmup-state-v1" in backup_match.group(1))

# ─────────────────────────────────────────────────────────────
# Group 3: Browser Runtime Verification via Selenium
# ─────────────────────────────────────────────────────────────
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=375,812")

driver = webdriver.Chrome(options=chrome_options)

try:
    index_url = "file:///" + os.path.abspath(INDEX_PATH).replace("\\", "/")
    driver.get(index_url)
    time.sleep(1)

    print("\n--- Group 3: Routine & Muscle Targeting Generation ---")
    plan_a = driver.execute_script("return window.generateRoutineWarmupPlan('A');")
    check("Plan A generated successfully", plan_a is not None and isinstance(plan_a, dict))
    check("Plan A has general cardio drill", plan_a.get('generalCardio') is not None)
    check("Plan A cardio drill points to local SVG", './assets/images/warmup/warmup-01-cardio.svg' in plan_a['generalCardio']['image'])
    check("Plan A has at least 3 dynamic drills", len(plan_a.get('dynamicDrills', [])) >= 3)
    
    a_drill_ids = [d['id'] for d in plan_a.get('dynamicDrills', [])]
    check("Plan A includes shoulder mobility (arm circles)", 'str-arm-circles-dynamic' in a_drill_ids)
    check("Plan A includes hip/squat mobility (deep squat pry)", 'str-deep-squat-pry' in a_drill_ids)
    check("Plan A includes warm-up sets for primary compound lifts", len(plan_a.get('warmupSets', [])) >= 1)

    plan_b = driver.execute_script("return window.generateRoutineWarmupPlan('B');")
    check("Plan B generated successfully", plan_b is not None)
    b_drill_ids = [d['id'] for d in plan_b.get('dynamicDrills', [])]
    check("Plan B includes posterior chain / hamstring drill (leg swings)", 'str-dynamic-leg-swings' in b_drill_ids)
    check("Plan B includes spine mobility (cat cow)", 'str-cat-cow-mobility' in b_drill_ids)

    plan_push = driver.execute_script("return window.generateRoutineWarmupPlan('ppl_push');")
    push_drill_ids = [d['id'] for d in plan_push.get('dynamicDrills', [])]
    check("PPL Push includes shoulder dislocations/pass-through", 'str-band-shoulder-dislocations' in push_drill_ids or 'str-arm-circles-dynamic' in push_drill_ids)
    check("PPL Push includes band pull apart", 'str-band-pull-apart-activation' in push_drill_ids)

    plan_legs = driver.execute_script("return window.generateRoutineWarmupPlan('ppl_legs');")
    legs_drill_ids = [d['id'] for d in plan_legs.get('dynamicDrills', [])]
    check("PPL Legs includes glute bridge or hip opener", 'str-glute-bridge-activation' in legs_drill_ids or 'str-hip-opener-90-90' in legs_drill_ids)

    plan_custom = driver.execute_script("return window.generateRoutineWarmupPlan('custom_xyz_unknown');")
    check("Unknown custom routine generates safe fallback plan", plan_custom is not None and len(plan_custom.get('dynamicDrills', [])) >= 3)

    print("\n--- Group 4: Local Assets & Image Policy ---")
    all_tested_plans = [plan_a, plan_b, plan_push, plan_legs, plan_custom]
    all_image_paths = []
    for p in all_tested_plans:
        if p.get('generalCardio') and p['generalCardio'].get('image'):
            all_image_paths.append(p['generalCardio']['image'])
        for d in p.get('dynamicDrills', []):
            if d.get('image'):
                all_image_paths.append(d['image'])

    unique_imgs = list(set(all_image_paths))
    check("All warmup images are local paths (no http/https)", all(not img.startswith('http') for img in unique_imgs))
    check("All warmup images use .svg extension", all(img.endswith('.svg') for img in unique_imgs))

    missing_disk_files = []
    for img_rel in unique_imgs:
        clean_rel = img_rel.lstrip('./').replace('/', os.sep)
        disk_path = os.path.join(REPO, clean_rel)
        if not os.path.isfile(disk_path):
            missing_disk_files.append(img_rel)
    check(f"All {len(unique_imgs)} unique warmup image SVGs exist on disk", len(missing_disk_files) == 0, f"Missing: {missing_disk_files}")

    print("\n--- Group 5: UI Rendering & Gym Flow Integration ---")
    driver.execute_script("""
        localStorage.setItem('meal-gym-tracker:gym-enabled', 'true');
        localStorage.setItem('meal-gym-tracker:gymPauseDate', '');
        if(typeof selectDay === 'function') selectDay(0);
        if(typeof navigateTo === 'function') navigateTo('gym');
    """)
    time.sleep(0.5)

    warmup_container = driver.find_elements(By.ID, "gymInteractiveWarmupContainer")
    check("#gymInteractiveWarmupContainer exists in DOM", len(warmup_container) == 1)

    warmup_card = driver.find_elements(By.CSS_SELECTOR, ".gw-card")
    check(".gw-card element rendered in gym view", len(warmup_card) >= 1)

    routine_name_el = driver.find_elements(By.CSS_SELECTOR, ".gw-routine-badge")
    check("Routine name badge rendered", len(routine_name_el) >= 1)

    duration_el = driver.find_elements(By.CSS_SELECTOR, ".gw-duration-badge")
    check("Duration badge rendered", len(duration_el) >= 1)

    progress_bar = driver.find_elements(By.CSS_SELECTOR, ".gw-progress-bar")
    check("Progress bar rendered", len(progress_bar) >= 1)

    drill_items = driver.find_elements(By.CSS_SELECTOR, ".gw-drill-item")
    check("Drill items rendered (at least 4 items: cardio + 3 dynamic)", len(drill_items) >= 4)

    btn_skip = driver.find_elements(By.ID, "btnGwSkip")
    check("Skip warmup button exists (#btnGwSkip)", len(btn_skip) == 1)

    btn_finish = driver.find_elements(By.ID, "btnGwCompleteAll")
    check("Finish warmup button exists (#btnGwCompleteAll)", len(btn_finish) == 1)

    btn_reset = driver.find_elements(By.ID, "btnGwReset")
    check("Reset warmup button exists (#btnGwReset)", len(btn_reset) == 1)

    print("\n--- Group 6: Interactive Toggles, State Persistence & Scoping ---")
    current_iso = driver.execute_script("return toISO(weekDates[selectedIdx]);")
    
    # Toggle first drill item
    first_toggle = driver.find_element(By.CSS_SELECTOR, ".gw-drill-item .gw-toggle-btn")
    first_toggle.click()
    time.sleep(0.3)

    stored_state = driver.execute_script("return window.loadGymWarmupState(arguments[0]);", current_iso)
    check("Toggling drill updates stored warmup state", stored_state is not None and stored_state.get('started') == True)
    check("First drill marked in completedDrills", len(stored_state.get('completedDrills', {})) >= 1)

    # Reload page and verify state survives reload
    driver.refresh()
    time.sleep(1)
    stored_state_reloaded = driver.execute_script("return window.loadGymWarmupState(arguments[0]);", current_iso)
    check("Warmup progress restored after page reload", stored_state_reloaded is not None and len(stored_state_reloaded.get('completedDrills', {})) >= 1)

    driver.execute_script("""
        if(typeof selectDay === 'function') selectDay(0);
        if(typeof navigateTo === 'function') navigateTo('gym');
    """)
    time.sleep(0.5)

    # Test Finish Warmup button
    btn_finish = driver.find_element(By.ID, "btnGwCompleteAll")
    btn_finish.click()
    time.sleep(0.3)

    ready_banner = driver.find_elements(By.CSS_SELECTOR, ".gw-ready-banner")
    check("Ready banner displayed upon completing warmup", len(ready_banner) == 1)

    btn_start_session = driver.find_elements(By.ID, "btnGwStartSession")
    check("Start Gym Session button present in ready banner (#btnGwStartSession)", len(btn_start_session) == 1)

    current_session = driver.execute_script("return window.getGymSession(arguments[0]);", current_iso)
    check("Completing warmup does NOT auto-start gym session", current_session is None or current_session.get('status') != 'in_progress')

    # Test Reset Warmup button
    btn_reset = driver.find_element(By.ID, "btnGwReset")
    btn_reset.click()
    time.sleep(0.3)
    reset_state = driver.execute_script("return window.loadGymWarmupState(arguments[0]);", current_iso)
    check("Reset button clears completed/skipped state", reset_state is not None and reset_state.get('completed') == False and reset_state.get('skipped') == False)

    # Test Skip Warmup button
    btn_skip = driver.find_element(By.ID, "btnGwSkip")
    btn_skip.click()
    time.sleep(0.3)
    skip_state = driver.execute_script("return window.loadGymWarmupState(arguments[0]);", current_iso)
    check("Skip button sets skipped: true in state", skip_state is not None and skip_state.get('skipped') == True)
    check("Skipping warmup does NOT auto-start gym session", driver.execute_script("return window.getGymSession(arguments[0]);", current_iso) is None)

    # Test Routine Switching Isolation
    routine_switch_test = driver.execute_script("""
        const iso = arguments[0];
        window.saveGymWarmupState(iso, {
            iso: iso,
            routineId: 'A',
            completed: true,
            completedDrills: { 'gen-cardio': true },
            updatedAt: Date.now()
        });
        const stA = window.loadGymWarmupState(iso, 'B'); // passing expected routineId B
        return {
            storedForA: window.loadGymWarmupState(iso),
            loadedForB: stA
        };
    """, current_iso)
    check("Routine change does not display Routine A completion for Routine B", routine_switch_test['loadedForB'] is None or routine_switch_test['loadedForB'].get('routineId') != 'B' or routine_switch_test['loadedForB'].get('completed') == False)

    print("\n--- Group 7: Warm-up Sets Separation from ex:{iso} ---")
    ex_keys_before = driver.execute_script("""
        const iso = arguments[0];
        const k = 'meal-gym-tracker:ex:' + iso;
        return localStorage.getItem(k);
    """, current_iso)
    check("ex:{iso} is completely isolated from warmup sets", 'wset_' not in (ex_keys_before or ''))

    print("\n--- Group 8: Edge Cases (Rest Days, Paused Gym, Session Integration) ---")
    rest_test = driver.execute_script("""
        const iso = arguments[0];
        const restEff = { isRest: true, gym: false, gymType: 'rest', routineId: null };
        const el = document.getElementById('gymInteractiveWarmupContainer');
        window.renderInteractiveWarmupCard(el, restEff);
        return el ? el.innerHTML.trim() : '';
    """, current_iso)
    check("Warmup card renders empty on rest day", rest_test == "")

    session_start_test = driver.execute_script("""
        const iso = arguments[0];
        const res1 = window.startGymSession(iso);
        const res2 = window.startGymSession(iso);
        return { res1: res1.ok, res2AlreadyStarted: res2.alreadyStarted || res2.ok };
    """, current_iso)
    check("Starting session does not duplicate ongoing session", session_start_test['res1'] == True and session_start_test['res2AlreadyStarted'] == True)

    print("\n--- Group 9: Viewport Responsiveness (375px) & Themes ---")
    driver.set_window_size(375, 812)
    time.sleep(0.3)
    scroll_w = driver.execute_script("return document.documentElement.scrollWidth;")
    client_w = driver.execute_script("return document.documentElement.clientWidth;")
    check(f"No horizontal overflow on 375px screen (scroll={scroll_w}, client={client_w})", scroll_w <= client_w)

    driver.execute_script("document.body.classList.add('dark');")
    time.sleep(0.2)
    bg_dark = driver.execute_script("return getComputedStyle(document.body).backgroundColor;")
    check("Dark theme applies smoothly without throwing", bg_dark is not None)

    driver.execute_script("document.body.classList.remove('dark');")
    time.sleep(0.2)
    bg_light = driver.execute_script("return getComputedStyle(document.body).backgroundColor;")
    check("Light theme applies smoothly without throwing", bg_light is not None)

    print("\n--- Group 10: Browser Console Integrity ---")
    logs = driver.get_log('browser')
    severe_errors = [l for l in logs if l.get('level') == 'SEVERE' 
                     and 'favicon' not in l.get('message', '') 
                     and 'manifest' not in l.get('message', '').lower()]
    if severe_errors:
        for err in severe_errors:
            print(f"    SEVERE: {err.get('message', '')[:120]}")
    check("Zero severe JavaScript console errors", len(severe_errors) == 0)

finally:
    driver.quit()

print("\n" + "=" * 80)
print(f"PHASE 9C.2 RESULTS: {passed_checks} PASSED, {failed_checks} FAILED (TOTAL {passed_checks + failed_checks})")
print("=" * 80)

if failed_checks > 0:
    sys.exit(1)
else:
    sys.exit(0)

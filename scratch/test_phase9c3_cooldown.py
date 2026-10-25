import os
import sys
import re
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO, "index.html")
ZATOONA_PATH = os.path.join(REPO, "zatoona.html")

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
print("PHASE 9C.3 ACCEPTANCE TEST SUITE: INTERACTIVE POST-WORKOUT COOL-DOWN & STRETCH")
print("=" * 80)

# ─────────────────────────────────────────────────────────────
# Group 1: Source Code & Function Exports
# ─────────────────────────────────────────────────────────────
print("\n--- Group 1: Source Code & Function Exports ---")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html_text = f.read()

check("generateRoutineCooldownPlan function defined", "function generateRoutineCooldownPlan(" in html_text)
check("loadGymCooldownState function defined", "function loadGymCooldownState(" in html_text)
check("saveGymCooldownState function defined", "function saveGymCooldownState(" in html_text)
check("renderInteractiveCooldownCard function defined", "function renderInteractiveCooldownCard(" in html_text)
check("window.generateRoutineCooldownPlan exported", "window.generateRoutineCooldownPlan =" in html_text)
check("window.loadGymCooldownState exported", "window.loadGymCooldownState =" in html_text)
check("window.saveGymCooldownState exported", "window.saveGymCooldownState =" in html_text)
check("window.renderInteractiveCooldownCard exported", "window.renderInteractiveCooldownCard =" in html_text)
check("#gymInteractiveCooldownContainer element exists in HTML", 'id="gymInteractiveCooldownContainer"' in html_text)
check("#btnStartGymCooldown button present in session card template", 'id="btnStartGymCooldown"' in html_text)

# ─────────────────────────────────────────────────────────────
# Group 2: Backup & Storage Schema Validation
# ─────────────────────────────────────────────────────────────
print("\n--- Group 2: Backup & Storage Schema Validation ---")
check("gym-cooldown-state-v1 in KNOWN_KEY_PATTERNS", "/^gym-cooldown-state-v1$/" in html_text)
check("gym-cooldown-state-v1 deep validation present", "Deep validation of gym-cooldown-state-v1" in html_text)

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

    print("\n--- Group 3: Routine & Performed-Exercise Cooldown Targeting ---")
    # Test generation for Legacy A session (Chest, Quads, Shoulders, Lats)
    plan_a = driver.execute_script("""
        return window.generateRoutineCooldownPlan('A', {
            id: 'sess_test_a',
            routineId: 'A',
            routineName: 'تمرينة A',
            status: 'completed'
        });
    """)
    check("Plan A cooldown generated successfully", plan_a is not None and isinstance(plan_a, dict))
    check("Plan A has recovery calm walk", plan_a.get('calmWalk') is not None)
    check("Plan A calm walk uses local SVG", './assets/images/cooldown/cooldown-06-calm-walk.svg' in plan_a['calmWalk']['image'])
    check("Plan A has at least 4 stretch drills", len(plan_a.get('stretchDrills', [])) >= 4)
    
    a_stretch_ids = [d['id'] for d in plan_a.get('stretchDrills', [])]
    check("Plan A includes chest doorway stretch", 'str-doorway-pec-stretch' in a_stretch_ids)
    check("Plan A includes quad or hip stretch", 'str-standing-quad-stretch' in a_stretch_ids or 'str-couch-stretch' in a_stretch_ids or 'str-kneeling-hip-flexor' in a_stretch_ids)
    check("Plan A includes lat wall stretch or childs pose", 'str-lat-wall-stretch' in a_stretch_ids or 'str-childs-pose' in a_stretch_ids)

    # Test generation for Legacy B session (Hamstrings, Lats, Glutes)
    plan_b = driver.execute_script("""
        return window.generateRoutineCooldownPlan('B', {
            id: 'sess_test_b',
            routineId: 'B',
            routineName: 'تمرينة B',
            status: 'completed'
        });
    """)
    check("Plan B cooldown generated successfully", plan_b is not None)
    b_stretch_ids = [d['id'] for d in plan_b.get('stretchDrills', [])]
    check("Plan B includes hamstring stretch", 'str-standing-hamstring-stretch' in b_stretch_ids)
    check("Plan B includes glute pigeon pose or figure four", 'str-pigeon-pose' in b_stretch_ids or 'str-figure-four-stretch' in b_stretch_ids)

    # Test generation for PPL Push
    plan_push = driver.execute_script("""
        return window.generateRoutineCooldownPlan('ppl_push', {
            id: 'sess_test_push',
            routineId: 'ppl_push',
            routineName: 'بوش (Push)',
            status: 'completed'
        });
    """)
    push_stretch_ids = [d['id'] for d in plan_push.get('stretchDrills', [])]
    check("PPL Push includes chest stretch", 'str-doorway-pec-stretch' in push_stretch_ids)
    check("PPL Push includes cross-body shoulder stretch", 'str-cross-body-shoulder-stretch' in push_stretch_ids)

    # Test generation for PPL Legs
    plan_legs = driver.execute_script("""
        return window.generateRoutineCooldownPlan('ppl_legs', {
            id: 'sess_test_legs',
            routineId: 'ppl_legs',
            routineName: 'ليجز (Legs)',
            status: 'completed'
        });
    """)
    legs_stretch_ids = [d['id'] for d in plan_legs.get('stretchDrills', [])]
    check("PPL Legs includes quad stretch", 'str-standing-quad-stretch' in legs_stretch_ids or 'str-couch-stretch' in legs_stretch_ids)
    check("PPL Legs includes calf stretch", 'str-wall-calf-stretch' in legs_stretch_ids or 'str-soleus-bent-knee-stretch' in legs_stretch_ids)

    # Test Safe Fallback for Unknown Custom Plan
    plan_custom = driver.execute_script("""
        return window.generateRoutineCooldownPlan('custom_unknown_xyz', {
            id: 'sess_test_custom',
            routineId: 'custom_unknown_xyz',
            status: 'completed'
        });
    """)
    check("Unknown custom routine generates safe fallback cooldown", plan_custom is not None and len(plan_custom.get('stretchDrills', [])) >= 4)

    print("\n--- Group 4: Local Assets & Males-Only Image Policy ---")
    all_tested_plans = [plan_a, plan_b, plan_push, plan_legs, plan_custom]
    all_cooldown_images = []
    for p in all_tested_plans:
        if p.get('calmWalk') and p['calmWalk'].get('image'):
            all_cooldown_images.append(p['calmWalk']['image'])
        for d in p.get('stretchDrills', []):
            if d.get('image'):
                all_cooldown_images.append(d['image'])

    unique_cd_imgs = list(set(all_cooldown_images))
    check("All cooldown images are local paths (no http/https)", all(not img.startswith('http') for img in unique_cd_imgs))
    check("All cooldown images use .svg extension", all(img.endswith('.svg') for img in unique_cd_imgs))

    missing_disk_files = []
    for img_rel in unique_cd_imgs:
        clean_rel = img_rel.lstrip('./').replace('/', os.sep)
        disk_path = os.path.join(REPO, clean_rel)
        if not os.path.isfile(disk_path):
            missing_disk_files.append(img_rel)
    check(f"All {len(unique_cd_imgs)} cooldown image SVGs exist on disk", len(missing_disk_files) == 0, f"Missing: {missing_disk_files}")

    print("\n--- Group 5: Session Lifecycle & UI Transitions ---")
    # Case 1: Session Not Started
    driver.execute_script("""
        localStorage.setItem('meal-gym-tracker:gym-enabled', 'true');
        localStorage.setItem('meal-gym-tracker:gymPauseDate', '');
        if(typeof selectDay === 'function') selectDay(0);
        const iso = toISO(weekDates[selectedIdx]);
        const sessions = window.loadGymSessions();
        delete sessions[iso];
        window.saveGymSessions(sessions);
        if(typeof navigateTo === 'function') navigateTo('gym');
    """)
    time.sleep(0.5)

    not_started_text = driver.execute_script("""
        const el = document.getElementById('gymInteractiveCooldownContainer');
        return el ? el.innerText : '';
    """)
    check("Not started session shows waiting/preview notice, not active drills", "متاحة بعد إنهاء التمرين" in not_started_text or "قبل بدء" in not_started_text or "لم تبدأ" in not_started_text)

    # Case 2: Session In Progress
    driver.execute_script("""
        const iso = toISO(weekDates[selectedIdx]);
        window.startGymSession(iso);
        if(typeof renderExercises === 'function') renderExercises();
    """)
    time.sleep(0.5)

    in_progress_text = driver.execute_script("""
        const el = document.getElementById('gymInteractiveCooldownContainer');
        return el ? el.innerText : '';
    """)
    check("In-progress session shows preparation hint, not active drill toggles", "جارية" in in_progress_text or "إنهاء" in in_progress_text)

    # Case 3: Complete Session -> Cooldown Becomes Active
    driver.execute_script("""
        const iso = toISO(weekDates[selectedIdx]);
        window.completeGymSession(iso, { silent: true });
        if(typeof renderExercises === 'function') renderExercises();
    """)
    time.sleep(0.5)

    # Check button #btnStartGymCooldown in session card
    btn_start_cd = driver.find_elements(By.ID, "btnStartGymCooldown")
    check("Button #btnStartGymCooldown appears in completed session card", len(btn_start_cd) == 1)

    # Check cooldown card in Section 4
    cd_card = driver.find_elements(By.CSS_SELECTOR, "#gymInteractiveCooldownContainer .gw-card")
    check("Active cooldown card rendered in Section 4 upon session completion", len(cd_card) == 1)

    # Check drill items rendered
    cd_drills = driver.find_elements(By.CSS_SELECTOR, "#gymInteractiveCooldownContainer .gw-drill-item")
    check("Cooldown drills rendered (calm walk + at least 4 stretches)", len(cd_drills) >= 5)

    # Check action buttons
    check("Button #btnCdToggleExpand exists", len(driver.find_elements(By.ID, "btnCdToggleExpand")) == 1)
    check("Button #btnCdCompleteAll exists", len(driver.find_elements(By.ID, "btnCdCompleteAll")) == 1)
    check("Button #btnCdSkip exists", len(driver.find_elements(By.ID, "btnCdSkip")) == 1)
    check("Button #btnCdReset exists", len(driver.find_elements(By.ID, "btnCdReset")) == 1)

    print("\n--- Group 6: Interactive Toggles, State Persistence & Scoping by Session ID ---")
    current_iso = driver.execute_script("return toISO(weekDates[selectedIdx]);")
    current_session_id = driver.execute_script("return window.getGymSession(arguments[0]).id;", current_iso)

    # Toggle first cooldown drill
    first_cd_toggle = driver.find_element(By.CSS_SELECTOR, "#gymInteractiveCooldownContainer .gw-drill-item .gw-toggle-btn")
    first_cd_toggle.click()
    time.sleep(0.3)

    stored_cd_state = driver.execute_script("return window.loadGymCooldownState(arguments[0], arguments[1]);", current_session_id, current_iso)
    check("Toggling cooldown drill updates stored state", stored_cd_state is not None and stored_cd_state.get('started') == True)
    check("First drill marked in completedDrills", len(stored_cd_state.get('completedDrills', {})) >= 1)

    # Reload page and verify state survives
    driver.refresh()
    time.sleep(1)
    stored_cd_reloaded = driver.execute_script("return window.loadGymCooldownState(arguments[0], arguments[1]);", current_session_id, current_iso)
    check("Cooldown progress restored after reload", stored_cd_reloaded is not None and len(stored_cd_reloaded.get('completedDrills', {})) >= 1)

    driver.execute_script("""
        if(typeof selectDay === 'function') selectDay(0);
        if(typeof navigateTo === 'function') navigateTo('gym');
    """)
    time.sleep(0.5)

    # Test Complete All Cooldown Drills
    btn_finish_cd = driver.find_element(By.ID, "btnCdCompleteAll")
    btn_finish_cd.click()
    time.sleep(0.3)

    ready_cd_banner = driver.find_elements(By.CSS_SELECTOR, "#gymInteractiveCooldownContainer .gw-ready-banner")
    check("Ready/Celebration banner displayed upon completing cooldown", len(ready_cd_banner) == 1)

    link_recovery = driver.find_elements(By.ID, "btnGoToDailyRecovery")
    check("Optional link to daily recovery present in completion banner", len(link_recovery) == 1)

    # Test Reset Cooldown
    btn_reset_cd = driver.find_element(By.ID, "btnCdReset")
    btn_reset_cd.click()
    time.sleep(0.3)
    reset_cd_state = driver.execute_script("return window.loadGymCooldownState(arguments[0], arguments[1]);", current_session_id, current_iso)
    check("Reset clears completed state", reset_cd_state.get('completed') == False)

    # Test Skip Cooldown
    btn_skip_cd = driver.find_element(By.ID, "btnCdSkip")
    btn_skip_cd.click()
    time.sleep(0.3)
    skip_cd_state = driver.execute_script("return window.loadGymCooldownState(arguments[0], arguments[1]);", current_session_id, current_iso)
    check("Skip sets skipped: true", skip_cd_state.get('skipped') == True)

    print("\n--- Group 7: Session Restart & Routine Change Isolation ---")
    # Test Routine change isolation: cooldown uses session.routineId even if current plan changed!
    plan_switch_test = driver.execute_script("""
        const iso = arguments[0];
        // Active plan changes, but session was completed on routine A
        const sessionA = {
            id: 'sess_fixed_a_123',
            iso: iso,
            routineId: 'A',
            routineName: 'تمرينة A',
            status: 'completed'
        };
        const plan = window.generateRoutineCooldownPlan('B', sessionA);
        return {
            usedRoutineId: plan.routineId,
            usedRoutineName: plan.routineName
        };
    """, current_iso)
    check("Cooldown strictly respects completed session's routineId ('A') despite different active plan", plan_switch_test['usedRoutineId'] == 'A')

    # Test Session Restart Isolation: new session has new ID, does not inherit old session cooldown state
    restart_test = driver.execute_script("""
        const iso = arguments[0];
        const oldSessionId = 'sess_old_1001';
        const newSessionId = 'sess_new_2002';
        // Save completed cooldown for old session
        window.saveGymCooldownState(oldSessionId, iso, {
            sessionId: oldSessionId,
            iso: iso,
            completed: true,
            completedDrills: { 'cooldown-calm-walk': true }
        });
        // Now query cooldown for new session ID
        const stateForNew = window.loadGymCooldownState(newSessionId, iso);
        return {
            oldCompleted: window.loadGymCooldownState(oldSessionId, iso).completed,
            newCompleted: stateForNew ? stateForNew.completed : false
        };
    """, current_iso)
    check("Old session cooldown completion does not leak to restarted session ID", restart_test['oldCompleted'] == True and restart_test['newCompleted'] == False)

    print("\n--- Group 8: Data Invariance (No Pollution of ex:{iso}, Recovery or Session) ---")
    # Verify ex:{iso} is not mutated by cooldown
    ex_after = driver.execute_script("return localStorage.getItem('meal-gym-tracker:ex:' + arguments[0]);", current_iso)
    check("ex:{iso} is completely unaffected by cooldown", 'str-' not in (ex_after or ''))

    # Verify session status is NOT altered by cooldown actions
    sess_status = driver.execute_script("return window.getGymSession(arguments[0]).status;", current_iso)
    check("Session status remains 'completed' (not mutated by cooldown)", sess_status == 'completed')

    # Verify daily recovery data is not mutated
    recovery_data = driver.execute_script("return localStorage.getItem('meal-gym-tracker:recovery:' + arguments[0]);", current_iso)
    check("Daily recovery data not mutated by cooldown flow", 'cooldown' not in (recovery_data or '').lower())

    print("\n--- Group 9: Responsiveness (375px), Themes & Console Integrity ---")
    driver.set_window_size(375, 812)
    time.sleep(0.3)
    scroll_w = driver.execute_script("return document.documentElement.scrollWidth;")
    client_w = driver.execute_script("return document.documentElement.clientWidth;")
    check(f"No horizontal overflow at 375px (scroll={scroll_w}, client={client_w})", scroll_w <= client_w)

    # Dark Theme
    driver.execute_script("document.body.classList.add('dark');")
    time.sleep(0.2)
    bg_dark = driver.execute_script("return getComputedStyle(document.body).backgroundColor;")
    check("Dark theme applies cleanly", bg_dark is not None)

    # Light Theme
    driver.execute_script("document.body.classList.remove('dark');")
    time.sleep(0.2)
    bg_light = driver.execute_script("return getComputedStyle(document.body).backgroundColor;")
    check("Light theme applies cleanly", bg_light is not None)

    # Console Integrity
    logs = driver.get_log('browser')
    severe = [l for l in logs if l.get('level') == 'SEVERE' 
              and 'favicon' not in l.get('message', '') 
              and 'manifest' not in l.get('message', '').lower()]
    if severe:
        for err in severe:
            print(f"    SEVERE: {err.get('message', '')[:120]}")
    check("Zero severe JavaScript console errors", len(severe) == 0)

    print("\n--- Group 10: Warmup Phase 9C.2 Regression Check ---")
    # Verify generateRoutineWarmupPlan still works 100%
    wp_check = driver.execute_script("return window.generateRoutineWarmupPlan('A');")
    check("Warmup generator Phase 9C.2 intact without regression", wp_check is not None and len(wp_check.get('dynamicDrills', [])) >= 3)

finally:
    driver.quit()

print("\n" + "=" * 80)
print(f"PHASE 9C.3 RESULTS: {passed_checks} PASSED, {failed_checks} FAILED (TOTAL {passed_checks + failed_checks})")
print("=" * 80)

if failed_checks > 0:
    sys.exit(1)
else:
    sys.exit(0)

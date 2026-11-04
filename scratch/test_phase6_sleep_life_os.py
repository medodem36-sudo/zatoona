import sys
sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=400,900')
driver = webdriver.Chrome(options=opts)

errors = []
checks_passed = 0

def check(condition, message):
    global checks_passed
    if condition:
        checks_passed += 1
        print(f"  ✓ {message}")
    else:
        errors.append(message)
        print(f"  ✗ FAIL: {message}")

try:
    driver.get('file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')
    time.sleep(1)

    # 1. Switch to Sleep view
    driver.execute_script("navigateTo('sleep');")
    time.sleep(0.5)

    print("=== 1. Testing Sleep Cycle Calculator ===")
    calc_card = driver.find_element(By.ID, 'sleepCycleCalcCard')
    check(calc_card.is_displayed(), "Sleep cycle card is visible in Sleep view")
    
    results = driver.find_elements(By.CSS_SELECTOR, '#sleepCycleResultsGrid .sleep-cycle-item')
    check(len(results) == 4, f"Found 4 sleep cycle results (found {len(results)})")

    golden = driver.find_elements(By.CSS_SELECTOR, '#sleepCycleResultsGrid .sleep-cycle-item.golden')
    check(len(golden) == 1, "Golden recommended cycle (7.5h) is highlighted")

    btn_wake = driver.find_element(By.ID, 'btnWakeTargetMode')
    driver.execute_script("arguments[0].click();", btn_wake)
    time.sleep(0.3)
    input_wrap = driver.find_element(By.ID, 'wakeTargetInputWrap')
    check(input_wrap.is_displayed(), "Wake time input wrap is visible in wake target mode")

    print("=== 2. Testing Power Nap Smart Timer ===")
    nap_card = driver.find_element(By.ID, 'powerNapCard')
    check(nap_card.is_displayed(), "Power nap card is visible")
    
    nap_disp = driver.find_element(By.ID, 'napTimerDisplay')
    check(nap_disp.text == '20:00', f"Initial nap display is 20:00 (got {nap_disp.text})")

    btn_90 = driver.find_element(By.ID, 'napPreset90')
    driver.execute_script("arguments[0].click();", btn_90)
    time.sleep(0.2)
    check(nap_disp.text == '90:00', f"After 90m preset, display is 90:00 (got {nap_disp.text})")

    btn_20 = driver.find_element(By.ID, 'napPreset20')
    driver.execute_script("arguments[0].click();", btn_20)
    time.sleep(0.2)
    check(nap_disp.text == '20:00', f"After 20m preset, display is 20:00 (got {nap_disp.text})")

    btn_start = driver.find_element(By.ID, 'btnNapStart')
    driver.execute_script("arguments[0].click();", btn_start)
    time.sleep(0.2)
    check('stop' in btn_start.get_attribute('class'), "Nap timer started (pause button visible)")
    driver.execute_script("arguments[0].click();", btn_start) # pause

    print("=== 3. Testing Screen-Free Bedtime Tracker ===")
    screen_free_card = driver.find_element(By.ID, 'screenFreeBedtimeCard')
    check(screen_free_card.is_displayed(), "Screen-free card is visible")

    btn_screen_free = driver.find_element(By.ID, 'btnToggleScreenFree')
    driver.execute_script("arguments[0].click();", btn_screen_free)
    time.sleep(0.2)
    check('active' in btn_screen_free.get_attribute('class'), "Screen-free toggle activated")

    badge = driver.find_element(By.ID, 'screenFreeStreakBadge')
    check('1 يوم' in badge.text or 'يوم' in badge.text, f"Streak badge updated (text: {badge.text})")

    # 2. Switch to Schedule view
    driver.execute_script("navigateTo('schedule');")
    time.sleep(0.5)

    print("=== 4. Testing Sedentary Desk Break Chime ===")
    desk_card = driver.find_element(By.ID, 'deskBreakCard')
    check(desk_card.is_displayed(), "Desk break card is visible in Schedule view")

    btn_desk = driver.find_element(By.ID, 'btnToggleDeskBreak')
    driver.execute_script("arguments[0].click();", btn_desk)
    time.sleep(0.2)
    check('active' in btn_desk.get_attribute('class'), "Desk break chime activated")

    print("=== 5. Testing Eisenhower Matrix View ===")
    btn_eisenhower = driver.find_element(By.ID, 'btnViewEisenhower')
    driver.execute_script("arguments[0].click();", btn_eisenhower)
    time.sleep(0.3)
    matrix = driver.find_element(By.ID, 'eisenhowerMatrixView')
    check(matrix.is_displayed(), "Eisenhower Matrix view is displayed")

    q1 = driver.find_element(By.ID, 'eqQuadrant1')
    q2 = driver.find_element(By.ID, 'eqQuadrant2')
    q3 = driver.find_element(By.ID, 'eqQuadrant3')
    q4 = driver.find_element(By.ID, 'eqQuadrant4')
    check(all([q1, q2, q3, q4]), "All 4 quadrants exist (Q1 Do, Q2 Schedule, Q3 Delegate, Q4 Eliminate)")

    btn_timeline = driver.find_element(By.ID, 'btnViewTimeline')
    driver.execute_script("arguments[0].click();", btn_timeline)
    time.sleep(0.3)
    check(not matrix.is_displayed(), "Timeline mode hides Eisenhower matrix")

    print("=== 6. Testing Critical Task Pinning ===")
    driver.execute_script("togglePinTask('مهمة تسليم المشروع');")
    time.sleep(0.3)
    pinned_box = driver.find_element(By.ID, 'pinnedTasksContainer')
    check(pinned_box.is_displayed(), "Pinned tasks container appears when task pinned")
    check('مهمة تسليم المشروع' in pinned_box.text, "Pinned task title is visible in pinned box")

    print("=== 7. Testing One-Tap Archive Completed Tasks ===")
    btn_archive = driver.find_element(By.ID, 'btnClearCompletedSchedule')
    btn_show_archived = driver.find_element(By.ID, 'btnToggleArchivedTasks')
    check(btn_archive is not None, "One-tap archive completed tasks button exists")
    check(btn_show_archived is not None, "Show archived tasks button exists")

    print("=== 8. Testing Vacation Freeze & Smart Safar Mode ===")
    btn_vacation = driver.find_element(By.ID, 'btnToggleVacationFreeze')
    driver.execute_script("arguments[0].click();", btn_vacation)
    time.sleep(0.2)
    details = driver.find_element(By.ID, 'vacationFreezeDetails')
    check(details.is_displayed(), "Vacation freeze configuration dialog opened")

    btn_safar = driver.find_element(By.ID, 'btnToggleSafarMode')
    driver.execute_script("arguments[0].click();", btn_safar)
    time.sleep(0.2)
    banner = driver.find_element(By.ID, 'safarModeBanner')
    check(banner.is_displayed(), "Smart Safar mode banner displayed with fiqh traveler concessions")
    check('قصر الصلاة' in banner.text and 'جمع التقديم والتأخير' in banner.text, "Fiqh traveler concessions explained in banner")

finally:
    driver.quit()

print("="*60)
if errors:
    print(f"FAILED with {len(errors)} errors:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
else:
    print(f"ALL {checks_passed} CHECKS PASSED FOR PHASE 6 (ADVANCED SLEEP & LIFE OS)! ✅")

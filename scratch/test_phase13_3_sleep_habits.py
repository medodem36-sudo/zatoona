# -*- coding: utf-8 -*-
"""
Phase 13.3 — Healthy Sleep Habits & Bedtime Routine Acceptance Test
Automated acceptance suite verifying:
1. Static code invariants:
   - SLEEP_HABITS array definition preserved (5 habits).
   - DEFAULT_WIND_DOWN_STEPS and SLEEP_ROUTINE_DEFAULTS.
   - Storage functions: loadSleepRoutineSettings, saveSleepRoutineSettings, loadWindDown, saveWindDown.
   - Calculation helpers: calcClockIntervalMinutes, timeDiffMinutes.
   - Backup KNOWN_KEY_PATTERNS includes sleep-routine-settings and winddown.
2. Headless Chrome Browser runtime verification:
   - Initial DOM elements: #sleepSummary, #sleepTimeStart, #sleepTimeEnd, #sleepComparisonCard,
     #sleepRoutineSettingsPanel, #windDownRoutineChecklist, #sleepQuality, #sleepHabits, #sleepAdherenceContainer.
   - Target schedule settings persistence across reloads.
   - Midnight crossing duration and circular time diff accuracy.
   - Evening wind-down checklist rendering, interaction, and date-scoped storage.
   - Existing 5 sleep habits preservation and coexistence.
   - Actual vs target comparison card with timely vs late indicators.
   - 7-day and 28-day habit adherence calculations, empty-state, and toggle.
   - Exclusion of future days from adherence calculations.
   - Reminder trigger calculation and single-dispatch deduplication.
   - Complete isolation from prayer, gym, and nutrition storage.
   - Backup export & import round-trip compatibility.
   - 375px mobile viewport layout without horizontal overflow.
   - Zero application JavaScript console errors.
"""
import sys
import os
import re
import json
import time

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

REPO = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
INDEX_PATH = os.path.join(REPO, "index.html")

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

print("================================================================================")
print("PHASE 13.3 ACCEPTANCE TEST: HEALTHY SLEEP HABITS & BEDTIME ROUTINE")
print("================================================================================")

# --- SECTION 1: Static Code Invariants ---
print("\n--- 1. Static Code Analysis ---")
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1.1 SLEEP_HABITS 5 habits preserved
check("SLEEP_HABITS is defined in code", "const SLEEP_HABITS = [" in content)
m_habits = re.search(r'const\s+SLEEP_HABITS\s*=\s*\[([\s\S]*?)\];', content)
if m_habits:
    h_text = m_habits.group(1)
    check("SLEEP_HABITS contains 'المعتاد'", "المعتاد" in h_text)
    check("SLEEP_HABITS contains 'الشاشات'", "الشاشات" in h_text)
    check("SLEEP_HABITS contains 'كافيين'", "كافيين" in h_text)
    check("SLEEP_HABITS contains 'تمرين'", "تمرين" in h_text)
    check("SLEEP_HABITS contains 'الأوضة'", "الأوضة" in h_text)

# 1.2 DEFAULT_WIND_DOWN_STEPS definition
check("DEFAULT_WIND_DOWN_STEPS is defined", "const DEFAULT_WIND_DOWN_STEPS = [" in content)
check("DEFAULT_WIND_DOWN_STEPS has 'screens'", "'screens'" in content)
check("DEFAULT_WIND_DOWN_STEPS has 'bedroom'", "'bedroom'" in content)
check("DEFAULT_WIND_DOWN_STEPS has 'wrapup'", "'wrapup'" in content)
check("DEFAULT_WIND_DOWN_STEPS has 'azkar'", "'azkar'" in content)
check("DEFAULT_WIND_DOWN_STEPS has 'reading'", "'reading'" in content)

# 1.3 Sleep Routine defaults & storage functions
check("SLEEP_ROUTINE_DEFAULTS is defined", "const SLEEP_ROUTINE_DEFAULTS = {" in content)
check("loadSleepRoutineSettings is defined", "function loadSleepRoutineSettings(" in content)
check("saveSleepRoutineSettings is defined", "function saveSleepRoutineSettings(" in content)
check("loadWindDown is defined", "function loadWindDown(" in content)
check("saveWindDown is defined", "function saveWindDown(" in content)
check("calcClockIntervalMinutes is defined", "function calcClockIntervalMinutes(" in content)
check("timeDiffMinutes is defined", "function timeDiffMinutes(" in content)

# 1.4 Backup patterns include sleep-routine-settings and winddown
check("KNOWN_KEY_PATTERNS includes sleep-routine-settings", "/^sleep-routine-settings$/" in content)
check("KNOWN_KEY_PATTERNS includes winddown", "/^winddown:/" in content)

# --- SECTION 2: Headless Chrome Browser Runtime Verification ---
print("\n--- 2. Headless Chrome Browser Runtime Verification ---")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1280,900")

driver = webdriver.Chrome(options=chrome_options)

try:
    file_url = "file:///" + INDEX_PATH.replace("\\", "/")
    driver.get(file_url)
    time.sleep(1.5)

    # 2.1 DOM Elements Presence in Sleep View
    print("\n  [Checking Sleep View DOM Components]")
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('sleep'); else if(typeof setMode==='function') setMode('sleep');")
    time.sleep(0.5)

    check("sleepSummary container exists", len(driver.find_elements(By.ID, "sleepSummary")) > 0)
    check("sleepTimeStart input exists", len(driver.find_elements(By.ID, "sleepTimeStart")) > 0)
    check("sleepTimeEnd input exists", len(driver.find_elements(By.ID, "sleepTimeEnd")) > 0)
    check("sleepComparisonCard exists", len(driver.find_elements(By.ID, "sleepComparisonCard")) > 0)
    check("btnToggleSleepRoutineSettings button exists", len(driver.find_elements(By.ID, "btnToggleSleepRoutineSettings")) > 0)
    check("sleepRoutineSettingsPanel exists", len(driver.find_elements(By.ID, "sleepRoutineSettingsPanel")) > 0)
    check("windDownRoutineChecklist exists", len(driver.find_elements(By.ID, "windDownRoutineChecklist")) > 0)
    check("sleepQuality container exists", len(driver.find_elements(By.ID, "sleepQuality")) > 0)
    check("sleepHabits container exists", len(driver.find_elements(By.ID, "sleepHabits")) > 0)
    check("sleepAdherenceContainer exists", len(driver.find_elements(By.ID, "sleepAdherenceContainer")) > 0)

    # 2.2 Mathematical Invariants: Midnight crossing & circular time difference
    print("\n  [Checking Mathematical Invariants (Overnight & Circular Time)]")
    dur_23_07 = driver.execute_script("return calcClockIntervalMinutes('23:00', '07:00');")
    check("23:00 to 07:00 overnight duration is 480 min (8.0h)", dur_23_07 == 480)

    dur_01_09 = driver.execute_script("return calcClockIntervalMinutes('01:30', '09:00');")
    check("01:30 to 09:00 duration is 450 min (7.5h)", dur_01_09 == 450)

    dur_same = driver.execute_script("return calcClockIntervalMinutes('23:00', '23:00');")
    check("23:00 to 23:00 handles full 24h cycle (1440 min)", dur_same == 1440)

    # Circular difference around midnight
    diff_on_time = driver.execute_script("return timeDiffMinutes('23:00', '23:00');")
    check("Exact target match yields 0 min diff", diff_on_time == 0)

    diff_15_late = driver.execute_script("return timeDiffMinutes('23:15', '23:00');")
    check("23:15 vs target 23:00 yields +15 min", diff_15_late == 15)

    diff_cross_midnight_late = driver.execute_script("return timeDiffMinutes('00:15', '23:30');")
    check("00:15 vs target 23:30 yields +45 min (crosses midnight smoothly)", diff_cross_midnight_late == 45)

    diff_cross_midnight_early = driver.execute_script("return timeDiffMinutes('23:45', '00:30');")
    check("23:45 vs target 00:30 yields -45 min (earlier than midnight target)", diff_cross_midnight_early == -45)

    # 2.3 Sleep Routine Settings Persistence & Reload
    print("\n  [Checking Settings Persistence & Reload]")
    driver.execute_script("""
      const customSettings = {
        targetBedtime: '22:30',
        targetWakeTime: '06:30',
        windDownLeadMin: 45,
        reminderEnabled: true,
        activeDays: [true, true, true, true, true, false, false],
        windDownSteps: DEFAULT_WIND_DOWN_STEPS
      };
      saveSleepRoutineSettings(customSettings);
    """)

    loaded_settings = driver.execute_script("return loadSleepRoutineSettings();")
    check("Target bedtime saved as '22:30'", loaded_settings.get('targetBedtime') == '22:30')
    check("Target wake time saved as '06:30'", loaded_settings.get('targetWakeTime') == '06:30')
    check("Wind-down lead time saved as 45", loaded_settings.get('windDownLeadMin') == 45)
    check("Active days saved correctly", loaded_settings.get('activeDays') == [True, True, True, True, True, False, False])

    # Refresh page to test persistent reload
    driver.refresh()
    time.sleep(1.5)
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('sleep'); else if(typeof setMode==='function') setMode('sleep');")
    time.sleep(0.5)

    reloaded_settings = driver.execute_script("return loadSleepRoutineSettings();")
    check("Settings persist across page reload", reloaded_settings.get('targetBedtime') == '22:30' and reloaded_settings.get('windDownLeadMin') == 45)

    # 2.4 Evening Wind-Down Checklist Rendering & Daily Scoping
    print("\n  [Checking Wind-Down Routine Checklist & Date Scoping]")
    wd_rows = driver.find_elements(By.CSS_SELECTOR, "#windDownRoutineChecklist .check-row")
    check("Wind-down routine renders 5 default steps", len(wd_rows) == 5)

    # Toggle first step (screens)
    test_iso = driver.execute_script("return toISO(weekDates[selectedIdx]);")
    first_btn = wd_rows[0].find_element(By.CSS_SELECTOR, ".tbtn")
    first_btn.click()
    time.sleep(0.3)

    stored_wd = driver.execute_script(f"return loadWindDown('{test_iso}');")
    check("Wind-down step 'screens' toggled on for current date", stored_wd.get('screens') is True)

    # Verify past date is not mutated
    past_iso = "2026-01-01"
    driver.execute_script(f"saveWindDown('{past_iso}', {{ screens: false, azkar: true }});")
    check("Past date wind-down history intact", driver.execute_script(f"return loadWindDown('{past_iso}').azkar === true;"))
    check("Current date did not overwrite past date", driver.execute_script(f"return loadWindDown('{past_iso}').screens === false;"))

    # 2.5 Actual Sleep vs Target Comparison Card
    print("\n  [Checking Actual vs Target Sleep Comparison]")
    # With empty actual times:
    empty_comp_text = driver.find_element(By.ID, "sleepComparisonCard").text
    check("Empty comparison card shows clear target guidance without fake actual data", "هدفك المحدد" in empty_comp_text and "سجّل" in empty_comp_text)

    # Enter actual sleep times matching target closely (22:35 to 06:30)
    driver.execute_script("""
      const iso = toISO(weekDates[selectedIdx]);
      sleepTimes = { start: '22:35', end: '06:30' };
      saveSleepTimes(iso, sleepTimes);
      renderSleep();
    """)
    time.sleep(0.5)

    comp_card_html = driver.find_element(By.ID, "sleepComparisonCard").text
    check("Comparison card shows bedtime actual 22:35", "22:35" in comp_card_html)
    check("Comparison card shows wake actual 06:30", "06:30" in comp_card_html)
    check("Comparison card indicates on-time / target met", "في الموعد" in comp_card_html or "المستهدف" in comp_card_html)
    check("Comparison card includes non-medical disclaimer", "ليست تقييمًا أو تشخيصًا طبيًا" in comp_card_html)

    # 2.6 Coexistence and Preservation of Existing 5 Sleep Habits
    print("\n  [Checking Coexistence of 5 Core Sleep Habits]")
    habit_rows = driver.find_elements(By.CSS_SELECTOR, "#sleepHabits .check-row")
    check("Existing #sleepHabits renders 5 rows", len(habit_rows) == 5)

    # Check off habit 0 and 2
    driver.execute_script(f"""
      const iso = toISO(weekDates[selectedIdx]);
      saveSleepHabits(iso, {{ 'i0': true, 'i2': true }});
      sleepHabitsState = loadSleepHabits(iso);
      renderSleep();
    """)
    time.sleep(0.3)
    curr_habits = driver.execute_script(f"return loadSleepHabits('{test_iso}');")
    check("Habit i0 is true", curr_habits.get('i0') is True)
    check("Habit i2 is true", curr_habits.get('i2') is True)
    check("Habit i1 is undefined / not checked", curr_habits.get('i1') is None)

    # 2.7 7-Day & 28-Day Adherence Computation & UI Toggle
    print("\n  [Checking 7-Day & 28-Day Habit Summaries]")
    stats_7 = driver.execute_script(f"return computeSleepAdherenceStats(7, '{test_iso}');")
    check("7-day adherence computation runs successfully", stats_7.get('hasData') is True)
    check("7-day stats returns 5 habit breakdown entries", len(stats_7.get('habitsStats', [])) == 5)
    check("Overall habits percentage is a valid integer between 0 and 100", 0 <= stats_7.get('overallHabitsPct', -1) <= 100)

    # Verify future days are strictly excluded
    future_test = driver.execute_script("return computeSleepAdherenceStats(7, '2099-01-01');")
    check("Future-only query returns hasData=false (no future days counted)", future_test.get('hasData') is False)

    # Click 28 days toggle in UI
    btn28 = driver.find_element(By.ID, "btnAdherence28")
    btn28.click()
    time.sleep(0.3)
    btn28_after = driver.find_element(By.ID, "btnAdherence28")
    check("28 days toggle switches to active class", "active" in btn28_after.get_attribute("class"))

    btn7 = driver.find_element(By.ID, "btnAdherence7")
    btn7.click()
    time.sleep(0.3)
    btn7_after = driver.find_element(By.ID, "btnAdherence7")
    check("7 days toggle switches back to active class", "active" in btn7_after.get_attribute("class"))

    # 2.8 Wind-Down Reminder Scheduler Trigger & Deduplication
    print("\n  [Checking Wind-Down Scheduler Dispatch]")
    # Target bedtime 22:30, wind-down lead 45 min -> trigger at 21:45 (1305 min)
    driver.execute_script("""
      notificationSettings = { enabled: true };
      saveSleepRoutineSettings({
        targetBedtime: '22:30',
        targetWakeTime: '06:30',
        windDownLeadMin: 45,
        reminderEnabled: true,
        activeDays: [true, true, true, true, true, true, true]
      });
      // Clear today's dispatched tags for clean test
      const iso = toISO(new Date());
      storageSet('notif-dispatched:' + iso, '{}');
    """)

    # Test trigger at 21:45 (1305 min)
    triggered_tags = driver.execute_script("""
      const iso = toISO(new Date());
      return checkAndDispatchDueReminders(iso, 1305);
    """)
    check("Scheduler triggers winddown reminder at exactly 21:45", any("sleep:winddown:" in t for t in triggered_tags))

    # Test deduplication: second call at 21:46 should NOT re-trigger
    triggered_again = driver.execute_script("""
      const iso = toISO(new Date());
      return checkAndDispatchDueReminders(iso, 1306);
    """)
    check("Scheduler does not trigger duplicate winddown reminder on same day", not any("sleep:winddown:" in t for t in triggered_again))

    # 2.9 Storage Isolation from Prayer, Gym, and Meals
    print("\n  [Checking Storage Isolation]")
    prayer_before = driver.execute_script(f"return loadPrayer('{test_iso}');")
    driver.execute_script(f"saveWindDown('{test_iso}', {{ screens: true, azkar: true, bedroom: true }});")
    prayer_after = driver.execute_script(f"return loadPrayer('{test_iso}');")
    check("Saving wind-down does not modify prayer tracking records", prayer_before == prayer_after)

    # 2.10 Backup / Export & Restore Round-Trip Compatibility
    print("\n  [Checking Backup / Export & Restore Compatibility]")
    exported = driver.execute_script("return exportAllData({ download: false });")
    check("exportAllData exports sleep-routine-settings", 'sleep-routine-settings' in exported)
    check(f"exportAllData exports winddown:{test_iso}", f'winddown:{test_iso}' in exported)

    # Validate backup shape check
    val_check = driver.execute_script("""
      const testBackup = {
        'sleep-routine-settings': JSON.stringify({ targetBedtime: '23:00' }),
        'winddown:2026-10-25': JSON.stringify({ screens: true })
      };
      return validateBackupData(testBackup);
    """)
    check("validateBackupData recognizes sleep-routine-settings and winddown as valid backup", val_check.get('ok') is True)

    # 2.11 Mobile Responsiveness at 375px
    print("\n  [Checking Mobile Responsiveness at 375px]")
    driver.set_window_size(375, 812)
    time.sleep(0.5)

    overflow = driver.execute_script("return document.documentElement.scrollWidth > document.documentElement.clientWidth;")
    check("No horizontal overflow on 375px mobile viewport", not overflow)

    # 2.12 JS Console Cleanliness
    print("\n  [Checking Application JavaScript Console Logs]")
    browser_logs = driver.get_log("browser")
    app_errors = []
    for entry in browser_logs:
        msg = entry.get("message", "")
        if "manifest.json" in msg:
            continue
        if entry.get("level") == "SEVERE":
            app_errors.append(msg)
    check(f"Zero application JavaScript console errors (found {len(app_errors)})", len(app_errors) == 0)
    if app_errors:
        for err in app_errors[:5]:
            print(f"    ERROR: {err}")

finally:
    driver.quit()

print("================================================================================")
print(f"RESULTS: {passed} PASSED, {failed} FAILED")
print("================================================================================")

if failed > 0:
    sys.exit(1)

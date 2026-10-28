# -*- coding: utf-8 -*-
"""
Phase C2 / Proposal #6: Habit Streaks Engine & Tracker Acceptance Test
Validates:
1. Static code analysis:
   - shiftIsoDay handles date shifting correctly across month/year boundaries.
   - computeHabitStreaks evaluates 6 core wellness habits (prayer, quran, azkar, sleep, water, schedule).
   - CSS rules .streak-pill and .streak-mini-card are defined with interactive states.
   - HTML includes #homeStreaksCard in homeView and #domainStreaks in overviewView.
   - renderHomeStreaks and renderDomainStreaks are defined and integrated into render pipelines.
2. Headless Chrome runtime verification:
   - Home view loads cleanly with zero JS console runtime errors.
   - #homeStreaksCard renders all 6 habit pills.
   - Dynamic streak calculation works accurately with mock consecutive history.
   - Clicking streak pill navigates cleanly to target mode.
   - Overview view displays #domainStreaks with 6 mini cards, fire emojis, and personal best records.
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
print("PHASE C2 ACCEPTANCE TEST: HABIT STREAKS ENGINE & TRACKER")
print("================================================================================")

# --- SECTION 1: Static Code Invariants ---
print("\n--- 1. Static Code Analysis ---")
with open(INDEX_PATH, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

check("shiftIsoDay is defined", "function shiftIsoDay(" in content)
check("computeHabitStreaks is defined", "function computeHabitStreaks(" in content)
check("renderDomainStreaks is defined", "function renderDomainStreaks(" in content)
check("renderHomeStreaks is defined", "function renderHomeStreaks(" in content)

check(".streak-pill CSS rule is defined", ".streak-pill{" in content)
check(".streak-mini-card CSS rule is defined", ".streak-mini-card{" in content)

check("HTML includes #homeStreaksCard in homeView", 'id="homeStreaksCard"' in content)
check("HTML includes #domainStreaks in overviewView", 'id="domainStreaks"' in content)

check("computeHabitStreaks evaluates prayer habit", "id: 'prayer'" in content)
check("computeHabitStreaks evaluates quran habit", "id: 'quran'" in content)
check("computeHabitStreaks evaluates azkar habit", "id: 'azkar'" in content)
check("computeHabitStreaks evaluates sleep habit", "id: 'sleep'" in content)
check("computeHabitStreaks evaluates water habit", "id: 'water'" in content)
check("computeHabitStreaks evaluates schedule habit", "id: 'schedule'" in content)

# --- SECTION 2: Headless Browser Runtime Verification ---
print("\n--- 2. Headless Chrome Browser Verification ---")

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
    time.sleep(1.0)

    # 2.1 Verify zero console errors
    logs = driver.get_log("browser")
    js_errors = [l for l in logs if l["level"] == "SEVERE" and "manifest" not in l["message"]]
    check("Zero SEVERE browser console runtime errors", len(js_errors) == 0)

    # 2.2 Shift date math test inside browser environment
    shift_test = driver.execute_script("""
        const t1 = shiftIsoDay('2026-03-01', -1); // leap/non-leap Feb transition
        const t2 = shiftIsoDay('2026-01-01', -1); // year transition
        const t3 = shiftIsoDay('2026-10-27', 3);
        return { t1, t2, t3 };
    """)
    check("shiftIsoDay('2026-03-01', -1) == '2026-02-28'", shift_test['t1'] == '2026-02-28')
    check("shiftIsoDay('2026-01-01', -1) == '2025-12-31'", shift_test['t2'] == '2025-12-31')
    check("shiftIsoDay('2026-10-27', 3) == '2026-10-30'", shift_test['t3'] == '2026-10-30')

    # 2.3 Verify home view renders #homeStreaksCard
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('home');")
    time.sleep(0.5)

    home_card = driver.find_element(By.ID, "homeStreaksCard")
    check("#homeStreaksCard is displayed in Home view", home_card.is_displayed())

    pills = home_card.find_elements(By.CSS_SELECTOR, ".streak-pill")
    check("#homeStreaksCard renders 6 habit pills", len(pills) == 6)

    # 2.4 Seed mock consecutive prayer data and verify streak calculation
    driver.execute_script("""
        const today = toISO(new Date());
        const d1 = shiftIsoDay(today, -1);
        const d2 = shiftIsoDay(today, -2);
        const fullPrayer = {
            fajr: { fard: true },
            dhuhr: { fard: true },
            asr: { fard: true },
            maghrib: { fard: true },
            isha: { fard: true }
        };
        // 3 consecutive days: today, yesterday, 2 days ago
        savePrayer(today, fullPrayer);
        savePrayer(d1, fullPrayer);
        savePrayer(d2, fullPrayer);

        // Re-render home
        renderHomeDashboard();
    """)
    time.sleep(0.5)

    prayer_streak_text = driver.find_element(By.CSS_SELECTOR, "#homeStreaksCard .streak-pill[data-nav='prayer']").text
    check("Prayer streak pill reflects 3 days (🔥 3)", "🔥 3" in prayer_streak_text)

    # 2.5 Test streak pill click navigation
    prayer_pill = driver.find_element(By.CSS_SELECTOR, "#homeStreaksCard .streak-pill[data-nav='prayer']")
    prayer_pill.click()
    time.sleep(0.5)

    prayer_view = driver.find_element(By.ID, "prayerView")
    check("Clicking prayer streak pill navigates to prayerView", "hidden" not in prayer_view.get_attribute("class"))

    # 2.6 Test Overview View renders #domainStreaks with 6 mini cards
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('overview');")
    time.sleep(0.5)

    domain_streaks = driver.find_element(By.ID, "domainStreaks")
    check("#domainStreaks is displayed in Overview view", domain_streaks.is_displayed())

    mini_cards = domain_streaks.find_elements(By.CSS_SELECTOR, ".streak-mini-card")
    check("#domainStreaks renders 6 mini cards", len(mini_cards) == 6)

    overview_prayer_card = mini_cards[0].text
    check("Overview prayer card reflects '🔥 3 يوم'", "🔥 3 يوم" in overview_prayer_card)
    check("Overview prayer card shows personal best trophy", "🏆 أفضل:" in overview_prayer_card)

finally:
    driver.quit()

print("\n================================================================================")
print(f"RESULTS: {passed} passed, {failed} failed")
print("================================================================================")

if failed > 0:
    sys.exit(1)

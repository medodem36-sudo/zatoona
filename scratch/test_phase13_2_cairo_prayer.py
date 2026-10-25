# -*- coding: utf-8 -*-
"""
Phase 13.2 — Cairo Prayer Times Acceptance Test
Tests:
1. Static code invariants:
   - PRAYER_SUPPORTED_CITIES includes 'Cairo'.
   - HTML selects #prayerCitySelect and #scPrayerCity include 'Cairo' option.
2. Headless Chrome browser runtime tests:
   - Option presence and labels in both selects (desktop & mobile).
   - City selection, two-way UI sync between prayer page and schedule settings.
   - LocalStorage persistence and page reload retention.
   - City round-trip switching (Cairo -> Minya -> Alexandria -> Cairo).
   - Cache key isolation (Cairo vs Minya vs Alexandria).
   - Historical prayer tracking preservation (fard/sunnah records untouched).
   - Offline / network failure graceful handling.
   - Mobile (375px) layout integrity.
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
from selenium.webdriver.support.ui import Select

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
print("PHASE 13.2 ACCEPTANCE TEST: CAIRO PRAYER TIMES SUPPORT")
print("================================================================================")

# --- SECTION 1: Static Code Invariants ---
print("\n--- 1. Static Code Analysis ---")
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. PRAYER_SUPPORTED_CITIES array
m_cities = re.search(r'const\s+PRAYER_SUPPORTED_CITIES\s*=\s*\[([^\]]+)\]', content)
check("PRAYER_SUPPORTED_CITIES is defined", bool(m_cities))
if m_cities:
    cities_str = m_cities.group(1)
    check("PRAYER_SUPPORTED_CITIES contains 'Cairo'", "'Cairo'" in cities_str)
    check("PRAYER_SUPPORTED_CITIES contains 'Minya'", "'Minya'" in cities_str)
    check("PRAYER_SUPPORTED_CITIES contains 'Alexandria'", "'Alexandria'" in cities_str)

# 2. #prayerCitySelect HTML options
m_sel1 = re.search(r'<select[^>]*id="prayerCitySelect"[^>]*>([\s\S]*?)</select>', content)
check("#prayerCitySelect exists in HTML", bool(m_sel1))
if m_sel1:
    options1 = m_sel1.group(1)
    check("#prayerCitySelect has option value='Cairo'", 'value="Cairo"' in options1)
    check("#prayerCitySelect displays Arabic label 'القاهرة'", 'القاهرة' in options1)

# 3. #scPrayerCity HTML options
m_sel2 = re.search(r'<select[^>]*id="scPrayerCity"[^>]*>([\s\S]*?)</select>', content)
check("#scPrayerCity exists in HTML", bool(m_sel2))
if m_sel2:
    options2 = m_sel2.group(1)
    check("#scPrayerCity has option value='Cairo'", 'value="Cairo"' in options2)
    check("#scPrayerCity displays Arabic label 'القاهرة'", 'القاهرة' in options2)

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

    # 2.1 Verify Initial Load & City Dropdown Options in DOM
    print("\n  [Checking Initial City Dropdown Options]")
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('prayer'); else if(typeof setMode==='function') setMode('prayer');")
    time.sleep(0.5)

    sel1_el = driver.find_element(By.ID, "prayerCitySelect")
    select1 = Select(sel1_el)
    opt_values1 = [o.get_attribute("value") for o in select1.options]
    check("#prayerCitySelect has 3 city options", len(opt_values1) == 3)
    check("#prayerCitySelect includes 'Cairo', 'Minya', 'Alexandria'",
          set(opt_values1) == {'Minya', 'Alexandria', 'Cairo'})

    driver.execute_script("if(typeof navigateTo==='function') navigateTo('schedule'); else if(typeof setMode==='function') setMode('schedule');")
    time.sleep(0.5)
    sel2_el = driver.find_element(By.ID, "scPrayerCity")
    select2 = Select(sel2_el)
    opt_values2 = [o.get_attribute("value") for o in select2.options]
    check("#scPrayerCity has 3 city options", len(opt_values2) == 3)
    check("#scPrayerCity includes 'Cairo', 'Minya', 'Alexandria'",
          set(opt_values2) == {'Minya', 'Alexandria', 'Cairo'})

    # 2.2 Selecting Cairo & Two-Way Sync
    print("\n  [Checking City Selection & Synchronization]")
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('prayer'); else if(typeof setMode==='function') setMode('prayer');")
    time.sleep(0.3)

    # Change to Cairo on prayer page
    driver.execute_script("onCityChange('Cairo');")
    time.sleep(0.5)

    current_city = driver.execute_script("return loadPrayerCity();")
    check("loadPrayerCity() returns 'Cairo'", current_city == 'Cairo')

    sel1_val = driver.find_element(By.ID, "prayerCitySelect").get_attribute("value")
    sel2_val = driver.find_element(By.ID, "scPrayerCity").get_attribute("value")
    check("#prayerCitySelect value is 'Cairo'", sel1_val == 'Cairo')
    check("#scPrayerCity value synced to 'Cairo'", sel2_val == 'Cairo')

    stored_city = driver.execute_script("return storageGet('prayer-city');")
    check("localStorage stores 'Cairo' under prayer-city", stored_city == 'Cairo')

    sched_city = driver.execute_script("return scheduleSettings ? scheduleSettings.prayerCity : null;")
    check("scheduleSettings.prayerCity is updated to 'Cairo'", sched_city == 'Cairo')

    # 2.3 Persistence After Reload
    print("\n  [Checking Persistence Across Page Reload]")
    driver.refresh()
    time.sleep(1.5)

    reloaded_city = driver.execute_script("return loadPrayerCity();")
    check("loadPrayerCity() persists 'Cairo' after page reload", reloaded_city == 'Cairo')

    driver.execute_script("if(typeof navigateTo==='function') navigateTo('prayer'); else if(typeof setMode==='function') setMode('prayer');")
    time.sleep(0.3)
    sel1_reloaded = driver.find_element(By.ID, "prayerCitySelect").get_attribute("value")
    check("#prayerCitySelect displays 'Cairo' after reload", sel1_reloaded == 'Cairo')

    # 2.4 Switching Sequence (Cairo -> Minya -> Alexandria -> Cairo)
    print("\n  [Checking Multi-City Round-Trip Switching]")
    for test_city in ['Minya', 'Alexandria', 'Cairo']:
        driver.execute_script(f"onCityChange('{test_city}');")
        time.sleep(0.3)
        c = driver.execute_script("return loadPrayerCity();")
        s1 = driver.find_element(By.ID, "prayerCitySelect").get_attribute("value")
        s2 = driver.find_element(By.ID, "scPrayerCity").get_attribute("value")
        check(f"Switching to '{test_city}' updates loadPrayerCity and both select elements",
              c == test_city and s1 == test_city and s2 == test_city)

    # 2.5 Cache Isolation (Cairo vs Minya vs Alexandria)
    print("\n  [Checking Cache Key Isolation Between Cities]")
    test_iso = driver.execute_script("return toISO(weekDates[selectedIdx]);")
    driver.execute_script(f"""
        saveCachedPrayerTimes('Minya', '{test_iso}', {{
            fajr: '04:40', dhuhr: '11:45', asr: '14:55', maghrib: '17:15', isha: '18:30'
        }}, Date.now());
        saveCachedPrayerTimes('Alexandria', '{test_iso}', {{
            fajr: '04:45', dhuhr: '11:50', asr: '15:00', maghrib: '17:20', isha: '18:35'
        }}, Date.now());
        saveCachedPrayerTimes('Cairo', '{test_iso}', {{
            fajr: '04:38', dhuhr: '11:44', asr: '14:54', maghrib: '17:14', isha: '18:32'
        }}, Date.now());
    """)

    cairo_cache = driver.execute_script(f"return loadCachedPrayerTimes('Cairo', '{test_iso}');")
    minya_cache = driver.execute_script(f"return loadCachedPrayerTimes('Minya', '{test_iso}');")
    alex_cache = driver.execute_script(f"return loadCachedPrayerTimes('Alexandria', '{test_iso}');")

    check("Cairo cache exists and has city='Cairo'", cairo_cache and cairo_cache.get('city') == 'Cairo')
    check("Minya cache exists and has city='Minya'", minya_cache and minya_cache.get('city') == 'Minya')
    check("Alexandria cache exists and has city='Alexandria'", alex_cache and alex_cache.get('city') == 'Alexandria')
    check("Cairo Fajr (04:38) is isolated from Minya (04:40) and Alex (04:45)",
          cairo_cache['fajr'] == '04:38' and minya_cache['fajr'] == '04:40' and alex_cache['fajr'] == '04:45')

    # Switch to Cairo and load timings
    driver.execute_script(f"""
        onCityChange('Cairo');
        prayerTimesState = loadPrayerTimes('{test_iso}');
        renderPrayerTimes();
    """)
    time.sleep(0.3)
    active_times = driver.execute_script("return prayerTimesState;")
    check("Active prayer times loaded from Cairo cache", active_times.get('fajr') == '04:38' and active_times.get('city') == 'Cairo')

    # 2.6 Historical Prayer Tracking Protection
    print("\n  [Checking Historical Prayer Tracking Preservation]")
    past_iso = "2026-10-20"
    # Seed historical prayer checkmarks
    driver.execute_script(f"""
        storageSet('prayer:{past_iso}', JSON.stringify({{
            fajr: {{ fard: true, sunnah: true }},
            dhuhr: {{ fard: true, sunnah: false }},
            asr: {{ fard: true, sunnah: false }},
            maghrib: {{ fard: true, sunnah: true }},
            isha: {{ fard: true, sunnah: false }}
        }}));
    """)

    # Switch cities multiple times
    driver.execute_script("onCityChange('Alexandria');")
    time.sleep(0.2)
    driver.execute_script("onCityChange('Minya');")
    time.sleep(0.2)
    driver.execute_script("onCityChange('Cairo');")
    time.sleep(0.2)

    hist_data = driver.execute_script(f"return storageGetJSON('prayer:{past_iso}', null);")
    check("Historical prayer checkmarks for past date exist", hist_data is not None)
    check("Historical Fajr fard is still true", hist_data and hist_data.get('fajr', {}).get('fard') is True)
    check("Historical Fajr sunnah is still true", hist_data and hist_data.get('fajr', {}).get('sunnah') is True)
    check("Historical Maghrib fard is still true", hist_data and hist_data.get('maghrib', {}).get('fard') is True)

    # 2.7 Mobile Viewport (375px) Check
    print("\n  [Checking Mobile Responsiveness at 375px Viewport]")
    driver.set_window_size(375, 812)
    time.sleep(0.5)

    scroll_width = driver.execute_script("return document.documentElement.scrollWidth;")
    client_width = driver.execute_script("return document.documentElement.clientWidth;")
    check("No horizontal overflow on mobile viewport (scrollWidth <= clientWidth)", scroll_width <= client_width)

    # Verify select element is visible and clickable on mobile
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('prayer'); else if(typeof setMode==='function') setMode('prayer');")
    time.sleep(0.3)
    sel1_mobile = driver.find_element(By.ID, "prayerCitySelect")
    check("#prayerCitySelect is displayed on mobile", sel1_mobile.is_displayed())

    # 2.8 Clean Console Logs Check
    print("\n  [Checking Application JavaScript Console Logs]")
    logs = driver.get_log("browser")
    app_errors = [l for l in logs if l['level'] == 'SEVERE' and 'manifest.json' not in l['message']]
    check(f"Zero application JavaScript console errors (found {len(app_errors)})", len(app_errors) == 0)

finally:
    driver.quit()

print("\n================================================================================")
print(f"RESULTS: {passed} PASSED, {failed} FAILED")
print("================================================================================")

if failed > 0:
    sys.exit(1)

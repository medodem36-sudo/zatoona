# -*- coding: utf-8 -*-
"""
Phase 13.1 — Checklist & Worship Labels Repair Acceptance Test
Tests:
1. Static code analysis: renderSimpleChecklist and renderScheduleChecklist include .check-left and .cname.
2. Headless Chrome Browser verification:
   - Worship section: qiyamWitr, nawafilExtra, azkar, quranWird render descriptive Arabic labels.
   - Sleep section: sleepHabits renders all 5 descriptive Arabic labels.
   - Schedule section: scheduleChecklist renders icons and descriptive task labels.
   - Interaction & Persistence: clicking toggles button state and persists to correct localStorage keys.
   - Mobile & Desktop responsiveness: layout integrity, alignment, and zero JavaScript errors.
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
print("PHASE 13.1 ACCEPTANCE TEST: CHECKLIST & WORSHIP LABELS REPAIR")
print("================================================================================")

# --- SECTION 1: Static Code Invariants ---
print("\n--- 1. Static Code Analysis ---")
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Check renderSimpleChecklist
m1 = re.search(r'function\s+renderSimpleChecklist\s*\([^{]*\{([\s\S]*?)\n\}', content)
check("renderSimpleChecklist function is defined", bool(m1))
if m1:
    body1 = m1.group(1)
    check("renderSimpleChecklist includes .check-left container", 'check-left' in body1)
    check("renderSimpleChecklist includes .cname label container", 'cname' in body1)
    check("renderSimpleChecklist escapes HTML labels safely", 'escapeHtml' in body1)
    check("renderSimpleChecklist preserves toggle-group button with data-key", 'data-key' in body1 and 'toggle-group' in body1)
    check("renderSimpleChecklist supports accessible aria-label", 'aria-label' in body1)
    check("renderSimpleChecklist supports whole-row clickability", 'row.style.cursor' in body1)

# Check renderScheduleChecklist
m2 = re.search(r'function\s+renderScheduleChecklist\s*\([^{]*\{([\s\S]*?)\n\}', content)
check("renderScheduleChecklist function is defined", bool(m2))
if m2:
    body2 = m2.group(1)
    check("renderScheduleChecklist includes .check-left container", 'check-left' in body2)
    check("renderScheduleChecklist includes .cname label container", 'cname' in body2)
    check("renderScheduleChecklist includes icon container or span", 'icon' in body2)
    check("renderScheduleChecklist escapes label safely", 'escapeHtml' in body2)
    check("renderScheduleChecklist preserves toggle-group button with data-key", 'data-key' in body2 and 'toggle-group' in body2)
    check("renderScheduleChecklist supports accessible aria-label", 'aria-label' in body2)
    check("renderScheduleChecklist supports whole-row clickability", 'row.style.cursor' in body2)

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
    time.sleep(1.5)

    # 2.1 Check Prayer & Worship Section
    print("\n  [Checking Worship Section]")
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('prayer'); else if(typeof setMode==='function') setMode('prayer');")
    time.sleep(0.5)

    # qiyamWitr
    qiyam_rows = driver.find_elements(By.CSS_SELECTOR, "#qiyamWitr .check-row")
    check("qiyamWitr has 2 rows rendered", len(qiyam_rows) == 2)
    if len(qiyam_rows) >= 2:
        text0 = qiyam_rows[0].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        text1 = qiyam_rows[1].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        check("qiyamWitr row 0 label is 'قيام الليل'", "قيام الليل" in text0)
        check("qiyamWitr row 1 label is 'الوتر'", "الوتر" in text1)

    # nawafilExtra
    nawafil_rows = driver.find_elements(By.CSS_SELECTOR, "#nawafilExtra .check-row")
    check("nawafilExtra has 3 rows rendered", len(nawafil_rows) == 3)
    if len(nawafil_rows) >= 3:
        n0 = nawafil_rows[0].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        n1 = nawafil_rows[1].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        n2 = nawafil_rows[2].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        check("nawafilExtra row 0 label is 'صلاة الضحى'", "صلاة الضحى" in n0)
        check("nawafilExtra row 1 label is 'تحية المسجد'", "تحية المسجد" in n1)
        check("nawafilExtra row 2 label is 'سنة الوضوء'", "سنة الوضوء" in n2)

    # azkar
    azkar_rows = driver.find_elements(By.CSS_SELECTOR, "#azkar .check-row")
    check("azkar has 2 rows rendered", len(azkar_rows) == 2)
    if len(azkar_rows) >= 2:
        az0 = azkar_rows[0].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        az1 = azkar_rows[1].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        check("azkar row 0 label is 'أذكار الصباح'", "أذكار الصباح" in az0)
        check("azkar row 1 label is 'أذكار المساء'", "أذكار المساء" in az1)

    # quranWird
    quran_rows = driver.find_elements(By.CSS_SELECTOR, "#quranWird .check-row")
    check("quranWird has 4 rows rendered", len(quran_rows) == 4)
    if len(quran_rows) >= 4:
        q0 = quran_rows[0].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        q1 = quran_rows[1].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        q2 = quran_rows[2].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        q3 = quran_rows[3].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        check("quranWird row 0 label includes 'سماع'", "سماع" in q0)
        check("quranWird row 1 label includes 'قراءة'", "قراءة" in q1)
        check("quranWird row 2 label includes 'حفظ آيتين'", "حفظ آيتين" in q2)
        check("quranWird row 3 label includes 'مراجعة'", "مراجعة" in q3)

    # 2.2 Check Sleep Habits Section
    print("\n  [Checking Sleep Habits Section]")
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('sleep'); else if(typeof setMode==='function') setMode('sleep');")
    time.sleep(0.5)

    sleep_rows = driver.find_elements(By.CSS_SELECTOR, "#sleepHabits .check-row")
    check("sleepHabits has 5 rows rendered", len(sleep_rows) == 5)
    if len(sleep_rows) >= 5:
        s0 = sleep_rows[0].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        s1 = sleep_rows[1].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        s2 = sleep_rows[2].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        s3 = sleep_rows[3].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        s4 = sleep_rows[4].find_element(By.CSS_SELECTOR, ".cname").text.strip()
        check("sleepHabits row 0 label has text", len(s0) > 10 and "معاد" in s0)
        check("sleepHabits row 1 label has text", len(s1) > 10 and "الشاشات" in s1)
        check("sleepHabits row 2 label has text", len(s2) > 10 and "كافيين" in s2)
        check("sleepHabits row 3 label has text", len(s3) > 10 and "تمرين" in s3)
        check("sleepHabits row 4 label has text", len(s4) > 10 and "مظلمة" in s4)

    # 2.3 Check Schedule Checklist Section
    print("\n  [Checking Daily Schedule Checklist Section]")
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('schedule'); else if(typeof setMode==='function') setMode('schedule');")
    time.sleep(0.5)

    sched_rows = driver.find_elements(By.CSS_SELECTOR, "#scheduleChecklist .check-row")
    check("scheduleChecklist has >= 15 rows rendered", len(sched_rows) >= 15)
    if len(sched_rows) >= 5:
        row0_cname = sched_rows[0].find_element(By.CSS_SELECTOR, ".cname")
        check("First schedule item has visible icon and label", len(row0_cname.text.strip()) > 3)
        # Check that multiple tasks have recognizable labels
        labels_text = " ".join([r.find_element(By.CSS_SELECTOR, ".cname").text for r in sched_rows])
        check("Schedule checklist includes 'الاستيقاظ'", "الاستيقاظ" in labels_text)
        check("Schedule checklist includes 'الفجر'", "الفجر" in labels_text)
        check("Schedule checklist includes 'الفطار'", "الفطار" in labels_text)

    # 2.4 Interaction & Persistence Check
    print("\n  [Checking Click Interaction & LocalStorage Persistence]")
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('prayer'); else if(typeof setMode==='function') setMode('prayer');")
    time.sleep(0.5)

    # Click qiyam row 0
    qiyam_row0 = driver.find_element(By.CSS_SELECTOR, "#qiyamWitr .check-row:first-child")
    btn0 = qiyam_row0.find_element(By.CSS_SELECTOR, ".tbtn")
    was_on = "on-right" in btn0.get_attribute("class")

    # Click on the label text
    qiyam_row0.find_element(By.CSS_SELECTOR, ".cname").click()
    time.sleep(0.3)

    qiyam_row0_after = driver.find_element(By.CSS_SELECTOR, "#qiyamWitr .check-row:first-child")
    btn0_after = qiyam_row0_after.find_element(By.CSS_SELECTOR, ".tbtn")
    is_on_now = "on-right" in btn0_after.get_attribute("class")
    check("Clicking row text toggles button state", is_on_now != was_on)

    # Verify localStorage via storageGet
    iso_date = driver.execute_script("return toISO(weekDates[selectedIdx]);")
    qiyam_stored = driver.execute_script(f"return storageGet('qiyam:' + '{iso_date}');")
    check("qiyam state persisted to localStorage under qiyam:YYYY-MM-DD", qiyam_stored is not None)
    if qiyam_stored:
        data = json.loads(qiyam_stored)
        check("qiyam stored data has key 'i0'", "i0" in data)

    # Toggle it back to keep state clean
    qiyam_row0_after.click()
    time.sleep(0.3)

    # 2.5 Mobile Responsiveness Check (375px Viewport)
    print("\n  [Checking Mobile Layout at 375px Viewport]")
    driver.set_window_size(375, 812)
    time.sleep(0.5)

    scroll_width = driver.execute_script("return document.documentElement.scrollWidth;")
    client_width = driver.execute_script("return document.documentElement.clientWidth;")
    check("No horizontal overflow on mobile viewport (scrollWidth <= clientWidth)", scroll_width <= client_width)

    # Ensure buttons and labels do not overlap
    row_el = driver.find_element(By.CSS_SELECTOR, "#qiyamWitr .check-row:first-child")
    cname_el = row_el.find_element(By.CSS_SELECTOR, ".cname")
    tbtn_el = row_el.find_element(By.CSS_SELECTOR, ".tbtn")
    cname_rect = cname_el.rect
    tbtn_rect = tbtn_el.rect
    check("Label and toggle button are cleanly separated in flex layout", cname_rect['x'] != tbtn_rect['x'])

    # 2.6 Application JavaScript Error Check
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

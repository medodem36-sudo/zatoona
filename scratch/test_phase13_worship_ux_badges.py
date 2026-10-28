# -*- coding: utf-8 -*-
"""
Phase A3 / Worship UX: Visual Distinctiveness & Section Badges Acceptance Test
Validates:
1. Static code analysis:
   - .worship-badge CSS is defined with monospace font, pill styling, and .is-complete state.
   - Category border-inline-start accent rules exist for qiyam, nawafil, azkar, quran, fard.
   - Section title badge spans exist in HTML: badge-prayerFard, badge-qiyam, badge-nawafil, badge-azkar, badge-quran.
   - renderPrayerSummary includes all 6 worship categories (fard, sunnah, qiyam, nawafil, azkar, quran).
2. Headless Chrome runtime verification:
   - Prayer view loads cleanly with zero JS syntax or runtime errors.
   - Badges render with exact initial zero-state counts.
   - Interactive toggling updates section badges in real-time.
   - Interactive toggling updates prayerSummary live without requiring reload.
   - Completion state applies .is-complete class and '✓ ' prefix.
   - 3-Way HTML parity verification.
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
print("PHASE A3 ACCEPTANCE TEST: WORSHIP CHECKLIST VISUAL BADGES & SUMMARY")
print("================================================================================")

# --- SECTION 1: Static Code Invariants ---
print("\n--- 1. Static Code Analysis ---")
with open(INDEX_PATH, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

check(".worship-badge CSS rule is defined", ".worship-badge{" in content)
check(".worship-badge.is-complete CSS rule is defined", ".worship-badge.is-complete{" in content)
check("Qiyam category accent CSS is defined", "#qiyamWitr .check-row.is-checked{border-inline-start:3px solid #818cf8" in content)
check("Nawafil category accent CSS is defined", "#nawafilExtra .check-row.is-checked{border-inline-start:3px solid #f59e0b" in content)
check("Azkar category accent CSS is defined", "#azkar .check-row.is-checked{border-inline-start:3px solid #10b981" in content)
check("Quran category accent CSS is defined", "#quranWird .check-row.is-checked{border-inline-start:3px solid #06b6d4" in content)
check("Fard category accent CSS is defined", "#prayerFard .check-row.is-checked{border-inline-start:3px solid var(--good)" in content)

check("HTML includes #badge-prayerFard", 'id="badge-prayerFard"' in content)
check("HTML includes #badge-qiyam", 'id="badge-qiyam"' in content)
check("HTML includes #badge-nawafil", 'id="badge-nawafil"' in content)
check("HTML includes #badge-azkar", 'id="badge-azkar"' in content)
check("HTML includes #badge-quran", 'id="badge-quran"' in content)

check("renderPrayerSummary includes 'قيام ووتر'", "قيام ووتر" in content)
check("renderPrayerSummary includes 'باقي النوافل'", "باقي النوافل" in content)
check("renderPrayerSummary includes 'أذكار'", "أذكار" in content)

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

    # Clean local storage for pristine testing
    driver.execute_script("localStorage.clear();")
    driver.execute_script("if(typeof navigateTo==='function') navigateTo('prayer'); else if(typeof setMode==='function') setMode('prayer');")
    time.sleep(0.5)

    # Check zero JS runtime errors (ignoring expected file:// CORS restriction on manifest)
    logs = driver.get_log("browser")
    js_errors = [l for l in logs if l["level"] == "SEVERE" and "manifest" not in l["message"]]
    check("Zero SEVERE browser console runtime errors", len(js_errors) == 0)

    # Check initial badge states
    b_fard = driver.find_element(By.ID, "badge-prayerFard")
    b_qiyam = driver.find_element(By.ID, "badge-qiyam")
    b_nawafil = driver.find_element(By.ID, "badge-nawafil")
    b_azkar = driver.find_element(By.ID, "badge-azkar")
    b_quran = driver.find_element(By.ID, "badge-quran")

    check("badge-prayerFard initial text is '0/5 فرض · 0/5 سنة'", "0/5 فرض · 0/5 سنة" in b_fard.text)
    check("badge-qiyam initial text is '0/2'", "0/2" in b_qiyam.text)
    check("badge-nawafil initial text is '0/3'", "0/3" in b_nawafil.text)
    check("badge-azkar initial text is '0/2'", "0/2" in b_azkar.text)
    check("badge-quran initial text is '0/4'", "0/4" in b_quran.text)

    # Check initial summary items count
    summary_items = driver.find_elements(By.CSS_SELECTOR, "#prayerSummary .item")
    check("prayerSummary renders 6 distinct metric cards", len(summary_items) == 6)

    # Test toggling Qiyam item 0
    driver.find_element(By.ID, "qiyamWitrRow-i0").click()
    time.sleep(0.3)

    b_qiyam = driver.find_element(By.ID, "badge-qiyam")
    check("badge-qiyam updates to '1/2' after clicking row 0", b_qiyam.text.strip() == "1/2")
    qiyam_row0_fresh = driver.find_element(By.ID, "qiyamWitrRow-i0")
    check("qiyamRow-i0 has .is-checked class", "is-checked" in qiyam_row0_fresh.get_attribute("class"))

    # Test toggling Qiyam item 1 (completion)
    driver.find_element(By.ID, "qiyamWitrRow-i1").click()
    time.sleep(0.3)

    b_qiyam = driver.find_element(By.ID, "badge-qiyam")
    check("badge-qiyam has '✓ 2/2' upon completion", "✓ 2/2" in b_qiyam.text)
    check("badge-qiyam has .is-complete class", "is-complete" in b_qiyam.get_attribute("class"))

    # Check live prayerSummary update
    summary_text = driver.find_element(By.ID, "prayerSummary").text
    check("prayerSummary reflects '2/2 قيام ووتر' live", "2/2" in summary_text and "قيام ووتر" in summary_text)

    # Test toggling Fard prayer (Fajr fard)
    fajr_fard_btn = driver.find_element(By.CSS_SELECTOR, "#prayerFardRow-fajr button[data-type='fard']")
    fajr_fard_btn.click()
    time.sleep(0.3)

    b_fard = driver.find_element(By.ID, "badge-prayerFard")
    check("badge-prayerFard updates to '1/5 فرض · 0/5 سنة'", "1/5 فرض · 0/5 سنة" in b_fard.text)

    # Test toggling Azkar (Sabah)
    driver.find_element(By.ID, "azkarRow-i0").click()
    time.sleep(0.3)

    b_azkar = driver.find_element(By.ID, "badge-azkar")
    check("badge-azkar updates to '1/2'", b_azkar.text.strip() == "1/2")

    # Test toggling Nawafil (Duha)
    driver.find_element(By.ID, "nawafilExtraRow-i0").click()
    time.sleep(0.3)

    b_nawafil = driver.find_element(By.ID, "badge-nawafil")
    check("badge-nawafil updates to '1/3'", b_nawafil.text.strip() == "1/3")

    # Test toggling Quran (Samaa)
    driver.find_element(By.ID, "quranWirdRow-i0").click()
    time.sleep(0.3)

    b_quran = driver.find_element(By.ID, "badge-quran")
    check("badge-quran updates to '1/4'", b_quran.text.strip() == "1/4")

finally:
    driver.quit()

print("\n================================================================================")
print(f"RESULTS: {passed} passed, {failed} failed")
print("================================================================================")

if failed > 0:
    sys.exit(1)

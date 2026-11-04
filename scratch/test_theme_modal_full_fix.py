import sys
sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=400,800')
driver = webdriver.Chrome(options=opts)

errors = []

try:
    driver.get('file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')
    time.sleep(1)

    print("--- 1. Testing Open Theme Customizer Modal ---")
    btn_open = driver.find_element(By.ID, 'btnOpenThemeModal')
    btn_open.click()
    time.sleep(0.3)
    
    overlay = driver.find_element(By.ID, 'themeModalOverlay')
    is_open = 'open' in overlay.get_attribute('class')
    print("Modal is open:", is_open)
    if not is_open:
        errors.append("Modal failed to open after clicking btnOpenThemeModal")

    print("--- 2. Testing Accent Color Change ('ocean' / أزرق) ---")
    ocean_btn = driver.find_element(By.CSS_SELECTOR, "[data-accent-choice='ocean']")
    ocean_btn.click()
    time.sleep(0.3)
    
    current_accent = driver.execute_script("return document.documentElement.getAttribute('data-accent');")
    is_ocean_active = 'active' in ocean_btn.get_attribute('class')
    print(f"Current accent: {current_accent}, Button active: {is_ocean_active}")
    if current_accent != 'ocean' or not is_ocean_active:
        errors.append(f"Accent change failed: current_accent={current_accent}, active={is_ocean_active}")

    print("--- 3. Testing Theme Change ('amoled') ---")
    amoled_btn = driver.find_element(By.CSS_SELECTOR, "[data-theme-choice='amoled']")
    amoled_btn.click()
    time.sleep(0.3)
    
    current_theme = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
    is_amoled_active = 'active' in amoled_btn.get_attribute('class')
    print(f"Current theme: {current_theme}, Button active: {is_amoled_active}")
    if current_theme != 'amoled' or not is_amoled_active:
        errors.append(f"Theme change failed: current_theme={current_theme}, active={is_amoled_active}")

    print("--- 4. Testing Font Scale Change ('large') ---")
    font_large_btn = driver.find_element(By.CSS_SELECTOR, "[data-font-choice='large']")
    font_large_btn.click()
    time.sleep(0.3)
    
    current_font = driver.execute_script("return document.documentElement.getAttribute('data-font-size');")
    is_font_active = 'active' in font_large_btn.get_attribute('class')
    print(f"Current font: {current_font}, Button active: {is_font_active}")
    if current_font != 'large' or not is_font_active:
        errors.append(f"Font change failed: current_font={current_font}, active={is_font_active}")

    print("--- 5. Testing Close Button ('✕') ---")
    btn_close = driver.find_element(By.ID, 'btnCloseThemeModal')
    btn_close.click()
    time.sleep(0.3)
    
    is_closed = 'open' not in overlay.get_attribute('class')
    print("Modal is closed after clicking '✕':", is_closed)
    if not is_closed:
        errors.append("Modal failed to close after clicking '✕' button")

    print("--- 6. Testing Backdrop Click to Close ---")
    btn_open.click()
    time.sleep(0.3)
    # Click outside sheet on overlay
    driver.execute_script("document.getElementById('themeModalOverlay').click();")
    time.sleep(0.3)
    is_closed_backdrop = 'open' not in overlay.get_attribute('class')
    print("Modal is closed after clicking backdrop:", is_closed_backdrop)
    if not is_closed_backdrop:
        errors.append("Modal failed to close after clicking overlay backdrop")

    print("--- 7. Testing Sheet Click Does Not Close (stopPropagation) ---")
    btn_open.click()
    time.sleep(0.3)
    sheet = driver.find_element(By.CLASS_NAME, 'theme-modal-sheet')
    sheet.click()
    time.sleep(0.3)
    still_open = 'open' in overlay.get_attribute('class')
    print("Modal remains open after clicking inside sheet:", still_open)
    if not still_open:
        errors.append("Modal erroneously closed when clicking inside sheet")

finally:
    driver.quit()

print("="*60)
if errors:
    print(f"FAILED with {len(errors)} errors:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
else:
    print("ALL 7 THEME MODAL TESTS PASSED PERFECTLY! ✅")

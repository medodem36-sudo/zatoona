import os, sys, time, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "index.html")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1280,1024")

driver = webdriver.Chrome(options=chrome_options)
passed = 0
failed = 0

def check(desc, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"  [PASS] {desc}")
    else:
        failed += 1
        print(f"  [FAIL] {desc}")

print("================================================================================")
print("TEST SUITE: AI INTERNET ACCESS, COMPACT RIBBON & SETTINGS REORDER")
print("================================================================================")

try:
    file_url = f"file:///{INDEX_PATH.replace(os.sep, '/')}"
    driver.get(file_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "homeHero")))
    time.sleep(1)

    print("\n--- 1. Check Removal of Outer Header Buttons & CSS Cleanliness ---")
    btn_header = driver.find_elements(By.ID, "btnHeaderSectionOrder")
    check("Header section order button removed from appHeader", len(btn_header) == 0)

    btn_home = driver.find_elements(By.ID, "btnHomeSectionOrder")
    check("Home section order button removed from homeHero", len(btn_home) == 0)

    # Check that .sec-reorder-group has display: none
    reorder_display = driver.execute_script("""
        const el = document.querySelector('.sec-reorder-group');
        return el ? window.getComputedStyle(el).display : 'none';
    """)
    check(".sec-reorder-group is hidden via CSS (display: none)", reorder_display == 'none')

    print("\n--- 2. Check AI Compact Ribbon & Toggle ---")
    # Verify AI functions
    has_funcs = driver.execute_script("""
        return typeof window.isAiCoachCollapsed === 'function' &&
               typeof window.toggleAiCoachCollapsed === 'function' &&
               typeof window.testGeminiConnectionNow === 'function' &&
               typeof window.syncAiSettingsUI === 'function';
    """)
    check("All AI assistant & ribbon control functions exist on window", has_funcs)

    # Enable AI Coach
    driver.execute_script("""
        const s = loadAiCoachSettings();
        s.enabled = true;
        s.consentGiven = true;
        saveAiCoachSettings(s);
        renderAiCoachCard();
    """)
    time.sleep(0.5)

    # Test collapsing AI coach into ribbon
    driver.execute_script("toggleAiCoachCollapsed(true);")
    time.sleep(0.5)
    is_ribbon_present = driver.execute_script("""
        return !!document.querySelector('.ai-compact-ribbon');
    """)
    check("AI assistant collapses into compact ribbon (.ai-compact-ribbon)", is_ribbon_present)
    check("localStorage reflects zatoona-ai-collapsed='true'", driver.execute_script("return localStorage.getItem('zatoona-ai-collapsed') === 'true';"))

    # Test expanding AI coach from ribbon
    driver.execute_script("toggleAiCoachCollapsed(false);")
    time.sleep(0.5)
    is_expanded_present = driver.execute_script("""
        return !document.querySelector('.ai-compact-ribbon') && !!document.getElementById('btnCollapseAiCoach');
    """)
    check("Clicking ribbon expands back to full AI coach with collapse button", is_expanded_present)
    check("localStorage reflects zatoona-ai-collapsed='false'", driver.execute_script("return localStorage.getItem('zatoona-ai-collapsed') === 'false';"))

    print("\n--- 3. Check Settings Tab AI Assistant Card ---")
    driver.execute_script("""
        mode = 'settings';
        applyMode();
        renderSettingsView();
    """)
    time.sleep(0.5)

    ai_card_present = driver.execute_script("return !!document.getElementById('settingsAiCard');")
    check("Settings tab includes #settingsAiCard", ai_card_present)

    ai_master_toggle = driver.execute_script("return !!document.getElementById('settingsAiMasterToggle');")
    check("#settingsAiMasterToggle exists in Settings", ai_master_toggle)

    ai_provider_sel = driver.execute_script("return !!document.getElementById('settingsAiProviderSelect');")
    check("#settingsAiProviderSelect exists in Settings", ai_provider_sel)

    ai_key_input = driver.execute_script("return !!document.getElementById('settingsAiApiKeyInput');")
    check("#settingsAiApiKeyInput exists in Settings", ai_key_input)

    btn_test_conn = driver.execute_script("return !!document.getElementById('btnTestAiConnection');")
    check("#btnTestAiConnection exists in Settings", btn_test_conn)

    # Test changing API key via Settings
    driver.execute_script("""
        onSettingsAiKeyInput('TEST_API_KEY_12345');
    """)
    time.sleep(0.2)
    saved_key = driver.execute_script("return loadAiCoachSettings().apiKey;")
    saved_prov = driver.execute_script("return loadAiCoachSettings().provider;")
    check("Entering API key saves key and switches provider to gemini", saved_key == 'TEST_API_KEY_12345' and saved_prov == 'gemini')

    # Test testing empty key warning
    driver.execute_script("""
        onSettingsAiKeyInput('');
        testGeminiConnectionNow();
    """)
    time.sleep(0.3)
    test_status = driver.execute_script("return document.getElementById('txtAiTestStatus').textContent;")
    check("Empty API key test reports warning", 'يرجى إدخال مفتاح' in test_status)

    print("\n--- 4. Check Settings Section Order Card & Interactive Reordering ---")
    order_card_present = driver.execute_script("return !!document.getElementById('settingsSectionOrderCard');")
    check("Settings tab includes #settingsSectionOrderCard", order_card_present)

    sec_grid_present = driver.execute_script("return !!document.getElementById('settingsSecOrderGrid');")
    check("#settingsSecOrderGrid section selector exists in Settings", sec_grid_present)

    # Click on homeHero section to reorder
    driver.execute_script("selectSectionForReorder('homeHero');")
    time.sleep(0.5)

    active_panel_visible = driver.execute_script("""
        const p = document.getElementById('settingsSecOrderActivePanel');
        return p && p.style.display !== 'none';
    """)
    check("Selecting section displays #settingsSecOrderActivePanel", active_panel_visible)

    items_count = driver.execute_script("""
        return document.querySelectorAll('#settingsSecOrderList .sec-order-item').length;
    """)
    check("Active panel renders reorder items for homeHero (> 5 items)", items_count > 5)

    # Test moving first item down
    first_key_before = driver.execute_script("""
        return document.querySelector('#homeHero > [data-sec-block]').getAttribute('data-sec-block');
    """)
    driver.execute_script(f"""
        settingsMoveSecBlock('homeHero', '{first_key_before}', 1);
    """)
    time.sleep(0.3)

    first_key_after = driver.execute_script("""
        return document.querySelector('#homeHero > [data-sec-block]').getAttribute('data-sec-block');
    """)
    check("settingsMoveSecBlock changes DOM order of blocks", first_key_before != first_key_after)

    # Check localStorage persistence
    saved_order = driver.execute_script("return JSON.parse(localStorage.getItem('zatoona-sec-order-homeHero') || '[]');")
    check("New order is persisted to localStorage (zatoona-sec-order-homeHero)", len(saved_order) > 0 and saved_order[1] == first_key_before)

    # Test reset section order
    driver.execute_script("resetSectionOrderFromSettings();")
    time.sleep(0.3)
    reset_order = driver.execute_script("return localStorage.getItem('zatoona-sec-order-homeHero');")
    check("resetSectionOrderFromSettings removes custom order from localStorage", reset_order is None)

    # Close panel
    driver.execute_script("closeSectionReorderPanel();")
    panel_closed = driver.execute_script("""
        return document.getElementById('settingsSecOrderActivePanel').style.display === 'none';
    """)
    check("closeSectionReorderPanel closes the active panel", panel_closed)

    print("\n--- 5. Browser Runtime Console Cleanliness ---")
    logs = driver.get_log("browser")
    severe_errors = [entry for entry in logs if entry["level"] == "SEVERE" and "favicon" not in entry["message"].lower() and "manifest.json" not in entry["message"] and "navigator.vibrate" not in entry["message"]]
    check("Zero SEVERE browser console runtime errors", len(severe_errors) == 0)
    if severe_errors:
        for err in severe_errors:
            print("  [ERROR]", err["message"])

finally:
    driver.quit()

print(f"\n================================================================================")
print(f"RESULTS: {passed} passed, {failed} failed")
print(f"================================================================================")

if failed > 0:
    sys.exit(1)

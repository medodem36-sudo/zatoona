import sys
sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

opts = Options()
opts.add_argument('--headless=new')
opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
driver = webdriver.Chrome(options=opts)

passed = 0
failed = 0

def test(name, condition, details=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name} {details}")
    else:
        failed += 1
        print(f"  [FAIL] {name} - {details}")

try:
    driver.get('file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')

    print("\n--- 1. Testing Water Cup Increment & Bug Fix ---")
    driver.execute_script("localStorage.removeItem('water:' + toISO(new Date()));")
    init_water = driver.execute_script("return loadWater(toISO(new Date()));")
    test("Initial water is 0", init_water == 0, f"got {init_water}")

    # Simulate clicking quick water button
    driver.execute_script("quickAddWaterUnified(1);")
    w1 = driver.execute_script("return loadWater(toISO(new Date()));")
    test("First click increments water to 1", w1 == 1, f"got {w1}")

    driver.execute_script("quickAddWaterUnified(1);")
    w2 = driver.execute_script("return loadWater(toISO(new Date()));")
    test("Second click increments water to 2", w2 == 2, f"got {w2}")

    # Test pointer event call simulation (like btnWater.click())
    driver.execute_script("quickAddWaterUnified({type: 'pointerdown'});")
    w3 = driver.execute_script("return loadWater(toISO(new Date()));")
    test("Passing event object defaults safely to +1 cup (does not reset or NaN)", w3 == 3, f"got {w3}")

    print("\n--- 2. Testing Weekly Date Navigator (renderTabs on week change) ---")
    day0_text = driver.execute_script("return document.querySelector('#tabs .tab:first-child .ddate').textContent;")
    driver.execute_script("shiftWeek(1);")
    day0_text_next = driver.execute_script("return document.querySelector('#tabs .tab:first-child .ddate').textContent;")
    test("Shifting week updates day dates in #tabs", day0_text != day0_text_next, f"old: {day0_text}, new: {day0_text_next}")
    driver.execute_script("shiftWeek(-1);") # return to current week

    print("\n--- 3. Testing Recovery Section DOM & Buttons ---")
    driver.execute_script("switchGymSubTab('recovery');")
    rec_scales_count = driver.execute_script("return document.querySelectorAll('#gymSubPaneRecovery .scale-row').length;")
    test("Recovery scales rendered inside gymSubPaneRecovery", rec_scales_count > 0, f"found {rec_scales_count} scales")

    # Click scale 4 on energy
    driver.execute_script("""
        const btn = document.querySelector('#gymSubPaneRecovery .scale-row[data-key="energy"] .scale-btn[data-val="4"]');
        if(btn) btn.click();
    """)
    energy_val = driver.execute_script("return recoveryState['energy'];")
    test("Clicking scale button updates recoveryState", energy_val == 4, f"got {energy_val}")

    print("\n--- 4. Testing Compact Mode & Conflict Prevention in Settings ---")
    driver.execute_script("toggleSettingsCompact(true);")
    is_compact = driver.execute_script("return document.body.classList.contains('compact-density');")
    test("toggleSettingsCompact(true) adds compact-density class to body", is_compact is True)

    # Now enable ultra-compact -> should disable compact-density
    driver.execute_script("toggleSettingsUltraCompact();")
    is_ultra = driver.execute_script("return document.body.classList.contains('ultra-compact');")
    is_compact_after = driver.execute_script("return document.body.classList.contains('compact-density');")
    test("Enabling ultra-compact disables compact-density to prevent conflict", is_ultra is True and is_compact_after is False)

    print("\n--- 5. Testing Qadaa & Shopping Buttons Toast Support ---")
    qadaa_toast = driver.execute_script("""
        window.ZATOONA_PHASE5.logFastMadeUp();
        const toast = document.querySelector('.zatoona-toast-pill');
        return toast ? toast.textContent : '';
    """)
    test("logFastMadeUp with 0 days shows informative toast instead of empty freeze", len(qadaa_toast) > 0, f"toast: {qadaa_toast[:50]}")

    print("\n--- 6. Testing Authentic Azkar Reader & Interactive Repetition Badges ---")
    has_azkar_reader = driver.execute_script("return document.getElementById('azkarReaderSection') !== null;")
    test("Azkar reader container exists in DOM", has_azkar_reader is True)

    driver.execute_script("toggleAzkarReader('morning');")
    morning_items_count = driver.execute_script("return document.querySelectorAll('#morningAzkarList .azkar-item-card').length;")
    test("Morning Azkar list renders full authentic prophetic texts", morning_items_count >= 10, f"found {morning_items_count} items")

    # Test decrementing a 3x dhikr (e.g. Ikhlas)
    driver.execute_script("decrementAzkarCount('morning', 'm_ikhlas', 3);")
    state_ikhlas = driver.execute_script("return getAzkarCountsState(toISO(new Date()), 'morning')['m_ikhlas'];")
    test("Tapping Azkar counter decrements remaining count", state_ikhlas == 2, f"remaining: {state_ikhlas}")

    print("\n--- 7. Testing Universal Section Block Reordering ---")
    first_block = driver.execute_script("return document.querySelector('#prayerView > [data-sec-block]').getAttribute('data-sec-block');")
    # Move the second block up
    driver.execute_script("""
        const secondBlock = document.querySelectorAll('#prayerView > [data-sec-block]')[1];
        const btnUp = secondBlock.querySelector('.sec-reorder-btn[title="تحريك لأعلى"]');
        if(btnUp) moveSecBlock(btnUp, -1);
    """)
    new_first_block = driver.execute_script("return document.querySelector('#prayerView > [data-sec-block]').getAttribute('data-sec-block');")
    test("moveSecBlock changes card order in the DOM", first_block != new_first_block, f"was {first_block}, now {new_first_block}")

    print("\n--- 8. Testing App User Guide in Settings ---")
    has_guide = driver.execute_script("return document.getElementById('settingsAppUserGuideCard') !== null;")
    test("App User Guide card exists in Settings", has_guide is True)
    guide_sections_count = driver.execute_script("return document.querySelectorAll('#userGuideAccordions .guide-item').length;")
    test("User Guide covers all main modules and buttons", guide_sections_count >= 6, f"found {guide_sections_count} guide sections")

    # Test guide search filter
    driver.execute_script("filterUserGuide('بومودورو');")
    visible_guide_items = driver.execute_script("""
        return Array.from(document.querySelectorAll('#userGuideAccordions .guide-item')).filter(it => it.style.display !== 'none').length;
    """)
    test("Guide search filter works accurately", visible_guide_items > 0, f"matching items: {visible_guide_items}")

    print("\n--- 9. Testing Local AI Assistant Placement ---")
    is_under_summary = driver.execute_script("""
        const summary = document.getElementById('homeSummaryCard');
        const ai = document.getElementById('aiCoachCard');
        return summary && ai && (summary.compareDocumentPosition(ai) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
    """)
    test("Local AI Assistant card is positioned under Daily Summary", is_under_summary is True)

finally:
    driver.quit()

print(f"\n==========================================")
print(f"Summary: {passed} passed, {failed} failed")
print(f"==========================================")
sys.exit(0 if failed == 0 else 1)

"""
Automated Acceptance Test Suite: Per-Manufacturer Battery Optimization Guide (Roadmap Proposal #15)
Phase 13.5B: OEM Battery Optimization Guide for Native & PWA Alarms
Tests DOM structure, modal opening/closing, tab switching, and Arabic content across major Android OEMs.
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.stdout.reconfigure(encoding='utf-8')

passed_count = 0
failed_count = 0

def test(name, condition, details=""):
    global passed_count, failed_count
    if condition:
        print(f"  [PASS] {name}")
        passed_count += 1
    else:
        print(f"  [FAIL] {name} - {details}")
        failed_count += 1

def run_tests():
    global passed_count, failed_count
    print("=" * 80)
    print("PHASE 13.5B ACCEPTANCE TEST SUITE: PER-MANUFACTURER BATTERY OPTIMIZATION GUIDE")
    print("=" * 80)

    html_path = os.path.abspath('index.html')
    file_url = 'file:///' + html_path.replace('\\', '/')

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--window-size=375,812')

    driver = webdriver.Chrome(options=opts)
    driver.get(file_url)
    time.sleep(1.0)

    def js(script):
        return driver.execute_script(script)

    try:
        # Group 1: DOM Elements Existence & Accessibility
        print("\n--- Group 1: DOM Elements & Accessibility ---")
        dom_check = js("""
            return {
                modal: !!document.getElementById('batteryGuideModal'),
                modalRole: document.getElementById('batteryGuideModal')?.getAttribute('role'),
                modalAria: document.getElementById('batteryGuideModal')?.getAttribute('aria-modal'),
                closeX: !!document.getElementById('batteryGuideCloseX'),
                closeBtn: !!document.getElementById('batteryGuideCloseBtn'),
                tabsContainer: !!document.querySelector('.battery-guide-tabs'),
                samsungTab: !!document.getElementById('bgTab-samsung'),
                xiaomiTab: !!document.getElementById('bgTab-xiaomi'),
                huaweiTab: !!document.getElementById('bgTab-huawei'),
                oppoTab: !!document.getElementById('bgTab-oppo'),
                pixelTab: !!document.getElementById('bgTab-pixel'),
                samsungPanel: !!document.getElementById('bgPanel-samsung'),
                xiaomiPanel: !!document.getElementById('bgPanel-xiaomi'),
                huaweiPanel: !!document.getElementById('bgPanel-huawei'),
                oppoPanel: !!document.getElementById('bgPanel-oppo'),
                pixelPanel: !!document.getElementById('bgPanel-pixel'),
                triggerBtn: !!document.getElementById('btnBatteryGuide')
            };
        """)

        test("#batteryGuideModal exists in DOM", dom_check.get('modal'))
        test("#batteryGuideModal has role='dialog'", dom_check.get('modalRole') == 'dialog')
        test("#batteryGuideModal has aria-modal='true'", dom_check.get('modalAria') == 'true')
        test("#batteryGuideCloseX exists", dom_check.get('closeX'))
        test("#batteryGuideCloseBtn exists", dom_check.get('closeBtn'))
        test("Battery guide tabs container exists", dom_check.get('tabsContainer'))
        test("All 5 OEM tabs exist (Samsung, Xiaomi, Huawei, Oppo, Pixel)", all([
            dom_check.get('samsungTab'),
            dom_check.get('xiaomiTab'),
            dom_check.get('huaweiTab'),
            dom_check.get('oppoTab'),
            dom_check.get('pixelTab')
        ]))
        test("All 5 OEM content panels exist", all([
            dom_check.get('samsungPanel'),
            dom_check.get('xiaomiPanel'),
            dom_check.get('huaweiPanel'),
            dom_check.get('oppoPanel'),
            dom_check.get('pixelPanel')
        ]))
        test("#btnBatteryGuide trigger button exists in UI", dom_check.get('triggerBtn'))

        # Group 2: Modal Open / Close Interactions
        print("\n--- Group 2: Modal Open / Close Interactions ---")
        
        # Test 1: Open via trigger button
        js("document.getElementById('btnBatteryGuide').click();")
        time.sleep(0.2)
        is_open = js("return document.getElementById('batteryGuideModal').classList.contains('open');")
        test("Clicking #btnBatteryGuide adds .open to modal", is_open)

        # Test 2: Close via X button
        js("document.getElementById('batteryGuideCloseX').click();")
        time.sleep(0.2)
        is_closed_x = js("return !document.getElementById('batteryGuideModal').classList.contains('open');")
        test("Clicking #batteryGuideCloseX removes .open", is_closed_x)

        # Test 3: Open via window.openBatteryGuide API with specific brand
        js("window.openBatteryGuide('xiaomi');")
        time.sleep(0.2)
        opened_xiaomi = js("""
            const modal = document.getElementById('batteryGuideModal');
            const xiaomiTab = document.getElementById('bgTab-xiaomi');
            const xiaomiPanel = document.getElementById('bgPanel-xiaomi');
            return modal.classList.contains('open') && 
                   xiaomiTab.classList.contains('active') && 
                   xiaomiPanel.classList.contains('active');
        """)
        test("window.openBatteryGuide('xiaomi') opens modal and activates Xiaomi tab", opened_xiaomi)

        # Test 4: Close via bottom button
        js("document.getElementById('batteryGuideCloseBtn').click();")
        time.sleep(0.2)
        is_closed_btn = js("return !document.getElementById('batteryGuideModal').classList.contains('open');")
        test("Clicking #batteryGuideCloseBtn removes .open", is_closed_btn)

        # Test 5: Close via Escape key
        js("window.openBatteryGuide('samsung');")
        time.sleep(0.2)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        time.sleep(0.2)
        is_closed_esc = js("return !document.getElementById('batteryGuideModal').classList.contains('open');")
        test("Pressing Escape key closes the battery guide modal", is_closed_esc)

        # Group 3: OEM Tab Switching Logic
        print("\n--- Group 3: OEM Tab Switching Logic ---")
        js("window.openBatteryGuide('samsung');")
        time.sleep(0.2)

        brands = ['samsung', 'xiaomi', 'huawei', 'oppo', 'pixel']
        for b in brands:
            js(f"document.getElementById('bgTab-{b}').click();")
            time.sleep(0.1)
            active_check = js(f"""
                const activeTab = document.getElementById('bgTab-{b}').classList.contains('active');
                const activePanel = document.getElementById('bgPanel-{b}').classList.contains('active');
                const otherPanelsHidden = ['samsung', 'xiaomi', 'huawei', 'oppo', 'pixel']
                    .filter(x => x !== '{b}')
                    .every(x => !document.getElementById('bgPanel-' + x).classList.contains('active'));
                return activeTab && activePanel && otherPanelsHidden;
            """)
            test(f"Switching to {b.capitalize()} tab correctly activates only its panel", active_check)

        # Group 4: Educational Content & Step Clarity Verification
        print("\n--- Group 4: Educational Content & Step Clarity ---")
        content_checks = js("""
            return {
                samsungText: document.getElementById('bgPanel-samsung').innerText,
                xiaomiText: document.getElementById('bgPanel-xiaomi').innerText,
                huaweiText: document.getElementById('bgPanel-huawei').innerText,
                oppoText: document.getElementById('bgPanel-oppo').innerText,
                pixelText: document.getElementById('bgPanel-pixel').innerText
            };
        """)

        samsung_valid = ("غير مقيّد" in content_checks['samsungText'] or "Unrestricted" in content_checks['samsungText']) and \
                        ("السكون" in content_checks['samsungText'] or "Sleep" in content_checks['samsungText'])
        test("Samsung panel mentions Unrestricted battery & Sleeping apps settings", samsung_valid)

        xiaomi_valid = ("التشغيل التلقائي" in content_checks['xiaomiText'] or "Autostart" in content_checks['xiaomiText']) and \
                       ("لا توجد قيود" in content_checks['xiaomiText'] or "No restrictions" in content_checks['xiaomiText'])
        test("Xiaomi panel mentions Autostart & No Restrictions settings", xiaomi_valid)

        huawei_valid = ("تشغيل التطبيقات" in content_checks['huaweiText'] or "App Launch" in content_checks['huaweiText']) and \
                       ("الإدارة التلقائية" in content_checks['huaweiText'] or "خلفية" in content_checks['huaweiText'])
        test("Huawei panel mentions App Launch & Manual Background Management", huawei_valid)

        oppo_valid = ("استخدام البطارية" in content_checks['oppoText'] or "نشاط الخلفية" in content_checks['oppoText']) and \
                     ("البدء التلقائي" in content_checks['oppoText'] or "تلقائي" in content_checks['oppoText'])
        test("Oppo/Realme panel mentions Background Activity & Auto-Launch", oppo_valid)

        pixel_valid = ("غير مقيّد" in content_checks['pixelText'] or "Unrestricted" in content_checks['pixelText']) and \
                      ("بطارية" in content_checks['pixelText'])
        test("Pixel/Stock panel mentions Unrestricted battery usage", pixel_valid)

        # Group 5: Native Android Shell Reassurance Detection
        print("\n--- Group 5: Native Android Shell Reassurance Detection ---")
        badge_pwa = js("""
            return document.getElementById('batteryGuideNativeBadge').innerText;
        """)
        test("PWA mode shows appropriate web/background guidance badge", "المتصفح" in badge_pwa or "الويب" in badge_pwa or "PWA" in badge_pwa)

        # Simulate window.ZatoonaNativeBridge
        js("""
            window.ZatoonaNativeBridge = { isMock: true };
            window.openBatteryGuide('samsung');
        """)
        time.sleep(0.1)
        badge_native = js("""
            return document.getElementById('batteryGuideNativeBadge').innerText;
        """)
        test("Native bridge presence activates native shell reassurance banner", "تطبيق" in badge_native or "Native" in badge_native or "أندرويد" in badge_native)

        # Cleanup
        js("window.closeBatteryGuide();")
        time.sleep(0.1)

    finally:
        driver.quit()

    print("\n" + "=" * 80)
    print(f"BATTERY OPTIMIZATION GUIDE TEST RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 80)
    return failed_count == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

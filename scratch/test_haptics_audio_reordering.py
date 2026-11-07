import os, sys, time, json
sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_test():
    print("=" * 70)
    print("TEST: Universal Card Reordering, Soft Haptics & Sound Control Center")
    print("=" * 70)

    html_path = os.path.abspath('index.html')
    file_url = f"file:///{html_path.replace(os.sep, '/')}"

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1280,1024')

    driver = webdriver.Chrome(options=opts)
    passed_checks = 0
    total_checks = 0

    def check(desc, condition):
        nonlocal passed_checks, total_checks
        total_checks += 1
        if condition:
            passed_checks += 1
            print(f"  [PASS] {desc}")
        else:
            print(f"  [FAIL] {desc}")

    try:
        driver.get(file_url)
        time.sleep(2)

        # 1. Haptics Settings Defaults
        print("\n--- 1. Testing Haptic Feedback Defaults & Softening ---")
        haptics_cfg = driver.execute_script("return loadHapticsSettings();")
        check("loadHapticsSettings exists and returns an object", isinstance(haptics_cfg, dict))
        check("Default haptics is enabled", haptics_cfg.get('enabled') is True)
        check("Default haptic strength is 'gentle' (softened)", haptics_cfg.get('strength') == 'gentle')
        check("Haptic buttons is enabled", haptics_cfg.get('buttons') is True)
        check("Haptic azkar is enabled", haptics_cfg.get('azkar') is True)
        check("Haptic timers is enabled", haptics_cfg.get('timers') is True)
        check("Haptic alerts is enabled", haptics_cfg.get('alerts') is True)
        check("Haptic logging is enabled", haptics_cfg.get('logging') is True)

        gentle_ms = driver.execute_script("return getHapticDuration('gentle', 'normal');")
        normal_ms = driver.execute_script("return getHapticDuration('normal', 'normal');")
        strong_ms = driver.execute_script("return getHapticDuration('strong', 'normal');")
        check(f"Gentle duration is soft (8ms) -> got {gentle_ms}", gentle_ms == 8)
        check(f"Normal duration is 15ms -> got {normal_ms}", normal_ms == 15)
        check(f"Strong duration is 28ms -> got {strong_ms}", strong_ms == 28)

        # 2. Haptics UI in Settings
        print("\n--- 2. Testing Haptics UI in Settings ---")
        driver.execute_script("navigateTo('settings');")
        time.sleep(0.5)

        haptic_card = driver.find_element(By.ID, "settingsHapticCard")
        check("settingsHapticCard exists in Settings view", haptic_card.is_displayed())

        # Test strength switching
        driver.execute_script("setHapticsStrengthChoice('strong');")
        check("Switched strength to strong", driver.execute_script("return loadHapticsSettings().strength;") == 'strong')
        driver.execute_script("setHapticsStrengthChoice('gentle');")
        check("Restored strength to gentle", driver.execute_script("return loadHapticsSettings().strength;") == 'gentle')

        # Test sub-feature toggle
        driver.execute_script("toggleHapticSubFeature('buttons');")
        check("Buttons haptic toggled off", driver.execute_script("return loadHapticsSettings().buttons;") is False)
        driver.execute_script("toggleHapticSubFeature('buttons');")
        check("Buttons haptic toggled on", driver.execute_script("return loadHapticsSettings().buttons;") is True)

        # Test master toggle
        driver.execute_script("toggleHapticsMaster();")
        check("Master haptics toggled off", driver.execute_script("return loadHapticsSettings().enabled;") is False)
        driver.execute_script("toggleHapticsMaster();")
        check("Master haptics toggled on", driver.execute_script("return loadHapticsSettings().enabled;") is True)

        # Test haptic button test click
        driver.execute_script("testHapticFeedbackNow();")
        status_txt = driver.find_element(By.ID, "txtHapticTestStatus").text
        check(f"Test haptic feedback button updates status text: '{status_txt}'", "تم الاهتزاز" in status_txt or "مللي" in status_txt)

        # 3. Audio & Sound Control Center
        print("\n--- 3. Testing Audio & Sound Control Center Defaults & Controls ---")
        audio_card = driver.find_element(By.ID, "settingsAudioCard")
        check("settingsAudioCard exists in Settings view", audio_card.is_displayed())

        audio_cfg = driver.execute_script("return loadAudioSettings();")
        check("loadAudioSettings exists and returns an object", isinstance(audio_cfg, dict))
        check("Default audio is enabled", audio_cfg.get('enabled') is True)
        check("Default volume is 70", audio_cfg.get('volume') == 70)
        check("Default tone is 'calm'", audio_cfg.get('tone') == 'calm')

        # Volume update
        driver.execute_script("updateAudioVolumeSetting(85);")
        check("Volume setting updated to 85%", driver.execute_script("return loadAudioSettings().volume;") == 85)
        check("Volume label shows 85%", driver.find_element(By.ID, "settingsAudioVolumeLabel").text == "85%")

        # Tone update
        driver.execute_script("saveAudioToneSetting('bell');")
        check("Tone updated to 'bell'", driver.execute_script("return loadAudioSettings().tone;") == 'bell')
        driver.execute_script("saveAudioToneSetting('water');")
        check("Tone updated to 'water'", driver.execute_script("return loadAudioSettings().tone;") == 'water')
        driver.execute_script("saveAudioToneSetting('calm');")
        check("Tone restored to 'calm'", driver.execute_script("return loadAudioSettings().tone;") == 'calm')

        # Sub-feature audio toggle
        driver.execute_script("toggleAudioSubFeature('azkar');")
        check("Azkar audio toggled off", driver.execute_script("return loadAudioSettings().azkar;") is False)
        driver.execute_script("toggleAudioSubFeature('azkar');")
        check("Azkar audio toggled on", driver.execute_script("return loadAudioSettings().azkar;") is True)

        # Audio test trigger
        driver.execute_script("testAppAudioNow();")
        audio_status = driver.find_element(By.ID, "txtAudioTestStatus").text
        check(f"Audio test button updates status text: '{audio_status}'", "تشغيل النغمة" in audio_status or "calm" in audio_status)

        # 4. Universal Card & Section Reordering
        print("\n--- 4. Testing Universal Card & Section Reordering ---")
        driver.execute_script("navigateTo('home');")
        time.sleep(0.5)

        home_blocks = driver.execute_script("""
            const c = document.getElementById('homeHero');
            return Array.from(c.children).filter(el => el.hasAttribute('data-sec-block')).map(el => el.getAttribute('data-sec-block'));
        """)
        check(f"Home section has registered data-sec-blocks: {home_blocks}", len(home_blocks) >= 4)

        # Test moveSecBlock on Home
        first_block = home_blocks[0]
        second_block = home_blocks[1]
        driver.execute_script(f"""
            const el = document.querySelector('[data-sec-block="{first_block}"]');
            const parent = el.parentElement;
            const next = el.nextElementSibling;
            parent.insertBefore(next, el);
            saveSecBlockOrder(parent);
        """)
        saved_order = driver.execute_script("return JSON.parse(localStorage.getItem('zatoona-sec-order-homeHero'));")
        check(f"Reorder persisted in localStorage: {saved_order[:2]}", saved_order[0] == second_block and saved_order[1] == first_block)

        # Test reset
        driver.execute_script("resetCurrentSectionOrder();")
        cleared_order = driver.execute_script("return localStorage.getItem('zatoona-sec-order-homeHero');")
        check("resetCurrentSectionOrder cleared localStorage", cleared_order is None)

        # Test Reorder Modal
        print("\n--- 5. Testing Section Reorder Modal Dialog ---")
        driver.execute_script("openCurrentSectionOrderModal();")
        modal = driver.find_element(By.ID, "sectionOrderModal")
        check("Section order modal opened", modal.is_displayed())

        list_items = driver.find_elements(By.CSS_SELECTOR, "#sectionOrderModalList .sec-order-item")
        check(f"Modal list populated with section cards: {len(list_items)} items", len(list_items) >= 4)

        driver.execute_script("closeSectionOrderModal();")
        check("Section order modal closed", not modal.is_displayed())

        # Test across Gym and Prayer views
        print("\n--- 6. Testing Gym & Prayer Views Card Blocks ---")
        driver.execute_script("navigateTo('gym');")
        time.sleep(0.5)
        gym_blocks = driver.execute_script("""
            const c = document.getElementById('gymView');
            return Array.from(c.querySelectorAll('[data-sec-block]')).map(el => el.getAttribute('data-sec-block'));
        """)
        check(f"Gym view has data-sec-blocks: {gym_blocks}", len(gym_blocks) >= 4)

        driver.execute_script("navigateTo('prayer');")
        time.sleep(0.5)
        prayer_blocks = driver.execute_script("""
            const c = document.getElementById('prayerView');
            return Array.from(c.querySelectorAll('[data-sec-block]')).map(el => el.getAttribute('data-sec-block'));
        """)
        check(f"Prayer view has data-sec-blocks: {prayer_blocks}", len(prayer_blocks) >= 5)

        # 7. Zero Console Errors
        print("\n--- 7. Checking Browser Console Logs ---")
        logs = driver.get_log('browser')
        severe_errors = [l for l in logs if l['level'] == 'SEVERE' and 'manifest.json' not in l['message'] and 'navigator.vibrate' not in l['message']]
        check(f"Zero SEVERE console errors (found {len(severe_errors)})", len(severe_errors) == 0)
        if severe_errors:
            for err in severe_errors[:5]:
                print(f"  [ERROR] {err['message']}")

    finally:
        driver.quit()

    print("\n" + "=" * 70)
    print(f"TEST RESULTS: {passed_checks} / {total_checks} PASSED ({(passed_checks/total_checks)*100:.1f}%)")
    print("=" * 70)
    return passed_checks == total_checks

if __name__ == '__main__':
    ok = run_test()
    sys.exit(0 if ok else 1)

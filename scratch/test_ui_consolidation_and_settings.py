#!/usr/bin/env python3
"""
Test Suite: UI Consolidation, Settings View, Themes, and Scrollbar Removal
========================================================================
Verifies:
1. Consolidation of Recovery & Stretches inside Gym with sub-tabs
2. Dedicated Settings View (#settingsView) with appearance, toggles, data, alarms
3. New color themes (Amber, Violet, Crimson, Emerald, Titanium, Sapphire, Sunset)
4. Ultra-compact layout toggle
5. Feature toggles for hiding/showing modules
6. Complete global scrollbar removal in CSS and native Android WebView
7. 3-Way HTML parity
8. Language selection and persistence
9. Centralized Data & Backup controls in Settings view
10. Overview Section 10 clean redirection without duplicate controls
"""
import unittest, os, hashlib, json, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO, 'index.html')
ZATOONA_PATH = os.path.join(REPO, 'zatoona.html')
ASSETS_PATH = os.path.join(REPO, 'android', 'app', 'src', 'main', 'assets', 'index.html')
MAIN_KT_PATH = os.path.join(REPO, 'android', 'app', 'src', 'main', 'java', 'com', 'zatoona', 'app', 'MainActivity.kt')
BRIDGE_KT_PATH = os.path.join(REPO, 'android', 'app', 'src', 'main', 'java', 'com', 'zatoona', 'app', 'ZatoonaBridge.kt')

class TestConsolidationAndSettings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            cls.html = f.read()

        opts = Options()
        opts.add_argument('--headless=new')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--window-size=412,915')
        cls.driver = webdriver.Chrome(options=opts)
        cls.driver.get(f"file:///{os.path.abspath(INDEX_PATH)}")
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()

    # --- 1. Three-way Parity ---
    def test_01_three_way_parity(self):
        h1 = hashlib.sha256(open(INDEX_PATH, 'rb').read()).hexdigest()
        h2 = hashlib.sha256(open(ZATOONA_PATH, 'rb').read()).hexdigest()
        h3 = hashlib.sha256(open(ASSETS_PATH, 'rb').read()).hexdigest()
        self.assertEqual(h1, h2, "index.html != zatoona.html")
        self.assertEqual(h1, h3, "index.html != android assets index.html")

    # --- 2. Scrollbar Removal ---
    def test_02_scrollbar_removal_css_and_kotlin(self):
        self.assertIn("scrollbar-width: none !important;", self.html)
        self.assertIn("::-webkit-scrollbar", self.html)
        self.assertIn("display: none !important;", self.html)

        with open(MAIN_KT_PATH, 'r', encoding='utf-8') as f:
            kt = f.read()
        self.assertIn("isVerticalScrollBarEnabled = false", kt)
        self.assertIn("isHorizontalScrollBarEnabled = false", kt)

    # --- 3. Gym Sub-Tabs Consolidation ---
    def test_03_gym_subtabs_exist_and_toggle(self):
        driver = self.driver
        driver.execute_script("navigateTo('gym');")
        time.sleep(0.3)

        # Sub-tabs container exists
        subtabs = driver.find_element(By.ID, "gymSubTabs")
        self.assertIsNotNone(subtabs)

        # Tab buttons exist
        btn_w = driver.find_element(By.ID, "gymTabWorkout")
        btn_s = driver.find_element(By.ID, "gymTabStretches")
        btn_r = driver.find_element(By.ID, "gymTabRecovery")
        self.assertTrue(btn_w.is_displayed())
        self.assertTrue(btn_s.is_displayed())
        self.assertTrue(btn_r.is_displayed())

        # Switch to Stretches
        driver.execute_script("switchGymSubTab('stretches');")
        time.sleep(0.2)
        pane_s = driver.find_element(By.ID, "gymSubPaneStretches")
        self.assertNotIn("hidden", pane_s.get_attribute("class"))

        # Switch to Recovery
        driver.execute_script("switchGymSubTab('recovery');")
        time.sleep(0.2)
        pane_r = driver.find_element(By.ID, "gymSubPaneRecovery")
        self.assertNotIn("hidden", pane_r.get_attribute("class"))

        # Switch back to Workout
        driver.execute_script("switchGymSubTab('workout');")
        time.sleep(0.2)
        pane_w = driver.find_element(By.ID, "gymWorkoutBlock")
        self.assertNotIn("hidden", pane_w.get_attribute("class"))

    # --- 4. Backwards-compatible Navigation Redirects ---
    def test_04_navigation_redirects_to_gym_subtabs(self):
        driver = self.driver
        # Navigate to 'recovery' -> should open gym on recovery subtab
        driver.execute_script("navigateTo('recovery');")
        time.sleep(0.3)
        current_mode = driver.execute_script("return mode;")
        self.assertEqual(current_mode, "gym")
        pane_r = driver.find_element(By.ID, "gymSubPaneRecovery")
        self.assertNotIn("hidden", pane_r.get_attribute("class"))

        # Navigate to 'stretches' -> should open gym on stretches subtab
        driver.execute_script("navigateTo('stretches');")
        time.sleep(0.3)
        current_mode = driver.execute_script("return mode;")
        self.assertEqual(current_mode, "gym")
        pane_s = driver.find_element(By.ID, "gymSubPaneStretches")
        self.assertNotIn("hidden", pane_s.get_attribute("class"))

    # --- 5. Settings View and Features ---
    def test_05_settings_view_structure(self):
        driver = self.driver
        driver.execute_script("navigateTo('settings');")
        time.sleep(0.3)

        view = driver.find_element(By.ID, "settingsView")
        self.assertNotIn("hidden", view.get_attribute("class"))

        # Light mode grid, Color theme grid, Accent grid
        self.assertIsNotNone(driver.find_element(By.ID, "settingsLightModeGrid"))
        self.assertIsNotNone(driver.find_element(By.ID, "settingsColorThemeGrid"))
        self.assertIsNotNone(driver.find_element(By.ID, "settingsAccentGrid"))

        # Toggles exist
        self.assertIsNotNone(driver.find_element(By.ID, "settingsFontToggle"))
        self.assertIsNotNone(driver.find_element(By.ID, "settingsCompactToggle"))
        self.assertIsNotNone(driver.find_element(By.ID, "settingsUltraCompactToggle"))

        # Feature toggles container exists
        self.assertIsNotNone(driver.find_element(By.ID, "settingsFeatureToggles"))

    # --- 6. New Color Themes (including Sapphire and Sunset) ---
    def test_06_new_color_themes(self):
        driver = self.driver
        themes = ['theme-amber', 'theme-violet', 'theme-crimson', 'theme-emerald', 'theme-titanium', 'theme-sapphire', 'theme-sunset']
        for t in themes:
            driver.execute_script(f"selectColorTheme('{t}');")
            body_class = driver.find_element(By.TAG_NAME, "body").get_attribute("class")
            self.assertIn(t, body_class)
            saved = driver.execute_script("return localStorage.getItem('zatoona-color-theme');")
            self.assertEqual(saved, t)

        # Reset to default
        driver.execute_script("selectColorTheme('');")
        saved = driver.execute_script("return localStorage.getItem('zatoona-color-theme');")
        self.assertEqual(saved, '')

    # --- 7. Ultra-Compact Mode ---
    def test_07_ultra_compact_mode(self):
        driver = self.driver
        driver.execute_script("toggleUltraCompact(true);")
        body_class = driver.find_element(By.TAG_NAME, "body").get_attribute("class")
        self.assertIn("ultra-compact", body_class)
        saved = driver.execute_script("return localStorage.getItem('zatoona-ultra-compact');")
        self.assertEqual(saved, "1")

        driver.execute_script("toggleUltraCompact(false);")
        body_class = driver.find_element(By.TAG_NAME, "body").get_attribute("class")
        self.assertNotIn("ultra-compact", body_class)

    # --- 8. Feature Toggles ---
    def test_08_feature_toggles_hide_and_show(self):
        driver = self.driver
        # Toggle 'study' off
        driver.execute_script("toggleFeature('study');")
        toggles = driver.execute_script("return getFeatureToggles();")
        self.assertFalse(toggles.get('study'))

        # Check that study nav is hidden
        study_draw = driver.find_element(By.ID, "drawNav-study")
        self.assertEqual(study_draw.value_of_css_property("display"), "none")

        # Toggle 'study' back on
        driver.execute_script("toggleFeature('study');")
        toggles = driver.execute_script("return getFeatureToggles();")
        self.assertTrue(toggles.get('study'))
        self.assertNotEqual(study_draw.value_of_css_property("display"), "none")

    # --- 9. Bridge Contract Updates ---
    def test_09_bridge_contract_includes_settings(self):
        with open(BRIDGE_KT_PATH, 'r', encoding='utf-8') as f:
            bkt = f.read()
        self.assertIn('"settings"', bkt)
        self.assertIn("'settings'", self.html)

    # --- 10. Clean Console on Navigation ---
    def test_10_zero_severe_console_errors(self):
        driver = self.driver
        # Navigate through all key views
        for m in ['home', 'prayer', 'gym', 'meal', 'sleep', 'schedule', 'study', 'budget', 'notes', 'overview', 'search', 'settings']:
            driver.execute_script(f"navigateTo('{m}');")
            time.sleep(0.1)

        logs = driver.get_log('browser')
        severe = [l for l in logs if l['level'] == 'SEVERE' and 'manifest.json' not in l['message']]
        self.assertEqual(len(severe), 0, f"Severe console errors found: {severe}")

    # --- 11. Language Setting Selection & Persistence ---
    def test_11_language_setting_selection_and_persistence(self):
        driver = self.driver
        driver.execute_script("navigateTo('settings');")
        time.sleep(0.2)
        lang_sel = driver.find_element(By.ID, "settingsLanguageSelect")
        self.assertIsNotNone(lang_sel)

        # Set to MSA
        driver.execute_script("saveLanguageSetting('ar-msa');")
        saved = driver.execute_script("return localStorage.getItem('zatoona-app-language');")
        self.assertEqual(saved, 'ar-msa')

        # Reset to Egyptian
        driver.execute_script("saveLanguageSetting('ar-eg');")
        saved = driver.execute_script("return localStorage.getItem('zatoona-app-language');")
        self.assertEqual(saved, 'ar-eg')

    # --- 12. Centralized Data & Backup Controls in Settings ---
    def test_12_centralized_data_backup_controls(self):
        driver = self.driver
        driver.execute_script("navigateTo('settings');")
        time.sleep(0.2)
        self.assertIsNotNone(driver.find_element(By.ID, "exportData"))
        self.assertIsNotNone(driver.find_element(By.ID, "importDataBtn"))
        self.assertIsNotNone(driver.find_element(By.ID, "importDataFile"))
        self.assertIsNotNone(driver.find_element(By.ID, "chkEncryptBackup"))
        self.assertIsNotNone(driver.find_element(By.ID, "selBackupReminderInterval"))

    # --- 13. Overview Section 10 Redirection Cleanliness ---
    def test_13_overview_clean_redirection(self):
        driver = self.driver
        driver.execute_script("navigateTo('overview');")
        time.sleep(0.2)
        overview = driver.find_element(By.ID, "overviewView")
        self.assertIn("تم نقل أدوات النسخ الاحتياطي للأمان المركزي", overview.text)

if __name__ == '__main__':
    unittest.main()

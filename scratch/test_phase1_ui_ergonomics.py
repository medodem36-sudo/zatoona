import unittest
import hashlib
import os
import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
ZATOONA_PATH = os.path.join(ROOT_DIR, "zatoona.html")
ANDROID_ASSET_PATH = os.path.join(ROOT_DIR, "android", "app", "src", "main", "assets", "index.html")
BRIDGE_PATH = os.path.join(ROOT_DIR, "android", "app", "src", "main", "java", "com", "zatoona", "app", "ZatoonaBridge.kt")

class TestPhase1UIErgonomics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            cls.html = f.read()
        with open(BRIDGE_PATH, "r", encoding="utf-8") as f:
            cls.bridge = f.read()

    def test_01_html_three_way_byte_parity(self):
        """All 3 entrypoint HTML files must have identical size and SHA-256."""
        files = [INDEX_PATH, ZATOONA_PATH, ANDROID_ASSET_PATH]
        hashes = set()
        sizes = set()
        for fp in files:
            with open(fp, "rb") as f:
                data = f.read()
                sizes.add(len(data))
                hashes.add(hashlib.sha256(data).hexdigest())
        self.assertEqual(len(sizes), 1, f"Sizes differ: {sizes}")
        self.assertEqual(len(hashes), 1, f"Hashes differ: {hashes}")

    def test_02_native_bridge_trigger_haptic(self):
        """ZatoonaBridge.kt must have @JavascriptInterface fun triggerHaptic."""
        self.assertIn("@JavascriptInterface", self.bridge)
        self.assertIn("fun triggerHaptic(durationMs: Long", self.bridge)
        self.assertIn("vibrator", self.bridge)

    def test_03_pitch_black_amoled_css_variables(self):
        """CSS must define [data-theme='amoled'] with #000000 black background and no glow/shadow."""
        self.assertIn('[data-theme="amoled"]', self.html)
        self.assertIn('--bg:#000000;', self.html)
        self.assertIn('--card:#0A0A0A;', self.html)

    def test_04_custom_accent_colors_css(self):
        """CSS must define accent colors: ocean, amber, royal."""
        self.assertIn('[data-accent="ocean"]', self.html)
        self.assertIn('[data-accent="amber"]', self.html)
        self.assertIn('[data-accent="royal"]', self.html)

    def test_05_custom_font_scaling_css(self):
        """CSS must define font scaling for large text."""
        self.assertIn('[data-font-size="large"]', self.html)

    def test_06_compact_dashboard_css(self):
        """CSS must define compact dashboard rules."""
        self.assertIn('.compact-dashboard', self.html)
        self.assertIn('.compact-dashboard .home-stat-card', self.html)

    def test_07_morning_briefing_card_markup_and_css(self):
        """Markup and CSS for morning briefing card must be present."""
        self.assertIn('id="morningBriefingCard"', self.html)
        self.assertIn('.morning-briefing-card', self.html)
        self.assertIn('.mbc-header', self.html)
        self.assertIn('.mbc-content', self.html)

    def test_08_dashboard_toolbar_markup_and_css(self):
        """Dashboard toolbar container and CSS must be present."""
        self.assertIn('id="dashboardToolbar"', self.html)
        self.assertIn('.dashboard-toolbar', self.html)
        self.assertIn('.dt-btn', self.html)

    def test_09_theme_customizer_modal_markup(self):
        """Theme customizer modal overlay and sheet must be present."""
        self.assertIn('id="themeModalOverlay"', self.html)
        self.assertIn('id="btnOpenThemeModal"', self.html)
        self.assertIn('data-theme-choice="amoled"', self.html)
        self.assertIn('data-accent-choice="emerald"', self.html)
        self.assertIn('data-font-choice="large"', self.html)

    def test_10_known_key_patterns_includes_new_keys(self):
        """KNOWN_KEY_PATTERNS must include compact-dashboard, dashboard-cards-order, morning-briefing-collapsed, theme-accent, theme-font-scale."""
        self.assertIn('compact-dashboard', self.html)
        self.assertIn('dashboard-cards-order', self.html)
        self.assertIn('morning-briefing-collapsed', self.html)
        self.assertIn('theme-accent', self.html)
        self.assertIn('theme-font-scale', self.html)

    def test_11_js_functions_defined(self):
        """JS helper functions for Phase 1 must be declared in index.html."""
        required_fns = [
            "function triggerHaptic(",
            "function loadThemeAccent(",
            "function saveThemeAccent(",
            "function applyThemeAccent(",
            "function loadThemeFontScale(",
            "function saveThemeFontScale(",
            "function applyThemeFontScale(",
            "function loadCompactDashboard(",
            "function saveCompactDashboard(",
            "function applyCompactDashboard(",
            "function toggleCompactDashboard(",
            "function loadDashboardCardsOrder(",
            "function saveDashboardCardsOrder(",
            "function moveDashboardCard(",
            "function toggleDashboardCustomizeMode(",
            "function resetDashboardCardsOrder(",
            "function loadMorningBriefingCollapsed(",
            "function toggleMorningBriefing(",
            "function renderMorningBriefingCard(",
            "function quickAddWater(",
            "function initThemeCustomizerModal(",
            "function openThemeCustomizer(",
            "function closeThemeCustomizer(",
        ]
        for fn in required_fns:
            self.assertIn(fn, self.html, f"Missing function: {fn}")

    def test_12_selenium_runtime_verification(self):
        """Test full runtime execution using headless Chrome."""
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--allow-file-access-from-files")

        driver = None
        try:
            driver = webdriver.Chrome(options=options)
            file_url = f"file:///{INDEX_PATH.replace(os.sep, '/')}"
            driver.get(file_url)

            # Wait for app ready
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return typeof renderHomeDashboard === 'function';")
            )

            # 1. Test Theme Cycling: Light -> Dark -> AMOLED -> Light
            driver.execute_script("applyTheme('light', true);")
            self.assertEqual(driver.execute_script("return document.documentElement.getAttribute('data-theme');"), "light")
            
            driver.execute_script("toggleTheme();")
            self.assertEqual(driver.execute_script("return document.documentElement.getAttribute('data-theme');"), "dark")

            driver.execute_script("toggleTheme();")
            self.assertEqual(driver.execute_script("return document.documentElement.getAttribute('data-theme');"), "amoled")

            driver.execute_script("toggleTheme();")
            self.assertEqual(driver.execute_script("return document.documentElement.getAttribute('data-theme');"), "light")

            # 2. Test Accent Colors
            driver.execute_script("saveThemeAccent('ocean');")
            self.assertEqual(driver.execute_script("return document.documentElement.getAttribute('data-accent');"), "ocean")

            driver.execute_script("saveThemeAccent('royal');")
            self.assertEqual(driver.execute_script("return document.documentElement.getAttribute('data-accent');"), "royal")

            driver.execute_script("saveThemeAccent('emerald');")
            self.assertEqual(driver.execute_script("return document.documentElement.getAttribute('data-accent');"), "emerald")

            # 3. Test Font Scaling
            driver.execute_script("saveThemeFontScale('large');")
            self.assertEqual(driver.execute_script("return document.documentElement.getAttribute('data-font-size');"), "large")

            driver.execute_script("saveThemeFontScale('normal');")
            self.assertEqual(driver.execute_script("return document.documentElement.getAttribute('data-font-size');"), "normal")

            # 4. Test Compact Dashboard Toggle
            driver.execute_script("renderHomeDashboard();")
            driver.execute_script("saveCompactDashboard(true);")
            self.assertTrue(driver.execute_script("return loadCompactDashboard();"))
            grid_classes = driver.execute_script("return document.getElementById('homeStatsGrid').className;")
            self.assertIn("compact-dashboard", grid_classes)

            driver.execute_script("saveCompactDashboard(false);")
            self.assertFalse(driver.execute_script("return loadCompactDashboard();"))
            grid_classes = driver.execute_script("return document.getElementById('homeStatsGrid').className;")
            self.assertNotIn("compact-dashboard", grid_classes)

            # 5. Test Dashboard Card Reordering
            initial_order = driver.execute_script("return loadDashboardCardsOrder();")
            self.assertEqual(initial_order[0], "prayer")
            
            # Move prayer down
            driver.execute_script("moveDashboardCard('prayer', 'down');")
            new_order = driver.execute_script("return loadDashboardCardsOrder();")
            self.assertEqual(new_order[1], "prayer")

            # Move prayer back up
            driver.execute_script("moveDashboardCard('prayer', 'up');")
            restored_order = driver.execute_script("return loadDashboardCardsOrder();")
            self.assertEqual(restored_order[0], "prayer")

            # 6. Test Morning Briefing Card Render & Toggle
            driver.execute_script("renderMorningBriefingCard('2026-11-01', new Date('2026-11-01T08:00:00'));")
            briefing_text = driver.execute_script("return document.getElementById('morningBriefingCard').innerText;")
            self.assertIn("صباح الخير", briefing_text)
            self.assertIn("الصلاة القادمة", briefing_text)

            # 7. Test Quick Water Logging (+1 cup, -1 cup)
            water_before = driver.execute_script("return loadWater(toISO(new Date()));")
            driver.execute_script("quickAddWater(1);")
            water_after = driver.execute_script("return loadWater(toISO(new Date()));")
            self.assertEqual(water_after, water_before + 1)

            driver.execute_script("quickAddWater(-1);")
            water_final = driver.execute_script("return loadWater(toISO(new Date()));")
            self.assertEqual(water_final, water_before)

            # 8. Test Modal Open & Close
            driver.execute_script("openThemeCustomizer();")
            is_open = driver.execute_script("return document.getElementById('themeModalOverlay').classList.contains('open');")
            self.assertTrue(is_open)

            driver.execute_script("closeThemeCustomizer();")
            is_closed = driver.execute_script("return !document.getElementById('themeModalOverlay').classList.contains('open');")
            self.assertTrue(is_closed)

        finally:
            if driver:
                driver.quit()

if __name__ == "__main__":
    unittest.main()

import unittest
import os
import hashlib
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(REPO_DIR, "index.html")
ZATOONA_HTML = os.path.join(REPO_DIR, "zatoona.html")
ASSETS_INDEX_HTML = os.path.join(REPO_DIR, "android", "app", "src", "main", "assets", "index.html")

class TestPhase4NutritionEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,1024")
        chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get(f"file:///{INDEX_HTML.replace(os.sep, '/')}")
        WebDriverWait(cls.driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)
        # Suppress alerts during test execution
        cls.driver.execute_script("window.alert = function(){};")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    def test_01_three_way_html_parity(self):
        """Verify 100% byte-for-byte and SHA-256 parity across the 3 HTML files."""
        for p in [INDEX_HTML, ZATOONA_HTML, ASSETS_INDEX_HTML]:
            self.assertTrue(os.path.exists(p), f"File missing: {p}")
            self.assertGreater(os.path.getsize(p), 1_500_000, f"File too small: {p}")

        h_idx = hashlib.sha256(open(INDEX_HTML, "rb").read()).hexdigest()
        h_zat = hashlib.sha256(open(ZATOONA_HTML, "rb").read()).hexdigest()
        h_ast = hashlib.sha256(open(ASSETS_INDEX_HTML, "rb").read()).hexdigest()

        self.assertEqual(h_idx, h_zat, "Parity mismatch: index.html != zatoona.html")
        self.assertEqual(h_idx, h_ast, "Parity mismatch: index.html != assets/index.html")

    def test_02_known_key_patterns_includes_phase4_keys(self):
        """Verify KNOWN_KEY_PATTERNS in index.html includes Phase 4 storage keys."""
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("/^nutrition-favorite-combos/", content)
        self.assertIn("/^nutrition-protein-cost/", content)
        self.assertIn("/^nutrition-carb-cycling/", content)

    def test_03_nutrition_intelligence_elements_rendered(self):
        """Verify presence of quick bar buttons and intelligence cards in meal view."""
        self.driver.execute_script("navigateTo('meal');")
        time.sleep(0.5)

        for el_id in [
            'btnOpenPantrySuggestions',
            'btnOpenProteinCostCalc',
            'btnOpenFavoriteCombos',
            'btnOpenCarbCycling',
            'carbCyclingStatusCard',
            'weeklyDeficitCard',
            'sodiumPotassiumCard'
        ]:
            el = self.driver.find_element(By.ID, el_id)
            self.assertIsNotNone(el, f"Element #{el_id} should be present in meal view")

    def test_04_pantry_meal_suggestions_workflow(self):
        """Verify opening pantry suggestions modal, filtering, and adding meal to current day."""
        self.driver.execute_script("navigateTo('meal');")
        time.sleep(0.3)
        self.driver.execute_script("window.ZATOONA_PHASE4.openPantrySuggestions();")
        time.sleep(0.3)

        modal = self.driver.find_element(By.ID, "pantryMealSuggestionsModal")
        self.assertIn("open", modal.get_attribute("class"))

        # Verify list is populated
        items_count = self.driver.execute_script("""
            const container = document.getElementById('pantryMealSuggestionsList');
            return container ? container.querySelectorAll('.pantry-meal-item').length : 0;
        """)
        self.assertGreater(items_count, 0, "Pantry suggestions list should contain items")

        # Test filter
        self.driver.execute_script("window.ZATOONA_PHASE4.filterPantryMeals('protein');")
        time.sleep(0.2)

        # Test adding suggestion to day
        success = self.driver.execute_script("""
            try {
                window.ZATOONA_PHASE4.addMealSuggestionToDay('شاورما دجاج تجريبية', 450, 40, 30, 10);
                return true;
            } catch(e) {
                return false;
            }
        """)
        self.assertTrue(success, "Adding meal suggestion to day should succeed")
        self.driver.execute_script("window.ZATOONA_PHASE4.closeModals();")

    def test_05_protein_to_cost_calculator_workflow(self):
        """Verify protein-to-cost calculator modal, table rendering, calculations, and price updates."""
        self.driver.execute_script("window.ZATOONA_PHASE4.openProteinCostCalc();")
        time.sleep(0.3)

        modal = self.driver.find_element(By.ID, "proteinCostCalcModal")
        self.assertIn("open", modal.get_attribute("class"))

        rows_count = self.driver.execute_script("""
            const tbody = document.getElementById('proteinCalcTableBody');
            return tbody ? tbody.querySelectorAll('tr').length : 0;
        """)
        self.assertGreaterEqual(rows_count, 8, "Protein calc table should have at least 8 sources")

        # Verify updating price
        updated = self.driver.execute_script("""
            try {
                window.ZATOONA_PHASE4.updateProteinSourcePrice(0, 6.0);
                return true;
            } catch(e) {
                return false;
            }
        """)
        self.assertTrue(updated, "Updating protein price should succeed")

        # Reset prices
        self.driver.execute_script("window.ZATOONA_PHASE4.resetProteinCostPrices();")
        self.driver.execute_script("window.ZATOONA_PHASE4.closeModals();")

    def test_06_favorite_combos_workflow(self):
        """Verify favorite combos modal, creating new combo, saving, and applying to day."""
        self.driver.execute_script("window.ZATOONA_PHASE4.openFavoriteCombos();")
        time.sleep(0.3)

        modal = self.driver.find_element(By.ID, "favoriteCombosModal")
        self.assertIn("open", modal.get_attribute("class"))

        # Verify adding new combo
        res = self.driver.execute_script("""
            try {
                document.getElementById('addComboForm').style.display = 'block';
                document.getElementById('comboNameInput').value = 'خلطة الطاقة الصباحية';
                document.getElementById('comboKcalInput').value = '500';
                document.getElementById('comboProteinInput').value = '35';
                document.getElementById('comboCarbInput').value = '60';
                document.getElementById('comboFatInput').value = '12';
                window.ZATOONA_PHASE4.saveNewCombo();
                return true;
            } catch(e) {
                return false;
            }
        """)
        self.assertTrue(res, "Saving new combo should succeed")

        # Verify combo exists in list
        found = self.driver.execute_script("""
            const text = document.getElementById('favoriteCombosList')?.textContent || '';
            return text.includes('خلطة الطاقة الصباحية');
        """)
        self.assertTrue(found, "Newly added combo should appear in combos list")

        self.driver.execute_script("window.ZATOONA_PHASE4.closeModals();")

    def test_07_smart_carb_cycling_workflow(self):
        """Verify carb cycling modal, settings, and dynamic day mode evaluation."""
        self.driver.execute_script("window.ZATOONA_PHASE4.openCarbCyclingModal();")
        time.sleep(0.3)

        modal = self.driver.find_element(By.ID, "carbCyclingModal")
        self.assertIn("open", modal.get_attribute("class"))

        mode_info = self.driver.execute_script("""
            return window.ZATOONA_PHASE4.getEffectiveCarbMode('2026-11-02');
        """)
        self.assertIsNotNone(mode_info, "Effective carb mode should return valid object")
        self.assertIn(mode_info.get('mode'), ['high', 'mod', 'low'])
        self.assertGreater(mode_info.get('grams', 0), 0)

        self.driver.execute_script("window.ZATOONA_PHASE4.closeModals();")

    def test_08_weekly_deficit_progress_tracking(self):
        """Verify weekly caloric deficit card updates with sensible values."""
        self.driver.execute_script("window.ZATOONA_PHASE4.updateWeeklyDeficitCard();")
        time.sleep(0.2)

        val_text = self.driver.find_element(By.ID, "weeklyDeficitValue").text
        fat_text = self.driver.find_element(By.ID, "weeklyFatLossEstimate").text
        self.assertTrue(len(val_text) > 0, "Weekly deficit value should be displayed")
        self.assertIn("كجم", fat_text, "Fat loss estimate should include kg unit")

    def test_09_sodium_potassium_balance_indicator(self):
        """Verify sodium-potassium balance indicator computes ratio and provides text advice."""
        self.driver.execute_script("window.ZATOONA_PHASE4.updateSodiumPotassiumCard();")
        time.sleep(0.2)

        na_text = self.driver.find_element(By.ID, "valTodaySodium").text
        k_text = self.driver.find_element(By.ID, "valTodayPotassium").text
        badge_text = self.driver.find_element(By.ID, "naKRatioBadge").text

        self.assertIn("مجم", na_text)
        self.assertIn("مجم", k_text)
        self.assertTrue(len(badge_text) > 0)

    def test_10_budget_view_daily_allowance_card(self):
        """Verify budget view injects and updates remaining daily spending allowance card."""
        self.driver.execute_script("navigateTo('budget');")
        time.sleep(0.5)

        card = self.driver.find_element(By.ID, "dailyAllowanceCard")
        self.assertIsNotNone(card, "dailyAllowanceCard should be present in budget view")

        allowance_text = self.driver.find_element(By.ID, "valDailyAllowance").text
        self.assertIn("ج.م", allowance_text)

if __name__ == '__main__':
    unittest.main()

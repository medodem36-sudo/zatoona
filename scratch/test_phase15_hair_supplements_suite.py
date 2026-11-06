# -*- coding: utf-8 -*-
import sys
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

class TestPhase15HairAndSupplementsSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        opts = Options()
        opts.add_argument('--headless=new')
        opts.add_argument('--window-size=400,900')
        cls.driver = webdriver.Chrome(options=opts)
        cls.driver.get('file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')
        time.sleep(1.5)
        cls.driver.execute_script("window.alert = function(){};")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.execute_script("window.alert = function(){};")

    # --- 1. LIMITLESS MAN MAX SUPPLEMENT ---
    def test_01_limitless_man_supplement_card_exists(self):
        self.driver.execute_script("navigateTo('meal');")
        time.sleep(0.3)
        card = self.driver.find_element(By.ID, 'cardLimitlessManSupplement')
        self.assertTrue(card.is_displayed(), "Limitless Man Max card should exist in meal view")
        badge = self.driver.find_element(By.ID, 'limitlessManStatusBadge')
        self.assertIn("مُضاف", badge.text, "Initial status should be added to routine")

    def test_02_limitless_man_intake_toggle(self):
        self.driver.execute_script("navigateTo('meal');")
        today = self.driver.execute_script("return window.getTodayIsoSafe();")
        # Toggle intake
        state = self.driver.execute_script("return window.toggleLimitlessTakenToday(true);")
        self.assertTrue(state, "Limitless pill should be marked as taken")
        is_taken = self.driver.execute_script("return window.isLimitlessTakenToday();")
        self.assertTrue(is_taken, "isLimitlessTakenToday should return True")

        btn = self.driver.find_element(By.ID, 'btnCheckLimitlessManToday')
        self.assertIn("تم أخذ الحبة", btn.text, "Button text should indicate tablet taken")

    def test_03_limitless_man_toggle_enable_disable(self):
        self.driver.execute_script("navigateTo('meal');")
        # Disable supplement
        enabled = self.driver.execute_script("return window.toggleLimitlessEnabled(false);")
        self.assertFalse(enabled, "Supplement should be disabled")
        inactive_box = self.driver.find_element(By.ID, 'limitlessManInactiveContent')
        self.assertTrue(inactive_box.is_displayed(), "Inactive content should be visible when disabled")

        # Re-enable
        enabled = self.driver.execute_script("return window.toggleLimitlessEnabled(true);")
        self.assertTrue(enabled, "Supplement should be re-enabled")
        active_box = self.driver.find_element(By.ID, 'limitlessManActiveContent')
        self.assertTrue(active_box.is_displayed(), "Active content should be visible when enabled")

    def test_04_limitless_man_formula_grid_rendered(self):
        self.driver.execute_script("navigateTo('meal');")
        grid = self.driver.find_element(By.ID, 'limitlessManFormulaGrid')
        items = grid.find_elements(By.XPATH, "./div")
        self.assertGreaterEqual(len(items), 20, "Formula grid should render 20+ micronutrient items")

    # --- 2. MEN'S HAIR & GROOMING ROUTINE ---
    def test_05_hair_view_navigation(self):
        self.driver.execute_script("navigateTo('hair');")
        time.sleep(0.3)
        view = self.driver.find_element(By.ID, 'hairView')
        self.assertTrue(view.is_displayed(), "hairView should be displayed after navigateTo('hair')")

        drawer_btn = self.driver.find_element(By.ID, 'drawNav-hair')
        self.assertIn("العناية بالشعر", drawer_btn.get_attribute("textContent"), "Drawer nav button should exist for hair care")

    def test_06_minoxidil_am_pm_toggle(self):
        self.driver.execute_script("navigateTo('hair');")
        # Toggle Morning dose
        am_state = self.driver.execute_script("return window.toggleHairItem('minoxAm', true);")
        self.assertTrue(am_state, "Morning minoxidil should be marked done")
        btn_am = self.driver.find_element(By.ID, 'btnToggleMinoxAm')
        self.assertIn("تم الصباح", btn_am.text, "Button should show morning dose complete")

        # Toggle Evening dose
        pm_state = self.driver.execute_script("return window.toggleHairItem('minoxPm', true);")
        self.assertTrue(pm_state, "Evening minoxidil should be marked done")
        btn_pm = self.driver.find_element(By.ID, 'btnToggleMinoxPm')
        self.assertIn("تم المساء", btn_pm.text, "Button should show evening dose complete")

    def test_07_acretin_routine_and_frequency(self):
        self.driver.execute_script("navigateTo('hair');")
        # Toggle acretin
        acretin_state = self.driver.execute_script("return window.toggleHairItem('acretin', true);")
        self.assertTrue(acretin_state, "Acretin should be marked applied")
        status_text = self.driver.find_element(By.ID, 'acretinStatusText')
        self.assertIn("تم تطبيق أكرتين", status_text.text, "Status should confirm application today")

    def test_08_dermaroller_routine_and_frequency(self):
        self.driver.execute_script("navigateTo('hair');")
        # Toggle dermaroller
        derma_state = self.driver.execute_script("return window.toggleHairItem('dermaroller', true);")
        self.assertTrue(derma_state, "Dermaroller session should be marked complete")
        status_text = self.driver.find_element(By.ID, 'dermarollerStatusText')
        self.assertIn("تمت جلسة الديرمارولر", status_text.text, "Status should confirm session today")

    def test_09_hair_adherence_and_14day_matrix(self):
        self.driver.execute_script("navigateTo('hair');")
        adh_stats = self.driver.execute_script("return window.calculateHairAdherence();")
        self.assertIn('pct', adh_stats, "Adherence stats should include pct")
        self.assertIn('streak', adh_stats, "Adherence stats should include streak")

        table = self.driver.find_element(By.ID, 'hairAdherenceMatrixTable')
        rows = table.find_elements(By.XPATH, ".//tbody/tr")
        self.assertEqual(len(rows), 4, "Matrix should have 4 rows (Minox AM, PM, Acretin, Dermaroller)")

    # --- 3. HIGH-IMPACT TOOLS ---
    def test_10_us_navy_body_fat_calculator(self):
        self.driver.execute_script("navigateTo('gym');")
        card = self.driver.find_element(By.ID, 'cardUSNavyFatCalc')
        self.assertTrue(card is not None, "US Navy Fat Card should exist in gymView")

        # Calculation test (Height 178, Neck 38, Waist 84)
        fat = self.driver.execute_script("return window.calculateUSNavyBodyFat(178, 38, 84);")
        self.assertIsNotNone(fat, "Fat calc should return object")
        self.assertAlmostEqual(fat['fatPct'], 22.2, delta=1.5, msg="Body fat should be around 22%")
        self.assertEqual(fat['category'], "متوسط طبيعي (Average)", "Category should match")

    def test_11_cost_per_protein_calculator(self):
        self.driver.execute_script("navigateTo('meal');")
        card = self.driver.find_element(By.ID, 'cardCostPerProtein')
        self.assertTrue(card is not None, "Cost Per Protein card should exist in mealView")

        items = self.driver.execute_script("return window.calculateCostPerProteinGram();")
        self.assertGreaterEqual(len(items), 4, "Should compare at least 4 Egyptian protein sources")
        self.assertTrue(items[0]['costPerProteinGramEgp'] <= items[-1]['costPerProteinGramEgp'], "Items should be sorted by cheapest per gram")

    def test_12_sleep_tools_sunan_and_visual_hygiene(self):
        self.driver.execute_script("navigateTo('sleep');")
        card_sunan = self.driver.find_element(By.ID, 'cardSunanOfSleep')
        self.assertTrue(card_sunan.is_displayed(), "Sunan of Sleep card should be visible")

        chks = card_sunan.find_elements(By.XPATH, ".//input[@type='checkbox']")
        self.assertEqual(len(chks), 5, "Sunan checklist should contain 5 core sunnahs")

        # Red shift & Eye break functions
        red_shift = self.driver.execute_script("return window.toggleUltraDarkRedShift(true);")
        self.assertTrue(red_shift, "Red shift should activate")
        red_off = self.driver.execute_script("return window.toggleUltraDarkRedShift(false);")
        self.assertFalse(red_off, "Red shift should deactivate")

    def test_13_overview_life_balance_and_screen_waste(self):
        self.driver.execute_script("navigateTo('overview');")
        card_lb = self.driver.find_element(By.ID, 'cardLifeBalanceWheel')
        self.assertTrue(card_lb.is_displayed(), "Life Balance Wheel card should be visible in overview")

        lb = self.driver.execute_script("return window.calculateLifeBalanceScore();")
        self.assertIn('overall', lb, "Life balance should include overall score")
        self.assertGreaterEqual(lb['overall'], 50, "Life balance overall should be valid percentage")

        # Screen waste calculator test
        waste = self.driver.execute_script("return window.calculateScreenTimeWaste(4);")
        self.assertAlmostEqual(waste['daysPerYear'], 60.8, delta=0.5, msg="4 hrs/day should equal ~60.8 days/yr")

if __name__ == '__main__':
    unittest.main()

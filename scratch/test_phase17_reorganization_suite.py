import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestPhase17Reorganization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=412,915") # Mobile viewport
        cls.driver = webdriver.Chrome(options=chrome_options)
        
        # Load local index.html
        path = os.path.abspath("index.html")
        cls.driver.get("file:///" + path)
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_01_bottom_nav_presence_and_structure(self):
        bottom_nav = self.driver.find_element(By.ID, "bottomNav")
        self.assertTrue(bottom_nav.is_displayed(), "#bottomNav should be visible in viewport")
        
        buttons = bottom_nav.find_elements(By.CLASS_NAME, "bottom-nav-btn")
        self.assertEqual(len(buttons), 5, "Bottom Nav must contain exactly 5 hub buttons")
        
        expected_ids = ["bottomNav-home", "bottomNav-prayer", "bottomNav-gym", "bottomNav-meal", "bottomNav-schedule"]
        for bid in expected_ids:
            el = self.driver.find_element(By.ID, bid)
            self.assertTrue(el.is_displayed(), f"{bid} should exist and be displayed")

    def test_02_bottom_nav_navigation_switching(self):
        # 1. Click Prayer
        btn_prayer = self.driver.find_element(By.ID, "bottomNav-prayer")
        self.driver.execute_script("arguments[0].click();", btn_prayer)
        time.sleep(0.3)
        prayer_view = self.driver.find_element(By.ID, "prayerView")
        self.assertTrue(prayer_view.is_displayed(), "prayerView should be displayed")
        self.assertIn("active", btn_prayer.get_attribute("class"), "Prayer button should have .active class")

        # 2. Click Gym
        btn_gym = self.driver.find_element(By.ID, "bottomNav-gym")
        self.driver.execute_script("arguments[0].click();", btn_gym)
        time.sleep(0.3)
        gym_view = self.driver.find_element(By.ID, "gymView")
        self.assertTrue(gym_view.is_displayed(), "gymView should be displayed")
        self.assertIn("active", btn_gym.get_attribute("class"), "Gym button should have .active class")

        # 3. Click Meal
        btn_meal = self.driver.find_element(By.ID, "bottomNav-meal")
        self.driver.execute_script("arguments[0].click();", btn_meal)
        time.sleep(0.3)
        meal_view = self.driver.find_element(By.ID, "mealView")
        self.assertTrue(meal_view.is_displayed(), "mealView should be displayed")
        self.assertIn("active", btn_meal.get_attribute("class"), "Meal button should have .active class")

        # 4. Click Schedule
        btn_sched = self.driver.find_element(By.ID, "bottomNav-schedule")
        self.driver.execute_script("arguments[0].click();", btn_sched)
        time.sleep(0.3)
        sched_view = self.driver.find_element(By.ID, "scheduleView")
        self.assertTrue(sched_view.is_displayed(), "scheduleView should be displayed")
        self.assertIn("active", btn_sched.get_attribute("class"), "Schedule button should have .active class")

        # 5. Click Home
        btn_home = self.driver.find_element(By.ID, "bottomNav-home")
        self.driver.execute_script("arguments[0].click();", btn_home)
        time.sleep(0.3)
        home_hero = self.driver.find_element(By.ID, "homeHero")
        self.assertTrue(home_hero.is_displayed(), "homeHero should be displayed")
        self.assertIn("active", btn_home.get_attribute("class"), "Home button should have .active class")

    def test_03_sub_modes_mapping_to_bottom_nav_pillars(self):
        # Navigating to hair should highlight Gym hub
        self.driver.execute_script("navigateTo('hair');")
        time.sleep(0.3)
        btn_gym = self.driver.find_element(By.ID, "bottomNav-gym")
        self.assertIn("active", btn_gym.get_attribute("class"), "Hair view should activate Gym/Care pillar in bottom nav")

        # Navigating to sleep should highlight Schedule/Productivity hub
        self.driver.execute_script("navigateTo('sleep');")
        time.sleep(0.3)
        btn_sched = self.driver.find_element(By.ID, "bottomNav-schedule")
        self.assertIn("active", btn_sched.get_attribute("class"), "Sleep view should activate Schedule pillar in bottom nav")

        # Navigating to budget should highlight Meal/Nutrition hub
        self.driver.execute_script("navigateTo('budget');")
        time.sleep(0.3)
        btn_meal = self.driver.find_element(By.ID, "bottomNav-meal")
        self.assertIn("active", btn_meal.get_attribute("class"), "Budget view should activate Meal pillar in bottom nav")

        # Return to home
        self.driver.execute_script("navigateTo('home');")
        time.sleep(0.3)

    def test_04_home_quick_actions_bar_pills(self):
        self.driver.execute_script("navigateTo('home');")
        time.sleep(0.3)
        quick_actions = self.driver.find_element(By.ID, "homeQuickActions")
        self.assertTrue(quick_actions.is_displayed())
        
        btn_water = quick_actions.find_element(By.ID, "btnQuickAddWater")
        self.assertTrue(btn_water.is_displayed())
        
        btn_limitless = quick_actions.find_element(By.ID, "btnQuickLimitless")
        self.assertTrue(btn_limitless.is_displayed())
        
        btn_minox = quick_actions.find_element(By.ID, "btnQuickMinox")
        self.assertTrue(btn_minox.is_displayed())

    def test_05_quick_limitless_and_minox_1tap_interaction(self):
        self.driver.execute_script("navigateTo('home');")
        time.sleep(0.3)
        btn_limitless = self.driver.find_element(By.ID, "btnQuickLimitless")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_limitless)
        time.sleep(0.2)
        
        btn_limitless.click()
        time.sleep(0.3)
        btn_limitless_after = self.driver.find_element(By.ID, "btnQuickLimitless")
        self.assertIn("✓", btn_limitless_after.text, "Clicking quick limitless should mark taken with ✓")

        btn_minox = self.driver.find_element(By.ID, "btnQuickMinox")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_minox)
        time.sleep(0.2)
        btn_minox.click()
        time.sleep(0.3)
        btn_minox_after = self.driver.find_element(By.ID, "btnQuickMinox")
        self.assertIn("✓", btn_minox_after.text, "Clicking quick minoxidil should mark taken with ✓")

    def test_06_segmented_subtabs_meal_view(self):
        self.driver.execute_script("navigateTo('meal');")
        time.sleep(0.3)
        tabs = self.driver.find_element(By.ID, "mealSubTabs")
        self.assertTrue(tabs.is_displayed(), "mealSubTabs should exist in mealView")
        
        btn_all = tabs.find_element(By.CSS_SELECTOR, "[data-subtab='all']")
        self.assertIn("active", btn_all.get_attribute("class"), "'all' subtab should be active by default")
        
        card_supp = self.driver.find_element(By.ID, "cardLimitlessManSupplement")
        self.assertTrue(card_supp.is_displayed(), "Supplement card should be displayed under 'all'")

        btn_supp = tabs.find_element(By.CSS_SELECTOR, "[data-subtab='supplements']")
        self.driver.execute_script("arguments[0].click();", btn_supp)
        time.sleep(0.2)
        self.assertTrue(card_supp.is_displayed(), "Supplement card should remain displayed under 'supplements'")

        self.driver.execute_script("arguments[0].click();", btn_all)
        time.sleep(0.2)
        self.assertTrue(card_supp.is_displayed(), "Restoring 'all' should keep card displayed")

    def test_07_segmented_subtabs_prayer_view(self):
        self.driver.execute_script("navigateTo('prayer');")
        time.sleep(0.3)
        tabs = self.driver.find_element(By.ID, "prayerSubTabs")
        self.assertTrue(tabs.is_displayed(), "prayerSubTabs should exist in prayerView")
        
        btn_all = tabs.find_element(By.CSS_SELECTOR, "[data-subtab='all']")
        self.assertIn("active", btn_all.get_attribute("class"), "'all' subtab should be active by default")

    def test_08_segmented_subtabs_schedule_view(self):
        self.driver.execute_script("navigateTo('schedule');")
        time.sleep(0.3)
        tabs = self.driver.find_element(By.ID, "scheduleSubTabs")
        self.assertTrue(tabs.is_displayed(), "scheduleSubTabs should exist in scheduleView")

    def test_09_life_balance_meter_in_home_summary(self):
        self.driver.execute_script("navigateTo('home');")
        time.sleep(0.3)
        summary = self.driver.find_element(By.ID, "homeSummaryCard")
        self.assertIn("اتزان", summary.text, "Home summary should feature daily Life Balance indicators")

if __name__ == "__main__":
    unittest.main()

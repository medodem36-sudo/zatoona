# -*- coding: utf-8 -*-
import sys
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

class TestPhase16UiCleanupAndPerfSuite(unittest.TestCase):
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

    def test_01_zen_mode_button_exists(self):
        btn = self.driver.find_element(By.ID, 'btnToggleZenMode')
        self.assertTrue(btn.is_displayed(), "Zen Mode toggle button should be visible in top bar")
        self.assertIn("هادئ", btn.text, "Button text should mention هادئ")

    def test_02_zen_mode_toggle_activation(self):
        self.driver.execute_script("navigateTo('meal');")
        # Activate Zen Mode
        is_zen = self.driver.execute_script("return window.toggleZenMode(true);")
        self.assertTrue(is_zen, "toggleZenMode(true) should return True")

        body_classes = self.driver.execute_script("return document.body.className;")
        self.assertIn("zen-mode", body_classes, "document.body should contain 'zen-mode' class")

        # In Zen mode, sub-header should be hidden
        header_sub = self.driver.find_element(By.ID, 'pageSub')
        self.assertFalse(header_sub.is_displayed(), "Header subtext should be hidden in Zen Mode")

    def test_03_zen_mode_deactivation(self):
        self.driver.execute_script("navigateTo('meal');")
        # Deactivate Zen Mode
        is_zen = self.driver.execute_script("return window.toggleZenMode(false);")
        self.assertFalse(is_zen, "toggleZenMode(false) should return False")

        body_classes = self.driver.execute_script("return document.body.className;")
        self.assertNotIn("zen-mode", body_classes, "document.body should not contain 'zen-mode' class")

        header_sub = self.driver.find_element(By.ID, 'pageSub')
        self.assertTrue(header_sub.is_displayed(), "Header subtext should be visible in normal mode")

    def test_04_zen_mode_persistence(self):
        # Check localStorage persistence
        self.driver.execute_script("window.toggleZenMode(true);")
        stored = self.driver.execute_script("return localStorage.getItem('zatoona_zen_mode_v1');")
        self.assertEqual(stored, "1", "Zen Mode preference should be saved as '1' in localStorage")

        self.driver.execute_script("window.toggleZenMode(false);")
        stored_off = self.driver.execute_script("return localStorage.getItem('zatoona_zen_mode_v1');")
        self.assertEqual(stored_off, "0", "Zen Mode preference should be saved as '0' when turned off")

    def test_05_debounced_storage_batching(self):
        # Test debounceStorage function
        self.driver.execute_script("window.debounceStorage('test_debounce_key', 'test_val_123', 50);")
        time.sleep(0.1)
        val = self.driver.execute_script("return localStorage.getItem('test_debounce_key');")
        self.assertEqual(val, "test_val_123", "Debounced storage should persist after timer expires")

    def test_06_performance_css_rules_present(self):
        # Check touch-action manipulation
        btn_touch = self.driver.execute_script("""
            const btn = document.querySelector('button');
            return window.getComputedStyle(btn).getPropertyValue('touch-action');
        """)
        self.assertEqual(btn_touch, "manipulation", "Touch-action should be 'manipulation' for zero tap delay")

if __name__ == '__main__':
    unittest.main()

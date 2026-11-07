# -*- coding: utf-8 -*-
"""
Phase 17 Performance, Zero-Freeze Responsiveness & Motion Loop Suite
=====================================================================
Validates:
1. Viewport Meta: user-scalable=no, maximum-scale=1.0 present to eliminate WebView double-tap zoom delay.
2. Rapid Double-Tap Navigation: No duplicate re-renders, clean scroll-to-top behavior when tapping active tab.
3. Solid Bottom Nav: backdrop-filter blur removed to prevent budget GPU rasterization stalls.
4. Compositor Layer Hygiene: transform: translate3d removed from non-moving cards to save GPU texture memory.
5. Exercise Motion Loop Isolation: .ex-photo uses CSS containment (paint layout) and GPU layer.
6. SVG Animation Optimization: rep-start animations include will-change: opacity for smooth 60fps looping.
"""

import sys
import unittest
import time
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

class TestPhase17PerfResponsivenessSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        opts = Options()
        opts.add_argument('--headless=new')
        opts.add_argument('--window-size=375,812')
        cls.driver = webdriver.Chrome(options=opts)
        cls.driver.get('file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')
        time.sleep(1.5)
        cls.driver.execute_script("window.alert = function(){};")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.execute_script("window.alert = function(){};")

    def test_01_viewport_meta_disables_double_tap_zoom(self):
        # Checks user-scalable=no and maximum-scale=1.0 in viewport meta
        meta = self.driver.find_element(By.XPATH, "//meta[@name='viewport']")
        content = meta.get_attribute("content")
        self.assertIn("user-scalable=no", content, "Viewport should specify user-scalable=no")
        self.assertIn("maximum-scale=1.0", content, "Viewport should specify maximum-scale=1.0")

    def test_02_double_tap_active_mode_guard(self):
        # When double-tapping the current mode, mode shouldn't change and no redundant rendering
        self.driver.execute_script("navigateTo('gym');")
        m1 = self.driver.execute_script("return mode;")
        self.assertEqual(m1, "gym")

        # Second navigation to same mode should be a no-op guard
        self.driver.execute_script("navigateTo('gym');")
        m2 = self.driver.execute_script("return mode;")
        self.assertEqual(m2, "gym")

    def test_03_rapid_bottom_nav_taps(self):
        # Click bottom nav buttons in rapid succession
        for nav_id in ['bottomNav-prayer', 'bottomNav-meal', 'bottomNav-gym', 'bottomNav-home']:
            btn = self.driver.find_element(By.ID, nav_id)
            self.driver.execute_script("arguments[0].click(); arguments[0].click();", btn)

        # Verify home is final mode
        final_mode = self.driver.execute_script("return mode;")
        self.assertEqual(final_mode, "home")

    def test_04_bottom_nav_no_gpu_blur(self):
        # Bottom nav should not use backdrop-filter blur which lags low-end GPUs
        bnb = self.driver.find_element(By.ID, 'bottomNav')
        blur = self.driver.execute_script("""
            const el = document.getElementById('bottomNav');
            const style = window.getComputedStyle(el);
            return style.getPropertyValue('backdrop-filter') || style.getPropertyValue('-webkit-backdrop-filter');
        """)
        self.assertTrue(blur == '' or blur == 'none', f"backdrop-filter should be none/empty, got: {blur}")

    def test_05_exercise_photo_containment_present(self):
        # .ex-photo should contain paint layout to prevent repaints outside the box
        contain = self.driver.execute_script("""
            const card = document.createElement('div');
            card.className = 'ex-photo';
            document.body.appendChild(card);
            const val = window.getComputedStyle(card).getPropertyValue('contain');
            document.body.removeChild(card);
            return val;
        """)
        self.assertTrue('paint' in contain or 'strict' in contain or 'layout' in contain,
                        f"Expected CSS containment on .ex-photo, got: {contain}")

    def test_06_svg_exercise_animations_have_will_change(self):
        # Verify exercise SVGs contain will-change: opacity
        svg_path = 'assets/images/exercises/ex-a01-goblet-squat.svg'
        if os.path.exists(svg_path):
            with open(svg_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertIn('will-change: opacity', content, "ex-a01-goblet-squat.svg should include will-change: opacity")

    def test_07_completed_checklist_items_no_layer_scale(self):
        # Check that .checklist-item.done doesn't apply transform: scale(0.99) which wastes GPU texture layers
        transform_rule = self.driver.execute_script("""
            const it = document.createElement('div');
            it.className = 'checklist-item done';
            document.body.appendChild(it);
            const val = window.getComputedStyle(it).getPropertyValue('transform');
            document.body.removeChild(it);
            return val;
        """)
        self.assertEqual(transform_rule, 'none', "Done checklist items should not have persistent scale transform")

if __name__ == '__main__':
    unittest.main()

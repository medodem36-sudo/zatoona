import sys
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

class TestPackageGFluidUX(unittest.TestCase):
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

    def test_01_view_pager_navigation(self):
        # Test navigation to next section
        next_sec = self.driver.execute_script("return window.navigateToNextSection();")
        self.assertIsNotNone(next_sec, "Should return next section name")

        # Test toggle swipe navigation
        state = self.driver.execute_script("return window.toggleSwipeNavigation(false);")
        self.assertFalse(state, "Swipe nav should be disabled")
        state_on = self.driver.execute_script("return window.toggleSwipeNavigation(true);")
        self.assertTrue(state_on, "Swipe nav should be re-enabled")

    def test_02_card_swipe_simulation(self):
        # Create a test element and simulate card swipe
        is_done = self.driver.execute_script("""
            const testEl = document.createElement('div');
            testEl.className = 'check-item';
            document.body.appendChild(testEl);
            window.simulateCardSwipe(testEl, 'right');
            const res = testEl.classList.contains('done');
            testEl.remove();
            return res;
        """)
        self.assertTrue(is_done, "simulateCardSwipe('right') should mark item as done")

    def test_03_shared_element_morph(self):
        morphed = self.driver.execute_script("""
            const testEl = document.createElement('div');
            testEl.className = 'card';
            document.body.appendChild(testEl);
            window.triggerSharedElementMorph(testEl);
            const hasClass = testEl.classList.contains('shared-element-expand');
            testEl.remove();
            return hasClass;
        """)
        self.assertTrue(morphed, "triggerSharedElementMorph should apply expansion animation class")

    def test_04_natural_language_quick_add(self):
        # Test parsing Egyptian Arabic sentence 1
        res1 = self.driver.execute_script("""
            return window.parseNaturalLanguageScheduleInput('مذاكرة فارما بكره ٤ العصر ٦٠ دقيقة');
        """)
        self.assertIn("مذاكرة فارما", res1['title'], "Title should contain مذاكرة فارما")
        self.assertEqual(res1['time'], "16:00", "4 العصر should be parsed to 16:00")
        self.assertEqual(res1['durationMinutes'], 60, "Duration should be 60 minutes")

        # Test parsing Egyptian Arabic sentence 2
        res2 = self.driver.execute_script("""
            return window.parseNaturalLanguageScheduleInput('تمرين جيم النهاردة ٥ المغرب ٣٠ دقيقة');
        """)
        self.assertIn("تمرين جيم", res2['title'], "Title should contain تمرين جيم")
        self.assertEqual(res2['time'], "17:00", "5 المغرب should be parsed to 17:00")
        self.assertEqual(res2['durationMinutes'], 30, "Duration should be 30 minutes")

    def test_05_dynamic_status_capsule(self):
        capsule = self.driver.find_element(By.ID, 'dynamicStatusCapsule')
        self.assertTrue(capsule.is_displayed(), "Dynamic status capsule should be visible at top")

        content = self.driver.find_element(By.ID, 'capsuleLiveContent')
        self.assertTrue(len(content.text) > 0, "Capsule live content should have non-empty text")

    def test_06_collapsible_sticky_header(self):
        # Trigger header scroll update
        self.driver.execute_script("window.scrollTo(0, 150); window.dispatchEvent(new Event('scroll'));")
        time.sleep(0.2)
        # Scroll back
        self.driver.execute_script("window.scrollTo(0, 0); window.dispatchEvent(new Event('scroll'));")

    def test_07_contextual_pull_to_refresh(self):
        indicator = self.driver.find_element(By.ID, 'pullToRefreshIndicator')
        self.assertIsNotNone(indicator, "pullToRefreshIndicator element should exist in DOM")

        # Trigger programmatic refresh
        self.driver.execute_script("window.triggerPullToRefresh();")
        time.sleep(0.3)
        self.assertTrue(indicator.is_displayed() or 'visible' in indicator.get_attribute('class'),
                        "Indicator should become visible on pull to refresh")

    def test_08_accordion_fold_unfold(self):
        # Toggle all cards collapsed
        is_collapsed = self.driver.execute_script("return window.toggleAccordionAll();")
        self.assertTrue(is_collapsed, "Cards should be collapsed")

        # Toggle all cards expanded back
        is_expanded = self.driver.execute_script("return window.toggleAccordionAll();")
        self.assertFalse(is_expanded, "Cards should be restored to expanded")

    def test_09_spotlight_dimming(self):
        dim_check = self.driver.execute_script("""
            const p = document.createElement('div');
            const c1 = document.createElement('div');
            const c2 = document.createElement('div');
            p.appendChild(c1);
            p.appendChild(c2);
            document.body.appendChild(p);

            window.setSpotlightTask(c1);
            const res = c1.classList.contains('spotlight-active') && c2.classList.contains('spotlight-dimmed');
            window.clearSpotlight();
            p.remove();
            return res;
        """)
        self.assertTrue(dim_check, "Target should have spotlight-active and sibling spotlight-dimmed")

    def test_10_pinch_to_zoom_font_scale(self):
        scale = self.driver.execute_script("return window.setFontScalePercentage(115);")
        self.assertEqual(scale, 115, "Font scale should be set to 115%")

        saved = self.driver.execute_script("return window.getFontScalePercentage();")
        self.assertEqual(saved, 115, "getFontScalePercentage should return 115%")

        # Reset cleanly
        self.driver.execute_script("window.setFontScalePercentage(100);")

    def test_11_border_aura_glow(self):
        aura = self.driver.find_element(By.ID, 'appBorderAura')
        self.assertIsNotNone(aura, "appBorderAura element should exist in DOM")

        res = self.driver.execute_script("return window.updateBorderAuraGlow(85);")
        self.assertEqual(res['percent'], 85, "Aura glow should calculate 85% completion")
        self.assertGreater(res['spread'], 5, "Spread should be greater than 5px at 85%")

    def test_12_time_aware_adaptive_dashboard(self):
        morn = self.driver.execute_script("return window.applyTimeAwareAdaptiveDashboard(8);")
        self.assertEqual(morn['period'], 'morning', "8:00 should be morning")

        aft = self.driver.execute_script("return window.applyTimeAwareAdaptiveDashboard(14);")
        self.assertEqual(aft['period'], 'afternoon', "14:00 should be afternoon")

        eve = self.driver.execute_script("return window.applyTimeAwareAdaptiveDashboard(21);")
        self.assertEqual(eve['period'], 'evening', "21:00 should be evening")

if __name__ == '__main__':
    unittest.main()

import sys
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

class TestPackageFNotesAndroid(unittest.TestCase):
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

    def test_01_feature_71_pin_notes(self):
        # Test pinning a note
        is_pinned = self.driver.execute_script("""
            window.togglePinNote('unit_test_note_key_1');
            return window.isNotePinned('unit_test_note_key_1');
        """)
        self.assertTrue(is_pinned, "Note should be pinned")

        # Test unpinning
        is_unpinned = self.driver.execute_script("""
            window.togglePinNote('unit_test_note_key_1');
            return window.isNotePinned('unit_test_note_key_1');
        """)
        self.assertFalse(is_unpinned, "Note should be unpinned")

    def test_02_feature_71_color_notes(self):
        # Set emerald color
        color = self.driver.execute_script("""
            window.setNoteColor('unit_test_note_key_2', '#10b981');
            return window.getNoteColor('unit_test_note_key_2');
        """)
        self.assertEqual(color, '#10b981', "Note color should be #10b981")

        # Clear color
        cleared = self.driver.execute_script("""
            window.setNoteColor('unit_test_note_key_2', null);
            return window.getNoteColor('unit_test_note_key_2');
        """)
        self.assertIsNone(cleared, "Note color should be cleared (null)")

    def test_03_feature_73_checklist_mode(self):
        # Toggle checklist mode on
        is_chk = self.driver.execute_script("""
            window.toggleNoteChecklistMode('unit_test_chk_note');
            return window.isNoteChecklistMode('unit_test_chk_note');
        """)
        self.assertTrue(is_chk, "Note checklist mode should be active")

        # Render checklist HTML
        html = self.driver.execute_script("""
            return window.renderNoteChecklistHtml('unit_test_chk_note', 'Item 1\\nItem 2');
        """)
        self.assertIn("type=\"checkbox\"", html, "Checklist HTML should contain checkbox inputs")
        self.assertIn("Item 1", html, "Checklist should contain Item 1")

        # Check line item
        self.driver.execute_script("window.toggleNoteChecklistItem('unit_test_chk_note', 0);")
        state = self.driver.execute_script("return window.getNoteChecklistState('unit_test_chk_note');")
        self.assertIn(0, state['checkedIndices'], "Index 0 should be marked checked")

    def test_04_feature_81_led_flash_alert(self):
        # Toggle flash alarm setting
        en = self.driver.execute_script("""
            window.toggleFlashAlarm(true);
            return window.isFlashAlarmEnabled();
        """)
        self.assertTrue(en, "Flash alarm should be enabled")

        # Trigger flash alert
        res = self.driver.execute_script("return window.triggerLedFlashAlert(500, 2);")
        self.assertIn("ok", res, "triggerLedFlashAlert should return status ok")

        # Verify flash overlay exists
        overlay = self.driver.find_element(By.ID, 'screenFlashOverlay')
        self.assertIsNotNone(overlay, "screenFlashOverlay element should exist in DOM")

    def test_05_feature_85_wake_lock(self):
        # Request wake lock
        active = self.driver.execute_script("""
            return window.toggleWakeLock();
        """)
        time.sleep(0.2)
        is_active = self.driver.execute_script("return window.isWakeLockActive();")
        self.assertTrue(is_active, "Wake lock should be active after toggle")

        # Release wake lock
        self.driver.execute_script("return window.toggleWakeLock();")
        time.sleep(0.2)
        is_inactive = self.driver.execute_script("return window.isWakeLockActive();")
        self.assertFalse(is_inactive, "Wake lock should be inactive after second toggle")

    def test_06_feature_86_custom_haptic_patterns(self):
        prayer_pat = self.driver.execute_script("return window.triggerCustomHaptic('prayer');")
        self.assertEqual(prayer_pat, [150, 100, 150, 100, 300], "Prayer haptic pattern should match")

        gym_pat = self.driver.execute_script("return window.triggerCustomHaptic('gym_timer');")
        self.assertEqual(gym_pat, [100, 80, 100, 80, 200], "Gym timer haptic pattern should match")

        water_pat = self.driver.execute_script("return window.triggerCustomHaptic('water');")
        self.assertEqual(water_pat, [80, 60, 80], "Water haptic pattern should match")

        danger_pat = self.driver.execute_script("return window.triggerCustomHaptic('danger');")
        self.assertEqual(danger_pat, [300, 100, 300, 100, 400], "Danger haptic pattern should match")

    def test_07_feature_88_all_in_one_widget(self):
        summary = self.driver.execute_script("return window.buildAllInOneDailySummary();")
        self.assertIn('nextPrayerName', summary, "Summary should have nextPrayerName")
        self.assertIn('workoutDayName', summary, "Summary should have workoutDayName")
        self.assertIn('waterLitersToday', summary, "Summary should have waterLitersToday")

        res = self.driver.execute_script("return window.syncAllInOneWidgetData();")
        self.assertIn('ok', res, "syncAllInOneWidgetData should return status ok")

    def test_08_feature_90_amoled_ultra_battery_saver(self):
        # Enable AMOLED mode
        active = self.driver.execute_script("""
            window.toggleAmoledMode(true);
            return window.isAmoledModeActive();
        """)
        self.assertTrue(active, "AMOLED mode should be active")

        has_class = self.driver.execute_script("return document.body.classList.contains('amoled-battery-saver');")
        self.assertTrue(has_class, "body should have 'amoled-battery-saver' class")

        # Disable AMOLED mode
        self.driver.execute_script("window.toggleAmoledMode(false);")
        has_class_after = self.driver.execute_script("return document.body.classList.contains('amoled-battery-saver');")
        self.assertFalse(has_class_after, "body should not have 'amoled-battery-saver' class after disable")

if __name__ == '__main__':
    unittest.main()

import sys
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

class TestPackageEScheduleTasks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        opts = Options()
        opts.add_argument('--headless=new')
        opts.add_argument('--window-size=400,900')
        cls.driver = webdriver.Chrome(options=opts)
        cls.driver.get('file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')
        time.sleep(1.5)
        # Suppress alerts
        cls.driver.execute_script("window.alert = function(){};")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.execute_script("window.alert = function(){};")

    def test_01_feature_42_sunlight_logger(self):
        self.driver.execute_script("navigateTo('sleep');")
        time.sleep(0.3)
        card = self.driver.find_element(By.ID, 'morningSunlightCard')
        self.assertTrue(card.is_displayed(), "Morning Sunlight card should be visible in sleep view")

        timer_disp = self.driver.find_element(By.ID, 'sunlightTimerDisplay')
        self.assertEqual(timer_disp.text.strip(), "15:00", "Default timer should be 15:00")

        # Test logging a 15-min sunlight session for today
        today_iso = self.driver.execute_script("return typeof window.getTodayIsoSafe === 'function' ? window.getTodayIsoSafe() : new Date().toISOString().slice(0, 10);")
        logged = self.driver.execute_script(f"""
            window.logSunlightSession(15, '{today_iso}');
            return window.isSunlightLoggedToday('{today_iso}');
        """)
        self.assertTrue(logged, "isSunlightLoggedToday should return True after logging")

        badge = self.driver.find_element(By.ID, 'sunlightStreakBadge')
        self.assertIn("15", badge.text, "Badge should display recorded minutes")

    def test_02_feature_44_stop_fluids_reminder(self):
        self.driver.execute_script("navigateTo('sleep');")
        card = self.driver.find_element(By.ID, 'stopFluidsCard')
        self.assertTrue(card.is_displayed(), "Stop fluids card should be visible in sleep view")

        cutoff = self.driver.execute_script("return window.calculateStopFluidsCutoff('23:00');")
        self.assertEqual(cutoff['time24'], "21:00", "23:00 minus 2hrs should be 21:00")
        self.assertIn("9:00", cutoff['time12'], "12-hr format should be 9:00")

        # Midnight rollover test (01:00 - 2hrs = 23:00)
        rollover = self.driver.execute_script("return window.calculateStopFluidsCutoff('01:00');")
        self.assertEqual(rollover['time24'], "23:00", "01:00 minus 2hrs should wrap around to 23:00")

        # Toggle reminder
        toggled = self.driver.execute_script("return window.toggleStopFluidsReminder(true);")
        self.assertTrue(toggled, "Reminder should be enabled")

    def test_03_feature_56_mandatory_stretch_break(self):
        self.driver.execute_script("navigateTo('study');")
        time.sleep(0.3)
        btn = self.driver.find_element(By.ID, 'btnStudyQuickStretch')
        self.assertTrue(btn.is_displayed(), "Quick stretch button should be visible in study view")

        # Test trigger modal after 2 pomodoros
        due = self.driver.execute_script("return window.triggerStretchBreakIfDue(2);")
        self.assertTrue(due, "Stretch break should be due on 2nd pomodoro")

        modal = self.driver.find_element(By.ID, 'modalStretchBreak')
        self.assertEqual(modal.value_of_css_property('display'), 'flex', "Stretch modal should be displayed")

        # Complete stretch break
        self.driver.execute_script("window.completeStretchBreak();")
        self.assertEqual(modal.value_of_css_property('display'), 'none', "Modal should close on completion")

        count = self.driver.execute_script("return window.getStretchBreakCount();")
        self.assertGreaterEqual(count, 1, "Stretch break count should be at least 1")

    def test_04_feature_61_visual_time_blocking(self):
        self.driver.execute_script("navigateTo('schedule');")
        time.sleep(0.3)
        card = self.driver.find_element(By.ID, 'visualTimeBlockingCard')
        self.assertTrue(card.is_displayed(), "Visual time blocking card should be visible in schedule view")

        slots = self.driver.execute_script("return window.generateTimeBlockSlots();")
        self.assertEqual(len(slots), 24, "Should generate exactly 24 hour slots")

        grid_items = self.driver.find_elements(By.CSS_SELECTOR, '#timeBlockingGrid .tb-slot')
        self.assertEqual(len(grid_items), 24, "Grid should render 24 slot elements")

        # Verify category slot exists (worship, gym, study, sleep)
        types = [s['type'] for s in slots]
        self.assertIn('sleep', types, "Slots should contain sleep blocks")
        self.assertIn('worship', types, "Slots should contain worship blocks")
        self.assertIn('gym', types, "Slots should contain gym blocks")

    def test_05_feature_62_task_carry_over(self):
        self.driver.execute_script("navigateTo('schedule');")
        btn = self.driver.find_element(By.ID, 'btnCarryOverTasks')
        self.assertTrue(btn.is_displayed(), "Carry-over button should be visible in schedule view")

        res = self.driver.execute_script("return window.carryOverIncompleteTasks('2026-11-04', '2026-11-05');")
        self.assertGreater(res['carriedCount'], 0, "Should carry over at least 1 incomplete task")
        self.assertEqual(res['targetIso'], '2026-11-05', "Target date should be tomorrow")

    def test_06_feature_64_time_accuracy(self):
        self.driver.execute_script("navigateTo('schedule');")
        card = self.driver.find_element(By.ID, 'scheduleTimeAccuracyCard')
        self.assertTrue(card.is_displayed(), "Time accuracy card should be visible in schedule view")

        # Seed custom task tracking
        self.driver.execute_script("""
            window.setTaskTimeEstimate('task_acc_test', 60, '2026-11-04');
            window.setTaskTimeActual('task_acc_test', 60, '2026-11-04');
        """)
        stats = self.driver.execute_script("return window.calculateScheduleTimeAccuracy('2026-11-04');")
        self.assertEqual(stats['accuracyPercent'], 100, "100% accuracy expected when est == act")

    def test_07_feature_65_subtasks_tree(self):
        # Add subtasks and check progress
        res = self.driver.execute_script("""
            const tId = 'task_sub_unit_1';
            const s1 = window.addSubtask(tId, 'Step 1: Research');
            const s2 = window.addSubtask(tId, 'Step 2: Implement');
            window.toggleSubtask(tId, s1.id);
            return window.calculateSubtaskProgress(tId);
        """)
        self.assertEqual(res['total'], 2, "Should have 2 subtasks total")
        self.assertEqual(res['done'], 1, "Should have 1 completed subtask")
        self.assertEqual(res['percent'], 50, "Should be 50% completed")

        # Open and close modal
        self.driver.execute_script("window.openSubtasksModal('task_sub_unit_1', 'Main Task');")
        modal = self.driver.find_element(By.ID, 'modalSubtasks')
        self.assertEqual(modal.value_of_css_property('display'), 'flex', "Subtasks modal should open")
        self.driver.execute_script("window.closeSubtasksModal();")
        self.assertEqual(modal.value_of_css_property('display'), 'none', "Subtasks modal should close")

    def test_08_feature_66_complex_recurring_tasks(self):
        self.driver.execute_script("navigateTo('schedule');")
        card = self.driver.find_element(By.ID, 'complexRecurringTasksCard')
        self.assertTrue(card.is_displayed(), "Complex recurring tasks card should be visible")

        tasks = self.driver.execute_script("return window.getComplexRecurringTasks();")
        self.assertGreaterEqual(len(tasks), 1, "Should have default recurring tasks")

        # Test Friday match
        # 2026-11-06 is Friday (getDay() == 5)
        friday_tasks = self.driver.execute_script("return window.getRecurringTasksForDate('2026-11-06');")
        titles = [t['title'] for t in friday_tasks]
        self.assertTrue(any('سورة الكهف' in t for t in titles), "Friday should match Friday recurring tasks")

    def test_09_feature_68_time_to_leave(self):
        self.driver.execute_script("navigateTo('schedule');")
        card = self.driver.find_element(By.ID, 'timeToLeaveCard')
        self.assertTrue(card.is_displayed(), "Time-to-leave card should be visible")

        # Calculate departure: 10:00 appointment - 30m travel - 15m buffer = 09:15
        calc = self.driver.execute_script("return window.calculateTimeToLeave('10:00', 30, 15);")
        self.assertEqual(calc['leaveTime24'], "09:15", "10:00 - 45m should be 09:15")
        self.assertIn("9:15", calc['leaveTime12'], "12-hr format should have 9:15")

        # Save and render UI
        self.driver.execute_script("""
            window.saveTimeToLeaveEvent({
                title: 'محاضرة الكلية',
                time: '10:00',
                travel: 30,
                buffer: 15
            });
        """)
        disp = self.driver.find_element(By.ID, 'ttlResultDisplay')
        self.assertTrue(disp.is_displayed(), "Result display should be visible after saving")
        self.assertIn("9:15", disp.text, "Result should show calculated departure time")

    def test_10_feature_97_conflict_detector(self):
        self.driver.execute_script("navigateTo('schedule');")
        card = self.driver.find_element(By.ID, 'scheduleConflictCard')
        self.assertTrue(card.is_displayed(), "Conflict card should be visible")

        # Test conflict detection algorithm
        conflicts = self.driver.execute_script("""
            return window.detectScheduleConflicts([
                { id: '1', title: 'مذاكرة مركزة', start: '09:00', dur: 120 },
                { id: '2', title: 'مشوار الكلية', start: '10:30', dur: 60 }
            ]);
        """)
        self.assertEqual(len(conflicts), 1, "Should detect exactly 1 conflict")
        self.assertEqual(conflicts[0]['overlapMinutes'], 30, "Overlap should be 30 minutes")
        self.assertIn('اقتراح', conflicts[0]['suggestion'], "Suggestion should be generated")

if __name__ == '__main__':
    unittest.main()

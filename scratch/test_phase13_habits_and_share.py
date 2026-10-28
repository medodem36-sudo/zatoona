"""
Automated Acceptance Test Suite: Custom Daily Habits & Skills Learning Tracker + Social Accountability Card
Phase 13.9: Daily Habits Acquisition, Skill Learning Tracker, Streaks, and Daily Summary Share Card (Proposal #13)
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

passed_count = 0
failed_count = 0

def test(name, condition, details=""):
    global passed_count, failed_count
    if condition:
        print(f"  [PASS] {name}")
        passed_count += 1
    else:
        print(f"  [FAIL] {name} - {details}")
        failed_count += 1

def run_tests():
    global passed_count, failed_count
    print("=" * 80)
    print("PHASE 13.9 ACCEPTANCE TEST SUITE: HABITS & LEARNING TRACKER + SHARE CARD")
    print("=" * 80)

    html_path = os.path.abspath('index.html')
    file_url = 'file:///' + html_path.replace('\\', '/')

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--window-size=375,812')

    driver = webdriver.Chrome(options=opts)
    driver.get(file_url)
    time.sleep(1.0)

    def js(script):
        return driver.execute_script(script)

    try:
        # Group 1: DOM Elements & Functions Presence
        print("\n--- Group 1: DOM Elements & Functions Presence ---")
        dom_check = js("""
            return {
                hasHabitsContainer: !!document.getElementById('customHabitsContainer'),
                hasShareCard: !!document.getElementById('dailyShareCard'),
                hasLoadList: typeof window.loadCustomHabitsList === 'function',
                hasAddHabit: typeof window.addCustomHabit === 'function',
                hasDeleteHabit: typeof window.deleteCustomHabit === 'function',
                hasToggleHabit: typeof window.toggleCustomHabit === 'function',
                hasComputeStreak: typeof window.computeCustomHabitStreak === 'function',
                hasRenderTracker: typeof window.renderCustomHabitsTracker === 'function',
                hasGenSummary: typeof window.generateDailySummaryText === 'function',
                hasRenderShare: typeof window.renderDailySummaryShareCard === 'function'
            };
        """)

        test("#customHabitsContainer exists in DOM", dom_check.get('hasHabitsContainer'))
        test("#dailyShareCard exists in DOM", dom_check.get('hasShareCard'))
        test("window.loadCustomHabitsList is a function", dom_check.get('hasLoadList'))
        test("window.addCustomHabit is a function", dom_check.get('hasAddHabit'))
        test("window.deleteCustomHabit is a function", dom_check.get('hasDeleteHabit'))
        test("window.toggleCustomHabit is a function", dom_check.get('hasToggleHabit'))
        test("window.computeCustomHabitStreak is a function", dom_check.get('hasComputeStreak'))
        test("window.renderCustomHabitsTracker is a function", dom_check.get('hasRenderTracker'))
        test("window.generateDailySummaryText is a function", dom_check.get('hasGenSummary'))
        test("window.renderDailySummaryShareCard is a function", dom_check.get('hasRenderShare'))

        # Group 2: Habit List CRUD Operations
        print("\n--- Group 2: Habit List CRUD Operations ---")
        crud_check = js("""
            const initialList = window.loadCustomHabitsList();
            const initialCount = initialList.length;

            // Add a new learning skill
            const added = window.addCustomHabit('تعلّم لغة ألمانية', 'learning', '٢٠ دقيقة');
            const afterAddList = window.loadCustomHabitsList();
            const foundAdded = afterAddList.find(h => h.id === added.id);

            // Delete the added habit
            window.deleteCustomHabit(added.id);
            const afterDelList = window.loadCustomHabitsList();
            const foundDeleted = afterDelList.find(h => h.id === added.id);

            return {
                hasDefaults: initialCount > 0,
                addedTitle: foundAdded ? foundAdded.title : null,
                addedType: foundAdded ? foundAdded.type : null,
                addedTarget: foundAdded ? foundAdded.target : null,
                isDeleted: !foundDeleted
            };
        """)

        test("Habits list initializes with default starter habits", crud_check.get('hasDefaults'))
        test("addCustomHabit saves title accurately", crud_check.get('addedTitle') == 'تعلّم لغة ألمانية')
        test("addCustomHabit sets type as learning", crud_check.get('addedType') == 'learning')
        test("addCustomHabit sets target correctly", crud_check.get('addedTarget') == '٢٠ دقيقة')
        test("deleteCustomHabit removes habit from list", crud_check.get('isDeleted') is True)

        # Group 3: Daily Progress & Habit Streaks Calculation
        print("\n--- Group 3: Daily Progress & Habit Streaks Calculation ---")
        streak_check = js("""
            const testId = 'test_habit_streak';
            const testDates = ['2026-11-01', '2026-11-02', '2026-11-03'];

            // Seed 3 consecutive completed days
            testDates.forEach(d => {
                const s = {};
                s[testId] = { done: true };
                window.saveDailyCustomHabits(d, s);
            });

            // Calculate streak at day 3
            const streakAtDay3 = window.computeCustomHabitStreak(testId, '2026-11-03');

            // Toggle day 2 off
            window.toggleCustomHabit(testId, '2026-11-02');
            const afterToggleDay2 = window.loadDailyCustomHabits('2026-11-02')[testId].done;

            // Cleanup
            testDates.forEach(d => {
                localStorage.removeItem('meal-gym-tracker:customhabits:' + d);
            });

            return {
                streak3: streakAtDay3.currentStreak,
                totalDone: streakAtDay3.totalDone,
                toggledOff: afterToggleDay2 === false
            };
        """)

        test("computeCustomHabitStreak calculates consecutive streak (3 days)", streak_check.get('streak3') == 3)
        test("computeCustomHabitStreak counts total completed days", streak_check.get('totalDone') == 3)
        test("toggleCustomHabit flips done state cleanly", streak_check.get('toggledOff') is True)

        # Group 4: Daily Summary Text & Social Accountability Card
        print("\n--- Group 4: Daily Summary Text & Social Accountability Card ---")
        summary_check = js("""
            const testIso = '2026-11-05';
            
            // Seed test prayer
            localStorage.setItem('meal-gym-tracker:prayer:' + testIso, JSON.stringify({
                fajr: { fard: true, sunnah: true },
                dhuhr: { fard: true, sunnah: false },
                asr: { fard: true, sunnah: false },
                maghrib: { fard: true, sunnah: true },
                isha: { fard: true, sunnah: false }
            }));

            // Seed fasting
            window.saveFasting(testIso, { fasted: true, type: 'sunnah' });

            // Seed water
            localStorage.setItem('meal-gym-tracker:water:' + testIso, '8');

            const text = window.generateDailySummaryText(testIso);

            // Cleanup
            localStorage.removeItem('meal-gym-tracker:prayer:' + testIso);
            localStorage.removeItem('meal-gym-tracker:fasting:' + testIso);
            localStorage.removeItem('meal-gym-tracker:water:' + testIso);

            return {
                hasDate: text.includes('2026-11-05'),
                hasFard: text.includes('5/5'),
                hasSunnah: text.includes('السنن: 2'),
                hasFasting: text.includes('صائم اليوم'),
                hasWater: text.includes('8/8'),
                hasSignature: text.includes('زيتونة')
            };
        """)

        test("Daily summary text includes ISO date", summary_check.get('hasDate'))
        test("Daily summary text reflects 5/5 Fard prayers", summary_check.get('hasFard'))
        test("Daily summary text reflects Sunnah count", summary_check.get('hasSunnah'))
        test("Daily summary text includes fasting status", summary_check.get('hasFasting'))
        test("Daily summary text includes water intake", summary_check.get('hasWater'))
        test("Daily summary text includes Zatoona signature", summary_check.get('hasSignature'))

        # Group 5: UI Integration in Schedule & Overview
        print("\n--- Group 5: UI Integration in Schedule & Overview ---")
        ui_check = js("""
            // 1. Schedule View
            window.routeNotificationClick({ mode: 'schedule' });
            window.renderCustomHabitsTracker();
            const habitsCard = document.getElementById('customHabitsContainer');
            const hasAddBtn = !!document.getElementById('btnToggleAddHabit');

            // 2. Overview View
            window.routeNotificationClick({ mode: 'overview' });
            window.renderDailySummaryShareCard();
            const shareCard = document.getElementById('dailyShareCard');
            const hasCopyBtn = !!document.getElementById('btnCopyDailySummary');
            const hasShareBtn = !!document.getElementById('btnShareDailySummary');

            return {
                habitsCardPopulated: !!habitsCard && habitsCard.innerHTML.length > 50,
                hasAddBtn,
                shareCardPopulated: !!shareCard && shareCard.innerHTML.length > 50,
                hasCopyBtn,
                hasShareBtn
            };
        """)

        test("Habits tracker renders inside schedule view", ui_check.get('habitsCardPopulated'))
        test("#btnToggleAddHabit exists in habits tracker", ui_check.get('hasAddBtn'))
        test("Daily summary card renders inside overview view", ui_check.get('shareCardPopulated'))
        test("#btnCopyDailySummary button exists in share card", ui_check.get('hasCopyBtn'))
        test("#btnShareDailySummary button exists in share card", ui_check.get('hasShareBtn'))

    finally:
        driver.quit()

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 80)

    if failed_count > 0:
        sys.exit(1)

if __name__ == '__main__':
    run_tests()

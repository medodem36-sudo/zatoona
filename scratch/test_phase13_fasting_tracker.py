"""
Automated Acceptance Test Suite: Fasting Tracker & Sunnah Days (Roadmap Proposal #12)
Phase 13.6B: Voluntary & Sunnah Fasting Tracker in Worship View (صيام التطوع والسنن والقضاء)
Tests DOM elements, date-specific persistence, fasting types, monthly count, and Sunnah day alerts.
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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
    print("PHASE 13.6B ACCEPTANCE TEST SUITE: FASTING TRACKER & SUNNAH DAYS (صيام التطوع)")
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
        # Group 1: DOM Elements & Functions
        print("\n--- Group 1: DOM Elements & Functions ---")
        dom_check = js("""
            return {
                hasCard: !!document.getElementById('fastingCard'),
                hasBadge: !!document.getElementById('badge-fasting'),
                hasLoadFasting: typeof window.loadFasting === 'function',
                hasSaveFasting: typeof window.saveFasting === 'function',
                hasRenderFasting: typeof window.renderFasting === 'function',
                hasCountMonthlyFasts: typeof window.countMonthlyFasts === 'function'
            };
        """)

        test("#fastingCard exists in DOM", dom_check.get('hasCard'))
        test("#badge-fasting exists in DOM", dom_check.get('hasBadge'))
        test("window.loadFasting is a function", dom_check.get('hasLoadFasting'))
        test("window.saveFasting is a function", dom_check.get('hasSaveFasting'))
        test("window.renderFasting is a function", dom_check.get('hasRenderFasting'))
        test("window.countMonthlyFasts is a function", dom_check.get('hasCountMonthlyFasts'))

        # Group 2: Fasting Toggle & Type Selection
        print("\n--- Group 2: Fasting Toggle & Type Selection ---")
        toggle_res = js("""
            const testIso = '2026-11-02'; // A Monday
            window.saveFasting(testIso, { fasted: true, type: 'sunnah', note: 'صيام الإثنين' });
            const loaded = window.loadFasting(testIso);
            
            // Unfasted date
            const unfasted = window.loadFasting('2026-11-03');
            
            return {
                fasted: loaded.fasted,
                type: loaded.type,
                note: loaded.note,
                unfastedState: unfasted.fasted
            };
        """)

        test("Fasting state saves and loads correctly", toggle_res.get('fasted') is True)
        test("Fasting type is recorded accurately", toggle_res.get('type') == 'sunnah')
        test("Fasting optional note is saved", toggle_res.get('note') == 'صيام الإثنين')
        test("Unfasted days default to fasted: false", toggle_res.get('unfastedState') is False)

        # Group 3: Monthly Fasting Calculations
        print("\n--- Group 3: Monthly Fasting Calculations ---")
        count_res = js("""
            const testMonth = '2026-11';
            // Save 3 fasts in November
            window.saveFasting('2026-11-02', { fasted: true, type: 'sunnah' });
            window.saveFasting('2026-11-05', { fasted: true, type: 'sunnah' });
            window.saveFasting('2026-11-12', { fasted: true, type: 'qadaa' });
            // Save 1 fast in December (should NOT count for November)
            window.saveFasting('2026-12-01', { fasted: true, type: 'sunnah' });

            const novCount = window.countMonthlyFasts('2026-11');
            const decCount = window.countMonthlyFasts('2026-12');

            // Clean up
            ['2026-11-02', '2026-11-05', '2026-11-12', '2026-12-01'].forEach(d => {
                localStorage.removeItem('meal-gym-tracker:fasting:' + d);
            });

            return { novCount, decCount };
        """)

        test("countMonthlyFasts calculates correct days in month", count_res.get('novCount') == 3)
        test("countMonthlyFasts isolates months properly", count_res.get('decCount') == 1)

        # Group 4: Interactive UI & Badge Updates
        print("\n--- Group 4: Interactive UI & Badge Updates ---")
        ui_res = js("""
            // Navigate to prayerView using routeNotificationClick
            window.routeNotificationClick({ mode: 'prayer' });
            const todayIso = toISO(weekDates[selectedIdx]);

            // Save fasted today
            window.saveFasting(todayIso, { fasted: true, type: 'sunnah' });
            window.renderFasting();

            const badgeTextFasted = document.getElementById('badge-fasting').textContent;
            const badgeHasComplete = document.getElementById('badge-fasting').classList.contains('is-complete');

            // Unfast today
            window.saveFasting(todayIso, { fasted: false });
            window.renderFasting();

            const badgeTextUnfasted = document.getElementById('badge-fasting').textContent;
            const badgeNoComplete = !document.getElementById('badge-fasting').classList.contains('is-complete');

            // Clean up
            localStorage.removeItem('meal-gym-tracker:fasting:' + todayIso);
            window.renderFasting();

            return {
                badgeTextFasted,
                badgeHasComplete,
                badgeTextUnfasted,
                badgeNoComplete
            };
        """)

        test("Badge reflects active fasting status", "صائم" in ui_res.get('badgeTextFasted'))
        test("Badge gets .is-complete class when fasted", ui_res.get('badgeHasComplete') is True)
        test("Badge reflects unfasted state without .is-complete", ui_res.get('badgeNoComplete') is True)

        # Group 5: Sunnah Recommendation Alerts (Monday & Thursday)
        print("\n--- Group 5: Sunnah Recommendation Alerts ---")
        sunnah_check = js("""
            const monIso = '2026-11-02'; // Monday (day 1)
            const sunIso = '2026-11-01'; // Sunday (day 0)

            const isMonSunnah = window.isSunnahFastingDay(monIso);
            const isSunSunnah = window.isSunnahFastingDay(sunIso);
            const thuIso = '2026-11-05'; // Thursday (day 4)
            const isThuSunnah = window.isSunnahFastingDay(thuIso);

            return { isMonSunnah, isSunSunnah, isThuSunnah };
        """)

        test("Monday is recognized as Sunnah fasting day", sunnah_check.get('isMonSunnah') is True)
        test("Thursday is recognized as Sunnah fasting day", sunnah_check.get('isThuSunnah') is True)
        test("Sunday is not flagged as weekly Sunnah fasting day", sunnah_check.get('isSunSunnah') is False)

    finally:
        driver.quit()

    print("\n" + "=" * 80)
    print(f"FASTING TRACKER TEST RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 80)
    return failed_count == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

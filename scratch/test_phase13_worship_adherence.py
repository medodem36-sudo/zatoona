"""
Automated Acceptance Test Suite: Weekly & Monthly Worship Adherence Report (Proposal #11)
Phase 13.7B: Visual Worship Consistency & Multi-Domain Adherence Report in Worship and Overview views
Tests DOM elements, 7/28-day window calculations, per-prayer breakdown, multi-pillar tracking, and Overview integration.
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
    print("PHASE 13.7B ACCEPTANCE TEST SUITE: WORSHIP ADHERENCE REPORT (PROPOSAL #11)")
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
        # Group 1: DOM Elements & Function Presence
        print("\n--- Group 1: DOM Elements & Function Presence ---")
        dom_check = js("""
            return {
                hasContainer: !!document.getElementById('worshipAdherenceContainer'),
                hasCompute: typeof window.computeWorshipAdherenceStats === 'function',
                hasRender: typeof window.renderWorshipAdherenceSummary === 'function',
                hasDomainWorship: !!document.getElementById('domainWorship')
            };
        """)

        test("#worshipAdherenceContainer exists in DOM", dom_check.get('hasContainer'))
        test("window.computeWorshipAdherenceStats is a function", dom_check.get('hasCompute'))
        test("window.renderWorshipAdherenceSummary is a function", dom_check.get('hasRender'))
        test("#domainWorship exists in DOM", dom_check.get('hasDomainWorship'))

        # Group 2: Empty / No-Data Handling
        print("\n--- Group 2: Empty / No-Data State Handling ---")
        empty_check = js("""
            // Clean future dates
            const futureIso = '2030-01-07';
            const emptyStats = window.computeWorshipAdherenceStats(7, futureIso);
            return {
                hasData: emptyStats.hasData,
                daysCount: emptyStats.daysCount
            };
        """)

        test("computeWorshipAdherenceStats handles days with no records", empty_check.get('hasData') is False)

        # Group 3: 7-Day Adherence Mathematical Accuracy
        print("\n--- Group 3: 7-Day Adherence Mathematical Accuracy ---")
        math_check = js("""
            const testDates = [
                '2026-11-01', '2026-11-02', '2026-11-03', '2026-11-04',
                '2026-11-05', '2026-11-06', '2026-11-07'
            ];
            
            // Days 1-4: All 5 Fard done, Fajr & Maghrib sunnah done (2 sunnah/day)
            for(let i = 0; i < 4; i++){
                const d = testDates[i];
                localStorage.setItem('meal-gym-tracker:prayer:' + d, JSON.stringify({
                    fajr: { fard: true, sunnah: true },
                    dhuhr: { fard: true, sunnah: false },
                    asr: { fard: true, sunnah: false },
                    maghrib: { fard: true, sunnah: true },
                    isha: { fard: true, sunnah: false }
                }));
            }

            // Days 5-6: Only 3 Fard done, 0 sunnah
            for(let i = 4; i < 6; i++){
                const d = testDates[i];
                localStorage.setItem('meal-gym-tracker:prayer:' + d, JSON.stringify({
                    fajr: { fard: true, sunnah: false },
                    dhuhr: { fard: true, sunnah: false },
                    asr: { fard: true, sunnah: false },
                    maghrib: { fard: false, sunnah: false },
                    isha: { fard: false, sunnah: false }
                }));
            }

            // Day 7: 0 Fard done
            localStorage.setItem('meal-gym-tracker:prayer:' + testDates[6], JSON.stringify({
                fajr: { fard: false, sunnah: false },
                dhuhr: { fard: false, sunnah: false },
                asr: { fard: false, sunnah: false },
                maghrib: { fard: false, sunnah: false },
                isha: { fard: false, sunnah: false }
            }));

            const stats = window.computeWorshipAdherenceStats(7, '2026-11-07');

            // Cleanup
            testDates.forEach(d => localStorage.removeItem('meal-gym-tracker:prayer:' + d));

            return {
                hasData: stats.hasData,
                totalFardDone: stats.totalFardDone,
                totalFardPossible: stats.totalFardPossible,
                overallFardPct: stats.overallFardPct,
                totalSunnahDone: stats.totalSunnahDone,
                fajrFard: stats.prayerStats.find(p => p.key === 'fajr').fardDone,
                ishaFard: stats.prayerStats.find(p => p.key === 'isha').fardDone
            };
        """)

        test("Stats recognizes logged prayer data (hasData: true)", math_check.get('hasData') is True)
        test("Total Fard completed is exactly 26", math_check.get('totalFardDone') == 26)
        test("Total Fard possible is exactly 35", math_check.get('totalFardPossible') == 35)
        test("Overall Fard percentage is 74%", math_check.get('overallFardPct') == 74)
        test("Total Sunnah completed is 8", math_check.get('totalSunnahDone') == 8)
        test("Fajr fard was completed 6 times", math_check.get('fajrFard') == 6)
        test("Isha fard was completed 4 times", math_check.get('ishaFard') == 4)

        # Group 4: Multi-Domain Worship Tracking (Qiyam, Quran, Azkar, Fasting)
        print("\n--- Group 4: Multi-Domain Worship Tracking ---")
        multi_check = js("""
            const testDates = ['2026-11-01', '2026-11-02', '2026-11-03', '2026-11-04'];
            
            // Qiyam on 2 nights
            localStorage.setItem('meal-gym-tracker:qiyam:' + testDates[0], JSON.stringify({ i0: true, i1: true }));
            localStorage.setItem('meal-gym-tracker:qiyam:' + testDates[1], JSON.stringify({ i0: true, i1: false }));
            
            // Fasting on 2 days
            window.saveFasting(testDates[0], { fasted: true, type: 'sunnah' });
            window.saveFasting(testDates[2], { fasted: true, type: 'qadaa' });

            // Quran on 3 days
            localStorage.setItem('meal-gym-tracker:quran:' + testDates[0], JSON.stringify({ i0: true, i1: true }));
            localStorage.setItem('meal-gym-tracker:quran:' + testDates[1], JSON.stringify({ i0: true, i1: true, i2: true }));
            localStorage.setItem('meal-gym-tracker:quran:' + testDates[2], JSON.stringify({ i0: true }));

            // Azkar on 2 days
            localStorage.setItem('meal-gym-tracker:azkar:' + testDates[0], JSON.stringify({ i0: true, i1: true }));
            localStorage.setItem('meal-gym-tracker:azkar:' + testDates[1], JSON.stringify({ i0: true, i1: false }));

            const stats = window.computeWorshipAdherenceStats(4, '2026-11-04');

            // Cleanup
            testDates.forEach(d => {
                localStorage.removeItem('meal-gym-tracker:qiyam:' + d);
                localStorage.removeItem('meal-gym-tracker:fasting:' + d);
                localStorage.removeItem('meal-gym-tracker:quran:' + d);
                localStorage.removeItem('meal-gym-tracker:azkar:' + d);
            });

            return {
                qiyamNights: stats.qiyamNights,
                totalFastingDays: stats.totalFastingDays,
                totalQuranItems: stats.totalQuranItemsDone,
                morningAzkar: stats.morningDone,
                eveningAzkar: stats.eveningDone
            };
        """)

        test("Qiyam nights counted correctly (2 nights)", multi_check.get('qiyamNights') == 2)
        test("Fasting days counted accurately (2 days)", multi_check.get('totalFastingDays') == 2)
        test("Quran completed items counted (6 items)", multi_check.get('totalQuranItems') == 6)
        test("Morning Azkar counted (2 mornings)", multi_check.get('morningAzkar') == 2)
        test("Evening Azkar counted (1 evening)", multi_check.get('eveningAzkar') == 1)

        # Group 5: UI Rendering, Range Toggle & Overview Integration
        print("\n--- Group 5: UI Rendering, Range Toggle & Overview Integration ---")
        ui_check = js("""
            window.routeNotificationClick({ mode: 'prayer' });
            
            // Seed 1 active day today
            const todayIso = toISO(weekDates[selectedIdx]);
            localStorage.setItem('meal-gym-tracker:prayer:' + todayIso, JSON.stringify({
                fajr: { fard: true, sunnah: true },
                dhuhr: { fard: true, sunnah: false },
                asr: { fard: true, sunnah: false },
                maghrib: { fard: true, sunnah: false },
                isha: { fard: true, sunnah: false }
            }));

            window.renderWorshipAdherenceSummary(7);
            const containerHtml = document.getElementById('worshipAdherenceContainer').innerHTML;
            const btn7Active = document.getElementById('btnWorshipAdherence7').classList.contains('active');

            // Switch to 28 days
            document.getElementById('btnWorshipAdherence28').click();
            const btn28Active = document.getElementById('btnWorshipAdherence28').classList.contains('active');

            // Switch to overview mode
            window.routeNotificationClick({ mode: 'overview' });
            const overviewHtml = document.getElementById('domainWorship').innerHTML;
            const hasGoBtn = !!document.getElementById('btnGoWorshipAdherence');

            // Cleanup
            localStorage.removeItem('meal-gym-tracker:prayer:' + todayIso);

            return {
                hasRenderedContent: containerHtml.includes('التزام الفروض'),
                btn7Active,
                btn28Active,
                overviewHasPill: overviewHtml.includes('score-pill'),
                hasGoBtn
            };
        """)

        test("Worship adherence card renders statistics content", ui_check.get('hasRenderedContent'))
        test("7-day button initializes with active class", ui_check.get('btn7Active'))
        test("28-day button toggles to active upon click", ui_check.get('btn28Active'))
        test("Overview domainWorship includes score-pill", ui_check.get('overviewHasPill'))
        test("Overview includes 'عرض التقرير المفصل' navigation button", ui_check.get('hasGoBtn'))

    finally:
        driver.quit()

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 80)

    if failed_count > 0:
        sys.exit(1)

if __name__ == '__main__':
    run_tests()

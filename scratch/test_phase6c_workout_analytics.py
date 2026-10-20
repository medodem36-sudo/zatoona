import os
import sys
import time
import json
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
    print("================================================================================")
    print("PHASE 6C ACCEPTANCE TEST SUITE: WORKOUT PROGRESS & PERFORMANCE ANALYTICS")
    print("================================================================================")

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

    def reset_storage():
        js("localStorage.clear();")

    try:
        # ---------------------------------------------------------
        # Group 1: Functions Export & Basic Checks
        # ---------------------------------------------------------
        print("\n--- Group 1: Window Exports & Function Availability ---")
        exports = js("""
            return {
                hasGetAnalyticsDateRange: typeof window.getAnalyticsDateRange === 'function',
                hasGetWorkoutSessionsAnalytics: typeof window.getWorkoutSessionsAnalytics === 'function',
                hasGetWorkoutPerformanceAnalytics: typeof window.getWorkoutPerformanceAnalytics === 'function',
                hasGetWorkoutProgressSummary: typeof window.getWorkoutProgressSummary === 'function',
                hasGetExerciseProgressionStats: typeof window.getExerciseProgressionStats === 'function',
                hasRenderWorkoutProgressionSVG: typeof window.renderWorkoutProgressionSVG === 'function',
                hasRenderWorkoutHistory: typeof window.renderWorkoutHistory === 'function',
            };
        """)
        for fn_name, present in exports.items():
            test(f"Export {fn_name} is a function", present)

        # ---------------------------------------------------------
        # Group 2: Session Analytics (Completed, In-Progress, Cancelled)
        # ---------------------------------------------------------
        print("\n--- Group 2: Session Analytics (Rules 1 & 2) ---")
        reset_storage()
        js("""
            const sessions = {
                '2026-10-01': {
                    id: 's1', iso: '2026-10-01', status: 'completed',
                    startedAt: '2026-10-01T10:00:00.000Z', completedAt: '2026-10-01T10:45:00.000Z',
                    durationSeconds: 2700, completedSetsCount: 15, totalSetsCount: 15
                },
                '2026-10-03': {
                    id: 's2', iso: '2026-10-03', status: 'cancelled',
                    startedAt: '2026-10-03T10:00:00.000Z', cancelledAt: '2026-10-03T10:15:00.000Z',
                    durationSeconds: 900
                },
                '2026-10-05': {
                    id: 's3', iso: '2026-10-05', status: 'in_progress',
                    startedAt: '2026-10-05T10:00:00.000Z', completedAt: null
                },
                '2026-10-07': {
                    id: 's4', iso: '2026-10-07', status: 'completed',
                    startedAt: '2026-10-07T10:00:00.000Z', completedAt: '2026-10-07T10:50:00.000Z',
                    durationSeconds: 3000,
                    history: [
                        { id: 's4_old', iso: '2026-10-07', status: 'completed', durationSeconds: 1800, completedAt: '2026-10-07T08:00:00.000Z' }
                    ]
                }
            };
            saveGymSessions(sessions);
        """)

        sess_res = js("return window.getWorkoutSessionsAnalytics();")
        test("Completed sessions count strictly excludes cancelled & in_progress", sess_res['completedCount'] == 3, f"got {sess_res['completedCount']}")
        test("Cancelled sessions counted separately", sess_res['cancelledCount'] == 1, f"got {sess_res['cancelledCount']}")
        test("In-progress sessions counted separately", sess_res['inProgressCount'] == 1, f"got {sess_res['inProgressCount']}")
        test("Average duration calculated from valid completed records", sess_res['avgDurationSeconds'] == 2500, f"got {sess_res['avgDurationSeconds']}")

        # ---------------------------------------------------------
        # Group 3: Zero Double Counting between Sessions and Logs (Rule 3, 8, 9)
        # ---------------------------------------------------------
        print("\n--- Group 3: Workout Days Count & Deduplication ---")
        reset_storage()
        js("""
            // Same day has BOTH completed session and exercise log
            const sessions = {
                '2026-10-10': { id: 's1', iso: '2026-10-10', status: 'completed', durationSeconds: 1800 },
                '2026-10-12': { id: 's2', iso: '2026-10-12', status: 'completed', durationSeconds: 1800 }
            };
            saveGymSessions(sessions);

            // 2026-10-10 (overlap), 2026-10-14 (only exercise log)
            saveEx('2026-10-10', {
                'bench': { sets: [true, true, true], weight: '60', reps: '10' }
            });
            saveEx('2026-10-14', {
                'squat': { sets: [true, true], weight: '80', reps: '8' }
            });
            // 2026-10-16 has empty sets (no completed workout)
            saveEx('2026-10-16', {
                'squat': { sets: [false, false], weight: '80', reps: '8' }
            });
        """)

        summary = js("return window.getWorkoutProgressSummary({ rangeKey: 'all' });")
        test("Total completed sessions count is 2", summary['completedSessionsCount'] == 2, f"got {summary['completedSessionsCount']}")
        test("Unique workout days count is 3 (2026-10-10 not double counted)", summary['workoutDaysCount'] == 3, f"got {summary['workoutDaysCount']}")
        test("Active weeks count correctly calculated", summary['activeWeeksCount'] >= 1, f"got {summary['activeWeeksCount']}")

        # ---------------------------------------------------------
        # Group 4: Volume Calculation & Precision (Rule 4 & 5)
        # ---------------------------------------------------------
        print("\n--- Group 4: Volume Calculation & Incomplete Data Guard ---")
        reset_storage()
        js("""
            // Entry 1: 3 sets done * 60kg * 10 reps = 1800 kg
            saveEx('2026-10-01', {
                'bench': { sets: [true, true, true], weight: '60', reps: '10' }
            });
            // Entry 2: 2 sets done (of 3) * 50kg * 8 reps = 800 kg
            saveEx('2026-10-03', {
                'bench': { sets: [true, false, true], weight: '50', reps: '8' }
            });
            // Entry 3: Incomplete data (missing reps) -> must NOT add fake volume
            saveEx('2026-10-05', {
                'overhead_press': { sets: [true, true], weight: '40', reps: '' }
            });
            // Entry 4: Incomplete data (missing weight) -> must NOT add fake volume
            saveEx('2026-10-07', {
                'pullup': { sets: [true, true, true], weight: '', reps: '10' }
            });
        """)

        perf = js("return window.getWorkoutPerformanceAnalytics({ from: '2026-10-01', to: '2026-10-10' });")
        test("Total volume sums only valid entries: 1800 + 800 = 2600 kg", perf['cumulativeVolume'] == 2600, f"got {perf['cumulativeVolume']}")
        test("Volume entries count is exactly 2 (incomplete records skipped)", perf['volumeEntriesCount'] == 2, f"got {perf['volumeEntriesCount']}")

        # Test when NO valid volume data exists at all
        reset_storage()
        js("""
            saveEx('2026-10-01', {
                'pullup': { sets: [true, true], weight: '', reps: '10' }
            });
        """)
        perf_empty = js("return window.getWorkoutPerformanceAnalytics();")
        test("Volume is null when no records have numeric weight & reps", perf_empty['cumulativeVolume'] is None, f"got {perf_empty['cumulativeVolume']}")

        # ---------------------------------------------------------
        # Group 5: PR Weight vs PR Reps Distinction (Rule 11)
        # ---------------------------------------------------------
        print("\n--- Group 5: PR Weight vs PR Reps Distinction ---")
        reset_storage()
        js("""
            saveEx('2026-10-01', {
                'bench': { sets: [true, true, true], weight: '80', reps: '5', note: 'Heavy day' }
            });
            saveEx('2026-10-05', {
                'bench': { sets: [true, true, true], weight: '60', reps: '15', note: 'Hypertrophy day' }
            });
            saveEx('2026-10-10', {
                'bench': { sets: [true, true, true, true], weight: '70', reps: '10', note: 'Volume PR' }
            });
        """)

        prog_stats = js("""
            const map = window.getWorkoutPerformanceAnalytics().exerciseDataMap;
            return window.getExerciseProgressionStats('bench', map);
        """)

        test("PR Weight is 80kg (from 2026-10-01)", prog_stats['prWeight']['weight'] == 80 and prog_stats['prWeight']['iso'] == '2026-10-01')
        test("PR Reps is 15 reps (from 2026-10-05)", prog_stats['prReps']['reps'] == 15 and prog_stats['prReps']['iso'] == '2026-10-05')
        test("Best session volume is 4 * 70 * 10 = 2800 kg (from 2026-10-10)", prog_stats['prVolume']['volume'] == 2800 and prog_stats['prVolume']['iso'] == '2026-10-10')

        # ---------------------------------------------------------
        # Group 6: Date Range Boundaries & Timezone Safety
        # ---------------------------------------------------------
        print("\n--- Group 6: Date Range Calculation & Timezone Boundaries ---")
        ref_iso = '2026-10-20'
        range_7d = js(f"""
            const ref = new Date('{ref_iso}T12:00:00');
            return window.getAnalyticsDateRange('7d', '', '', ref);
        """)
        test("7d range spans exactly 7 calendar days inclusive", range_7d['from'] == '2026-10-14' and range_7d['to'] == '2026-10-20', f"got {range_7d}")

        range_30d = js(f"""
            const ref = new Date('{ref_iso}T12:00:00');
            return window.getAnalyticsDateRange('30d', '', '', ref);
        """)
        test("30d range spans exactly 30 calendar days inclusive", range_30d['from'] == '2026-09-21' and range_30d['to'] == '2026-10-20', f"got {range_30d}")

        range_all = js("return window.getAnalyticsDateRange('all');")
        test("all range returns empty bounds", range_all['from'] == '' and range_all['to'] == '', f"got {range_all}")

        # ---------------------------------------------------------
        # Group 7: Exercise Progression & SVG Chart Rendering
        # ---------------------------------------------------------
        print("\n--- Group 7: Progression Chart & Single Data Point Handling ---")
        svg_multi = js("""
            const points = [
                { iso: '2026-10-01', weight: 60, reps: 10 },
                { iso: '2026-10-05', weight: 65, reps: 8 },
                { iso: '2026-10-10', weight: 70, reps: 6 }
            ];
            return window.renderWorkoutProgressionSVG(points);
        """)
        test("SVG chart renders <svg> element for >=2 points", '<svg' in svg_multi and '<polyline' in svg_multi)
        test("SVG chart includes circles with tooltips", '<circle' in svg_multi and '<title>' in svg_multi)

        svg_single = js("""
            const points = [{ iso: '2026-10-01', weight: 60, reps: 10 }];
            return window.renderWorkoutProgressionSVG(points);
        """)
        test("Single point displays polite note without breaking or fake line", '<svg' not in svg_single and 'نقطة تسجيل واحدة' in svg_single)

        svg_zero = js("return window.renderWorkoutProgressionSVG([]);")
        test("Zero points displays empty message", 'لا توجد بيانات كافية' in svg_zero)

        # ---------------------------------------------------------
        # Group 8: Excluded Exercises with Historical Records
        # ---------------------------------------------------------
        print("\n--- Group 8: Excluded Exercises with History (Rule 7) ---")
        reset_storage()
        js("""
            saveExcludedExercises({ 'bench': true });
            saveEx('2026-10-01', {
                'bench': { sets: [true, true], weight: '65', reps: '10' }
            });
            renderWorkoutHistory();
        """)
        time.sleep(0.3)

        picker_html = js("return document.getElementById('workoutHistoryPicker') ? document.getElementById('workoutHistoryPicker').innerHTML : '';")
        test("Excluded exercise with history appears in picker tagged '(مستبعد)'", 'مستبعد' in picker_html and 'data-key="bench"' in picker_html)

        # ---------------------------------------------------------
        # Group 9: Corrupt & Missing Data Resilience
        # ---------------------------------------------------------
        print("\n--- Group 9: Resilience Against Corrupt Data ---")
        reset_storage()
        js("""
            // Put malformed JSON in an ex key
            localStorage.setItem('meal-gym-tracker:ex:2026-10-01', 'NOT_JSON{bad');
            // Put non-object in gym-sessions-v1
            localStorage.setItem('meal-gym-tracker:gym-sessions-v1', '"a string instead of map"');
        """)

        no_crash = js("""
            try {
                window.getWorkoutSessionsAnalytics();
                window.getWorkoutPerformanceAnalytics();
                window.getWorkoutProgressSummary();
                window.renderWorkoutHistory();
                return true;
            } catch(e) {
                return false;
            }
        """)
        test("Analytics functions and render survive corrupt localStorage without throwing", no_crash)

        # ---------------------------------------------------------
        # Group 10: Read-Only Invariance
        # ---------------------------------------------------------
        print("\n--- Group 10: Read-Only Invariance (Rule 10 & Core Constraint) ---")
        reset_storage()
        js("""
            const origEx = { 'bench': { sets: [true, true], weight: '60', reps: '10' } };
            saveEx('2026-10-01', origEx);
            const origSess = { '2026-10-01': { id: 's1', iso: '2026-10-01', status: 'completed', durationSeconds: 1800 } };
            saveGymSessions(origSess);
        """)

        before_state = js("""
            return {
                exVal: localStorage.getItem('meal-gym-tracker:ex:2026-10-01'),
                sessVal: localStorage.getItem('meal-gym-tracker:gym-sessions-v1')
            };
        """)

        js("""
            for(let i=0; i<5; i++){
                window.getWorkoutProgressSummary({ rangeKey: 'all' });
                window.renderWorkoutHistory();
            }
        """)

        after_state = js("""
            return {
                exVal: localStorage.getItem('meal-gym-tracker:ex:2026-10-01'),
                sessVal: localStorage.getItem('meal-gym-tracker:gym-sessions-v1')
            };
        """)

        test("ex:{iso} is not mutated by analytics calculations", before_state['exVal'] == after_state['exVal'])
        test("gym-sessions-v1 is not mutated by analytics calculations", before_state['sessVal'] == after_state['sessVal'])

        # ---------------------------------------------------------
        # Group 11: UI Interactivity & Range Selection
        # ---------------------------------------------------------
        print("\n--- Group 11: UI Interactivity & Range Selector ---")
        reset_storage()
        js("""
            saveEx('2026-10-15', { 'bench': { sets: [true, true], weight: '70', reps: '10' } });
            renderWorkoutHistory();
        """)
        time.sleep(0.3)

        range_chips = js("""
            const chips = document.querySelectorAll('#gymAnalyticsRangeChips .day-chip');
            return Array.from(chips).map(c => ({ range: c.dataset.range, text: c.textContent.trim() }));
        """)
        test("Range chips include 7d, 30d, 90d, all", len(range_chips) == 4 and any(c['range']=='7d' for c in range_chips) and any(c['range']=='all' for c in range_chips))

        js("""
            const chip7 = document.querySelector('#gymAnalyticsRangeChips .day-chip[data-range=\"7d\"]');
            if(chip7) chip7.click();
        """)
        time.sleep(0.3)
        cur_range = js("return window.workoutAnalyticsRange;")
        test("Clicking 7d chip switches workoutAnalyticsRange to '7d'", cur_range == '7d')

        # ---------------------------------------------------------
        # Group 12: Empty State
        # ---------------------------------------------------------
        print("\n--- Group 12: Empty State ---")
        reset_storage()
        js("renderWorkoutHistory();")
        time.sleep(0.2)
        empty_html = js("return document.getElementById('workoutHistoryBody') ? document.getElementById('workoutHistoryBody').innerHTML : '';")
        test("Empty state renders message when no records exist", 'لسه معندكش سجل تمارين' in empty_html)

        # ---------------------------------------------------------
        # Group 13: Viewport Responsiveness (375px) & No Horizontal Scroll
        # ---------------------------------------------------------
        print("\n--- Group 13: Viewport Responsiveness (375px) ---")
        driver.set_window_size(375, 812)
        js("""
            saveEx('2026-10-15', { 'bench': { sets: [true, true], weight: '70', reps: '10' } });
            renderWorkoutHistory();
        """)
        time.sleep(0.3)

        overflow = js("""
            const body = document.getElementById('workoutHistoryBody');
            if(!body) return { overflow: false };
            return {
                scrollWidth: body.scrollWidth,
                clientWidth: body.clientWidth,
                hasOverflow: body.scrollWidth > body.clientWidth + 2
            };
        """)
        test("No horizontal overflow on 375px mobile screen", not overflow.get('hasOverflow', True), f"scroll={overflow.get('scrollWidth')} vs client={overflow.get('clientWidth')}")

        # ---------------------------------------------------------
        # Group 14: Browser Console Integrity
        # ---------------------------------------------------------
        print("\n--- Group 14: Browser Console Integrity ---")
        logs = driver.get_log('browser')
        js_errors = [l for l in logs if l['level'] == 'SEVERE' and 'manifest.json' not in l['message']]
        test("Zero severe JavaScript console errors during analytics runs", len(js_errors) == 0, f"errors: {js_errors}")

    finally:
        driver.quit()

    print("\n================================================================================")
    print(f"RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("================================================================================")
    if failed_count > 0:
        sys.exit(1)

if __name__ == '__main__':
    run_tests()

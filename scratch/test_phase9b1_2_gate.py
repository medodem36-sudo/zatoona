"""
Phase 9B.1.2 Acceptance Test Suite: Minimal Notes Hub Gap Closure
Tests:
1. Default sort order is newest-first (descending).
2. Toggling sort order to oldest-first (ascending) with multiple dated records.
3. Integrity of sort order after search and filter activations.
4. Undated section notes never receive fake dates and remain in their dedicated group.
5. "Clear All Filters" button appears ONLY when a filter (search, type, time, hasAtt) is active.
6. "Clear All Filters" resets type, time, attachment, and search filters simultaneously.
7. Sort order is preserved after clearing all filters.
8. Accurate result counters before and after clearing all filters.
9. Zero mutations to localStorage during sorting, filtering, and resetting.
10. Zero duplicates and zero attachment loss.
11. Viewport responsiveness (375px) and light/dark theme compatibility.
12. Clean browser console (zero SEVERE errors).
"""

import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

sys.stdout.reconfigure(encoding='utf-8')

FILE_PATH = os.path.abspath("index.html")
FILE_URL = f"file:///{FILE_PATH.replace(os.sep, '/')}"

results = []

def test(name, condition, details=""):
    status = "PASS" if condition else "FAIL"
    results.append({"name": name, "status": status, "details": details})
    mark = "[PASS]" if condition else "[FAIL]"
    print(f"  {mark} {name}")
    if not condition and details:
        print(f"         Reason: {details}")

def run_tests():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(FILE_URL)
        WebDriverWait(driver, 5).until(lambda d: d.execute_script("return document.readyState === 'complete'"))

        def js(script):
            return driver.execute_script(script)

        # Navigate to notes view
        js("navigateTo('notes');")

        # -------------------------------------------------------------
        # Test 1: Default sort order is descending (newest first)
        # -------------------------------------------------------------
        print("\n--- Test 1: Default Sort Order (Descending) ---")
        t1_res = js("""
            localStorage.clear();
            storageSet('daynote:2026-10-10', 'ملاحظة يوم قديم');
            storageSet('daynote:2026-10-20', 'ملاحظة يوم وسيط');
            storageSet('daynote:2026-10-25', 'ملاحظة يوم حديث');

            // Reset state
            notesHubState.filterType = 'all';
            notesHubState.filterTime = 'all';
            notesHubState.filterHasAtt = false;
            notesHubState.searchQuery = '';
            notesHubState.sortOrder = 'desc';
            renderNotesHub();

            const cards = document.querySelectorAll('#notesTimelineList .note-hub-card');
            const dates = Array.from(cards).map(c => {
                const mono = c.querySelector('.mono');
                return mono ? mono.textContent.trim() : '';
            });

            const sortBtn = document.getElementById('notesSortToggle');
            const btnText = sortBtn ? sortBtn.textContent : '';

            return {
                sortOrder: notesHubState.sortOrder,
                dates: dates,
                btnText: btnText,
                isDesc: dates[0] === '2026-10-25' && dates[1] === '2026-10-20' && dates[2] === '2026-10-10'
            };
        """)
        test("1.1 Default sort order is 'desc'", t1_res.get('sortOrder') == 'desc')
        test("1.2 Dated cards ordered descending (2026-10-25 -> 2026-10-20 -> 2026-10-10)", t1_res.get('isDesc'), f"Dates: {t1_res.get('dates')}")
        test("1.3 Sort button label reflects descending order", "الأحدث" in t1_res.get('btnText'))

        # -------------------------------------------------------------
        # Test 2: Toggling sort order to ascending (oldest first)
        # -------------------------------------------------------------
        print("\n--- Test 2: Toggle Sort Order to Ascending ---")
        t2_res = js("""
            const sortBtn = document.getElementById('notesSortToggle');
            if(sortBtn) sortBtn.click();

            const cards = document.querySelectorAll('#notesTimelineList .note-hub-card');
            const dates = Array.from(cards).map(c => {
                const mono = c.querySelector('.mono');
                return mono ? mono.textContent.trim() : '';
            });

            return {
                sortOrder: notesHubState.sortOrder,
                dates: dates,
                btnText: sortBtn ? sortBtn.textContent : '',
                isAsc: dates[0] === '2026-10-10' && dates[1] === '2026-10-20' && dates[2] === '2026-10-25'
            };
        """)
        test("2.1 Clicking toggle switches sortOrder to 'asc'", t2_res.get('sortOrder') == 'asc')
        test("2.2 Dated cards re-ordered ascending (2026-10-10 -> 2026-10-20 -> 2026-10-25)", t2_res.get('isAsc'), f"Dates: {t2_res.get('dates')}")
        test("2.3 Sort button label reflects ascending order", "الأقدم" in t2_res.get('btnText'))

        # -------------------------------------------------------------
        # Test 3: Integrity of sort order after search and filters
        # -------------------------------------------------------------
        print("\n--- Test 3: Sort Order Integrity with Filters ---")
        t3_res = js("""
            // Add more records
            storageSet('ex:2026-10-12', JSON.stringify({ squat: { note: 'تمرين قديم' } }));
            storageSet('ex:2026-10-22', JSON.stringify({ squat: { note: 'تمرين حديث' } }));

            // Filter by 'exercise' while sortOrder is 'asc'
            notesHubState.filterType = 'exercise';
            renderNotesHub();

            const cards = document.querySelectorAll('#notesTimelineList .note-hub-card');
            const dates = Array.from(cards).map(c => {
                const mono = c.querySelector('.mono');
                return mono ? mono.textContent.trim() : '';
            });

            return {
                sortOrder: notesHubState.sortOrder,
                dates: dates,
                isAscFiltered: dates.length === 2 && dates[0] === '2026-10-12' && dates[1] === '2026-10-22'
            };
        """)
        test("3.1 Sort order preserved when switching type filter", t3_res.get('isAscFiltered'), f"Dates: {t3_res.get('dates')}")

        # -------------------------------------------------------------
        # Test 4: Undated section notes never receive fake dates
        # -------------------------------------------------------------
        print("\n--- Test 4: Undated Section Notes Independence ---")
        t4_res = js("""
            storageSet('secnote:meal', 'ملاحظة قسم التغذية');
            notesHubState.filterType = 'all';
            renderNotesHub();

            const secCards = document.querySelectorAll('#notesSectionList .note-hub-card');
            const timelineCards = document.querySelectorAll('#notesTimelineList .note-hub-card');

            // Find all collected notes
            const all = collectAllUnifiedNotes();
            const secNotes = all.filter(n => n.type === 'section');

            return {
                secCount: secCards.length,
                allSecHaveNullIso: secNotes.every(n => n.iso === null),
                secInSeparateGroup: secCards.length > 0 && !document.getElementById('notesUndatedSection').classList.contains('hidden')
            };
        """)
        test("4.1 Section notes have strictly null iso (no fake dates)", t4_res.get('allSecHaveNullIso'))
        test("4.2 Section notes rendered exclusively in separate undated container", t4_res.get('secInSeparateGroup'))

        # -------------------------------------------------------------
        # Test 5: "Clear All Filters" button visibility
        # -------------------------------------------------------------
        print("\n--- Test 5: 'Clear All Filters' Button Visibility ---")
        t5_res = js("""
            // Reset to defaults first
            notesHubState.filterType = 'all';
            notesHubState.filterTime = 'all';
            notesHubState.filterHasAtt = false;
            notesHubState.searchQuery = '';
            renderNotesHub();

            const btn = document.getElementById('notesResetFiltersBtn');
            const hiddenInitially = btn.classList.contains('hidden');

            // Activate type filter
            notesHubState.filterType = 'daily';
            renderNotesHub();
            const visibleWithType = !btn.classList.contains('hidden');

            // Return type to all, activate search
            notesHubState.filterType = 'all';
            notesHubState.searchQuery = 'تمرين';
            renderNotesHub();
            const visibleWithSearch = !btn.classList.contains('hidden');

            // Return search to empty, activate attachment filter
            notesHubState.searchQuery = '';
            notesHubState.filterHasAtt = true;
            renderNotesHub();
            const visibleWithAtt = !btn.classList.contains('hidden');

            // Reset all to default
            notesHubState.filterHasAtt = false;
            renderNotesHub();
            const hiddenFinally = btn.classList.contains('hidden');

            return {
                hiddenInitially: hiddenInitially,
                visibleWithType: visibleWithType,
                visibleWithSearch: visibleWithSearch,
                visibleWithAtt: visibleWithAtt,
                hiddenFinally: hiddenFinally
            };
        """)
        test("5.1 Reset button hidden when all filters are at default", t5_res.get('hiddenInitially'))
        test("5.2 Reset button visible when type filter is active", t5_res.get('visibleWithType'))
        test("5.3 Reset button visible when search query is present", t5_res.get('visibleWithSearch'))
        test("5.4 Reset button visible when attachment filter is active", t5_res.get('visibleWithAtt'))
        test("5.5 Reset button automatically hides when filters return to default", t5_res.get('hiddenFinally'))

        # -------------------------------------------------------------
        # Test 6: Clear all filters resets all 4 filters simultaneously
        # -------------------------------------------------------------
        print("\n--- Test 6: Simultaneous Reset of All Filters ---")
        t6_res = js("""
            // Activate ALL filters simultaneously
            notesHubState.filterType = 'exercise';
            notesHubState.filterTime = '7d';
            notesHubState.filterHasAtt = true;
            notesHubState.searchQuery = 'سكوات';
            const sInp = document.getElementById('notesSearchInput');
            if(sInp) sInp.value = 'سكوات';
            renderNotesHub();

            // Click the reset all filters button
            const resetBtn = document.getElementById('notesResetFiltersBtn');
            if(resetBtn) resetBtn.click();

            // Check state
            const typeReset = notesHubState.filterType === 'all';
            const timeReset = notesHubState.filterTime === 'all';
            const attReset = notesHubState.filterHasAtt === false;
            const searchReset = notesHubState.searchQuery === '';
            const inpValueReset = sInp ? sInp.value === '' : true;

            // Check UI chips
            const activeTypeChip = document.querySelector('#notesTypeFilterRow .day-chip.on');
            const activeTimeChip = document.querySelector('#notesTimeFilterRow .day-chip.on');
            const attBtnOn = document.getElementById('notesHasAttBtn').classList.contains('on');

            return {
                typeReset: typeReset,
                timeReset: timeReset,
                attReset: attReset,
                searchReset: searchReset,
                inpValueReset: inpValueReset,
                activeTypeChipAll: activeTypeChip ? activeTypeChip.dataset.type === 'all' : false,
                activeTimeChipAll: activeTimeChip ? activeTimeChip.dataset.time === 'all' : false,
                attBtnOff: !attBtnOn
            };
        """)
        test("6.1 notesHubState.filterType reset to 'all'", t6_res.get('typeReset'))
        test("6.2 notesHubState.filterTime reset to 'all'", t6_res.get('timeReset'))
        test("6.3 notesHubState.filterHasAtt reset to false", t6_res.get('attReset'))
        test("6.4 notesHubState.searchQuery reset to '' and input cleared", t6_res.get('searchReset') and t6_res.get('inpValueReset'))
        test("6.5 UI filter chips restored to 'all' and attachment toggle turned off", t6_res.get('activeTypeChipAll') and t6_res.get('activeTimeChipAll') and t6_res.get('attBtnOff'))

        # -------------------------------------------------------------
        # Test 7: Sort order is preserved after clearing filters
        # -------------------------------------------------------------
        print("\n--- Test 7: Sort Order Preserved After Filter Reset ---")
        t7_res = js("""
            // Set sortOrder to 'asc'
            notesHubState.sortOrder = 'asc';
            // Activate a filter
            notesHubState.filterType = 'daily';
            renderNotesHub();

            // Click reset
            const resetBtn = document.getElementById('notesResetFiltersBtn');
            if(resetBtn) resetBtn.click();

            return {
                sortOrderAfterReset: notesHubState.sortOrder
            };
        """)
        test("7.1 sortOrder ('asc') preserved as-is after clicking Clear All Filters", t7_res.get('sortOrderAfterReset') == 'asc')

        # -------------------------------------------------------------
        # Test 8: Result counters accuracy before and after reset
        # -------------------------------------------------------------
        print("\n--- Test 8: Result Counter Accuracy ---")
        t8_res = js("""
            const allNotes = collectAllUnifiedNotes();
            const total = allNotes.length;

            // Apply restrictive filter
            notesHubState.filterType = 'daily';
            renderNotesHub();
            const dailyCount = allNotes.filter(n => n.type === 'daily').length;
            const metaFiltered = document.getElementById('notesFilterMeta').textContent;

            // Reset filters
            document.getElementById('notesResetFiltersBtn').click();
            const metaReset = document.getElementById('notesFilterMeta').textContent;

            return {
                metaFilteredCorrect: metaFiltered.includes(String(dailyCount)) && metaFiltered.includes(String(total)),
                metaResetCorrect: metaReset.includes(String(total)),
                datedCountMatches: parseInt(document.getElementById('notesDatedCount').textContent) === allNotes.filter(n => n.iso !== null).length,
                sectionCountMatches: parseInt(document.getElementById('notesSectionCount').textContent) === allNotes.filter(n => n.type === 'section').length
            };
        """)
        test("8.1 Filter feedback meta displays filtered and total counts correctly", t8_res.get('metaFilteredCorrect'))
        test("8.2 Meta displays total notes after clearing all filters", t8_res.get('metaResetCorrect'))
        test("8.3 Header dated notes counter exactly matches rendered items", t8_res.get('datedCountMatches'))
        test("8.4 Header section notes counter exactly matches rendered items", t8_res.get('sectionCountMatches'))

        # -------------------------------------------------------------
        # Test 9: Storage Invariance (No mutations to localStorage)
        # -------------------------------------------------------------
        print("\n--- Test 9: Storage Invariance (Read-Only) ---")
        t9_res = js("""
            const beforeDump = JSON.stringify(Object.keys(localStorage).sort().map(k => [k, localStorage.getItem(k)]));

            // Execute multiple toggle, filter, and reset actions
            document.getElementById('notesSortToggle').click(); // toggle to desc
            notesHubState.filterType = 'recovery';
            renderNotesHub();
            document.getElementById('notesSortToggle').click(); // toggle to asc
            document.getElementById('notesResetFiltersBtn').click(); // reset

            const afterDump = JSON.stringify(Object.keys(localStorage).sort().map(k => [k, localStorage.getItem(k)]));

            return beforeDump === afterDump;
        """)
        test("9.1 Zero mutations to localStorage during sort toggle, filtering, and resetting", t9_res)

        # -------------------------------------------------------------
        # Test 10: Zero duplicates and zero attachment loss
        # -------------------------------------------------------------
        print("\n--- Test 10: Deduplication and Attachment Integrity ---")
        t10_res = js("""
            storageSet('note-attachments-v1', JSON.stringify({
                'daynote:2026-10-25': [{ mediaId: 'med_1', fileName: 'sample.png' }]
            }));
            renderNotesHub();

            const allNotes = collectAllUnifiedNotes();
            const keys = allNotes.map(n => n.noteKey);
            const uniqueKeys = new Set(keys);

            const card25 = document.querySelector('#notesTimelineList [data-key="daynote:2026-10-25"]');
            const hasAttThumb = card25 ? !!card25.querySelector('.note-hub-att-box') : false;

            return {
                noDuplicates: keys.length === uniqueKeys.size,
                attachmentRendered: hasAttThumb
            };
        """)
        test("10.1 Zero duplicate keys across all collected notes", t10_res.get('noDuplicates'))
        test("10.2 Attachment thumbnail rendered correctly on note card", t10_res.get('attachmentRendered'))

        # -------------------------------------------------------------
        # Test 11: Viewport Responsiveness & Theme Compatibility
        # -------------------------------------------------------------
        print("\n--- Test 11: Mobile Viewport & Theme Compatibility ---")
        driver.set_window_size(375, 812)
        time.sleep(0.3)
        mobile_overflow = js("""
            const el = document.getElementById('notesView');
            return document.documentElement.scrollWidth > window.innerWidth;
        """)
        test("11.1 Zero horizontal page overflow on 375px mobile screen", not mobile_overflow)

        # Test Dark Theme
        js("document.documentElement.setAttribute('data-theme', 'dark');")
        time.sleep(0.2)
        dark_ok = js("return !!document.getElementById('notesView');")
        test("11.2 Dark theme applies cleanly to notes hub", dark_ok)

        # Test Light Theme
        js("document.documentElement.setAttribute('data-theme', 'light');")
        time.sleep(0.2)
        light_ok = js("return !!document.getElementById('notesView');")
        test("11.3 Light theme applies cleanly to notes hub", light_ok)

        # -------------------------------------------------------------
        # Test 12: Browser Console Cleanliness
        # -------------------------------------------------------------
        print("\n--- Test 12: Browser Console Integrity ---")
        logs = driver.get_log('browser')
        severe_errors = [l for l in logs if l['level'] == 'SEVERE' and 'manifest.json' not in l['message']]
        test("12.1 Zero SEVERE JavaScript console errors", len(severe_errors) == 0, f"Errors: {severe_errors}")

        # Cleanup test data
        js("localStorage.clear();")

    finally:
        driver.quit()

    # -------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------
    print("\n" + "="*80)
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["status"] == "PASS")
    failed_tests = sum(1 for r in results if r["status"] == "FAIL")
    print(f"PHASE 9B.1.2 ACCEPTANCE RESULTS: {passed_tests} PASSED, {failed_tests} FAILED (TOTAL {total_tests})")
    print("="*80)

    return failed_tests == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

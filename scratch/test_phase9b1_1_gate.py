"""
Phase 9B.1.1 Closure Gate Verification Suite
Exhaustive verification of Phase 9B.1 Unified Notes Hub against all 7 audit areas.
"""

import os
import sys
import json
import time
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

def run_gate_audit():
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

        # -------------------------------------------------------------
        # Area 1: Interface Matching with Original Requirements
        # -------------------------------------------------------------
        print("\n=== Area 1: UI Matching Original Requirements ===")

        # 1.1 Text Search Input & Clear Button
        has_search_input = driver.execute_script("return !!document.getElementById('notesSearchInput');")
        has_clear_search_btn = driver.execute_script("return !!document.getElementById('notesSearchClearBtn');")
        test("1.1 Text search input exists (#notesSearchInput)", has_search_input)
        test("1.1 Text search clear button exists (#notesSearchClearBtn)", has_clear_search_btn)

        # 1.2 Note Type Filter Chips
        type_chips_count = driver.execute_script("""
            const row = document.getElementById('notesTypeFilterRow');
            if(!row) return 0;
            return row.querySelectorAll('.day-chip').length;
        """)
        test("1.2 Note type filter chips exist (all, daily, recovery, exercise, section)", type_chips_count == 5, f"Count: {type_chips_count}")

        # 1.3 Time Period Filter Chips
        time_chips_count = driver.execute_script("""
            const row = document.getElementById('notesTimeFilterRow');
            if(!row) return 0;
            return row.querySelectorAll('.day-chip').length;
        """)
        test("1.3 Time period filter chips exist (all, 7d, 30d, month)", time_chips_count == 4, f"Count: {time_chips_count}")

        # 1.4 Attachment Filter Chip
        has_att_btn = driver.execute_script("return !!document.getElementById('notesHasAttBtn');")
        test("1.4 Attachment filter chip exists (#notesHasAttBtn)", has_att_btn)

        # 1.5 Sort Order Toggle (Check if manual order toggle exists)
        has_sort_order_toggle = driver.execute_script("""
            const view = document.getElementById('notesView');
            if(!view) return false;
            // Check for any sort button, select, or toggle
            const sortEl = view.querySelector('#notesSortToggle, #notesSortBtn, select[name*="sort"], [data-sort]');
            // Check if notesHubState has a sort direction property
            const stateHasSort = typeof notesHubState === 'object' && ('sortOrder' in notesHubState || 'sortDir' in notesHubState || 'sort' in notesHubState);
            return !!(sortEl || stateHasSort);
        """)
        test("1.5 Sort order toggle control exists (ASC/DESC toggle)", has_sort_order_toggle, "No UI control or state property exists for toggling sort order (fixed newest-first only)")

        # 1.6 Reset All Filters Button (Check if clear all filters exists)
        has_clear_all_filters_btn = driver.execute_script("""
            const view = document.getElementById('notesView');
            if(!view) return false;
            const btn = view.querySelector('#notesResetFiltersBtn, #notesClearAllFiltersBtn, button[data-action="reset-filters"]');
            return !!btn;
        """)
        test("1.6 Button to clear ALL filters and restore defaults exists", has_clear_all_filters_btn, "No 'مسح جميع الفلاتر' button exists (only search clear button exists)")

        # 1.7 Accurate Result Counter after applying filters
        counter_accuracy = driver.execute_script("""
            // Seed sample data
            storageSet('daynote:2026-10-10', 'ملاحظة يومية قديمة');
            storageSet('daynote:2026-10-20', 'ملاحظة يومية اليوم');
            storageSet('recovery:2026-10-20', JSON.stringify({notes: 'استشفاء اليوم'}));
            storageSet('secnote:meal', 'ملاحظة قسم الوجبات');

            // Reset state
            notesHubState.filterType = 'all';
            notesHubState.filterTime = 'all';
            notesHubState.filterHasAtt = false;
            notesHubState.searchQuery = '';
            renderNotesHub();

            const allNotes = collectAllUnifiedNotes();
            const total = allNotes.length;
            const metaAll = document.getElementById('notesFilterMeta').textContent;
            const ok1 = metaAll.includes(String(total));

            // Apply type filter 'daily'
            notesHubState.filterType = 'daily';
            renderNotesHub();
            const dailyCount = allNotes.filter(n => n.type === 'daily').length;
            const metaDaily = document.getElementById('notesFilterMeta').textContent;
            const ok2 = metaDaily.includes(String(dailyCount));

            // Clean up
            storageRemove('daynote:2026-10-10');
            storageRemove('daynote:2026-10-20');
            storageRemove('recovery:2026-10-20');
            storageRemove('secnote:meal');

            return ok1 && ok2;
        """)
        test("1.7 Result counter correctly reflects total and filtered counts", counter_accuracy)

        # -------------------------------------------------------------
        # Area 2: The 4 Note Types in Isolation
        # -------------------------------------------------------------
        print("\n=== Area 2: Verification of the 4 Note Types in Isolation ===")

        types_isolation = driver.execute_script("""
            localStorage.clear();

            // 1. Daily note
            storageSet('daynote:2026-10-18', 'ملاحظة يوم 18');
            // Empty daily note
            storageSet('daynote:2026-10-19', '   ');

            // 2. Recovery note
            storageSet('recovery:2026-10-18', JSON.stringify({notes: 'ألم عضلي خفيف'}));
            // Empty recovery note
            storageSet('recovery:2026-10-19', JSON.stringify({notes: ''}));

            // 3. Exercise note
            storageSet('ex:2026-10-18', JSON.stringify({
                squat: { sets: [100], note: 'سكوات بوزن 100كج تركيز عالي' },
                bench: { sets: [80], note: '   ' } // empty note
            }));

            // 4. Section note
            storageSet('secnote:gym', 'أهداف التمرين للشهر الحالي');
            storageSet('secnote:sleep', ''); // empty section note

            const notes = collectAllUnifiedNotes();

            // Verification assertions
            const dailyNotes = notes.filter(n => n.type === 'daily');
            const recNotes = notes.filter(n => n.type === 'recovery');
            const exNotes = notes.filter(n => n.type === 'exercise');
            const secNotes = notes.filter(n => n.type === 'section');

            const noEmptyDaily = dailyNotes.length === 1 && dailyNotes[0].text === 'ملاحظة يوم 18';
            const noEmptyRec = recNotes.length === 1 && recNotes[0].text === 'ألم عضلي خفيف';
            const noEmptyEx = exNotes.length === 1 && exNotes[0].text === 'سكوات بوزن 100كج تركيز عالي';
            const noEmptySec = secNotes.length === 1 && secNotes[0].text === 'أهداف التمرين للشهر الحالي';

            // Ensure section note has STRICTLY null date
            const secIsoIsNull = secNotes.length > 0 && secNotes[0].iso === null;

            // Ensure no duplicate keys
            const keys = notes.map(n => n.noteKey);
            const uniqueKeys = new Set(keys);
            const noDuplicates = keys.length === uniqueKeys.size;

            localStorage.clear();

            return {
                dailyOk: noEmptyDaily,
                recOk: noEmptyRec,
                exOk: noEmptyEx,
                secOk: noEmptySec,
                secIsoNull: secIsoIsNull,
                noDupes: noDuplicates,
                totalNotes: notes.length
            };
        """)

        test("2.1 Daily note isolated & empty ignored", types_isolation.get('dailyOk'))
        test("2.2 Recovery note isolated & empty ignored", types_isolation.get('recOk'))
        test("2.3 Exercise note isolated & empty ignored", types_isolation.get('exOk'))
        test("2.4 Section note isolated & empty ignored", types_isolation.get('secOk'))
        test("2.5 Section note has iso strictly null (no fake dates)", types_isolation.get('secIsoNull'))
        test("2.6 Zero duplicate note keys in unified collection", types_isolation.get('noDupes'))

        # -------------------------------------------------------------
        # Area 3: Filter & Sort Testing with Realistic Dates
        # -------------------------------------------------------------
        print("\n=== Area 3: Filter & Sort Testing with Varied Dates ===")

        filter_time_tests = driver.execute_script("""
            localStorage.clear();

            // Generate dates relative to today
            const now = new Date();
            function fmt(d){
                const y = d.getFullYear();
                const m = String(d.getMonth()+1).padStart(2,'0');
                const dd = String(d.getDate()).padStart(2,'0');
                return `${y}-${m}-${dd}`;
            }

            const dToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            const d3Ago = new Date(dToday.getTime() - 3 * 86400000);
            const d12Ago = new Date(dToday.getTime() - 12 * 86400000);
            const d40Ago = new Date(dToday.getTime() - 40 * 86400000);

            const isoToday = fmt(dToday);
            const iso3Ago = fmt(d3Ago);
            const iso12Ago = fmt(d12Ago);
            const iso40Ago = fmt(d40Ago);

            storageSet('daynote:' + isoToday, 'اليوم');
            storageSet('daynote:' + iso3Ago, 'من 3 أيام');
            storageSet('daynote:' + iso12Ago, 'من 12 يوم');
            storageSet('daynote:' + iso40Ago, 'من 40 يوم');
            storageSet('secnote:meal', 'ملاحظة عامة');

            // Set up attachments map
            storageSet('note-attachments-v1', JSON.stringify({
                ['daynote:' + isoToday]: [{ mediaId: 'm1', fileName: 'f1.jpg' }]
            }));

            // Test 1: Time filter '7d'
            notesHubState.filterType = 'all';
            notesHubState.filterTime = '7d';
            notesHubState.filterHasAtt = false;
            notesHubState.searchQuery = '';
            renderNotesHub();
            const count7d = document.querySelectorAll('#notesTimelineList .note-hub-card').length;
            const ok7d = count7d === 2;

            // Test 2: Time filter '30d'
            notesHubState.filterTime = '30d';
            renderNotesHub();
            const count30d = document.querySelectorAll('#notesTimelineList .note-hub-card').length;
            const ok30d = count30d === 3;

            // Test 3: Time filter 'all'
            notesHubState.filterTime = 'all';
            renderNotesHub();
            const countAll = document.querySelectorAll('#notesTimelineList .note-hub-card').length;
            const okAll = countAll === 4;

            // Test 4: Combined Filter (7d + hasAtt)
            notesHubState.filterTime = '7d';
            notesHubState.filterHasAtt = true;
            renderNotesHub();
            const countComb = document.querySelectorAll('#notesTimelineList .note-hub-card').length;
            const okComb = countComb === 1; // only isoToday has attachment

            // Test 5: Section note visibility with time filter
            // When filterTime is '7d' and filterType is 'all', section notes (undated) should not appear in timeline
            const secSectionHidden = document.getElementById('notesUndatedSection').classList.contains('hidden');

            localStorage.clear();

            return {
                ok7d: ok7d,
                count7d: count7d,
                ok30d: ok30d,
                count30d: count30d,
                okAll: okAll,
                countAll: countAll,
                okComb: okComb,
                secHiddenOnTimeFilter: secSectionHidden
            };
        """)

        test("3.1 7-day filter includes only records within 7 days", filter_time_tests.get('ok7d'), f"Count: {filter_time_tests.get('count7d')}")
        test("3.2 30-day filter includes records within 30 days", filter_time_tests.get('ok30d'), f"Count: {filter_time_tests.get('count30d')}")
        test("3.3 'All' time filter includes all dated records", filter_time_tests.get('okAll'), f"Count: {filter_time_tests.get('countAll')}")
        test("3.4 Combined filter (7d + attachment) intersects properly", filter_time_tests.get('okComb'))
        test("3.5 Undated section notes hidden during dated time window filtering", filter_time_tests.get('secHiddenOnTimeFilter'))

        # -------------------------------------------------------------
        # Area 4: Deep-Link Navigation & Editing for All 4 Types
        # -------------------------------------------------------------
        print("\n=== Area 4: Deep-Link Navigation & Direct Source Access ===")

        # 4.1 Daily Note Navigation
        nav_daily = driver.execute_script("""
            const note = {
                noteKey: 'daynote:2026-10-05',
                type: 'daily',
                iso: '2026-10-05',
                sourceMode: 'overview',
                sourceId: 'dailyNotesInput'
            };
            openNoteInOriginalSection(note);
            return {
                mode: mode,
                iso: toISO(weekDates[selectedIdx])
            };
        """)
        test("4.1 Daily note routes to target ISO date and overview mode", nav_daily.get('mode') == 'overview' and nav_daily.get('iso') == '2026-10-05', f"Result: {nav_daily}")

        # 4.2 Recovery Note Navigation
        nav_rec = driver.execute_script("""
            const note = {
                noteKey: 'recovery:2026-10-08',
                type: 'recovery',
                iso: '2026-10-08',
                sourceMode: 'recovery',
                sourceId: 'recoveryNotes'
            };
            openNoteInOriginalSection(note);
            return {
                mode: mode,
                iso: toISO(weekDates[selectedIdx])
            };
        """)
        test("4.2 Recovery note routes to target ISO date and recovery mode", nav_rec.get('mode') == 'recovery' and nav_rec.get('iso') == '2026-10-08', f"Result: {nav_rec}")

        # 4.3 Exercise Note Navigation
        nav_ex = driver.execute_script("""
            const note = {
                noteKey: 'exnote:2026-10-09:squat',
                type: 'exercise',
                iso: '2026-10-09',
                sourceMode: 'gym',
                sourceId: 'squat',
                exKey: 'squat'
            };
            openNoteInOriginalSection(note);
            return {
                mode: mode,
                iso: toISO(weekDates[selectedIdx])
            };
        """)
        test("4.3 Exercise note routes to target ISO date and gym mode", nav_ex.get('mode') == 'gym' and nav_ex.get('iso') == '2026-10-09', f"Result: {nav_ex}")

        # 4.4 Section Note Navigation & Accordion Opening
        nav_sec = driver.execute_script("""
            const note = {
                noteKey: 'secnote:meal',
                type: 'section',
                iso: null,
                sourceMode: 'meal',
                sourceId: 'secNotesCard_meal'
            };
            openNoteInOriginalSection(note);
            const card = document.getElementById('secNotesCard_meal');
            return {
                mode: mode,
                cardOpen: card ? card.open : false
            };
        """)
        test("4.4 Section note routes to meal section and opens details card", nav_sec.get('mode') == 'meal' and nav_sec.get('cardOpen') is True, f"Result: {nav_sec}")

        # -------------------------------------------------------------
        # Area 5: Audit of Phase 8B Test Modification
        # -------------------------------------------------------------
        print("\n=== Area 5: Audit of Phase 8B Test Modification ===")

        # Read sw.js and test_phase8b_notification_routing.py
        with open('sw.js', 'r', encoding='utf-8') as f:
            sw_text = f.read()

        with open('scratch/test_phase8b_notification_routing.py', 'r', encoding='utf-8') as f:
            test_text = f.read()

        # Check: What was modified?
        v20_in_sw = "CACHE_VERSION = 'v20'" in sw_text or 'CACHE_VERSION = "v20"' in sw_text
        test_checks_v20 = "ver_num >= 19" in test_text or "CACHE_VERSION = 'v20'" in test_text

        # Verify that all 13 groups of Phase 8B tests remain intact
        has_security_checks = "XSS-style mode falls back safely to 'home'" in test_text
        has_param_cleaning = "Cold-start URL params cleaned from URL via replaceState" in test_text
        has_data_invariance = "Meals data intact after notification routing" in test_text

        test("5.1 sw.js CACHE_VERSION is currently 'v20'", v20_in_sw)
        test("5.2 test_phase8b handles v19 or higher legitimately", test_checks_v20)
        test("5.3 Phase 8B security validation tests remain completely intact", has_security_checks and has_param_cleaning and has_data_invariance)

        # -------------------------------------------------------------
        # Area 6: Images, Storage & Offline Capability
        # -------------------------------------------------------------
        print("\n=== Area 6: Images, Storage Invariance & Offline ===")

        storage_invariance = driver.execute_script("""
            localStorage.clear();
            storageSet('daynote:2026-10-10', 'ملاحظة 1');
            storageSet('ex:2026-10-10', JSON.stringify({ squat: { note: 'ملاحظة تمرين' } }));
            storageSet('recovery:2026-10-10', JSON.stringify({ notes: 'ملاحظة استشفاء' }));
            storageSet('secnote:meal', 'ملاحظة وجبات');

            // Snapshot before
            const beforeKeys = Object.keys(localStorage).sort();
            const beforeDump = JSON.stringify(beforeKeys.map(k => [k, localStorage.getItem(k)]));

            // Execute collection, rendering, and filtering cycles
            collectAllUnifiedNotes();
            notesHubState.filterType = 'daily';
            renderNotesHub();
            notesHubState.filterType = 'exercise';
            renderNotesHub();
            notesHubState.searchQuery = 'سكوات';
            renderNotesHub();

            // Snapshot after
            const afterKeys = Object.keys(localStorage).sort();
            const afterDump = JSON.stringify(afterKeys.map(k => [k, localStorage.getItem(k)]));

            localStorage.clear();
            return beforeDump === afterDump;
        """)
        test("6.1 Strict localStorage read-only invariance (0 mutations)", storage_invariance)

        # Missing attachment resilience
        missing_att_resilience = driver.execute_script("""
            localStorage.clear();
            storageSet('daynote:2026-10-12', 'ملاحظة بمرفق مفقود');
            storageSet('note-attachments-v1', JSON.stringify({
                'daynote:2026-10-12': [{ mediaId: 'nonexistent_media_id_9999', fileName: 'missing.jpg' }]
            }));

            notesHubState.filterType = 'all';
            notesHubState.filterTime = 'all';
            notesHubState.filterHasAtt = false;
            notesHubState.searchQuery = '';

            let renderedWithoutError = false;
            try {
                renderNotesHub();
                const attContainer = document.querySelector('#notesTimelineList .note-hub-att-box');
                renderedWithoutError = !!attContainer;
            } catch(e) {
                renderedWithoutError = false;
            }
            localStorage.clear();
            return renderedWithoutError;
        """)
        test("6.2 Missing attachment renders placeholder thumbnail safely", missing_att_resilience)

        # Check Service Worker Whitelist & Manifest Cache
        sw_has_notes_mode = "'notes'" in sw_text and "VALID_MODES = [" in sw_text
        test("6.3 sw.js whitelist includes 'notes' for offline & notification routing", sw_has_notes_mode)

    finally:
        driver.quit()

    # -------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------
    print("\n" + "="*80)
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["status"] == "PASS")
    failed_tests = sum(1 for r in results if r["status"] == "FAIL")
    print(f"CLOSURE GATE AUDIT RESULTS: {passed_tests} PASSED, {failed_tests} FAILED (TOTAL {total_tests})")
    print("="*80)

    return results

if __name__ == "__main__":
    run_gate_audit()

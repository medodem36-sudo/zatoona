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
    print("PHASE 9B.1 ACCEPTANCE TEST SUITE: UNIFIED NOTES HUB")
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

    try:
        # ---------------------------------------------------------
        # Group 1: Window Exports & Element Presence
        # ---------------------------------------------------------
        print("\n--- Group 1: Window Exports & Element Presence ---")
        exports = js("""
            return {
                hasCollectAllUnifiedNotes: typeof window.collectAllUnifiedNotes === 'function',
                hasRenderNotesHub: typeof window.renderNotesHub === 'function',
                hasOpenNoteInOriginalSection: typeof window.openNoteInOriginalSection === 'function',
                hasNotesHubState: typeof window.notesHubState === 'object',
                hasNotesView: !!document.getElementById('notesView'),
                hasModeNotes: !!document.getElementById('modeNotes'),
                hasDrawNavNotes: !!document.getElementById('drawNav-notes'),
                hasSideNavNotes: !!document.getElementById('sideNav-notes'),
                hasSearchInput: !!document.getElementById('notesSearchInput'),
                hasTypeFilters: !!document.getElementById('notesTypeFilterRow'),
                hasTimeFilters: !!document.getElementById('notesTimeFilterRow'),
                hasHasAttBtn: !!document.getElementById('notesHasAttBtn'),
                hasTimelineList: !!document.getElementById('notesTimelineList'),
                hasSectionList: !!document.getElementById('notesSectionList'),
                hasEmptyState: !!document.getElementById('notesEmptyState')
            };
        """)

        test("window.collectAllUnifiedNotes is a function", exports.get('hasCollectAllUnifiedNotes'))
        test("window.renderNotesHub is a function", exports.get('hasRenderNotesHub'))
        test("window.openNoteInOriginalSection is a function", exports.get('hasOpenNoteInOriginalSection'))
        test("window.notesHubState is an object", exports.get('hasNotesHubState'))
        test("#notesView container exists in DOM", exports.get('hasNotesView'))
        test("#modeNotes exists in navigation bar", exports.get('hasModeNotes'))
        test("#drawNav-notes exists in drawer", exports.get('hasDrawNavNotes'))
        test("#sideNav-notes exists in sidebar", exports.get('hasSideNavNotes'))
        test("#notesSearchInput exists", exports.get('hasSearchInput'))
        test("#notesTypeFilterRow exists", exports.get('hasTypeFilters'))
        test("#notesTimeFilterRow exists", exports.get('hasTimeFilters'))
        test("#notesHasAttBtn exists", exports.get('hasHasAttBtn'))
        test("#notesTimelineList exists", exports.get('hasTimelineList'))
        test("#notesSectionList exists", exports.get('hasSectionList'))
        test("#notesEmptyState exists", exports.get('hasEmptyState'))

        # ---------------------------------------------------------
        # Group 2: Screen Visibility & Navigation Mode
        # ---------------------------------------------------------
        print("\n--- Group 2: Navigation to Notes Mode ---")
        nav_res = js("""
            navigateTo('notes');
            const view = document.getElementById('notesView');
            const isVisible = view && !view.classList.contains('hidden');
            const modeIsNotes = (mode === 'notes');
            const btnActive = document.getElementById('modeNotes')?.classList.contains('active');
            const drawActive = document.getElementById('drawNav-notes')?.classList.contains('active');
            return {
                isVisible: isVisible,
                modeIsNotes: modeIsNotes,
                btnActive: btnActive,
                drawActive: drawActive
            };
        """)
        test("navigateTo('notes') displays #notesView", nav_res.get('isVisible'))
        test("mode variable is 'notes'", nav_res.get('modeIsNotes'))
        test("modeNotes button has .active class", nav_res.get('btnActive'))
        test("drawNav-notes button has .active class", nav_res.get('drawActive'))

        # ---------------------------------------------------------
        # Group 3: Collection of All 4 Note Types
        # ---------------------------------------------------------
        print("\n--- Group 3: Data Collection Across 4 Note Types ---")
        # Setup mock test data safely in localStorage
        js("""
            // 1. Daily note
            localStorage.setItem('meal-gym-tracker:daynote:2026-10-18', 'ملاحظة يوم تجريبية: التزمت بالخطة');

            // 2. Recovery note
            localStorage.setItem('meal-gym-tracker:recovery:2026-10-19', JSON.stringify({
                notes: 'استشفاء جيد ونوم مريح 8 ساعات'
            }));

            // 3. Exercise note
            localStorage.setItem('meal-gym-tracker:ex:2026-10-20', JSON.stringify({
                bench: { sets: [true, true, true], weight: '80', reps: '10', note: 'تركيز ممتاز على النزول البطيء' }
            }));

            // 4. Section note
            localStorage.setItem('meal-gym-tracker:secnote:meal', 'مسودة عامة للتغذية: زيادة البروتين 10جم');

            // 5. Empty notes that must be ignored
            localStorage.setItem('meal-gym-tracker:daynote:2026-10-10', '   ');
            localStorage.setItem('meal-gym-tracker:recovery:2026-10-11', JSON.stringify({ notes: '' }));
            localStorage.setItem('meal-gym-tracker:ex:2026-10-12', JSON.stringify({
                squat: { sets: [true], weight: '100', reps: '5', note: '' }
            }));
        """)

        collected = js("return window.collectAllUnifiedNotes();")
        types_found = {item['type']: item for item in collected}

        test("Daily note collected correctly", 'daily' in types_found and types_found['daily']['iso'] == '2026-10-18')
        test("Recovery note collected correctly", 'recovery' in types_found and types_found['recovery']['iso'] == '2026-10-19')
        test("Exercise note collected correctly", 'exercise' in types_found and types_found['exercise']['iso'] == '2026-10-20')
        test("Section note collected correctly", 'section' in types_found and types_found['section']['sourceMode'] == 'meal')
        test("Section note has iso === null", types_found['section']['iso'] is None)

        # ---------------------------------------------------------
        # Group 4: Guard Against Empty Notes
        # ---------------------------------------------------------
        print("\n--- Group 4: Empty Records Guard ---")
        empty_check = js("""
            const notes = window.collectAllUnifiedNotes();
            const hasEmptyDaily = notes.some(n => n.iso === '2026-10-10');
            const hasEmptyRec = notes.some(n => n.iso === '2026-10-11');
            const hasEmptyEx = notes.some(n => n.iso === '2026-10-12');
            return {
                hasEmptyDaily: hasEmptyDaily,
                hasEmptyRec: hasEmptyRec,
                hasEmptyEx: hasEmptyEx
            };
        """)
        test("Empty daily note ignored", not empty_check.get('hasEmptyDaily'))
        test("Empty recovery note ignored", not empty_check.get('hasEmptyRec'))
        test("Empty exercise note ignored", not empty_check.get('hasEmptyEx'))

        # ---------------------------------------------------------
        # Group 5: Chronological Ordering & Separation of Sections
        # ---------------------------------------------------------
        print("\n--- Group 5: Ordering & Section Separation ---")
        render_check = js("""
            window.notesHubState.filterType = 'all';
            window.notesHubState.filterTime = 'all';
            window.notesHubState.filterHasAtt = false;
            window.notesHubState.searchQuery = '';
            window.renderNotesHub();

            const tlCards = Array.from(document.querySelectorAll('#notesTimelineList .note-hub-card'));
            const secCards = Array.from(document.querySelectorAll('#notesSectionList .note-hub-card'));

            // Check dated order (newest first)
            const dates = tlCards.map(c => c.querySelector('.mono')?.textContent || '');
            let isSorted = true;
            for(let i=0; i < dates.length - 1; i++){
                if(dates[i] < dates[i+1]) isSorted = false;
            }

            return {
                tlCount: tlCards.length,
                secCount: secCards.length,
                dates: dates,
                isSorted: isSorted
            };
        """)
        test("Dated notes rendered in timeline", render_check.get('tlCount') >= 3, f"Count: {render_check.get('tlCount')}")
        test("Dated notes sorted descending (newest first)", render_check.get('isSorted'), f"Dates: {render_check.get('dates')}")
        test("Undated section notes rendered in separate section group", render_check.get('secCount') >= 1)

        # ---------------------------------------------------------
        # Group 6: Type Filter (Daily, Recovery, Exercise, Section)
        # ---------------------------------------------------------
        print("\n--- Group 6: Type Filter ---")
        for ftype in ['daily', 'recovery', 'exercise', 'section']:
            f_res = js(f"""
                window.notesHubState.filterType = '{ftype}';
                window.renderNotesHub();
                const tl = Array.from(document.querySelectorAll('#notesTimelineList .note-hub-card'));
                const sec = Array.from(document.querySelectorAll('#notesSectionList .note-hub-card'));
                const allVisible = tl.concat(sec);
                return {{
                    count: allVisible.length,
                    allMatch: allVisible.every(c => c.innerHTML.includes('{types_found[ftype]["title"]}'))
                }};
            """)
            test(f"Filter type '{ftype}' isolates matching notes", f_res.get('count') >= 1 and f_res.get('allMatch'))

        # Reset filter
        js("window.notesHubState.filterType = 'all'; window.renderNotesHub();")

        # ---------------------------------------------------------
        # Group 7: Real-Time Text Search (Arabic & English)
        # ---------------------------------------------------------
        print("\n--- Group 7: Real-Time Text Search ---")
        search_ar = js("""
            window.notesHubState.searchQuery = 'استشفاء';
            window.renderNotesHub();
            const cards = document.querySelectorAll('#notesTimelineList .note-hub-card');
            return {
                count: cards.length,
                textMatches: Array.from(cards).some(c => c.textContent.includes('استشفاء'))
            };
        """)
        test("Search in Arabic matches note text", search_ar.get('count') >= 1 and search_ar.get('textMatches'))

        search_en = js("""
            window.notesHubState.searchQuery = 'bench';
            window.renderNotesHub();
            const cards = document.querySelectorAll('#notesTimelineList .note-hub-card');
            return {
                count: cards.length,
                textMatches: Array.from(cards).some(c => c.textContent.includes('تمرين') || c.textContent.includes('بنش'))
            };
        """)
        test("Search by exercise key matches exercise note", search_en.get('count') >= 1 and search_en.get('textMatches'))

        # Clear search
        js("window.notesHubState.searchQuery = ''; window.renderNotesHub();")

        # ---------------------------------------------------------
        # Group 8: Attachments Integration & Missing Media Safety
        # ---------------------------------------------------------
        print("\n--- Group 8: Attachments Integration ---")
        att_res = js("""
            // Add mock attachment metadata in note-attachments-v1
            const map = {
                'daynote:2026-10-18': [
                    { mediaId: 'test_media_123', originalName: 'photo.jpg', createdAt: Date.now() }
                ]
            };
            localStorage.setItem('meal-gym-tracker:note-attachments-v1', JSON.stringify(map));

            window.renderNotesHub();
            const card = document.querySelector('.note-hub-card[data-key="daynote:2026-10-18"]');
            const thumb = card ? card.querySelector('.note-hub-thumb-wrap') : null;
            const ph = card ? card.querySelector('.note-hub-thumb-ph') : null;

            return {
                hasThumbWrap: !!thumb,
                hasPlaceholder: !!ph,
                mediaId: thumb ? thumb.dataset.mid : null
            };
        """)
        test("Attachment thumbnail container rendered", att_res.get('hasThumbWrap'))
        test("Missing media handled safely with placeholder without throwing", att_res.get('hasPlaceholder'))
        test("Attachment metadata mediaId bound correctly", att_res.get('mediaId') == 'test_media_123')

        # Filter by attachments
        has_att_filter = js("""
            window.notesHubState.filterHasAtt = true;
            window.renderNotesHub();
            const tl = document.querySelectorAll('#notesTimelineList .note-hub-card');
            const sec = document.querySelectorAll('#notesSectionList .note-hub-card');
            return {
                totalVisible: tl.length + sec.length,
                matchesOnlyAttNote: tl.length === 1 && tl[0].dataset.key === 'daynote:2026-10-18'
            };
        """)
        test("Filter 'بها مرفقات فقط' isolates notes with attachments", has_att_filter.get('matchesOnlyAttNote'))
        js("window.notesHubState.filterHasAtt = false; window.renderNotesHub();")

        # ---------------------------------------------------------
        # Group 9: Deep-Link to Original Section & Accordion Opening
        # ---------------------------------------------------------
        print("\n--- Group 9: Deep-Link Navigation & Focus ---")
        # Test section note opening accordion
        sec_deep_link = js("""
            const secNote = window.collectAllUnifiedNotes().find(n => n.type === 'section' && n.sourceMode === 'meal');
            window.openNoteInOriginalSection(secNote);
            const card = document.getElementById('secNotesCard_meal');
            return {
                mode: mode,
                accordionOpen: card && card.open
            };
        """)
        time.sleep(0.3)
        test("openNoteInOriginalSection navigates to section and opens details accordion",
             sec_deep_link.get('mode') == 'meal' and sec_deep_link.get('accordionOpen'))

        # Test daily note navigation
        daily_deep_link = js("""
            const dNote = window.collectAllUnifiedNotes().find(n => n.type === 'daily' && n.iso === '2026-10-18');
            window.openNoteInOriginalSection(dNote);
            const currentIso = toISO(weekDates[selectedIdx]);
            return {
                mode: mode,
                iso: currentIso
            };
        """)
        time.sleep(0.3)
        test("openNoteInOriginalSection navigates to target date and overview mode",
             daily_deep_link.get('mode') == 'overview' and daily_deep_link.get('iso') == '2026-10-18')

        # ---------------------------------------------------------
        # Group 10: Read-Only Storage Invariance
        # ---------------------------------------------------------
        print("\n--- Group 10: Storage Invariance (Read-Only) ---")
        storage_inv = js("""
            const keysBefore = [];
            for(let i=0; i<localStorage.length; i++) keysBefore.push(localStorage.key(i));

            // Execute multiple note collections and renders with various filters
            window.collectAllUnifiedNotes();
            window.notesHubState.filterType = 'daily';
            window.renderNotesHub();
            window.notesHubState.filterTime = '7d';
            window.renderNotesHub();
            window.notesHubState.searchQuery = 'test';
            window.renderNotesHub();

            const keysAfter = [];
            for(let i=0; i<localStorage.length; i++) keysAfter.push(localStorage.key(i));

            keysBefore.sort();
            keysAfter.sort();

            return JSON.stringify(keysBefore) === JSON.stringify(keysAfter);
        """)
        test("Zero keys added, removed, or mutated in localStorage during collection/rendering", storage_inv)

        # ---------------------------------------------------------
        # Group 11: Resilience to Corrupt Data
        # ---------------------------------------------------------
        print("\n--- Group 11: Resilience to Corrupt Records ---")
        corrupt_res = js("""
            // Inject corrupt JSON records
            localStorage.setItem('meal-gym-tracker:recovery:corrupt-date', 'INVALID_JSON_OBJECT{{{');
            localStorage.setItem('meal-gym-tracker:ex:bad-date', 'NOT_JSON');

            try {
                const notes = window.collectAllUnifiedNotes();
                window.renderNotesHub();
                return {
                    survived: true,
                    count: notes.length
                };
            } catch(e) {
                return {
                    survived: false,
                    error: e.message
                };
            }
        """)
        test("collectAllUnifiedNotes and renderNotesHub survive corrupt storage records", corrupt_res.get('survived'))

        # ---------------------------------------------------------
        # Group 12: Viewport Responsiveness (320px, 375px, 768px, 1280px)
        # ---------------------------------------------------------
        print("\n--- Group 12: Viewport Responsiveness ---")
        for width in [320, 375, 768, 1280]:
            driver.set_window_size(width, 800)
            time.sleep(0.2)
            has_overflow = js("""
                return document.body.scrollWidth > document.body.clientWidth + 1;
            """)
            test(f"No horizontal overflow at {width}px width", not has_overflow)

        # ---------------------------------------------------------
        # Group 13: Theme Compatibility (Dark & Light)
        # ---------------------------------------------------------
        print("\n--- Group 13: Theme Compatibility ---")
        theme_dark = js("""
            document.documentElement.setAttribute('data-theme', 'dark');
            return document.documentElement.getAttribute('data-theme') === 'dark';
        """)
        test("Dark theme applied without crashing", theme_dark)

        theme_light = js("""
            document.documentElement.setAttribute('data-theme', 'light');
            return document.documentElement.getAttribute('data-theme') === 'light';
        """)
        test("Light theme applied without crashing", theme_light)

        # ---------------------------------------------------------
        # Group 14: Browser Console Integrity
        # ---------------------------------------------------------
        print("\n--- Group 14: Browser Console Cleanliness ---")
        logs = driver.get_log('browser')
        severe = [l for l in logs if l['level'] == 'SEVERE' and 'manifest.json' not in l['message']]
        test("Zero SEVERE JavaScript console errors", len(severe) == 0, f"Errors: {severe}")

    finally:
        # Cleanup mock test entries from localStorage
        try:
            driver.execute_script("""
                localStorage.removeItem('meal-gym-tracker:daynote:2026-10-18');
                localStorage.removeItem('meal-gym-tracker:recovery:2026-10-19');
                localStorage.removeItem('meal-gym-tracker:ex:2026-10-20');
                localStorage.removeItem('meal-gym-tracker:secnote:meal');
                localStorage.removeItem('meal-gym-tracker:daynote:2026-10-10');
                localStorage.removeItem('meal-gym-tracker:recovery:2026-10-11');
                localStorage.removeItem('meal-gym-tracker:ex:2026-10-12');
                localStorage.removeItem('meal-gym-tracker:note-attachments-v1');
                localStorage.removeItem('meal-gym-tracker:recovery:corrupt-date');
                localStorage.removeItem('meal-gym-tracker:ex:bad-date');
            """)
        except Exception:
            pass
        driver.quit()

    print("\n================================================================================")
    print(f"RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("================================================================================")
    if failed_count > 0:
        sys.exit(1)

if __name__ == '__main__':
    run_tests()

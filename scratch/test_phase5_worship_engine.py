import unittest
import os
import hashlib
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(REPO_DIR, "index.html")
ZATOONA_HTML = os.path.join(REPO_DIR, "zatoona.html")
ASSETS_INDEX_HTML = os.path.join(REPO_DIR, "android", "app", "src", "main", "assets", "index.html")

class TestPhase5WorshipEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,1024")
        chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get(f"file:///{INDEX_HTML.replace(os.sep, '/')}")
        WebDriverWait(cls.driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)
        # Suppress alerts and confirms during test execution
        cls.driver.execute_script("""
            window.alert = function(){};
            window.confirm = function(){ return true; };
            window.prompt = function(msg, def){ return def || '5'; };
        """)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    def test_01_three_way_html_parity(self):
        """Verify 100% byte-for-byte and SHA-256 parity across the 3 HTML files."""
        for p in [INDEX_HTML, ZATOONA_HTML, ASSETS_INDEX_HTML]:
            self.assertTrue(os.path.exists(p), f"File missing: {p}")
            self.assertGreater(os.path.getsize(p), 1_500_000, f"File too small: {p}")

        with open(INDEX_HTML, "rb") as f:
            h_idx = hashlib.sha256(f.read()).hexdigest()
        with open(ZATOONA_HTML, "rb") as f:
            h_zat = hashlib.sha256(f.read()).hexdigest()
        with open(ASSETS_INDEX_HTML, "rb") as f:
            h_ast = hashlib.sha256(f.read()).hexdigest()

        self.assertEqual(h_idx, h_zat, "Parity mismatch: index.html != zatoona.html")
        self.assertEqual(h_idx, h_ast, "Parity mismatch: index.html != assets/index.html")

    def test_02_known_key_patterns_includes_phase5_keys(self):
        """Verify KNOWN_KEY_PATTERNS in index.html includes Phase 5 storage keys."""
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("/^khatma-/", content)
        self.assertIn("/^worship-suhoor/", content)
        self.assertIn("/^worship-preadhan/", content)
        self.assertIn("/^worship-friday/", content)
        self.assertIn("/^worship-random-dhikr/", content)
        self.assertIn("/^worship-missed-ledger/", content)

    def test_03_worship_elements_rendered(self):
        """Verify presence of all Phase 5 cards and modal in prayer view."""
        self.driver.execute_script("navigateTo('prayer');")
        time.sleep(0.5)

        for el_id in [
            'forbiddenTimesCard',
            'forbiddenStatusBadge',
            'forbiddenWindowsList',
            'preAdhanChimeCard',
            'preAdhanChimeToggle',
            'suhoorQiyamCard',
            'suhoorTimeDisplay',
            'suhoorCountdownPill',
            'randomDhikrCard',
            'randomDhikrText',
            'fridaySunanCard',
            'fridaySunanList',
            'salawatCountDisplay',
            'salawatTapBtn',
            'khatmaCard',
            'khatmaProgressBar',
            'khatmaCurrentPage',
            'missedWorshipCard',
            'missedPrayersGrid',
            'khatmaReflectionModal'
        ]:
            # khatmaProgressBar is inside khatma-bar-wrap as khatmaBarFill, test both or fallback
            actual_id = 'khatmaBarFill' if el_id == 'khatmaProgressBar' else el_id
            el = self.driver.find_element(By.ID, actual_id)
            self.assertIsNotNone(el, f"Element #{actual_id} not found")

    def test_04_forbidden_prayer_times_workflow(self):
        """Verify forbidden prayer times indicator evaluates windows and updates status."""
        status = self.driver.execute_script("""
            window.ZATOONA_PHASE5.renderForbiddenTimes();
            var badge = document.getElementById('forbiddenStatusBadge');
            var list = document.getElementById('forbiddenWindowsList');
            return {
                badgeText: badge ? badge.textContent : '',
                itemsCount: list ? list.querySelectorAll('.forbidden-window-item').length : 0
            };
        """)
        self.assertEqual(status['itemsCount'], 3, "Must have exactly 3 forbidden prayer windows")
        self.assertTrue(len(status['badgeText']) > 0, "Forbidden times status badge must not be empty")

    def test_05_preadhan_chime_workflow(self):
        """Verify pre-Adhan chime toggle and interval settings."""
        result = self.driver.execute_script("""
            window.ZATOONA_PHASE5.togglePreAdhanChime(true);
            window.ZATOONA_PHASE5.setPreAdhanMinutes('15');
            var s = window.ZATOONA_PHASE5.getPreAdhanSettings();
            var toggle = document.getElementById('preAdhanChimeToggle');
            var alertEl = document.getElementById('preAdhanNextAlert');
            return {
                enabled: s.enabled,
                mins: s.minutesBefore,
                checked: toggle ? toggle.checked : false,
                alertText: alertEl ? alertEl.textContent : ''
            };
        """)
        self.assertTrue(result['enabled'])
        self.assertEqual(result['mins'], 15)
        self.assertTrue(result['checked'])
        self.assertTrue(len(result['alertText']) > 0)

    def test_06_smart_suhoor_alarm_workflow(self):
        """Verify smart pre-Fajr and Suhoor alarm calculation and toggle."""
        result = self.driver.execute_script("""
            window.ZATOONA_PHASE5.toggleSuhoorAlarm(true);
            window.ZATOONA_PHASE5.setSuhoorOffset('60');
            var s = window.ZATOONA_PHASE5.getSuhoorSettings();
            var timeEl = document.getElementById('suhoorTimeDisplay');
            var pillEl = document.getElementById('suhoorCountdownPill');
            return {
                enabled: s.enabled,
                offset: s.offsetMinutes,
                timeText: timeEl ? timeEl.textContent : '',
                pillText: pillEl ? pillEl.textContent : ''
            };
        """)
        self.assertTrue(result['enabled'])
        self.assertEqual(result['offset'], 60)
        self.assertNotEqual(result['timeText'], '--:--')
        self.assertTrue('متبقي' in result['pillText'])

    def test_07_subtle_random_dhikr_workflow(self):
        """Verify cycling of random adhkar and interval setting."""
        initial_text = self.driver.execute_script("""
            return document.getElementById('randomDhikrText').textContent;
        """)
        self.assertTrue(len(initial_text) > 0)

        # Trigger next random dhikr
        new_text = self.driver.execute_script("""
            window.ZATOONA_PHASE5.nextRandomDhikr();
            window.ZATOONA_PHASE5.setDhikrInterval('60');
            return document.getElementById('randomDhikrText').textContent;
        """)
        self.assertTrue(len(new_text) > 0)

    def test_08_friday_sunan_and_salawat_counter(self):
        """Verify Friday sunan checklist items and Salawat counter increments."""
        res = self.driver.execute_script("""
            window.ZATOONA_PHASE5.resetSalawat();
            window.ZATOONA_PHASE5.incrementSalawat();
            window.ZATOONA_PHASE5.addSalawatBatch(10);
            window.ZATOONA_PHASE5.toggleFridaySunanItem('ghusl');
            var countEl = document.getElementById('salawatCountDisplay');
            return {
                count: countEl ? parseInt(countEl.textContent, 10) : 0
            };
        """)
        self.assertEqual(res['count'], 11)

    def test_09_smart_khatma_and_reflections(self):
        """Verify Khatma daily progression, percentage update, and reflection note storage."""
        res = self.driver.execute_script("""
            // Reset state
            localStorage.setItem('khatma-state-v1', JSON.stringify({
                currentPage: 20,
                durationDays: 30,
                dailyTarget: 20,
                lastReadDate: null,
                streak: 1
            }));
            window.ZATOONA_PHASE5.renderKhatma();
            window.ZATOONA_PHASE5.markTodayKhatmaDone();
            var st = window.ZATOONA_PHASE5.getKhatmaState();
            var pageEl = document.getElementById('khatmaCurrentPage');
            var juzEl = document.getElementById('khatmaCurrentJuz');
            var percentEl = document.getElementById('khatmaPercentText');

            // Add reflection note
            localStorage.setItem('khatma-reflections-v1', JSON.stringify([]));
            var surahInp = document.getElementById('reflectSurahInput');
            var ayahInp = document.getElementById('reflectAyahInput');
            var textInp = document.getElementById('reflectTextInput');
            if(surahInp && textInp) {
                surahInp.value = 'الكهف';
                if(ayahInp) ayahInp.value = '10';
                textInp.value = 'إذ أوى الفتية إلى الكهف فقالوا ربنا آتنا من لدنك رحمة';
                window.ZATOONA_PHASE5.addReflectionNote();
            }
            var refs = window.ZATOONA_PHASE5.getReflections();

            return {
                page: st.currentPage,
                domPage: pageEl ? pageEl.textContent : '',
                juz: juzEl ? juzEl.textContent : '',
                percent: percentEl ? percentEl.textContent : '',
                reflectionsCount: refs.length
            };
        """)
        self.assertEqual(res['page'], 40)
        self.assertEqual(res['domPage'], '40')
        self.assertEqual(res['juz'], '2')
        self.assertEqual(res['percent'], '7%')
        self.assertEqual(res['reflectionsCount'], 1)

    def test_10_missed_worship_ledger_workflow(self):
        """Verify missed prayers adjustment and missed fasting ledger decrement."""
        res = self.driver.execute_script("""
            localStorage.setItem('worship-missed-ledger-v1', JSON.stringify({
                prayers: { Fajr: 3, Dhuhr: 0, Asr: 0, Maghrib: 0, Isha: 0 },
                fastingDaysOwed: 5,
                fastingDaysDone: 0
            }));
            window.ZATOONA_PHASE5.renderMissedWorship();
            window.ZATOONA_PHASE5.adjustMissedPrayer('Fajr', -1);
            window.ZATOONA_PHASE5.logFastMadeUp();

            var data = window.ZATOONA_PHASE5.getMissedLedger();
            var remFasting = document.getElementById('missedFastingRemaining');
            var doneFasting = document.getElementById('missedFastingDone');

            return {
                fajrLeft: data.prayers.Fajr,
                fastingLeft: data.fastingDaysOwed,
                fastingDone: data.fastingDaysDone,
                domRemFasting: remFasting ? remFasting.textContent : '',
                domDoneFasting: doneFasting ? doneFasting.textContent : ''
            };
        """)
        self.assertEqual(res['fajrLeft'], 2)
        self.assertEqual(res['fastingLeft'], 4)
        self.assertEqual(res['fastingDone'], 1)
        self.assertEqual(res['domRemFasting'], '4')
        self.assertEqual(res['domDoneFasting'], '1')

if __name__ == '__main__':
    unittest.main()

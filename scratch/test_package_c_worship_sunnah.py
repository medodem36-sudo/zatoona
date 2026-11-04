import sys, os, time, unittest, hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

INDEX_PATH = os.path.abspath('index.html')
ZATOONA_PATH = os.path.abspath('zatoona.html')
ASSETS_PATH = os.path.abspath('android/app/src/main/assets/index.html')

class TestPackageCWorshipSunnah(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        opts = Options()
        opts.add_argument('--headless=new')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--window-size=412,915')
        cls.driver = webdriver.Chrome(options=opts)
        cls.driver.get(f"file:///{INDEX_PATH}")
        time.sleep(1)
        cls.driver.execute_script("window.alert = function(){};")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()

    def setUp(self):
        self.driver.execute_script("window.alert = function(){};")

    def test_01_three_way_parity(self):
        h1 = hashlib.sha256(open(INDEX_PATH, 'rb').read()).hexdigest()
        h2 = hashlib.sha256(open(ZATOONA_PATH, 'rb').read()).hexdigest()
        h3 = hashlib.sha256(open(ASSETS_PATH, 'rb').read()).hexdigest()
        self.assertEqual(h1, h2)
        self.assertEqual(h1, h3)

    def test_02_gradual_fajr_alarm(self):
        driver = self.driver
        res = driver.execute_script("""
            const sched = typeof calculateGradualFajrSchedule === 'function' ? calculateGradualFajrSchedule('05:00') : null;
            if(typeof toggleGradualFajrAlarm === 'function') toggleGradualFajrAlarm(true);
            const activeOn = typeof isGradualFajrAlarmActive === 'function' ? isGradualFajrAlarmActive() : false;
            if(typeof toggleGradualFajrAlarm === 'function') toggleGradualFajrAlarm(false);
            const activeOff = typeof isGradualFajrAlarmActive === 'function' ? isGradualFajrAlarmActive() : true;
            return {
                sched: sched,
                preAlarmTime: sched ? sched.preAlarmTime : null,
                activeOn: activeOn,
                activeOff: activeOff
            };
        """)
        self.assertIsNotNone(res['sched'])
        self.assertEqual(res['preAlarmTime'], '04:45')
        self.assertTrue(res['activeOn'])
        self.assertFalse(res['activeOff'])

    def test_03_friday_special_package(self):
        driver = self.driver
        res = driver.execute_script("""
            const status = typeof getFridayPackageStatus === 'function' ? getFridayPackageStatus() : null;
            if(typeof incrementSalawatCount === 'function') incrementSalawatCount();
            const statusAfter = typeof getFridayPackageStatus === 'function' ? getFridayPackageStatus() : null;
            return {
                hasStatus: status !== null,
                totalSunan: status ? status.totalSunan : 0,
                countBefore: status ? status.salawatCount : 0,
                countAfter: statusAfter ? statusAfter.salawatCount : 0
            };
        """)
        self.assertTrue(res['hasStatus'])
        self.assertGreaterEqual(res['totalSunan'], 4)
        self.assertEqual(res['countAfter'], res['countBefore'] + 1)

    def test_04_adhkar_auto_hide_toggle(self):
        driver = self.driver
        res = driver.execute_script("""
            if(typeof toggleAdhkarAutoHide === 'function') toggleAdhkarAutoHide(true);
            const onVal = typeof isAdhkarAutoHideEnabled === 'function' ? isAdhkarAutoHideEnabled() : false;
            if(typeof toggleAdhkarAutoHide === 'function') toggleAdhkarAutoHide(false);
            const offVal = typeof isAdhkarAutoHideEnabled === 'function' ? isAdhkarAutoHideEnabled() : true;
            return { onVal, offVal };
        """)
        self.assertTrue(res['onVal'])
        self.assertFalse(res['offVal'])

    def test_05_missed_prayer_qada_calculator(self):
        driver = self.driver
        res = driver.execute_script("""
            const sampleCounts = { fajr: 30, dhuhr: 30, asr: 30, maghrib: 30, isha: 30 };
            const plan = typeof calculateQadaPlan === 'function' ? calculateQadaPlan(sampleCounts, 1) : null;
            
            // Log 1 qada prayer
            const logged = typeof logQadaPrayer === 'function' ? logQadaPrayer('fajr') : false;
            
            return {
                plan: plan,
                totalMissed: plan ? plan.totalMissed : 0,
                daysToComplete: plan ? plan.daysToComplete : 0,
                logged: logged
            };
        """)
        self.assertIsNotNone(res['plan'])
        self.assertEqual(res['totalMissed'], 150)
        self.assertEqual(res['daysToComplete'], 30)
        self.assertTrue(res['logged'])

    def test_06_last_third_of_night_astronomical_calc(self):
        driver = self.driver
        res = driver.execute_script("""
            // Maghrib 18:00, Fajr 06:00 -> duration 12h, 1/3 is 4h -> last third starts at 02:00
            const calc = typeof calculateLastThirdOfNight === 'function' ? calculateLastThirdOfNight('18:00', '06:00') : null;
            return calc;
        """)
        self.assertIsNotNone(res)
        self.assertEqual(res['nightDurationHours'], 12)
        self.assertEqual(res['lastThirdStartStr'], '02:00')
        self.assertEqual(res['midnightStr'], '00:00')

    def test_07_sunnah_rawatib_tracker(self):
        driver = self.driver
        res = driver.execute_script("""
            navigateTo('prayer');
            const initial = typeof calculateSunnahRawatibAdherence === 'function' ? calculateSunnahRawatibAdherence() : null;
            if(typeof toggleRawatibItem === 'function') toggleRawatibItem('fajr');
            const afterToggle = typeof calculateSunnahRawatibAdherence === 'function' ? calculateSunnahRawatibAdherence() : null;
            return {
                hasInitial: initial !== null,
                totalRakaat: initial ? initial.totalRakaat : 0,
                doneAfter: afterToggle ? afterToggle.completedRakaat : 0
            };
        """)
        self.assertTrue(res['hasInitial'])
        self.assertEqual(res['totalRakaat'], 12)
        self.assertGreaterEqual(res['doneAfter'], 2)

    def test_08_silent_istighfar_and_suhoor_alert(self):
        driver = self.driver
        res = driver.execute_script("""
            // Silent istighfar toggle
            if(typeof toggleSilentIstighfarNudge === 'function') toggleSilentIstighfarNudge(true);
            const istighfarActive = typeof isSilentIstighfarActive === 'function' ? isSilentIstighfarActive() : false;
            
            // Fasting recommendation on Sunday -> Monday
            const sundayDate = new Date(2026, 10, 8); // Sunday
            const rec = typeof checkTomorrowFastingRecommendation === 'function' ? checkTomorrowFastingRecommendation(sundayDate) : null;
            
            return {
                istighfarActive,
                rec
            };
        """)
        self.assertTrue(res['istighfarActive'])
        self.assertIsNotNone(res['rec'])
        self.assertTrue(res['rec']['isFastingRecommended'])
        self.assertEqual(res['rec']['reason'], 'monday')

if __name__ == '__main__':
    unittest.main()

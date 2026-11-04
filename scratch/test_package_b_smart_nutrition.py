import sys, os, time, unittest, hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

INDEX_PATH = os.path.abspath('index.html')
ZATOONA_PATH = os.path.abspath('zatoona.html')
ASSETS_PATH = os.path.abspath('android/app/src/main/assets/index.html')

class TestPackageBSmartNutrition(unittest.TestCase):
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

    def setUp(self):
        self.driver.execute_script("window.alert = function(){};")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()

    def test_01_three_way_parity(self):
        h1 = hashlib.sha256(open(INDEX_PATH, 'rb').read()).hexdigest()
        h2 = hashlib.sha256(open(ZATOONA_PATH, 'rb').read()).hexdigest()
        h3 = hashlib.sha256(open(ASSETS_PATH, 'rb').read()).hexdigest()
        self.assertEqual(h1, h2)
        self.assertEqual(h1, h3)

    def test_02_cheat_day_recovery_calculation_and_storage(self):
        driver = self.driver
        res = driver.execute_script("""
            // 1. Pure calculation
            const calc = typeof calculateCheatRecovery === 'function' ? calculateCheatRecovery(900, 3) : null;
            
            // 2. Storage
            if(typeof saveCheatRecovery === 'function') saveCheatRecovery(900, 3);
            const offset = typeof getCheatRecoveryOffset === 'function' ? getCheatRecoveryOffset() : 0;
            
            // 3. Clear
            if(typeof clearCheatRecovery === 'function') clearCheatRecovery();
            const clearedOffset = typeof getCheatRecoveryOffset === 'function' ? getCheatRecoveryOffset() : -1;
            
            return {
                hasCalc: calc !== null,
                dailyReduction: calc ? calc.dailyReduction : 0,
                isSafe: calc ? calc.isSafe : false,
                offset: offset,
                clearedOffset: clearedOffset
            };
        """)
        self.assertTrue(res['hasCalc'])
        self.assertEqual(res['dailyReduction'], 300)
        self.assertTrue(res['isSafe'])
        self.assertEqual(res['offset'], 300)
        self.assertEqual(res['clearedOffset'], 0)

    def test_03_protein_completeness_calculation(self):
        driver = self.driver
        res = driver.execute_script("""
            navigateTo('meal');
            const sampleMeals = [
                { name: 'صدور دجاج مشوية', kcal: 330, protein: 50, carb: 0, fat: 3 }, // complete
                { name: 'طبق عدس وشوفان', kcal: 250, protein: 20, carb: 40, fat: 2 }   // incomplete
            ];
            const comp = typeof calculateProteinCompleteness === 'function' ? calculateProteinCompleteness(null, sampleMeals) : null;
            return comp;
        """)
        self.assertIsNotNone(res)
        self.assertIn('completeGrams', res)
        self.assertIn('incompleteGrams', res)
        self.assertIn('completePct', res)
        self.assertIn('incompletePct', res)
        self.assertEqual(res['completeGrams'], 50)
        self.assertEqual(res['incompleteGrams'], 20)
        self.assertEqual(res['completePct'] + res['incompletePct'], 100)

    def test_04_egyptian_popular_food_catalog_and_quick_log(self):
        driver = self.driver
        res = driver.execute_script("""
            const catalog = typeof getEgyptianFoodCatalog === 'function' ? getEgyptianFoodCatalog('all') : [];
            const hasKoshari = catalog.some(f => f.id === 'koshari_med' || f.name.includes('كشري'));
            const hasTa3meya = catalog.some(f => f.id === 'ta3meya_airfryer' || f.name.includes('طعمية'));
            
            // Quick log 2 ta3meya
            const logged = typeof quickLogEgyptianFood === 'function' ? quickLogEgyptianFood('ta3meya_airfryer', 2) : false;
            
            return {
                catalogLength: catalog.length,
                hasKoshari: hasKoshari,
                hasTa3meya: hasTa3meya,
                logged: logged
            };
        """)
        self.assertGreaterEqual(res['catalogLength'], 10)
        self.assertTrue(res['hasKoshari'])
        self.assertTrue(res['hasTa3meya'])
        self.assertTrue(res['logged'])

    def test_05_package_b_ui_cards_and_modals_presence(self):
        driver = self.driver
        res = driver.execute_script("""
            navigateTo('meal');
            return {
                hasCheatCard: !!document.getElementById('cheatRecoveryCard'),
                hasProteinCompCard: !!document.getElementById('proteinCompletenessCard'),
                hasCheatModal: !!document.getElementById('modalCheatRecovery'),
                hasEgyptianModal: !!document.getElementById('modalEgyptianFoodGuide')
            };
        """)
        self.assertTrue(res['hasCheatCard'])
        self.assertTrue(res['hasProteinCompCard'])
        self.assertTrue(res['hasCheatModal'])
        self.assertTrue(res['hasEgyptianModal'])

if __name__ == '__main__':
    unittest.main()

import sys, os, time, unittest, hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

INDEX_PATH = os.path.abspath('index.html')
ZATOONA_PATH = os.path.abspath('zatoona.html')
ASSETS_PATH = os.path.abspath('android/app/src/main/assets/index.html')

class TestPackageAGymIntelligence(unittest.TestCase):
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

    def test_02_plateau_detector_logic_and_modal(self):
        driver = self.driver
        # Seed 3 past workouts with same weight (e.g. 50kg) for bench_press
        res = driver.execute_script("""
            localStorage.setItem('meal-gym-tracker:ex:2026-10-10', JSON.stringify({
                squat: { sets: [true, true, true], weight: '50', reps: '8' }
            }));
            localStorage.setItem('meal-gym-tracker:ex:2026-10-17', JSON.stringify({
                squat: { sets: [true, true, true], weight: '50', reps: '8' }
            }));
            localStorage.setItem('meal-gym-tracker:ex:2026-10-24', JSON.stringify({
                squat: { sets: [true, true, true], weight: '50', reps: '8' }
            }));
            
            const plat = typeof detectExercisePlateau === 'function' ? detectExercisePlateau('squat') : null;
            return {
                detected: plat !== null,
                weight: plat ? plat.weight : 0,
                hasAdvice: plat && !!plat.advice
            };
        """)
        self.assertTrue(res['detected'], "Plateau should be detected for 3 sessions at 50kg")
        self.assertEqual(res['weight'], 50)
        self.assertTrue(res['hasAdvice'])

    def test_03_ppl_balance_computation(self):
        driver = self.driver
        res = driver.execute_script("""
            const bal = typeof computeWeeklyPPLBalance === 'function' ? computeWeeklyPPLBalance() : null;
            return bal;
        """)
        self.assertIsNotNone(res)
        self.assertIn('pushPct', res)
        self.assertIn('pullPct', res)
        self.assertIn('legsPct', res)
        self.assertGreater(res['pushPct'] + res['pullPct'] + res['legsPct'], 95)

    def test_04_copy_last_workout_weights(self):
        driver = self.driver
        # Seed a previous workout for squat
        res = driver.execute_script("""
            navigateTo('gym');
            for(let i=0; i<weekDates.length; i++){
                const eff = getEffectiveGymDay(toISO(weekDates[i]), i);
                if(!eff.isRest && eff.gymType !== 'rest' && eff.gym){
                    selectedIdx = i;
                    break;
                }
            }
            renderExercises();

            // Set last session weight
            localStorage.setItem('meal-gym-tracker:ex:2026-10-25', JSON.stringify({
                squat: { sets: [true, true, true], weight: '65.5', reps: '10' }
            }));

            // Call copy
            const copied = typeof copyLastWorkoutWeights === 'function' ? copyLastWorkoutWeights() : false;
            const inputVal = document.querySelector('#w_squat') ? document.querySelector('#w_squat').value : '';
            return { copied, inputVal };
        """)
        self.assertTrue(res['copied'])
        self.assertEqual(res['inputVal'], '65.5')

    def test_05_home_workout_converter_toggle(self):
        driver = self.driver
        res = driver.execute_script("""
            navigateTo('gym');
            for(let i=0; i<weekDates.length; i++){
                const eff = getEffectiveGymDay(toISO(weekDates[i]), i);
                if(!eff.isRest && eff.gymType !== 'rest' && eff.gym){
                    selectedIdx = i;
                    break;
                }
            }
            renderExercises();

            // Toggle Home Mode ON
            toggleHomeWorkoutMode(true);
            const isHomeOn = isHomeWorkoutModeActive();
            const banner = document.getElementById('gymHomeWorkoutBanner');
            const isBannerVisible = banner && !banner.classList.contains('hidden');

            // Toggle Home Mode OFF
            toggleHomeWorkoutMode(false);
            const isHomeOff = !isHomeWorkoutModeActive();

            return { isHomeOn, isBannerVisible, isHomeOff };
        """)
        self.assertTrue(res['isHomeOn'])
        self.assertTrue(res['isBannerVisible'])
        self.assertTrue(res['isHomeOff'])

if __name__ == '__main__':
    unittest.main()

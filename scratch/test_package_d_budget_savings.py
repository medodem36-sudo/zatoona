import sys, os, time, unittest, hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

INDEX_PATH = os.path.abspath('index.html')
ZATOONA_PATH = os.path.abspath('zatoona.html')
ASSETS_PATH = os.path.abspath('android/app/src/main/assets/index.html')

class TestPackageDBudgetSavings(unittest.TestCase):
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

    def test_02_daily_allowance_calculation(self):
        driver = self.driver
        res = driver.execute_script("""
            const testDate = new Date(2026, 10, 10); // Nov 10 (30 days total in Nov -> 21 remaining days)
            const calc = typeof calculateBudgetDailyAllowance === 'function' ? calculateBudgetDailyAllowance(testDate, 6000, 1800) : null;
            return calc;
        """)
        self.assertIsNotNone(calc := res)
        self.assertIn('dailyAllowance', calc)
        self.assertIn('remainingBudget', calc)
        self.assertEqual(calc['remainingBudget'], 4200) # 6000 - 1800
        self.assertEqual(calc['remainingDays'], 21)     # 30 - 10 + 1
        self.assertEqual(calc['dailyAllowance'], 200)   # 4200 / 21

    def test_03_recurring_subscriptions_detector(self):
        driver = self.driver
        res = driver.execute_script("""
            const subs = typeof getUpcomingSubscriptions === 'function' ? getUpcomingSubscriptions() : [];
            const hasNet = subs.some(s => s.id === 'sub_net' || s.title.includes('الإنترنت'));
            const hasGym = subs.some(s => s.id === 'sub_gym' || s.title.includes('الجيم'));
            return {
                length: subs.length,
                hasNet,
                hasGym
            };
        """)
        self.assertGreaterEqual(res['length'], 2)
        self.assertTrue(res['hasNet'])
        self.assertTrue(res['hasGym'])

    def test_04_virtual_savings_goals(self):
        driver = self.driver
        res = driver.execute_script("""
            const goals = typeof getSavingsGoals === 'function' ? getSavingsGoals() : [];
            const firstGoal = goals[0];
            const initAmt = firstGoal ? firstGoal.currentAmount : 0;
            
            // Deposit 300
            if(firstGoal && typeof depositToSavingsGoal === 'function'){
                depositToSavingsGoal(firstGoal.id, 300);
            }
            const afterDeposit = (typeof getSavingsGoals === 'function' ? getSavingsGoals() : [])[0].currentAmount;
            
            // Withdraw 100
            if(firstGoal && typeof withdrawFromSavingsGoal === 'function'){
                withdrawFromSavingsGoal(firstGoal.id, 100);
            }
            const afterWithdraw = (typeof getSavingsGoals === 'function' ? getSavingsGoals() : [])[0].currentAmount;
            
            return {
                initAmt,
                afterDeposit,
                afterWithdraw
            };
        """)
        self.assertEqual(res['afterDeposit'], res['initAmt'] + 300)
        self.assertEqual(res['afterWithdraw'], res['initAmt'] + 200)

    def test_05_package_d_ui_cards_rendered(self):
        driver = self.driver
        res = driver.execute_script("""
            navigateTo('budget');
            return {
                hasAllowanceCard: !!document.getElementById('dailyAllowanceCard'),
                hasSubsCard: !!document.getElementById('upcomingSubscriptionsCard'),
                hasSavingsCard: !!document.getElementById('savingsGoalsCard')
            };
        """)
        self.assertTrue(res['hasAllowanceCard'])
        self.assertTrue(res['hasSubsCard'])
        self.assertTrue(res['hasSavingsCard'])

if __name__ == '__main__':
    unittest.main()

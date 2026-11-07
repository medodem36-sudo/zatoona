import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=375,812')
opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=opts)
driver.get('file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')
driver.execute_script("window.alert = function(){};")

modes = ['home','meal','gym','sleep','prayer','schedule','recovery','overview','search','budget','notes','stretches','study','hair','settings']

for m in modes:
    try:
        driver.execute_script(f"navigateTo('{m}'); navigateTo('{m}');")
        print(f"Success rapid navigateTo for '{m}'")
    except Exception as e:
        print(f"ERROR rapid navigateTo for '{m}': {e}")

logs = driver.get_log('browser')
print(f'\nTotal browser errors: {len(logs)}')
for l in logs:
    if l['level'] in ['SEVERE', 'WARNING']:
        print(f"[{l['level']}] {l['message']}")

driver.quit()

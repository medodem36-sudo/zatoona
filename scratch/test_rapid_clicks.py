import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=375,812')
# Enable logging
opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=opts)
print('Loading index.html...')
t0 = time.time()
driver.get('file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')
time.sleep(2)
print(f'Page loaded in {time.time()-t0:.2f}s')

# Check console logs
logs = driver.get_log('browser')
print(f'Total console logs on startup: {len(logs)}')
for l in logs:
    if l['level'] in ['SEVERE', 'WARNING']:
        print(f"[{l['level']}] {l['message']}")

# Test rapid double-tap on bottom nav buttons
print('\nTesting rapid clicks on bottom nav...')
for bnb_id in ['bottomNav-prayer', 'bottomNav-gym', 'bottomNav-meal', 'bottomNav-schedule', 'bottomNav-home']:
    btn = driver.find_element(By.ID, bnb_id)
    t1 = time.time()
    # click twice rapidly
    driver.execute_script("arguments[0].click(); arguments[0].click();", btn)
    dur = time.time() - t1
    print(f'Double click {bnb_id} took {dur*1000:.1f}ms')

# Check console logs after rapid clicks
logs2 = driver.get_log('browser')
print(f'Console logs after clicks: {len(logs2)}')
for l in logs2:
    if l['level'] in ['SEVERE', 'WARNING']:
        print(f"[{l['level']}] {l['message']}")

driver.quit()

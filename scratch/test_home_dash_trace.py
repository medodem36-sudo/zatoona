from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=opts)

p = os.path.abspath('index.html')
driver.get(f"file:///{p}")

try:
    driver.execute_script("renderHomeDashboard();")
    print("SUCCESS renderHomeDashboard()")
except Exception as e:
    print("EXCEPTION in renderHomeDashboard():", e)

logs = driver.get_log('browser')
print("Browser logs:")
for l in logs:
    if l['level'] == 'SEVERE':
        print("  ", l)

driver.quit()

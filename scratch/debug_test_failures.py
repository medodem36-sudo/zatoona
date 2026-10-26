import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.get("file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html")

# 1. Print STORAGE_PREFIX
prefix = driver.execute_script("return typeof STORAGE_PREFIX !== 'undefined' ? STORAGE_PREFIX : 'UNDEFINED';")
print("STORAGE_PREFIX:", prefix)

# 2. Print all localStorage keys
keys = driver.execute_script("return Object.keys(localStorage);")
print("All localStorage keys:", keys)

# 3. Print browser logs
logs = driver.get_log("browser")
print("\nBrowser console logs:")
for l in logs:
    print(f"[{l['level']}] {l['message']}")

driver.quit()

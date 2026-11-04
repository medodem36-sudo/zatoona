import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=375,812')

driver = webdriver.Chrome(options=options)
try:
    abs_path = os.path.abspath('index.html')
    driver.get(f'file:///{abs_path}')
    res = driver.execute_script("""
        return {
            bodyScrollWidth: document.body.scrollWidth,
            bodyClientWidth: document.body.clientWidth,
            hasOverflow: document.body.scrollWidth > document.body.clientWidth + 1
        };
    """)
    print("375px screen test:", res)
finally:
    driver.quit()

import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1200,800')

driver = webdriver.Chrome(options=options)
try:
    is_wd = driver.execute_script("return !!navigator.webdriver;")
    print("navigator.webdriver in Selenium:", is_wd)
finally:
    driver.quit()

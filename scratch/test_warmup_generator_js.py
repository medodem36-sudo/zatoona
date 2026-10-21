import json, re, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding="utf-8")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

try:
    import os
    index_url = "file:///" + os.path.abspath("index.html").replace("\\", "/")
    driver.get(index_url)
    
    # Check that stretch catalog is loaded
    cat_len = driver.execute_script("return (window.ZATOONA_STRETCH_CATALOG || []).length;")
    print("Catalog loaded in runtime:", cat_len)
    
    # Check EX_A and EX_B
    ex_a_len = driver.execute_script("return (window.EX_A || []).length;")
    print("EX_A length:", ex_a_len)

    # Check template registry
    reg_keys = driver.execute_script("return Object.keys(window.GYM_PLAN_TEMPLATE_REGISTRY || {});")
    print("Template registry keys:", reg_keys)
finally:
    driver.quit()

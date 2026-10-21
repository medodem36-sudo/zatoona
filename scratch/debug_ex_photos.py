# -*- coding: utf-8 -*-
import sys, os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=1200,1000')
driver = webdriver.Chrome(options=opts)

try:
    index_url = "file:///" + os.path.join(repo, "index.html").replace("\\", "/")
    driver.get(index_url)
    driver.execute_script("""
        localStorage.setItem('meal-gym-tracker:gym-enabled', 'true');
        localStorage.setItem('meal-gym-tracker:gymPauseDate', '');
        if(typeof navigateTo === 'function') navigateTo('gym');
    """)
    driver.get(index_url)
    driver.execute_script("""
        if(typeof navigateTo === 'function') navigateTo('gym');
    """)
    time.sleep(1)
    
    imgs = driver.find_elements("css selector", ".ex-photo img")
    print(f"Found {len(imgs)} imgs in .ex-photo:")
    for idx, img in enumerate(imgs):
        driver.execute_script("arguments[0].scrollIntoView(); arguments[0].loading = 'eager';", img)
    time.sleep(1)
    for idx, img in enumerate(imgs):
        src = img.get_attribute("src")
        complete = driver.execute_script("return arguments[0].complete;", img)
        nw = driver.execute_script("return arguments[0].naturalWidth;", img)
        print(f"  {idx}: nw={nw} | complete={complete} | src={src}")
finally:
    driver.quit()

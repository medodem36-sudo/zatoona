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
    driver.execute_script("if(typeof navigateTo === 'function') navigateTo('gym');")
    time.sleep(1)

    # Set custom image for squat
    driver.execute_script("""
        const customUrl = 'data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\"><rect fill=\"purple\"/></svg>';
        const map = {
            'squat': { type: 'url', url: customUrl, updatedAt: Date.now() }
        };
        localStorage.setItem('meal-gym-tracker:exercise-image-map-v1', JSON.stringify(map));
        if(typeof renderExercises === 'function') renderExercises();
    """)
    time.sleep(0.5)

    squat_src = driver.execute_script("""
        const el = document.querySelector('[data-ex-key=\"squat\"] img');
        return el ? el.src : '';
    """)
    print("Squat custom src:", squat_src)
    assert 'data:image/svg+xml' in squat_src, "Custom image did not take priority!"

    # Remove custom image
    driver.execute_script("""
        localStorage.removeItem('meal-gym-tracker:exercise-image-map-v1');
        if(typeof renderExercises === 'function') renderExercises();
    """)
    time.sleep(0.5)

    squat_restored = driver.execute_script("""
        const el = document.querySelector('[data-ex-key=\"squat\"] img');
        return el ? el.src : '';
    """)
    print("Squat restored src:", squat_restored)
    assert 'ex-a01-goblet-squat.svg' in squat_restored, "Default SVG not restored!"
    print("CUSTOM IMAGE PRIORITY TEST PASSED!")
finally:
    driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=375,812")
driver = webdriver.Chrome(options=chrome_options)
driver.get("file:///" + os.path.abspath("index.html"))
time.sleep(1)

driver.execute_script("""
    localStorage.setItem('meal-gym-tracker:gym-enabled', 'true');
    localStorage.setItem('meal-gym-tracker:gymPauseDate', '');
    if(typeof selectDay === 'function') selectDay(0);
    if(typeof navigateTo === 'function') navigateTo('gym');
""")
time.sleep(1)

# Try sticky
driver.execute_script("""
const bnav = document.getElementById('bottomNav');
if(bnav){
  bnav.style.position = 'sticky';
  bnav.style.bottom = '0';
}
""")
time.sleep(0.3)

first_toggle = driver.find_element(By.CSS_SELECTOR, ".gw-drill-item .gw-toggle-btn")
print("Before click:", first_toggle.location, first_toggle.size)
try:
    first_toggle.click()
    print("Click succeeded with position: sticky!")
except Exception as e:
    print("Click failed with sticky:", type(e), e)

driver.quit()

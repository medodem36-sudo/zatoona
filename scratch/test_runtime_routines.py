from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os, sys

sys.stdout.reconfigure(encoding="utf-8")

chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)
driver.get('file:///' + os.path.abspath('index.html').replace('\\', '/'))

print('getRoutineExercises(A):', driver.execute_script("return getRoutineExercises('A').length;"))
print('getRoutineExercises(B):', driver.execute_script("return getRoutineExercises('B').length;"))
print('getRoutineExercises(fb_a):', driver.execute_script("return getRoutineExercises('fb_a').length;"))
print('getRoutineExercises(ppl_push):', driver.execute_script("return getRoutineExercises('ppl_push').length;"))
print('getRoutineExercises(ul_upper):', driver.execute_script("return getRoutineExercises('ul_upper').length;"))
print('getRoutineExercises(bro_chest):', driver.execute_script("return getRoutineExercises('bro_chest').length;"))

driver.quit()

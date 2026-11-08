import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--allow-file-access-from-files')
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=chrome_options)
driver.get('file:///' + os.path.abspath('index.html').replace('\\', '/'))

print('Page loaded title:', driver.title)

logs = driver.get_log('browser')
print(f'Browser logs count: {len(logs)}')
for l in logs:
    if l['level'] in ['SEVERE', 'WARNING']:
        print(f"[{l['level']}] {l['message']}")

try:
    res = driver.execute_script('''
        openAiVoiceSettingsModal();
        var m = document.getElementById("aiVoiceSettingsModal");
        return m ? m.style.display : "not found";
    ''')
    print('openAiVoiceSettingsModal executed, display is:', res)
except Exception as e:
    print('Error executing openAiVoiceSettingsModal:', e)

driver.quit()

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
        const neg = [];
        document.querySelectorAll('*').forEach(el => {
            const rect = el.getBoundingClientRect();
            if(rect.left < -5){
                neg.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    left: rect.left,
                    right: rect.right,
                    width: rect.width
                });
            }
        });
        return neg;
    """)
    print("Negative left elements:")
    for n in res:
        print(n)
finally:
    driver.quit()

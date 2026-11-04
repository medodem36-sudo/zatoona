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
        const list = Array.from(document.body.childNodes);
        for(let i = list.length - 1; i >= 0; i--){
            const node = list[i];
            const name = node.nodeType === 1 ? (node.tagName + '#' + node.id + '.' + node.className) : ('NODE_' + node.nodeType);
            node.remove();
            if(document.body.scrollWidth < 600){
                return { culprit: name, remaining: document.body.scrollWidth };
            }
        }
        return { notFound: true, current: document.body.scrollWidth };
    """)
    print("Result:", res)
finally:
    driver.quit()

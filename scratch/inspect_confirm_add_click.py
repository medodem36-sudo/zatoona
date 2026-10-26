import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const confirmAddBtn = document\.getElementById\(\'encConfirmAddBtn\'\);[\s\S]*?\}\);', text)
if not m:
    m = re.search(r'encConfirmAddBtn[\s\S]{0,1000}', text)
if m:
    print(m.group(0)[:1500])

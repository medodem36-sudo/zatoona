import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'document\.getElementById\(\'encConfirmAddBtn\'\)[\s\S]*?\}\);', text)
if m:
    print('=== encConfirmAddBtn handler ===')
    print(m.group(0)[:1500])

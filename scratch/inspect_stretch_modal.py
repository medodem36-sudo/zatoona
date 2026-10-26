import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function openStretchModal\s*\([\s\S]*?\nfunction\s+', text)
if m:
    print(m.group(0)[:1500])

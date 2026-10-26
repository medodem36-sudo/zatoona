import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'VERSION|v23|v24|cacheName|CACHE_NAME', text, re.IGNORECASE):
    p = m.start()
    print(text[max(0, p-40):min(len(text), p+60)].replace('\n', ' '))
    print('---')

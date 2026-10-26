import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'ZATOONA_STRETCH_CATALOG', text)]
print(f'Found {len(matches)} occurrences of ZATOONA_STRETCH_CATALOG in index.html')
for p in matches[:3]:
    print(text[max(0, p-50):min(len(text), p+300)])
    print('---')

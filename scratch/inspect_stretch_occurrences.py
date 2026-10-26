import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'assets/images/stretches', text)]
print(f'Found {len(matches)} occurrences of assets/images/stretches in index.html')
for p in matches[:3]:
    print(text[max(0, p-100):min(len(text), p+200)])
    print('---')

# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for renderSleep calls and day selection
print("=== renderSleep calls ===")
for m in re.finditer(r'renderSleep\(\)', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 100)
    print(text[start:end].replace('\n', ' '))
    print('---')

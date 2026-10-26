# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function computeDotClassSleep[\s\S]*?(?=\nfunction [a-zA-Z0-9_]+\s*\()', text)
if m:
    print(m.group(0))

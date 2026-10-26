# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'sw.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const\s+CACHE_VERSION\s*=\s*[\'"][^\'"]+[\'"];', text)
if m:
    print(m.group(0))

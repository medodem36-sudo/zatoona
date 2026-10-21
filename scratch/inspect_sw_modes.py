# -*- coding: utf-8 -*-
import sys, re, os

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
with open(os.path.join(repo, "sw.js"), "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'whitelist|VALID_MODES|ALLOWED_MODES|modes', text, re.IGNORECASE)
lines = text.split('\n')
for i, l in enumerate(lines):
    if 'whitelist' in l.lower() or 'nav_mode' in l.lower() or 'notes' in l.lower() or 'mode' in l.lower():
        if 'notification' in l.lower() or 'valid' in l.lower() or 'const' in l.lower() or 'let' in l.lower():
            print(f"Line {i+1}: {l.strip()[:100]}")

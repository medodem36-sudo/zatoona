# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function checkAndDispatchDueReminders[\s\S]*?(?=\nfunction [a-zA-Z0-9_]+\s*\()', text)
if m:
    lines = m.group(0).split('\n')
    for i in range(50, min(130, len(lines))):
        print(f"{i+1:3d}: {lines[i]}")

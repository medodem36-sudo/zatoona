# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m_import = re.search(r'function importAllData[\s\S]*?(?=\nfunction [a-zA-Z0-9_]+\s*\()', text)
if m_import:
    lines = m_import.group(0).split('\n')
    for line in lines[40:100]:
        print(line)

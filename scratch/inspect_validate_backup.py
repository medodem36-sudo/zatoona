# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m_val = re.search(r'function validateBackupData[\s\S]*?(?=\nfunction [a-zA-Z0-9_]+\s*\()', text)
if m_val:
    print("=== VALIDATE BACKUP DATA ===")
    print(m_val.group(0)[:1500])

# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m_export = re.search(r'function exportAllData[\s\S]*?(?=\nfunction [a-zA-Z0-9_]+\s*\()', text)
if m_export:
    print("=== EXPORT ALL DATA ===")
    print(m_export.group(0)[:2500])

m_import = re.search(r'function importAllData[\s\S]*?(?=\nfunction [a-zA-Z0-9_]+\s*\()', text)
if m_import:
    print("\n=== IMPORT ALL DATA ===")
    print(m_import.group(0)[:2500])

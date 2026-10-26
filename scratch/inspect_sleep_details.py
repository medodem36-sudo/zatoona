# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Search for backup / export / import
print("=== BACKUP / EXPORT / IMPORT SEARCH ===")
for m in re.finditer(r'(function\s+(?:export|import|backup|restore)[a-zA-Z0-9_]*\s*\([^\)]*\))', text, re.IGNORECASE):
    print(m.group(0))

# Also search for 'export' or 'backup' in UI buttons
for m in re.finditer(r'id="[^"]*(?:export|backup|restore|import)[^"]*"', text, re.IGNORECASE):
    print("Element:", m.group(0))

# 2. Notification scheduler functions
print("\n=== NOTIFICATION SCHEDULER SEARCH ===")
for m in re.finditer(r'function\s+([a-zA-Z0-9_]*(?:Notification|Reminder|Alarm)[a-zA-Z0-9_]*)\s*\(', text):
    print("Func:", m.group(1))

# 3. Schedule settings defaults and sleep fields
print("\n=== SCHED_DEFAULTS & SLEEP ===")
m_defaults = re.search(r'const\s+SCHED_DEFAULTS\s*=\s*\{([\s\S]*?)\};', text)
if m_defaults:
    print(m_defaults.group(0))

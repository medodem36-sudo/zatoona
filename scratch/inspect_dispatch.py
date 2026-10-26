# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m_dispatch = re.search(r'function checkAndDispatchDueReminders[\s\S]*?(?=\nfunction initNotificationScheduler|\n/\* ================= )', text)
if m_dispatch:
    print("=== DISPATCH DUE REMINDERS ===")
    print(m_dispatch.group(0)[:2500])

# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m_notifs = re.search(r'function loadReminders[\s\S]*?(?=\nfunction renderNotificationSettingsUI|\n/\* ================= )', text)
if m_notifs:
    print("=== NOTIFICATION & REMINDER SYSTEM ===")
    print(m_notifs.group(0)[:3000])

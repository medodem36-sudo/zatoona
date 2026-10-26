# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Recovery view
m_rec = re.search(r'<div id="recoveryView"[\s\S]*?(?=<div id="[a-zA-Z0-9_-]+View"|<div id="scheduleView")', text)
if m_rec:
    print("=== RECOVERY VIEW ===")
    print(m_rec.group(0)[:1500])

# 2. Schedule settings modal / view
m_sched = re.search(r'id="scheduleSettingsModal"[\s\S]*?(?=</div>\s*</div>\s*</div>)', text)
if m_sched:
    print("\n=== SCHEDULE SETTINGS MODAL ===")
    print(m_sched.group(0)[:1500])

# 3. Notification scheduler
m_notif = re.search(r'function (?:scheduleReminders|initNotifications|scheduleDailyReminders)[\s\S]*?(?=\nfunction |\n/\*)', text)
if m_notif:
    print("\n=== NOTIFICATION SCHEDULER ===")
    print(m_notif.group(0)[:1500])

# 4. Backup & Export
m_backup = re.search(r'function exportData[\s\S]*?(?=\nfunction |\n/\*)', text)
if m_backup:
    print("\n=== EXPORT DATA ===")
    print(m_backup.group(0)[:1000])

m_import = re.search(r'function importData[\s\S]*?(?=\nfunction |\n/\*)', text)
if m_import:
    print("\n=== IMPORT DATA ===")
    print(m_import.group(0)[:1000])

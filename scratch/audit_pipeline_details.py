# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'manifest.json', 'r', encoding='utf-8') as f:
    print("=== MANIFEST.JSON ===")
    print(f.read())

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Notification scheduler interval
m_sched = re.search(r'function initNotificationScheduler[\s\S]*?(?=\nfunction renderNotificationSettingsUI)', text)
if m_sched:
    print("\n=== initNotificationScheduler ===")
    print(m_sched.group(0))

# dispatchNotification
m_disp = re.search(r'function dispatchNotification[\s\S]*?(?=\nfunction checkAndDispatchDueReminders)', text)
if m_disp:
    print("\n=== dispatchNotification & tryDispatchWindowNotification ===")
    print(m_disp.group(0))

# sw.js notificationclick
with open(r'sw.js', 'r', encoding='utf-8') as f:
    sw_text = f.read()

m_sw_notif = re.search(r'self\.addEventListener\([\'"]notificationclick[\'"][\s\S]*?(?=\n\/\*|\nself\.addEventListener|\Z)', sw_text)
if m_sw_notif:
    print("\n=== sw.js notificationclick ===")
    print(m_sw_notif.group(0))

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('function checkAndDispatchDueReminders')
if idx1 != -1:
    print('=== checkAndDispatchDueReminders ===')
    print(text[idx1:idx1+2500])

idx2 = text.find('function initNotificationScheduler')
if idx2 != -1:
    print('\n=== initNotificationScheduler ===')
    print(text[idx2:idx2+1500])

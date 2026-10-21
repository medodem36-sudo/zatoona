import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('/* ================= STAGE 6: NOTIFICATIONS & REMINDERS SYSTEM ================= */')
if idx != -1:
    line_no = text[:idx].count('\n') + 1
    print(f'Notifications system @ line {line_no}:')
    print(text[idx:idx+3500])
else:
    print('Notifications system NOT FOUND!')

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function checkAndDispatchDueReminders')
if idx != -1:
    line_no = text[:idx].count('\n') + 1
    print(f'checkAndDispatchDueReminders @ line {line_no}:')
    print(text[idx:idx+3000])
else:
    print('checkAndDispatchDueReminders not found!')

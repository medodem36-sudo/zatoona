import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('function dispatchNotification')
if idx1 != -1:
    print(text[idx1:idx1+2000])

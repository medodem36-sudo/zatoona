import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('function routeNotificationClick')
if idx1 != -1:
    print(text[idx1:idx1+1500])

idx2 = text.find('function switchMode')
if idx2 != -1:
    print(text[idx2:idx2+500])

import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for i in [m.start() for m in re.finditer(r'navigator\.storage\.estimate', text)]:
    line_no = text[:i].count('\n') + 1
    print(f'Line {line_no}:')
    print(text[i-50:i+300])
    print('-'*50)

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

imp_idx = text.find('function importAllData')
print(text[imp_idx+2500:imp_idx+5000])

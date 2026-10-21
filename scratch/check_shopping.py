import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function computeShoppingList')
if idx != -1:
    line_no = text[:idx].count('\n') + 1
    print(f'computeShoppingList @ line {line_no}:')
    print(text[idx:idx+2500])
else:
    print('computeShoppingList not found')

idx2 = text.find('function renderShopping')
if idx2 != -1:
    line_no = text[:idx2].count('\n') + 1
    print(f'\nrenderShopping @ line {line_no}:')
    print(text[idx2:idx2+2500])

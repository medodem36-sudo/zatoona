import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def print_section(title, start_str, length=2000):
    print(f'\n========================================\n{title}\n========================================')
    idx = text.find(start_str)
    if idx != -1:
        line_no = text[:idx].count('\n') + 1
        print(f'Found at line {line_no}:')
        print(text[idx:idx+length])
    else:
        print('NOT FOUND!')

# 1. importAllData rollback logic
print_section('importAllData rollback logic', 'function importAllData', 3000)

# 2. ZatoonaMediaStorage implementation
print_section('ZatoonaMediaStorage', 'const ZatoonaMediaStorage', 2000)

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'function\s+render[a-zA-Z0-9_]*(?:Plan|Custom|Template)[a-zA-Z0-9_]*\s*\(', text)
print('Matching plan render functions:', matches)

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'function\s+([a-zA-Z0-9_]*Custom[a-zA-Z0-9_]*)\s*\(', text)
print('Custom functions:', set(m))

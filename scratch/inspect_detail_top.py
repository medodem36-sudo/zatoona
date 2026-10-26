import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function renderEncyclopediaDetailHtml\s*\([\s\S]*?\nfunction\s+', text)
if m:
    code = m.group(0)
    print('Code length:', len(code))
    # Look at the returned template string
    lines = code.split('\n')
    for i, l in enumerate(lines[:60]):
        print(f'{i:2d}: {l}')

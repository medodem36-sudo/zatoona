import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Search for functions with 'Catalog' in their name
matches = re.findall(r'function\s+([a-zA-Z0-9_]*Catalog[a-zA-Z0-9_]*)\s*\(', html)
print('Catalog functions:', set(matches))

# Let's inspect renderExerciseCatalog or similar
for fn in set(matches):
    m = re.search(r'function\s+' + fn + r'\s*\([\s\S]*?\{[\s\S]*?\n\}', html)
    if m:
        lines = m.group(0).split('\n')
        print(f'\n--- {fn} ({len(lines)} lines) ---')
        print('\n'.join(lines[:25]))

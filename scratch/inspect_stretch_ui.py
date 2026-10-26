import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'function\s+([a-zA-Z0-9_]*Stretch[a-zA-Z0-9_]*)\s*\(', text)
print('Stretch functions:', set(m))

for fn in ['renderStretchDetail', 'renderStretchCatalogModal', 'renderStretchEncyclopedia']:
    m = re.search(r'function\s+' + fn + r'\s*\([\s\S]*?\{([\s\S]*?)\n\}', text)
    if m:
        lines = [l for l in m.group(0).split('\n') if '<img' in l or 'image' in l or 'photo' in l]
        print(f'{fn} images:')
        print('\n'.join(lines[:10]))

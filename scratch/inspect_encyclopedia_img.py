import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for fn in ['renderGymEncyclopedia', 'renderEncyclopediaDetailHtml']:
    m = re.search(r'function\s+' + fn + r'\s*\([\s\S]*?\{([\s\S]*?)\n\}', html)
    if m:
        print(f'=== {fn} ===')
        code = m.group(0)
        # Search for img or image handling inside function
        img_lines = [l for l in code.split('\n') if 'img' in l.lower() or 'image' in l.lower() or 'photo' in l.lower() or 'svg' in l.lower()]
        print('\n'.join(img_lines[:20]))

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const\s+CACHE_NAME\s*=\s*[\'\"]([^\'\"]+)[\'\"];', text)
print('Current CACHE_NAME:', m.group(0) if m else 'NOT FOUND')

m2 = re.search(r'const\s+SHELL_ASSETS\s*=\s*(\[[\s\S]*?\]);', text)
if m2:
    assets = re.findall(r'[\'\"]([^\'\"]+)[\'\"]', m2.group(1))
    print(f'SHELL_ASSETS count: {len(assets)}')
    ex_assets = [a for a in assets if 'exercises' in a]
    print(f'Exercise assets in SHELL_ASSETS ({len(ex_assets)}):')
    for a in ex_assets:
        print('  ', a)

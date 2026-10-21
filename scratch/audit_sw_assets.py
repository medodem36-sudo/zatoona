import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('const SHELL_ASSETS = [')
idx_end = text.find('];', idx)
block = text[idx:idx_end+2]
print('=== SHELL_ASSETS AUDIT ===')
assets = re.findall(r'["\']([^"\']+)["\']', block)
for a in assets:
    if a in ['./', './index.html']:
        exists = os.path.exists('index.html')
    else:
        clean_path = a.lstrip('./').replace('/', os.sep)
        exists = os.path.exists(clean_path)
    print(f'  {a:45} exists: {exists}')

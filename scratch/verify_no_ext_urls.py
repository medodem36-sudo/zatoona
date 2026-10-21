# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Verify WARMUP and COOLDOWN no longer have external URLs
warmup_match = re.search(r'const WARMUP = \[(.*?)\];', text, re.DOTALL)
cooldown_match = re.search(r'const COOLDOWN = \[(.*?)\];', text, re.DOTALL)

for label, m in [('WARMUP', warmup_match), ('COOLDOWN', cooldown_match)]:
    block = m.group(1)
    ext_urls = re.findall(r'https?://\S+', block)
    local_urls = re.findall(r'\./assets/images/\S+', block)
    print(f'{label}:')
    print(f'  External URLs: {len(ext_urls)}')
    for u in ext_urls:
        print(f'    VIOLATION: {u}')
    print(f'  Local SVG paths: {len(local_urls)}')
    for u in local_urls:
        print(f'    OK: {u}')
    print()

# Check for any remaining external Wikimedia image URLs in EX_A_DEFAULTS etc
print('=== Remaining external Wikimedia image URLs in full file ===')
lines = text.split('\n')
count = 0
for i, line in enumerate(lines):
    if 'commons.wikimedia.org/wiki/Special:FilePath/' in line:
        count += 1
        print(f'  Line {i+1}: {line.strip()[:120]}')
print(f'Total remaining Wikimedia image references: {count}')

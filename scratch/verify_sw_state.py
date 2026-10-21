# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('sw.js','r',encoding='utf-8') as f:
    sw = f.read()
m = re.search(r"const CACHE_VERSION\s*=\s*'([^']+)'", sw)
print('CACHE_VERSION:', m.group(1))
sb = re.search(r'const SHELL_ASSETS\s*=\s*\[(.*?)\];', sw, re.DOTALL).group(1)
entries = re.findall(r"'(\./[^']*?)'", sb)
print('SHELL_ASSETS count:', len(entries))
dups = [e for e in entries if entries.count(e) > 1]
print('Duplicates:', set(dups) if dups else 'None')
# Count by category
stretches = [e for e in entries if 'stretches/' in e]
exercises = [e for e in entries if 'exercises/' in e]
warmup = [e for e in entries if 'warmup/' in e]
cooldown = [e for e in entries if 'cooldown/' in e]
print(f'Breakdown: stretches={len(stretches)}, exercises={len(exercises)}, warmup={len(warmup)}, cooldown={len(cooldown)}')

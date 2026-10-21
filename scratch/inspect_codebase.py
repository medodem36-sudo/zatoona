# -*- coding: utf-8 -*-
import re, json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    cat_text = f.read()

m = re.search(r'window\.([a-zA-Z0-9_]+)\s*=', cat_text)
if m:
    print('Exercise catalog global var:', m.group(1))

ids = re.findall(r'id:\s*[\'"]([^\'"]+)[\'"]', cat_text)
print('Catalog exercise IDs count:', len(ids))
print('Sample IDs:', ids[:25])

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check arabic normalizer
norm_matches = re.findall(r'function\s+([a-zA-Z0-9_]*norm[a-zA-Z0-9_]*)\s*\(', html, re.I)
print('Normalizer functions in index.html:', norm_matches)
for nm in norm_matches:
    idx = html.find('function ' + nm)
    print(nm, '-->', html[idx:idx+250])

# Check how modals are opened and styled in index.html
modals = re.findall(r'id=[\'"]([^\'"]*modal[^\'"]*)[\'"]', html, re.I)
print('Sample modals in index.html:', modals[:10])

# Check drawer navigation
m_drawer = re.search(r'id=[\'"]drawerNav[\'"].*?</ul>', html, re.DOTALL)
if m_drawer:
    print('Drawer items:\n', m_drawer.group(0)[:500])

# Check where exercise-catalog.js is imported
cat_tag = re.findall(r'<script\s+src=[\'"][^\'"]*exercise-catalog\.js[\'"].*?</script>', html)
print('exercise-catalog script tag:', cat_tag)

# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for querySelectorAll('.drawer-nav-btn')
matches = [m.start() for m in re.finditer(r'drawer-nav-btn', text)]
for idx in matches:
    snippet = text[max(0, idx-50):min(len(text), idx+200)]
    if 'addEventListener' in snippet or 'forEach' in snippet or 'onclick' in snippet:
        print('Found listener snippet:\n', snippet)

# Search for modeMeal listener
idx_m = text.find("'modeMeal'")
if idx_m != -1:
    print('\nmodeMeal context:\n', text[idx_m-50:idx_m+500])

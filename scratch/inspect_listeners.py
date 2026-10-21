# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("addEventListener('click'")
matches = re.finditer(r"getElementById\('modeNotes'\)\.addEventListener", text)
for m in matches:
    idx2 = m.start()
    print(text[idx2-100:idx2+300])

# Also check for drawer listener
matches_draw = re.finditer(r"drawer-nav-btn", text)
for md in list(matches_draw)[:3]:
    idx_d = md.start()
    print('drawer listener around:', text[idx_d-100:idx_d+200])

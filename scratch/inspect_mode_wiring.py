# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'document\.getElementById\([\'"]mode[A-Z][a-zA-Z0-9_]*[\'"]\)', text)
print('mode button references:', set(m))

idx = text.find("modeNotes")
if idx != -1:
    print('Around modeNotes:\n', text[idx-100:idx+300])

# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_m = text.find('function applyMode(')
if idx_m != -1:
    print('applyMode full:\n', text[idx_m:idx_m+2500])

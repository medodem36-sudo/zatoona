# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_m = text.find('id="modesBar"')
if idx_m != -1:
    print('modesBar:\n', text[idx_m:idx_m+1500])

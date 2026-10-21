# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.mode-btn')
while idx != -1:
    print('mode-btn at', idx, ':\n', text[idx-50:idx+250])
    idx = text.find('.mode-btn', idx+1)

# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function syncNavigation(')
if idx != -1:
    print('syncNavigation:\n', text[idx:idx+800])

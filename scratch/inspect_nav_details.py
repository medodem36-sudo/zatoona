# -*- coding: utf-8 -*-
import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find NAV_MODES
idx = text.find('const NAV_MODES')
if idx != -1:
    print('NAV_MODES section:\n', text[idx:idx+400])

# Find applyMode
idx_m = text.find('function applyMode(')
if idx_m != -1:
    print('\napplyMode section:\n', text[idx_m:idx_m+1200])

# Find switchMode or navigateTo
idx_s = text.find('function switchMode(')
if idx_s != -1:
    print('\nswitchMode section:\n', text[idx_s:idx_s+500])

# Find drawerNav in HTML
idx_d = text.find('id="drawerNav"')
if idx_d != -1:
    print('\ndrawerNav HTML:\n', text[idx_d:idx_d+1500])

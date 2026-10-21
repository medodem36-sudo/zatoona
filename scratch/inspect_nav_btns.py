# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

sidebar_matches = re.findall(r'<button[^>]*sidebar-nav-btn[^>]*>', text)
print('sidebar-nav-btn count:', len(sidebar_matches))
for b in sidebar_matches:
    print(b)

drawer_matches = re.findall(r'<button[^>]*drawer-nav-btn[^>]*>', text)
print('\ndrawer-nav-btn count:', len(drawer_matches))
for b in drawer_matches:
    print(b)

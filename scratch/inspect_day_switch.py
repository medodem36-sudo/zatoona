# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(22640, 22710):
    print(f"{i+1:5d}: {lines[i]}", end='')

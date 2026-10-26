# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'sw.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(0, min(50, len(lines))):
    print(f"{i+1:3d}: {lines[i]}", end='')

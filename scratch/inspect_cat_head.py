# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Total lines in exercise-catalog.js:', len(lines))
for i in range(min(50, len(lines))):
    print(f"{i+1:3d}: {lines[i]}", end='')

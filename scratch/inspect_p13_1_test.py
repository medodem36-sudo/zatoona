# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'scratch/test_phase13_1_checklist_labels.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Checklist test search for sleep:")
for line in text.split('\n'):
    if 'sleep' in line.lower():
        print(line)

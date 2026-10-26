# -*- coding: utf-8 -*-
import sys
import os
import glob
sys.stdout.reconfigure(encoding='utf-8')

for p in glob.glob(r'scratch/test_*.py'):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'sleephabits' in content.lower() or 'sleeptime' in content.lower() or 'sleepview' in content.lower():
        print(f"File {p} references sleep:")
        for line in content.split('\n'):
            if any(k in line.lower() for k in ['sleephabits', 'sleeptime', 'sleepview', '#sleep']):
                print(f"  {line.strip()[:100]}")

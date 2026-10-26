# -*- coding: utf-8 -*-
import sys
import glob
sys.stdout.reconfigure(encoding='utf-8')

for p in glob.glob(r'scratch/test_*.py'):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'cache_version' in content.lower():
        print(f"File {p} checks cache version:")
        for line in content.split('\n'):
            if 'cache_version' in line.lower() or 'v24' in line:
                print(f"  {line.strip()[:100]}")

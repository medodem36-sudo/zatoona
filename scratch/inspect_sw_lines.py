# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find CACHE_VERSION, SHELL_ASSETS, VALID_MODES line numbers
for i, line in enumerate(lines):
    if 'CACHE_VERSION' in line and 'const' in line:
        print(f"Line {i+1}: {line.rstrip()}")
    if 'SHELL_ASSETS' in line and 'const' in line:
        print(f"Line {i+1}: {line.rstrip()}")
    if 'VALID_MODES' in line:
        print(f"Line {i+1}: {line.rstrip()}")

# Find end of SHELL_ASSETS array
in_shell = False
for i, line in enumerate(lines):
    if 'const SHELL_ASSETS' in line:
        in_shell = True
    if in_shell and '];' in line:
        print(f"\nSHELL_ASSETS ends at line {i+1}: {line.rstrip()}")
        # Print a few lines before the end
        for j in range(max(0, i-5), i+1):
            print(f"  {j+1}: {lines[j].rstrip()}")
        break

# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the end of notesView div - look for closing div pattern after line 3287
depth = 0
in_notes = False
for i in range(3286, min(len(lines), 3500)):
    line = lines[i]
    if 'id="notesView"' in line:
        in_notes = True
    if in_notes:
        depth += line.count('<div') + line.count('<DIV')
        depth -= line.count('</div') + line.count('</DIV')
        if depth <= 0:
            print(f"notesView closes at line {i+1}: {line.rstrip()[:120]}")
            # Print a few lines after
            for j in range(i+1, min(len(lines), i+10)):
                print(f"  Line {j+1}: {lines[j].rstrip()[:120]}")
            break

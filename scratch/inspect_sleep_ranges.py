# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_range(start, end, title):
    print(f"\n==================== {title} (L{start}-L{end}) ====================")
    for i in range(start - 1, min(end, len(lines))):
        print(f"{i + 1:5d}: {lines[i]}", end='')

print_range(6365, 6420, "SLEEP_HABITS & Constants")
print_range(8105, 8140, "Sleep Storage Functions")
print_range(15695, 15785, "Sleep Render Functions")

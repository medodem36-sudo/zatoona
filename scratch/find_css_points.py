# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find notes-related CSS
for i, line in enumerate(lines):
    if 'notesHub' in line.lower() or 'notes-hub' in line.lower() or '#notesView' in line:
        if i < 3286:  # only CSS part (before HTML)
            print(f"Line {i+1}: {line.rstrip()[:120]}")

# Find last CSS before </style>
for i, line in enumerate(lines):
    if '</style>' in line and i < 2200:
        print(f"\n</style> at line {i+1}")
        for j in range(max(0, i-3), i+1):
            print(f"  Line {j+1}: {lines[j].rstrip()[:120]}")

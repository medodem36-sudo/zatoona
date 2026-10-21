# -*- coding: utf-8 -*-
"""Find exact line numbers for all insertion points in index.html"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = [
    "exercise-catalog.js",           # script include position
    "const NAV_MODES",               # nav modes array
    "drawNav-notes",                 # last drawer button
    "sideNav-notes",                 # last sidebar button
    "modeNotes",                     # last mode button in modesBar
    "id=\"notesView\"",              # notes view div start
    "function applyMode(",           # applyMode function
    "notes: document.getElementById('notesView')",  # views map
    "notes: document.getElementById('modeNotes')",  # btns map
    "notes: ['📝",                  # titles map
    "if(mode==='notes') renderNotesHub()",  # render call
    "mode==='budget' || mode==='notes'",    # week cal hide
    "wireActivate(document.getElementById('modeNotes')",  # wire
    "</head>",                       # end of head (for CSS)
    "</body>",                       # end of body
    "function renderNotesHub(",      # notes hub function
]

for t in targets:
    found = False
    for i, line in enumerate(lines):
        if t in line:
            print(f"Line {i+1}: {t}")
            print(f"  Content: {line.rstrip()[:120]}")
            found = True
            break
    if not found:
        print(f"NOT FOUND: {t}")

print(f"\nTotal lines: {len(lines)}")

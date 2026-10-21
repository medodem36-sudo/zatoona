import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
output_lines.append(f"Total lines: {len(lines)}")

# 1. Inspect notesView HTML
for i, line in enumerate(lines):
    if 'id="notesView"' in line:
        output_lines.append(f"\n=== Found #notesView at line {i+1} ===")
        for j in range(i, min(len(lines), i + 140)):
            output_lines.append(f"{j+1}: {lines[j]}")
            if '</div' in lines[j] and j > i + 100:
                pass
        break

# 2. Inspect notes JS functions
functions_to_find = [
    'notesHubState',
    'function collectAllUnifiedNotes',
    'function renderNotesHub',
    'function openNoteInOriginalSection',
    'function initNotesHubEvents'
]

for fn in functions_to_find:
    found = False
    for i, line in enumerate(lines):
        if fn in line:
            output_lines.append(f"\n=== Found {fn} at line {i+1} ===")
            for j in range(i, min(len(lines), i + 120)):
                output_lines.append(f"{j+1}: {lines[j]}")
            found = True
            break
    if not found:
        output_lines.append(f"\n=== NOT FOUND: {fn} ===")

with open('scratch/notes_code_extracted.txt', 'w', encoding='utf-8') as out:
    out.write(''.join(output_lines))

print("Extracted to scratch/notes_code_extracted.txt")

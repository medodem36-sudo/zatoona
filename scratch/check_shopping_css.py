import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '.check-row' in line or '.checklist' in line or '.list-footer' in line:
        print(f"=== Found at line {i+1} ===")
        for j in range(max(0, i-2), min(len(lines), i+25)):
            print(f"{j+1}: {lines[j]}", end='')
        break

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'function renderTabs' in line or 'function setMode' in line:
        print(f"=== Found at line {i+1} ===")
        for j in range(max(0, i-2), min(len(lines), i+30)):
            print(f"{j+1}: {lines[j]}", end='')

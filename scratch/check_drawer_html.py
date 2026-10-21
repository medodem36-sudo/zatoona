import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="drawer"' in line or 'class="drawer' in line or 'id="sidebar"' in line or 'class="sidebar' in line:
        print(f"=== Found at line {i+1} ===")
        for j in range(max(0, i-2), min(len(lines), i+35)):
            print(f"{j+1}: {lines[j]}", end='')

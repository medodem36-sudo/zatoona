import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'function switchMode' in line or 'function setMode' in line or 'mode-btn' in line:
        print(f"=== Found at line {i+1} ===")
        for j in range(max(0, i-2), min(len(lines), i+20)):
            print(f"{j+1}: {lines[j]}", end='')
        break

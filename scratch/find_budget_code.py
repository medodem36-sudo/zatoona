import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'function addExpense' in line:
        print(f"=== Found at line {i+1} ===")
        start = max(0, i - 10)
        end = min(len(lines), i + 70)
        for j in range(start, end):
            print(f"{j+1}: {lines[j]}", end='')

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="mealView"' in line or "id='mealView'" in line:
        print(f"=== Found mealView at line {i+1} ===")
        for j in range(max(0, i-5), min(len(lines), i+40)):
            print(f"{j+1}: {lines[j]}", end='')
        break

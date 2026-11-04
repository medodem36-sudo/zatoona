import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('docs/PROJECT_STATUS.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("PROJECT_STATUS.md lines:", len(lines))
for i in range(max(0, len(lines)-25), len(lines)):
    print(f"{i+1}: {lines[i]}", end='')

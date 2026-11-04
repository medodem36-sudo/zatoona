import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('docs/PROJECT_STATUS.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("PROJECT_STATUS.md length:", len(text))
# Let's print the last sections of PROJECT_STATUS.md
lines = text.splitlines()
for l in lines[-60:]:
    print(l)

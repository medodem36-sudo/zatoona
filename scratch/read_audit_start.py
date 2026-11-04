import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('docs/Final_Master_Plan_Acceptance_Audit.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("Final_Master_Plan_Acceptance_Audit.md length:", len(text))
for line in text.splitlines()[:50]:
    print(line)

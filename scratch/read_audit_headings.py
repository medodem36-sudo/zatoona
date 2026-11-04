import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('docs/Final_Master_Plan_Acceptance_Audit.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find sections around recommendations or gaps
for line in text.splitlines():
    if line.startswith('## 3') or line.startswith('## 4') or line.startswith('## 5') or line.startswith('## 6') or 'Proposal' in line or 'Recommendation' in line or 'Roadmap' in line:
        print(line)

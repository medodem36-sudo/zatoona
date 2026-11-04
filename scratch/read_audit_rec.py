import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('docs/Final_Master_Plan_Acceptance_Audit.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('## 5. Prioritized Improvement Recommendations')
print(text[idx:idx+3500])

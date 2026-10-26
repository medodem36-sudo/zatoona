import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/Final_Master_Plan_Reconciliation_v3.md', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('| **9.2**')
end_idx = text.find('## 4. التدقيق المتخصص لأنظمة التدريب والتمارين')

if start_idx != -1 and end_idx != -1:
    section3_rest = text[start_idx:end_idx]
    for line in section3_rest.splitlines()[:60]:
        print(line)

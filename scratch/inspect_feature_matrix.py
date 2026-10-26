import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/Final_Master_Plan_Reconciliation_v3.md', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('## 3. مصفوفة الجرد الشاملة لجميع الميزات')
end_idx = text.find('## 4. التدقيق المتخصص لأنظمة التدريب والتمارين')

if start_idx != -1 and end_idx != -1:
    section3 = text[start_idx:end_idx]
    print("Section 3 length:", len(section3))
    # Print the first 50 lines
    for line in section3.splitlines()[:60]:
        print(line)
else:
    print("Could not find section boundaries")

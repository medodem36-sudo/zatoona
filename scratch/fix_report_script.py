import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/write_phase13_1_report.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('content = """', 'content = r"""')
with open('scratch/write_phase13_1_report.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed write_phase13_1_report.py")

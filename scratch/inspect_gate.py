import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/test_master_regression_gate.py', 'r', encoding='utf-8') as f:
    text = f.read()

print('=== test_master_regression_gate.py ===')
print(text[:1500])
print('...\n' + text[-1000:])

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'getElementById\([\'\"]encConfirmAddBtn[\'\"]\)', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 800)
    print('--- Found getElementById encConfirmAddBtn ---')
    print(text[start:end])

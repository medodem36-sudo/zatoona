import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function saveCustomExercise\s*\([\s\S]*?\nfunction\s+', text)
if m:
    code = m.group(0)
    for line in code.split('\n'):
        if 'img' in line:
            print(line)

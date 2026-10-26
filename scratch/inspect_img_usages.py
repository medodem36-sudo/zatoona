import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for pattern in [r'\bex\.img\b', r'\bex-photo\b', r'getExerciseImageRecord']:
    matches = [m.start() for m in re.finditer(pattern, text)]
    print(f'Pattern "{pattern}": {len(matches)} occurrences')
    for p in matches[:3]:
        print('  ', text[max(0, p-60):min(len(text), p+140)].replace('\n', ' '))

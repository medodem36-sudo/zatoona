import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'catalogExerciseId', text)]
print(f'Found {len(matches)} occurrences of catalogExerciseId')
for p in matches[:5]:
    print('  ', text[max(0, p-40):min(len(text), p+80)].replace('\n', ' '))

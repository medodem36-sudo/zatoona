import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function getExerciseImageRecord\([^\)]*\)\s*\{[\s\S]*?\n\}', text)
if m:
    print('=== getExerciseImageRecord ===')
    print(m.group(0))

m2 = re.search(r'function setExerciseLocalImage\([^\)]*\)\s*\{[\s\S]*?\n\}', text)
if m2:
    print('\n=== setExerciseLocalImage ===')
    print(m2.group(0)[:600])

m3 = re.search(r'function refreshExerciseViewsAfterImageChange\([^\)]*\)\s*\{[\s\S]*?\n\}', text)
if m3:
    print('\n=== refreshExerciseViewsAfterImageChange ===')
    print(m3.group(0))

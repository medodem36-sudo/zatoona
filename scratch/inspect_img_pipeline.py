import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Search for transformTemplateExerciseToRuntime
m = re.search(r'function transformTemplateExerciseToRuntime\([\s\S]*?\{[\s\S]*?\n\}', html)
if m:
    print('=== transformTemplateExerciseToRuntime ===')
    print(m.group(0))

# Search for how ex.img is resolved in renderExercises or wherever exercise cards are built
ex_card_matches = re.findall(r'(\bex\.img\b[\s\S]{0,100})', html)
print(f'\nFound {len(ex_card_matches)} occurrences of ex.img:')
for i, c in enumerate(ex_card_matches[:6]):
    print(f'[{i}] {c.strip()}\n---')

# Search for exercise-image-map
img_map_matches = re.findall(r'(\bexercise-image-map-v1\b[\s\S]{0,200})', html)
print(f'\nFound {len(img_map_matches)} occurrences of exercise-image-map-v1:')
for i, c in enumerate(img_map_matches[:3]):
    print(f'[{i}] {c.strip()}\n---')

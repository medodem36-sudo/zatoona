with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Total lines in exercise-catalog.js:', len(lines))
print('First 10 lines:')
for l in lines[:10]:
    print('  ', l.rstrip())

print('\nLast 10 lines:')
for l in lines[-10:]:
    print('  ', l.rstrip())

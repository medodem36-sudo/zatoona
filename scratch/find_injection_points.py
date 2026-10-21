with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '</style>' in line:
        print(f'CSS ends at line {i+1}: {line.strip()}')
    if 'id="gymWorkoutBlock"' in line:
        print(f'gymWorkoutBlock at line {i+1}: {line.strip()}')
    if 'function renderWarmup()' in line:
        print(f'renderWarmup at line {i+1}: {line.strip()}')
    if 'renderRestTimerCard();' in line:
        print(f'renderRestTimerCard called at line {i+1}: {line.strip()}')
    if 'const KNOWN_KEY_PATTERNS =' in line:
        print(f'KNOWN_KEY_PATTERNS at line {i+1}: {line.strip()[:80]}')

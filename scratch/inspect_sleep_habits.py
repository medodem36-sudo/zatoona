import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

terms = [
    'SLEEP_QUALITY_OPTS', 'sleepq:', 'sleepQuality', 'renderSleepBlock',
    'scheduleSleepBlock', 'scSleepHours', 'scNapEnabled', 'scNapDuration',
    'scSleepStartOffset', 'nap', 'bedtime'
]

for t in terms:
    matches = [m.start() for m in re.finditer(re.escape(t), content)]
    print(f"=== {t} matches: {len(matches)} ===")
    for p in matches[:2]:
        print(content[max(0, p-60):min(len(content), p+250)])
        print("-" * 30)

# Check all functions containing 'sleep' or 'nap'
funcs = set(re.findall(r'function\s+([a-zA-Z0-9_]*(?:sleep|nap|bedtime|recovery)[a-zA-Z0-9_]*)\s*\(', content, re.IGNORECASE))
print(f"\nFunctions with sleep/nap/bedtime/recovery: {funcs}")

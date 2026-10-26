import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'const\s+SLEEP_HABITS\s*=\s*\[', content)
if m:
    start = m.start()
    print("=== SLEEP_HABITS ===")
    print(content[start:start+600])

m2 = re.search(r'function\s+renderSleepHabits\s*\(', content)
if m2:
    start = m2.start()
    print("\n=== renderSleepHabits ===")
    print(content[start:start+800])
else:
    # search for where 'sleepHabits' is used in rendering
    matches = [m.start() for m in re.finditer(r'sleepHabits', content)]
    print(f"\nMatches for sleepHabits: {len(matches)}")
    for p in matches[2:6]:
        print(content[max(0, p-50):min(len(content), p+250)])
        print("-" * 30)

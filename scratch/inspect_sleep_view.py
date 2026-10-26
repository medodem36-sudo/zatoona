import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

terms = ['sleepHabits', 'loadSleepHabits', 'saveSleepHabits', 'renderSleep']

for t in terms:
    pattern = rf'(?:function|let|const|var)\s+{t}[^{{;]*'
    m = re.search(pattern, content)
    if m:
        start = m.start()
        print(f"\n=== FOUND: {t} ===")
        print(content[start:start+1200])
    else:
        matches = [m.start() for m in re.finditer(re.escape(t), content)]
        print(f"\n=== SEARCH: {t} ({len(matches)} matches) ===")
        for p in matches[:3]:
            print(content[max(0, p-50):min(len(content), p+350)])
            print("-" * 30)

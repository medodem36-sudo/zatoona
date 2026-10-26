import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

terms = ['scheduleCheckState', 'saveScheduleCheck', 'loadScheduleCheck', 'scheduleCheck:']
for t in terms:
    matches = [m.start() for m in re.finditer(re.escape(t), content)]
    print(f"=== {t} matches: {len(matches)} ===")
    for p in matches[:3]:
        print(content[max(0, p-40):min(len(content), p+200)])
        print("-" * 30)

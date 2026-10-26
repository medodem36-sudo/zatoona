import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for sid in ['prayerCitySelect', 'scPrayerCity']:
    matches = [m.start() for m in re.finditer(re.escape(sid), content)]
    print(f"=== {sid} matches: {len(matches)} ===")
    for p in matches:
        print(content[max(0, p-100):min(len(content), p+300)])
        print("-" * 40)

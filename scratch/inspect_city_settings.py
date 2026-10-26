import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check default schedule settings
m = re.search(r'(?:const|let|var)\s+[a-zA-Z0-9_]*SETTINGS[^{;]*=\s*\{[^}]+\}', content, re.IGNORECASE)
if m:
    print("=== Settings ===")
    print(m.group(0))

# Search for prayerCity in schedule settings
matches = [m.start() for m in re.finditer(r'prayerCity', content)]
print(f"=== prayerCity occurrences: {len(matches)} ===")
for p in matches:
    print(content[max(0, p-60):min(len(content), p+150)].replace('\n', ' '))
    print("-" * 30)

# Check loadScheduleSettings / DEFAULT_SCHEDULE_SETTINGS
m2 = re.search(r'function\s+loadScheduleSettings\s*\([^{]*\{', content)
if m2:
    start = m2.start()
    print("=== loadScheduleSettings ===")
    print(content[start:start+600])

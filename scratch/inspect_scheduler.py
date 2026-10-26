import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'function\s+initNotificationScheduler\s*\([^{]*\{', content)
if m:
    start = m.start()
    print("=== initNotificationScheduler ===")
    print(content[start:start+1200])

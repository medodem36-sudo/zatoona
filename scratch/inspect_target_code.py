import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS styling for .check-row, .check-left, .cname, .toggle-group, .tbtn
css_match = re.search(r'\.checklist\{[^}]+\}', content)
if css_match:
    start = css_match.start()
    print("=== CSS for checklist & check-row ===")
    print(content[start:start+1200])

# 2. Exact code of renderSimpleChecklist
m1 = re.search(r'function\s+renderSimpleChecklist\s*\([^{]*\{', content)
if m1:
    start = m1.start()
    print("\n=== renderSimpleChecklist ===")
    print(content[start:start+600])

# 3. Exact code of renderScheduleChecklist
m2 = re.search(r'function\s+renderScheduleChecklist\s*\([^{]*\{', content)
if m2:
    start = m2.start()
    print("\n=== renderScheduleChecklist ===")
    print(content[start:start+750])

# 4. Check how other checklist items are rendered (e.g., renderPrayerFard)
m3 = re.search(r'function\s+renderPrayerFard\s*\([^{]*\{', content)
if m3:
    start = m3.start()
    print("\n=== renderPrayerFard (reference style) ===")
    print(content[start:start+750])

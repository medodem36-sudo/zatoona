import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Inspect renderScheduleChecklist
m = re.search(r'function\s+renderScheduleChecklist\s*\([^{]*\{', content)
if m:
    start = m.start()
    print("=== renderScheduleChecklist ===")
    print(content[start:start+2000])

# Also check other checklists in the app:
# Let's search for all .className = 'check-row' or innerHTML with check-row
print("\n=== All check-row constructions in the app ===")
matches = [m.start() for m in re.finditer(r'check-row', content)]
print(f"Total occurrences of check-row: {len(matches)}")

for idx, pos in enumerate(matches):
    snippet = content[max(0, pos-100):min(len(content), pos+350)]
    # print context of each
    first_line = snippet.split('\n')[0]
    print(f"\n--- Occurrence {idx+1} (char {pos}) ---")
    print('\n'.join(snippet.splitlines()[:10]))

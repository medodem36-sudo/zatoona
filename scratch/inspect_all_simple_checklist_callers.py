import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

matches = [m.start() for m in re.finditer(r'renderSimpleChecklist\s*\(', content)]
print(f"Total callers of renderSimpleChecklist: {len(matches)}")

for idx, p in enumerate(matches):
    print(f"\n--- Caller {idx+1} (char {p}) ---")
    snippet = content[max(0, p-50):min(len(content), p+350)]
    print(snippet)

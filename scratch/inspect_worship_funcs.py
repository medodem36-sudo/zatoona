import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

funcs_to_find = [
    'renderSimpleChecklist', 'renderPrayerFard', 'renderQuranWird',
    'renderAzkar', 'renderScheduleChecklist', 'loadPrayer', 'savePrayer',
    'loadQuran', 'saveQuran', 'loadAzkar', 'saveAzkar'
]

for fn in funcs_to_find:
    pattern = rf'function\s+{fn}\s*\([^{{]*\{{'
    m = re.search(pattern, content)
    if m:
        start = m.start()
        # Find closing brace (simplified: next 1500 chars or until next function)
        snippet = content[start:start+2500]
        print(f"\n==================== FUNCTION: {fn} ====================")
        print(snippet[:1800])
    else:
        print(f"\n[NOT FOUND] Function: {fn}")

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

terms = [
    'قيام الليل', 'باقي النوافل', 'أذكار الصباح', 'القرآن والورد',
    'سماع القرآن', 'قراءة القرآن', 'حفظ آيتين', 'مراجعة الحفظ',
    'تشيك ليست', 'checklist', 'worship'
]

print("=== 1. SEARCH FOR WORSHIP AND CHECKLIST TERMS ===")
for t in terms:
    matches = [m.start() for m in re.finditer(re.escape(t), content, re.IGNORECASE)]
    print(f"\n>>> Term: '{t}' -> {len(matches)} occurrences")
    for idx, p in enumerate(matches[:3]):
        snippet = content[max(0, p-150):min(len(content), p+250)]
        # replace newlines with \n for compact display
        cleaned = '\n'.join([line.strip() for line in snippet.splitlines() if line.strip()])
        print(f"  [Match {idx+1} at char {p}]:\n{cleaned}\n")

# Find functions related to worship and checklist
print("\n=== 2. FUNCTIONS RELATED TO WORSHIP / CHECKLIST ===")
func_matches = re.findall(r'function\s+([a-zA-Z0-9_]*(?:worship|checklist|azkar|quran|prayer)[a-zA-Z0-9_]*)\s*\(', content, re.IGNORECASE)
print(f"Functions found: {set(func_matches)}")

# Also look for object keys or state definitions
print("\n=== 3. DATA STRUCTURES & KEYS ===")
storage_keys = set(re.findall(r"localStorage\.(?:getItem|setItem)\(['\"]([^'\"]*(?:worship|checklist|azkar|quran|habit)[^'\"]*)['\"]", content, re.IGNORECASE))
print(f"LocalStorage keys matching pattern: {storage_keys}")

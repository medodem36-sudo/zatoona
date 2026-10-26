import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Search for PRAYER_SUPPORTED_CITIES
for m in re.finditer(r'PRAYER_SUPPORTED_CITIES', content):
    p = m.start()
    print("=== PRAYER_SUPPORTED_CITIES ===")
    print(content[max(0, p-50):min(len(content), p+400)])
    print("-" * 40)

# 2. Search for all Minya / Alexandria / Cairo occurrences
for city in ['Minya', 'Alexandria', 'Cairo', 'المنيا', 'الإسكندرية', 'القاهرة']:
    matches = [m.start() for m in re.finditer(re.escape(city), content)]
    print(f"=== City term '{city}': {len(matches)} occurrences ===")
    for p in matches[:5]:
        print(content[max(0, p-60):min(len(content), p+150)].replace('\n', ' '))
    print("-" * 40)

# 3. Check HTML select elements for city selection
for sel in ['prayerCitySelect', 'scPrayerCity']:
    matches = [m.start() for m in re.finditer(re.escape(sel), content)]
    print(f"=== Select ID '{sel}': {len(matches)} occurrences ===")
    for p in matches:
        print(content[max(0, p-60):min(len(content), p+200)].replace('\n', ' '))
    print("-" * 40)

# 4. Check loadPrayerCity, savePrayerCity, onCityChange
funcs = ['loadPrayerCity', 'savePrayerCity', 'onCityChange', 'ensurePrayerTimes', 'fetchPrayerTimesForMonth']
for fn in funcs:
    m = re.search(rf'function\s+{fn}\s*\([^{{]*\{{', content)
    if m:
        start = m.start()
        print(f"=== Function {fn} ===")
        print(content[start:start+700])
        print("-" * 40)

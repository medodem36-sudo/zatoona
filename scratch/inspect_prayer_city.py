import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

terms = [
    'PRAYER_SUPPORTED_CITIES', 'loadPrayerCity', 'savePrayerCity',
    'fetchPrayerTimesForMonth', 'PRAYER_API_BASE', 'prayerCitySelect',
    'onPrayerRefresh', 'ensurePrayerTimes', 'loadCachedPrayerTimes',
    'saveCachedPrayerTimes', 'PRAYERS'
]

for t in terms:
    pattern = rf'(?:const|function|var|let)\s+{t}[^{{;]*'
    m = re.search(pattern, content)
    if m:
        start = m.start()
        print(f"\n==================== FOUND: {t} ====================")
        print(content[start:start+1200])
    else:
        # Search anywhere
        matches = [m.start() for m in re.finditer(re.escape(t), content)]
        print(f"\n==================== SEARCH: {t} ({len(matches)} matches) ====================")
        if matches:
            p = matches[0]
            print(content[max(0, p-50):min(len(content), p+400)])

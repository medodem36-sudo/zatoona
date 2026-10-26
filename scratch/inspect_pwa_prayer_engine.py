import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    text = f.read()

for fn in ['ensurePrayerTimes', 'fetchPrayerTimesFromAPI', 'fallbackPrayerTimes', 'FALLBACK_PRAYER_TIMES']:
    idx = text.find(fn)
    if idx != -1:
        print(f"=== {fn} ===")
        print(text[idx:idx+800])

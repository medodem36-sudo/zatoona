import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('fetchPrayerTimesForMonth')
print(text[idx:idx+1500])

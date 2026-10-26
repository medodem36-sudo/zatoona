import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. NOTIFICATIONS IN sw.js ===")
with open('sw.js', 'r', encoding='utf-8') as f:
    sw_content = f.read()

sw_notif = re.findall(r'(?:push|notification|alarm|sync|message)[a-zA-Z0-9_]*', sw_content, re.IGNORECASE)
print(f"Terms in sw.js: {set(sw_notif)}")
# Check all event listeners in sw.js
listeners = re.findall(r"self\.addEventListener\(['\"]([^'\"]+)['\"]", sw_content)
print(f"All addEventListener in sw.js: {listeners}")

print("\n=== 2. NOTIFICATIONS IN manifest.json ===")
with open('manifest.json', 'r', encoding='utf-8') as f:
    manifest_content = f.read()
print(manifest_content[:500])

print("\n=== 3. NOTIFICATIONS IN index.html ===")
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

notif_patterns = [
    r'Notification\.requestPermission',
    r'showNotification',
    r'new Notification',
    r'navigator\.serviceWorker\.ready',
    r'PushManager',
    r'pushManager',
    r'function\s+[a-zA-Z0-9_]*remind[a-zA-Z0-9_]*',
    r'function\s+[a-zA-Z0-9_]*notif[a-zA-Z0-9_]*',
    r'function\s+[a-zA-Z0-9_]*alarm[a-zA-Z0-9_]*'
]

for p in notif_patterns:
    matches = list(re.finditer(p, html_content, re.IGNORECASE))
    print(f"Pattern '{p}': {len(matches)} matches")
    for m in matches[:2]:
        start = m.start()
        print(html_content[max(0, start-40):min(len(html_content), start+200)])
        print("-" * 30)

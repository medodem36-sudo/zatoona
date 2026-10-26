import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

funcs = [
    'checkAndDispatchDueReminders', 'tryDispatchNotification',
    'tryDispatchWindowNotification', 'routeNotificationClick',
    'startReminderInterval', 'initNotifications'
]

for fn in funcs:
    pattern = rf'function\s+{fn}\s*\([^{{]*\{{'
    m = re.search(pattern, content)
    if m:
        start = m.start()
        print(f"\n=== FUNCTION: {fn} ===")
        print(content[start:start+1200])
    else:
        # Search anywhere
        matches = [m.start() for m in re.finditer(re.escape(fn), content)]
        print(f"\n=== SEARCH: {fn} ({len(matches)} matches) ===")
        if matches:
            p = matches[0]
            print(content[max(0, p-50):min(len(content), p+400)])

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'\.toggle-group\{[^}]+\}', content)
if m:
    start = m.start()
    print("=== .toggle-group CSS ===")
    print(content[start:start+400])

m2 = re.search(r'\.tbtn\{[^}]+\}', content)
if m2:
    start = m2.start()
    print("=== .tbtn CSS ===")
    print(content[start:start+400])

m3 = re.search(r'\.tbtn\.on-right\{[^}]+\}', content)
if m3:
    start = m3.start()
    print("=== .tbtn.on-right CSS ===")
    print(content[start:start+400])

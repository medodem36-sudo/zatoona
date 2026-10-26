import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'function\s+renderShopping\s*\([^{]*\{', content)
if m:
    start = m.start()
    print("=== renderShopping body ===")
    print(content[start+1000:start+2800])

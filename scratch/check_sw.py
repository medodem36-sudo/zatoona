import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    text = f.read()

listeners = re.findall(r'self\.addEventListener\s*\(\s*["\']([^"\']+)["\']', text)
print('Service worker event listeners:', listeners)

for l in listeners:
    idx = text.find(f"addEventListener('{l}'")
    if idx == -1:
        idx = text.find(f'addEventListener("{l}"')
    if idx != -1:
        print(f'\n--- Listener: {l} ---')
        print(text[idx:idx+400])

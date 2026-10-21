import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

with open('manifest.json', 'r', encoding='utf-8') as f:
    mf = json.load(f)

print('=== MANIFEST.JSON AUDIT ===')
print('Name:', mf.get('name'))
print('Short name:', mf.get('short_name'))
print('Start URL:', mf.get('start_url'))
print('Display:', mf.get('display'))
print('Theme color:', mf.get('theme_color'))
print('Background color:', mf.get('background_color'))
print('Icons count:', len(mf.get('icons', [])))
for icon in mf.get('icons', []):
    src = icon.get('src')
    exists = os.path.exists(src) if src else False
    print(f'  {str(src):30} ({icon.get("sizes")}) exists: {exists}')

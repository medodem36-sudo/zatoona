import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target1 = """        <select id="prayerCitySelect" class="weight-input" style="padding:4px 8px; font-size:.8rem; border-radius:6px;">
          <option value="Minya">المنيا (Minya)</option>
          <option value="Alexandria">الإسكندرية (Alexandria)</option>
        </select>"""

replacement1 = """        <select id="prayerCitySelect" class="weight-input" style="padding:4px 8px; font-size:.8rem; border-radius:6px;">
          <option value="Minya">المنيا (Minya)</option>
          <option value="Alexandria">الإسكندرية (Alexandria)</option>
          <option value="Cairo">القاهرة (Cairo)</option>
        </select>"""

target2 = """        <select id="scPrayerCity" class="weight-input" style="width:100%;">
          <option value="Minya">المنيا (Minya)</option>
          <option value="Alexandria">الإسكندرية (Alexandria)</option>
        </select>"""

replacement2 = """        <select id="scPrayerCity" class="weight-input" style="width:100%;">
          <option value="Minya">المنيا (Minya)</option>
          <option value="Alexandria">الإسكندرية (Alexandria)</option>
          <option value="Cairo">القاهرة (Cairo)</option>
        </select>"""

target3 = """/* ================= STAGE 3D: PRAYER API & CACHE ================= */
const PRAYER_SUPPORTED_CITIES = ['Minya', 'Alexandria'];"""

replacement3 = """/* ================= STAGE 3D: PRAYER API & CACHE ================= */
const PRAYER_SUPPORTED_CITIES = ['Minya', 'Alexandria', 'Cairo'];"""

target4 = """  prayerCity:'Minya', // Stage 3D: selected prayer city (Minya | Alexandria)"""
replacement4 = """  prayerCity:'Minya', // Stage 3D: selected prayer city (Minya | Alexandria | Cairo)"""

for idx, (t, r) in enumerate([(target1, replacement1), (target2, replacement2), (target3, replacement3), (target4, replacement4)]):
    count = content.count(t)
    print(f"Target {idx+1} occurrences: {count}")
    if count != 1:
        print(f"ERROR: Target {idx+1} not found exactly once.")
        sys.exit(1)

content = content.replace(target1, replacement1, 1)
content = content.replace(target2, replacement2, 1)
content = content.replace(target3, replacement3, 1)
content = content.replace(target4, replacement4, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('zatoona.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: index.html and zatoona.html updated and synchronized byte-for-byte!")

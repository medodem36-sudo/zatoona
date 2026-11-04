import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

targets = {
    'target_css': "/* --- Phase 7 Styles --- */",
    'target_amoled_place': '''<div class="settings-row">
        <div>
          <div class="settings-row-label">حجم الخط</div>
          <div class="settings-row-desc">عادي (100%) أو كبير مريح (112%)</div>
        </div>
        <button type="button" class="settings-toggle" id="settingsFontToggle" onclick="toggleSettingsFont()"></button>
      </div>''',
    'target_flash_place': '''<div class="settings-row">
        <div>
          <div class="settings-row-label">مدينة الصلاة</div>
          <div class="settings-row-desc">لحساب مواقيت الصلاة والأذان</div>
        </div>
        <select id="settingsPrayerCity" class="str-filter-dropdown" style="max-width:140px;" onchange="savePrayerCitySetting(this.value)">
          <option value="cairo">القاهرة</option>
          <option value="alexandria">الإسكندرية</option>
          <option value="minya">المنيا</option>
        </select>
      </div>''',
    'target_overlay_place': "</body>",
    'target_js_place': "</script>\n\n<!-- 3. Zatoona Wrapped Fullscreen Festive Modal -->"
}

all_found = True
for name, t in targets.items():
    found = t in content
    print(f"Target '{name}': {found}")
    if not found:
        all_found = False

print("ALL TARGETS FOUND:", all_found)

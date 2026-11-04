#!/usr/bin/env python3
"""
Zatoona Consolidation Phase — Master Injection Script
=====================================================
1. Remove scrollbar column (CSS + Android WebView)
2. Consolidate Recovery & Stretches into Gym as sub-tabs
3. Reorganize navigation (Drawer, Sidebar, ModesBar) with new order
4. Add dedicated Settings view (#settingsView)
5. Add new color themes (Amber, Violet, Crimson, Emerald, Titanium)
6. Add ultra-compact layout toggle
7. Add feature toggles (hide/show modules)
8. Update applyMode, navigateTo, NAV_MODES, syncNavigation
9. Update ALLOWED_MODES in ZatoonaBridge.kt
10. Maintain 3-way HTML parity
"""
import hashlib, os, shutil, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

INDEX = 'index.html'
ZATOONA = 'zatoona.html'
ANDROID_HTML = 'android/app/src/main/assets/index.html'
BRIDGE_KT = 'android/app/src/main/java/com/zatoona/app/ZatoonaBridge.kt'
MAIN_KT = 'android/app/src/main/java/com/zatoona/app/MainActivity.kt'

def read_utf8(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_utf8(path, content):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

def sha256(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

# ─── Verify initial parity ───
h0 = sha256(INDEX)
assert sha256(ZATOONA) == h0, "Parity broken before start"
assert sha256(ANDROID_HTML) == h0, "Parity broken before start"
print(f"[OK] Initial parity confirmed: {h0}")

html = read_utf8(INDEX)

# ============================================================
# STEP 1: Global scrollbar removal CSS
# ============================================================
print("[1/10] Injecting global scrollbar removal CSS...")

SCROLLBAR_CSS = """
/* === Global scrollbar removal === */
html, body, * {
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
}
::-webkit-scrollbar {
  display: none !important;
  width: 0 !important;
  height: 0 !important;
}
"""

# Insert after the very first <style> opening tag
first_style_pos = html.find('<style>')
assert first_style_pos != -1, "Cannot find <style> tag"
insert_after = html.find('\n', first_style_pos) + 1
html = html[:insert_after] + SCROLLBAR_CSS + html[insert_after:]
print("  Scrollbar CSS injected.")

# ============================================================
# STEP 2: Add new color theme CSS variables
# ============================================================
print("[2/10] Injecting new color theme CSS...")

NEW_THEMES_CSS = """
/* === New Color Themes === */
body.theme-amber {
  --bg: #fef3c7; --bg-2: #fde68a; --card: #fffbeb; --card-alt: #fef9c3;
  --text: #78350f; --muted: #92400e; --line: #fbbf24; --accent: #d97706;
  --good: #059669; --bad: #dc2626; --shadow: rgba(217,119,6,.12);
}
body.theme-amber.dark-mode, body.theme-amber.amoled-mode {
  --bg: #1c1107; --bg-2: #2a1b0a; --card: #312311; --card-alt: #3d2c14;
  --text: #fef3c7; --muted: #fbbf24; --line: #78350f; --accent: #f59e0b;
  --shadow: rgba(245,158,11,.15);
}
body.theme-violet {
  --bg: #ede9fe; --bg-2: #ddd6fe; --card: #f5f3ff; --card-alt: #ede9fe;
  --text: #3b0764; --muted: #6b21a8; --line: #a78bfa; --accent: #7c3aed;
  --good: #059669; --bad: #dc2626; --shadow: rgba(124,58,237,.12);
}
body.theme-violet.dark-mode, body.theme-violet.amoled-mode {
  --bg: #0f0720; --bg-2: #1a0e33; --card: #1e1145; --card-alt: #27175a;
  --text: #ede9fe; --muted: #a78bfa; --line: #4c1d95; --accent: #8b5cf6;
  --shadow: rgba(139,92,246,.18);
}
body.theme-crimson {
  --bg: #fef2f2; --bg-2: #fecaca; --card: #fff5f5; --card-alt: #fee2e2;
  --text: #7f1d1d; --muted: #991b1b; --line: #fca5a5; --accent: #dc2626;
  --good: #059669; --bad: #c026d3; --shadow: rgba(220,38,38,.12);
}
body.theme-crimson.dark-mode, body.theme-crimson.amoled-mode {
  --bg: #1a0505; --bg-2: #2d0a0a; --card: #3b1010; --card-alt: #4a1515;
  --text: #fef2f2; --muted: #fca5a5; --line: #7f1d1d; --accent: #ef4444;
  --shadow: rgba(239,68,68,.18);
}
body.theme-emerald {
  --bg: #ecfdf5; --bg-2: #a7f3d0; --card: #f0fdf4; --card-alt: #d1fae5;
  --text: #064e3b; --muted: #065f46; --line: #6ee7b7; --accent: #059669;
  --good: #2563eb; --bad: #dc2626; --shadow: rgba(5,150,105,.12);
}
body.theme-emerald.dark-mode, body.theme-emerald.amoled-mode {
  --bg: #021c14; --bg-2: #042f22; --card: #064e3b; --card-alt: #065f46;
  --text: #ecfdf5; --muted: #6ee7b7; --line: #064e3b; --accent: #10b981;
  --shadow: rgba(16,185,129,.18);
}
body.theme-titanium {
  --bg: #f4f4f5; --bg-2: #d4d4d8; --card: #fafafa; --card-alt: #e4e4e7;
  --text: #18181b; --muted: #52525b; --line: #a1a1aa; --accent: #52525b;
  --good: #059669; --bad: #dc2626; --shadow: rgba(82,82,91,.10);
}
body.theme-titanium.dark-mode, body.theme-titanium.amoled-mode {
  --bg: #09090b; --bg-2: #18181b; --card: #27272a; --card-alt: #3f3f46;
  --text: #fafafa; --muted: #a1a1aa; --line: #3f3f46; --accent: #a1a1aa;
  --shadow: rgba(161,161,170,.12);
}

/* === Ultra-compact density === */
body.ultra-compact .section-title { margin-top: 6px; margin-bottom: 2px; font-size: .78rem; }
body.ultra-compact .section-hint { margin-bottom: 4px; font-size: .68rem; }
body.ultra-compact .info-card { padding: 8px 10px; margin-bottom: 6px; }
body.ultra-compact .check-row { padding: 4px 6px; min-height: 28px; }
body.ultra-compact .settings-card { padding: 6px; }
body.ultra-compact .mode-btn { padding: 8px 6px; }
body.ultra-compact .home-card { padding: 10px; margin-bottom: 6px; }

/* === Gym Sub-Tabs === */
.gym-subtabs {
  display: flex; gap: 0; margin-bottom: 14px; border-radius: 10px;
  overflow: hidden; border: 1px solid var(--line); background: var(--card-alt);
}
.gym-subtab-btn {
  flex: 1; padding: 9px 6px; font-size: .78rem; font-weight: 700;
  border: none; background: transparent; color: var(--muted); cursor: pointer;
  transition: background .2s, color .2s; text-align: center; white-space: nowrap;
}
.gym-subtab-btn.active {
  background: var(--accent); color: #fff;
}

/* === Settings View Styles === */
.settings-section-card {
  background: var(--card); border: 1px solid var(--line); border-radius: 12px;
  padding: 16px; margin-bottom: 14px;
}
.settings-section-title {
  font-size: .85rem; font-weight: 800; color: var(--text); margin-bottom: 10px;
  display: flex; align-items: center; gap: 8px;
}
.settings-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 0; border-bottom: 1px solid var(--line);
}
.settings-row:last-child { border-bottom: none; }
.settings-row-label {
  font-size: .78rem; color: var(--text); font-weight: 600;
}
.settings-row-desc {
  font-size: .68rem; color: var(--muted); margin-top: 2px;
}
.settings-toggle {
  position: relative; width: 42px; height: 24px; border-radius: 12px;
  background: var(--line); border: none; cursor: pointer; transition: background .2s;
}
.settings-toggle.on { background: var(--accent); }
.settings-toggle::after {
  content: ''; position: absolute; top: 3px; left: 3px;
  width: 18px; height: 18px; border-radius: 50%; background: #fff;
  transition: transform .2s;
}
.settings-toggle.on::after { transform: translateX(18px); }
.settings-theme-chip {
  display: inline-flex; align-items: center; gap: 4px; padding: 6px 12px;
  border-radius: 8px; border: 2px solid var(--line); background: var(--card-alt);
  font-size: .75rem; font-weight: 700; color: var(--text); cursor: pointer;
  transition: border-color .2s, background .2s;
}
.settings-theme-chip.active {
  border-color: var(--accent); background: var(--accent); color: #fff;
}
.settings-themes-grid {
  display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px;
}
"""

# Find the injection point — right before the closing </style>
last_style_close = html.rfind('</style>')
assert last_style_close != -1, "Cannot find </style>"
html = html[:last_style_close] + NEW_THEMES_CSS + html[last_style_close:]
print("  New theme + settings CSS injected.")


# ============================================================
# STEP 3: Add gym sub-tabs inside #gymView (right after gymView opens)
# ============================================================
print("[3/10] Adding gym sub-tabs for workout/stretches/recovery...")

GYM_SUBTABS_HTML = """    <!-- Gym Unified Sub-Tabs (Consolidation) -->
    <div class="gym-subtabs" id="gymSubTabs">
      <button type="button" class="gym-subtab-btn active" data-gym-tab="workout" id="gymTabWorkout">🏋️ تمارين اليوم</button>
      <button type="button" class="gym-subtab-btn" data-gym-tab="stretches" id="gymTabStretches">🧘 الاستطالات</button>
      <button type="button" class="gym-subtab-btn" data-gym-tab="recovery" id="gymTabRecovery">🩺 الاستشفاء</button>
    </div>
    <!-- Gym Sub-Tab: Stretches (embedded from stretchesView) -->
    <div id="gymSubPaneStretches" class="hidden"></div>
    <!-- Gym Sub-Tab: Recovery (embedded from recoveryView) -->
    <div id="gymSubPaneRecovery" class="hidden"></div>
"""

# Insert right after <div id="gymView" class="hidden">
gym_view_tag = '<div id="gymView" class="hidden">'
gym_view_pos = html.find(gym_view_tag)
assert gym_view_pos != -1, "Cannot find gymView div"
insert_pos = html.find('\n', gym_view_pos) + 1
html = html[:insert_pos] + GYM_SUBTABS_HTML + html[insert_pos:]
print("  Gym sub-tabs HTML injected.")


# ============================================================
# STEP 4: Add Settings View HTML (before </div><!-- app-main -->)
# ============================================================
print("[4/10] Adding #settingsView HTML...")

SETTINGS_VIEW_HTML = """
  <!-- ===== SETTINGS MODE ===== -->
  <div id="settingsView" class="hidden">
    <div class="section-title"><span class="n">⚙️</span> إعدادات زتونة</div>
    <div class="section-hint">خصّص التطبيق على ذوقك — المظهر والألوان والواجهة والبيانات والتنبيهات</div>

    <!-- 1. Appearance & Themes -->
    <div class="settings-section-card">
      <div class="settings-section-title">🎨 المظهر والثيمات</div>

      <div style="margin-bottom:10px;">
        <div class="settings-row-label" style="margin-bottom:6px;">نمط الإضاءة</div>
        <div class="settings-themes-grid" id="settingsLightModeGrid">
          <button type="button" class="settings-theme-chip" data-theme-choice="light" onclick="selectThemeChoice('light')">☀️ فاتح</button>
          <button type="button" class="settings-theme-chip" data-theme-choice="dark" onclick="selectThemeChoice('dark')">🌙 داكن</button>
          <button type="button" class="settings-theme-chip" data-theme-choice="amoled" onclick="selectThemeChoice('amoled')">🖤 AMOLED</button>
        </div>
      </div>

      <div style="margin-bottom:10px;">
        <div class="settings-row-label" style="margin-bottom:6px;">ثيم الألوان</div>
        <div class="settings-themes-grid" id="settingsColorThemeGrid">
          <button type="button" class="settings-theme-chip" data-color-theme="" onclick="selectColorTheme('')">🌿 الافتراضي</button>
          <button type="button" class="settings-theme-chip" data-color-theme="theme-amber" onclick="selectColorTheme('theme-amber')">🏜️ كهرماني</button>
          <button type="button" class="settings-theme-chip" data-color-theme="theme-violet" onclick="selectColorTheme('theme-violet')">🔮 بنفسجي</button>
          <button type="button" class="settings-theme-chip" data-color-theme="theme-crimson" onclick="selectColorTheme('theme-crimson')">🍷 أحمر</button>
          <button type="button" class="settings-theme-chip" data-color-theme="theme-emerald" onclick="selectColorTheme('theme-emerald')">🍃 نعناعي</button>
          <button type="button" class="settings-theme-chip" data-color-theme="theme-titanium" onclick="selectColorTheme('theme-titanium')">⚙️ تيتانيوم</button>
        </div>
      </div>

      <div style="margin-bottom:10px;">
        <div class="settings-row-label" style="margin-bottom:6px;">لون التمييز</div>
        <div class="settings-themes-grid" id="settingsAccentGrid">
          <button type="button" class="settings-theme-chip" data-accent-choice="emerald" style="border-color:#10b981;" onclick="selectAccentChoice('emerald')">🌿 زمردي</button>
          <button type="button" class="settings-theme-chip" data-accent-choice="ocean" style="border-color:#3b82f6;" onclick="selectAccentChoice('ocean')">🌊 أزرق</button>
          <button type="button" class="settings-theme-chip" data-accent-choice="amber" style="border-color:#f59e0b;" onclick="selectAccentChoice('amber')">🌅 كهرماني</button>
          <button type="button" class="settings-theme-chip" data-accent-choice="royal" style="border-color:#8b5cf6;" onclick="selectAccentChoice('royal')">🔮 بنفسجي</button>
        </div>
      </div>

      <div class="settings-row">
        <div>
          <div class="settings-row-label">حجم الخط</div>
          <div class="settings-row-desc">عادي (100%) أو كبير مريح (112%)</div>
        </div>
        <button type="button" class="settings-toggle" id="settingsFontToggle" onclick="toggleSettingsFont()"></button>
      </div>

      <div class="settings-row">
        <div>
          <div class="settings-row-label">الوضع المضغوط</div>
          <div class="settings-row-desc">تقليل المسافات لعرض أكثر في شاشة أصغر</div>
        </div>
        <button type="button" class="settings-toggle" id="settingsCompactToggle" onclick="toggleSettingsCompact()"></button>
      </div>

      <div class="settings-row">
        <div>
          <div class="settings-row-label">الانضغاط الفائق</div>
          <div class="settings-row-desc">أقصى كثافة ممكنة — للشاشات الصغيرة جدًا</div>
        </div>
        <button type="button" class="settings-toggle" id="settingsUltraCompactToggle" onclick="toggleSettingsUltraCompact()"></button>
      </div>
    </div>

    <!-- 2. Feature Toggles -->
    <div class="settings-section-card">
      <div class="settings-section-title">📱 إخفاء / إظهار الأقسام</div>
      <div class="section-hint" style="margin-bottom:8px;">أخفِ أي قسم مش محتاجه — هيختفي من القائمة والشاشة الرئيسية</div>
      <div id="settingsFeatureToggles"></div>
    </div>

    <!-- 3. Data & Backup -->
    <div class="settings-section-card">
      <div class="settings-section-title">🛡️ البيانات والنسخ الاحتياطي</div>
      <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:6px;">
        <button type="button" class="day-chip" onclick="if(typeof exportData==='function')exportData()">📤 تصدير البيانات</button>
        <button type="button" class="day-chip" onclick="document.getElementById('importFileInput')?.click()">📥 استيراد البيانات</button>
        <button type="button" class="day-chip" onclick="if(typeof openEncryptedBackup==='function')openEncryptedBackup()">🔐 نسخة مشفرة</button>
      </div>
      <div class="settings-row" style="margin-top:10px;">
        <div>
          <div class="settings-row-label">تذكير النسخ الاحتياطي</div>
          <div class="settings-row-desc">تنبيه دوري لعمل نسخة احتياطية</div>
        </div>
        <select id="settingsBackupInterval" class="str-filter-dropdown" style="max-width:120px;" onchange="saveBackupInterval(this.value)">
          <option value="off">مغلق</option>
          <option value="3">كل ٣ أيام</option>
          <option value="7">كل أسبوع</option>
          <option value="14">كل أسبوعين</option>
          <option value="30">كل شهر</option>
        </select>
      </div>
    </div>

    <!-- 4. Prayer & Alarms -->
    <div class="settings-section-card">
      <div class="settings-section-title">⏰ التنبيهات ومواقيت الصلاة</div>
      <div class="settings-row">
        <div>
          <div class="settings-row-label">مدينة الصلاة</div>
          <div class="settings-row-desc">لحساب مواقيت الصلاة والأذان</div>
        </div>
        <select id="settingsPrayerCity" class="str-filter-dropdown" style="max-width:140px;" onchange="savePrayerCitySetting(this.value)">
          <option value="cairo">القاهرة</option>
          <option value="alexandria">الإسكندرية</option>
          <option value="minya">المنيا</option>
        </select>
      </div>
    </div>

    <!-- About -->
    <div class="settings-section-card" style="text-align:center; color:var(--muted); font-size:.72rem;">
      🌿 زتونة — رفيقك اليومي<br>
      تطبيق تخطيط شخصي • بياناتك على جهازك فقط<br>
      <span id="settingsVersionLabel"></span>
    </div>
  </div>

"""

# Find stretchesView end (</div> at line 8078 area), then studyView, then insert settingsView after studyView
# Better: find the comment "<!-- ===== STRETCH & MOBILITY" and the entire stretchesView block
# Insert settingsView right before the first modal or before </div><!-- app-main -->
# Let's find the end of studyView and insert after it
study_view_start = html.find('id="studyView"')
assert study_view_start != -1, "Cannot find studyView"
# Find the next top-level view/comment/modal after studyView
# Look for the pattern <!-- Phase or <!-- ==== or <div class="...modal
# The studyView ends where the next major section begins.
# From our research, after studyView there are modals. Let's find the first modal or major div after studyView.
# Actually we know the structure: studyView is followed by modals. Let's find the closing tag count.

# Simpler approach: find the next <!-- that starts a new major block after studyView
# From the research, stretchesView ends at line ~8078, studyView starts at ~8081
# Let's find end of studyView by searching for the next major comment after studyView start

# Find all "<!-- =====" markers
major_comments = [(m.start(), m.group()) for m in re.finditer(r'<!-- ={3,}', html)]
study_comment_idx = None
for idx, (pos, txt) in enumerate(major_comments):
    if pos > study_view_start:
        # This is the next major section after studyView
        settings_insert_pos = pos
        break

html = html[:settings_insert_pos] + SETTINGS_VIEW_HTML + html[settings_insert_pos:]
print("  Settings view HTML injected.")


# ============================================================
# STEP 5: Update navigation — Drawer, Sidebar, ModesBar
# ============================================================
print("[5/10] Reorganizing navigation order and adding Settings...")

# --- 5a: Update Drawer Nav ---
# New order: home, prayer, gym, meal, sleep, schedule, study, budget, notes, overview, search, settings
# Remove recovery & stretches entries, add settings, reorder

# Old drawer nav entries (from research):
# home, meal, gym, sleep, prayer, schedule, recovery, overview, search, budget, notes, stretches, study

OLD_DRAWER_NAV = '''    <button type="button" class="drawer-nav-btn active" data-nav="home" id="drawNav-home">
      <span class="dnb-icon" aria-hidden="true">🏠</span>
      <div class="dnb-text">
        <span class="dnb-label">الرئيسية</span>
        <span class="dnb-desc">لوحة التحكم والملخص</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="meal" id="drawNav-meal">
      <span class="dnb-icon" aria-hidden="true">🍽️</span>
      <div class="dnb-text">
        <span class="dnb-label">الأكل</span>
        <span class="dnb-desc">الخطة الغذائية والتسوق</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="gym" id="drawNav-gym">
      <span class="dnb-icon" aria-hidden="true">🏋️</span>
      <div class="dnb-text">
        <span class="dnb-label">الجيم</span>
        <span class="dnb-desc">تمارينك وسجل الأوزان</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="sleep" id="drawNav-sleep">
      <span class="dnb-icon" aria-hidden="true">😴</span>
      <div class="dnb-text">
        <span class="dnb-label">النوم</span>
        <span class="dnb-desc">مواعيد نومك وعاداتك</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="prayer" id="drawNav-prayer">
      <span class="dnb-icon" aria-hidden="true">🕌</span>
      <div class="dnb-text">
        <span class="dnb-label">الصلاة</span>
        <span class="dnb-desc">الفروض والسنن والقرآن</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="schedule" id="drawNav-schedule">
      <span class="dnb-icon" aria-hidden="true">📅</span>
      <div class="dnb-text">
        <span class="dnb-label">الجدول</span>
        <span class="dnb-desc">جدولك اليومي والمواعيد</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="recovery" id="drawNav-recovery">
      <span class="dnb-icon" aria-hidden="true">🩺</span>
      <div class="dnb-text">
        <span class="dnb-label">الاستشفاء</span>
        <span class="dnb-desc">مؤشرات التعب والجاهزية</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="overview" id="drawNav-overview">
      <span class="dnb-icon" aria-hidden="true">📊</span>
      <div class="dnb-text">
        <span class="dnb-label">نظرة عامة</span>
        <span class="dnb-desc">التحليلات والاتجاهات</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="search" id="drawNav-search">
      <span class="dnb-icon" aria-hidden="true">🔍</span>
      <div class="dnb-text">
        <span class="dnb-label">بحث</span>
        <span class="dnb-desc">البحث في السجلات القديمة</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="budget" id="drawNav-budget">
      <span class="dnb-icon" aria-hidden="true">💰</span>
      <div class="dnb-text">
        <span class="dnb-label">الميزانية</span>
        <span class="dnb-desc">المصروفات الشهرية والميزانية</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="notes" id="drawNav-notes">
      <span class="dnb-icon" aria-hidden="true">📝</span>
      <div class="dnb-text">
        <span class="dnb-label">الملاحظات</span>
        <span class="dnb-desc">دفتر الملاحظات الموحد والمرفقات</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="stretches" id="drawNav-stretches">
      <span class="dnb-icon" aria-hidden="true">🧘</span>
      <div class="dnb-text">
        <span class="dnb-label">الاستطالات والمرونة</span>
        <span class="dnb-desc">موسوعة حركات الإطالة والتحضير</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="study" id="drawNav-study">
      <span class="dnb-icon" aria-hidden="true">📚</span>
      <div class="dnb-text">
        <span class="dnb-label">المذاكرة والتعلم الذاتي</span>
        <span class="dnb-desc">المؤقت والبطاقات وتكرار المذاكرة</span>
      </div>
    </button>'''

NEW_DRAWER_NAV = '''    <button type="button" class="drawer-nav-btn active" data-nav="home" id="drawNav-home">
      <span class="dnb-icon" aria-hidden="true">🏠</span>
      <div class="dnb-text">
        <span class="dnb-label">الرئيسية</span>
        <span class="dnb-desc">لوحة التحكم والملخص</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="prayer" id="drawNav-prayer">
      <span class="dnb-icon" aria-hidden="true">🕌</span>
      <div class="dnb-text">
        <span class="dnb-label">الصلاة</span>
        <span class="dnb-desc">الفروض والسنن والقرآن</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="gym" id="drawNav-gym">
      <span class="dnb-icon" aria-hidden="true">🏋️</span>
      <div class="dnb-text">
        <span class="dnb-label">الجيم والاستشفاء</span>
        <span class="dnb-desc">التمارين والاستطالات والاستشفاء</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="meal" id="drawNav-meal">
      <span class="dnb-icon" aria-hidden="true">🍽️</span>
      <div class="dnb-text">
        <span class="dnb-label">التغذية</span>
        <span class="dnb-desc">الخطة الغذائية والتسوق</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="sleep" id="drawNav-sleep">
      <span class="dnb-icon" aria-hidden="true">😴</span>
      <div class="dnb-text">
        <span class="dnb-label">النوم</span>
        <span class="dnb-desc">مواعيد نومك وعاداتك</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="schedule" id="drawNav-schedule">
      <span class="dnb-icon" aria-hidden="true">📅</span>
      <div class="dnb-text">
        <span class="dnb-label">الجدول</span>
        <span class="dnb-desc">جدولك اليومي والمواعيد</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="study" id="drawNav-study">
      <span class="dnb-icon" aria-hidden="true">📚</span>
      <div class="dnb-text">
        <span class="dnb-label">المذاكرة</span>
        <span class="dnb-desc">المؤقت والبطاقات والتكرار</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="budget" id="drawNav-budget">
      <span class="dnb-icon" aria-hidden="true">💰</span>
      <div class="dnb-text">
        <span class="dnb-label">الميزانية</span>
        <span class="dnb-desc">المصروفات الشهرية والميزانية</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="overview" id="drawNav-overview">
      <span class="dnb-icon" aria-hidden="true">📊</span>
      <div class="dnb-text">
        <span class="dnb-label">نظرة عامة</span>
        <span class="dnb-desc">التحليلات والاتجاهات</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="notes" id="drawNav-notes">
      <span class="dnb-icon" aria-hidden="true">📝</span>
      <div class="dnb-text">
        <span class="dnb-label">الملاحظات</span>
        <span class="dnb-desc">دفتر الملاحظات الموحد</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="search" id="drawNav-search">
      <span class="dnb-icon" aria-hidden="true">🔍</span>
      <div class="dnb-text">
        <span class="dnb-label">بحث</span>
        <span class="dnb-desc">البحث في السجلات القديمة</span>
      </div>
    </button>
    <button type="button" class="drawer-nav-btn" data-nav="settings" id="drawNav-settings">
      <span class="dnb-icon" aria-hidden="true">⚙️</span>
      <div class="dnb-text">
        <span class="dnb-label">الإعدادات</span>
        <span class="dnb-desc">المظهر والبيانات والتفضيلات</span>
      </div>
    </button>'''

assert OLD_DRAWER_NAV in html, "Cannot find old drawer nav block"
html = html.replace(OLD_DRAWER_NAV, NEW_DRAWER_NAV)
print("  Drawer nav reorganized.")

# --- 5b: Update Sidebar Nav ---
OLD_SIDEBAR_NAV = '''      <button type="button" class="sidebar-nav-btn active" data-nav="home" id="sideNav-home" title="الرئيسية">
        <span class="snb-icon" aria-hidden="true">🏠</span>
        <div class="snb-text">
          <span class="snb-label">الرئيسية</span>
          <span class="snb-desc">لوحة التحكم والملخص</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="meal" id="sideNav-meal" title="الأكل">
        <span class="snb-icon" aria-hidden="true">🍽️</span>
        <div class="snb-text">
          <span class="snb-label">الأكل</span>
          <span class="snb-desc">الخطة الغذائية والتسوق</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="gym" id="sideNav-gym" title="الجيم">
        <span class="snb-icon" aria-hidden="true">🏋️</span>
        <div class="snb-text">
          <span class="snb-label">الجيم</span>
          <span class="snb-desc">تمارينك وسجل الأوزان</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="sleep" id="sideNav-sleep" title="النوم">
        <span class="snb-icon" aria-hidden="true">😴</span>
        <div class="snb-text">
          <span class="snb-label">النوم</span>
          <span class="snb-desc">مواعيد نومك وعاداتك</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="prayer" id="sideNav-prayer" title="الصلاة">
        <span class="snb-icon" aria-hidden="true">🕌</span>
        <div class="snb-text">
          <span class="snb-label">الصلاة</span>
          <span class="snb-desc">الفروض والسنن والقرآن</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="schedule" id="sideNav-schedule" title="الجدول">
        <span class="snb-icon" aria-hidden="true">📅</span>
        <div class="snb-text">
          <span class="snb-label">الجدول</span>
          <span class="snb-desc">جدولك اليومي والمواعيد</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="recovery" id="sideNav-recovery" title="الاستشفاء">
        <span class="snb-icon" aria-hidden="true">🩺</span>
        <div class="snb-text">
          <span class="snb-label">الاستشفاء</span>
          <span class="snb-desc">مؤشرات التعب والجاهزية</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="overview" id="sideNav-overview" title="نظرة عامة">
        <span class="snb-icon" aria-hidden="true">📊</span>
        <div class="snb-text">
          <span class="snb-label">نظرة عامة</span>
          <span class="snb-desc">التحليلات والاتجاهات</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="search" id="sideNav-search" title="بحث">
        <span class="snb-icon" aria-hidden="true">🔍</span>
        <div class="snb-text">
          <span class="snb-label">بحث</span>
          <span class="snb-desc">البحث في السجلات القديمة</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="budget" id="sideNav-budget" title="الميزانية">
        <span class="snb-icon" aria-hidden="true">💰</span>
        <div class="snb-text">
          <span class="snb-label">الميزانية</span>
          <span class="snb-desc">المصروفات الشهرية والميزانية</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="notes" id="sideNav-notes" title="الملاحظات">
        <span class="snb-icon" aria-hidden="true">📝</span>
        <div class="snb-text">
          <span class="snb-label">الملاحظات</span>
          <span class="snb-desc">دفتر الملاحظات الموحد</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="stretches" id="sideNav-stretches" title="الاستطالات">
        <span class="snb-icon" aria-hidden="true">🧘</span>
        <div class="snb-text">
          <span class="snb-label">الاستطالات</span>
          <span class="snb-desc">موسوعة الحركات والمرونة</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="study" id="sideNav-study" title="المذاكرة والتعلم">
        <span class="snb-icon" aria-hidden="true">📚</span>
        <div class="snb-text">
          <span class="snb-label">المذاكرة والتعلم</span>
          <span class="snb-desc">المؤقت والبطاقات والامتحانات</span>
        </div>
      </button>'''

NEW_SIDEBAR_NAV = '''      <button type="button" class="sidebar-nav-btn active" data-nav="home" id="sideNav-home" title="الرئيسية">
        <span class="snb-icon" aria-hidden="true">🏠</span>
        <div class="snb-text">
          <span class="snb-label">الرئيسية</span>
          <span class="snb-desc">لوحة التحكم والملخص</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="prayer" id="sideNav-prayer" title="الصلاة">
        <span class="snb-icon" aria-hidden="true">🕌</span>
        <div class="snb-text">
          <span class="snb-label">الصلاة</span>
          <span class="snb-desc">الفروض والسنن والقرآن</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="gym" id="sideNav-gym" title="الجيم والاستشفاء">
        <span class="snb-icon" aria-hidden="true">🏋️</span>
        <div class="snb-text">
          <span class="snb-label">الجيم والاستشفاء</span>
          <span class="snb-desc">التمارين والاستطالات والاستشفاء</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="meal" id="sideNav-meal" title="التغذية">
        <span class="snb-icon" aria-hidden="true">🍽️</span>
        <div class="snb-text">
          <span class="snb-label">التغذية</span>
          <span class="snb-desc">الخطة الغذائية والتسوق</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="sleep" id="sideNav-sleep" title="النوم">
        <span class="snb-icon" aria-hidden="true">😴</span>
        <div class="snb-text">
          <span class="snb-label">النوم</span>
          <span class="snb-desc">مواعيد نومك وعاداتك</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="schedule" id="sideNav-schedule" title="الجدول">
        <span class="snb-icon" aria-hidden="true">📅</span>
        <div class="snb-text">
          <span class="snb-label">الجدول</span>
          <span class="snb-desc">جدولك اليومي والمواعيد</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="study" id="sideNav-study" title="المذاكرة">
        <span class="snb-icon" aria-hidden="true">📚</span>
        <div class="snb-text">
          <span class="snb-label">المذاكرة</span>
          <span class="snb-desc">المؤقت والبطاقات والتكرار</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="budget" id="sideNav-budget" title="الميزانية">
        <span class="snb-icon" aria-hidden="true">💰</span>
        <div class="snb-text">
          <span class="snb-label">الميزانية</span>
          <span class="snb-desc">المصروفات الشهرية</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="overview" id="sideNav-overview" title="نظرة عامة">
        <span class="snb-icon" aria-hidden="true">📊</span>
        <div class="snb-text">
          <span class="snb-label">نظرة عامة</span>
          <span class="snb-desc">التحليلات والاتجاهات</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="notes" id="sideNav-notes" title="الملاحظات">
        <span class="snb-icon" aria-hidden="true">📝</span>
        <div class="snb-text">
          <span class="snb-label">الملاحظات</span>
          <span class="snb-desc">دفتر الملاحظات الموحد</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="search" id="sideNav-search" title="بحث">
        <span class="snb-icon" aria-hidden="true">🔍</span>
        <div class="snb-text">
          <span class="snb-label">بحث</span>
          <span class="snb-desc">البحث في السجلات</span>
        </div>
      </button>
      <button type="button" class="sidebar-nav-btn" data-nav="settings" id="sideNav-settings" title="الإعدادات">
        <span class="snb-icon" aria-hidden="true">⚙️</span>
        <div class="snb-text">
          <span class="snb-label">الإعدادات</span>
          <span class="snb-desc">المظهر والبيانات</span>
        </div>
      </button>'''

assert OLD_SIDEBAR_NAV in html, "Cannot find old sidebar nav block"
html = html.replace(OLD_SIDEBAR_NAV, NEW_SIDEBAR_NAV)
print("  Sidebar nav reorganized.")


# ============================================================
# STEP 6: Update ModesBar (home grid) — reorder + remove recovery/stretches + add settings
# ============================================================
print("[6/10] Updating home modesBar grid...")

OLD_MODES_BAR_CONTENT = '''    <div class="mode-btn active" id="modeMeal" role="button" tabindex="0" aria-label="الأكل"><span class="mb-ico">🍽️</span><span class="mb-label">الأكل</span><span class="mb-desc">خطتك الغذائية والتسوق والمياه</span></div>
    <div class="mode-btn" id="modeGym" role="button" tabindex="0" aria-label="الجيم"><span class="mb-ico">🏋️</span><span class="mb-label">الجيم</span><span class="mb-desc">تمارينك وتتبع تقدّمك في الأوزان</span></div>
    <div class="mode-btn" id="modeSleep" role="button" tabindex="0" aria-label="النوم"><span class="mb-ico">😴</span><span class="mb-label">النوم</span><span class="mb-desc">مواعيد نومك وعاداتك الصحية</span></div>
    <div class="mode-btn" id="modePrayer" role="button" tabindex="0" aria-label="الصلاة"><span class="mb-ico">🕌</span><span class="mb-label">الصلاة</span><span class="mb-desc">الفروض والسنن والقرآن اليومي</span></div>
    <div class="mode-btn" id="modeSchedule" role="button" tabindex="0" aria-label="الجدول"><span class="mb-ico">📅</span><span class="mb-label">الجدول</span><span class="mb-desc">جدولك اليومي الكامل ووقتك المتاح</span></div>
    <div class="mode-btn" id="modeRecovery" role="button" tabindex="0" aria-label="الاستشفاء"><span class="mb-ico">🩺</span><span class="mb-label">الاستشفاء</span><span class="mb-desc">حالتك اليومية قبل ما تكمل على الخطة</span></div>
    <div class="mode-btn" id="modeOverview" role="button" tabindex="0" aria-label="نظرة عامة"><span class="mb-ico">📊</span><span class="mb-label">نظرة عامة</span><span class="mb-desc">تحليلاتك واتجاهاتك بمرور الوقت</span></div>
    <div class="mode-btn" id="modeSearch" role="button" tabindex="0" aria-label="بحث"><span class="mb-ico">🔍</span><span class="mb-label">بحث</span><span class="mb-desc">دوّر في يومياتك القديمة كلها</span></div>
    <div class="mode-btn" id="modeBudget" role="button" tabindex="0" aria-label="الميزانية"><span class="mb-ico">💰</span><span class="mb-label">الميزانية</span><span class="mb-desc">مصروفاتك الشهرية وميزانيتك</span></div>
    <div class="mode-btn" id="modeNotes" role="button" tabindex="0" aria-label="الملاحظات"><span class="mb-ico">📝</span><span class="mb-label">الملاحظات</span><span class="mb-desc">دفتر الملاحظات الموحد والمرفقات</span></div>
    <div class="mode-btn" id="modeStretches" role="button" tabindex="0" aria-label="الاستطالات"><span class="mb-ico">🧘</span><span class="mb-label">الاستطالات</span><span class="mb-desc">موسوعة حركات الإطالة والمرونة</span></div>
    <div class="mode-btn" id="modeStudy" role="button" tabindex="0" aria-label="المذاكرة"><span class="mb-ico">📚</span><span class="mb-label">المذاكرة</span><span class="mb-desc">المؤقت والبطاقات والمراجعات</span></div>'''

NEW_MODES_BAR_CONTENT = '''    <div class="mode-btn" id="modePrayer" role="button" tabindex="0" aria-label="الصلاة"><span class="mb-ico">🕌</span><span class="mb-label">الصلاة</span><span class="mb-desc">الفروض والسنن والقرآن اليومي</span></div>
    <div class="mode-btn" id="modeGym" role="button" tabindex="0" aria-label="الجيم"><span class="mb-ico">🏋️</span><span class="mb-label">الجيم والاستشفاء</span><span class="mb-desc">التمارين والاستطالات والاستشفاء</span></div>
    <div class="mode-btn active" id="modeMeal" role="button" tabindex="0" aria-label="التغذية"><span class="mb-ico">🍽️</span><span class="mb-label">التغذية</span><span class="mb-desc">خطتك الغذائية والتسوق والمياه</span></div>
    <div class="mode-btn" id="modeSleep" role="button" tabindex="0" aria-label="النوم"><span class="mb-ico">😴</span><span class="mb-label">النوم</span><span class="mb-desc">مواعيد نومك وعاداتك الصحية</span></div>
    <div class="mode-btn" id="modeSchedule" role="button" tabindex="0" aria-label="الجدول"><span class="mb-ico">📅</span><span class="mb-label">الجدول</span><span class="mb-desc">جدولك اليومي الكامل ووقتك المتاح</span></div>
    <div class="mode-btn" id="modeStudy" role="button" tabindex="0" aria-label="المذاكرة"><span class="mb-ico">📚</span><span class="mb-label">المذاكرة</span><span class="mb-desc">المؤقت والبطاقات والمراجعات</span></div>
    <div class="mode-btn" id="modeBudget" role="button" tabindex="0" aria-label="الميزانية"><span class="mb-ico">💰</span><span class="mb-label">الميزانية</span><span class="mb-desc">مصروفاتك الشهرية وميزانيتك</span></div>
    <div class="mode-btn" id="modeOverview" role="button" tabindex="0" aria-label="نظرة عامة"><span class="mb-ico">📊</span><span class="mb-label">نظرة عامة</span><span class="mb-desc">تحليلاتك واتجاهاتك بمرور الوقت</span></div>
    <div class="mode-btn" id="modeNotes" role="button" tabindex="0" aria-label="الملاحظات"><span class="mb-ico">📝</span><span class="mb-label">الملاحظات</span><span class="mb-desc">دفتر الملاحظات الموحد والمرفقات</span></div>
    <div class="mode-btn" id="modeSearch" role="button" tabindex="0" aria-label="بحث"><span class="mb-ico">🔍</span><span class="mb-label">بحث</span><span class="mb-desc">دوّر في يومياتك القديمة كلها</span></div>
    <div class="mode-btn" id="modeSettings" role="button" tabindex="0" aria-label="الإعدادات"><span class="mb-ico">⚙️</span><span class="mb-label">الإعدادات</span><span class="mb-desc">المظهر والبيانات والتفضيلات</span></div>'''

assert OLD_MODES_BAR_CONTENT in html, "Cannot find old modesBar content"
html = html.replace(OLD_MODES_BAR_CONTENT, NEW_MODES_BAR_CONTENT)
print("  ModesBar grid reorganized.")


# ============================================================
# STEP 7: Update applyMode() — add settings view, keep recovery/stretches for compatibility but redirect
# ============================================================
print("[7/10] Updating applyMode(), navigateTo(), NAV_MODES...")

# 7a: Update NAV_MODES
OLD_NAV_MODES = "const NAV_MODES = ['home','meal','gym','sleep','prayer','schedule','recovery','overview','search','budget','notes','stretches','study'];"
NEW_NAV_MODES = "const NAV_MODES = ['home','meal','gym','sleep','prayer','schedule','recovery','overview','search','budget','notes','stretches','study','settings'];"
assert OLD_NAV_MODES in html, "Cannot find NAV_MODES"
html = html.replace(OLD_NAV_MODES, NEW_NAV_MODES)

# 7b: Update applyMode views map — add settings
OLD_VIEWS_MAP = """    study: document.getElementById('studyView'),
  };"""
NEW_VIEWS_MAP = """    study: document.getElementById('studyView'),
    settings: document.getElementById('settingsView'),
  };"""
assert OLD_VIEWS_MAP in html, "Cannot find views map end"
html = html.replace(OLD_VIEWS_MAP, NEW_VIEWS_MAP)

# 7c: Update applyMode btns map — add settings (keep recovery/stretches for compat)
OLD_BTNS_MAP = """    study: document.getElementById('modeStudy'),
  };"""
NEW_BTNS_MAP = """    study: document.getElementById('modeStudy'),
    settings: document.getElementById('modeSettings'),
  };"""
assert OLD_BTNS_MAP in html, "Cannot find btns map end"
html = html.replace(OLD_BTNS_MAP, NEW_BTNS_MAP)

# 7d: Update applyMode titles map — add settings
OLD_TITLES_STUDY = "    study: ['📚 ركن المذاكرة والتعلم الذاتي', 'مؤقتات بومودورو للتركيز، البطاقات والتكرار المتباعد، تقنية فاينمان والملاحظات المنظمة'],"
NEW_TITLES_WITH_SETTINGS = """    study: ['📚 ركن المذاكرة والتعلم الذاتي', 'مؤقتات بومودورو للتركيز، البطاقات والتكرار المتباعد، تقنية فاينمان والملاحظات المنظمة'],
    settings: ['⚙️ إعدادات زتونة', 'المظهر والألوان والواجهة والبيانات والتنبيهات — خصّص التطبيق على ذوقك'],"""
assert OLD_TITLES_STUDY in html, "Cannot find study title in applyMode"
html = html.replace(OLD_TITLES_STUDY, NEW_TITLES_WITH_SETTINGS)

# 7e: Update the week cal hidden modes to include settings
OLD_WEEKCAL_HIDE = "if(mode==='budget' || mode==='notes' || mode==='stretches' || mode==='study' || isHome){"
NEW_WEEKCAL_HIDE = "if(mode==='budget' || mode==='notes' || mode==='stretches' || mode==='study' || mode==='settings' || isHome){"
assert OLD_WEEKCAL_HIDE in html, "Cannot find weekcal hide condition"
html = html.replace(OLD_WEEKCAL_HIDE, NEW_WEEKCAL_HIDE)

# 7f: Add settings render call in applyMode
OLD_STUDY_RENDER = "  if(mode==='study') renderStudyView();"
NEW_STUDY_SETTINGS_RENDER = """  if(mode==='study') renderStudyView();
  if(mode==='settings') renderSettingsView();"""
assert OLD_STUDY_RENDER in html, "Cannot find study render in applyMode"
html = html.replace(OLD_STUDY_RENDER, NEW_STUDY_SETTINGS_RENDER)

# 7g: Update navigateTo to handle recovery/stretches redirect to gym sub-tabs
OLD_NAVIGATE_TO = """function navigateTo(newMode, opts){
  opts = opts || {};
  mode = NAV_MODES.includes(newMode) ? newMode : 'home';
  applyMode();"""

NEW_NAVIGATE_TO = """function navigateTo(newMode, opts){
  opts = opts || {};
  // Consolidation: redirect recovery/stretches to gym sub-tabs
  if(newMode === 'recovery'){
    newMode = 'gym';
    window._gymSubTabTarget = 'recovery';
  } else if(newMode === 'stretches'){
    newMode = 'gym';
    window._gymSubTabTarget = 'stretches';
  }
  mode = NAV_MODES.includes(newMode) ? newMode : 'home';
  applyMode();"""

assert OLD_NAVIGATE_TO in html, "Cannot find old navigateTo"
html = html.replace(OLD_NAVIGATE_TO, NEW_NAVIGATE_TO)

print("  applyMode/navigateTo/NAV_MODES updated.")


# ============================================================
# STEP 8: Inject Settings + Gym Sub-Tab + Feature Toggle + Color Theme JS engine
# ============================================================
print("[8/10] Injecting JavaScript engine for settings, gym sub-tabs, feature toggles, themes...")

SETTINGS_JS_ENGINE = """
/* ============================================================
   CONSOLIDATION: Settings View, Gym Sub-Tabs, Feature Toggles, Color Themes
   ============================================================ */

/* --- Color Theme Selection --- */
function selectColorTheme(themeClass){
  const THEMES = ['theme-amber','theme-violet','theme-crimson','theme-emerald','theme-titanium'];
  THEMES.forEach(t => document.body.classList.remove(t));
  if(themeClass) document.body.classList.add(themeClass);
  localStorage.setItem('zatoona-color-theme', themeClass || '');
  syncSettingsUI();
}
function loadColorTheme(){
  const saved = localStorage.getItem('zatoona-color-theme');
  if(saved){
    document.body.classList.add(saved);
  }
}

/* --- Ultra-Compact Toggle --- */
function toggleUltraCompact(on){
  if(typeof on === 'undefined') on = !document.body.classList.contains('ultra-compact');
  document.body.classList.toggle('ultra-compact', on);
  localStorage.setItem('zatoona-ultra-compact', on ? '1' : '0');
  syncSettingsUI();
}
function loadUltraCompact(){
  if(localStorage.getItem('zatoona-ultra-compact') === '1'){
    document.body.classList.add('ultra-compact');
  }
}

/* --- Feature Toggles --- */
const FEATURE_TOGGLE_MODULES = [
  {key:'study', label:'📚 المذاكرة والتعلم', default:true},
  {key:'budget', label:'💰 الميزانية المالية', default:true},
  {key:'notes', label:'📝 الملاحظات', default:true},
  {key:'search', label:'🔍 البحث', default:true},
  {key:'overview', label:'📊 نظرة عامة', default:true},
];
function getFeatureToggles(){
  try {
    const raw = localStorage.getItem('zatoona-feature-toggles-v1');
    if(raw) return JSON.parse(raw);
  } catch(e){}
  const defaults = {};
  FEATURE_TOGGLE_MODULES.forEach(m => defaults[m.key] = m.default);
  return defaults;
}
function saveFeatureToggles(toggles){
  localStorage.setItem('zatoona-feature-toggles-v1', JSON.stringify(toggles));
}
function toggleFeature(key){
  const toggles = getFeatureToggles();
  toggles[key] = !toggles[key];
  saveFeatureToggles(toggles);
  applyFeatureToggles();
  renderSettingsView();
}
function applyFeatureToggles(){
  const toggles = getFeatureToggles();
  FEATURE_TOGGLE_MODULES.forEach(m => {
    const isVisible = toggles[m.key] !== false;
    // Hide/show in all nav locations
    ['drawNav-','sideNav-','mode'].forEach(prefix => {
      const navId = prefix === 'mode' ? 'mode' + m.key.charAt(0).toUpperCase() + m.key.slice(1) : prefix + m.key;
      const el = document.getElementById(navId);
      if(el) el.style.display = isVisible ? '' : 'none';
    });
  });
}

/* --- Backup interval --- */
function saveBackupInterval(val){
  localStorage.setItem('zatoona-backup-interval', val);
}

/* --- Prayer city setting --- */
function savePrayerCitySetting(val){
  localStorage.setItem('zatoona-prayer-city-setting', val);
}

/* --- Settings toggle helpers --- */
function toggleSettingsFont(){
  const isLarge = document.body.classList.contains('font-large');
  if(typeof selectFontChoice === 'function') selectFontChoice(isLarge ? 'normal' : 'large');
  syncSettingsUI();
}
function toggleSettingsCompact(){
  if(typeof toggleCompactFromModal === 'function') toggleCompactFromModal();
  syncSettingsUI();
}
function toggleSettingsUltraCompact(){
  toggleUltraCompact();
}

function syncSettingsUI(){
  // Sync light mode chips
  const lightMode = document.body.classList.contains('amoled-mode') ? 'amoled' :
                    document.body.classList.contains('dark-mode') ? 'dark' : 'light';
  document.querySelectorAll('#settingsLightModeGrid .settings-theme-chip').forEach(chip => {
    chip.classList.toggle('active', chip.dataset.themeChoice === lightMode);
  });
  // Sync color theme chips
  const colorTheme = localStorage.getItem('zatoona-color-theme') || '';
  document.querySelectorAll('#settingsColorThemeGrid .settings-theme-chip').forEach(chip => {
    chip.classList.toggle('active', chip.dataset.colorTheme === colorTheme);
  });
  // Sync accent chips
  const accent = localStorage.getItem('zatoona-accent') || 'emerald';
  document.querySelectorAll('#settingsAccentGrid .settings-theme-chip').forEach(chip => {
    chip.classList.toggle('active', chip.dataset.accentChoice === accent);
  });
  // Sync toggles
  const fontToggle = document.getElementById('settingsFontToggle');
  if(fontToggle) fontToggle.classList.toggle('on', document.body.classList.contains('font-large'));
  const compactToggle = document.getElementById('settingsCompactToggle');
  if(compactToggle) compactToggle.classList.toggle('on', document.body.classList.contains('compact-density'));
  const ultraToggle = document.getElementById('settingsUltraCompactToggle');
  if(ultraToggle) ultraToggle.classList.toggle('on', document.body.classList.contains('ultra-compact'));

  // Also sync the theme modal chips (keep old modal in sync)
  document.querySelectorAll('.tms-option-btn[data-theme-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.themeChoice === lightMode);
  });
  document.querySelectorAll('.tms-option-btn[data-accent-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.accentChoice === accent);
  });
}

/* --- Render Settings View --- */
function renderSettingsView(){
  syncSettingsUI();
  // Render feature toggles
  const container = document.getElementById('settingsFeatureToggles');
  if(!container) return;
  const toggles = getFeatureToggles();
  container.innerHTML = FEATURE_TOGGLE_MODULES.map(m => `
    <div class="settings-row">
      <div>
        <div class="settings-row-label">${m.label}</div>
      </div>
      <button type="button" class="settings-toggle ${toggles[m.key] !== false ? 'on' : ''}"
              onclick="toggleFeature('${m.key}')"></button>
    </div>
  `).join('');

  // Sync backup interval
  const backupSel = document.getElementById('settingsBackupInterval');
  if(backupSel) backupSel.value = localStorage.getItem('zatoona-backup-interval') || 'off';

  // Sync prayer city
  const citySel = document.getElementById('settingsPrayerCity');
  if(citySel) citySel.value = localStorage.getItem('zatoona-prayer-city-setting') || localStorage.getItem('zatoona-prayer-city') || 'cairo';

  // Version label
  const vLabel = document.getElementById('settingsVersionLabel');
  if(vLabel) vLabel.textContent = 'الإصدار ٢.٠ — ' + new Date().toLocaleDateString('ar-EG');
}

/* --- Gym Sub-Tabs Engine --- */
function switchGymSubTab(tabKey){
  const allPanes = {
    workout: document.getElementById('gymWorkoutBlock'),
    stretches: document.getElementById('gymSubPaneStretches'),
    recovery: document.getElementById('gymSubPaneRecovery'),
  };
  const gymContent = document.getElementById('gymView');
  if(!gymContent) return;

  // If switching to stretches, clone stretchesView content into gymSubPaneStretches if empty
  if(tabKey === 'stretches'){
    const pane = allPanes.stretches;
    if(pane && pane.innerHTML.trim() === ''){
      const src = document.getElementById('stretchesView');
      if(src) pane.innerHTML = src.innerHTML;
    }
    if(typeof renderStretchesView === 'function'){
      // Re-render within the pane context
      setTimeout(() => renderStretchesView(), 50);
    }
  }

  // If switching to recovery, clone recoveryView content into gymSubPaneRecovery if empty
  if(tabKey === 'recovery'){
    const pane = allPanes.recovery;
    if(pane && pane.innerHTML.trim() === ''){
      const src = document.getElementById('recoveryView');
      if(src) pane.innerHTML = src.innerHTML;
    }
    if(typeof renderRecovery === 'function'){
      setTimeout(() => { renderRecovery(); renderRecoveryStatus(); }, 50);
    }
  }

  // Toggle visibility
  Object.keys(allPanes).forEach(k => {
    const el = allPanes[k];
    if(el) el.classList.toggle('hidden', k !== tabKey);
  });

  // Also hide other gymView children that belong to workout when not on workout tab
  const gymSettings = document.getElementById('gymSettingsContainer');
  const gymEncyc = document.getElementById('gymEncyclopediaContainer');
  const gymExMgr = document.getElementById('gymExManagerContainer');
  const gymRest = document.getElementById('gymRestBlock');
  const gymTools = document.getElementById('gymToolsQuickBarContainer');
  const gymDayOverride = document.getElementById('gymDayOverrideContainer');
  const gymPause = document.getElementById('gymPauseBanner');
  const gymSession = document.getElementById('gymSessionContainer');
  const isWorkout = tabKey === 'workout';
  [gymSettings, gymEncyc, gymExMgr, gymTools, gymDayOverride, gymSession].forEach(el => {
    if(el) el.style.display = isWorkout ? '' : 'none';
  });

  // Update tab buttons
  document.querySelectorAll('.gym-subtab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.gymTab === tabKey);
  });
}

// Wire gym sub-tab clicks
document.addEventListener('DOMContentLoaded', function(){
  const subTabs = document.getElementById('gymSubTabs');
  if(subTabs){
    subTabs.addEventListener('click', function(e){
      const btn = e.target.closest('.gym-subtab-btn');
      if(btn) switchGymSubTab(btn.dataset.gymTab);
    });
  }
  // Load saved settings on startup
  loadColorTheme();
  loadUltraCompact();
  applyFeatureToggles();
});

// Handle gym sub-tab redirect after navigation
const _origApplyMode = typeof applyMode === 'function' ? applyMode : null;
if(_origApplyMode){
  const _wrapped = applyMode;
  // We'll patch after applyMode runs instead
}
// Simpler: hook into navigateTo post-processing
(function(){
  const origNav = window.navigateTo;
  if(!origNav) return;
  // Already patched above in navigateTo replacement — handle _gymSubTabTarget in applyMode
  // Add a MutationObserver or just check after applyMode
})();

// Patch: after each applyMode call, check for sub-tab redirect
const _patchedApplyModeForGymTabs = (function(){
  const origApply = window.applyMode;
  if(!origApply) return;
  window.applyMode = function(){
    origApply.apply(this, arguments);
    if(mode === 'gym' && window._gymSubTabTarget){
      switchGymSubTab(window._gymSubTabTarget);
      delete window._gymSubTabTarget;
    } else if(mode === 'gym'){
      switchGymSubTab('workout');
    }
    if(mode === 'settings') renderSettingsView();
  };
})();

"""

# Inject before the closing </script> tag
last_script_close = html.rfind('</script>')
assert last_script_close != -1, "Cannot find </script>"
html = html[:last_script_close] + SETTINGS_JS_ENGINE + html[last_script_close:]
print("  JavaScript engine injected.")


# ============================================================
# STEP 9: Write index.html + sync parity
# ============================================================
print("[9/10] Writing modified HTML and syncing 3-way parity...")

# Normalize line endings to LF for consistency
html = html.replace('\r\n', '\n')

write_utf8(INDEX, html)
shutil.copy2(INDEX, ZATOONA)
shutil.copy2(INDEX, ANDROID_HTML)

h1 = sha256(INDEX)
h2 = sha256(ZATOONA)
h3 = sha256(ANDROID_HTML)
assert h1 == h2 == h3, f"PARITY BROKEN! {h1} vs {h2} vs {h3}"
sz = os.path.getsize(INDEX)
print(f"  3-way parity confirmed: {h1} ({sz:,} bytes)")


# ============================================================
# STEP 10: Update ALLOWED_MODES in ZatoonaBridge.kt + scrollbar in MainActivity.kt
# ============================================================
print("[10/10] Updating Android Kotlin files...")

# 10a: Add "settings" to ALLOWED_MODES
bridge_kt = read_utf8(BRIDGE_KT)
OLD_ALLOWED = '''        val ALLOWED_MODES = setOf(
            "home", "meal", "gym", "sleep", "prayer", "schedule",
            "recovery", "overview", "search", "budget", "notes", "stretches", "study"
        )'''
NEW_ALLOWED = '''        val ALLOWED_MODES = setOf(
            "home", "meal", "gym", "sleep", "prayer", "schedule",
            "recovery", "overview", "search", "budget", "notes", "stretches", "study", "settings"
        )'''
assert OLD_ALLOWED in bridge_kt, "Cannot find ALLOWED_MODES in ZatoonaBridge.kt"
bridge_kt = bridge_kt.replace(OLD_ALLOWED, NEW_ALLOWED)
write_utf8(BRIDGE_KT, bridge_kt)
print("  ALLOWED_MODES updated in ZatoonaBridge.kt")

# 10b: Add scrollbar disable to MainActivity.kt
main_kt = read_utf8(MAIN_KT)
OLD_SET_CONTENT = """        webView = WebView(this)
        setContentView(webView)"""
NEW_SET_CONTENT = """        webView = WebView(this)
        webView.isVerticalScrollBarEnabled = false
        webView.isHorizontalScrollBarEnabled = false
        setContentView(webView)"""
assert OLD_SET_CONTENT in main_kt, "Cannot find setContentView in MainActivity.kt"
main_kt = main_kt.replace(OLD_SET_CONTENT, NEW_SET_CONTENT)
write_utf8(MAIN_KT, main_kt)
print("  Scrollbar disabled in MainActivity.kt")

print("\n" + "="*60)
print("✅ ALL 10 STEPS COMPLETE — Consolidation injection done!")
print(f"   HTML SHA-256: {h1}")
print(f"   HTML Size: {sz:,} bytes")
print("="*60)

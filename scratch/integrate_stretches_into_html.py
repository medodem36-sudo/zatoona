# -*- coding: utf-8 -*-
"""
Phase 9C.1 Integration Script
Modifies index.html to add Stretch & Mobility Encyclopedia:
1. CSS before </style>
2. Drawer nav button after notes drawer button
3. Sidebar nav button after notes sidebar button
4. Mode button card after notes mode button
5. Stretches view HTML after notesView
6. Script tag for stretch-catalog.js
7. NAV_MODES update
8. applyMode() views, btns, titles maps
9. Week calendar hiding for stretches mode
10. renderStretchesView() call
11. wireActivate for stretches mode button
12. Stretch encyclopedia JS controller code
"""
import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

html_path = 'index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)
print(f"Original index.html size: {original_len} bytes")

# ===============================================================
# 1. CSS — insert before </style>
# ===============================================================
STRETCH_CSS = """
  /* ================= PHASE 9C.1: STRETCH & MOBILITY ENCYCLOPEDIA ================= */
  .str-search-row{
    display:flex; gap:8px; margin-bottom:10px; flex-wrap:wrap;
  }
  .str-search-input{
    flex:1; min-width:200px; padding:10px 14px; border-radius:var(--radius);
    border:1px solid var(--line); background:var(--card); color:var(--text);
    font-family:inherit; font-size:.92rem;
  }
  .str-search-input::placeholder{ color:var(--muted); }
  .str-filter-bar{
    display:flex; gap:6px; flex-wrap:wrap; margin-bottom:12px;
  }
  .str-filter-chip{
    padding:5px 12px; border-radius:20px; border:1px solid var(--line);
    background:var(--card); color:var(--text); font-size:.78rem; font-weight:600;
    cursor:pointer; user-select:none; transition:all .15s ease;
    font-family:inherit; white-space:nowrap;
  }
  .str-filter-chip:hover{ border-color:var(--accent); }
  .str-filter-chip.active{
    background:linear-gradient(135deg, var(--accent), var(--accent-dim));
    color:var(--btn-active-text); border-color:var(--accent);
  }
  .str-filter-dropdown{
    padding:6px 10px; border-radius:var(--radius); border:1px solid var(--line);
    background:var(--card); color:var(--text); font-family:inherit; font-size:.82rem;
    min-width:100px; cursor:pointer;
  }
  .str-count-bar{
    font-size:.82rem; color:var(--muted); font-weight:500; margin-bottom:10px;
    display:flex; justify-content:space-between; align-items:center;
  }
  .str-grid{
    display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr));
    gap:14px; margin-bottom:20px;
  }
  .str-card{
    border:1px solid var(--line); border-radius:var(--radius); background:var(--card);
    overflow:hidden; box-shadow:var(--shadow); transition:transform .15s ease, box-shadow .15s ease;
    cursor:pointer;
  }
  .str-card:hover{
    transform:translateY(-2px); box-shadow:var(--shadow-md); border-color:var(--accent);
  }
  .str-card-img{
    width:100%; height:160px; object-fit:cover; background:var(--card-alt);
    display:block; border-bottom:1px solid var(--line);
  }
  .str-card-body{
    padding:12px 14px;
  }
  .str-card-title{
    font-weight:800; font-size:.95rem; color:var(--text); margin-bottom:4px;
    line-height:1.4;
  }
  .str-card-name-en{
    font-size:.78rem; color:var(--muted); margin-bottom:6px; font-weight:500;
  }
  .str-card-meta{
    display:flex; gap:6px; flex-wrap:wrap; align-items:center;
  }
  .str-card-tag{
    font-size:.7rem; padding:2px 8px; border-radius:10px; font-weight:600;
    background:var(--card-alt); color:var(--muted); border:1px solid var(--line);
  }
  .str-card-tag.type-tag{
    background:var(--accent); color:var(--btn-active-text); border-color:var(--accent);
  }
  .str-empty-state{
    text-align:center; padding:40px 20px; color:var(--muted);
  }
  .str-empty-state .str-empty-icon{ font-size:3rem; margin-bottom:12px; display:block; }
  .str-empty-state .str-empty-text{ font-size:.95rem; margin-bottom:14px; line-height:1.6; }
  .str-reset-btn{
    padding:8px 20px; border-radius:var(--radius); border:1px solid var(--accent);
    background:transparent; color:var(--accent); font-weight:700; font-size:.85rem;
    cursor:pointer; font-family:inherit;
  }
  .str-reset-btn:hover{ background:var(--accent); color:var(--btn-active-text); }

  /* Detail Modal Overlay */
  .str-modal-overlay{
    position:fixed; top:0; left:0; width:100%; height:100%; z-index:1200;
    background:rgba(0,0,0,.55); display:flex; align-items:center; justify-content:center;
    padding:16px; opacity:0; pointer-events:none; transition:opacity .2s ease;
  }
  .str-modal-overlay.open{ opacity:1; pointer-events:auto; }
  .str-modal{
    background:var(--card); border-radius:var(--radius); width:100%; max-width:640px;
    max-height:85vh; overflow-y:auto; box-shadow:var(--shadow-lg); position:relative;
    scrollbar-width:thin;
  }
  .str-modal-header{
    position:sticky; top:0; background:var(--card); z-index:2; padding:16px 18px 10px;
    border-bottom:1px solid var(--line); display:flex; justify-content:space-between; align-items:flex-start;
  }
  .str-modal-close{
    background:none; border:none; font-size:1.5rem; cursor:pointer; color:var(--muted);
    padding:4px 8px; border-radius:6px; line-height:1;
  }
  .str-modal-close:hover{ background:var(--card-alt); color:var(--text); }
  .str-modal-img{
    width:100%; max-height:220px; object-fit:contain; background:var(--card-alt);
    display:block;
  }
  .str-modal-body{ padding:16px 18px 20px; }
  .str-modal-title{ font-weight:800; font-size:1.1rem; color:var(--text); margin-bottom:2px; }
  .str-modal-subtitle{ font-size:.85rem; color:var(--muted); margin-bottom:10px; }
  .str-modal-section{ margin-bottom:14px; }
  .str-modal-section-title{
    font-weight:700; font-size:.88rem; color:var(--accent); margin-bottom:6px;
    display:flex; align-items:center; gap:6px;
  }
  .str-modal-section ol,
  .str-modal-section ul{
    margin:0; padding-right:22px; padding-left:0; list-style-position:outside;
  }
  .str-modal-section li{
    font-size:.85rem; color:var(--text); line-height:1.7; margin-bottom:4px;
  }
  .str-modal-info-grid{
    display:grid; grid-template-columns:1fr 1fr; gap:8px;
  }
  .str-modal-info-item{
    background:var(--card-alt); border-radius:8px; padding:8px 10px;
    border:1px solid var(--line);
  }
  .str-modal-info-label{ font-size:.72rem; color:var(--muted); font-weight:600; }
  .str-modal-info-value{ font-size:.88rem; color:var(--text); font-weight:700; margin-top:2px; }
  .str-modal-safety{
    background:rgba(245,158,11,.08); border:1px solid rgba(245,158,11,.25);
    border-radius:8px; padding:10px 12px; font-size:.82rem; color:var(--text); line-height:1.6;
  }
  .str-modal-related{
    display:flex; gap:6px; flex-wrap:wrap;
  }
  .str-modal-related-chip{
    padding:4px 10px; border-radius:10px; font-size:.75rem; font-weight:600;
    background:var(--card-alt); border:1px solid var(--line); color:var(--text);
    cursor:default;
  }
  @media (max-width: 480px) {
    .str-grid{ grid-template-columns:1fr; }
    .str-card-img{ height:140px; }
    .str-modal-info-grid{ grid-template-columns:1fr; }
    .str-modal{ max-height:92vh; }
  }
"""

content = content.replace('</style>', STRETCH_CSS + '\n</style>', 1)
print("✓ CSS injected before </style>")

# ===============================================================
# 2. Drawer nav button — after notes drawer button
# ===============================================================
NOTES_DRAWER_BTN = """    <button type="button" class="drawer-nav-btn" data-nav="notes" id="drawNav-notes">
      <span class="dnb-icon" aria-hidden="true">📝</span>
      <div class="dnb-text">
        <span class="dnb-label">الملاحظات</span>
        <span class="dnb-desc">دفتر الملاحظات الموحد والمرفقات</span>
      </div>
    </button>"""

STRETCHES_DRAWER_BTN = """    <button type="button" class="drawer-nav-btn" data-nav="notes" id="drawNav-notes">
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
    </button>"""

content = content.replace(NOTES_DRAWER_BTN, STRETCHES_DRAWER_BTN, 1)
print("✓ Drawer nav button added")

# ===============================================================
# 3. Sidebar nav button — after notes sidebar button
# ===============================================================
NOTES_SIDEBAR = """      <button type="button" class="sidebar-nav-btn" data-nav="notes" id="sideNav-notes" title="الملاحظات">
        <span class="snb-icon" aria-hidden="true">📝</span>
        <div class="snb-text">
          <span class="snb-label">الملاحظات</span>
          <span class="snb-desc">دفتر الملاحظات الموحد</span>
        </div>
      </button>
    </nav>"""

STRETCHES_SIDEBAR = """      <button type="button" class="sidebar-nav-btn" data-nav="notes" id="sideNav-notes" title="الملاحظات">
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
    </nav>"""

content = content.replace(NOTES_SIDEBAR, STRETCHES_SIDEBAR, 1)
print("✓ Sidebar nav button added")

# ===============================================================
# 4. Mode button card — after notes mode button
# ===============================================================
NOTES_MODE_BTN = """    <div class="mode-btn" id="modeNotes" role="button" tabindex="0" aria-label="الملاحظات"><span class="mb-ico">📝</span><span class="mb-label">الملاحظات</span><span class="mb-desc">دفتر الملاحظات الموحد والمرفقات</span></div>
  </div>"""

STRETCHES_MODE_BTN = """    <div class="mode-btn" id="modeNotes" role="button" tabindex="0" aria-label="الملاحظات"><span class="mb-ico">📝</span><span class="mb-label">الملاحظات</span><span class="mb-desc">دفتر الملاحظات الموحد والمرفقات</span></div>
    <div class="mode-btn" id="modeStretches" role="button" tabindex="0" aria-label="الاستطالات"><span class="mb-ico">🧘</span><span class="mb-label">الاستطالات</span><span class="mb-desc">موسوعة حركات الإطالة والمرونة</span></div>
  </div>"""

content = content.replace(NOTES_MODE_BTN, STRETCHES_MODE_BTN, 1)
print("✓ Mode button card added")

# ===============================================================
# 5. Stretches View HTML — after notesView closing </div>
# ===============================================================
STRETCHES_VIEW_HTML = """
  <!-- ===== STRETCH & MOBILITY ENCYCLOPEDIA (Phase 9C.1) ===== -->
  <div id="stretchesView" class="hidden">
    <div class="section-title"><span class="n">🧘</span> موسوعة الاسترتشات والمرونة</div>
    <div class="section-hint">حركات إطالة وتحضير مفصلي وتنشيط عضلي مبنية على أسس تشريحية — للإحماء والتهدئة والاستشفاء الحركي</div>

    <!-- Search Bar -->
    <div class="str-search-row">
      <input type="search" class="str-search-input" id="stretchSearchInput" placeholder="ابحث باسم الحركة أو العضلة (عربي / إنجليزي)..." autocomplete="off">
    </div>

    <!-- Filter Chips Row -->
    <div class="str-filter-bar" id="stretchFilterBar">
      <select class="str-filter-dropdown" id="strFilterType" aria-label="نوع الحركة">
        <option value="">كل الأنواع</option>
        <option value="static_stretch">إطالة ثابتة</option>
        <option value="dynamic_stretch">إطالة ديناميكية</option>
        <option value="joint_mobility">مرونة مفصلية</option>
        <option value="activation">تنشيط عضلي</option>
        <option value="warmup_drill">إحماء تحضيري</option>
      </select>
      <select class="str-filter-dropdown" id="strFilterRegion" aria-label="منطقة الجسم">
        <option value="">كل المناطق</option>
        <option value="chest_shoulders">الصدر والكتفين</option>
        <option value="back_lats">الظهر واللاتس</option>
        <option value="neck_upper_back">الرقبة وأعلى الظهر</option>
        <option value="hips_pelvis">الورك والحوض</option>
        <option value="thighs_legs">الفخذين والساقين</option>
        <option value="glutes">المؤخرة</option>
        <option value="calves_ankles">السمانة والكاحل</option>
        <option value="wrists_forearms">الرسغ والساعد</option>
        <option value="spine_rotation">العمود الفقري والدوران</option>
        <option value="full_body">كامل الجسم</option>
      </select>
      <select class="str-filter-dropdown" id="strFilterEquipment" aria-label="المعدات">
        <option value="">كل المعدات</option>
        <option value="none">بدون معدات</option>
        <option value="mat">بساط تمرين</option>
        <option value="wall">حائط / جدار</option>
        <option value="band">شريط مقاومة</option>
      </select>
      <select class="str-filter-dropdown" id="strFilterLevel" aria-label="المستوى">
        <option value="">كل المستويات</option>
        <option value="beginner">مبتدئ</option>
        <option value="intermediate">متوسط</option>
        <option value="advanced">متقدم</option>
      </select>
      <select class="str-filter-dropdown" id="strFilterPurpose" aria-label="الغرض">
        <option value="">كل الأغراض</option>
        <option value="warmup">إحماء</option>
        <option value="cooldown">تهدئة</option>
        <option value="mobility">مرونة وحركة</option>
      </select>
    </div>

    <!-- Count Bar -->
    <div class="str-count-bar">
      <span id="stretchCountLabel">34 حركة</span>
    </div>

    <!-- Cards Grid -->
    <div class="str-grid" id="stretchesGrid"></div>

    <!-- Empty State -->
    <div class="str-empty-state hidden" id="stretchesEmptyState">
      <span class="str-empty-icon">🔍</span>
      <div class="str-empty-text">لم يتم العثور على حركات تطابق معايير البحث والفلترة الحالية</div>
      <button class="str-reset-btn" id="stretchesResetBtn" type="button">مسح الفلاتر والبحث</button>
    </div>
  </div>

  <!-- Stretch Detail Modal -->
  <div class="str-modal-overlay" id="stretchDetailModal" role="dialog" aria-modal="true" aria-label="تفاصيل الحركة">
    <div class="str-modal">
      <div class="str-modal-header">
        <div>
          <div class="str-modal-title" id="strModalTitle"></div>
          <div class="str-modal-subtitle" id="strModalSubtitle"></div>
        </div>
        <button class="str-modal-close" id="strModalCloseBtn" aria-label="إغلاق" type="button">&times;</button>
      </div>
      <img class="str-modal-img" id="strModalImg" alt="" loading="lazy">
      <div class="str-modal-body" id="strModalBody"></div>
    </div>
  </div>"""

# Insert stretchesView after notesView's closing </div> and before footer
NOTES_VIEW_END_MARKER = """  <!-- ===== UNIFIED NOTES HUB MODE (Phase 9B.1) ===== -->"""

# We'll insert the stretchesView HTML right before the footer line
FOOTER_LINE = """  <footer>البيانات محفوظة في متصفحك على الجهاز ده بس — افتح نفس الملف من نفس المتصفح عشان ترجعلك.</footer>"""

content = content.replace(FOOTER_LINE, STRETCHES_VIEW_HTML + '\n\n' + FOOTER_LINE, 1)
print("✓ Stretches view HTML injected")

# ===============================================================
# 6. Script tag for stretch-catalog.js
# ===============================================================
content = content.replace(
    '<script src="./assets/data/exercise-catalog.js"></script>',
    '<script src="./assets/data/exercise-catalog.js"></script>\n<script src="./assets/data/stretch-catalog.js"></script>',
    1
)
print("✓ stretch-catalog.js script tag added")

# ===============================================================
# 7. NAV_MODES update
# ===============================================================
content = content.replace(
    "const NAV_MODES = ['home','meal','gym','sleep','prayer','schedule','recovery','overview','search','budget','notes'];",
    "const NAV_MODES = ['home','meal','gym','sleep','prayer','schedule','recovery','overview','search','budget','notes','stretches'];",
    1
)
print("✓ NAV_MODES updated")

# ===============================================================
# 8. applyMode() — views map
# ===============================================================
content = content.replace(
    "    notes: document.getElementById('notesView'),\n  };",
    "    notes: document.getElementById('notesView'),\n    stretches: document.getElementById('stretchesView'),\n  };",
    1
)
print("✓ applyMode views map updated")

# 8b. applyMode() — btns map
content = content.replace(
    "    notes: document.getElementById('modeNotes'),\n  };",
    "    notes: document.getElementById('modeNotes'),\n    stretches: document.getElementById('modeStretches'),\n  };",
    1
)
print("✓ applyMode btns map updated")

# 8c. applyMode() — titles map
content = content.replace(
    "    notes: ['📝 دفتر الملاحظات الموحد', 'سجل شامل لملاحظاتك اليومية وملاحظات التمارين والاستشفاء والأقسام ومرفقاتها'],\n  };",
    "    notes: ['📝 دفتر الملاحظات الموحد', 'سجل شامل لملاحظاتك اليومية وملاحظات التمارين والاستشفاء والأقسام ومرفقاتها'],\n    stretches: ['🧘 موسوعة الاسترتشات والمرونة', 'حركات إطالة وتحضير مفصلي وتنشيط عضلي — للإحماء والتهدئة والاستشفاء الحركي'],\n  };",
    1
)
print("✓ applyMode titles map updated")

# ===============================================================
# 9. Week calendar hiding for stretches mode
# ===============================================================
content = content.replace(
    "if(mode==='budget' || mode==='notes' || isHome){",
    "if(mode==='budget' || mode==='notes' || mode==='stretches' || isHome){",
    1
)
print("✓ Week calendar hiding updated for stretches")

# ===============================================================
# 10. renderStretchesView() call in applyMode
# ===============================================================
content = content.replace(
    "  if(mode==='notes') renderNotesHub();",
    "  if(mode==='notes') renderNotesHub();\n  if(mode==='stretches') renderStretchesView();",
    1
)
print("✓ renderStretchesView() call added")

# ===============================================================
# 11. wireActivate for stretches mode button
# ===============================================================
content = content.replace(
    "wireActivate(document.getElementById('modeNotes'), ()=> navigateTo('notes'));",
    "wireActivate(document.getElementById('modeNotes'), ()=> navigateTo('notes'));\nwireActivate(document.getElementById('modeStretches'), ()=> navigateTo('stretches'));",
    1
)
print("✓ wireActivate for modeStretches added")

# ===============================================================
# 12. Stretch Encyclopedia JS Controller
# ===============================================================
STRETCH_JS_CONTROLLER = """

/* ================= PHASE 9C.1: STRETCH & MOBILITY ENCYCLOPEDIA CONTROLLER ================= */
function renderStretchesView(){
  const catalog = window.ZATOONA_STRETCH_CATALOG || [];
  const grid = document.getElementById('stretchesGrid');
  const emptyState = document.getElementById('stretchesEmptyState');
  const countLabel = document.getElementById('stretchCountLabel');
  const searchInput = document.getElementById('stretchSearchInput');
  const filterType = document.getElementById('strFilterType');
  const filterRegion = document.getElementById('strFilterRegion');
  const filterEquipment = document.getElementById('strFilterEquipment');
  const filterLevel = document.getElementById('strFilterLevel');
  const filterPurpose = document.getElementById('strFilterPurpose');
  const resetBtn = document.getElementById('stretchesResetBtn');

  if(!grid) return;

  const TYPE_LABELS = {
    'static_stretch': 'إطالة ثابتة',
    'dynamic_stretch': 'إطالة ديناميكية',
    'joint_mobility': 'مرونة مفصلية',
    'activation': 'تنشيط عضلي',
    'warmup_drill': 'إحماء تحضيري'
  };

  const REGION_LABELS = {
    'chest_shoulders': 'الصدر والكتفين',
    'back_lats': 'الظهر واللاتس',
    'neck_upper_back': 'الرقبة وأعلى الظهر',
    'hips_pelvis': 'الورك والحوض',
    'thighs_legs': 'الفخذين والساقين',
    'glutes': 'المؤخرة',
    'calves_ankles': 'السمانة والكاحل',
    'wrists_forearms': 'الرسغ والساعد',
    'spine_rotation': 'العمود الفقري',
    'full_body': 'كامل الجسم'
  };

  const EQUIPMENT_LABELS = {
    'none': 'بدون معدات',
    'mat': 'بساط تمرين',
    'wall': 'حائط',
    'band': 'شريط مقاومة'
  };

  const LEVEL_LABELS = {
    'beginner': 'مبتدئ',
    'intermediate': 'متوسط',
    'advanced': 'متقدم'
  };

  function normalizeArabicSearch(s){
    return String(s||'').toLowerCase()
      .replace(/[أإآٱ]/g, 'ا')
      .replace(/[ؤ]/g, 'و')
      .replace(/[ئ]/g, 'ي')
      .replace(/[ة]/g, 'ه')
      .replace(/[ى]/g, 'ي')
      .replace(/[\\u064B-\\u065F\\u0670]/g, '')
      .trim();
  }

  function getSearchableText(m){
    const parts = [
      m.name, m.nameAr,
      ...(m.aliases || []),
      ...(m.primaryMuscles || []),
      ...(m.secondaryMuscles || []),
      ...(m.bodyRegions || []),
      m.equipment || '',
      TYPE_LABELS[m.type] || m.type || '',
      REGION_LABELS[(m.bodyRegions||[])[0]] || ''
    ];
    return normalizeArabicSearch(parts.join(' '));
  }

  function applyFilters(){
    const q = normalizeArabicSearch(searchInput.value);
    const tVal = filterType.value;
    const rVal = filterRegion.value;
    const eVal = filterEquipment.value;
    const lVal = filterLevel.value;
    const pVal = filterPurpose.value;

    const results = catalog.filter(m => {
      if(q && !getSearchableText(m).includes(q)) return false;
      if(tVal && m.type !== tVal) return false;
      if(rVal && !(m.bodyRegions||[]).includes(rVal)) return false;
      if(eVal && m.equipment !== eVal) return false;
      if(lVal && m.level !== lVal) return false;
      if(pVal && !(m.suitableFor||[]).includes(pVal)) return false;
      return true;
    });

    renderCards(results);
  }

  function renderCards(items){
    grid.innerHTML = '';
    if(items.length === 0){
      grid.classList.add('hidden');
      emptyState.classList.remove('hidden');
      countLabel.textContent = 'لا توجد نتائج';
    } else {
      grid.classList.remove('hidden');
      emptyState.classList.add('hidden');
      countLabel.textContent = items.length + ' حركة';
      items.forEach(m => {
        const card = document.createElement('div');
        card.className = 'str-card';
        card.setAttribute('role','button');
        card.setAttribute('tabindex','0');
        card.setAttribute('aria-label', m.nameAr);

        const durationText = m.durationSeconds
          ? m.durationSeconds + ' ث'
          : (m.recommendedReps || '');
        const regionLabel = REGION_LABELS[(m.bodyRegions||[])[0]] || '';
        const typeLabel = TYPE_LABELS[m.type] || m.type;

        card.innerHTML = '<img class="str-card-img" src="' + (m.image || '') + '" alt="' + (m.nameAr||'') + '" loading="lazy" onerror="this.style.display=\\'none\\'">' +
          '<div class="str-card-body">' +
          '<div class="str-card-title">' + (m.nameAr||'') + '</div>' +
          '<div class="str-card-name-en">' + (m.name||'') + '</div>' +
          '<div class="str-card-meta">' +
          '<span class="str-card-tag type-tag">' + typeLabel + '</span>' +
          (regionLabel ? '<span class="str-card-tag">' + regionLabel + '</span>' : '') +
          (durationText ? '<span class="str-card-tag">' + durationText + '</span>' : '') +
          '</div></div>';

        card.addEventListener('click', () => openStretchModal(m));
        card.addEventListener('keydown', e => { if(e.key==='Enter'||e.key===' '){ e.preventDefault(); openStretchModal(m); }});
        grid.appendChild(card);
      });
    }
  }

  function openStretchModal(m){
    const overlay = document.getElementById('stretchDetailModal');
    const title = document.getElementById('strModalTitle');
    const subtitle = document.getElementById('strModalSubtitle');
    const img = document.getElementById('strModalImg');
    const body = document.getElementById('strModalBody');

    title.textContent = m.nameAr || '';
    subtitle.textContent = m.name || '';
    img.src = m.image || '';
    img.alt = m.nameAr || '';
    img.onerror = function(){ this.style.display='none'; };

    let html = '';

    // Type & Tags
    const typeLabel = TYPE_LABELS[m.type] || m.type;
    const regionLabel = REGION_LABELS[(m.bodyRegions||[])[0]] || '';
    html += '<div class="str-modal-section"><div class="str-modal-info-grid">';
    html += '<div class="str-modal-info-item"><div class="str-modal-info-label">نوع الحركة</div><div class="str-modal-info-value">' + typeLabel + '</div></div>';
    html += '<div class="str-modal-info-item"><div class="str-modal-info-label">المنطقة</div><div class="str-modal-info-value">' + regionLabel + '</div></div>';
    html += '<div class="str-modal-info-item"><div class="str-modal-info-label">المستوى</div><div class="str-modal-info-value">' + (LEVEL_LABELS[m.level]||m.level||'') + '</div></div>';
    html += '<div class="str-modal-info-item"><div class="str-modal-info-label">المعدات</div><div class="str-modal-info-value">' + (EQUIPMENT_LABELS[m.equipment]||m.equipment||'بدون') + '</div></div>';
    if(m.durationSeconds){
      html += '<div class="str-modal-info-item"><div class="str-modal-info-label">المدة</div><div class="str-modal-info-value">' + m.durationSeconds + ' ثانية</div></div>';
    }
    if(m.recommendedReps){
      html += '<div class="str-modal-info-item"><div class="str-modal-info-label">التكرارات</div><div class="str-modal-info-value">' + m.recommendedReps + '</div></div>';
    }
    html += '</div></div>';

    // Muscles
    const primaryAr = (m.primaryMuscles||[]).join('، ');
    const secondaryAr = (m.secondaryMuscles||[]).join('، ');
    if(primaryAr || secondaryAr){
      html += '<div class="str-modal-section"><div class="str-modal-section-title">💪 العضلات المستهدفة</div>';
      if(primaryAr) html += '<div style="font-size:.85rem;color:var(--text);margin-bottom:4px"><strong>أساسية:</strong> ' + primaryAr + '</div>';
      if(secondaryAr) html += '<div style="font-size:.85rem;color:var(--muted)"><strong>ثانوية:</strong> ' + secondaryAr + '</div>';
      html += '</div>';
    }

    // Instructions
    if(m.instructions && m.instructions.length){
      html += '<div class="str-modal-section"><div class="str-modal-section-title">📋 خطوات التنفيذ</div><ol>';
      m.instructions.forEach(step => { html += '<li>' + step + '</li>'; });
      html += '</ol></div>';
    }

    // Breathing
    if(m.breathing){
      html += '<div class="str-modal-section"><div class="str-modal-section-title">🌬️ التنفس</div>';
      html += '<div style="font-size:.85rem;color:var(--text);line-height:1.7">' + m.breathing + '</div></div>';
    }

    // Common mistakes
    if(m.commonMistakes && m.commonMistakes.length){
      html += '<div class="str-modal-section"><div class="str-modal-section-title">⚠️ أخطاء شائعة</div><ul>';
      m.commonMistakes.forEach(err => { html += '<li>' + err + '</li>'; });
      html += '</ul></div>';
    }

    // Safety notes
    if(m.safetyNotes){
      html += '<div class="str-modal-section"><div class="str-modal-section-title">🛡️ تحذيرات الأمان</div>';
      html += '<div class="str-modal-safety">' + m.safetyNotes + '</div></div>';
    }

    // Suitable for
    if(m.suitableFor && m.suitableFor.length){
      const purposeLabels = {'warmup':'إحماء','cooldown':'تهدئة','mobility':'مرونة وحركة'};
      html += '<div class="str-modal-section"><div class="str-modal-section-title">🎯 مناسبة لـ</div>';
      html += '<div class="str-modal-related">';
      m.suitableFor.forEach(p => { html += '<span class="str-modal-related-chip">' + (purposeLabels[p]||p) + '</span>'; });
      html += '</div></div>';
    }

    // Related exercises
    if(m.relatedExerciseIds && m.relatedExerciseIds.length){
      const exCatalog = window.ZATOONA_EXERCISE_CATALOG || [];
      html += '<div class="str-modal-section"><div class="str-modal-section-title">🔗 تمارين مقاومة مرتبطة</div>';
      html += '<div class="str-modal-related">';
      m.relatedExerciseIds.forEach(eid => {
        const ex = exCatalog.find(e => e.id === eid);
        const label = ex ? (ex.nameAr || ex.name) : eid;
        html += '<span class="str-modal-related-chip">' + label + '</span>';
      });
      html += '</div></div>';
    }

    body.innerHTML = html;
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  // Close modal
  function closeStretchModal(){
    const overlay = document.getElementById('stretchDetailModal');
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  document.getElementById('strModalCloseBtn').addEventListener('click', closeStretchModal);
  document.getElementById('stretchDetailModal').addEventListener('click', function(e){
    if(e.target === this) closeStretchModal();
  });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape'){
      const overlay = document.getElementById('stretchDetailModal');
      if(overlay && overlay.classList.contains('open')) closeStretchModal();
    }
  });

  // Wire filters
  searchInput.addEventListener('input', applyFilters);
  filterType.addEventListener('change', applyFilters);
  filterRegion.addEventListener('change', applyFilters);
  filterEquipment.addEventListener('change', applyFilters);
  filterLevel.addEventListener('change', applyFilters);
  filterPurpose.addEventListener('change', applyFilters);

  // Reset
  resetBtn.addEventListener('click', function(){
    searchInput.value = '';
    filterType.value = '';
    filterRegion.value = '';
    filterEquipment.value = '';
    filterLevel.value = '';
    filterPurpose.value = '';
    applyFilters();
  });

  // Initial render
  applyFilters();
}
/* ================= END PHASE 9C.1 ================= */
"""

# Insert before the final </script> tag (which is before </body>)
# Find the last </script> before </body>
last_script_end = content.rfind('</script>')
if last_script_end != -1:
    content = content[:last_script_end] + STRETCH_JS_CONTROLLER + content[last_script_end:]
    print("✓ Stretch JS controller injected")
else:
    print("ERROR: Could not find </script> to inject controller!")

# ===============================================================
# Write the modified file
# ===============================================================
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"\nModified index.html size: {new_len} bytes (delta: +{new_len - original_len} bytes)")
print("Done! All 12 integration steps completed.")

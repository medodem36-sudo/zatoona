import os
import re
import sys
import subprocess

sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO, "index.html")
ZATOONA_PATH = os.path.join(REPO, "zatoona.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────
# 1. Inject CSS before </style>
# ─────────────────────────────────────────────────────────────
css_snippet = """
/* ================= PRE-WORKOUT INTERACTIVE WARM-UP (Phase 9C.2) ================= */
.gw-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 14px 16px;
  margin-bottom: 14px;
  transition: border-color .2s ease;
}
.gw-card.status-in_progress {
  border-color: var(--accent);
  box-shadow: 0 0 0 1px var(--accent-bg);
}
.gw-card.status-completed {
  border-color: var(--good);
}
.gw-card.status-skipped {
  opacity: 0.88;
}
.gw-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}
.gw-title-area {
  display: flex;
  align-items: center;
  gap: 8px;
}
.gw-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text);
  margin: 0;
}
.gw-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 9px;
  border-radius: 999px;
  font-size: .75rem;
  font-weight: 700;
}
.gw-status-badge.status-not_started { background: var(--bg-2); color: var(--muted); border: 1px solid var(--line); }
.gw-status-badge.status-in_progress { background: #e0f2fe; color: #0284c7; }
body.dark .gw-status-badge.status-in_progress { background: rgba(2, 132, 199, 0.2); color: #38bdf8; }
.gw-status-badge.status-completed { background: #dcfce7; color: #16a34a; }
body.dark .gw-status-badge.status-completed { background: rgba(22, 163, 74, 0.2); color: #4ade80; }
.gw-status-badge.status-skipped { background: var(--bg-2); color: var(--muted); }

.gw-meta-chips {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}
.gw-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 6px;
  background: var(--bg-2);
  border: 1px solid var(--line);
  font-size: .75rem;
  color: var(--muted);
}
.gw-chip strong { color: var(--text); }

.gw-progress-wrap {
  margin-bottom: 12px;
}
.gw-progress-bar {
  width: 100%;
  height: 6px;
  background: var(--bg-2);
  border-radius: 999px;
  overflow: hidden;
  margin-top: 4px;
}
.gw-progress-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 999px;
  transition: width .3s ease;
}
.gw-card.status-completed .gw-progress-fill {
  background: var(--good);
}

.gw-actions-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 8px;
  border-top: 1px dashed var(--line);
  margin-top: 10px;
}
.gw-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: .8rem;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--line);
  background: var(--card);
  color: var(--text);
  transition: all .15s ease;
}
.gw-btn:hover { background: var(--bg-2); }
.gw-btn-primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.gw-btn-primary:hover { opacity: .92; }
.gw-btn-good { background: var(--good); color: #fff; border-color: var(--good); }
.gw-btn-good:hover { opacity: .92; }
.gw-btn-subtle { background: transparent; color: var(--muted); border-color: transparent; font-size: .75rem; }
.gw-btn-subtle:hover { background: var(--bg-2); color: var(--text); }

.gw-drills-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 12px;
}
.gw-drill-item {
  display: flex;
  align-items: stretch;
  background: var(--bg-2);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  transition: all .2s ease;
}
.gw-drill-item.done {
  border-color: var(--good);
  background: rgba(22, 163, 74, 0.04);
}
body.dark .gw-drill-item.done {
  background: rgba(22, 163, 74, 0.08);
}
.gw-drill-thumb {
  flex: 0 0 100px;
  width: 100px;
  background: var(--card);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-left: 1px solid var(--line);
}
.gw-drill-thumb img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #fff;
}
body.dark .gw-drill-thumb img {
  filter: brightness(0.95);
}
.gw-drill-content {
  flex: 1;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 6px;
}
.gw-drill-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}
.gw-drill-title-wrap {
  flex: 1;
}
.gw-drill-name-ar {
  font-size: .92rem;
  font-weight: 700;
  color: var(--text);
  line-height: 1.4;
}
.gw-drill-name-en {
  font-size: .72rem;
  color: var(--muted);
}
.gw-drill-badges {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
  margin-top: 4px;
}
.gw-drill-badge {
  font-size: .68rem;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--card);
  border: 1px solid var(--line);
  color: var(--muted);
}
.gw-drill-badge.accent {
  background: var(--accent-bg);
  color: var(--accent);
  border-color: transparent;
  font-weight: 600;
}
.gw-drill-steps {
  margin: 4px 0 0;
  padding-right: 18px;
  font-size: .8rem;
  color: var(--text);
  line-height: 1.5;
}
.gw-drill-steps li {
  margin-bottom: 2px;
}
.gw-drill-cue {
  font-size: .72rem;
  color: var(--muted);
  font-style: italic;
  margin-top: 2px;
}
.gw-toggle-btn {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: .78rem;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid var(--line);
  background: var(--card);
  color: var(--muted);
  transition: all .15s ease;
  white-space: nowrap;
}
.gw-toggle-btn.done {
  background: var(--good);
  color: #fff;
  border-color: var(--good);
}

/* Warmup Sets Box */
.gw-warmup-sets-box {
  background: var(--bg-2);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 12px 14px;
  margin-top: 10px;
}
.gw-sets-ex-header {
  font-size: .9rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.gw-set-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 8px;
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 6px;
  margin-bottom: 6px;
  font-size: .8rem;
}
.gw-set-info {
  display: flex;
  flex-direction: column;
}
.gw-set-desc { font-weight: 600; color: var(--text); }
.gw-set-reps { font-size: .72rem; color: var(--muted); }
.gw-set-chip {
  padding: 3px 8px;
  border-radius: 4px;
  font-size: .72rem;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--line);
  background: var(--bg-2);
  color: var(--muted);
}
.gw-set-chip.done {
  background: var(--good);
  color: #fff;
  border-color: var(--good);
}
.gw-sets-notice {
  font-size: .7rem;
  color: var(--muted);
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Ready Banner */
.gw-ready-banner {
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.12), rgba(16, 185, 129, 0.06));
  border: 1px solid var(--good);
  border-radius: var(--radius);
  padding: 14px 16px;
  margin-top: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.gw-ready-text-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}
.gw-ready-icon { font-size: 1.8rem; }
.gw-ready-title { font-weight: 700; color: var(--text); font-size: .95rem; }
.gw-ready-sub { font-size: .78rem; color: var(--muted); margin-top: 2px; }
.gw-btn-start-session {
  padding: 8px 16px;
  font-size: .88rem;
  font-weight: 700;
  border-radius: 8px;
  background: var(--good);
  color: #fff;
  border: none;
  cursor: pointer;
  transition: opacity .15s ease;
}
.gw-btn-start-session:hover { opacity: .92; }

@media (max-width: 480px) {
  .gw-drill-item { flex-direction: column; }
  .gw-drill-thumb { width: 100%; height: 110px; border-left: none; border-bottom: 1px solid var(--line); }
  .gw-actions-bar { justify-content: stretch; }
  .gw-btn { flex: 1; }
}
"""

if "/* ================= PRE-WORKOUT INTERACTIVE WARM-UP (Phase 9C.2) ================= */" not in content:
    content = content.replace("</style>", css_snippet + "\n</style>", 1)
    print("1. Injected CSS before </style>")
else:
    print("1. CSS already present")

# ─────────────────────────────────────────────────────────────
# 2. Update HTML markup for #gymWorkoutBlock
# ─────────────────────────────────────────────────────────────
old_html_warmup = """      <div class="section-title"><span class="n">٢</span> الإحماء العام (8-10 دقايق)</div>
      <div class="section-hint">إحماء عام + سيتات إحماء تدريجية قبل التمرين التقيل — من غير استريتش ثابت طويل قبل الحديد (بيقلل القوة مؤقتًا)</div>
      <div class="checklist" id="warmup"></div>"""

new_html_warmup = """      <div class="section-title"><span class="n">٢</span> الإحماء قبل التمرين</div>
      <div class="section-hint">إحماء عام وحركات ديناميكية وتنشيطية موجهة لروتين اليوم — من غير استريتش ثابت طويل قبل الحديد</div>
      <div id="gymInteractiveWarmupContainer" style="margin-bottom:14px;"></div>
      <div class="checklist" id="warmup" style="display:none;"></div>"""

if old_html_warmup in content:
    content = content.replace(old_html_warmup, new_html_warmup, 1)
    print("2. Injected #gymInteractiveWarmupContainer into Section 2")
elif 'id="gymInteractiveWarmupContainer"' in content:
    print("2. #gymInteractiveWarmupContainer already present")
else:
    print("2. WARNING: Could not find old_html_warmup target")

# ─────────────────────────────────────────────────────────────
# 3. Add JS Functions & Logic
# ─────────────────────────────────────────────────────────────
js_warmup_code = """
/* ================= PRE-WORKOUT INTERACTIVE WARM-UP (Phase 9C.2) ================= */
const GYM_WARMUP_STORAGE_KEY = 'gym-warmup-state-v1';

function loadGymWarmupState(iso, expectedRoutineId){
  if(!iso || typeof iso !== 'string') return null;
  try {
    const raw = storageGetJSON(GYM_WARMUP_STORAGE_KEY, {});
    const rec = raw[iso] || null;
    if(rec && expectedRoutineId && rec.routineId && rec.routineId !== expectedRoutineId){
      // Routine was switched on this date — start fresh for new routine
      return {
        iso: iso,
        routineId: expectedRoutineId,
        started: false,
        completed: false,
        skipped: false,
        collapsed: false,
        completedDrills: {},
        completedWarmupSets: {},
        updatedAt: Date.now()
      };
    }
    return rec;
  } catch(e) {
    console.warn('[GymWarmup] Error loading state:', e);
    return null;
  }
}

function saveGymWarmupState(iso, state){
  if(!iso || typeof iso !== 'string' || !state) return false;
  try {
    const raw = storageGetJSON(GYM_WARMUP_STORAGE_KEY, {});
    raw[iso] = Object.assign({}, raw[iso] || {}, state, { iso: iso, updatedAt: Date.now() });
    storageSet(GYM_WARMUP_STORAGE_KEY, JSON.stringify(raw));
    return true;
  } catch(e) {
    console.warn('[GymWarmup] Error saving state:', e);
    return false;
  }
}

function generateRoutineWarmupPlan(routineId, effDay){
  const catalog = (typeof window !== 'undefined' && Array.isArray(window.ZATOONA_STRETCH_CATALOG))
    ? window.ZATOONA_STRETCH_CATALOG
    : [];

  // Step 1: General Cardio Drill
  const cardioStep = {
    id: 'gen-cardio',
    category: 'cardio',
    categoryLabel: 'إحماء عام',
    nameAr: 'إحماء قلبي حركي خفيف (كارديو)',
    name: 'General Light Cardio',
    target: 'الجسم كامل، رفع حرارة العضلات وتنشيط الدورة الدموية',
    durationOrReps: '3-5 دقائق',
    typeBadge: 'إحماء عام',
    equipment: 'بدون أجهزة / حبل / سير',
    image: './assets/images/warmup/warmup-01-cardio.svg',
    steps: [
      'ابدأ بمشي سريع، أو هرولة خفيفة في المكان، أو دراجة ثابتة، أو نط حبل خفيف.',
      'حافظ على وتيرة معتدلة ومنتظمة تسمح بالتنفس الطبيعي دون إرهاق.',
      'الهدف هو رفع معدل نبض القلب وزيادة تدفق الدم إلى العضلات والمفاصل.'
    ],
    cue: 'لا تبذل مجهودًا قاسيًا — الهدف تسخين الجسم فقط وليس التعب.'
  };

  const routineExList = (typeof getRoutineExercises === 'function') ? getRoutineExercises(routineId) : [];
  const targetedMuscles = new Set();
  let hasUpper = false, hasLower = false, hasPress = false, hasPull = false, hasLegs = false, hasHinge = false;

  const exCatalog = (typeof window !== 'undefined' && Array.isArray(window.ZATOONA_EXERCISE_CATALOG))
    ? window.ZATOONA_EXERCISE_CATALOG
    : [];
  const exCatalogMap = {};
  exCatalog.forEach(ex => { if(ex && ex.id) exCatalogMap[ex.id] = ex; });

  const compoundExercises = [];

  routineExList.forEach(ex => {
    if(!ex) return;
    const catId = ex.catalogExerciseId || ex.key || '';
    const targetStr = ((ex.target || '') + ' ' + (ex.name || '')).toLowerCase();

    const catEntry = exCatalogMap[catId];
    if(catEntry){
      (catEntry.primaryMuscles || []).forEach(m => targetedMuscles.add(m));
      (catEntry.secondaryMuscles || []).forEach(m => targetedMuscles.add(m));
      if(catEntry.mechanic === 'compound' || catEntry.category === 'strength'){
        compoundExercises.push(ex);
      }
    }

    if(/صدر|بنش|bench|chest|ضغط|push/i.test(targetStr)){ targetedMuscles.add('chest'); hasUpper = true; hasPress = true; }
    if(/كتف|شولدر|press|shoulder/i.test(targetStr)){ targetedMuscles.add('shoulders'); hasUpper = true; hasPress = true; }
    if(/ظهر|لاتس|سحب|عقلة|row|lat|pull/i.test(targetStr)){ targetedMuscles.add('lats'); hasUpper = true; hasPull = true; }
    if(/تراي|باي|ذراع|arm|triceps|biceps/i.test(targetStr)){ targetedMuscles.add('arms'); hasUpper = true; }
    if(/سكوات|squat|فخذ أمامي|أرجل|رجل|quad/i.test(targetStr)){ targetedMuscles.add('quads'); targetedMuscles.add('hips'); hasLower = true; hasLegs = true; }
    if(/ديدليفت|deadlift|rdl|فخذ خلفي|خلفيات|hamstring/i.test(targetStr)){ targetedMuscles.add('hamstrings'); targetedMuscles.add('glutes'); hasLower = true; hasHinge = true; }
    if(/مؤخرة|جلوتس|glute|ورك|حوض/i.test(targetStr)){ targetedMuscles.add('glutes'); targetedMuscles.add('hips'); hasLower = true; }
    if(/سمانة|كاحل|calf|ankle/i.test(targetStr)){ targetedMuscles.add('calves'); targetedMuscles.add('ankles'); hasLower = true; }
    if(/بطن|كرانش|بلانك|core|abs/i.test(targetStr)){ targetedMuscles.add('core'); targetedMuscles.add('spine'); }

    if(['squat', 'bench', 'pulldown', 'press', 'rdl', 'row', 'pullup', 'pushup'].includes(ex.key)){
      if(!compoundExercises.some(c => c.key === ex.key)) compoundExercises.push(ex);
    }
  });

  const rIdStr = String(routineId || '').toLowerCase();
  if(rIdStr === 'a'){ hasUpper = true; hasLower = true; hasPress = true; hasPull = true; hasLegs = true; }
  else if(rIdStr === 'b'){ hasUpper = true; hasLower = true; hasPull = true; hasHinge = true; hasPress = true; }
  else if(rIdStr.includes('push') || rIdStr.includes('chest')){ hasUpper = true; hasPress = true; }
  else if(rIdStr.includes('pull') || rIdStr.includes('back')){ hasUpper = true; hasPull = true; }
  else if(rIdStr.includes('leg') || rIdStr.includes('lower')){ hasLower = true; hasLegs = true; hasHinge = true; }
  else if(rIdStr.includes('upper')){ hasUpper = true; hasPress = true; hasPull = true; }
  else if(rIdStr.includes('fb') || rIdStr.includes('full')){ hasUpper = true; hasLower = true; }

  const selectedDrillIds = [];
  function addStretch(id){
    if(!selectedDrillIds.includes(id) && catalog.some(s => s.id === id)){
      selectedDrillIds.push(id);
    }
  }

  if(rIdStr === 'a'){
    addStretch('str-arm-circles-dynamic');
    addStretch('str-deep-squat-pry');
    addStretch('str-band-pull-apart-activation');
    addStretch('str-worlds-greatest-stretch');
  } else if(rIdStr === 'b'){
    addStretch('str-dynamic-leg-swings');
    addStretch('str-cat-cow-mobility');
    addStretch('str-band-pull-apart-activation');
    addStretch('str-glute-bridge-activation');
  } else if(hasLegs && !hasUpper){
    addStretch('str-dynamic-leg-swings');
    addStretch('str-hip-opener-90-90');
    addStretch('str-glute-bridge-activation');
    addStretch('str-deep-squat-pry');
    if(targetedMuscles.has('calves') || targetedMuscles.has('ankles')){
      addStretch('str-ankle-wall-mobilization');
    }
  } else if(hasPress && !hasPull && !hasLower){
    addStretch('str-arm-circles-dynamic');
    addStretch('str-band-shoulder-dislocations');
    addStretch('str-band-pull-apart-activation');
    addStretch('str-thoracic-spine-rotations');
  } else if(hasPull && !hasPress && !hasLower){
    addStretch('str-cat-cow-mobility');
    addStretch('str-band-pull-apart-activation');
    addStretch('str-arm-circles-dynamic');
    addStretch('str-bird-dog-activation');
  } else if(hasUpper && !hasLower){
    addStretch('str-arm-circles-dynamic');
    addStretch('str-band-shoulder-dislocations');
    addStretch('str-band-pull-apart-activation');
    addStretch('str-thoracic-spine-rotations');
  } else if(hasLower && !hasUpper){
    addStretch('str-dynamic-leg-swings');
    addStretch('str-hip-opener-90-90');
    addStretch('str-glute-bridge-activation');
    addStretch('str-deep-squat-pry');
  } else {
    addStretch('str-arm-circles-dynamic');
    addStretch('str-worlds-greatest-stretch');
    addStretch('str-deep-squat-pry');
    addStretch('str-cat-cow-mobility');
  }

  const safeFallbacks = ['str-worlds-greatest-stretch', 'str-cat-cow-mobility', 'str-deep-squat-pry', 'str-arm-circles-dynamic', 'str-bird-dog-activation'];
  for(const fid of safeFallbacks){
    if(selectedDrillIds.length >= 4) break;
    addStretch(fid);
  }

  const typeLabels = {
    'warmup_drill': 'إحماء تحضيري',
    'joint_mobility': 'مرونة مفصلية',
    'activation': 'تنشيط عضلي',
    'dynamic_stretch': 'إطالة ديناميكية',
    'static_stretch': 'إطالة ثابتة'
  };

  const dynamicSteps = selectedDrillIds.map(id => {
    const s = catalog.find(item => item.id === id);
    if(!s) return null;
    return {
      id: s.id,
      category: 'dynamic',
      categoryLabel: typeLabels[s.type] || 'حركة تحضيرية',
      nameAr: s.nameAr || s.name,
      name: s.name,
      target: (s.primaryMuscles || []).join('، ') || (s.bodyRegions || []).join('، '),
      durationOrReps: s.recommendedReps || (s.durationSeconds ? (s.durationSeconds + ' ثانية') : '10-12 تكرار'),
      typeBadge: typeLabels[s.type] || 'تحضير حركي',
      equipment: s.equipment === 'none' ? 'بدون أجهزة' : (s.equipment === 'band' ? 'حزام مقاومة (باند)' : (s.equipment === 'wall' ? 'حائط' : 'مفرش تمرين')),
      image: s.image,
      steps: s.instructions || [],
      cue: s.safetyNotes || s.breathing || ''
    };
  }).filter(Boolean);

  const warmupSetsExercises = [];
  const primaryCompoundCandidates = compoundExercises.slice(0, 2);
  if(primaryCompoundCandidates.length === 0 && routineExList.length > 0){
    primaryCompoundCandidates.push(routineExList[0]);
    if(routineExList.length > 1 && !routineExList[1].optional) primaryCompoundCandidates.push(routineExList[1]);
  }

  primaryCompoundCandidates.forEach(ex => {
    const exKey = ex.key || ex.catalogExerciseId || ex.templateExerciseId || 'ex';
    const exName = ex.name || 'التمرين الأول';
    warmupSetsExercises.push({
      exKey: exKey,
      exName: exName,
      sets: [
        {
          setNum: 1,
          id: `wset_${exKey}_1`,
          desc: 'المجموعة 1: البار فاضي أو وزن خفيف (40-50% من وزن التشغيل)',
          reps: '10-12 تكرار متحكم'
        },
        {
          setNum: 2,
          id: `wset_${exKey}_2`,
          desc: 'المجموعة 2: وزن متوسط (65-75% من وزن التشغيل)',
          reps: '5-6 تكرارات لتهيئة العضلات'
        },
        {
          setNum: 3,
          id: `wset_${exKey}_3`,
          desc: 'المجموعة 3: وزن شبه عملي (80-85% من وزن التشغيل)',
          reps: '2-3 تكرارات لإيقاظ الجهاز العصبي'
        }
      ]
    });
  });

  return {
    routineId: routineId,
    routineName: (effDay && effDay.routineName) ? effDay.routineName : (routineId === 'A' ? 'تمرينة A' : (routineId === 'B' ? 'تمرينة B' : routineId)),
    estimatedMinutes: '7-10 دقائق',
    generalCardio: cardioStep,
    dynamicDrills: dynamicSteps,
    warmupSets: warmupSetsExercises,
    totalStepsCount: 1 + dynamicSteps.length + warmupSetsExercises.reduce((acc, curr) => acc + curr.sets.length, 0)
  };
}

function renderInteractiveWarmupCard(targetEl, effOverride){
  const container = targetEl || document.getElementById('gymInteractiveWarmupContainer');
  if(!container) return;

  const iso = (typeof weekDates !== 'undefined' && Array.isArray(weekDates) && weekDates[selectedIdx])
    ? toISO(weekDates[selectedIdx])
    : (new Date().toISOString().slice(0, 10));

  const eff = effOverride || ((typeof getEffectiveGymDay === 'function') ? getEffectiveGymDay(iso, selectedIdx) : null);

  if(!eff || eff.isRest || eff.gymType === 'rest' || !eff.gym){
    container.innerHTML = '';
    return;
  }

  const routineId = eff.routineId || eff.gymType;
  const warmupPlan = generateRoutineWarmupPlan(routineId, eff);
  if(!warmupPlan){
    container.innerHTML = '';
    return;
  }

  let state = loadGymWarmupState(iso, routineId);
  if(!state){
    state = {
      iso: iso,
      routineId: routineId,
      started: false,
      completed: false,
      skipped: false,
      collapsed: false,
      completedDrills: {},
      completedWarmupSets: {}
    };
  }

  const completedDrills = state.completedDrills || {};
  const completedWarmupSets = state.completedWarmupSets || {};

  const allDrills = [warmupPlan.generalCardio].concat(warmupPlan.dynamicDrills);
  const totalDrillsCount = allDrills.length;
  let doneDrillsCount = 0;
  allDrills.forEach(d => {
    if(completedDrills[d.id]) doneDrillsCount++;
  });

  let totalSetsCount = 0;
  let doneSetsCount = 0;
  (warmupPlan.warmupSets || []).forEach(ex => {
    (ex.sets || []).forEach(s => {
      totalSetsCount++;
      if(completedWarmupSets[s.id]) doneSetsCount++;
    });
  });

  const totalSteps = totalDrillsCount + totalSetsCount;
  const doneSteps = doneDrillsCount + doneSetsCount;
  const percent = totalSteps > 0 ? Math.min(100, Math.round((doneSteps / totalSteps) * 100)) : 0;
  const isAllDone = totalSteps > 0 && doneSteps === totalSteps;

  let status = 'not_started';
  let statusLabel = 'لم يبدأ';
  if(state.skipped){
    status = 'skipped';
    statusLabel = 'تم التخطي ⏭️';
  } else if(state.completed || isAllDone){
    status = 'completed';
    statusLabel = 'مكتمل ✓';
  } else if(doneSteps > 0 || state.started){
    status = 'in_progress';
    statusLabel = 'جاري الإحماء ⏱️';
  }

  const isCollapsed = !!state.collapsed;
  const remainingCount = Math.max(0, totalSteps - doneSteps);

  let html = `
    <div class="gw-card status-${status}">
      <div class="gw-header">
        <div class="gw-title-area">
          <span style="font-size:1.25rem;">🔥</span>
          <div class="gw-title">إحماء ما قبل التمرين: ${escapeHtml(warmupPlan.routineName)}</div>
        </div>
        <span class="gw-status-badge status-${status}">${statusLabel}</span>
      </div>

      <div class="gw-meta-chips">
        <div class="gw-chip gw-routine-badge">📋 الروتين: <strong>${escapeHtml(warmupPlan.routineName)}</strong></div>
        <div class="gw-chip gw-duration-badge">⏱️ المدة التقديرية: <strong>${escapeHtml(warmupPlan.estimatedMinutes)}</strong></div>
        <div class="gw-chip">🎯 المنجز: <strong>${doneSteps}/${totalSteps} (${percent}%)</strong></div>
        ${remainingCount > 0 ? `<div class="gw-chip" style="color:var(--accent);">متبقي: <strong>${remainingCount}</strong></div>` : ''}
      </div>

      <div class="gw-progress-wrap">
        <div class="gw-progress-bar"><div class="gw-progress-fill" style="width:${percent}%;"></div></div>
      </div>

      <div class="gw-actions-bar">
        <button type="button" class="gw-btn" id="btnGwToggleExpand" title="${isCollapsed ? 'توسيع عرض الحركات' : 'طي عرض الحركات'}">
          ${isCollapsed ? 'عرض الحركات 🔽' : 'طي التفاصيل 🔼'}
        </button>
        ${!state.completed && !isAllDone ? `
          <button type="button" class="gw-btn gw-btn-good" id="btnGwCompleteAll">
            إنهاء الإحماء ✓
          </button>
        ` : ''}
        ${!state.skipped && !state.completed ? `
          <button type="button" class="gw-btn" id="btnGwSkip">
            تخطي الإحماء ⏭️
          </button>
        ` : ''}
        <button type="button" class="gw-btn gw-btn-subtle" id="btnGwReset">
          إعادة تعيين 🔄
        </button>
      </div>
  `;

  if(!isCollapsed){
    html += `<div class="gw-drills-list" id="gwDrillsList">`;

    const cardio = warmupPlan.generalCardio;
    const cardioDone = !!completedDrills[cardio.id];
    html += `
      <div class="gw-drill-item ${cardioDone ? 'done' : ''}" data-drill-id="${cardio.id}">
        <div class="gw-drill-thumb">
          <img loading="lazy" src="${cardio.image}" alt="${escapeHtml(cardio.nameAr)}" onerror="this.style.display='none';">
        </div>
        <div class="gw-drill-content">
          <div class="gw-drill-header">
            <div class="gw-drill-title-wrap">
              <div class="gw-drill-name-ar">١. ${escapeHtml(cardio.nameAr)}</div>
              <div class="gw-drill-name-en">${escapeHtml(cardio.name)}</div>
              <div class="gw-drill-badges">
                <span class="gw-drill-badge accent">${cardio.typeBadge}</span>
                <span class="gw-drill-badge">🎯 ${escapeHtml(cardio.target)}</span>
                <span class="gw-drill-badge">⏱️ ${escapeHtml(cardio.durationOrReps)}</span>
              </div>
            </div>
            <button type="button" class="gw-toggle-btn ${cardioDone ? 'done' : ''}" data-action="toggle-drill" data-drill-id="${cardio.id}">
              ${cardioDone ? 'تم ✓' : '✓ إكمال'}
            </button>
          </div>
          <ul class="gw-drill-steps">
            ${cardio.steps.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
          </ul>
          ${cardio.cue ? `<div class="gw-drill-cue">💡 ${escapeHtml(cardio.cue)}</div>` : ''}
        </div>
      </div>
    `;

    warmupPlan.dynamicDrills.forEach((drill, idx) => {
      const dDone = !!completedDrills[drill.id];
      const stepNum = idx + 2;
      html += `
        <div class="gw-drill-item ${dDone ? 'done' : ''}" data-drill-id="${drill.id}">
          <div class="gw-drill-thumb">
            <img loading="lazy" src="${drill.image}" alt="${escapeHtml(drill.nameAr)}" onerror="this.style.display='none';">
          </div>
          <div class="gw-drill-content">
            <div class="gw-drill-header">
              <div class="gw-drill-title-wrap">
                <div class="gw-drill-name-ar">${stepNum}. ${escapeHtml(drill.nameAr)}</div>
                <div class="gw-drill-name-en">${escapeHtml(drill.name)}</div>
                <div class="gw-drill-badges">
                  <span class="gw-drill-badge accent">${drill.typeBadge}</span>
                  <span class="gw-drill-badge">🎯 ${escapeHtml(drill.target)}</span>
                  <span class="gw-drill-badge">🔄 ${escapeHtml(drill.durationOrReps)}</span>
                  <span class="gw-drill-badge">📦 ${escapeHtml(drill.equipment)}</span>
                </div>
              </div>
              <button type="button" class="gw-toggle-btn ${dDone ? 'done' : ''}" data-action="toggle-drill" data-drill-id="${drill.id}">
                ${dDone ? 'تم ✓' : '✓ إكمال'}
              </button>
            </div>
            <ul class="gw-drill-steps">
              ${(drill.steps || []).map(s => `<li>${escapeHtml(s)}</li>`).join('')}
            </ul>
            ${drill.cue ? `<div class="gw-drill-cue">💡 ${escapeHtml(drill.cue)}</div>` : ''}
          </div>
        </div>
      `;
    });

    if(warmupPlan.warmupSets && warmupPlan.warmupSets.length > 0){
      html += `
        <div class="gw-warmup-sets-box">
          <div class="gw-sets-ex-header">
            <span>🏋️</span> مجموعات تمهيدية للتمارين الأساسية (سيتات تسخين تدريجية)
          </div>
      `;

      warmupPlan.warmupSets.forEach(ex => {
        html += `
          <div style="margin-bottom:8px;">
            <div style="font-weight:700; font-size:.85rem; color:var(--text); margin-bottom:4px;">
              🔹 ${escapeHtml(ex.exName)}
            </div>
        `;
        ex.sets.forEach(s => {
          const sDone = !!completedWarmupSets[s.id];
          html += `
            <div class="gw-set-row">
              <div class="gw-set-info">
                <div class="gw-set-desc">${escapeHtml(s.desc)}</div>
                <div class="gw-set-reps">${escapeHtml(s.reps)}</div>
              </div>
              <button type="button" class="gw-set-chip ${sDone ? 'done' : ''}" data-action="toggle-set" data-set-id="${s.id}">
                ${sDone ? 'تم ✓' : 'سيت تمهيدي'}
              </button>
            </div>
          `;
        });
        html += `</div>`;
      });

      html += `
          <div class="gw-sets-notice">
            <span>ℹ️</span> مجموعات التسخين لا تُسجّل ضمن مجموعات العمل في سجل التمرين، ولا تؤثر على الحجم التدريبي أو الأرقام القياسية.
          </div>
        </div>
      `;
    }

    html += `</div>`;
  }

  if(state.completed || isAllDone){
    const session = (typeof getGymSession === 'function') ? getGymSession(iso) : null;
    const isSessionActive = session && session.status === 'in_progress';
    const isSessionDone = session && session.status === 'completed';

    html += `
      <div class="gw-ready-banner">
        <div class="gw-ready-text-wrap">
          <div class="gw-ready-icon">💪</div>
          <div>
            <div class="gw-ready-title">عاش يا بطل! عضلاتك ومفاصلك مهيأة لبدء الحصة</div>
            <div class="gw-ready-sub">أكملت التحضير الحركي والإحماء بنجاح. ابدأ الجلسة لمتابعة وقت التدريب وتسجيل أوزانك.</div>
          </div>
        </div>
        ${!isSessionActive && !isSessionDone ? `
          <button type="button" class="btn-session-start gw-btn-start-session" id="btnGwStartSession">
            ▶️ بدء جلسة التمرين الآن
          </button>
        ` : (isSessionActive ? `
          <span style="font-weight:700; color:var(--good); font-size:.88rem;">⏱️ جلسة التدريب جارية الآن!</span>
        ` : `
          <span style="font-weight:700; color:var(--accent); font-size:.88rem;">🏆 الجلسة مكتملة</span>
        `)}
      </div>
    `;
  }

  html += `</div>`;
  container.innerHTML = html;

  const toggleExpandBtn = container.querySelector('#btnGwToggleExpand');
  if(toggleExpandBtn){
    toggleExpandBtn.addEventListener('click', () => {
      state.collapsed = !state.collapsed;
      saveGymWarmupState(iso, state);
      renderInteractiveWarmupCard(container, eff);
    });
  }

  const completeAllBtn = container.querySelector('#btnGwCompleteAll');
  if(completeAllBtn){
    completeAllBtn.addEventListener('click', () => {
      state.completed = true;
      state.skipped = false;
      state.started = true;
      allDrills.forEach(d => { state.completedDrills[d.id] = true; });
      (warmupPlan.warmupSets || []).forEach(ex => {
        (ex.sets || []).forEach(s => { state.completedWarmupSets[s.id] = true; });
      });
      saveGymWarmupState(iso, state);
      renderInteractiveWarmupCard(container, eff);
    });
  }

  const skipBtn = container.querySelector('#btnGwSkip');
  if(skipBtn){
    skipBtn.addEventListener('click', () => {
      state.skipped = true;
      state.completed = false;
      saveGymWarmupState(iso, state);
      renderInteractiveWarmupCard(container, eff);
    });
  }

  const resetBtn = container.querySelector('#btnGwReset');
  if(resetBtn){
    resetBtn.addEventListener('click', () => {
      state.completed = false;
      state.skipped = false;
      state.started = false;
      state.completedDrills = {};
      state.completedWarmupSets = {};
      saveGymWarmupState(iso, state);
      renderInteractiveWarmupCard(container, eff);
    });
  }

  container.querySelectorAll('[data-action="toggle-drill"]').forEach(btn => {
    btn.addEventListener('click', () => {
      const drillId = btn.getAttribute('data-drill-id');
      if(!drillId) return;
      state.started = true;
      if(state.completedDrills[drillId]){
        delete state.completedDrills[drillId];
        state.completed = false;
      } else {
        state.completedDrills[drillId] = true;
      }
      state.skipped = false;
      saveGymWarmupState(iso, state);
      renderInteractiveWarmupCard(container, eff);
    });
  });

  container.querySelectorAll('[data-action="toggle-set"]').forEach(btn => {
    btn.addEventListener('click', () => {
      const setId = btn.getAttribute('data-set-id');
      if(!setId) return;
      state.started = true;
      if(state.completedWarmupSets[setId]){
        delete state.completedWarmupSets[setId];
        state.completed = false;
      } else {
        state.completedWarmupSets[setId] = true;
      }
      state.skipped = false;
      saveGymWarmupState(iso, state);
      renderInteractiveWarmupCard(container, eff);
    });
  });

  const startSessionBtn = container.querySelector('#btnGwStartSession');
  if(startSessionBtn){
    startSessionBtn.addEventListener('click', () => {
      if(typeof startGymSession === 'function'){
        startGymSession(iso);
      }
      renderInteractiveWarmupCard(container, eff);
    });
  }
}

// Window exposures
window.generateRoutineWarmupPlan = generateRoutineWarmupPlan;
window.loadGymWarmupState = loadGymWarmupState;
window.saveGymWarmupState = saveGymWarmupState;
window.renderInteractiveWarmupCard = renderInteractiveWarmupCard;
"""

# Update renderWarmup
old_render_warmup = """function renderWarmup(){
  const iso = toISO(weekDates[selectedIdx]);
  renderImageChecklist('warmup', WARMUP, warmupState, (key)=>{
    if(warmupState[key]) delete warmupState[key]; else warmupState[key] = true;
    saveWarmup(iso, warmupState);
    renderWarmup();
  });
}"""

new_render_warmup = """function renderWarmup(){
  const iso = toISO(weekDates[selectedIdx]);
  renderImageChecklist('warmup', WARMUP, warmupState, (key)=>{
    if(warmupState[key]) delete warmupState[key]; else warmupState[key] = true;
    saveWarmup(iso, warmupState);
    renderWarmup();
  });
  renderInteractiveWarmupCard();
}"""

if old_render_warmup in content:
    content = content.replace(old_render_warmup, new_render_warmup + "\n" + js_warmup_code, 1)
    print("3. Injected JS warmup logic and updated renderWarmup()")
elif "function generateRoutineWarmupPlan(" in content:
    print("3. JS warmup logic already present")
else:
    print("3. WARNING: Could not find old_render_warmup target")

# ─────────────────────────────────────────────────────────────
# 4. Call renderInteractiveWarmupCard in renderExercises()
# ─────────────────────────────────────────────────────────────
old_render_ex_hook = """  renderGymSessionCard();
  renderRestTimerCard();"""

new_render_ex_hook = """  renderGymSessionCard();
  renderRestTimerCard();
  renderInteractiveWarmupCard();"""

if old_render_ex_hook in content and new_render_ex_hook not in content:
    content = content.replace(old_render_ex_hook, new_render_ex_hook, 1)
    print("4. Added renderInteractiveWarmupCard() call to renderExercises()")
else:
    print("4. renderInteractiveWarmupCard() already hooked into renderExercises()")

# ─────────────────────────────────────────────────────────────
# 5. Update validateBackupData with gym-warmup-state-v1
# ─────────────────────────────────────────────────────────────
old_known_keys = "/^shopping-purchases-v1$/, /^zatoona-media-v1$/, /^media$/];"
new_known_keys = "/^shopping-purchases-v1$/, /^gym-warmup-state-v1$/, /^zatoona-media-v1$/, /^media$/];"

if old_known_keys in content:
    content = content.replace(old_known_keys, new_known_keys, 1)
    print("5. Added gym-warmup-state-v1 to KNOWN_KEY_PATTERNS")
else:
    print("5. gym-warmup-state-v1 already in KNOWN_KEY_PATTERNS or pattern not found")

deep_val_hook = """  // Deep validation of gym-warmup-state-v1 if present in backup
  if(data['gym-warmup-state-v1'] !== undefined && data['gym-warmup-state-v1'] !== null){
    let wMap = data['gym-warmup-state-v1'];
    if(typeof wMap === 'string'){
      try {
        wMap = JSON.parse(wMap);
      } catch(e){
        return { ok: false, reason: 'ملف النسخة الاحتياطية يحتوي على سجلات إحماء تالفة (JSON غير صالح).' };
      }
    }
    if(!wMap || typeof wMap !== 'object' || Array.isArray(wMap)){
      return { ok: false, reason: 'بنية سجلات الإحماء غير صالحة.' };
    }
    for(const k of Object.keys(wMap)){
      if(!/^\\d{4}-\\d{2}-\\d{2}$/.test(k)){
        return { ok: false, reason: `مفتاح سجل الإحماء ${k} غير صالح (يجب أن يكون تاريخ YYYY-MM-DD).` };
      }
      const item = wMap[k];
      if(!item || typeof item !== 'object' || Array.isArray(item)){
        return { ok: false, reason: `سجل الإحماء للتاريخ ${k} غير صالح.` };
      }
    }
  }
"""

if "Deep validation of gym-warmup-state-v1" not in content:
    content = content.replace("  // Deep validation of gym-sessions-v1", deep_val_hook + "\n  // Deep validation of gym-sessions-v1", 1)
    print("6. Added deep validation of gym-warmup-state-v1 in validateBackupData()")
else:
    print("6. Deep validation already present")

# Write to index.html and zatoona.html byte-identically
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

with open(ZATOONA_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("\nSaved index.html and zatoona.html successfully.")

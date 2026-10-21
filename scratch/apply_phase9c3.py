import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO, "index.html")
ZATOONA_PATH = os.path.join(REPO, "zatoona.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────
# 1. Update HTML markup for Section 4 in #gymWorkoutBlock
# ─────────────────────────────────────────────────────────────
old_html_cooldown = """      <div class="section-title"><span class="n">٤</span> تبريد واسترتش <span style="color:var(--muted); font-weight:400;">(اختياري)</span></div>
      <div class="checklist" id="cooldown"></div>"""

new_html_cooldown = """      <div class="section-title"><span class="n">٤</span> تبريد واسترتش بعد التمرين <span style="color:var(--muted); font-weight:400;">(اختياري)</span></div>
      <div class="section-hint" id="cdSectionHint">تهدئة تدريجية واستطالة ثابتة مخصصة للعضلات التي تم تمرينها في حصة اليوم</div>
      <div id="gymInteractiveCooldownContainer" style="margin-bottom:14px;"></div>
      <div class="checklist" id="cooldown" style="display:none;"></div>"""

if old_html_cooldown in content:
    content = content.replace(old_html_cooldown, new_html_cooldown, 1)
    print("1. Injected #gymInteractiveCooldownContainer into Section 4")
elif 'id="gymInteractiveCooldownContainer"' in content:
    print("1. #gymInteractiveCooldownContainer already present")
else:
    print("1. WARNING: Could not find old_html_cooldown target")

# ─────────────────────────────────────────────────────────────
# 2. Update renderGymSessionCard completed state actions row
# ─────────────────────────────────────────────────────────────
old_session_completed_actions = """        <div class="session-actions-row">
          <button type="button" class="btn-session-restart" id="btnRestartGymSession">
            🔄 بدء جلسة جديدة لهذا اليوم
          </button>
        </div>"""

new_session_completed_actions = """        <div class="session-actions-row">
          <button type="button" class="btn-session-finish" id="btnStartGymCooldown" style="background:var(--accent); border-color:var(--accent);">
            🧘 بدء التهدئة والاستطالة بعد التمرين
          </button>
          <button type="button" class="btn-session-restart" id="btnRestartGymSession">
            🔄 بدء جلسة جديدة لهذا اليوم
          </button>
        </div>"""

if old_session_completed_actions in content:
    content = content.replace(old_session_completed_actions, new_session_completed_actions, 1)
    print("2. Added #btnStartGymCooldown to completed session actions row")
else:
    print("2. #btnStartGymCooldown already present in completed session actions row")

# Wire #btnStartGymCooldown inside renderGymSessionCard
old_session_binds = """  const btnRestart = container.querySelector('#btnRestartGymSession');
  if(btnRestart){
    btnRestart.addEventListener('click', ()=>{
      restartGymSession(iso);
    });
  }"""

new_session_binds = """  const btnRestart = container.querySelector('#btnRestartGymSession');
  if(btnRestart){
    btnRestart.addEventListener('click', ()=>{
      restartGymSession(iso);
    });
  }

  const btnCdStart = container.querySelector('#btnStartGymCooldown');
  if(btnCdStart){
    btnCdStart.addEventListener('click', ()=>{
      const cdEl = document.getElementById('gymInteractiveCooldownContainer');
      if(cdEl){
        cdEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        const toggleBtn = cdEl.querySelector('#btnCdToggleExpand');
        if(toggleBtn && toggleBtn.textContent.includes('عرض')){
          toggleBtn.click();
        }
      }
    });
  }"""

if old_session_binds in content and "btnStartGymCooldown" not in content.split("const btnRestart = container.querySelector('#btnRestartGymSession');")[1][:300]:
    content = content.replace(old_session_binds, new_session_binds, 1)
    print("2b. Wired #btnStartGymCooldown click event in renderGymSessionCard()")

# ─────────────────────────────────────────────────────────────
# 3. Add JS Cooldown Logic
# ─────────────────────────────────────────────────────────────
js_cooldown_code = """
/* ================= POST-WORKOUT INTERACTIVE COOL-DOWN (Phase 9C.3) ================= */
const GYM_COOLDOWN_STORAGE_KEY = 'gym-cooldown-state-v1';

function loadGymCooldownState(sessionId, iso, expectedRoutineId){
  const key = sessionId || (iso ? ('iso_' + iso) : null);
  if(!key) return null;
  try {
    const raw = storageGetJSON(GYM_COOLDOWN_STORAGE_KEY, {});
    const rec = raw[key] || null;
    if(rec && expectedRoutineId && rec.routineId && rec.routineId !== expectedRoutineId){
      return {
        sessionId: sessionId || null,
        iso: iso || null,
        routineId: expectedRoutineId,
        started: false,
        completed: false,
        skipped: false,
        collapsed: false,
        completedDrills: {},
        updatedAt: Date.now()
      };
    }
    return rec;
  } catch(e) {
    console.warn('[GymCooldown] Error loading state:', e);
    return null;
  }
}

function saveGymCooldownState(sessionId, iso, state){
  const key = sessionId || (iso ? ('iso_' + iso) : null);
  if(!key || !state) return false;
  try {
    const raw = storageGetJSON(GYM_COOLDOWN_STORAGE_KEY, {});
    raw[key] = Object.assign({}, raw[key] || {}, state, {
      sessionId: sessionId || (raw[key] && raw[key].sessionId) || null,
      iso: iso || (raw[key] && raw[key].iso) || null,
      updatedAt: Date.now()
    });
    storageSet(GYM_COOLDOWN_STORAGE_KEY, JSON.stringify(raw));
    return true;
  } catch(e) {
    console.warn('[GymCooldown] Error saving state:', e);
    return false;
  }
}

function generateRoutineCooldownPlan(routineId, session, exStateOverride){
  const catalog = (typeof window !== 'undefined' && Array.isArray(window.ZATOONA_STRETCH_CATALOG))
    ? window.ZATOONA_STRETCH_CATALOG
    : [];

  // Crucial: Use session's locked routineId first, not just active plan
  const targetRoutineId = (session && session.routineId) ? session.routineId : routineId;
  const targetRoutineName = (session && session.routineName)
    ? session.routineName
    : (targetRoutineId === 'A' ? 'تمرينة A' : (targetRoutineId === 'B' ? 'تمرينة B' : targetRoutineId));

  // Step 1: Calm walk / cardiovascular recovery
  const calmWalkStep = {
    id: 'cooldown-calm-walk',
    category: 'recovery_walk',
    categoryLabel: 'تهدئة حركية',
    nameAr: 'مشي هادئ لخفض النبض وعودة التنفس',
    name: 'Calm Cardiovascular Recovery Walk',
    target: 'خفض نبض القلب تدريجيًا، تهدئة الجهاز العصبي، ومنع تجمع الدم في الأطراف',
    durationOrReps: '2-3 دقائق',
    typeBadge: 'تهدئة حركية',
    equipment: 'بدون أجهزة',
    image: './assets/images/cooldown/cooldown-06-calm-walk.svg',
    steps: [
      'امشِ بخطوات هادئة وبطيئة ومريحة داخل الصالة أو في مكان جيد التهوية.',
      'ركّز على التنفس العميق والبطيء: شهيق من الأنف في 4 ثوانٍ وزفير مريح من الفم في 4 ثوانٍ.',
      'الهدف هو خفض ضربات القلب تدريجيًا ومساعدة العضلات على التخلص من حمض اللاكتيك.'
    ],
    cue: 'لا تجلس أو تستلقِ مباشرة بعد آخر مجموعة شاقة — المشي الهادئ أساسي للتعافي.'
  };

  const routineExList = (typeof getRoutineExercises === 'function') ? getRoutineExercises(targetRoutineId) : [];
  const iso = (session && session.iso) ? session.iso : (typeof weekDates !== 'undefined' && weekDates[selectedIdx] ? toISO(weekDates[selectedIdx]) : '');
  const activeExState = exStateOverride || ((typeof weekDates !== 'undefined' && iso === toISO(weekDates[selectedIdx])) ? exState : ((typeof loadEx === 'function') ? loadEx(iso) : {}));

  const targetedMuscles = new Set();
  let hasUpper = false, hasLower = false, hasPress = false, hasPull = false, hasLegs = false, hasHinge = false;

  const exCatalog = (typeof window !== 'undefined' && Array.isArray(window.ZATOONA_EXERCISE_CATALOG))
    ? window.ZATOONA_EXERCISE_CATALOG
    : [];
  const exCatalogMap = {};
  exCatalog.forEach(ex => { if(ex && ex.id) exCatalogMap[ex.id] = ex; });

  // Priority 1: Performed exercises with completed sets
  // Priority 2: Routine exercises
  routineExList.forEach(ex => {
    if(!ex) return;
    const catId = ex.catalogExerciseId || ex.key || '';
    const targetStr = ((ex.target || '') + ' ' + (ex.name || '')).toLowerCase();
    const st = activeExState ? activeExState[ex.key] : null;
    const wasPerformed = st && Array.isArray(st.sets) && st.sets.some(Boolean);

    const catEntry = exCatalogMap[catId];
    if(catEntry){
      (catEntry.primaryMuscles || []).forEach(m => targetedMuscles.add(m));
      (catEntry.secondaryMuscles || []).forEach(m => targetedMuscles.add(m));
    }

    if(/صدر|بنش|bench|chest|ضغط|push/i.test(targetStr)){ targetedMuscles.add('chest'); hasUpper = true; hasPress = true; }
    if(/كتف|شولدر|press|shoulder/i.test(targetStr)){ targetedMuscles.add('shoulders'); hasUpper = true; hasPress = true; }
    if(/ظهر|لاتس|سحب|عقلة|row|lat|pull/i.test(targetStr)){ targetedMuscles.add('lats'); hasUpper = true; hasPull = true; }
    if(/تراي|باي|ذراع|arm|triceps|biceps/i.test(targetStr)){ targetedMuscles.add('arms'); hasUpper = true; }
    if(/سكوات|squat|فخذ أمامي|أرجل|رجل|quad/i.test(targetStr)){ targetedMuscles.add('quads'); targetedMuscles.add('hips'); hasLower = true; hasLegs = true; }
    if(/ديدليفت|deadlift|rdl|فخذ خلفي|خلفيات|hamstring/i.test(targetStr)){ targetedMuscles.add('hamstrings'); targetedMuscles.add('glutes'); hasLower = true; hasHinge = true; }
    if(/مؤخرة|جلوتس|glute|ورك|حوض/i.test(targetStr)){ targetedMuscles.add('glutes'); targetedMuscles.add('hips'); hasLower = true; }
    if(/سمانة|كاحل|calf|ankle/i.test(targetStr)){ targetedMuscles.add('calves'); targetedMuscles.add('ankles'); hasLower = true; }
    if(/بطن|كرانش|بلانك|core|abs/i.test(targetStr)){ targetedMuscles.add('abs'); targetedMuscles.add('spine'); }
  });

  const rIdStr = String(targetRoutineId || '').toLowerCase();
  if(rIdStr === 'a'){ hasUpper = true; hasLower = true; hasPress = true; hasPull = true; hasLegs = true; }
  else if(rIdStr === 'b'){ hasUpper = true; hasLower = true; hasPull = true; hasHinge = true; hasPress = true; }
  else if(rIdStr.includes('push') || rIdStr.includes('chest')){ hasUpper = true; hasPress = true; }
  else if(rIdStr.includes('pull') || rIdStr.includes('back')){ hasUpper = true; hasPull = true; }
  else if(rIdStr.includes('leg') || rIdStr.includes('lower')){ hasLower = true; hasLegs = true; hasHinge = true; }
  else if(rIdStr.includes('upper')){ hasUpper = true; hasPress = true; hasPull = true; }
  else if(rIdStr.includes('fb') || rIdStr.includes('full')){ hasUpper = true; hasLower = true; }

  const selectedStretchIds = [];
  function addStretch(id){
    if(!selectedStretchIds.includes(id) && catalog.some(s => s.id === id)){
      selectedStretchIds.push(id);
    }
  }

  // Targeted Cooldown Selection
  if(rIdStr === 'a'){
    // A: Squat, Bench, Lat Pulldown, DB Press, Plank, Face Pull
    addStretch('str-doorway-pec-stretch');        // Chest
    addStretch('str-standing-quad-stretch');      // Quads / Squat
    addStretch('str-cross-body-shoulder-stretch');// Shoulders
    addStretch('str-lat-wall-stretch');           // Lats
    addStretch('str-childs-pose');                // Lower back & spine
  } else if(rIdStr === 'b'){
    // B: RDL, Barbell Row, Push-up, Pull-up, Crunch, Lunges
    addStretch('str-standing-hamstring-stretch'); // Hamstrings / RDL
    addStretch('str-pigeon-pose');                // Glutes
    addStretch('str-lat-wall-stretch');           // Lats / Row / Pull-up
    addStretch('str-doorway-pec-stretch');        // Chest / Push-up
    addStretch('str-cobra-lumbar-stretch');       // Abs / Crunch & spine
  } else if(hasLegs && !hasUpper){
    // Pure Legs / Lower
    addStretch('str-standing-quad-stretch');
    addStretch('str-standing-hamstring-stretch');
    addStretch('str-pigeon-pose');
    addStretch('str-wall-calf-stretch');
    addStretch('str-kneeling-hip-flexor');
  } else if(hasPress && !hasPull && !hasLower){
    // Pure Push
    addStretch('str-doorway-pec-stretch');
    addStretch('str-cross-body-shoulder-stretch');
    addStretch('str-upper-trap-stretch');
    addStretch('str-childs-pose');
  } else if(hasPull && !hasPress && !hasLower){
    // Pure Pull
    addStretch('str-lat-wall-stretch');
    addStretch('str-childs-pose');
    addStretch('str-cross-body-shoulder-stretch');
    addStretch('str-wrist-extensor-stretch');
  } else if(hasUpper && !hasLower){
    // Upper Body
    addStretch('str-doorway-pec-stretch');
    addStretch('str-cross-body-shoulder-stretch');
    addStretch('str-lat-wall-stretch');
    addStretch('str-childs-pose');
    addStretch('str-upper-trap-stretch');
  } else if(hasLower && !hasUpper){
    // Lower Body
    addStretch('str-standing-quad-stretch');
    addStretch('str-standing-hamstring-stretch');
    addStretch('str-pigeon-pose');
    addStretch('str-kneeling-hip-flexor');
    addStretch('str-wall-calf-stretch');
  } else {
    // Full Body or balanced / Custom routine
    addStretch('str-doorway-pec-stretch');
    addStretch('str-standing-hamstring-stretch');
    addStretch('str-childs-pose');
    addStretch('str-standing-quad-stretch');
    addStretch('str-pigeon-pose');
  }

  const safeFallbacks = ['str-childs-pose', 'str-standing-hamstring-stretch', 'str-doorway-pec-stretch', 'str-pigeon-pose', 'str-cross-body-shoulder-stretch', 'str-wall-calf-stretch'];
  for(const fid of safeFallbacks){
    if(selectedStretchIds.length >= 4) break;
    addStretch(fid);
  }

  const stretchSteps = selectedStretchIds.map(id => {
    const s = catalog.find(item => item.id === id);
    if(!s) return null;
    return {
      id: s.id,
      category: 'stretch',
      categoryLabel: s.type === 'static_stretch' ? 'إطالة ثابتة' : 'تهدئة حركية',
      nameAr: s.nameAr || s.name,
      name: s.name,
      target: (s.primaryMuscles || []).join('، ') || (s.bodyRegions || []).join('، '),
      durationOrReps: s.durationSeconds ? (s.durationSeconds + ' ثانية لكل جانب') : (s.recommendedReps || '20-30 ثانية'),
      typeBadge: s.type === 'static_stretch' ? 'إطالة ثابتة' : 'استطالة ومرونة',
      equipment: s.equipment === 'none' ? 'بدون أجهزة' : (s.equipment === 'wall' ? 'حائط' : 'مفرش تمرين'),
      image: s.image,
      steps: s.instructions || [],
      cue: s.safetyNotes || s.breathing || ''
    };
  }).filter(Boolean);

  return {
    routineId: targetRoutineId,
    routineName: targetRoutineName,
    sessionId: session ? session.id : null,
    estimatedMinutes: '5-7 دقائق',
    calmWalk: calmWalkStep,
    stretchDrills: stretchSteps,
    totalStepsCount: 1 + stretchSteps.length
  };
}

function renderInteractiveCooldownCard(targetEl, sessionOverride){
  const container = targetEl || document.getElementById('gymInteractiveCooldownContainer');
  if(!container) return;

  const iso = (typeof weekDates !== 'undefined' && Array.isArray(weekDates) && weekDates[selectedIdx])
    ? toISO(weekDates[selectedIdx])
    : (new Date().toISOString().slice(0, 10));

  const eff = (typeof getEffectiveGymDay === 'function') ? getEffectiveGymDay(iso, selectedIdx) : null;
  if(!eff || eff.isRest || eff.gymType === 'rest' || !eff.gym){
    container.innerHTML = '';
    return;
  }

  const session = sessionOverride || ((typeof getGymSession === 'function') ? getGymSession(iso) : null);
  const status = session ? session.status : 'not_started';

  // Case 1: Session not started
  if(!session || status === 'not_started'){
    container.innerHTML = `
      <div class="gw-card status-not_started">
        <div class="gw-header">
          <div class="gw-title-area">
            <span style="font-size:1.25rem;">🧘</span>
            <div class="gw-title">التهدئة والاستطالة بعد التمرين</div>
          </div>
          <span class="gw-status-badge status-not_started">متاحة بعد إنهاء التمرين ⏱️</span>
        </div>
        <div class="gw-drill-cue" style="padding:6px 0; font-size:.82rem;">
          مسار الاستطالة والتهدئة يُخصص تلقائيًا للعضلات التي ستدربها اليوم لمساعدة الجسم على الاسترخاء وخفض النبض. سيتاح هنا فور إنهاء جلسة اليوم.
        </div>
      </div>
    `;
    return;
  }

  // Case 2: Session in progress
  if(status === 'in_progress'){
    container.innerHTML = `
      <div class="gw-card status-in_progress">
        <div class="gw-header">
          <div class="gw-title-area">
            <span style="font-size:1.25rem;">🧘</span>
            <div class="gw-title">التهدئة والاستطالة بعد التمرين</div>
          </div>
          <span class="gw-status-badge status-in_progress">في انتظار إنهاء الحصة ⏱️</span>
        </div>
        <div class="gw-drill-cue" style="padding:6px 0; font-size:.82rem;">
          جلسة التمرين جارية الآن 🔥 — فور إنهائك للحصة، سيتم تجهيز مسار استطالة ثابتة وتهدئة مخصص للعضلات التي أنجزت تمرينها.
        </div>
      </div>
    `;
    return;
  }

  // Case 3: Session cancelled
  if(status === 'cancelled'){
    container.innerHTML = `
      <div class="gw-card status-skipped">
        <div class="gw-header">
          <div class="gw-title-area">
            <span style="font-size:1.25rem;">🧘</span>
            <div class="gw-title">التهدئة والاستطالة بعد التمرين</div>
          </div>
          <span class="gw-status-badge status-skipped">أُلغيت الجلسة ⛔</span>
        </div>
        <div class="gw-drill-cue" style="padding:6px 0; font-size:.82rem;">
          أُلغيت جلسة التمرين. مسار التهدئة يرتبط بالحصة المكتملة، ولكن يمكنك تصفح موسوعة الاسترتشات في أي وقت للاستطالة والمرونة.
        </div>
        <div style="margin-top:8px;">
          <button type="button" class="gw-btn" onclick="if(typeof navigateTo==='function') navigateTo('stretches');">
            📖 فتح موسوعة الاسترتشات والمرونة
          </button>
        </div>
      </div>
    `;
    return;
  }

  // Case 4: Session completed!
  const routineId = session.routineId || eff.routineId || eff.gymType;
  const cooldownPlan = generateRoutineCooldownPlan(routineId, session);
  if(!cooldownPlan){
    container.innerHTML = '';
    return;
  }

  const sessionId = session.id;
  let state = loadGymCooldownState(sessionId, iso, routineId);
  if(!state){
    state = {
      sessionId: sessionId,
      iso: iso,
      routineId: routineId,
      started: false,
      completed: false,
      skipped: false,
      collapsed: false,
      completedDrills: {}
    };
  }

  const completedDrills = state.completedDrills || {};
  const allDrills = [cooldownPlan.calmWalk].concat(cooldownPlan.stretchDrills);
  const totalSteps = allDrills.length;
  let doneSteps = 0;
  allDrills.forEach(d => {
    if(completedDrills[d.id]) doneSteps++;
  });

  const percent = totalSteps > 0 ? Math.min(100, Math.round((doneSteps / totalSteps) * 100)) : 0;
  const isAllDone = totalSteps > 0 && doneSteps === totalSteps;

  let cdStatus = 'not_started';
  let cdStatusLabel = 'جاهزة للبدء';
  if(state.skipped){
    cdStatus = 'skipped';
    cdStatusLabel = 'تم التخطي ⏭️';
  } else if(state.completed || isAllDone){
    cdStatus = 'completed';
    cdStatusLabel = 'مكتملة ✓';
  } else if(doneSteps > 0 || state.started){
    cdStatus = 'in_progress';
    cdStatusLabel = 'جاري التهدئة ⏱️';
  }

  const isCollapsed = !!state.collapsed;
  const remainingCount = Math.max(0, totalSteps - doneSteps);

  let html = `
    <div class="gw-card status-${cdStatus}">
      <div class="gw-header">
        <div class="gw-title-area">
          <span style="font-size:1.25rem;">🧘</span>
          <div class="gw-title">تهدئة واستطالة ما بعد التمرين: ${escapeHtml(cooldownPlan.routineName)}</div>
        </div>
        <span class="gw-status-badge status-${cdStatus}">${cdStatusLabel}</span>
      </div>

      <div class="gw-meta-chips">
        <div class="gw-chip">📋 الروتين: <strong>${escapeHtml(cooldownPlan.routineName)}</strong></div>
        <div class="gw-chip">⏱️ المدة التقديرية: <strong>${escapeHtml(cooldownPlan.estimatedMinutes)}</strong></div>
        <div class="gw-chip">🎯 المنجز: <strong>${doneSteps}/${totalSteps} (${percent}%)</strong></div>
        ${remainingCount > 0 ? `<div class="gw-chip" style="color:var(--accent);">متبقي: <strong>${remainingCount}</strong></div>` : ''}
      </div>

      <div class="gw-progress-wrap">
        <div class="gw-progress-bar"><div class="gw-progress-fill" style="width:${percent}%;"></div></div>
      </div>

      <div class="gw-actions-bar">
        <button type="button" class="gw-btn" id="btnCdToggleExpand" title="${isCollapsed ? 'توسيع عرض الحركات' : 'طي عرض الحركات'}">
          ${isCollapsed ? 'عرض الحركات 🔽' : 'طي التفاصيل 🔼'}
        </button>
        <button type="button" class="gw-btn gw-btn-good" id="btnCdCompleteAll">
          ${state.completed || isAllDone ? 'إعادة تأكيد الإكمال ✓' : 'إنهاء التهدئة ✓'}
        </button>
        <button type="button" class="gw-btn" id="btnCdSkip">
          تخطي التهدئة ⏭️
        </button>
        <button type="button" class="gw-btn gw-btn-subtle" id="btnCdReset">
          إعادة تعيين 🔄
        </button>
      </div>
  `;

  if(!isCollapsed){
    html += `<div class="gw-drills-list" id="cdDrillsList">`;

    // 1. Calm Walk
    const walk = cooldownPlan.calmWalk;
    const walkDone = !!completedDrills[walk.id];
    html += `
      <div class="gw-drill-item ${walkDone ? 'done' : ''}" data-drill-id="${walk.id}">
        <div class="gw-drill-thumb">
          <img loading="lazy" src="${walk.image}" alt="${escapeHtml(walk.nameAr)}" onerror="this.style.display='none';">
        </div>
        <div class="gw-drill-content">
          <div class="gw-drill-header">
            <div class="gw-drill-title-wrap">
              <div class="gw-drill-name-ar">١. ${escapeHtml(walk.nameAr)}</div>
              <div class="gw-drill-name-en">${escapeHtml(walk.name)}</div>
              <div class="gw-drill-badges">
                <span class="gw-drill-badge accent">${walk.typeBadge}</span>
                <span class="gw-drill-badge">🎯 ${escapeHtml(walk.target)}</span>
                <span class="gw-drill-badge">⏱️ ${escapeHtml(walk.durationOrReps)}</span>
              </div>
            </div>
            <button type="button" class="gw-toggle-btn ${walkDone ? 'done' : ''}" data-action="toggle-cd-drill" data-drill-id="${walk.id}">
              ${walkDone ? 'تم ✓' : '✓ إكمال'}
            </button>
          </div>
          <ul class="gw-drill-steps">
            ${walk.steps.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
          </ul>
          ${walk.cue ? `<div class="gw-drill-cue">💡 ${escapeHtml(walk.cue)}</div>` : ''}
        </div>
      </div>
    `;

    // 2. Targeted Static Stretches
    cooldownPlan.stretchDrills.forEach((drill, idx) => {
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
                  <span class="gw-drill-badge">⏱️ ${escapeHtml(drill.durationOrReps)}</span>
                  <span class="gw-drill-badge">📦 ${escapeHtml(drill.equipment)}</span>
                </div>
              </div>
              <button type="button" class="gw-toggle-btn ${dDone ? 'done' : ''}" data-action="toggle-cd-drill" data-drill-id="${drill.id}">
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

    html += `</div>`;
  }

  // Completion / Ready Banner
  if(state.completed || isAllDone){
    html += `
      <div class="gw-ready-banner" style="border-color:var(--accent); background:linear-gradient(135deg, rgba(2, 132, 199, 0.12), rgba(14, 165, 233, 0.06));">
        <div class="gw-ready-text-wrap">
          <div class="gw-ready-icon">🧘‍♂️</div>
          <div>
            <div class="gw-ready-title">استشفاء ممتاز! اكتملت التهدئة بنجاح</div>
            <div class="gw-ready-sub">أراحت عضلاتك ومفاصلك وبدأت مرحلة البناء والتعافي. يمكنك الآن تسجيل ملاحظات استشفائك اليومي.</div>
          </div>
        </div>
        <button type="button" class="gw-btn gw-btn-primary" id="btnGoToDailyRecovery" onclick="if(typeof navigateTo==='function') navigateTo('recovery');">
          📊 الانتقال إلى سجل الاستشفاء اليومي
        </button>
      </div>
    `;
  }

  html += `</div>`;
  container.innerHTML = html;

  // Bind Events
  const toggleExpandBtn = container.querySelector('#btnCdToggleExpand');
  if(toggleExpandBtn){
    toggleExpandBtn.addEventListener('click', () => {
      state.collapsed = !state.collapsed;
      saveGymCooldownState(sessionId, iso, state);
      renderInteractiveCooldownCard(container, session);
    });
  }

  const completeAllBtn = container.querySelector('#btnCdCompleteAll');
  if(completeAllBtn){
    completeAllBtn.addEventListener('click', () => {
      state.completed = true;
      state.skipped = false;
      state.started = true;
      allDrills.forEach(d => { state.completedDrills[d.id] = true; });
      saveGymCooldownState(sessionId, iso, state);
      renderInteractiveCooldownCard(container, session);
    });
  }

  const skipBtn = container.querySelector('#btnCdSkip');
  if(skipBtn){
    skipBtn.addEventListener('click', () => {
      state.skipped = true;
      state.completed = false;
      saveGymCooldownState(sessionId, iso, state);
      renderInteractiveCooldownCard(container, session);
    });
  }

  const resetBtn = container.querySelector('#btnCdReset');
  if(resetBtn){
    resetBtn.addEventListener('click', () => {
      state.completed = false;
      state.skipped = false;
      state.started = false;
      state.completedDrills = {};
      saveGymCooldownState(sessionId, iso, state);
      renderInteractiveCooldownCard(container, session);
    });
  }

  container.querySelectorAll('[data-action="toggle-cd-drill"]').forEach(btn => {
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
      saveGymCooldownState(sessionId, iso, state);
      renderInteractiveCooldownCard(container, session);
    });
  });
}

// Window exposures
window.generateRoutineCooldownPlan = generateRoutineCooldownPlan;
window.loadGymCooldownState = loadGymCooldownState;
window.saveGymCooldownState = saveGymCooldownState;
window.renderInteractiveCooldownCard = renderInteractiveCooldownCard;
"""

# Update renderCooldown
old_render_cooldown = """function renderCooldown(){
  const iso = toISO(weekDates[selectedIdx]);
  renderImageChecklist('cooldown', COOLDOWN, cooldownState, (key)=>{
    if(cooldownState[key]) delete cooldownState[key]; else cooldownState[key] = true;
    saveCooldown(iso, cooldownState);
    renderCooldown();
  });
}"""

new_render_cooldown = """function renderCooldown(){
  const iso = toISO(weekDates[selectedIdx]);
  renderImageChecklist('cooldown', COOLDOWN, cooldownState, (key)=>{
    if(cooldownState[key]) delete cooldownState[key]; else cooldownState[key] = true;
    saveCooldown(iso, cooldownState);
    renderCooldown();
  });
  renderInteractiveCooldownCard();
}"""

if old_render_cooldown in content:
    content = content.replace(old_render_cooldown, new_render_cooldown + "\n" + js_cooldown_code, 1)
    print("3. Injected JS cooldown logic and updated renderCooldown()")
elif "function generateRoutineCooldownPlan(" in content:
    print("3. JS cooldown logic already present")
else:
    print("3. WARNING: Could not find old_render_cooldown target")

# ─────────────────────────────────────────────────────────────
# 4. Call renderInteractiveCooldownCard in renderExercises()
# ─────────────────────────────────────────────────────────────
old_render_ex_hook = """  renderGymSessionCard();
  renderRestTimerCard();
  renderInteractiveWarmupCard();"""

new_render_ex_hook = """  renderGymSessionCard();
  renderRestTimerCard();
  renderInteractiveWarmupCard();
  renderInteractiveCooldownCard();"""

if old_render_ex_hook in content and new_render_ex_hook not in content:
    content = content.replace(old_render_ex_hook, new_render_ex_hook, 1)
    print("4. Added renderInteractiveCooldownCard() call to renderExercises()")
else:
    print("4. renderInteractiveCooldownCard() already hooked into renderExercises()")

# ─────────────────────────────────────────────────────────────
# 5. Update validateBackupData with gym-cooldown-state-v1
# ─────────────────────────────────────────────────────────────
old_known_keys = "/^gym-warmup-state-v1$/, /^zatoona-media-v1$/, /^media$/];"
new_known_keys = "/^gym-warmup-state-v1$/, /^gym-cooldown-state-v1$/, /^zatoona-media-v1$/, /^media$/];"

if old_known_keys in content:
    content = content.replace(old_known_keys, new_known_keys, 1)
    print("5. Added gym-cooldown-state-v1 to KNOWN_KEY_PATTERNS")
else:
    print("5. gym-cooldown-state-v1 already in KNOWN_KEY_PATTERNS or pattern not found")

deep_val_cooldown_hook = """  // Deep validation of gym-cooldown-state-v1 if present in backup
  if(data['gym-cooldown-state-v1'] !== undefined && data['gym-cooldown-state-v1'] !== null){
    let cMap = data['gym-cooldown-state-v1'];
    if(typeof cMap === 'string'){
      try {
        cMap = JSON.parse(cMap);
      } catch(e){
        return { ok: false, reason: 'ملف النسخة الاحتياطية يحتوي على سجلات تهدئة تالفة (JSON غير صالح).' };
      }
    }
    if(!cMap || typeof cMap !== 'object' || Array.isArray(cMap)){
      return { ok: false, reason: 'بنية سجلات التهدئة غير صالحة.' };
    }
    for(const k of Object.keys(cMap)){
      const item = cMap[k];
      if(!item || typeof item !== 'object' || Array.isArray(item)){
        return { ok: false, reason: `سجل التهدئة للجلسة ${k} غير صالح.` };
      }
    }
  }
"""

if "Deep validation of gym-cooldown-state-v1" not in content:
    content = content.replace("  // Deep validation of gym-warmup-state-v1", deep_val_cooldown_hook + "\n  // Deep validation of gym-warmup-state-v1", 1)
    print("6. Added deep validation of gym-cooldown-state-v1 in validateBackupData()")
else:
    print("6. Deep validation of gym-cooldown-state-v1 already present")

# Write to index.html and zatoona.html byte-identically
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

with open(ZATOONA_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("\nSaved index.html and zatoona.html byte-identically.")

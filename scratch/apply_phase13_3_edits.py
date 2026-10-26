# -*- coding: utf-8 -*-
"""
Phase 13.3 — Apply Healthy Sleep Habits & Bedtime Routine Edits
Applies targeted additions to index.html and replicates identically to zatoona.html.
"""
import os
import re

INDEX_PATH = r"C:\Users\Lenovo\Documents\GitHub\zatoona\index.html"
ZATOONA_PATH = r"C:\Users\Lenovo\Documents\GitHub\zatoona\zatoona.html"

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# -----------------------------------------------------------------------------
# 1. HTML: Update #sleepView structure
# -----------------------------------------------------------------------------
old_sleep_view = '''  <!-- ===== SLEEP MODE ===== -->
  <div id="sleepView" class="hidden">
    <div id="secNotes-sleep"></div>
    <div class="section-title"><span class="n">١</span> ملخص النوم</div>
    <div class="summary" id="sleepSummary"></div>

    <div class="section-title"><span class="n">٢</span> مواعيد النوم</div>
    <div class="water-card">
      <div class="water-info" style="flex:1;">
        <div class="wtitle">سجّل مواعيدك</div>
        <div class="wsub">هدف: 7-9 ساعات نوم متصلة</div>
        <div style="display:flex; gap:10px; margin-top:10px; flex-wrap:wrap;">
          <label style="flex:1; min-width:120px;">
            <div style="color:var(--muted); font-size:.72rem; margin-bottom:4px;">وقت النوم</div>
            <input type="time" id="sleepTimeStart" class="weight-input" style="width:100%;">
          </label>
          <label style="flex:1; min-width:120px;">
            <div style="color:var(--muted); font-size:.72rem; margin-bottom:4px;">وقت الصحيان</div>
            <input type="time" id="sleepTimeEnd" class="weight-input" style="width:100%;">
          </label>
        </div>
      </div>
    </div>

    <div class="section-title"><span class="n">٣</span> جودة النوم</div>
    <div class="checklist" id="sleepQuality"></div>

    <div class="section-title"><span class="n">٤</span> عادات نوم صحية</div>
    <div class="section-hint">علّم اللي التزمت بيه النهاردة</div>
    <div class="checklist" id="sleepHabits"></div>
  </div>'''

new_sleep_view = '''  <!-- ===== SLEEP MODE ===== -->
  <div id="sleepView" class="hidden">
    <div id="secNotes-sleep"></div>
    <div class="section-title"><span class="n">١</span> ملخص النوم</div>
    <div class="summary" id="sleepSummary"></div>

    <div class="section-title"><span class="n">٢</span> مواعيد النوم ومقارنة الهدف</div>
    <div class="water-card">
      <div class="water-info" style="flex:1;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <div>
            <div class="wtitle">سجّل مواعيدك الفعلية</div>
            <div class="wsub">هدف: 7-9 ساعات نوم متصلة، ومقارنة يومية مع هدفك المخطط</div>
          </div>
          <button type="button" class="reset-btn" id="btnToggleSleepRoutineSettings" style="font-size:.78rem; padding:4px 10px;">⚙️ إعدادات الهدف</button>
        </div>
        <div style="display:flex; gap:10px; margin-top:10px; flex-wrap:wrap;">
          <label style="flex:1; min-width:120px;">
            <div style="color:var(--muted); font-size:.72rem; margin-bottom:4px;">وقت النوم الفعلي</div>
            <input type="time" id="sleepTimeStart" class="weight-input" style="width:100%;">
          </label>
          <label style="flex:1; min-width:120px;">
            <div style="color:var(--muted); font-size:.72rem; margin-bottom:4px;">وقت الصحيان الفعلي</div>
            <input type="time" id="sleepTimeEnd" class="weight-input" style="width:100%;">
          </label>
        </div>
        <div id="sleepComparisonCard" style="margin-top:12px;"></div>
      </div>
    </div>

    <!-- Sleep Target & Routine Settings Panel -->
    <div id="sleepRoutineSettingsPanel" style="display:none; margin-top:12px; margin-bottom:14px;">
      <div class="card" style="background:var(--card-alt); border:1.5px solid var(--primary); border-radius:12px; padding:14px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="font-weight:700; font-size:.92rem; color:var(--text);">⚙️ إعدادات هدف النوم وروتين التهدئة المسائي</div>
          <button type="button" class="reset-btn" id="btnCloseSleepSettings" style="padding:2px 8px; font-size:.75rem;">✕ إغلاق</button>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:10px; margin-bottom:12px;">
          <label>
            <div style="font-size:.75rem; color:var(--muted); margin-bottom:4px;">هدف وقت النوم:</div>
            <input type="time" id="setTargetBedtime" class="weight-input" style="width:100%;">
          </label>
          <label>
            <div style="font-size:.75rem; color:var(--muted); margin-bottom:4px;">هدف وقت الصحيان:</div>
            <input type="time" id="setTargetWakeTime" class="weight-input" style="width:100%;">
          </label>
          <label>
            <div style="font-size:.75rem; color:var(--muted); margin-bottom:4px;">بدء التهدئة قبل النوم بـ:</div>
            <select id="setWindDownLeadMin" class="weight-input" style="width:100%; padding:6px;">
              <option value="15">15 دقيقة</option>
              <option value="30">30 دقيقة (افتراضي)</option>
              <option value="45">45 دقيقة</option>
              <option value="60">60 دقيقة</option>
            </select>
          </label>
        </div>

        <div style="margin-bottom:12px;">
          <div style="font-size:.75rem; color:var(--muted); margin-bottom:6px;">أيام تفعيل الروتين:</div>
          <div class="day-toggle-row" id="sleepActiveDaysRow" style="margin-bottom:6px;"></div>
        </div>

        <div style="display:flex; align-items:center; justify-content:space-between; padding:8px 10px; background:var(--card); border-radius:8px; border:1px solid var(--line); margin-bottom:8px;">
          <span style="font-size:.82rem; font-weight:600;">تنبيه بدء روتين التهدئة</span>
          <button type="button" class="tbtn" id="toggleWindDownReminder">✓</button>
        </div>
        <div style="font-size:.72rem; color:var(--muted); line-height:1.4;">
          ⚠️ ملاحظة: التنبيهات تعمل أثناء فتح التطبيق أو تشغيله بالخلفية. التنبيه مع إغلاق المتصفح تمامًا سيتم دعمه في مرحلة معمارية قادمة.
        </div>

        <div style="margin-top:12px; text-align:left;">
          <button type="button" class="save-btn" id="btnSaveSleepRoutineSettings" style="padding:6px 16px; font-size:.82rem;">حفظ الإعدادات</button>
        </div>
      </div>
    </div>

    <div class="section-title"><span class="n">٣</span> روتين التهدئة المسائي</div>
    <div class="section-hint">خطوات مهدئة تساعدك تستعد للنوم بجودة أعلى</div>
    <div class="checklist" id="windDownRoutineChecklist"></div>

    <div class="section-title"><span class="n">٤</span> جودة النوم</div>
    <div class="checklist" id="sleepQuality"></div>

    <div class="section-title"><span class="n">٥</span> عادات نوم صحية</div>
    <div class="section-hint">علّم اللي التزمت بيه النهاردة</div>
    <div class="checklist" id="sleepHabits"></div>

    <div class="section-title"><span class="n">٦</span> مؤشرات الالتزام بالعادات</div>
    <div class="section-hint">متابعة تراكمية لالتزامك بعادات وروتين النوم</div>
    <div id="sleepAdherenceContainer" style="margin-top:8px;"></div>
  </div>'''

assert old_sleep_view in content, "Error: old_sleep_view not found in content"
content = content.replace(old_sleep_view, new_sleep_view, 1)
print("1. Replaced HTML #sleepView successfully.")

# -----------------------------------------------------------------------------
# 2. Storage & Model Functions: Sleep Routine & Wind-down
# -----------------------------------------------------------------------------
old_storage = '''function loadSleepTimes(iso){ return storageGetJSON('sleeptime:'+iso, {start:'', end:''}); }
function saveSleepTimes(iso,obj){ storageSet('sleeptime:'+iso, JSON.stringify(obj)); }
function loadSleepHabits(iso){ return storageGetJSON('sleephabits:'+iso, {}); }
function saveSleepHabits(iso,obj){ storageSet('sleephabits:'+iso, JSON.stringify(obj)); }'''

new_storage = '''function loadSleepTimes(iso){ return storageGetJSON('sleeptime:'+iso, {start:'', end:''}); }
function saveSleepTimes(iso,obj){ storageSet('sleeptime:'+iso, JSON.stringify(obj)); }
function loadSleepHabits(iso){ return storageGetJSON('sleephabits:'+iso, {}); }
function saveSleepHabits(iso,obj){ storageSet('sleephabits:'+iso, JSON.stringify(obj)); }

/* ================= SLEEP ROUTINE & WIND-DOWN DATA (PHASE 13.3) ================= */
const DEFAULT_WIND_DOWN_STEPS = [
  { id: 'screens', label: 'تقليل أو إيقاف استخدام الشاشات', icon: '📱', enabled: true },
  { id: 'bedroom', label: 'تجهيز غرفة النوم وتعتيم الإضاءة', icon: '🛏️', enabled: true },
  { id: 'wrapup', label: 'إنهاء المهام اليومية والاستعداد للنوم', icon: '📝', enabled: true },
  { id: 'azkar', label: 'أذكار النوم والدعاء المأثور', icon: '🤲', enabled: true },
  { id: 'reading', label: 'قراءة هادئة أو نشاط مريح قبل النوم', icon: '📖', enabled: true },
];

const SLEEP_ROUTINE_DEFAULTS = {
  targetBedtime: '23:00',
  targetWakeTime: '07:00',
  windDownLeadMin: 30,
  reminderEnabled: true,
  activeDays: [true, true, true, true, true, true, true],
  windDownSteps: DEFAULT_WIND_DOWN_STEPS
};

function loadSleepRoutineSettings(){
  const raw = storageGet('sleep-routine-settings');
  if(!raw) return Object.assign({}, SLEEP_ROUTINE_DEFAULTS);
  try {
    const parsed = JSON.parse(raw);
    if(!parsed || typeof parsed !== 'object') return Object.assign({}, SLEEP_ROUTINE_DEFAULTS);
    const merged = Object.assign({}, SLEEP_ROUTINE_DEFAULTS, parsed);
    if(!Array.isArray(merged.activeDays) || merged.activeDays.length !== 7){
      merged.activeDays = [true, true, true, true, true, true, true];
    }
    if(!Array.isArray(merged.windDownSteps) || merged.windDownSteps.length === 0){
      merged.windDownSteps = DEFAULT_WIND_DOWN_STEPS;
    }
    return merged;
  } catch(e) {
    return Object.assign({}, SLEEP_ROUTINE_DEFAULTS);
  }
}

function saveSleepRoutineSettings(settings){
  if(!settings || typeof settings !== 'object') return;
  storageSet('sleep-routine-settings', JSON.stringify(settings));
}

function loadWindDown(iso){
  return storageGetJSON('winddown:' + iso, {});
}

function saveWindDown(iso, obj){
  storageSet('winddown:' + iso, JSON.stringify(obj || {}));
}

function calcClockIntervalMinutes(startStr, endStr){
  if(!startStr || !endStr) return null;
  const partsS = startStr.split(':').map(Number);
  const partsE = endStr.split(':').map(Number);
  if(partsS.length < 2 || partsE.length < 2) return null;
  const [sh, sm] = partsS;
  const [eh, em] = partsE;
  if(isNaN(sh) || isNaN(sm) || isNaN(eh) || isNaN(em)) return null;
  let mins = (eh * 60 + em) - (sh * 60 + sm);
  if(mins <= 0) mins += 1440;
  return mins;
}

function timeDiffMinutes(actualStr, targetStr){
  if(!actualStr || !targetStr) return null;
  const partsA = actualStr.split(':').map(Number);
  const partsT = targetStr.split(':').map(Number);
  if(partsA.length < 2 || partsT.length < 2) return null;
  const [ah, am] = partsA;
  const [th, tm] = partsT;
  if(isNaN(ah) || isNaN(am) || isNaN(th) || isNaN(tm)) return null;
  const aMin = ah * 60 + am;
  const tMin = th * 60 + tm;
  let diff = aMin - tMin;
  while(diff > 720) diff -= 1440;
  while(diff <= -720) diff += 1440;
  return diff;
}'''

assert old_storage in content, "Error: old_storage not found in content"
content = content.replace(old_storage, new_storage, 1)
print("2. Replaced Storage & Model Functions successfully.")

# -----------------------------------------------------------------------------
# 3. Render Functions: Sleep Comparison, Wind-Down Routine, Adherence Summaries
# -----------------------------------------------------------------------------
old_render = '''function renderSleep(){
  document.getElementById('sleepTimeStart').value = sleepTimes.start || '';
  document.getElementById('sleepTimeEnd').value = sleepTimes.end || '';
  renderSimpleChecklist('sleepHabits', SLEEP_HABITS, sleepHabitsState, (key)=>{
    const iso = toISO(weekDates[selectedIdx]);
    if(sleepHabitsState[key]) delete sleepHabitsState[key]; else sleepHabitsState[key] = true;
    saveSleepHabits(iso, sleepHabitsState);
    weekDotsSleep[iso] = computeDotClassSleep(sleepTimes, sleepHabitsState);
    renderSleep();
    renderTabs();
  });
  renderSleepQuality();
  renderSleepSummary();
}

function onSleepTimeChange(){
  const iso = toISO(weekDates[selectedIdx]);
  sleepTimes = {
    start: document.getElementById('sleepTimeStart').value,
    end: document.getElementById('sleepTimeEnd').value,
  };
  saveSleepTimes(iso, sleepTimes);
  weekDotsSleep[iso] = computeDotClassSleep(sleepTimes, sleepHabitsState);
  renderSleepSummary();
  renderTabs();
}'''

new_render = '''let sleepRoutineSettingsOpen = false;
let sleepAdherenceDays = 7;

function renderSleepTargetComparison(){
  const el = document.getElementById('sleepComparisonCard');
  if(!el) return;
  const routine = loadSleepRoutineSettings();
  const tgtBed = routine.targetBedtime || '23:00';
  const tgtWake = routine.targetWakeTime || '07:00';
  const tgtDurMin = calcClockIntervalMinutes(tgtBed, tgtWake) || 480;
  const tgtDurHours = (tgtDurMin / 60).toFixed(1);

  if(!sleepTimes || !sleepTimes.start || !sleepTimes.end){
    el.innerHTML = `
      <div style="background:var(--card-alt); border:1px dashed var(--line); border-radius:8px; padding:10px 12px; font-size:.78rem; color:var(--muted); line-height:1.5;">
        🎯 <b>هدفك المحدد:</b> النوم الساعة <b>${tgtBed}</b> والاستيقاظ <b>${tgtWake}</b> (${tgtDurHours} ساعات).<br>
        سجّل وقت النوم والصحيان الفعلي بالأعلى لعرض المقارنة التلقائية مع هدفك.
      </div>
    `;
    return;
  }

  const bedDiff = timeDiffMinutes(sleepTimes.start, tgtBed);
  const wakeDiff = timeDiffMinutes(sleepTimes.end, tgtWake);
  const actDurMin = calcClockIntervalMinutes(sleepTimes.start, sleepTimes.end);
  const actDurHours = actDurMin ? (actDurMin / 60).toFixed(1) : '—';
  const durDiffHours = actDurMin ? ((actDurMin - tgtDurMin) / 60) : 0;

  let bedLabel = '';
  let bedColor = 'var(--primary)';
  if(Math.abs(bedDiff) <= 15){
    bedLabel = 'في الموعد المستهدف تقريبًا ✓';
    bedColor = 'var(--primary)';
  } else if(bedDiff > 15){
    bedLabel = `متأخر عن الهدف بـ ${bedDiff} دقيقة ⚠️`;
    bedColor = 'var(--warn)';
  } else {
    bedLabel = `أبكر من الهدف بـ ${Math.abs(bedDiff)} دقيقة ⚡`;
    bedColor = 'var(--info)';
  }

  let wakeLabel = '';
  let wakeColor = 'var(--primary)';
  if(Math.abs(wakeDiff) <= 15){
    wakeLabel = 'في موعد الاستيقاظ تقريبًا ✓';
    wakeColor = 'var(--primary)';
  } else if(wakeDiff > 15){
    wakeLabel = `استيقاظ متأخر بـ ${wakeDiff} دقيقة`;
    wakeColor = 'var(--warn)';
  } else {
    wakeLabel = `استيقاظ مبكر بـ ${Math.abs(wakeDiff)} دقيقة`;
    wakeColor = 'var(--info)';
  }

  let durLabel = '';
  if(Math.abs(durDiffHours) < 0.25){
    durLabel = 'مطابق للمدة المستهدفة ✓';
  } else if(durDiffHours > 0){
    durLabel = `أزيد بـ ${durDiffHours.toFixed(1)} س من الهدف`;
  } else {
    durLabel = `أقل بـ ${Math.abs(durDiffHours).toFixed(1)} س من الهدف`;
  }

  el.innerHTML = `
    <div class="card" style="background:var(--card-alt); border:1px solid var(--line); border-radius:10px; padding:12px;">
      <div style="font-weight:700; font-size:.82rem; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
        <span style="color:var(--text);">📊 مقارنة اليوم بالهدف المخطط</span>
        <span style="font-size:.72rem; color:var(--muted);">الهدف: ${tgtBed} ➔ ${tgtWake} (${tgtDurHours} س)</span>
      </div>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:8px;">
        <div style="background:var(--card); padding:8px 10px; border-radius:8px; border:1px solid var(--line);">
          <div style="font-size:.7rem; color:var(--muted);">وقت النوم الفعلي</div>
          <div style="font-weight:700; font-size:.9rem; margin:2px 0;">${sleepTimes.start}</div>
          <div style="font-size:.72rem; color:${bedColor}; font-weight:600;">${bedLabel}</div>
        </div>
        <div style="background:var(--card); padding:8px 10px; border-radius:8px; border:1px solid var(--line);">
          <div style="font-size:.7rem; color:var(--muted);">وقت الاستيقاظ الفعلي</div>
          <div style="font-weight:700; font-size:.9rem; margin:2px 0;">${sleepTimes.end}</div>
          <div style="font-size:.72rem; color:${wakeColor}; font-weight:600;">${wakeLabel}</div>
        </div>
        <div style="background:var(--card); padding:8px 10px; border-radius:8px; border:1px solid var(--line);">
          <div style="font-size:.7rem; color:var(--muted);">ساعات النوم الفعلية</div>
          <div style="font-weight:700; font-size:.9rem; margin:2px 0;">${actDurHours} س</div>
          <div style="font-size:.72rem; color:var(--text);">${durLabel}</div>
        </div>
      </div>
      <div style="font-size:.68rem; color:var(--muted); margin-top:8px; text-align:right;">
        ℹ️ هذه الإحصائيات للمتابعة الشخصية اليومية وليست تقييمًا أو تشخيصًا طبيًا.
      </div>
    </div>
  `;
}

function renderWindDownChecklist(){
  const el = document.getElementById('windDownRoutineChecklist');
  if(!el) return;
  el.innerHTML = '';
  const iso = toISO(weekDates[selectedIdx]);
  const routine = loadSleepRoutineSettings();
  const windDownState = loadWindDown(iso);
  const steps = (routine.windDownSteps || DEFAULT_WIND_DOWN_STEPS).filter(s => s.enabled !== false);

  steps.forEach(step => {
    const on = !!windDownState[step.id];
    const row = document.createElement('div');
    row.className = 'check-row';
    row.id = 'windDownRow-' + step.id;
    const safeLabel = typeof escapeHtml === 'function' ? escapeHtml(step.label) : step.label;
    const safeIcon = typeof escapeHtml === 'function' ? escapeHtml(step.icon) : step.icon;
    row.innerHTML = `
      <div class="check-left">
        <div class="cname">
          <span class="cicon" style="margin-left:8px;font-size:1.05rem;vertical-align:middle;">${safeIcon}</span>
          <span>${safeLabel}</span>
        </div>
      </div>
      <div class="toggle-group">
        <button type="button" class="tbtn ${on ? 'on-right' : ''}" data-key="${step.id}" aria-label="${safeLabel}">✓</button>
      </div>
    `;
    const btn = row.querySelector('.tbtn');
    const toggle = () => {
      if(windDownState[step.id]) delete windDownState[step.id];
      else windDownState[step.id] = true;
      saveWindDown(iso, windDownState);
      renderWindDownChecklist();
      renderSleepSummary();
      renderSleepAdherenceSummary();
    };
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      toggle();
    });
    row.style.cursor = 'pointer';
    row.addEventListener('click', (e) => {
      if(e.target === btn || btn.contains(e.target)) return;
      toggle();
    });
    el.appendChild(row);
  });
}

function computeSleepAdherenceStats(windowDays, refIso){
  const routine = loadSleepRoutineSettings();
  const refDate = refIso ? new Date(refIso + 'T00:00:00') : new Date();
  const today = new Date();
  const todayIso = toISO(today);

  const days = [];
  for(let i = windowDays - 1; i >= 0; i--){
    const d = new Date(refDate);
    d.setDate(d.getDate() - i);
    const iso = toISO(d);
    if(iso <= todayIso){
      days.push({ iso, dateObj: d });
    }
  }

  if(days.length === 0){
    return { hasData: false, totalDays: 0 };
  }

  const habitsStats = SLEEP_HABITS.map((label, idx) => {
    const key = 'i' + idx;
    let completedCount = 0;
    days.forEach(day => {
      const hState = loadSleepHabits(day.iso);
      if(hState && hState[key]) completedCount++;
    });
    const pct = days.length > 0 ? Math.round((completedCount / days.length) * 100) : 0;
    return { key, label, completed: completedCount, total: days.length, pct };
  });

  const totalHabitSlots = days.length * SLEEP_HABITS.length;
  let totalHabitsDone = 0;
  habitsStats.forEach(h => totalHabitsDone += h.completed);
  const overallHabitsPct = totalHabitSlots > 0 ? Math.round((totalHabitsDone / totalHabitSlots) * 100) : 0;

  const enabledSteps = (routine.windDownSteps || DEFAULT_WIND_DOWN_STEPS).filter(s => s.enabled !== false);
  let scheduledWindDownDays = 0;
  let totalWindDownStepsDone = 0;
  const windDownStats = enabledSteps.map(step => ({
    id: step.id,
    label: step.label,
    icon: step.icon,
    completed: 0,
    scheduledDays: 0,
    pct: 0
  }));

  days.forEach(day => {
    const dayIdx = (day.dateObj.getDay() + 1) % 7;
    const isScheduled = Array.isArray(routine.activeDays) ? !!routine.activeDays[dayIdx] : true;
    if(isScheduled){
      scheduledWindDownDays++;
      const wdState = loadWindDown(day.iso);
      windDownStats.forEach(stat => {
        stat.scheduledDays++;
        if(wdState && wdState[stat.id]){
          stat.completed++;
          totalWindDownStepsDone++;
        }
      });
    }
  });

  windDownStats.forEach(stat => {
    stat.pct = stat.scheduledDays > 0 ? Math.round((stat.completed / stat.scheduledDays) * 100) : 0;
  });

  const totalWindDownSlots = scheduledWindDownDays * enabledSteps.length;
  const overallWindDownPct = totalWindDownSlots > 0 ? Math.round((totalWindDownStepsDone / totalWindDownSlots) * 100) : 0;

  let daysWithActualTimes = 0;
  let onTimeBedCount = 0;
  days.forEach(day => {
    const t = loadSleepTimes(day.iso);
    if(t && t.start && t.end){
      daysWithActualTimes++;
      const diff = timeDiffMinutes(t.start, routine.targetBedtime);
      if(diff !== null && Math.abs(diff) <= 30){
        onTimeBedCount++;
      }
    }
  });

  const hasAnyData = totalHabitsDone > 0 || totalWindDownStepsDone > 0 || daysWithActualTimes > 0;

  return {
    hasData: hasAnyData,
    daysCount: days.length,
    scheduledWindDownDays,
    overallHabitsPct,
    habitsStats,
    overallWindDownPct,
    windDownStats,
    daysWithActualTimes,
    onTimeBedCount
  };
}

function renderSleepAdherenceSummary(requestedDays){
  const el = document.getElementById('sleepAdherenceContainer');
  if(!el) return;
  if(requestedDays !== undefined) sleepAdherenceDays = requestedDays;
  const iso = toISO(weekDates[selectedIdx]);
  const stats = computeSleepAdherenceStats(sleepAdherenceDays, iso);

  let html = `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
      <div style="font-weight:700; font-size:.88rem; color:var(--text);">نظرة عامة على الالتزام</div>
      <div class="day-toggle-row" style="margin-bottom:0;">
        <button type="button" class="dbtn ${sleepAdherenceDays===7?'active':''}" id="btnAdherence7" style="padding:4px 10px; font-size:.76rem;">٧ أيام</button>
        <button type="button" class="dbtn ${sleepAdherenceDays===28?'active':''}" id="btnAdherence28" style="padding:4px 10px; font-size:.76rem;">٢٨ يومًا</button>
      </div>
    </div>
  `;

  if(!stats.hasData){
    html += `
      <div class="card" style="background:var(--card-alt); border:1px solid var(--line); border-radius:10px; padding:16px; text-align:center; color:var(--muted); font-size:.82rem; line-height:1.5;">
        🌙 لا توجد بيانات كافية مسجلة في آخر ${sleepAdherenceDays} يومًا حتى الآن.<br>
        سجّل مواعيدك وعاداتك اليومية لتظهر هنا مؤشرات الالتزام التراكمية.
      </div>
    `;
  } else {
    html += `
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:8px; margin-bottom:12px;">
        <div style="background:var(--card-alt); padding:10px; border-radius:10px; border:1px solid var(--line); text-align:center;">
          <div style="font-size:1.15rem; font-weight:700; color:var(--primary);">${stats.overallHabitsPct}%</div>
          <div style="font-size:.72rem; color:var(--muted); margin-top:2px;">التزام العادات الصحية</div>
        </div>
        <div style="background:var(--card-alt); padding:10px; border-radius:10px; border:1px solid var(--line); text-align:center;">
          <div style="font-size:1.15rem; font-weight:700; color:var(--primary);">${stats.overallWindDownPct}%</div>
          <div style="font-size:.72rem; color:var(--muted); margin-top:2px;">التزام روتين التهدئة</div>
        </div>
        <div style="background:var(--card-alt); padding:10px; border-radius:10px; border:1px solid var(--line); text-align:center;">
          <div style="font-size:1.15rem; font-weight:700; color:var(--text);">${stats.onTimeBedCount} / ${stats.daysWithActualTimes}</div>
          <div style="font-size:.72rem; color:var(--muted); margin-top:2px;">نوم في الموعد (±30د)</div>
        </div>
      </div>

      <div class="card" style="background:var(--card-alt); border:1px solid var(--line); border-radius:10px; padding:12px; margin-bottom:10px;">
        <div style="font-weight:700; font-size:.8rem; margin-bottom:8px; color:var(--text);">تفاصيل العادات الصحية الخمس (${stats.daysCount} أيام):</div>
        ${stats.habitsStats.map(h => `
          <div style="margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; font-size:.76rem; margin-bottom:3px;">
              <span>${typeof escapeHtml === 'function' ? escapeHtml(h.label) : h.label}</span>
              <span class="mono" style="color:var(--muted);">${h.completed}/${h.total} (${h.pct}%)</span>
            </div>
            <div class="bar-track" style="height:6px;"><div class="bar-fill" style="width:${h.pct}%;"></div></div>
          </div>
        `).join('')}
      </div>

      <div class="card" style="background:var(--card-alt); border:1px solid var(--line); border-radius:10px; padding:12px;">
        <div style="font-weight:700; font-size:.8rem; margin-bottom:8px; color:var(--text);">تفاصيل روتين التهدئة المسائي (${stats.scheduledWindDownDays} أيام مجدولة):</div>
        ${stats.windDownStats.map(s => `
          <div style="margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; font-size:.76rem; margin-bottom:3px;">
              <span>${typeof escapeHtml === 'function' ? escapeHtml(s.icon) : s.icon} ${typeof escapeHtml === 'function' ? escapeHtml(s.label) : s.label}</span>
              <span class="mono" style="color:var(--muted);">${s.completed}/${s.scheduledDays} (${s.pct}%)</span>
            </div>
            <div class="bar-track" style="height:6px;"><div class="bar-fill" style="width:${s.pct}%;"></div></div>
          </div>
        `).join('')}
      </div>
    `;
  }

  el.innerHTML = html;

  const btn7 = document.getElementById('btnAdherence7');
  if(btn7) btn7.addEventListener('click', () => renderSleepAdherenceSummary(7));
  const btn28 = document.getElementById('btnAdherence28');
  if(btn28) btn28.addEventListener('click', () => renderSleepAdherenceSummary(28));
}

function renderSleepRoutineSettingsUI(){
  const panel = document.getElementById('sleepRoutineSettingsPanel');
  if(!panel) return;
  panel.style.display = sleepRoutineSettingsOpen ? 'block' : 'none';
  if(!sleepRoutineSettingsOpen) return;

  const routine = loadSleepRoutineSettings();
  const setBed = document.getElementById('setTargetBedtime');
  if(setBed) setBed.value = routine.targetBedtime || '23:00';
  const setWake = document.getElementById('setTargetWakeTime');
  if(setWake) setWake.value = routine.targetWakeTime || '07:00';
  const setLead = document.getElementById('setWindDownLeadMin');
  if(setLead) setLead.value = String(routine.windDownLeadMin || 30);

  const tbtn = document.getElementById('toggleWindDownReminder');
  if(tbtn){
    if(routine.reminderEnabled) tbtn.classList.add('on-right');
    else tbtn.classList.remove('on-right');
  }

  const daysRow = document.getElementById('sleepActiveDaysRow');
  if(daysRow){
    const dayLabels = (typeof SCHED_DAY_ABBR !== 'undefined') ? SCHED_DAY_ABBR : ['سبت','أحد','إثنين','ثلاثاء','أربعاء','خميس','جمعة'];
    daysRow.innerHTML = dayLabels.map((lbl, idx) => {
      const active = Array.isArray(routine.activeDays) ? !!routine.activeDays[idx] : true;
      return `<button type="button" class="dbtn ${active?'active':''}" data-day="${idx}" style="padding:4px 8px; font-size:.75rem;">${lbl}</button>`;
    }).join('');
    daysRow.querySelectorAll('.dbtn').forEach(btn => {
      btn.addEventListener('click', () => {
        const dIdx = Number(btn.dataset.day);
        if(!Array.isArray(routine.activeDays)) routine.activeDays = [true,true,true,true,true,true,true];
        routine.activeDays[dIdx] = !routine.activeDays[dIdx];
        saveSleepRoutineSettings(routine);
        renderSleepRoutineSettingsUI();
        renderSleepAdherenceSummary();
      });
    });
  }
}

function renderSleep(){
  document.getElementById('sleepTimeStart').value = sleepTimes.start || '';
  document.getElementById('sleepTimeEnd').value = sleepTimes.end || '';
  renderSimpleChecklist('sleepHabits', SLEEP_HABITS, sleepHabitsState, (key)=>{
    const iso = toISO(weekDates[selectedIdx]);
    if(sleepHabitsState[key]) delete sleepHabitsState[key]; else sleepHabitsState[key] = true;
    saveSleepHabits(iso, sleepHabitsState);
    weekDotsSleep[iso] = computeDotClassSleep(sleepTimes, sleepHabitsState);
    renderSleep();
    renderTabs();
  });
  renderSleepQuality();
  renderSleepSummary();
  renderSleepTargetComparison();
  renderWindDownChecklist();
  renderSleepRoutineSettingsUI();
  renderSleepAdherenceSummary();
}

function onSleepTimeChange(){
  const iso = toISO(weekDates[selectedIdx]);
  sleepTimes = {
    start: document.getElementById('sleepTimeStart').value,
    end: document.getElementById('sleepTimeEnd').value,
  };
  saveSleepTimes(iso, sleepTimes);
  weekDotsSleep[iso] = computeDotClassSleep(sleepTimes, sleepHabitsState);
  renderSleepSummary();
  renderSleepTargetComparison();
  renderSleepAdherenceSummary();
  renderTabs();
}'''

assert old_render in content, "Error: old_render not found in content"
content = content.replace(old_render, new_render, 1)
print("3. Replaced Render Functions successfully.")

# -----------------------------------------------------------------------------
# 4. Scheduler: Dispatch Wind-Down Routine Reminder
# -----------------------------------------------------------------------------
old_scheduler_return = '''          tryTrigger(tag, info, targetMin);
        }
      }
    });
  }

  return triggered;
}'''

new_scheduler_return = '''          tryTrigger(tag, info, targetMin);
        }
      }
    });
  }

  // 4. Sleep Wind-Down Routine Reminder (Phase 13.3)
  const sleepRoutine = (typeof loadSleepRoutineSettings === 'function') ? loadSleepRoutineSettings() : null;
  if(sleepRoutine && sleepRoutine.reminderEnabled && sleepRoutine.targetBedtime){
    const dObj = new Date(iso + 'T00:00:00');
    const dayIdx = isNaN(dObj.getTime()) ? 0 : (dObj.getDay() + 1) % 7;
    const isDayActive = Array.isArray(sleepRoutine.activeDays) ? !!sleepRoutine.activeDays[dayIdx] : true;
    if(isDayActive){
      const bedMin = (typeof timeToMinStage3D === 'function') ? timeToMinStage3D(sleepRoutine.targetBedtime) : null;
      if(bedMin !== null){
        const leadMin = Number(sleepRoutine.windDownLeadMin) || 30;
        let triggerMin = bedMin - leadMin;
        if(triggerMin < 0) triggerMin += 1440;
        const tag = `sleep:winddown:${iso}`;
        const timeLabel = (typeof schedMinToTime12 === 'function') ? schedMinToTime12(triggerMin) : `${triggerMin}m`;
        const bedLabel = (typeof schedMinToTime12 === 'function') ? schedMinToTime12(bedMin) : sleepRoutine.targetBedtime;
        const info = {
          icon: '🌙',
          title: '🌙 موعد الاستعداد للنوم',
          sub: `روتين التهدئة المسائي (${timeLabel})`,
          plainBody: `حان وقت بدء روتين التهدئة المسائي قبل موعد نومك المستهدف (${bedLabel}).`,
          body: `حان وقت بدء <b>روتين التهدئة المسائي</b> للاستعداد للنوم بحلول الساعة <b>${bedLabel}</b> (تنبيه مسبق بـ ${leadMin} دقيقة).`,
          mode: 'sleep',
          date: iso,
          targetId: 'winddown'
        };
        tryTrigger(tag, info, triggerMin);
      }
    }
  }

  return triggered;
}'''

assert old_scheduler_return in content, "Error: old_scheduler_return not found in content"
content = content.replace(old_scheduler_return, new_scheduler_return, 1)
print("4. Updated Scheduler Dispatch successfully.")

# -----------------------------------------------------------------------------
# 5. Backup Validation: Add sleep-routine-settings & winddown
# -----------------------------------------------------------------------------
old_backup_patterns = '''/^gym-warmup-state-v1$/, /^gym-cooldown-state-v1$/, /^zatoona-media-v1$/, /^media$/];'''
new_backup_patterns = '''/^gym-warmup-state-v1$/, /^gym-cooldown-state-v1$/, /^zatoona-media-v1$/, /^media$/, /^sleep-routine-settings$/, /^winddown:/];'''

assert old_backup_patterns in content, "Error: old_backup_patterns not found in content"
content = content.replace(old_backup_patterns, new_backup_patterns, 1)
print("5. Updated Backup Validation Patterns successfully.")

# -----------------------------------------------------------------------------
# 6. Event Wiring: Wire Sleep Routine Settings Controls
# -----------------------------------------------------------------------------
old_wiring = '''document.getElementById('sleepTimeStart').addEventListener('change', onSleepTimeChange);
document.getElementById('sleepTimeEnd').addEventListener('change', onSleepTimeChange);'''

new_wiring = '''document.getElementById('sleepTimeStart').addEventListener('change', onSleepTimeChange);
document.getElementById('sleepTimeEnd').addEventListener('change', onSleepTimeChange);

const btnTglSleepSettings = document.getElementById('btnToggleSleepRoutineSettings');
if(btnTglSleepSettings){
  btnTglSleepSettings.addEventListener('click', ()=>{
    sleepRoutineSettingsOpen = !sleepRoutineSettingsOpen;
    renderSleepRoutineSettingsUI();
  });
}
const btnCloseSleepSettings = document.getElementById('btnCloseSleepSettings');
if(btnCloseSleepSettings){
  btnCloseSleepSettings.addEventListener('click', ()=>{
    sleepRoutineSettingsOpen = false;
    renderSleepRoutineSettingsUI();
  });
}
const btnTglWindDownRem = document.getElementById('toggleWindDownReminder');
if(btnTglWindDownRem){
  btnTglWindDownRem.addEventListener('click', ()=>{
    const routine = loadSleepRoutineSettings();
    routine.reminderEnabled = !routine.reminderEnabled;
    saveSleepRoutineSettings(routine);
    renderSleepRoutineSettingsUI();
  });
}
const btnSaveSleepSettings = document.getElementById('btnSaveSleepRoutineSettings');
if(btnSaveSleepSettings){
  btnSaveSleepSettings.addEventListener('click', ()=>{
    const routine = loadSleepRoutineSettings();
    const setBed = document.getElementById('setTargetBedtime');
    const setWake = document.getElementById('setTargetWakeTime');
    const setLead = document.getElementById('setWindDownLeadMin');
    if(setBed && setBed.value) routine.targetBedtime = setBed.value;
    if(setWake && setWake.value) routine.targetWakeTime = setWake.value;
    if(setLead && setLead.value) routine.windDownLeadMin = Number(setLead.value) || 30;
    saveSleepRoutineSettings(routine);
    sleepRoutineSettingsOpen = false;
    renderSleepRoutineSettingsUI();
    renderSleepTargetComparison();
    renderSleepAdherenceSummary();
  });
}'''

assert old_wiring in content, "Error: old_wiring not found in content"
content = content.replace(old_wiring, new_wiring, 1)
print("6. Wired Sleep Routine Settings Controls successfully.")

# -----------------------------------------------------------------------------
# Write identically to index.html and zatoona.html
# -----------------------------------------------------------------------------
with open(INDEX_PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

with open(ZATOONA_PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Applied Phase 13.3 edits to index.html and zatoona.html successfully.")

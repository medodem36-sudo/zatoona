import hashlib, shutil, sys, os

def apply():
    with open('index.html', 'rb') as f:
        raw = f.read()

    expected_sha = 'de512cf5254193266332a31aa29f1621c88884928006b5444e990b80ee2ce345'
    cur_sha = hashlib.sha256(raw).hexdigest()
    if cur_sha != expected_sha:
        print(f"Error: index.html SHA mismatch!\nExpected: {expected_sha}\nGot:      {cur_sha}")
        return False

    content = raw.decode('utf-8')

    # 1. CSS Target
    css_anchor = '/* ===== Schedule mode ===== */'
    if css_anchor not in content:
        print("Error: CSS anchor not found!")
        return False

    css_code = """/* ================= PHASE 6C: WORKOUT PROGRESS & PERFORMANCE ANALYTICS ================= */
  .gym-analytics-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 14px 16px;
    margin-bottom: 14px;
    box-sizing: border-box;
  }
  .gym-analytics-title {
    font-weight: 700;
    font-size: .95rem;
    color: var(--text);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    flex-wrap: wrap;
  }
  .gym-analytics-stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 8px;
    margin-bottom: 12px;
  }
  .gym-analytics-stat {
    background: var(--card-alt);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 9px 10px;
    text-align: right;
    box-sizing: border-box;
  }
  .gym-analytics-stat .gas-val {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--text);
    line-height: 1.2;
  }
  .gym-analytics-stat .gas-lbl {
    font-size: .74rem;
    color: var(--muted);
    margin-top: 2px;
    font-weight: 500;
  }
  .gym-analytics-stat .gas-sub {
    font-size: .67rem;
    color: var(--muted);
    margin-top: 3px;
    line-height: 1.2;
  }
  .gym-prog-chart-wrap {
    background: var(--card-alt);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 10px 8px;
    margin: 10px 0;
    position: relative;
    box-sizing: border-box;
  }
  .gym-prog-chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 4px 6px;
    font-size: .75rem;
    color: var(--muted);
  }
  .gym-prog-chart-svg {
    width: 100%;
    height: auto;
    max-height: 140px;
    display: block;
    overflow: visible;
  }
  .gym-chart-empty-note {
    color: var(--muted);
    font-size: .78rem;
    padding: 16px 8px;
    text-align: center;
    line-height: 1.5;
  }
  .gym-pr-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(95px, 1fr));
    gap: 6px;
    background: var(--card-alt);
    border-radius: 8px;
    padding: 8px 10px;
    margin: 8px 0 10px;
    box-sizing: border-box;
  }
  .gym-pr-item {
    min-width: 0;
  }
  .gym-pr-item .pv {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: .88rem;
    color: var(--text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .gym-pr-item .pl {
    font-size: .67rem;
    color: var(--muted);
    margin-top: 1px;
  }
  @media (max-width: 420px) {
    .gym-analytics-stat-grid {
      grid-template-columns: 1fr 1fr;
    }
    .gym-pr-row {
      grid-template-columns: 1fr 1fr;
    }
  }

  """

    content = content.replace(css_anchor, css_code + css_anchor, 1)

    # 2. JS Target
    s_idx = content.find('/* ================= WORKOUT HISTORY: render')
    e_idx = content.find('/* ================= REMINDERS: render/handlers')
    if s_idx == -1 or e_idx == -1:
        print("Error: JS slice markers not found!")
        return False

    js_replacement = """/* ================= PHASE 6C: WORKOUT PROGRESS & PERFORMANCE ANALYTICS ================= */

let workoutAnalyticsRange = 'all'; // '7d' | '30d' | '90d' | 'all' | 'custom'

function getAnalyticsDateRange(rangeKey, customFrom, customTo, refDate){
  if(rangeKey === 'all'){
    return { from: '', to: '' };
  }
  if(rangeKey === 'custom'){
    return { from: customFrom || '', to: customTo || '' };
  }
  const ref = (refDate instanceof Date && !isNaN(refDate.getTime())) ? new Date(refDate.getTime()) : new Date();
  const end = new Date(ref.getFullYear(), ref.getMonth(), ref.getDate());
  let days = 30;
  if(rangeKey === '7d') days = 7;
  else if(rangeKey === '90d') days = 90;
  const start = new Date(end.getFullYear(), end.getMonth(), end.getDate() - (days - 1));
  return {
    from: toISO(start),
    to: toISO(end)
  };
}

function getWorkoutSessionsAnalytics(filter = {}){
  const { from, to } = filter;
  const rawSessions = (typeof loadGymSessions === 'function') ? loadGymSessions() : {};
  const completedSessions = [];
  const cancelledSessions = [];
  const inProgressSessions = [];
  const completedDatesSet = new Set();
  let totalDurationSeconds = 0;
  let durationCount = 0;

  function processRecord(sess){
    if(!sess || typeof sess !== 'object' || !sess.iso) return;
    const iso = sess.iso;
    if(from && iso < from) return;
    if(to && iso > to) return;

    if(sess.status === 'completed'){
      completedSessions.push(sess);
      completedDatesSet.add(iso);
      const dur = typeof sess.durationSeconds === 'number' ? sess.durationSeconds : null;
      let validTime = true;
      if(sess.startedAt && isNaN(new Date(sess.startedAt).getTime())) validTime = false;
      if(sess.completedAt && isNaN(new Date(sess.completedAt).getTime())) validTime = false;
      if(validTime && dur !== null && !isNaN(dur) && dur > 0){
        totalDurationSeconds += dur;
        durationCount++;
      }
    } else if(sess.status === 'cancelled'){
      cancelledSessions.push(sess);
    } else if(sess.status === 'in_progress'){
      inProgressSessions.push(sess);
    }
  }

  for(const iso of Object.keys(rawSessions)){
    const sess = rawSessions[iso];
    if(!sess) continue;
    if(Array.isArray(sess.history)){
      for(const snap of sess.history){
        processRecord(snap);
      }
    }
    processRecord(sess);
  }

  return {
    completedSessions,
    completedCount: completedSessions.length,
    cancelledCount: cancelledSessions.length,
    inProgressCount: inProgressSessions.length,
    completedDatesSet,
    totalDurationSeconds,
    avgDurationSeconds: durationCount > 0 ? Math.round(totalDurationSeconds / durationCount) : 0
  };
}

function getWorkoutPerformanceAnalytics(filter = {}){
  const { from, to } = filter;
  const prefix = STORAGE_PREFIX + 'ex:';
  const activeDatesSet = new Set();
  const exerciseDataMap = {};
  let cumulativeVolume = 0;
  let volumeEntriesCount = 0;
  let totalCompletedSetsCount = 0;

  for(let i = 0; i < localStorage.length; i++){
    const k = localStorage.key(i);
    if(!k || k.indexOf(prefix) !== 0) continue;
    const iso = k.slice(prefix.length);
    if(!/^\\d{4}-\\d{2}-\\d{2}$/.test(iso)) continue;
    if(from && iso < from) continue;
    if(to && iso > to) continue;

    let obj = null;
    try { obj = JSON.parse(localStorage.getItem(k)); } catch(e){ continue; }
    if(!obj || typeof obj !== 'object') continue;

    let dateHasActivity = false;
    for(const key of Object.keys(obj)){
      const st = obj[key];
      if(!st || typeof st !== 'object') continue;
      const hasSets = Array.isArray(st.sets) && st.sets.some(Boolean);
      if(!hasSets) continue;

      dateHasActivity = true;
      const doneSets = st.sets.filter(Boolean).length;
      totalCompletedSetsCount += doneSets;

      let w = null;
      if(st.weight !== undefined && st.weight !== null && String(st.weight).trim() !== ''){
        const parsedW = parseFloat(st.weight);
        if(!isNaN(parsedW) && parsedW >= 0) w = parsedW;
      }

      let r = null;
      if(st.reps !== undefined && st.reps !== null && String(st.reps).trim() !== ''){
        const parsedR = parseInt(st.reps, 10);
        if(!isNaN(parsedR) && parsedR > 0) r = parsedR;
      }

      let vol = null;
      if(w !== null && w > 0 && r !== null && r > 0 && doneSets > 0){
        vol = doneSets * w * r;
        cumulativeVolume += vol;
        volumeEntriesCount++;
      }

      if(!exerciseDataMap[key]) exerciseDataMap[key] = [];
      exerciseDataMap[key].push({
        iso,
        weight: w,
        reps: r,
        rawReps: st.reps || '',
        rawWeight: st.weight || '',
        rir: st.rir || '',
        note: st.note || '',
        setsCount: doneSets,
        volume: vol
      });
    }

    if(dateHasActivity){
      activeDatesSet.add(iso);
    }
  }

  for(const key of Object.keys(exerciseDataMap)){
    exerciseDataMap[key].sort((a, b) => (a.iso < b.iso ? 1 : -1));
  }

  return {
    activeDatesSet,
    exerciseDataMap,
    totalCompletedSetsCount,
    cumulativeVolume: volumeEntriesCount > 0 ? Math.round(cumulativeVolume) : null,
    volumeEntriesCount,
    totalExercisesLogged: Object.keys(exerciseDataMap).length
  };
}

function getWorkoutProgressSummary(filter = {}){
  const { rangeKey = workoutAnalyticsRange || 'all', customFrom = workoutHistoryFrom, customTo = workoutHistoryTo, refDate = new Date() } = filter;
  const range = getAnalyticsDateRange(rangeKey, customFrom, customTo, refDate);
  const from = range.from;
  const to = range.to;

  const sessAnalytics = getWorkoutSessionsAnalytics({ from, to });
  const perfAnalytics = getWorkoutPerformanceAnalytics({ from, to });

  // Unified unique workout days (ZERO double-counting between sessions and exercise records)
  const uniqueWorkoutDates = new Set([
    ...sessAnalytics.completedDatesSet,
    ...perfAnalytics.activeDatesSet
  ]);
  const workoutDaysCount = uniqueWorkoutDates.size;

  // Group by calendar weeks (Saturday-first Egyptian week start)
  const activeWeekKeys = new Set();
  uniqueWorkoutDates.forEach(iso => {
    const [y, mo, da] = iso.split('-').map(Number);
    const d = new Date(y, mo - 1, da);
    const dayOfWeek = (d.getDay() + 1) % 7;
    const weekStart = new Date(y, mo - 1, da - dayOfWeek);
    activeWeekKeys.add(toISO(weekStart));
  });
  const activeWeeksCount = activeWeekKeys.size;
  const weeklyFrequency = activeWeeksCount > 0 ? (workoutDaysCount / activeWeeksCount).toFixed(1) : '0';

  // Planned gym days count in range
  let plannedDaysCount = 0;
  if(from && to){
    const [sy, sm, sd] = from.split('-').map(Number);
    const [ey, em, ed] = to.split('-').map(Number);
    const cur = new Date(sy, sm - 1, sd);
    const end = new Date(ey, em - 1, ed);
    let guard = 0;
    while(cur <= end && guard < 400){
      const dayIso = toISO(cur);
      if(typeof getEffectiveGymDay === 'function'){
        const eff = getEffectiveGymDay(dayIso);
        if(eff && eff.gym && !eff.isRest && eff.gymType !== 'rest'){
          plannedDaysCount++;
        }
      }
      cur.setDate(cur.getDate() + 1);
      guard++;
    }
  }

  return {
    from,
    to,
    rangeKey,
    completedSessionsCount: sessAnalytics.completedCount,
    cancelledSessionsCount: sessAnalytics.cancelledCount,
    inProgressSessionsCount: sessAnalytics.inProgressCount,
    workoutDaysCount,
    plannedDaysCount,
    activeWeeksCount,
    weeklyFrequency,
    totalExercisesLogged: perfAnalytics.totalExercisesLogged,
    totalCompletedSets: perfAnalytics.totalCompletedSetsCount,
    totalVolume: perfAnalytics.cumulativeVolume,
    volumeEntriesCount: perfAnalytics.volumeEntriesCount,
    avgDurationSeconds: sessAnalytics.avgDurationSeconds,
    exerciseDataMap: perfAnalytics.exerciseDataMap
  };
}

function getExerciseProgressionStats(exKey, exerciseDataMap, filter = {}){
  if(!exKey) return null;
  const historyDesc = (exerciseDataMap && exerciseDataMap[exKey]) ? exerciseDataMap[exKey] : [];
  const filteredDesc = historyDesc.filter(h => {
    if(filter.from && h.iso < filter.from) return false;
    if(filter.to && h.iso > filter.to) return false;
    return true;
  });

  const last = filteredDesc[0] || null;
  let prWeight = null;
  let prReps = null;
  let prVolume = null;

  filteredDesc.forEach(h => {
    if(h.weight !== null && h.weight > 0){
      if(!prWeight || h.weight > prWeight.weight){
        prWeight = { weight: h.weight, reps: h.reps, rawReps: h.rawReps, iso: h.iso, rir: h.rir };
      }
    }
    if(h.reps !== null && h.reps > 0){
      if(!prReps || h.reps > prReps.reps){
        prReps = { reps: h.reps, weight: h.weight, rawWeight: h.rawWeight, iso: h.iso, rir: h.rir };
      }
    }
    if(h.volume !== null && h.volume > 0){
      if(!prVolume || h.volume > prVolume.volume){
        prVolume = { volume: h.volume, weight: h.weight, reps: h.reps, setsCount: h.setsCount, iso: h.iso };
      }
    }
  });

  const pointsAsc = filteredDesc.slice().reverse();

  return {
    exKey,
    count: filteredDesc.length,
    historyDesc: filteredDesc,
    pointsAsc,
    last,
    prWeight,
    prReps,
    prVolume
  };
}

function renderWorkoutProgressionSVG(pointsAsc){
  if(!pointsAsc || pointsAsc.length < 2){
    if(pointsAsc && pointsAsc.length === 1){
      const p = pointsAsc[0];
      return `<div class="gym-chart-empty-note">نقطة تسجيل واحدة (${p.weight !== null ? p.weight + ' كجم' : ''}${p.rawReps ? ' × ' + p.rawReps : ''}) في ${p.iso}. سجّل جلسة تانية عشان يظهر المنحنى البياني للتقدم.</div>`;
    }
    return `<div class="gym-chart-empty-note">لا توجد بيانات كافية لرسم منحنى التقدم البياني في هذه الفترة.</div>`;
  }

  const validPoints = pointsAsc.filter(p => p.weight !== null && !isNaN(p.weight) && p.weight > 0);
  if(validPoints.length < 2){
    return `<div class="gym-chart-empty-note">يلزم تسجيل الوزن لنقطتين على الأقل لإظهار منحنى التقدم.</div>`;
  }

  const weights = validPoints.map(p => p.weight);
  const minW = Math.min(...weights);
  const maxW = Math.max(...weights);
  const rangeW = (maxW - minW) || 1;

  const w = 340, h = 110;
  const padX = 28, padY = 16, bPad = 22;
  const chartH = h - padY - bPad;
  const n = validPoints.length;
  const stepX = (w - padX * 2) / (n - 1);

  const coords = [];
  const circles = [];
  const labels = [];

  validPoints.forEach((p, i) => {
    const x = padX + stepX * i;
    const y = padY + chartH * (1 - (p.weight - minW) / rangeW);
    coords.push(`${x.toFixed(1)},${y.toFixed(1)}`);
    circles.push(`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="var(--accent)" stroke="var(--card)" stroke-width="1.5"><title>${p.iso}: ${p.weight} كجم${p.rawReps ? ' × ' + p.rawReps : ''}</title></circle>`);
    const shortDate = p.iso.slice(5).replace('-', '/');
    if(n <= 5 || i === 0 || i === n - 1 || i % 2 === 0){
      labels.push(`<text x="${x.toFixed(1)}" y="${h - 4}" font-size="8.5" text-anchor="middle" fill="var(--muted)" font-family="monospace">${shortDate}</text>`);
    }
  });

  return `
    <div class="gym-prog-chart-wrap">
      <div class="gym-prog-chart-header">
        <span>📈 منحنى تطور الوزن (${minW.toFixed(1)} - ${maxW.toFixed(1)} كجم)</span>
        <span>${validPoints.length} نقاط</span>
      </div>
      <svg viewBox="0 0 ${w} ${h}" class="gym-prog-chart-svg">
        <line x1="${padX}" y1="${padY}" x2="${w - padX}" y2="${padY}" stroke="var(--line)" stroke-dasharray="3,3" opacity="0.6"/>
        <line x1="${padX}" y1="${padY + chartH / 2}" x2="${w - padX}" y2="${padY + chartH / 2}" stroke="var(--line)" stroke-dasharray="3,3" opacity="0.6"/>
        <line x1="${padX}" y1="${padY + chartH}" x2="${w - padX}" y2="${padY + chartH}" stroke="var(--line)" stroke-dasharray="3,3" opacity="0.6"/>
        <polyline points="${coords.join(' ')}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
        ${circles.join('')}
        ${labels.join('')}
      </svg>
    </div>
  `;
}

function renderWorkoutHistory(){
  const picker = document.getElementById('workoutHistoryPicker');
  const body = document.getElementById('workoutHistoryBody');
  if(!picker || !body) return;

  const allDefs = (typeof getAllExerciseDefinitions === 'function') ? getAllExerciseDefinitions() : {};
  const histByKey = getAllExHistory();

  const activeKeys = [...(typeof EX_A !== 'undefined' ? EX_A.map(e=>e.key) : []), ...(typeof EX_B !== 'undefined' ? EX_B.map(e=>e.key) : [])];
  const historyKeys = Object.keys(histByKey).filter(k=> (histByKey[k]||[]).length>0);
  const combinedKeys = Array.from(new Set([...activeKeys, ...historyKeys]));

  const withHistory = [];
  combinedKeys.forEach(k=>{
    if((histByKey[k]||[]).length>0){
      const def = allDefs[k] || { key: k, name: k };
      const isExcluded = (typeof excludedExercises !== 'undefined') && !!excludedExercises[k];
      withHistory.push({
        key: k,
        name: isExcluded ? `${def.name} (مستبعد)` : def.name,
        rawName: def.name,
        isExcluded
      });
    }
  });

  if(withHistory.length===0){
    picker.innerHTML = '';
    body.innerHTML = '<div class="empty-note">لسه معندكش سجل تمارين — سجّل أول مجموعة بالوزن من تاب الجيم فوق وهتظهر هنا تلقائيًا</div>';
    return;
  }

  if(!workoutHistorySelectedKey || !withHistory.some(ex=>ex.key===workoutHistorySelectedKey)){
    workoutHistorySelectedKey = withHistory[0].key;
  }

  picker.innerHTML = withHistory.map(ex=>
    `<div class="day-chip ${ex.key===workoutHistorySelectedKey?'on':''}" data-key="${ex.key}">${escapeHtml(ex.name)}</div>`
  ).join('');
  picker.querySelectorAll('.day-chip').forEach(chip=>{
    chip.addEventListener('click', ()=>{ workoutHistorySelectedKey = chip.dataset.key; renderWorkoutHistory(); });
  });

  const summary = getWorkoutProgressSummary({
    rangeKey: workoutAnalyticsRange,
    customFrom: workoutHistoryFrom,
    customTo: workoutHistoryTo
  });

  if(workoutAnalyticsRange !== 'custom'){
    workoutHistoryFrom = summary.from || '';
    workoutHistoryTo = summary.to || '';
  }

  const exProg = getExerciseProgressionStats(workoutHistorySelectedKey, summary.exerciseDataMap, {
    from: workoutHistoryFrom,
    to: workoutHistoryTo
  });

  let hist = (exProg ? exProg.historyDesc : []).slice();
  if(workoutHistorySortAsc) hist = hist.slice().reverse();

  const legacyProg = exProgression(workoutHistorySelectedKey, '');
  const prStr = (exProg && exProg.prWeight)
    ? `${exProg.prWeight.weight} كجم${exProg.prWeight.rawReps ? ' × ' + exProg.prWeight.rawReps : ''}`
    : (legacyProg.pr ? `${legacyProg.pr.weight} كجم${legacyProg.pr.reps ? ' × ' + legacyProg.pr.reps : ''}` : '—');
  const lastStr = (exProg && exProg.last)
    ? `${exProg.last.weight !== null ? exProg.last.weight : '—'} كجم${exProg.last.rawReps ? ' × ' + exProg.last.rawReps : ''}${exProg.last.rir ? ' (RIR' + exProg.last.rir + ')' : ''}`
    : (legacyProg.last ? `${legacyProg.last.weight} كجم${legacyProg.last.reps ? ' × ' + legacyProg.last.reps : ''}${legacyProg.last.rir ? ' (RIR' + legacyProg.last.rir + ')' : ''}` : '—');

  const maxRepsStr = (exProg && exProg.prReps)
    ? `${exProg.prReps.reps} تكرار${exProg.prReps.weight !== null ? ' @ ' + exProg.prReps.weight + ' كجم' : ''}`
    : '—';
  const maxVolStr = (exProg && exProg.prVolume)
    ? `${exProg.prVolume.volume.toLocaleString('ar-EG')} كجم`
    : '—';

  const chartHtml = renderWorkoutProgressionSVG(exProg ? exProg.pointsAsc : []);

  const rows = hist.map(h=>{
    const d = new Date(h.iso+'T00:00:00');
    const dayName = isNaN(d.getTime()) ? '' : d.toLocaleDateString('ar-EG',{weekday:'long'});
    const volStr = h.volume !== null ? ` · حجم: ${h.volume.toLocaleString('ar-EG')} كجم` : '';
    const setsStr = h.setsCount ? `${h.setsCount} م` : '';
    return `<div class="check-row"><div class="check-left">
      <div class="cname mono">${h.iso}${dayName?' — '+dayName:''}</div>
      <div class="cqty">${h.weight !== null ? h.weight + ' كجم' : '—'}${h.rawReps ? ' × ' + h.rawReps + ' تكرار' : ''}${setsStr ? ' (' + setsStr + ')' : ''}${h.rir ? ' · RIR ' + h.rir : ''}${volStr}</div>
      ${h.note ? `<div class="tl-note" style="margin-top:2px;">📝 ${escapeHtml(h.note)}</div>` : ''}
    </div></div>`;
  }).join('');

  let adherenceSub = 'لا تشمل أيام الراحة';
  if(summary.plannedDaysCount > 0){
    const pct = Math.min(100, Math.round((summary.workoutDaysCount / summary.plannedDaysCount) * 100));
    adherenceSub = `من أصل ${summary.plannedDaysCount} يوم مخطط (${pct}%)`;
  }

  const volTotalStr = summary.totalVolume !== null
    ? `${summary.totalVolume.toLocaleString('ar-EG')} كجم`
    : 'غير متاح';

  body.innerHTML = `
    <!-- Range Filter Chips -->
    <div class="sc-field" style="margin-bottom:10px;">
      <div class="day-toggle-row" id="gymAnalyticsRangeChips" style="margin-bottom:0;">
        <div class="day-chip ${workoutAnalyticsRange==='7d'?'on':''}" data-range="7d">آخر ٧ أيام</div>
        <div class="day-chip ${workoutAnalyticsRange==='30d'?'on':''}" data-range="30d">آخر ٣٠ يوم</div>
        <div class="day-chip ${workoutAnalyticsRange==='90d'?'on':''}" data-range="90d">آخر ٩٠ يوم</div>
        <div class="day-chip ${workoutAnalyticsRange==='all'?'on':''}" data-range="all">كل السجل</div>
      </div>
    </div>

    <!-- Summary Metrics Card Grid -->
    <div class="gym-analytics-stat-grid">
      <div class="gym-analytics-stat">
        <div class="gas-val">${summary.completedSessionsCount}</div>
        <div class="gas-lbl">🏋️‍♂️ جلسات مكتملة</div>
        <div class="gas-sub">${summary.inProgressSessionsCount > 0 ? summary.inProgressSessionsCount + ' جارية' : (summary.cancelledSessionsCount > 0 ? summary.cancelledSessionsCount + ' ملغاة' : 'مسجلة بالمحرك')}</div>
      </div>
      <div class="gym-analytics-stat">
        <div class="gas-val">${summary.workoutDaysCount}</div>
        <div class="gas-lbl">📅 أيام التدريب</div>
        <div class="gas-sub">${adherenceSub}</div>
      </div>
      <div class="gym-analytics-stat">
        <div class="gas-val">${volTotalStr}</div>
        <div class="gas-lbl">📈 حجم التدريب</div>
        <div class="gas-sub">مجموعات × كجم × تكرار</div>
      </div>
      <div class="gym-analytics-stat">
        <div class="gas-val">${summary.activeWeeksCount}</div>
        <div class="gas-lbl">🔄 أسابيع نشطة</div>
        <div class="gas-sub">${summary.weeklyFrequency} تمرين/أسبوع</div>
      </div>
    </div>

    <!-- Selected Exercise Progression Stats -->
    <div class="prog-row">
      <div class="prog-item"><div class="pv">🏆 ${prStr}</div><div class="pl">أفضل أداء (PR)</div></div>
      <div class="prog-item"><div class="pv">⚡ ${maxRepsStr}</div><div class="pl">أعلى تكرار</div></div>
      <div class="prog-item"><div class="pv">📊 ${maxVolStr}</div><div class="pl">أعلى حجم جلسة</div></div>
      <div class="prog-item"><div class="pv">${lastStr}</div><div class="pl">آخر جلسة</div></div>
      <div class="prog-item"><div class="pv">${hist.length}</div><div class="pl">جلسات في الفترة دي</div></div>
    </div>

    <!-- Progress SVG Chart -->
    ${chartHtml}

    <!-- Custom Date Filter Inputs & Sort -->
    <div class="sc-grid" style="margin-bottom:8px;">
      <div class="sc-field"><label>من تاريخ</label><input type="date" id="workoutHistFrom" class="weight-input" style="width:100%;" value="${escapeHtml(workoutHistoryFrom)}"></div>
      <div class="sc-field"><label>لحد تاريخ</label><input type="date" id="workoutHistTo" class="weight-input" style="width:100%;" value="${escapeHtml(workoutHistoryTo)}"></div>
    </div>
    <div style="display:flex; justify-content:flex-end; margin-bottom:8px;">
      <button class="reset-btn" id="workoutHistSortBtn">${workoutHistorySortAsc?'⬆ الأقدم أولًا':'⬇ الأحدث أولًا'}</button>
    </div>

    <!-- History Log Rows -->
    <div class="checklist">${rows || '<div class="empty-note">مفيش جلسات في الفترة المحددة</div>'}</div>
  `;

  const rangeWrap = document.getElementById('gymAnalyticsRangeChips');
  if(rangeWrap){
    rangeWrap.querySelectorAll('.day-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const r = chip.dataset.range;
        if(r){
          workoutAnalyticsRange = r;
          try { storageSet('gym-analytics-range', r); } catch(e){}
          renderWorkoutHistory();
        }
      });
    });
  }

  const fromEl = document.getElementById('workoutHistFrom');
  if(fromEl){
    fromEl.addEventListener('change', (e) => {
      workoutHistoryFrom = e.target.value;
      workoutAnalyticsRange = 'custom';
      renderWorkoutHistory();
    });
  }
  const toEl = document.getElementById('workoutHistTo');
  if(toEl){
    toEl.addEventListener('change', (e) => {
      workoutHistoryTo = e.target.value;
      workoutAnalyticsRange = 'custom';
      renderWorkoutHistory();
    });
  }

  const sortBtn = document.getElementById('workoutHistSortBtn');
  if(sortBtn){
    sortBtn.addEventListener('click', () => {
      workoutHistorySortAsc = !workoutHistorySortAsc;
      renderWorkoutHistory();
    });
  }
}

// Window exports for testing and external integrations
window.getAnalyticsDateRange = getAnalyticsDateRange;
window.getWorkoutSessionsAnalytics = getWorkoutSessionsAnalytics;
window.getWorkoutPerformanceAnalytics = getWorkoutPerformanceAnalytics;
window.getWorkoutProgressSummary = getWorkoutProgressSummary;
window.getExerciseProgressionStats = getExerciseProgressionStats;
window.renderWorkoutProgressionSVG = renderWorkoutProgressionSVG;
window.renderWorkoutHistory = renderWorkoutHistory;
"""

    content = content[:s_idx] + js_replacement.strip() + "\n\n" + content[e_idx:]

    with open('index.html', 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    with open('index.html', 'rb') as f:
        new_sha = hashlib.sha256(f.read()).hexdigest()
    print("index.html updated successfully! New SHA:", new_sha)

    # Sync zatoona.html
    shutil.copy2('index.html', 'zatoona.html')
    print("zatoona.html synchronized.")
    return True

if __name__ == '__main__':
    apply()

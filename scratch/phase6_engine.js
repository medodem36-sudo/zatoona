/* ==========================================================================
   PHASE 6: ADVANCED SLEEP & LIFE OS CONTROLLER
   Circadian Cycles, Power Nap, Screen-Free Wind-down, Desk Breaks,
   Eisenhower Matrix, Critical Task Pinning, Archive, Vacation Freeze & Safar
   ========================================================================== */

(function(){
  'use strict';

  // -------------------------------------------------------------
  // 1. SLEEP CYCLE CALCULATOR (90-Minute Circadian Rhythm Engine)
  // -------------------------------------------------------------
  let sleepCycleMode = 'now'; // 'now' or 'wake'

  function formatTimeArabic12(d){
    let h = d.getHours();
    const m = d.getMinutes();
    const suffix = h >= 12 ? 'م' : 'ص';
    h = h % 12 || 12;
    const mm = m < 10 ? '0' + m : m;
    return `${h}:${mm} ${suffix}`;
  }

  function setSleepCycleMode(mode){
    sleepCycleMode = mode;
    const btnNow = document.getElementById('btnSleepNowMode');
    const btnWake = document.getElementById('btnWakeTargetMode');
    const inputWrap = document.getElementById('wakeTargetInputWrap');
    if(btnNow) btnNow.classList.toggle('active', mode === 'now');
    if(btnWake) btnWake.classList.toggle('active', mode === 'wake');
    if(inputWrap) inputWrap.style.display = (mode === 'wake') ? 'flex' : 'none';
    calculateSleepCycles();
  }

  function calculateSleepCycles(){
    const grid = document.getElementById('sleepCycleResultsGrid');
    if(!grid) return;

    const cycles = [
      { count: 3, hours: 4.5, title: 'إنقاذ سريع', desc: 'حد أدنى للنشاط', golden: false },
      { count: 4, hours: 6.0, title: 'نوم خفيف', desc: 'مناسب لضيق الوقت', golden: false },
      { count: 5, hours: 7.5, title: 'المثالي والموصى به 🌟', desc: 'أعلى تركيز واستشفاء', golden: true },
      { count: 6, hours: 9.0, title: 'استشفاء عميق', desc: 'للرياضيين والإرهاق', golden: false }
    ];

    let html = '';
    const latencyMinutes = 14; // Average human sleep latency

    if(sleepCycleMode === 'now'){
      const now = new Date();
      cycles.forEach(c => {
        const wakeTime = new Date(now.getTime() + (latencyMinutes * 60000) + (c.hours * 3600000));
        const formatted = formatTimeArabic12(wakeTime);
        html += `
          <div class="sleep-cycle-item ${c.golden ? 'golden' : ''}">
            <span class="sleep-cycle-badge">${c.count} دورات (${c.hours} س)</span>
            <div class="sleep-cycle-time">${formatted}</div>
            <div style="font-size:.72rem; color:var(--text); font-weight:700;">${c.title}</div>
            <div style="font-size:.68rem; color:var(--muted);">${c.desc}</div>
          </div>
        `;
      });
    } else {
      const input = document.getElementById('targetWakeTimeInput');
      const timeVal = (input && input.value) ? input.value : '06:30';
      const parts = timeVal.split(':').map(Number);
      const wakeDate = new Date();
      wakeDate.setHours(parts[0], parts[1], 0, 0);

      cycles.forEach(c => {
        const bedTime = new Date(wakeDate.getTime() - (latencyMinutes * 60000) - (c.hours * 3600000));
        const formatted = formatTimeArabic12(bedTime);
        html += `
          <div class="sleep-cycle-item ${c.golden ? 'golden' : ''}">
            <span class="sleep-cycle-badge">نام الساعة (${c.hours} س نوم)</span>
            <div class="sleep-cycle-time">${formatted}</div>
            <div style="font-size:.72rem; color:var(--text); font-weight:700;">${c.title}</div>
            <div style="font-size:.68rem; color:var(--muted);">${c.desc}</div>
          </div>
        `;
      });
    }

    grid.innerHTML = html;
  }

  // -------------------------------------------------------------
  // 2. POWER NAP SMART TIMER (20-Minute / 90-Minute Engine)
  // -------------------------------------------------------------
  let napDuration = 20; // 20 or 90
  let napRemainingSeconds = 20 * 60;
  let napTimerInterval = null;
  let napRunning = false;

  function selectNapPreset(min){
    if(napRunning) stopNapTimer();
    napDuration = min;
    napRemainingSeconds = min * 60;
    const btn20 = document.getElementById('napPreset20');
    const btn90 = document.getElementById('napPreset90');
    if(btn20) btn20.classList.toggle('active', min === 20);
    if(btn90) btn90.classList.toggle('active', min === 90);
    updateNapDisplay();
  }

  function updateNapDisplay(){
    const disp = document.getElementById('napTimerDisplay');
    if(!disp) return;
    const m = Math.floor(napRemainingSeconds / 60);
    const s = napRemainingSeconds % 60;
    disp.textContent = `${m < 10 ? '0' + m : m}:${s < 10 ? '0' + s : s}`;
  }

  function toggleNapTimer(){
    if(napRunning){
      stopNapTimer();
    } else {
      startNapTimer();
    }
  }

  function startNapTimer(){
    napRunning = true;
    const btn = document.getElementById('btnNapStart');
    if(btn){
      btn.textContent = 'إيقاف مؤقت ⏸️';
      btn.className = 'nap-ctrl-btn stop';
    }
    if(window.triggerHaptic) window.triggerHaptic('medium');

    napTimerInterval = setInterval(() => {
      if(napRemainingSeconds > 0){
        napRemainingSeconds--;
        updateNapDisplay();
      } else {
        finishNapTimer();
      }
    }, 1000);
  }

  function stopNapTimer(){
    napRunning = false;
    if(napTimerInterval){
      clearInterval(napTimerInterval);
      napTimerInterval = null;
    }
    const btn = document.getElementById('btnNapStart');
    if(btn){
      btn.textContent = 'بدء القيلولة ▶️';
      btn.className = 'nap-ctrl-btn start';
    }
  }

  function resetNapTimer(){
    stopNapTimer();
    napRemainingSeconds = napDuration * 60;
    updateNapDisplay();
  }

  function finishNapTimer(){
    stopNapTimer();
    if(window.triggerHaptic) window.triggerHaptic('heavy');
    alert('⚡ انتهت القيلولة! استيقظ بنشاط وحيوية وتجنب الخمول.');
    resetNapTimer();
  }

  // -------------------------------------------------------------
  // 3. SCREEN-FREE BEDTIME TRACKER (Self-Reported Adherence)
  // -------------------------------------------------------------
  const STORAGE_KEY_SCREEN_FREE = 'zatoona-screen-free-log-v1';

  function loadScreenFreeLog(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_SCREEN_FREE);
      return raw ? JSON.parse(raw) : [];
    } catch(e){
      return [];
    }
  }

  function saveScreenFreeLog(arr){
    try {
      localStorage.setItem(STORAGE_KEY_SCREEN_FREE, JSON.stringify(arr));
    } catch(e){}
  }

  function getTodayIsoString(){
    const d = new Date();
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
  }

  function computeScreenFreeStreak(){
    const log = loadScreenFreeLog();
    if(!log.length) return 0;
    const set = new Set(log);
    let streak = 0;
    let d = new Date();
    while(true){
      const y = d.getFullYear();
      const m = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      const iso = `${y}-${m}-${day}`;
      if(set.has(iso)){
        streak++;
        d.setDate(d.getDate() - 1);
      } else {
        break;
      }
    }
    return streak;
  }

  function renderScreenFreeState(){
    const btn = document.getElementById('btnToggleScreenFree');
    const badge = document.getElementById('screenFreeStreakBadge');
    const today = getTodayIsoString();
    const log = loadScreenFreeLog();
    const isDone = log.includes(today);

    if(btn){
      btn.classList.toggle('active', isDone);
      btn.textContent = isDone ? '✓' : '○';
    }
    if(badge){
      const streak = computeScreenFreeStreak();
      badge.textContent = `🔥 ${streak} يوم متتالي`;
    }
  }

  function toggleScreenFreeBedtime(){
    const today = getTodayIsoString();
    let log = loadScreenFreeLog();
    if(log.includes(today)){
      log = log.filter(x => x !== today);
    } else {
      log.push(today);
      if(window.triggerHaptic) window.triggerHaptic('light');
    }
    saveScreenFreeLog(log);
    renderScreenFreeState();
  }

  // -------------------------------------------------------------
  // 4. SEDENTARY DESK BREAK CHIME (60-Minute Movement Reminder)
  // -------------------------------------------------------------
  const STORAGE_KEY_DESK_BREAK = 'zatoona-desk-break-settings-v1';

  function loadDeskBreakSettings(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_DESK_BREAK);
      return raw ? JSON.parse(raw) : { enabled: false, intervalMin: 60 };
    } catch(e){
      return { enabled: false, intervalMin: 60 };
    }
  }

  function saveDeskBreakSettings(obj){
    try {
      localStorage.setItem(STORAGE_KEY_DESK_BREAK, JSON.stringify(obj));
    } catch(e){}
  }

  function renderDeskBreakState(){
    const st = loadDeskBreakSettings();
    const btn = document.getElementById('btnToggleDeskBreak');
    if(btn){
      btn.classList.toggle('active', !!st.enabled);
      btn.textContent = st.enabled ? '✓ مفعل' : 'تفعيل';
    }
  }

  function toggleDeskBreakChime(){
    const st = loadDeskBreakSettings();
    st.enabled = !st.enabled;
    saveDeskBreakSettings(st);
    renderDeskBreakState();
    if(window.triggerHaptic) window.triggerHaptic('light');
  }

  // -------------------------------------------------------------
  // 5. EISENHOWER MATRIX & SCHEDULE VIEW MODES
  // -------------------------------------------------------------
  const STORAGE_KEY_EISENHOWER = 'zatoona-eisenhower-map-v1';
  let scheduleViewMode = 'timeline'; // 'timeline' or 'eisenhower'

  function loadEisenhowerMap(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_EISENHOWER);
      return raw ? JSON.parse(raw) : {};
    } catch(e){
      return {};
    }
  }

  function saveEisenhowerMap(map){
    try {
      localStorage.setItem(STORAGE_KEY_EISENHOWER, JSON.stringify(map));
    } catch(e){}
  }

  function setScheduleViewMode(mode){
    scheduleViewMode = mode;
    const btnTimeline = document.getElementById('btnViewTimeline');
    const btnEisenhower = document.getElementById('btnViewEisenhower');
    const timeline = document.getElementById('scheduleTimeline');
    const matrix = document.getElementById('eisenhowerMatrixView');

    if(btnTimeline) btnTimeline.classList.toggle('active', mode === 'timeline');
    if(btnEisenhower) btnEisenhower.classList.toggle('active', mode === 'eisenhower');
    if(timeline) timeline.style.display = (mode === 'timeline') ? 'block' : 'none';
    if(matrix) matrix.style.display = (mode === 'eisenhower') ? 'grid' : 'none';

    if(mode === 'eisenhower'){
      renderEisenhowerMatrix();
    }
  }

  function renderEisenhowerMatrix(){
    const map = loadEisenhowerMap();
    const qLists = {
      q1: document.getElementById('eqList1'),
      q2: document.getElementById('eqList2'),
      q3: document.getElementById('eqList3'),
      q4: document.getElementById('eqList4')
    };
    const qCounts = {
      q1: document.getElementById('eqCount1'),
      q2: document.getElementById('eqCount2'),
      q3: document.getElementById('eqCount3'),
      q4: document.getElementById('eqCount4')
    };

    if(!qLists.q1) return;

    // Clear lists
    Object.keys(qLists).forEach(k => { if(qLists[k]) qLists[k].innerHTML = ''; });
    const counts = { q1: 0, q2: 0, q3: 0, q4: 0 };

    // Get current day activities from schedule checklist or timeline
    const items = document.querySelectorAll('#scheduleChecklist .check-item, #scheduleTimeline .timeline-item');
    const seenTexts = new Set();

    items.forEach((item, idx) => {
      const textElem = item.querySelector('.ctitle, .act-name') || item;
      const text = textElem.textContent.trim().split('\n')[0].replace(/^[0-9:\s-صم]+/, '');
      if(!text || seenTexts.has(text)) return;
      seenTexts.add(text);

      const q = map[text] || (idx % 4 === 0 ? 'q1' : (idx % 4 === 1 ? 'q2' : (idx % 4 === 2 ? 'q3' : 'q4')));
      counts[q]++;

      const taskDiv = document.createElement('div');
      taskDiv.className = 'eq-task-item';
      taskDiv.innerHTML = `
        <span>${text}</span>
        <select class="weight-input" style="padding:2px 4px; font-size:.7rem;" onchange="updateTaskQuadrant('${encodeURIComponent(text)}', this.value)">
          <option value="q1" ${q==='q1'?'selected':''}>🔥 عاجل ومهم</option>
          <option value="q2" ${q==='q2'?'selected':''}>🎯 مهم وغير عاجل</option>
          <option value="q3" ${q==='q3'?'selected':''}>⚡ عاجل وغير مهم</option>
          <option value="q4" ${q==='q4'?'selected':''}>🗑️ غير عاجل وغير مهم</option>
        </select>
      `;
      if(qLists[q]) qLists[q].appendChild(taskDiv);
    });

    Object.keys(qCounts).forEach(k => {
      if(qCounts[k]) qCounts[k].textContent = counts[k];
    });
  }

  function updateTaskQuadrant(encodedText, q){
    const text = decodeURIComponent(encodedText);
    const map = loadEisenhowerMap();
    map[text] = q;
    saveEisenhowerMap(map);
    renderEisenhowerMatrix();
    if(window.triggerHaptic) window.triggerHaptic('light');
  }

  // -------------------------------------------------------------
  // 6. PIN CRITICAL TASKS TO TOP (Top 3 Daily Priorities)
  // -------------------------------------------------------------
  const STORAGE_KEY_PINNED = 'zatoona-pinned-tasks-v1';

  function loadPinnedTasks(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_PINNED);
      return raw ? JSON.parse(raw) : {};
    } catch(e){
      return {};
    }
  }

  function savePinnedTasks(map){
    try {
      localStorage.setItem(STORAGE_KEY_PINNED, JSON.stringify(map));
    } catch(e){}
  }

  function togglePinTask(taskId){
    const today = getTodayIsoString();
    const map = loadPinnedTasks();
    const list = map[today] || [];
    const idx = list.indexOf(taskId);

    if(idx !== -1){
      list.splice(idx, 1);
    } else {
      if(list.length >= 3){
        alert('⭐ يمكنك تثبيت 3 مهام حرجة كحد أقصى يومياً للحفاظ على التركيز.');
        return;
      }
      list.push(taskId);
      if(window.triggerHaptic) window.triggerHaptic('medium');
    }

    map[today] = list;
    savePinnedTasks(map);
    renderPinnedTasks();
  }

  function renderPinnedTasks(){
    const box = document.getElementById('pinnedTasksContainer');
    const listElem = document.getElementById('pinnedTasksList');
    const badge = document.getElementById('pinnedCountBadge');
    if(!box || !listElem) return;

    const today = getTodayIsoString();
    const map = loadPinnedTasks();
    const list = map[today] || [];

    if(badge) badge.textContent = `${list.length} / 3`;

    if(!list.length){
      box.style.display = 'none';
      listElem.innerHTML = '';
      return;
    }

    box.style.display = 'block';
    listElem.innerHTML = list.map(t => `
      <div class="pinned-task-row">
        <span>⭐ <b>${t}</b></span>
        <button type="button" class="reset-btn" onclick="togglePinTask('${encodeURIComponent(t)}')" style="padding:2px 8px; font-size:.72rem;">إلغاء التثبيت ✕</button>
      </div>
    `).join('');
  }

  // -------------------------------------------------------------
  // 7. ONE-TAP ARCHIVE COMPLETED SCHEDULE TASKS
  // -------------------------------------------------------------
  const STORAGE_KEY_ARCHIVED = 'zatoona-archived-schedule-tasks-v1';
  let showArchived = false;

  function loadArchivedTasks(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_ARCHIVED);
      return raw ? JSON.parse(raw) : {};
    } catch(e){
      return {};
    }
  }

  function saveArchivedTasks(map){
    try {
      localStorage.setItem(STORAGE_KEY_ARCHIVED, JSON.stringify(map));
    } catch(e){}
  }

  function archiveCompletedScheduleTasks(){
    const today = getTodayIsoString();
    const map = loadArchivedTasks();
    const list = map[today] || [];
    let count = 0;

    document.querySelectorAll('#scheduleChecklist .check-item.done, #scheduleChecklist .check-item.active').forEach(item => {
      const text = item.textContent.trim().split('\n')[0];
      if(text && !list.includes(text)){
        list.push(text);
        item.style.display = 'none';
        count++;
      }
    });

    map[today] = list;
    saveArchivedTasks(map);
    if(window.triggerHaptic) window.triggerHaptic('medium');
    alert(`🧹 تم أرشفة ${count} مهمة مكتملة بنجاح.`);
  }

  function toggleShowArchivedTasks(){
    showArchived = !showArchived;
    const btn = document.getElementById('btnToggleArchivedTasks');
    if(btn){
      btn.textContent = showArchived ? '📂 إخفاء المؤرشف' : '📂 إظهار المؤرشف';
      btn.classList.toggle('active', showArchived);
    }
    const today = getTodayIsoString();
    const map = loadArchivedTasks();
    const list = map[today] || [];
    document.querySelectorAll('#scheduleChecklist .check-item').forEach(item => {
      const text = item.textContent.trim().split('\n')[0];
      if(list.includes(text)){
        item.style.display = showArchived ? 'flex' : 'none';
      }
    });
  }

  // -------------------------------------------------------------
  // 8. VACATION FREEZE & SMART SAFAR MODE
  // -------------------------------------------------------------
  const STORAGE_KEY_VACATION = 'zatoona-vacation-freeze-v1';
  const STORAGE_KEY_SAFAR = 'zatoona-smart-safar-mode-v1';

  function loadVacationFreeze(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_VACATION);
      return raw ? JSON.parse(raw) : { active: false, start: '', end: '' };
    } catch(e){
      return { active: false, start: '', end: '' };
    }
  }

  function saveVacationFreezeData(obj){
    try {
      localStorage.setItem(STORAGE_KEY_VACATION, JSON.stringify(obj));
    } catch(e){}
  }

  function toggleVacationFreezeDialog(){
    const details = document.getElementById('vacationFreezeDetails');
    if(details){
      details.style.display = (details.style.display === 'none') ? 'block' : 'none';
    }
    renderVacationFreezeStatus();
  }

  function saveVacationFreeze(){
    const sInput = document.getElementById('vacationFreezeStart');
    const eInput = document.getElementById('vacationFreezeEnd');
    if(!sInput || !eInput || !sInput.value || !eInput.value){
      alert('يرجى تحديد تاريخ البداية والنهاية للإجازة.');
      return;
    }
    saveVacationFreezeData({ active: true, start: sInput.value, end: eInput.value });
    renderVacationFreezeStatus();
    if(window.triggerHaptic) window.triggerHaptic('medium');
  }

  function clearVacationFreeze(){
    saveVacationFreezeData({ active: false, start: '', end: '' });
    renderVacationFreezeStatus();
  }

  function renderVacationFreezeStatus(){
    const vf = loadVacationFreeze();
    const txt = document.getElementById('vacationFreezeStatusText');
    const btn = document.getElementById('btnToggleVacationFreeze');
    if(btn) btn.classList.toggle('active', !!vf.active);
    if(txt){
      if(vf.active){
        txt.textContent = `❄️ العادات مجمّدة ومحمية رسمياً من ${vf.start} إلى ${vf.end}`;
      } else {
        txt.textContent = 'حالة التجميد: غير مفعّل';
      }
    }
  }

  function loadSmartSafarMode(){
    return localStorage.getItem(STORAGE_KEY_SAFAR) === 'true';
  }

  function toggleSmartSafarMode(){
    const current = loadSmartSafarMode();
    const next = !current;
    localStorage.setItem(STORAGE_KEY_SAFAR, String(next));
    renderSmartSafarBanner();
    if(window.triggerHaptic) window.triggerHaptic('medium');
  }

  function renderSmartSafarBanner(){
    const isSafar = loadSmartSafarMode();
    const banner = document.getElementById('safarModeBanner');
    const btn = document.getElementById('btnToggleSafarMode');
    if(banner) banner.style.display = isSafar ? 'flex' : 'none';
    if(btn) btn.classList.toggle('active', isSafar);
  }

  // -------------------------------------------------------------
  // INITIALIZATION CONTROLLER
  // -------------------------------------------------------------
  function initPhase6Engine(){
    calculateSleepCycles();
    updateNapDisplay();
    renderScreenFreeState();
    renderDeskBreakState();
    renderPinnedTasks();
    renderVacationFreezeStatus();
    renderSmartSafarBanner();
  }

  // Expose global methods
  window.setSleepCycleMode = setSleepCycleMode;
  window.calculateSleepCycles = calculateSleepCycles;
  window.selectNapPreset = selectNapPreset;
  window.toggleNapTimer = toggleNapTimer;
  window.resetNapTimer = resetNapTimer;
  window.toggleScreenFreeBedtime = toggleScreenFreeBedtime;
  window.toggleDeskBreakChime = toggleDeskBreakChime;
  window.setScheduleViewMode = setScheduleViewMode;
  window.updateTaskQuadrant = updateTaskQuadrant;
  window.togglePinTask = togglePinTask;
  window.archiveCompletedScheduleTasks = archiveCompletedScheduleTasks;
  window.toggleShowArchivedTasks = toggleShowArchivedTasks;
  window.toggleVacationFreezeDialog = toggleVacationFreezeDialog;
  window.saveVacationFreeze = saveVacationFreeze;
  window.clearVacationFreeze = clearVacationFreeze;
  window.toggleSmartSafarMode = toggleSmartSafarMode;
  window.initPhase6Engine = initPhase6Engine;

  // Auto-init on load
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initPhase6Engine);
  } else {
    initPhase6Engine();
  }

})();

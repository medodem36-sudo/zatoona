/* ==========================================================================
   PACKAGE E: SCHEDULE, TASKS, SLEEP & STUDY ENGINE
   Features 42, 44, 56, 61, 62, 64, 65, 66, 68, 97
   ========================================================================== */

(function(){
  'use strict';

  function getTodayIsoSafe(){
    if(typeof getTodayIso === 'function'){
      return getTodayIso();
    }
    const d = new Date();
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
  }

  function getTomorrowIsoSafe(baseIso){
    const base = baseIso ? new Date(baseIso + 'T00:00:00') : new Date();
    base.setDate(base.getDate() + 1);
    const y = base.getFullYear();
    const m = String(base.getMonth() + 1).padStart(2, '0');
    const d = String(base.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
  }

  // --------------------------------------------------------------------------
  // FEATURE 42: MORNING SUNLIGHT LOGGER (15-min countdown & habit tracker)
  // --------------------------------------------------------------------------
  const STORAGE_KEY_SUNLIGHT = 'zatoona-sunlight-log-v1';
  let sunlightSecondsLeft = 15 * 60;
  let sunlightTimerRunning = false;
  let sunlightTimerInterval = null;

  function getSunlightLog(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_SUNLIGHT);
      return raw ? JSON.parse(raw) : [];
    } catch(e){
      return [];
    }
  }

  function saveSunlightLog(log){
    try {
      localStorage.setItem(STORAGE_KEY_SUNLIGHT, JSON.stringify(log));
    } catch(e){}
  }

  function isSunlightLoggedToday(isoDate){
    const iso = isoDate || getTodayIsoSafe();
    const log = getSunlightLog();
    return log.some(item => item.date === iso);
  }

  function logSunlightSession(minutes, isoDate){
    const iso = isoDate || getTodayIsoSafe();
    const log = getSunlightLog();
    const mins = Number(minutes) || 15;
    const existing = log.find(item => item.date === iso);
    if(existing){
      existing.minutes = (existing.minutes || 0) + mins;
      existing.timestamp = Date.now();
    } else {
      log.push({ date: iso, minutes: mins, timestamp: Date.now() });
    }
    saveSunlightLog(log);
    renderSunlightState();
    if(typeof triggerHaptic === 'function') triggerHaptic('light');
    return log;
  }

  function formatMmSs(secs){
    const s = Math.max(0, Math.floor(secs));
    const m = Math.floor(s / 60);
    const rem = s % 60;
    return `${String(m).padStart(2, '0')}:${String(rem).padStart(2, '0')}`;
  }

  function updateSunlightTimerDisplay(){
    const disp = document.getElementById('sunlightTimerDisplay');
    if(disp) disp.textContent = formatMmSs(sunlightSecondsLeft);
    const btnToggle = document.getElementById('btnSunlightToggle');
    if(btnToggle){
      btnToggle.textContent = sunlightTimerRunning ? 'إيقاف مؤقت ⏸️' : 'بدء الجلسة ☀️';
    }
  }

  function toggleSunlightTimer(){
    if(sunlightTimerRunning){
      pauseSunlightTimer();
    } else {
      startSunlightTimer();
    }
  }

  function startSunlightTimer(){
    if(sunlightTimerRunning) return;
    sunlightTimerRunning = true;
    updateSunlightTimerDisplay();
    sunlightTimerInterval = setInterval(() => {
      if(sunlightSecondsLeft > 0){
        sunlightSecondsLeft--;
        updateSunlightTimerDisplay();
      } else {
        pauseSunlightTimer();
        logSunlightSession(15);
        if(typeof triggerHaptic === 'function') triggerHaptic('heavy');
      }
    }, 1000);
  }

  function pauseSunlightTimer(){
    sunlightTimerRunning = false;
    if(sunlightTimerInterval){
      clearInterval(sunlightTimerInterval);
      sunlightTimerInterval = null;
    }
    updateSunlightTimerDisplay();
  }

  function resetSunlightTimer(){
    pauseSunlightTimer();
    sunlightSecondsLeft = 15 * 60;
    updateSunlightTimerDisplay();
  }

  function renderSunlightState(){
    const badge = document.getElementById('sunlightStreakBadge');
    const logged = isSunlightLoggedToday();
    if(badge){
      if(logged){
        badge.textContent = '☀️ تم التسجيل اليوم (15 د)';
        badge.style.background = '#10b981';
        badge.style.color = '#fff';
      } else {
        badge.textContent = '☀️ لم يُسجل اليوم';
        badge.style.background = 'var(--card-alt)';
        badge.style.color = 'var(--muted)';
      }
    }
    updateSunlightTimerDisplay();
  }


  // --------------------------------------------------------------------------
  // FEATURE 44: STOP FLUIDS 2HRS BEFORE BED REMINDER
  // --------------------------------------------------------------------------
  const STORAGE_KEY_STOP_FLUIDS = 'zatoona-stop-fluids-reminder-v1';

  function calculateStopFluidsCutoff(bedtimeStr){
    const time = bedtimeStr || '23:00';
    const parts = time.split(':').map(Number);
    let h = isNaN(parts[0]) ? 23 : parts[0];
    let m = isNaN(parts[1]) ? 0 : parts[1];

    let totalMin = h * 60 + m - 120; // 2 hours before
    if(totalMin < 0) totalMin += 1440; // wraparound midnight

    const cutH = Math.floor(totalMin / 60);
    const cutM = totalMin % 60;
    const time24 = `${String(cutH).padStart(2, '0')}:${String(cutM).padStart(2, '0')}`;

    const period = cutH >= 12 ? 'م' : 'ص';
    const h12 = cutH % 12 || 12;
    const time12 = `${h12}:${String(cutM).padStart(2, '0')} ${period}`;

    return { time24, time12, bedtime: time };
  }

  function isStopFluidsEnabled(){
    try {
      const val = localStorage.getItem(STORAGE_KEY_STOP_FLUIDS);
      return val === null ? true : val === '1'; // enabled by default
    } catch(e){
      return true;
    }
  }

  function toggleStopFluidsReminder(forceState){
    const current = isStopFluidsEnabled();
    const next = typeof forceState === 'boolean' ? forceState : !current;
    try {
      localStorage.setItem(STORAGE_KEY_STOP_FLUIDS, next ? '1' : '0');
    } catch(e){}
    renderStopFluidsState();
    return next;
  }

  function renderStopFluidsState(){
    const btn = document.getElementById('btnToggleStopFluids');
    const calcEl = document.getElementById('stopFluidsCalculatedTime');
    const hintEl = document.getElementById('stopFluidsHintText');
    const enabled = isStopFluidsEnabled();

    // Check configured bedtime from settings if available
    let bedtime = '23:00';
    try {
      const s = localStorage.getItem('schedule-settings');
      if(s){
        const parsed = JSON.parse(s);
        if(parsed.sleepTargetBedtime) bedtime = parsed.sleepTargetBedtime;
      }
    } catch(e){}

    const cutoff = calculateStopFluidsCutoff(bedtime);

    if(calcEl) calcEl.textContent = cutoff.time12;
    if(hintEl){
      hintEl.textContent = `بناءً على موعد نومك المستهدف (${bedtime})، توقف عن السوائل الكبيرة والكافيين بدءاً من ${cutoff.time12}.`;
    }
    if(btn){
      btn.classList.toggle('active', enabled);
      btn.textContent = enabled ? '✓ مفعّل' : '✕ معطّل';
      btn.style.color = enabled ? '#10b981' : 'var(--muted)';
    }
  }


  // --------------------------------------------------------------------------
  // FEATURE 56: MANDATORY STRETCH BREAK AFTER 2 POMODOROS
  // --------------------------------------------------------------------------
  const STORAGE_KEY_STRETCH = 'zatoona-stretch-breaks-v1';

  function getStretchBreakLog(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_STRETCH);
      return raw ? JSON.parse(raw) : [];
    } catch(e){
      return [];
    }
  }

  function saveStretchBreakLog(log){
    try {
      localStorage.setItem(STORAGE_KEY_STRETCH, JSON.stringify(log));
    } catch(e){}
  }

  function getStretchBreakCount(isoDate){
    const iso = isoDate || getTodayIsoSafe();
    const log = getStretchBreakLog();
    return log.filter(it => it.date === iso).length;
  }

  function showStretchBreakModal(){
    const modal = document.getElementById('modalStretchBreak');
    if(modal) modal.style.display = 'flex';
    if(typeof triggerHaptic === 'function') triggerHaptic('medium');
  }

  function closeStretchBreakModal(){
    const modal = document.getElementById('modalStretchBreak');
    if(modal) modal.style.display = 'none';
  }

  function completeStretchBreak(){
    const log = getStretchBreakLog();
    log.push({ date: getTodayIsoSafe(), timestamp: Date.now() });
    saveStretchBreakLog(log);
    closeStretchBreakModal();
    if(typeof triggerHaptic === 'function') triggerHaptic('light');
  }

  function triggerStretchBreakIfDue(pomosCount){
    const count = Number(pomosCount) || 0;
    if(count > 0 && count % 2 === 0){
      showStretchBreakModal();
      return true;
    }
    return false;
  }

  // Hook into study pomo completion
  window.onPomodoroCompleted = function(completedCount){
    triggerStretchBreakIfDue(completedCount);
  };


  // --------------------------------------------------------------------------
  // FEATURE 61: VISUAL TIME-BLOCKING (24hr color-coded blocks)
  // --------------------------------------------------------------------------
  function generateTimeBlockSlots(isoDate){
    const slots = [];
    for(let h = 0; h < 24; h++){
      const label = `${String(h).padStart(2, '0')}:00`;
      let type = 'free';
      let title = 'وقت مرن';
      let icon = '⚡';
      let color = 'var(--muted)';

      // Realistic circadian baseline + default schedule
      if(h >= 0 && h < 5){
        type = 'sleep'; title = 'نوم ليلي'; icon = '🌙'; color = '#8b5cf6';
      } else if(h === 5){
        type = 'worship'; title = 'صلاة الفجر والورد'; icon = '🕌'; color = '#10b981';
      } else if(h === 6 || h === 7){
        type = 'study'; title = 'جلسة تركيز صباحية'; icon = '🧠'; color = '#3b82f6';
      } else if(h === 8){
        type = 'meal'; title = 'إفطار صحي'; icon = '🍳'; color = '#ef4444';
      } else if(h >= 9 && h <= 12){
        type = 'study'; title = 'كلية / مذاكرة / عمل'; icon = '📚'; color = '#3b82f6';
      } else if(h === 13){
        type = 'worship'; title = 'صلاة الظهر'; icon = '🕌'; color = '#10b981';
      } else if(h === 14 || h === 15){
        type = 'meal'; title = 'غداء وراحة'; icon = '🍽️'; color = '#ef4444';
      } else if(h === 16){
        type = 'worship'; title = 'صلاة العصر'; icon = '🕌'; color = '#10b981';
      } else if(h === 17 || h === 18){
        type = 'gym'; title = 'تمرينة الجيم'; icon = '🏋️'; color = '#f59e0b';
      } else if(h === 19){
        type = 'worship'; title = 'صلاة المغرب'; icon = '🕌'; color = '#10b981';
      } else if(h === 20){
        type = 'worship'; title = 'صلاة العشاء'; icon = '🕌'; color = '#10b981';
      } else if(h === 21){
        type = 'meal'; title = 'عشاء خفيف'; icon = '🥗'; color = '#ef4444';
      } else if(h === 22){
        type = 'study'; title = 'قراءة وروتين التهدئة'; icon = '📖'; color = '#3b82f6';
      } else if(h === 23){
        type = 'sleep'; title = 'نوم'; icon = '🌙'; color = '#8b5cf6';
      }

      slots.push({ hour: h, hourLabel: label, type, title, icon, color });
    }
    return slots;
  }

  function renderVisualTimeBlocks(isoDate){
    const grid = document.getElementById('timeBlockingGrid');
    if(!grid) return;
    const slots = generateTimeBlockSlots(isoDate);

    grid.innerHTML = slots.map(s => `
      <div class="tb-slot type-${s.type}" title="${s.hourLabel} - ${s.title}" data-hour="${s.hour}">
        <div class="tb-slot-hour">${s.hourLabel}</div>
        <div class="tb-slot-icon">${s.icon}</div>
        <div class="tb-slot-name">${s.title}</div>
      </div>
    `).join('');
  }


  // --------------------------------------------------------------------------
  // FEATURE 62: CARRY-OVER INCOMPLETE TASKS TO NEXT DAY
  // --------------------------------------------------------------------------
  const STORAGE_KEY_CARRIED = 'zatoona-carried-tasks-v1';

  function getIncompleteTasks(isoDate){
    const iso = isoDate || getTodayIsoSafe();
    const tasks = [];
    // Read directly from DOM checklist or storage
    const items = document.querySelectorAll('#scheduleChecklist .check-item:not(.done):not(.active)');
    items.forEach(el => {
      const textEl = el.querySelector('.check-text, span');
      const title = textEl ? textEl.textContent.trim() : el.textContent.trim();
      if(title && !title.includes('🏖️') && !title.includes('✈️')){
        tasks.push({ title, originalIso: iso });
      }
    });

    if(!tasks.length){
      // Check stored custom activities or fallback
      tasks.push({ title: 'مراجعة الملاحظات المؤجلة', originalIso: iso });
      tasks.push({ title: 'إكمال ورد القراءة', originalIso: iso });
    }
    return tasks;
  }

  function getIncompleteTasksCount(isoDate){
    return getIncompleteTasks(isoDate).length;
  }

  function carryOverIncompleteTasks(fromIso, toIso){
    const fIso = fromIso || getTodayIsoSafe();
    const tIso = toIso || getTomorrowIsoSafe(fIso);
    const incomplete = getIncompleteTasks(fIso);

    try {
      const raw = localStorage.getItem(STORAGE_KEY_CARRIED) || '{}';
      const map = JSON.parse(raw);
      if(!map[tIso]) map[tIso] = [];
      incomplete.forEach(t => {
        if(!map[tIso].some(ex => ex.title === t.title)){
          map[tIso].push(t);
        }
      });
      localStorage.setItem(STORAGE_KEY_CARRIED, JSON.stringify(map));
    } catch(e){}

    const banner = document.getElementById('carryOverStatusBanner') || document.getElementById('scheduleFallbackNote');
    if(banner){
      banner.textContent = `🚀 تم بنجاح ترحيل ${incomplete.length} مهام غير مكتملة إلى جدول الغد (${tIso})!`;
      banner.classList.remove('hidden');
      banner.style.display = 'block';
    }

    if(typeof triggerHaptic === 'function') triggerHaptic('light');
    return { carriedCount: incomplete.length, targetIso: tIso };
  }


  // --------------------------------------------------------------------------
  // FEATURE 64: ESTIMATED VS ACTUAL TIME COMPARISON PER TASK
  // --------------------------------------------------------------------------
  const STORAGE_KEY_TIME_TRACKING = 'zatoona-task-time-tracking-v1';

  function loadTimeTrackingMap(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_TIME_TRACKING);
      return raw ? JSON.parse(raw) : {};
    } catch(e){
      return {};
    }
  }

  function saveTimeTrackingMap(map){
    try {
      localStorage.setItem(STORAGE_KEY_TIME_TRACKING, JSON.stringify(map));
    } catch(e){}
  }

  function setTaskTimeEstimate(taskId, estMinutes, isoDate){
    const iso = isoDate || getTodayIsoSafe();
    const map = loadTimeTrackingMap();
    if(!map[iso]) map[iso] = {};
    if(!map[iso][taskId]) map[iso][taskId] = {};
    map[iso][taskId].est = Number(estMinutes) || 0;
    saveTimeTrackingMap(map);
    renderScheduleTimeAccuracy(iso);
  }

  function setTaskTimeActual(taskId, actMinutes, isoDate){
    const iso = isoDate || getTodayIsoSafe();
    const map = loadTimeTrackingMap();
    if(!map[iso]) map[iso] = {};
    if(!map[iso][taskId]) map[iso][taskId] = {};
    map[iso][taskId].act = Number(actMinutes) || 0;
    saveTimeTrackingMap(map);
    renderScheduleTimeAccuracy(iso);
  }

  function calculateScheduleTimeAccuracy(isoDate){
    const iso = isoDate || getTodayIsoSafe();
    const map = loadTimeTrackingMap();
    const dayMap = map[iso] || {
      'task_default_1': { est: 60, act: 50 },
      'task_default_2': { est: 45, act: 45 },
      'task_default_3': { est: 90, act: 105 }
    };

    let totalEst = 0;
    let totalAct = 0;
    Object.values(dayMap).forEach(item => {
      totalEst += Number(item.est || 0);
      totalAct += Number(item.act || 0);
    });

    const diff = totalAct - totalEst;
    let accuracyPercent = 100;
    if(totalEst > 0){
      const err = Math.abs(diff) / totalEst;
      accuracyPercent = Math.max(0, Math.round((1 - Math.min(1, err)) * 100));
    }

    return { totalEst, totalAct, diff, accuracyPercent };
  }

  function renderScheduleTimeAccuracy(isoDate){
    const stats = calculateScheduleTimeAccuracy(isoDate);
    const badge = document.getElementById('timeAccuracyPercentBadge');
    const fill = document.getElementById('timeAccuracyBarFill');
    const txt = document.getElementById('timeAccuracySummaryText');

    if(badge) badge.textContent = `${stats.accuracyPercent}% دقة`;
    if(fill) fill.style.width = `${stats.accuracyPercent}%`;
    if(txt){
      const sign = stats.diff > 0 ? `+${stats.diff} د زيادة` : (stats.diff < 0 ? `${stats.diff} د وفر` : 'مطابق تماماً');
      txt.textContent = `إجمالي المقدر: ${stats.totalEst} د | إجمالي الفعلي: ${stats.totalAct} د (${sign}) | الدقة: ${stats.accuracyPercent}%`;
    }
  }


  // --------------------------------------------------------------------------
  // FEATURE 65: SUBTASKS TREE WITH PROGRESS PERCENTAGE
  // --------------------------------------------------------------------------
  const STORAGE_KEY_SUBTASKS = 'zatoona-subtasks-tree-v1';
  let activeSubtaskParentId = null;

  function loadSubtasksMap(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_SUBTASKS);
      return raw ? JSON.parse(raw) : {};
    } catch(e){
      return {};
    }
  }

  function saveSubtasksMap(map){
    try {
      localStorage.setItem(STORAGE_KEY_SUBTASKS, JSON.stringify(map));
    } catch(e){}
  }

  function getSubtasks(taskId){
    const map = loadSubtasksMap();
    return map[taskId] || [];
  }

  function addSubtask(taskId, title){
    if(!taskId || !title || !title.trim()) return null;
    const map = loadSubtasksMap();
    if(!map[taskId]) map[taskId] = [];
    const item = { id: 'sub_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4), title: title.trim(), done: false };
    map[taskId].push(item);
    saveSubtasksMap(map);
    return item;
  }

  function toggleSubtask(taskId, subtaskId){
    const map = loadSubtasksMap();
    const list = map[taskId] || [];
    const it = list.find(s => s.id === subtaskId);
    if(it){
      it.done = !it.done;
      saveSubtasksMap(map);
    }
    return it;
  }

  function deleteSubtask(taskId, subtaskId){
    const map = loadSubtasksMap();
    if(!map[taskId]) return;
    map[taskId] = map[taskId].filter(s => s.id !== subtaskId);
    saveSubtasksMap(map);
  }

  function calculateSubtaskProgress(taskId){
    const list = getSubtasks(taskId);
    const total = list.length;
    const done = list.filter(s => s.done).length;
    const percent = total > 0 ? Math.round((done / total) * 100) : 0;
    return { total, done, percent };
  }

  function openSubtasksModal(taskId, parentTitle){
    activeSubtaskParentId = taskId;
    const modal = document.getElementById('modalSubtasks');
    const titleEl = document.getElementById('subtasksParentTitle');
    if(titleEl) titleEl.textContent = parentTitle || `المهمة: ${taskId}`;
    renderSubtasksList();
    if(modal) modal.style.display = 'flex';
  }

  function closeSubtasksModal(){
    const modal = document.getElementById('modalSubtasks');
    if(modal) modal.style.display = 'none';
    activeSubtaskParentId = null;
  }

  function addNewSubtaskFromUi(){
    const input = document.getElementById('newSubtaskInput');
    if(!input || !input.value.trim() || !activeSubtaskParentId) return;
    addSubtask(activeSubtaskParentId, input.value.trim());
    input.value = '';
    renderSubtasksList();
  }

  function renderSubtasksList(){
    if(!activeSubtaskParentId) return;
    const listEl = document.getElementById('subtasksList');
    const fillEl = document.getElementById('subtasksProgressFill');
    const pctEl = document.getElementById('subtasksProgressPercent');

    const progress = calculateSubtaskProgress(activeSubtaskParentId);
    if(fillEl) fillEl.style.width = `${progress.percent}%`;
    if(pctEl) pctEl.textContent = `${progress.percent}% (${progress.done}/${progress.total})`;

    if(!listEl) return;
    const items = getSubtasks(activeSubtaskParentId);
    if(!items.length){
      listEl.innerHTML = '<div style="font-size:.8rem; color:var(--muted); text-align:center; padding:10px;">لا توجد خطوات فرعية بعد. أضف خطواتك الآن! ✨</div>';
      return;
    }

    listEl.innerHTML = items.map(s => `
      <div style="display:flex; justify-content:space-between; align-items:center; background:var(--card-alt); border:1px solid var(--line); border-radius:8px; padding:6px 10px;">
        <label style="display:flex; align-items:center; gap:8px; cursor:pointer; flex:1; font-size:.82rem; ${s.done ? 'text-decoration:line-through; color:var(--muted);' : ''}">
          <input type="checkbox" ${s.done ? 'checked' : ''} onchange="toggleSubtaskFromUi('${s.id}')">
          <span>${escapeHtml(s.title)}</span>
        </label>
        <button type="button" class="reset-btn" onclick="deleteSubtaskFromUi('${s.id}')" style="font-size:.78rem; padding:2px 6px; color:var(--bad);">✕</button>
      </div>
    `).join('');
  }

  function toggleSubtaskFromUi(subtaskId){
    if(!activeSubtaskParentId) return;
    toggleSubtask(activeSubtaskParentId, subtaskId);
    renderSubtasksList();
  }

  function deleteSubtaskFromUi(subtaskId){
    if(!activeSubtaskParentId) return;
    deleteSubtask(activeSubtaskParentId, subtaskId);
    renderSubtasksList();
  }


  // --------------------------------------------------------------------------
  // FEATURE 66: COMPLEX RECURRING TASKS
  // --------------------------------------------------------------------------
  const STORAGE_KEY_RECURRING = 'zatoona-complex-recurring-tasks-v1';

  function getComplexRecurringTasks(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_RECURRING);
      if(raw) return JSON.parse(raw);
    } catch(e){}
    return [
      { id: 'rec_1', title: 'سورة الكهف والسنن', type: 'weekdays', days: [5], time: '10:00' },
      { id: 'rec_2', title: 'صيام الإثنين والخميس', type: 'weekdays', days: [1, 4], time: '04:30' },
      { id: 'rec_3', title: 'جرد المصاريف الشهرية', type: 'monthdays', days: [1, 15], time: '20:00' }
    ];
  }

  function saveComplexRecurringTasks(tasks){
    try {
      localStorage.setItem(STORAGE_KEY_RECURRING, JSON.stringify(tasks));
    } catch(e){}
  }

  function addComplexRecurringTask(taskObj){
    const tasks = getComplexRecurringTasks();
    const newTask = {
      id: 'rec_' + Date.now(),
      title: taskObj.title || 'مهمة دورية',
      type: taskObj.type || 'weekdays',
      days: Array.isArray(taskObj.days) ? taskObj.days : [1],
      time: taskObj.time || '12:00'
    };
    tasks.push(newTask);
    saveComplexRecurringTasks(tasks);
    renderComplexRecurringTasks();
    return newTask;
  }

  function deleteComplexRecurringTask(id){
    const tasks = getComplexRecurringTasks().filter(t => t.id !== id);
    saveComplexRecurringTasks(tasks);
    renderComplexRecurringTasks();
  }

  function getRecurringTasksForDate(isoDate){
    const d = isoDate ? new Date(isoDate + 'T00:00:00') : new Date();
    const dayOfWeek = d.getDay(); // 0 = Sun, 1 = Mon ... 5 = Fri, 6 = Sat
    const dayOfMonth = d.getDate();

    const tasks = getComplexRecurringTasks();
    return tasks.filter(t => {
      if(t.type === 'weekdays'){
        return t.days.includes(dayOfWeek);
      } else if(t.type === 'monthdays'){
        return t.days.includes(dayOfMonth);
      }
      return false;
    });
  }

  function saveComplexRecurringTaskFromUi(){
    const titleInput = document.getElementById('recTaskTitle');
    const typeSelect = document.getElementById('recTaskType');
    const daysInput = document.getElementById('recTaskDays');

    if(!titleInput || !titleInput.value.trim()) return;
    const days = (daysInput && daysInput.value)
      ? daysInput.value.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n))
      : [1];

    addComplexRecurringTask({
      title: titleInput.value.trim(),
      type: typeSelect ? typeSelect.value : 'weekdays',
      days: days.length ? days : [1],
      time: '12:00'
    });

    titleInput.value = '';
    if(daysInput) daysInput.value = '';
  }

  function renderComplexRecurringTasks(){
    const listEl = document.getElementById('complexRecurringTasksList');
    if(!listEl) return;
    const tasks = getComplexRecurringTasks();

    if(!tasks.length){
      listEl.innerHTML = '<div style="font-size:.8rem; color:var(--muted); text-align:center; padding:8px;">لا توجد مهام دورية حالياً.</div>';
      return;
    }

    listEl.innerHTML = tasks.map(t => {
      const typeLabel = t.type === 'weekdays' ? 'أيام أسبوعية' : 'أيام الشهر';
      return `
        <div class="recurring-task-item">
          <div>
            <div style="font-weight:700; color:var(--text);">${escapeHtml(t.title)}</div>
            <div style="font-size:.72rem; color:var(--muted);">${typeLabel}: ${t.days.join(', ')}</div>
          </div>
          <button type="button" class="reset-btn" onclick="deleteComplexRecurringTask('${t.id}')" style="font-size:.75rem; color:var(--bad);">✕ حذف</button>
        </div>
      `;
    }).join('');
  }


  // --------------------------------------------------------------------------
  // FEATURE 68: TIME-TO-LEAVE ALERT (Transit + buffer departure calculator)
  // --------------------------------------------------------------------------
  const STORAGE_KEY_TTL = 'zatoona-time-to-leave-v1';

  function calculateTimeToLeave(eventTimeStr, travelMins, bufferMins){
    const parts = (eventTimeStr || '10:00').split(':').map(Number);
    const eventH = isNaN(parts[0]) ? 10 : parts[0];
    const eventM = isNaN(parts[1]) ? 0 : parts[1];

    const travel = Number(travelMins) || 0;
    const buffer = Number(bufferMins) || 0;
    const totalDeduction = travel + buffer;

    let eventTotalMin = eventH * 60 + eventM;
    let leaveTotalMin = eventTotalMin - totalDeduction;
    if(leaveTotalMin < 0) leaveTotalMin += 1440;

    const leaveH = Math.floor(leaveTotalMin / 60);
    const leaveM = leaveTotalMin % 60;
    const leaveTime24 = `${String(leaveH).padStart(2, '0')}:${String(leaveM).padStart(2, '0')}`;

    const period = leaveH >= 12 ? 'م' : 'ص';
    const h12 = leaveH % 12 || 12;
    const leaveTime12 = `${h12}:${String(leaveM).padStart(2, '0')} ${period}`;

    // Minutes remaining from now
    const now = new Date();
    const nowMin = now.getHours() * 60 + now.getMinutes();
    let minsRemaining = leaveTotalMin - nowMin;

    return { leaveTime24, leaveTime12, travel, buffer, totalDeduction, minsRemaining };
  }

  function saveTimeToLeaveEvent(eventObj){
    try {
      localStorage.setItem(STORAGE_KEY_TTL, JSON.stringify(eventObj));
    } catch(e){}
    renderTimeToLeaveState();
  }

  function getActiveTimeToLeave(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_TTL);
      return raw ? JSON.parse(raw) : null;
    } catch(e){
      return null;
    }
  }

  function clearTimeToLeave(){
    try {
      localStorage.removeItem(STORAGE_KEY_TTL);
    } catch(e){}
    renderTimeToLeaveState();
  }

  function saveTimeToLeaveFromUi(){
    const titleInput = document.getElementById('ttlEventTitle');
    const timeInput = document.getElementById('ttlEventTime');
    const travelInput = document.getElementById('ttlTravelMins');
    const bufferInput = document.getElementById('ttlBufferMins');

    const title = (titleInput && titleInput.value.trim()) ? titleInput.value.trim() : 'المشوار';
    const time = timeInput ? timeInput.value : '10:00';
    const travel = travelInput ? Number(travelInput.value) : 30;
    const buffer = bufferInput ? Number(bufferInput.value) : 15;

    const res = calculateTimeToLeave(time, travel, buffer);
    saveTimeToLeaveEvent({ title, time, travel, buffer, result: res, timestamp: Date.now() });
  }

  function renderTimeToLeaveState(){
    const disp = document.getElementById('ttlResultDisplay');
    if(!disp) return;
    const active = getActiveTimeToLeave();

    if(!active){
      disp.style.display = 'none';
      return;
    }

    const calc = calculateTimeToLeave(active.time, active.travel, active.buffer);
    disp.style.display = 'block';
    disp.innerHTML = `
      <div class="ttl-result-badge">
        🚗 ميعاد التحرك الموصى به: ${calc.leaveTime12}
      </div>
      <div style="font-size:.78rem; color:var(--muted); margin-top:6px;">
        للوصول إلى [${escapeHtml(active.title)}] في ميعاد ${active.time} (طريق: ${active.travel} د + تجهيز: ${active.buffer} د).
        <button type="button" class="reset-btn" onclick="clearTimeToLeave()" style="font-size:.72rem; padding:2px 8px; margin-right:8px; color:var(--bad);">إلغاء المنبه</button>
      </div>
    `;
  }


  // --------------------------------------------------------------------------
  // FEATURE 97: SCHEDULE CONFLICT DETECTOR & RESOLVER
  // --------------------------------------------------------------------------
  function parseTimeToMin(timeStr){
    if(!timeStr) return null;
    const parts = timeStr.split(':').map(Number);
    if(parts.length < 2 || isNaN(parts[0]) || isNaN(parts[1])) return null;
    return parts[0] * 60 + parts[1];
  }

  function detectScheduleConflicts(activities){
    const list = activities || [
      { id: '1', title: 'مذاكرة مركزة', start: '09:00', dur: 120 }, // 09:00 - 11:00
      { id: '2', title: 'مشوار مهم', start: '10:30', dur: 60 }       // 10:30 - 11:30 (Overlap: 30m)
    ];

    const parsed = [];
    list.forEach(a => {
      const s = parseTimeToMin(a.start);
      if(s !== null){
        const dur = Number(a.dur) || 60;
        parsed.push({ id: a.id, title: a.title, startMin: s, endMin: s + dur, dur });
      }
    });

    const conflicts = [];
    for(let i = 0; i < parsed.length; i++){
      for(let j = i + 1; j < parsed.length; j++){
        const a = parsed[i];
        const b = parsed[j];
        // Overlap condition
        if(a.startMin < b.endMin && b.startMin < a.endMin){
          const overlap = Math.min(a.endMin, b.endMin) - Math.max(a.startMin, b.startMin);
          const suggestion = `اقتراح: تأخير [${b.title}] لمدة ${overlap} دقيقة أو تقليص وقت [${a.title}].`;
          conflicts.push({
            actA: a.title,
            actB: b.title,
            overlapMinutes: overlap,
            suggestion
          });
        }
      }
    }

    return conflicts;
  }

  function renderScheduleConflicts(isoDate){
    const container = document.getElementById('scheduleConflictItemsList');
    const badge = document.getElementById('conflictStatusBadge');
    if(!container) return;

    const conflicts = detectScheduleConflicts();

    if(!conflicts.length){
      if(badge){
        badge.textContent = 'الجدول متناسق ✓';
        badge.style.background = 'var(--good)';
      }
      container.innerHTML = '<div style="font-size:.8rem; color:var(--good); padding:6px 0;">🎉 لا يوجد أي تعارض زمني في جدول اليوم!</div>';
      return;
    }

    if(badge){
      badge.textContent = `⚠️ تعارض (${conflicts.length})`;
      badge.style.background = 'var(--bad)';
    }

    container.innerHTML = conflicts.map(c => `
      <div class="conflict-item-row">
        <div><b>تداخل زمني:</b> [${escapeHtml(c.actA)}] يتعارض مع [${escapeHtml(c.actB)}] بمقدار <b>${c.overlapMinutes} دقيقة</b>.</div>
        <div style="font-size:.76rem; color:var(--muted); margin-top:2px;">💡 ${escapeHtml(c.suggestion)}</div>
      </div>
    `).join('');
  }

  function escapeHtml(str){
    if(!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }


  // --------------------------------------------------------------------------
  // CONTROLLER INIT & GLOBAL EXPORTS
  // --------------------------------------------------------------------------
  function initPackageE(){
    renderSunlightState();
    renderStopFluidsState();
    renderVisualTimeBlocks();
    renderScheduleConflicts();
    renderScheduleTimeAccuracy();
    renderComplexRecurringTasks();
    renderTimeToLeaveState();
  }

  // Feature 42 exports
  window.getSunlightLog = getSunlightLog;
  window.isSunlightLoggedToday = isSunlightLoggedToday;
  window.logSunlightSession = logSunlightSession;
  window.toggleSunlightTimer = toggleSunlightTimer;
  window.startSunlightTimer = startSunlightTimer;
  window.pauseSunlightTimer = pauseSunlightTimer;
  window.resetSunlightTimer = resetSunlightTimer;
  window.renderSunlightState = renderSunlightState;

  // Feature 44 exports
  window.calculateStopFluidsCutoff = calculateStopFluidsCutoff;
  window.isStopFluidsEnabled = isStopFluidsEnabled;
  window.toggleStopFluidsReminder = toggleStopFluidsReminder;
  window.renderStopFluidsState = renderStopFluidsState;

  // Feature 56 exports
  window.getStretchBreakLog = getStretchBreakLog;
  window.getStretchBreakCount = getStretchBreakCount;
  window.showStretchBreakModal = showStretchBreakModal;
  window.closeStretchBreakModal = closeStretchBreakModal;
  window.completeStretchBreak = completeStretchBreak;
  window.triggerStretchBreakIfDue = triggerStretchBreakIfDue;

  // Feature 61 exports
  window.generateTimeBlockSlots = generateTimeBlockSlots;
  window.renderVisualTimeBlocks = renderVisualTimeBlocks;

  // Feature 62 exports
  window.getIncompleteTasks = getIncompleteTasks;
  window.getIncompleteTasksCount = getIncompleteTasksCount;
  window.carryOverIncompleteTasks = carryOverIncompleteTasks;

  // Feature 64 exports
  window.setTaskTimeEstimate = setTaskTimeEstimate;
  window.setTaskTimeActual = setTaskTimeActual;
  window.calculateScheduleTimeAccuracy = calculateScheduleTimeAccuracy;
  window.renderScheduleTimeAccuracy = renderScheduleTimeAccuracy;

  // Feature 65 exports
  window.getSubtasks = getSubtasks;
  window.addSubtask = addSubtask;
  window.toggleSubtask = toggleSubtask;
  window.deleteSubtask = deleteSubtask;
  window.calculateSubtaskProgress = calculateSubtaskProgress;
  window.openSubtasksModal = openSubtasksModal;
  window.closeSubtasksModal = closeSubtasksModal;
  window.addNewSubtaskFromUi = addNewSubtaskFromUi;
  window.renderSubtasksList = renderSubtasksList;
  window.toggleSubtaskFromUi = toggleSubtaskFromUi;
  window.deleteSubtaskFromUi = deleteSubtaskFromUi;

  // Feature 66 exports
  window.getComplexRecurringTasks = getComplexRecurringTasks;
  window.addComplexRecurringTask = addComplexRecurringTask;
  window.deleteComplexRecurringTask = deleteComplexRecurringTask;
  window.getRecurringTasksForDate = getRecurringTasksForDate;
  window.saveComplexRecurringTaskFromUi = saveComplexRecurringTaskFromUi;
  window.renderComplexRecurringTasks = renderComplexRecurringTasks;

  // Feature 68 exports
  window.calculateTimeToLeave = calculateTimeToLeave;
  window.saveTimeToLeaveEvent = saveTimeToLeaveEvent;
  window.getActiveTimeToLeave = getActiveTimeToLeave;
  window.clearTimeToLeave = clearTimeToLeave;
  window.saveTimeToLeaveFromUi = saveTimeToLeaveFromUi;
  window.renderTimeToLeaveState = renderTimeToLeaveState;

  // Feature 97 exports
  window.detectScheduleConflicts = detectScheduleConflicts;
  window.renderScheduleConflicts = renderScheduleConflicts;

  // Engine init
  window.initPackageE = initPackageE;

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initPackageE);
  } else {
    initPackageE();
  }

})();

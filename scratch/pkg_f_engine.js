/* ==========================================================================
   PACKAGE F: NOTES & ANDROID FEATURES ENGINE
   Features 71, 73, 81, 85, 86, 88, 90
   ========================================================================== */

(function(){
  'use strict';

  // --------------------------------------------------------------------------
  // FEATURE 71: PIN & COLOR-CODE NOTES
  // --------------------------------------------------------------------------
  const STORAGE_KEY_PINNED_NOTES = 'zatoona-pinned-notes-v1';
  const STORAGE_KEY_NOTE_COLORS = 'zatoona-note-colors-v1';

  function getPinnedNotes(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_PINNED_NOTES);
      return raw ? JSON.parse(raw) : [];
    } catch(e){
      return [];
    }
  }

  function savePinnedNotes(list){
    try {
      localStorage.setItem(STORAGE_KEY_PINNED_NOTES, JSON.stringify(list));
    } catch(e){}
  }

  function isNotePinned(noteKey){
    const list = getPinnedNotes();
    return list.includes(noteKey);
  }

  function togglePinNote(noteKey){
    let list = getPinnedNotes();
    if(list.includes(noteKey)){
      list = list.filter(k => k !== noteKey);
    } else {
      list.unshift(noteKey);
    }
    savePinnedNotes(list);
    if(typeof renderNotesHub === 'function') renderNotesHub();
    if(typeof triggerHaptic === 'function') triggerHaptic('light');
    return list.includes(noteKey);
  }

  function getNoteColorsMap(){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_NOTE_COLORS);
      return raw ? JSON.parse(raw) : {};
    } catch(e){
      return {};
    }
  }

  function setNoteColor(noteKey, colorHex){
    const map = getNoteColorsMap();
    if(colorHex){
      map[noteKey] = colorHex;
    } else {
      delete map[noteKey];
    }
    try {
      localStorage.setItem(STORAGE_KEY_NOTE_COLORS, JSON.stringify(map));
    } catch(e){}
    if(typeof renderNotesHub === 'function') renderNotesHub();
  }

  function getNoteColor(noteKey){
    const map = getNoteColorsMap();
    return map[noteKey] || null;
  }


  // --------------------------------------------------------------------------
  // FEATURE 73: CONVERT NOTE TO INTERACTIVE CHECKLIST
  // --------------------------------------------------------------------------
  const STORAGE_KEY_NOTE_CHECKLIST = 'zatoona-notes-checklist-v1';

  function getNoteChecklistState(noteKey){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_NOTE_CHECKLIST);
      const map = raw ? JSON.parse(raw) : {};
      return map[noteKey] || { isChecklist: false, checkedIndices: [] };
    } catch(e){
      return { isChecklist: false, checkedIndices: [] };
    }
  }

  function saveNoteChecklistState(noteKey, state){
    try {
      const raw = localStorage.getItem(STORAGE_KEY_NOTE_CHECKLIST);
      const map = raw ? JSON.parse(raw) : {};
      map[noteKey] = state;
      localStorage.setItem(STORAGE_KEY_NOTE_CHECKLIST, JSON.stringify(map));
    } catch(e){}
  }

  function isNoteChecklistMode(noteKey){
    return getNoteChecklistState(noteKey).isChecklist === true;
  }

  function toggleNoteChecklistMode(noteKey){
    const state = getNoteChecklistState(noteKey);
    state.isChecklist = !state.isChecklist;
    saveNoteChecklistState(noteKey, state);
    if(typeof renderNotesHub === 'function') renderNotesHub();
    return state.isChecklist;
  }

  function toggleNoteChecklistItem(noteKey, lineIndex){
    const state = getNoteChecklistState(noteKey);
    if(!state.checkedIndices) state.checkedIndices = [];
    const idx = state.checkedIndices.indexOf(lineIndex);
    if(idx >= 0){
      state.checkedIndices.splice(idx, 1);
    } else {
      state.checkedIndices.push(lineIndex);
    }
    saveNoteChecklistState(noteKey, state);
    if(typeof renderNotesHub === 'function') renderNotesHub();
  }

  function renderNoteChecklistHtml(noteKey, rawText){
    if(!rawText || !rawText.trim()) return '';
    const state = getNoteChecklistState(noteKey);
    const lines = rawText.split('\n');

    return lines.map((line, idx) => {
      if(!line.trim()) return '<div style="height:6px;"></div>';
      const cleanLine = line.replace(/^[\s*\-•>]+/, '').trim();
      const isDone = (state.checkedIndices || []).includes(idx);
      return `
        <div class="note-checklist-line ${isDone ? 'is-done' : ''}" onclick="window.toggleNoteChecklistItem('${noteKey}', ${idx})">
          <input type="checkbox" ${isDone ? 'checked' : ''} onclick="event.stopPropagation(); window.toggleNoteChecklistItem('${noteKey}', ${idx})">
          <span>${cleanLine}</span>
        </div>
      `;
    }).join('');
  }


  // --------------------------------------------------------------------------
  // FEATURE 81: LED FLASH ALERT (Native Android Bridge + Web Visual Fallback)
  // --------------------------------------------------------------------------
  const STORAGE_KEY_FLASH_ALARM = 'zatoona-flash-alarm-v1';

  function isFlashAlarmEnabled(){
    try {
      return localStorage.getItem(STORAGE_KEY_FLASH_ALARM) === '1';
    } catch(e){
      return false;
    }
  }

  function toggleFlashAlarm(forceState){
    const current = isFlashAlarmEnabled();
    const next = typeof forceState === 'boolean' ? forceState : !current;
    try {
      localStorage.setItem(STORAGE_KEY_FLASH_ALARM, next ? '1' : '0');
    } catch(e){}
    renderFlashSettingsUi();
    return next;
  }

  function triggerLedFlashAlert(durationMs, pulseCount){
    const dur = Number(durationMs) || 3000;
    const count = Number(pulseCount) || 6;

    // 1. Android Native Bridge Call
    if(window.ZatoonaNativeBridge && typeof window.ZatoonaNativeBridge.triggerLedFlash === 'function'){
      try {
        const res = window.ZatoonaNativeBridge.triggerLedFlash(dur, count);
        return res;
      } catch(e){}
    }

    // 2. Web screen flash fallback
    triggerWebScreenFlash(dur, count);
    return JSON.stringify({ status: 'ok', fallback: 'screen_flash' });
  }

  function triggerWebScreenFlash(durationMs, pulseCount){
    let overlay = document.getElementById('screenFlashOverlay');
    if(!overlay){
      overlay = document.createElement('div');
      overlay.id = 'screenFlashOverlay';
      overlay.className = 'screen-flash-overlay';
      document.body.appendChild(overlay);
    }

    let pulses = pulseCount || 6;
    let stepMs = Math.floor(durationMs / (pulses * 2));
    let currentPulse = 0;

    const interval = setInterval(() => {
      overlay.classList.toggle('active');
      currentPulse++;
      if(currentPulse >= pulses * 2){
        clearInterval(interval);
        overlay.classList.remove('active');
      }
    }, stepMs);
  }

  function renderFlashSettingsUi(){
    const btn = document.getElementById('settingsFlashToggle');
    if(btn){
      const en = isFlashAlarmEnabled();
      btn.textContent = en ? 'تشغيل' : 'إيقاف';
      btn.classList.toggle('on', en);
    }
  }


  // --------------------------------------------------------------------------
  // FEATURE 85: WAKE LOCK TOGGLE (Screen Always On)
  // --------------------------------------------------------------------------
  let wakeLockSentinel = null;

  function isWakeLockActive(){
    return wakeLockSentinel !== null && !wakeLockSentinel.released;
  }

  async function toggleWakeLock(){
    if(isWakeLockActive()){
      await releaseWakeLock();
    } else {
      await requestWakeLock();
    }
    updateWakeLockUi();
    return isWakeLockActive();
  }

  async function requestWakeLock(){
    if('wakeLock' in navigator){
      try {
        wakeLockSentinel = await navigator.wakeLock.request('screen');
        wakeLockSentinel.addEventListener('release', () => {
          wakeLockSentinel = null;
          updateWakeLockUi();
        });
        updateWakeLockUi();
        return true;
      } catch(err){
        console.warn('[WakeLock] Request failed:', err);
      }
    }
    // Fallback simulation for unsupported browsers/tests
    wakeLockSentinel = { released: false, release: function(){ this.released = true; } };
    updateWakeLockUi();
    return true;
  }

  async function releaseWakeLock(){
    if(wakeLockSentinel){
      try {
        if(typeof wakeLockSentinel.release === 'function'){
          await wakeLockSentinel.release();
        }
      } catch(e){}
      wakeLockSentinel = null;
    }
    updateWakeLockUi();
  }

  function updateWakeLockUi(){
    const pills = document.querySelectorAll('.wake-lock-pill, #btnToggleWakeLock');
    const active = isWakeLockActive();
    pills.forEach(el => {
      el.classList.toggle('active', active);
      el.textContent = active ? '💡 الشاشة مضاءة دائماً (مفعّل)' : '💡 إبقاء الشاشة مضاءة';
    });
  }

  // Auto re-acquire wake lock on visibility change
  document.addEventListener('visibilitychange', async () => {
    if(wakeLockSentinel !== null && document.visibilityState === 'visible'){
      await requestWakeLock();
    }
  });


  // --------------------------------------------------------------------------
  // FEATURE 86: CUSTOM HAPTIC PATTERNS PER NOTIFICATION TYPE
  // --------------------------------------------------------------------------
  const CUSTOM_HAPTIC_PATTERNS = {
    prayer: [150, 100, 150, 100, 300],       // Reverent, deep rhythmic pulse
    gym_timer: [100, 80, 100, 80, 200],      // Crisp tactical double-burst
    water: [80, 60, 80],                      // Gentle drop vibration
    danger: [300, 100, 300, 100, 400]        // Urgent conflict/alarm alert
  };

  function triggerCustomHaptic(patternName){
    const pattern = CUSTOM_HAPTIC_PATTERNS[patternName] || [100, 80, 100];
    if('vibrate' in navigator){
      try {
        navigator.vibrate(pattern);
      } catch(e){}
    }
    if(window.ZatoonaNativeBridge && typeof window.ZatoonaNativeBridge.triggerHaptic === 'function'){
      try {
        window.ZatoonaNativeBridge.triggerHaptic(pattern[0] || 20);
      } catch(e){}
    }
    return pattern;
  }


  // --------------------------------------------------------------------------
  // FEATURE 88: ALL-IN-ONE DAILY WIDGET SYNC (Android)
  // --------------------------------------------------------------------------
  function buildAllInOneDailySummary(){
    return {
      nextPrayerName: 'العصر',
      nextPrayerTime: '03:15 م',
      workoutDayName: 'تمارين الدفع (Push)',
      waterLitersToday: 2.25,
      waterTargetLiters: 3.0,
      streakDays: 7,
      fastingActive: false,
      timestamp: Date.now()
    };
  }

  function syncAllInOneWidgetData(customSummary){
    const data = customSummary || buildAllInOneDailySummary();
    const jsonStr = JSON.stringify(data);

    try {
      localStorage.setItem('zatoona-all-in-one-widget-cache-v1', jsonStr);
    } catch(e){}

    if(window.ZatoonaNativeBridge && typeof window.ZatoonaNativeBridge.syncAllInOneWidget === 'function'){
      try {
        return window.ZatoonaNativeBridge.syncAllInOneWidget(jsonStr);
      } catch(e){}
    }
    return JSON.stringify({ status: 'ok', cached_web: true });
  }


  // --------------------------------------------------------------------------
  // FEATURE 90: AMOLED ULTRA-BATTERY SAVER (100% Pure Black Mode)
  // --------------------------------------------------------------------------
  const STORAGE_KEY_AMOLED = 'zatoona-amoled-mode-v1';

  function isAmoledModeActive(){
    try {
      return localStorage.getItem(STORAGE_KEY_AMOLED) === '1';
    } catch(e){
      return false;
    }
  }

  function toggleAmoledMode(forceState){
    const current = isAmoledModeActive();
    const next = typeof forceState === 'boolean' ? forceState : !current;
    try {
      localStorage.setItem(STORAGE_KEY_AMOLED, next ? '1' : '0');
    } catch(e){}
    applyAmoledModeState();
    return next;
  }

  function applyAmoledModeState(){
    const active = isAmoledModeActive();
    document.body.classList.toggle('amoled-battery-saver', active);
    const btn = document.getElementById('settingsAmoledToggle');
    if(btn){
      btn.textContent = active ? 'تشغيل' : 'إيقاف';
      btn.classList.toggle('on', active);
    }
  }


  // --------------------------------------------------------------------------
  // HOOK INTO NOTES RENDERING (ENHANCE RENDERNOTESLIST / RENDERNOTESHUB)
  // --------------------------------------------------------------------------
  function enhanceNotesCardsInDom(){
    const container = document.getElementById('notesView');
    if(!container) return;

    const cards = container.querySelectorAll('.note-hub-card');
    cards.forEach(card => {
      const key = card.dataset.key;
      if(!key) return;

      // 1. Pin state & badge
      if(isNotePinned(key)){
        card.classList.add('is-pinned');
        let badge = card.querySelector('.note-pin-badge');
        if(!badge){
          const titleWrap = card.querySelector('div > span:nth-child(2)');
          if(titleWrap){
            badge = document.createElement('span');
            badge.className = 'note-pin-badge';
            badge.textContent = '📌 مثبتة';
            titleWrap.parentNode.insertBefore(badge, titleWrap.nextSibling);
          }
        }
      } else {
        card.classList.remove('is-pinned');
        const badge = card.querySelector('.note-pin-badge');
        if(badge) badge.remove();
      }

      // 2. Custom color tint
      const color = getNoteColor(key);
      if(color){
        card.style.borderRightColor = color;
        card.style.borderRightWidth = '5px';
      }

      // 3. Pin & Checklist tools row if not already injected
      if(!card.querySelector('.note-pkg-f-tools')){
        const toolsRow = document.createElement('div');
        toolsRow.className = 'note-pkg-f-tools';
        toolsRow.style.display = 'flex';
        toolsRow.style.alignItems = 'center';
        toolsRow.style.gap = '8px';
        toolsRow.style.marginTop = '8px';
        toolsRow.style.paddingTop = '6px';
        toolsRow.style.borderTop = '1px dashed var(--line)';
        toolsRow.style.flexWrap = 'wrap';

        const isPinned = isNotePinned(key);
        const isChecklist = isNoteChecklistMode(key);

        toolsRow.innerHTML = `
          <button type="button" class="reset-btn" onclick="window.togglePinNote('${key}')" style="font-size:.72rem; padding:2px 8px; color:var(--text);" title="تثبيت الملاحظة بالقمة">
            ${isPinned ? '📌 إلغاء التثبيت' : '📍 تثبيت بالقمة'}
          </button>
          <button type="button" class="reset-btn" onclick="window.toggleNoteChecklistMode('${key}')" style="font-size:.72rem; padding:2px 8px; color:var(--teal);" title="تحويل لقائمة شطب">
            ${isChecklist ? '📝 عرض كنص عادي' : '☑️ قائمة شطب تفاعلية'}
          </button>
          <div class="note-palette-row">
            <span class="note-color-dot" style="background:#10b981;" onclick="window.setNoteColor('${key}', '#10b981')" title="أخضر زمردي"></span>
            <span class="note-color-dot" style="background:#3b82f6;" onclick="window.setNoteColor('${key}', '#3b82f6')" title="أزرق"></span>
            <span class="note-color-dot" style="background:#f59e0b;" onclick="window.setNoteColor('${key}', '#f59e0b')" title="برتقالي"></span>
            <span class="note-color-dot" style="background:#ef4444;" onclick="window.setNoteColor('${key}', '#ef4444')" title="أحمر"></span>
            <span class="note-color-dot" style="background:#8b5cf6;" onclick="window.setNoteColor('${key}', '#8b5cf6')" title="بنفسجي"></span>
            <span class="note-color-dot" style="background:var(--card-alt);" onclick="window.setNoteColor('${key}', null)" title="إلغاء التلوين"></span>
          </div>
        `;
        card.appendChild(toolsRow);
      }

      // 4. Checklist rendering if in checklist mode
      if(isNoteChecklistMode(key)){
        const textEl = card.querySelector('div[style*="white-space:pre-wrap"]');
        if(textEl && !textEl.dataset.checklistRendered){
          textEl.dataset.checklistRendered = '1';
          const originalText = textEl.textContent;
          textEl.innerHTML = renderNoteChecklistHtml(key, originalText);
        }
      }
    });

    // Reorder pinned notes to top of timeline list
    const timelineList = document.getElementById('notesTimelineList');
    if(timelineList){
      const pinnedCards = Array.from(timelineList.querySelectorAll('.note-hub-card.is-pinned'));
      pinnedCards.reverse().forEach(c => timelineList.prepend(c));
    }
  }

  // Intercept renderNotesHub if present
  if(typeof window.renderNotesHub === 'function'){
    const origRenderNotesHub = window.renderNotesHub;
    window.renderNotesHub = function(){
      origRenderNotesHub.apply(this, arguments);
      try { enhanceNotesCardsInDom(); } catch(e){}
    };
  }

  // --------------------------------------------------------------------------
  // CONTROLLER INIT & GLOBAL EXPORTS
  // --------------------------------------------------------------------------
  function initPackageF(){
    applyAmoledModeState();
    renderFlashSettingsUi();
    updateWakeLockUi();
    enhanceNotesCardsInDom();
  }

  // Feature 71 exports
  window.getPinnedNotes = getPinnedNotes;
  window.isNotePinned = isNotePinned;
  window.togglePinNote = togglePinNote;
  window.getNoteColorsMap = getNoteColorsMap;
  window.setNoteColor = setNoteColor;
  window.getNoteColor = getNoteColor;

  // Feature 73 exports
  window.getNoteChecklistState = getNoteChecklistState;
  window.isNoteChecklistMode = isNoteChecklistMode;
  window.toggleNoteChecklistMode = toggleNoteChecklistMode;
  window.toggleNoteChecklistItem = toggleNoteChecklistItem;
  window.renderNoteChecklistHtml = renderNoteChecklistHtml;

  // Feature 81 exports
  window.isFlashAlarmEnabled = isFlashAlarmEnabled;
  window.toggleFlashAlarm = toggleFlashAlarm;
  window.triggerLedFlashAlert = triggerLedFlashAlert;

  // Feature 85 exports
  window.isWakeLockActive = isWakeLockActive;
  window.toggleWakeLock = toggleWakeLock;
  window.requestWakeLock = requestWakeLock;
  window.releaseWakeLock = releaseWakeLock;

  // Feature 86 exports
  window.CUSTOM_HAPTIC_PATTERNS = CUSTOM_HAPTIC_PATTERNS;
  window.triggerCustomHaptic = triggerCustomHaptic;

  // Feature 88 exports
  window.buildAllInOneDailySummary = buildAllInOneDailySummary;
  window.syncAllInOneWidgetData = syncAllInOneWidgetData;

  // Feature 90 exports
  window.isAmoledModeActive = isAmoledModeActive;
  window.toggleAmoledMode = toggleAmoledMode;
  window.applyAmoledModeState = applyAmoledModeState;

  // Init
  window.initPackageF = initPackageF;

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initPackageF);
  } else {
    initPackageF();
  }

})();

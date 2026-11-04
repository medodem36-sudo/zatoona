/**
 * ZATOONA PHASE 5: WORSHIP & SMART KHATMA ENGINE
 * Covers the 7 worship features of the Zatoona Grand Blueprint:
 * 1. Smart Khatma & Quran Reflection Hub
 * 2. Smart Pre-Fajr & Suhoor Alarm
 * 3. Pre-Adhan Preparation Chime
 * 4. Forbidden Prayer Times Indicator
 * 5. Friday Sunan Interactive Checklist
 * 6. Subtle Random Dhikr Treasury & Notification
 * 7. Missed Fasting & Prayers Make-up Ledger
 */
(function() {
  'use strict';

  // Storage Keys
  const KEYS = {
    KHATMA_STATE: 'khatma-state-v1',
    KHATMA_REFLECTIONS: 'khatma-reflections-v1',
    SUHOOR_SETTINGS: 'worship-suhoor-settings-v1',
    PREADHAN_SETTINGS: 'worship-preadhan-settings-v1',
    FRIDAY_PREFIX: 'worship-friday-sunan-',
    RANDOM_DHIKR: 'worship-random-dhikr-v1',
    MISSED_LEDGER: 'worship-missed-ledger-v1'
  };

  // Safe Storage Helpers
  function getJSON(key, defaultVal) {
    try {
      const val = localStorage.getItem(key);
      return val ? JSON.parse(val) : defaultVal;
    } catch(e) {
      console.warn('[Phase5] getJSON error for', key, e);
      return defaultVal;
    }
  }

  function setJSON(key, val) {
    try {
      localStorage.setItem(key, JSON.stringify(val));
    } catch(e) {
      console.warn('[Phase5] setJSON error for', key, e);
    }
  }

  function getSelectedDateISO() {
    if (typeof weekDates !== 'undefined' && typeof selectedIdx !== 'undefined' && weekDates[selectedIdx]) {
      return typeof toISO === 'function' ? toISO(weekDates[selectedIdx]) : weekDates[selectedIdx].toISOString().split('T')[0];
    }
    return new Date().toISOString().split('T')[0];
  }

  // Authentic Treasury of Adhkar
  const DHIKR_TREASURY = [
    { text: "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ", virtue: "كلمتان خفيفتان على اللسان، ثقيلتان في الميزان، حبيبتان إلى الرحمن" },
    { text: "لا حَوْلَ وَلا قُوَّةَ إِلا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ", virtue: "كنز من كنوز الجنة، وباب عظيم من أبواب الفرج ودفع الهموم" },
    { text: "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ الَّذِي لا إِلَهَ إِلا هُوَ الْحَيَّ الْقَيُّومَ وَأَتُوبُ إِلَيْهِ", virtue: "مَن قالها غُفرت ذنوبه وإن كان فرّ من الزحف" },
    { text: "لا إِلَهَ إِلا اللَّهُ وَحْدَهُ لا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ", virtue: "أفضل ما قاله النبي ﷺ والنبيون من قبله، حرز من الشيطان" },
    { text: "اللَّهُمَّ صَلِّ وَسَلِّمْ وَبَارِكْ عَلَى نَبِيِّنَا مُحَمَّدٍ", virtue: "مَن صلى عليّ صلاة صلى الله عليه بها عشراً وحُطت عنه عشر خطيئات" },
    { text: "سُبْحَانَ اللَّهِ ، وَالْحَمْدُ لِلَّهِ ، وَلا إِلَهَ إِلا اللَّهُ ، وَاللَّهُ أَكْبَرُ", virtue: "أحب الكلام إلى الله، أحب إليّ مما طلعت عليه الشمس" },
    { text: "يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ ، أَصْلِحْ لِي شَأْنِي كُلَّهُ وَلا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ", virtue: "وصية النبي ﷺ لفاطمة رضي الله عنها في الصباح والمساء" },
    { text: "اللَّهُمَّ إِنَّكَ عَفُوٌّ كَرِيمٌ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي", virtue: "الدعاء النبوي الجامع المبارك لأوقات الإجابة وليالي الفضل" },
    { text: "رَضِيتُ بِاللَّهِ رَبًّا، وَبِالإِسْلامِ دِينًا، وَبِمُحَمَّدٍ ﷺ نَبِيًّا وَرَسُولاً", virtue: "مَن قالها حين يصبح وحين يمسي كان حقاً على الله أن يرضيه" },
    { text: "حَسْبِيَ اللَّهُ لا إِلَهَ إِلا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ", virtue: "مَن قالها سبع مرات كفاه الله ما أهمه من أمر الدنيا والآخرة" }
  ];

  // Helper: parse HH:MM to minutes
  function timeToMinutes(tStr) {
    if (!tStr || typeof tStr !== 'string') return null;
    const parts = tStr.trim().split(':');
    if (parts.length < 2) return null;
    const h = parseInt(parts[0], 10);
    const m = parseInt(parts[1], 10);
    return isNaN(h) || isNaN(m) ? null : h * 60 + m;
  }

  function minutesToTime(totalMins) {
    totalMins = (totalMins + 1440) % 1440;
    const h = Math.floor(totalMins / 60);
    const m = totalMins % 60;
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
  }

  function formatTime12h(time24) {
    if (!time24) return '--:--';
    const parts = time24.split(':');
    if (parts.length < 2) return time24;
    let h = parseInt(parts[0], 10);
    const m = parts[1].padStart(2, '0');
    const ampm = h >= 12 ? 'م' : 'ص';
    h = h % 12 || 12;
    return `${h}:${m} ${ampm}`;
  }

  function getEffectivePrayerTimes() {
    if (typeof prayerTimesState !== 'undefined' && prayerTimesState && Object.keys(prayerTimesState).length > 0) {
      return prayerTimesState;
    }
    // Fallback defaults
    return {
      Fajr: "04:55",
      Sunrise: "06:22",
      Dhuhr: "11:50",
      Asr: "14:55",
      Maghrib: "17:18",
      Isha: "18:38"
    };
  }

  // =========================================================================
  // 1. FORBIDDEN PRAYER TIMES INDICATOR
  // =========================================================================
  function renderForbiddenTimes() {
    const listEl = document.getElementById('forbiddenWindowsList');
    const badgeEl = document.getElementById('forbiddenStatusBadge');
    if (!listEl || !badgeEl) return;

    const times = getEffectivePrayerTimes();
    const fajrM = timeToMinutes(times.Fajr) || (4 * 60 + 55);
    const sunriseM = timeToMinutes(times.Sunrise) || (6 * 60 + 22);
    const dhuhrM = timeToMinutes(times.Dhuhr) || (11 * 60 + 50);
    const asrM = timeToMinutes(times.Asr) || (14 * 60 + 55);
    const maghribM = timeToMinutes(times.Maghrib) || (17 * 60 + 18);

    // 3 Forbidden Windows:
    // Window 1: From Fajr until Sunrise + 15 min
    const w1Start = fajrM;
    const w1End = sunriseM + 15;

    // Window 2: From Dhuhr - 10 min until Dhuhr (Zenith / Istiwaa)
    const w2Start = dhuhrM - 10;
    const w2End = dhuhrM;

    // Window 3: From Asr until Maghrib
    const w3Start = asrM;
    const w3End = maghribM;

    const now = new Date();
    const nowM = now.getHours() * 60 + now.getMinutes();

    const isW1 = (nowM >= w1Start && nowM < w1End);
    const isW2 = (nowM >= w2Start && nowM < w2End);
    const isW3 = (nowM >= w3Start && nowM < w3End);
    const isForbiddenNow = isW1 || isW2 || isW3;

    if (isForbiddenNow) {
      badgeEl.className = 'forbidden-status-badge forbidden';
      badgeEl.innerHTML = '<span>⚠️</span> <span>الآن: وقت كراهة (يُنهى عن النفل)</span>';
    } else {
      badgeEl.className = 'forbidden-status-badge allowed';
      badgeEl.innerHTML = '<span>✅</span> <span>الآن: وقت إباحة التطوع مستحب</span>';
    }

    listEl.innerHTML = `
      <div class="forbidden-window-item ${isW1 ? 'active-window' : ''}">
        <div>
          <strong>١. بعد صلاة الفجر حتى طلوع الشمس وارتفاعها:</strong>
          <div class="worship-subtext">حتى تطلع الشمس قيد رمح (الشروق + 15 دقيقة)</div>
        </div>
        <div style="font-weight:700; color:${isW1 ? '#f85149' : 'var(--text)'};">
          ${formatTime12h(times.Fajr)} ➔ ${formatTime12h(minutesToTime(w1End))}
        </div>
      </div>

      <div class="forbidden-window-item ${isW2 ? 'active-window' : ''}">
        <div>
          <strong>٢. عند استواء الشمس في كبد السماء (قبل الظهر):</strong>
          <div class="worship-subtext">وقت تسجير جهنم قبيل أذان الظهر بـ 10 دقائق</div>
        </div>
        <div style="font-weight:700; color:${isW2 ? '#f85149' : 'var(--text)'};">
          ${formatTime12h(minutesToTime(w2Start))} ➔ ${formatTime12h(times.Dhuhr)}
        </div>
      </div>

      <div class="forbidden-window-item ${isW3 ? 'active-window' : ''}">
        <div>
          <strong>٣. بعد صلاة العصر حتى غروب الشمس:</strong>
          <div class="worship-subtext">حتى يغيب قرص الشمس ويؤذن للمغرب تماماً</div>
        </div>
        <div style="font-weight:700; color:${isW3 ? '#f85149' : 'var(--text)'};">
          ${formatTime12h(times.Asr)} ➔ ${formatTime12h(times.Maghrib)}
        </div>
      </div>
    `;
  }

  // =========================================================================
  // 2. PRE-ADHAN PREPARATION CHIME
  // =========================================================================
  function getPreAdhanSettings() {
    return getJSON(KEYS.PREADHAN_SETTINGS, { enabled: false, minutesBefore: 10 });
  }

  function renderPreAdhan() {
    const toggleEl = document.getElementById('preAdhanChimeToggle');
    const selectEl = document.getElementById('preAdhanMinutesSelect');
    const nextAlertEl = document.getElementById('preAdhanNextAlert');
    if (!toggleEl || !selectEl) return;

    const settings = getPreAdhanSettings();
    toggleEl.checked = !!settings.enabled;
    selectEl.value = String(settings.minutesBefore || 10);

    if (nextAlertEl) {
      if (settings.enabled) {
        const times = getEffectivePrayerTimes();
        const now = new Date();
        const nowM = now.getHours() * 60 + now.getMinutes();
        const mins = Number(settings.minutesBefore) || 10;

        let nextPrayer = null;
        let nextAlertTime = null;

        const prayersOrder = [
          { name: 'الفجر', key: 'Fajr' },
          { name: 'الظهر', key: 'Dhuhr' },
          { name: 'العصر', key: 'Asr' },
          { name: 'المغرب', key: 'Maghrib' },
          { name: 'العشاء', key: 'Isha' }
        ];

        for (let p of prayersOrder) {
          const pM = timeToMinutes(times[p.key]);
          if (pM !== null) {
            const alertM = pM - mins;
            if (alertM > nowM) {
              nextPrayer = p.name;
              nextAlertTime = minutesToTime(alertM);
              break;
            }
          }
        }

        if (nextPrayer && nextAlertTime) {
          nextAlertEl.innerHTML = `🔔 التنبيه القادم: صلاة <strong>${nextPrayer}</strong> الساعة <strong>${formatTime12h(nextAlertTime)}</strong> (قبل الأذان بـ ${mins} دقائق)`;
        } else {
          nextAlertEl.innerHTML = `🔔 تم الانتهاء من تنبيهات صلوات اليوم، يبدأ غداً فجراً.`;
        }
      } else {
        nextAlertEl.innerHTML = `🔕 المنبه المسبق معطل حالياً`;
      }
    }
  }

  function togglePreAdhanChime(enabled) {
    const s = getPreAdhanSettings();
    s.enabled = !!enabled;
    setJSON(KEYS.PREADHAN_SETTINGS, s);
    renderPreAdhan();
  }

  function setPreAdhanMinutes(val) {
    const s = getPreAdhanSettings();
    s.minutesBefore = parseInt(val, 10) || 10;
    setJSON(KEYS.PREADHAN_SETTINGS, s);
    renderPreAdhan();
  }

  // =========================================================================
  // 3. SMART PRE-FAJR & SUHOOR ALARM
  // =========================================================================
  function getSuhoorSettings() {
    return getJSON(KEYS.SUHOOR_SETTINGS, { enabled: false, offsetMinutes: 45 });
  }

  function renderSuhoor() {
    const toggleEl = document.getElementById('suhoorAlarmToggle');
    const offsetEl = document.getElementById('suhoorOffsetSelect');
    const timeEl = document.getElementById('suhoorTimeDisplay');
    const pillEl = document.getElementById('suhoorCountdownPill');
    if (!timeEl || !offsetEl || !toggleEl) return;

    const settings = getSuhoorSettings();
    toggleEl.checked = !!settings.enabled;
    offsetEl.value = String(settings.offsetMinutes || 45);

    const times = getEffectivePrayerTimes();
    const fajrM = timeToMinutes(times.Fajr) || (4 * 60 + 55);
    const offset = Number(settings.offsetMinutes) || 45;
    const suhoorM = fajrM - offset;
    const suhoorTimeStr = minutesToTime(suhoorM);

    timeEl.textContent = formatTime12h(suhoorTimeStr);

    if (pillEl) {
      const now = new Date();
      const nowM = now.getHours() * 60 + now.getMinutes();
      let diff = suhoorM - nowM;
      if (diff < 0) diff += 1440; // Next day
      const diffH = Math.floor(diff / 60);
      const diffM = diff % 60;
      pillEl.textContent = `متبقي: ${diffH} ساعة و ${diffM} دقيقة`;
    }
  }

  function toggleSuhoorAlarm(enabled) {
    const s = getSuhoorSettings();
    s.enabled = !!enabled;
    setJSON(KEYS.SUHOOR_SETTINGS, s);
    renderSuhoor();
  }

  function setSuhoorOffset(val) {
    const s = getSuhoorSettings();
    s.offsetMinutes = parseInt(val, 10) || 45;
    setJSON(KEYS.SUHOOR_SETTINGS, s);
    renderSuhoor();
  }

  // =========================================================================
  // 4. SUBTLE RANDOM DHIKR
  // =========================================================================
  function getRandomDhikrSettings() {
    return getJSON(KEYS.RANDOM_DHIKR, { intervalMinutes: 120, enabled: true, lastDhikrIdx: 0 });
  }

  function renderRandomDhikr() {
    const textEl = document.getElementById('randomDhikrText');
    const virtueEl = document.getElementById('randomDhikrVirtue');
    const selectEl = document.getElementById('randomDhikrIntervalSelect');
    if (!textEl || !virtueEl) return;

    const s = getRandomDhikrSettings();
    if (selectEl) {
      selectEl.value = s.enabled ? String(s.intervalMinutes) : 'off';
    }

    const idx = (s.lastDhikrIdx >= 0 && s.lastDhikrIdx < DHIKR_TREASURY.length) ? s.lastDhikrIdx : 0;
    const item = DHIKR_TREASURY[idx];
    textEl.textContent = item.text;
    virtueEl.textContent = item.virtue;
  }

  function nextRandomDhikr() {
    const s = getRandomDhikrSettings();
    let nextIdx;
    do {
      nextIdx = Math.floor(Math.random() * DHIKR_TREASURY.length);
    } while (nextIdx === s.lastDhikrIdx && DHIKR_TREASURY.length > 1);

    s.lastDhikrIdx = nextIdx;
    setJSON(KEYS.RANDOM_DHIKR, s);
    renderRandomDhikr();
  }

  function setDhikrInterval(val) {
    const s = getRandomDhikrSettings();
    if (val === 'off') {
      s.enabled = false;
    } else {
      s.enabled = true;
      s.intervalMinutes = parseInt(val, 10) || 120;
    }
    setJSON(KEYS.RANDOM_DHIKR, s);
    renderRandomDhikr();
  }

  // =========================================================================
  // 5. FRIDAY SUNAN INTERACTIVE CHECKLIST
  // =========================================================================
  const FRIDAY_ITEMS = [
    { id: 'ghusl', text: 'الاغتسال والتطيب ولبس أحسن الثياب 🧼✨' },
    { id: 'kahf', text: 'قراءة سورة الكهف أو الاستماع إليها 📖' },
    { id: 'early', text: 'التبكير للمسجد والمشي بالسكينة والوقار 🚶‍♂️🕌' },
    { id: 'dua', text: 'تحري ساعة الإجابة (آخر ساعة بعد العصر) 🤲' }
  ];

  function getFridayState(iso) {
    const key = KEYS.FRIDAY_PREFIX + iso;
    return getJSON(key, { ghusl: false, kahf: false, early: false, dua: false, salawatCount: 0 });
  }

  function saveFridayState(iso, state) {
    const key = KEYS.FRIDAY_PREFIX + iso;
    setJSON(key, state);
  }

  function renderFridaySunan() {
    const listEl = document.getElementById('fridaySunanList');
    const badgeEl = document.getElementById('fridayBadgeIndicator');
    const salawatEl = document.getElementById('salawatCountDisplay');
    if (!listEl) return;

    const iso = getSelectedDateISO();
    const dateObj = new Date(iso + 'T00:00:00');
    const isFriday = dateObj.getDay() === 5;
    const state = getFridayState(iso);

    if (badgeEl) {
      badgeEl.textContent = isFriday ? 'الجمعة المباركة 🌟' : 'سنن الجمعة (معاينة)';
    }

    if (salawatEl) {
      salawatEl.textContent = state.salawatCount || 0;
    }

    listEl.innerHTML = FRIDAY_ITEMS.map(item => {
      const isDone = !!state[item.id];
      return `
        <div class="friday-check-item ${isDone ? 'done' : ''}" onclick="window.ZATOONA_PHASE5.toggleFridaySunanItem('${item.id}')">
          <input type="checkbox" ${isDone ? 'checked' : ''} style="cursor:pointer; width:18px; height:18px; accent-color:#3fb950;">
          <div class="friday-title" style="font-size:0.86rem; font-weight:600;">${item.text}</div>
        </div>
      `;
    }).join('');
  }

  function toggleFridaySunanItem(id) {
    const iso = getSelectedDateISO();
    const state = getFridayState(iso);
    state[id] = !state[id];
    saveFridayState(iso, state);
    renderFridaySunan();
  }

  function incrementSalawat() {
    const iso = getSelectedDateISO();
    const state = getFridayState(iso);
    state.salawatCount = (state.salawatCount || 0) + 1;
    saveFridayState(iso, state);
    const el = document.getElementById('salawatCountDisplay');
    if (el) el.textContent = state.salawatCount;
  }

  function addSalawatBatch(amount) {
    const iso = getSelectedDateISO();
    const state = getFridayState(iso);
    state.salawatCount = (state.salawatCount || 0) + amount;
    saveFridayState(iso, state);
    const el = document.getElementById('salawatCountDisplay');
    if (el) el.textContent = state.salawatCount;
  }

  function resetSalawat() {
    const iso = getSelectedDateISO();
    const state = getFridayState(iso);
    state.salawatCount = 0;
    saveFridayState(iso, state);
    const el = document.getElementById('salawatCountDisplay');
    if (el) el.textContent = 0;
  }

  // =========================================================================
  // 6. SMART KHATMA & QURAN REFLECTION HUB
  // =========================================================================
  function getKhatmaState() {
    return getJSON(KEYS.KHATMA_STATE, {
      currentPage: 1,
      durationDays: 30,
      dailyTarget: 20,
      lastReadDate: null,
      streak: 0
    });
  }

  function saveKhatmaState(st) {
    setJSON(KEYS.KHATMA_STATE, st);
  }

  function getReflections() {
    return getJSON(KEYS.KHATMA_REFLECTIONS, []);
  }

  function saveReflections(list) {
    setJSON(KEYS.KHATMA_REFLECTIONS, list);
  }

  function pageToJuz(p) {
    if (p <= 21) return 1;
    if (p <= 41) return 2;
    if (p <= 61) return 3;
    if (p <= 81) return 4;
    if (p <= 101) return 5;
    if (p <= 121) return 6;
    if (p <= 141) return 7;
    if (p <= 161) return 8;
    if (p <= 181) return 9;
    if (p <= 201) return 10;
    if (p <= 221) return 11;
    if (p <= 241) return 12;
    if (p <= 261) return 13;
    if (p <= 281) return 14;
    if (p <= 301) return 15;
    if (p <= 321) return 16;
    if (p <= 341) return 17;
    if (p <= 361) return 18;
    if (p <= 381) return 19;
    if (p <= 401) return 20;
    if (p <= 421) return 21;
    if (p <= 441) return 22;
    if (p <= 461) return 23;
    if (p <= 481) return 24;
    if (p <= 501) return 25;
    if (p <= 521) return 26;
    if (p <= 541) return 27;
    if (p <= 561) return 28;
    if (p <= 581) return 29;
    return 30;
  }

  function renderKhatma() {
    const pageEl = document.getElementById('khatmaCurrentPage');
    const juzEl = document.getElementById('khatmaCurrentJuz');
    const targetEl = document.getElementById('khatmaDailyTarget');
    const barEl = document.getElementById('khatmaBarFill');
    const percentEl = document.getElementById('khatmaPercentText');
    if (!pageEl || !barEl || !percentEl) return;

    const st = getKhatmaState();
    const curP = Math.max(1, Math.min(604, st.currentPage || 1));
    const percent = Math.min(100, Math.round((curP / 604) * 100));

    pageEl.textContent = curP;
    if (juzEl) juzEl.textContent = pageToJuz(curP);
    if (targetEl) targetEl.textContent = st.dailyTarget || 20;

    barEl.style.width = percent + '%';
    percentEl.textContent = percent + '%';
  }

  function markTodayKhatmaDone() {
    const st = getKhatmaState();
    const target = st.dailyTarget || 20;
    st.currentPage = Math.min(604, (st.currentPage || 1) + target);
    st.lastReadDate = getSelectedDateISO();
    saveKhatmaState(st);
    renderKhatma();
  }

  function openKhatmaModal(tab) {
    const modal = document.getElementById('khatmaReflectionModal');
    if (!modal) return;
    modal.classList.add('active');
    switchKhatmaTab(tab || 'plan');
  }

  function closeModals() {
    const modals = document.querySelectorAll('.p5-modal-overlay');
    modals.forEach(m => m.classList.remove('active'));
  }

  function switchKhatmaTab(tab) {
    const planTab = document.getElementById('khatmaTabPlanContent');
    const reflectTab = document.getElementById('khatmaTabReflectContent');
    const planBtn = document.getElementById('khatmaTabPlanBtn');
    const reflectBtn = document.getElementById('khatmaTabReflectBtn');

    if (tab === 'reflections') {
      if (planTab) planTab.style.display = 'none';
      if (reflectTab) reflectTab.style.display = 'block';
      if (planBtn) planBtn.style.opacity = '0.7';
      if (reflectBtn) reflectBtn.style.opacity = '1';
      renderReflectionsList();
    } else {
      if (planTab) planTab.style.display = 'block';
      if (reflectTab) reflectTab.style.display = 'none';
      if (planBtn) planBtn.style.opacity = '1';
      if (reflectBtn) reflectBtn.style.opacity = '0.7';

      const st = getKhatmaState();
      const durSel = document.getElementById('khatmaDurationSelect');
      const pageInp = document.getElementById('khatmaManualPageInput');
      if (durSel) durSel.value = String(st.durationDays || 30);
      if (pageInp) pageInp.value = st.currentPage || 1;
    }
  }

  function saveKhatmaPlanSettings() {
    const durSel = document.getElementById('khatmaDurationSelect');
    const pageInp = document.getElementById('khatmaManualPageInput');
    const st = getKhatmaState();

    if (durSel) {
      const dur = durSel.value;
      if (dur === '15') {
        st.durationDays = 15;
        st.dailyTarget = 40;
      } else if (dur === '60') {
        st.durationDays = 60;
        st.dailyTarget = 10;
      } else if (dur === 'custom') {
        st.durationDays = 'custom';
      } else {
        st.durationDays = 30;
        st.dailyTarget = 20;
      }
    }

    if (pageInp) {
      const p = parseInt(pageInp.value, 10);
      if (!isNaN(p) && p >= 1 && p <= 604) {
        st.currentPage = p;
      }
    }

    saveKhatmaState(st);
    renderKhatma();
    closeModals();
  }

  function renderReflectionsList() {
    const listEl = document.getElementById('reflectionsList');
    if (!listEl) return;
    const items = getReflections();

    if (items.length === 0) {
      listEl.innerHTML = '<div style="text-align:center; color:var(--muted); font-size:0.8rem; padding:12px;">لا توجد خواطر أو تدبرات مسجلة بعد. أضف أول تدبر لك بالأعلى! ✨</div>';
      return;
    }

    listEl.innerHTML = items.slice().reverse().map(item => `
      <div class="reflection-card-item">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
          <span class="reflection-ayah-badge">سورة ${escapeHtml(item.surah || '')} : آية ${escapeHtml(String(item.ayah || ''))}</span>
          <span style="font-size:0.7rem; color:var(--muted);">${item.date || ''}</span>
        </div>
        <div style="font-size:0.85rem; line-height:1.5; margin-bottom:6px;">${escapeHtml(item.note || '')}</div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:0.75rem; color:#e3b341;">#${escapeHtml(item.tag || 'تدبر')}</span>
          <button type="button" class="btn-subtle" style="font-size:0.7rem; padding:2px 6px; color:#f85149;" onclick="window.ZATOONA_PHASE5.deleteReflectionNote('${item.id}')">حذف</button>
        </div>
      </div>
    `).join('');
  }

  function addReflectionNote() {
    const surahInp = document.getElementById('reflectSurahInput');
    const ayahInp = document.getElementById('reflectAyahInput');
    const tagSel = document.getElementById('reflectTagSelect');
    const textInp = document.getElementById('reflectTextInput');

    if (!surahInp || !textInp || !textInp.value.trim()) return;

    const list = getReflections();
    const newNote = {
      id: 'ref_' + Date.now(),
      surah: surahInp.value.trim(),
      ayah: ayahInp ? ayahInp.value.trim() : '',
      tag: tagSel ? tagSel.value : 'تدبر',
      note: textInp.value.trim(),
      date: getSelectedDateISO()
    };

    list.push(newNote);
    saveReflections(list);

    surahInp.value = '';
    if (ayahInp) ayahInp.value = '';
    textInp.value = '';

    renderReflectionsList();
  }

  function deleteReflectionNote(id) {
    let list = getReflections();
    list = list.filter(item => item.id !== id);
    saveReflections(list);
    renderReflectionsList();
  }

  // =========================================================================
  // 7. MISSED WORSHIP & FASTING LEDGER
  // =========================================================================
  const OBLIGATORY_PRAYERS = [
    { key: 'Fajr', name: 'الفجر' },
    { key: 'Dhuhr', name: 'الظهر' },
    { key: 'Asr', name: 'العصر' },
    { key: 'Maghrib', name: 'المغرب' },
    { key: 'Isha', name: 'العشاء' }
  ];

  function getMissedLedger() {
    return getJSON(KEYS.MISSED_LEDGER, {
      prayers: { Fajr: 0, Dhuhr: 0, Asr: 0, Maghrib: 0, Isha: 0 },
      fastingDaysOwed: 0,
      fastingDaysDone: 0
    });
  }

  function saveMissedLedger(data) {
    setJSON(KEYS.MISSED_LEDGER, data);
  }

  function renderMissedWorship() {
    const gridEl = document.getElementById('missedPrayersGrid');
    const remFastingEl = document.getElementById('missedFastingRemaining');
    const doneFastingEl = document.getElementById('missedFastingDone');
    if (!gridEl) return;

    const data = getMissedLedger();

    if (remFastingEl) remFastingEl.textContent = data.fastingDaysOwed || 0;
    if (doneFastingEl) doneFastingEl.textContent = data.fastingDaysDone || 0;

    gridEl.innerHTML = OBLIGATORY_PRAYERS.map(p => {
      const count = data.prayers[p.key] || 0;
      return `
        <div class="missed-prayer-card">
          <div class="missed-prayer-name">${p.name}</div>
          <div class="missed-count-display" id="missedCount-${p.key}">${count}</div>
          <div class="missed-ctrl-btns">
            <button type="button" class="missed-ctrl-btn" onclick="window.ZATOONA_PHASE5.adjustMissedPrayer('${p.key}', -1)">-1</button>
            <button type="button" class="missed-ctrl-btn" onclick="window.ZATOONA_PHASE5.adjustMissedPrayer('${p.key}', 1)">+1</button>
            <button type="button" class="missed-ctrl-btn" onclick="window.ZATOONA_PHASE5.adjustMissedPrayer('${p.key}', 5)">+5</button>
          </div>
        </div>
      `;
    }).join('');
  }

  function adjustMissedPrayer(key, delta) {
    const data = getMissedLedger();
    const cur = data.prayers[key] || 0;
    data.prayers[key] = Math.max(0, cur + delta);
    saveMissedLedger(data);
    renderMissedWorship();
  }

  function logFastMadeUp() {
    const data = getMissedLedger();
    if (data.fastingDaysOwed > 0) {
      data.fastingDaysOwed--;
      data.fastingDaysDone = (data.fastingDaysDone || 0) + 1;
      saveMissedLedger(data);
      renderMissedWorship();
      // If fastingCard is on screen, update it
      if (typeof saveFasting === 'function') {
        const iso = getSelectedDateISO();
        saveFasting(iso, { fasted: true, type: 'qadaa' });
        if (typeof renderFasting === 'function') renderFasting();
      }
    } else {
      alert('لا توجد أيام قضاء مسجلة عليك. يمكنك تعديل الإجمالي أولاً!');
    }
  }

  function editMissedFastingDays() {
    const data = getMissedLedger();
    const cur = data.fastingDaysOwed || 0;
    const input = prompt('أدخل إجمالي أيام الصيام الواجب قضاؤها (مثلاً: 5):', cur);
    if (input !== null) {
      const num = parseInt(input, 10);
      if (!isNaN(num) && num >= 0) {
        data.fastingDaysOwed = num;
        saveMissedLedger(data);
        renderMissedWorship();
      }
    }
  }

  // =========================================================================
  // MAIN LIFECYCLE HOOK
  // =========================================================================
  function onWorshipViewRendered() {
    renderForbiddenTimes();
    renderPreAdhan();
    renderSuhoor();
    renderRandomDhikr();
    renderFridaySunan();
    renderKhatma();
    renderMissedWorship();
  }

  // Escape HTML helper
  function escapeHtml(str) {
    if (typeof str !== 'string') return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Export public API
  window.ZATOONA_PHASE5 = {
    onWorshipViewRendered,
    // Forbidden Times
    renderForbiddenTimes,
    // Pre-Adhan
    togglePreAdhanChime,
    setPreAdhanMinutes,
    renderPreAdhan,
    // Suhoor
    toggleSuhoorAlarm,
    setSuhoorOffset,
    renderSuhoor,
    // Random Dhikr
    nextRandomDhikr,
    setDhikrInterval,
    renderRandomDhikr,
    // Friday Sunan
    toggleFridaySunanItem,
    incrementSalawat,
    addSalawatBatch,
    resetSalawat,
    renderFridaySunan,
    // Khatma & Reflections
    renderKhatma,
    markTodayKhatmaDone,
    openKhatmaModal,
    closeModals,
    switchKhatmaTab,
    saveKhatmaPlanSettings,
    addReflectionNote,
    deleteReflectionNote,
    renderReflectionsList,
    // Missed Worship
    adjustMissedPrayer,
    logFastMadeUp,
    editMissedFastingDays,
    renderMissedWorship,
    // Getters for testing
    getKhatmaState,
    getReflections,
    getMissedLedger,
    getSuhoorSettings,
    getPreAdhanSettings
  };

  // Auto-init when DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      onWorshipViewRendered();
    });
  } else {
    setTimeout(onWorshipViewRendered, 50);
  }

})();
/* END PHASE 5 */

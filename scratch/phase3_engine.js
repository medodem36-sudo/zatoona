/* ================= PHASE 3: NEXT-GEN GYM & STRENGTH ENGINE ================= */
(function(){
  // --- Storage Keys ---
  const KEY_BLACKLIST = 'gym-blacklist-v1';
  const KEY_PAIN_FLAGS = 'gym-pain-flags-v1';
  const KEY_1RM_HISTORY = 'gym-1rm-history-v1';
  const KEY_TEMPO_SETTINGS = 'gym-tempo-settings-v1';

  // --- Safe Storage Helpers ---
  function p3StorageGet(key, fallback){
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch(e) {
      return fallback;
    }
  }

  function p3StorageSet(key, val){
    try {
      localStorage.setItem(key, JSON.stringify(val));
    } catch(e) {
      console.warn('[Phase 3 Gym Engine] storage error:', e);
    }
  }

  function getP3DefaultExercises(){
    const a = (typeof EX_A_DEFAULTS !== 'undefined') ? EX_A_DEFAULTS : (window.EX_A_DEFAULTS || []);
    const b = (typeof EX_B_DEFAULTS !== 'undefined') ? EX_B_DEFAULTS : (window.EX_B_DEFAULTS || []);
    return [].concat(a, b);
  }

  // --- Web Audio Synthesizer (Offline) ---
  let p3AudioCtx = null;
  function getP3AudioContext(){
    if(!p3AudioCtx){
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if(AudioContextClass){
        p3AudioCtx = new AudioContextClass();
      }
    }
    if(p3AudioCtx && p3AudioCtx.state === 'suspended'){
      p3AudioCtx.resume();
    }
    return p3AudioCtx;
  }

  function playP3Tone(freq, durationMs, type){
    try {
      const ctx = getP3AudioContext();
      if(!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = type || 'sine';
      osc.frequency.setValueAtTime(freq, ctx.currentTime);
      gain.gain.setValueAtTime(0.15, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + (durationMs / 1000));
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + (durationMs / 1000));
    } catch(e) {}
  }

  // Haptic feedback trigger with fallback
  function triggerP3Haptic(ms){
    try {
      const duration = ms || 20;
      if(window.ZatoonaNativeBridge && typeof window.ZatoonaNativeBridge.triggerHaptic === 'function'){
        window.ZatoonaNativeBridge.triggerHaptic(duration);
      } else if(navigator.vibrate){
        navigator.vibrate(duration);
      }
    } catch(e) {}
  }

  // ================= 1. 1RM & RPE CALCULATOR =================
  function compute1RM(weight, reps, rir){
    const w = parseFloat(weight) || 0;
    const r = parseInt(reps, 10) || 1;
    const extra = parseFloat(rir || 0) || 0;
    const totalReps = Math.max(1, r + extra);

    if(w <= 0) return 0;
    if(totalReps === 1) return w;

    // Epley formula: w * (1 + r / 30)
    const epley = w * (1 + totalReps / 30);
    // Brzycki formula: w * (36 / (37 - r))
    const brzycki = (totalReps < 37) ? w * (36 / (37 - totalReps)) : epley;

    const avg = (epley + brzycki) / 2;
    return Math.round(avg * 10) / 10;
  }

  function generate1RMPctTable(oneRm){
    const pcts = [
      { pct: 100, reps: '1 تكرار أقصى (1RM)' },
      { pct: 95,  reps: '2 تكرار' },
      { pct: 90,  reps: '3-4 تكرارات' },
      { pct: 85,  reps: '5-6 تكرارات' },
      { pct: 80,  reps: '7-8 تكرارات' },
      { pct: 75,  reps: '9-10 تكرارات' },
      { pct: 70,  reps: '11-12 تكرار' },
      { pct: 65,  reps: '13-15 تكرار' },
      { pct: 60,  reps: '16-20 تكرار' },
      { pct: 50,  reps: 'إحماء ومرونة' }
    ];

    return pcts.map(function(item){
      const targetWeight = Math.round((oneRm * item.pct / 100) * 2) / 2;
      return {
        pct: item.pct,
        weight: targetWeight,
        reps: item.reps
      };
    });
  }

  let activeTargetExKeyFor1RM = null;

  function openGym1RMCalc(prefillKey, prefillWeight, prefillReps){
    activeTargetExKeyFor1RM = prefillKey || null;
    const modal = document.getElementById('gym1RMCalcModal');
    if(!modal) return;

    const wInput = document.getElementById('calc1rmWeightInput');
    const rInput = document.getElementById('calc1rmRepsInput');

    if(prefillWeight && wInput) wInput.value = prefillWeight;
    if(prefillReps && rInput) rInput.value = prefillReps;

    update1RMDisplay();
    modal.classList.add('open');
  }

  function closeGym1RMCalc(){
    const modal = document.getElementById('gym1RMCalcModal');
    if(modal) modal.classList.remove('open');
  }

  function update1RMDisplay(){
    const w = parseFloat(document.getElementById('calc1rmWeightInput')?.value) || 0;
    const r = parseInt(document.getElementById('calc1rmRepsInput')?.value, 10) || 1;
    const rir = parseFloat(document.getElementById('calc1rmRpeSelect')?.value) || 0;

    const oneRm = compute1RM(w, r, rir);
    const outEl = document.getElementById('calc1rmOutput');
    if(outEl) outEl.textContent = oneRm + ' كجم';

    const tbody = document.getElementById('calc1rmTableBody');
    if(tbody){
      const table = generate1RMPctTable(oneRm);
      tbody.innerHTML = table.map(function(row){
        return '<tr>' +
          '<td style="font-weight:700; color:var(--accent);">' + row.pct + '%</td>' +
          '<td style="font-weight:700; font-family:\'IBM Plex Mono\', monospace;">' + row.weight + ' كجم</td>' +
          '<td style="color:var(--muted);">' + row.reps + '</td>' +
        '</tr>';
      }).join('');
    }
  }

  // ================= 2. SMART WARMUP PROGRESSION & PLATE LOADER =================
  function computePlateBreakdown(workWeight, barWeight){
    const bw = (typeof barWeight === 'number') ? barWeight : 20;
    const sideWeight = Math.max(0, (workWeight - bw) / 2);
    const availablePlates = [25, 20, 15, 10, 5, 2.5, 1.25];
    const platesUsed = [];
    let rem = sideWeight;

    for(let i = 0; i < availablePlates.length; i++){
      const p = availablePlates[i];
      while(rem >= p - 0.001){
        platesUsed.push(p);
        rem -= p;
      }
    }

    return {
      sideWeight: Math.round(sideWeight * 100) / 100,
      plates: platesUsed
    };
  }

  function computeWarmupSetsList(workWeight, barWeight){
    const bw = (typeof barWeight === 'number') ? barWeight : 20;
    const w = Math.max(bw, workWeight);
    return [
      { set: 'مجموعة 1 (تسخين مفاصل)', pct: 'البار فقط', weight: bw, reps: '10 تكرارات', rest: '30 ثانية' },
      { set: 'مجموعة 2 (بناء المسار)', pct: '45%', weight: Math.max(bw, Math.round(w * 0.45 / 2.5) * 2.5), reps: '6 تكرارات', rest: '45 ثانية' },
      { set: 'مجموعة 3 (تنشيط عصبي)', pct: '65%', weight: Math.max(bw, Math.round(w * 0.65 / 2.5) * 2.5), reps: '4 تكرارات', rest: '60 ثانية' },
      { set: 'مجموعة 4 (اقتراب)', pct: '80%', weight: Math.max(bw, Math.round(w * 0.80 / 2.5) * 2.5), reps: '2 تكرار', rest: '90 ثانية' },
      { set: 'مجموعة 5 (تحفيز أقصى)', pct: '90%', weight: Math.max(bw, Math.round(w * 0.90 / 2.5) * 2.5), reps: '1 تكرار', rest: '120 ثانية' },
      { set: 'مجموعات العمل (Work Sets)', pct: '100%', weight: w, reps: 'حسب الخطة', rest: '2-3 دقائق' }
    ];
  }

  function openGymWarmupCalc(prefillWeight){
    const modal = document.getElementById('gymWarmupCalcModal');
    if(!modal) return;
    if(prefillWeight){
      const input = document.getElementById('calcWarmupTargetWeight');
      if(input) input.value = prefillWeight;
    }
    updateWarmupCalcDisplay();
    modal.classList.add('open');
  }

  function closeGymWarmupCalc(){
    const modal = document.getElementById('gymWarmupCalcModal');
    if(modal) modal.classList.remove('open');
  }

  function getPlateColor(weight){
    switch(weight){
      case 25: return '#dc2626';
      case 20: return '#2563eb';
      case 15: return '#ca8a04';
      case 10: return '#16a34a';
      case 5: return '#64748b';
      case 2.5: return '#ef4444';
      case 1.25: return '#94a3b8';
      default: return '#3b82f6';
    }
  }

  function updateWarmupCalcDisplay(){
    const w = parseFloat(document.getElementById('calcWarmupTargetWeight')?.value) || 100;
    const bar = parseFloat(document.getElementById('calcWarmupBarType')?.value) || 20;

    const breakdown = computePlateBreakdown(w, bar);
    const container = document.getElementById('plateDiscsContainer');
    const pills = document.getElementById('plateSummaryPills');

    if(container){
      if(breakdown.plates.length === 0){
        container.innerHTML = '<span style="font-size:0.8rem; color:var(--muted); margin:0 8px;">لا توجد أوزان إضافية (البار فقط)</span>';
      } else {
        container.innerHTML = breakdown.plates.map(function(p){
          const cls = (p === 2.5) ? 'p2_5' : ((p === 1.25) ? 'p1_25' : ('p' + p));
          return '<div class="plate-disc ' + cls + '" title="' + p + ' كجم">' + p + '</div>';
        }).join('');
      }
    }

    if(pills){
      if(breakdown.plates.length === 0){
        pills.innerHTML = '<div class="plate-pill">وزن كل جانب: 0 كجم</div>';
      } else {
        const counts = {};
        breakdown.plates.forEach(function(p){ counts[p] = (counts[p] || 0) + 1; });
        const pillsHtml = Object.keys(counts).map(function(p){
          return '<div class="plate-pill">' +
            '<span class="plate-dot" style="background:' + getPlateColor(parseFloat(p)) + '"></span>' +
            p + ' كجم &times; ' + counts[p] +
          '</div>';
        }).join('');
        pills.innerHTML = '<div class="plate-pill" style="font-weight:700; color:var(--accent);">لكل جانب: ' + breakdown.sideWeight + ' كجم</div>' + pillsHtml;
      }
    }

    const tbody = document.getElementById('warmupSetsTableBody');
    if(tbody){
      const sets = computeWarmupSetsList(w, bar);
      tbody.innerHTML = sets.map(function(s){
        return '<tr>' +
          '<td style="font-weight:700;">' + s.set + '</td>' +
          '<td style="color:var(--accent);">' + s.pct + '</td>' +
          '<td style="font-weight:700; font-family:\'IBM Plex Mono\', monospace;">' + s.weight + ' كجم</td>' +
          '<td>' + s.reps + '</td>' +
          '<td style="color:var(--muted); font-size:0.8rem;">' + s.rest + '</td>' +
        '</tr>';
      }).join('');
    }
  }

  // ================= 3. LIVE EXERCISE SWAP ("الجهاز مشغول؟") =================
  let currentSwapExKey = null;

  function findMuscleGroupForExercise(exKey){
    const catalog = Array.isArray(window.ZATOONA_EXERCISE_CATALOG) ? window.ZATOONA_EXERCISE_CATALOG : [];
    const catItem = catalog.find(function(c){ return c.id === exKey || c.id === ('barbell_' + exKey) || c.id === ('dumbbell_' + exKey); });
    if(catItem && Array.isArray(catItem.primaryMuscles) && catItem.primaryMuscles.length > 0){
      return catItem.primaryMuscles[0];
    }
    const k = (exKey || '').toLowerCase();
    if(k.includes('bench') || k.includes('chest') || k.includes('pushup') || k.includes('dip')) return 'chest';
    if(k.includes('row') || k.includes('pull') || k.includes('lat') || k.includes('chin')) return 'back';
    if(k.includes('press') || k.includes('shoulder') || k.includes('lateral')) return 'shoulders';
    if(k.includes('squat') || k.includes('leg_press') || k.includes('lunge') || k.includes('quad')) return 'quadriceps';
    if(k.includes('deadlift') || (k.includes('curl') && k.includes('leg')) || k.includes('rdl')) return 'hamstrings';
    if(k.includes('curl')) return 'biceps';
    if(k.includes('tricep') || k.includes('extension')) return 'triceps';
    if(k.includes('calf') || k.includes('calves')) return 'calves';
    return 'chest';
  }

  function openExerciseSwapModal(exKey){
    currentSwapExKey = exKey;
    const modal = document.getElementById('gymExerciseSwapModal');
    if(!modal) return;

    const catalog = Array.isArray(window.ZATOONA_EXERCISE_CATALOG) ? window.ZATOONA_EXERCISE_CATALOG : [];
    const defaults = getP3DefaultExercises();
    const def = defaults.find(function(d){ return d.key === exKey; }) || catalog.find(function(c){ return c.id === exKey; });

    const nameEl = document.getElementById('swapCurrentExName');
    const targetEl = document.getElementById('swapCurrentExTarget');

    if(nameEl) nameEl.textContent = def ? (def.name || def.nameAr) : (exKey || 'تمرين اليوم');
    if(targetEl) targetEl.textContent = def ? ('العضلات المستهدفة: ' + (def.target || (def.primaryMuscles || []).join(', '))) : '';

    renderSwapAlternatives('all');
    modal.classList.add('open');
  }

  function closeExerciseSwapModal(){
    const modal = document.getElementById('gymExerciseSwapModal');
    if(modal) modal.classList.remove('open');
  }

  function renderSwapAlternatives(equipFilter){
    const filter = equipFilter || 'all';
    const listEl = document.getElementById('swapAltList');
    if(!listEl) return;

    const catalog = Array.isArray(window.ZATOONA_EXERCISE_CATALOG) ? window.ZATOONA_EXERCISE_CATALOG : [];
    const targetMuscle = findMuscleGroupForExercise(currentSwapExKey);
    const blacklist = p3StorageGet(KEY_BLACKLIST, {});

    const matches = catalog.filter(function(ex){
      if(ex.id === currentSwapExKey) return false;
      if(blacklist[ex.id]) return false;
      const isTarget = (Array.isArray(ex.primaryMuscles) && ex.primaryMuscles.includes(targetMuscle));
      if(!isTarget) return false;
      if(filter !== 'all'){
        const eq = (ex.equipment || '').toLowerCase();
        if(filter === 'dumbbell' && !eq.includes('dumbbell')) return false;
        if(filter === 'barbell' && !eq.includes('barbell')) return false;
        if(filter === 'machine' && !eq.includes('machine')) return false;
        if(filter === 'cable' && !eq.includes('cable')) return false;
        if(filter === 'bodyweight' && !eq.includes('body')) return false;
      }
      return true;
    });

    if(matches.length === 0){
      listEl.innerHTML = '<div style="text-align:center; padding:20px; color:var(--muted); font-size:0.85rem;">لا توجد بدائل مطابقة لهذا الفلتر حالياً. جرب فلتر "الكل".</div>';
      return;
    }

    listEl.innerHTML = matches.slice(0, 10).map(function(ex){
      return '<div class="swap-alt-card">' +
        '<div class="swap-alt-info">' +
          '<div class="swap-alt-name">' + (ex.nameAr || ex.name) + '</div>' +
          '<div class="swap-alt-sub">الأداة: ' + (ex.equipment || 'غير محدد') + ' • الصعوبة: ' + (ex.level || 'متوسط') + '</div>' +
        '</div>' +
        '<button type="button" class="swap-action-btn" data-swap-id="' + ex.id + '" data-swap-name="' + (ex.nameAr || ex.name) + '">استبدال الآن 🔄</button>' +
      '</div>';
    }).join('');

    listEl.querySelectorAll('.swap-action-btn').forEach(function(btn){
      btn.addEventListener('click', function(){
        const newId = btn.dataset.swapId;
        const newName = btn.dataset.swapName;
        performSwap(currentSwapExKey, newId, newName);
      });
    });
  }

  function performSwap(oldKey, newId, newName){
    try {
      const overrides = (typeof loadExerciseOverrides === 'function') ? loadExerciseOverrides() : {};
      overrides[oldKey] = Object.assign({}, overrides[oldKey] || {}, {
        name: newName,
        catalogSwapId: newId,
        swappedAt: new Date().toISOString()
      });
      if(typeof saveExerciseOverrides === 'function') saveExerciseOverrides(overrides);
      if(typeof rebuildExercises === 'function') rebuildExercises();
      if(typeof renderExercises === 'function') renderExercises();
      closeExerciseSwapModal();
      triggerP3Haptic(30);
      alert('تم استبدال التمرين بـ "' + newName + '" بنجاح!');
    } catch(e) {
      console.error('[Phase 3 Swap] error:', e);
      alert('حدث خطأ أثناء استبدال التمرين.');
    }
  }

  // ================= 4. BLACKLIST / EXCLUDED EXERCISES =================
  function openGymBlacklistModal(){
    const modal = document.getElementById('gymBlacklistModal');
    if(!modal) return;
    populateBlacklistSelect();
    renderBlacklistedItems();
    modal.classList.add('open');
  }

  function closeGymBlacklistModal(){
    const modal = document.getElementById('gymBlacklistModal');
    if(modal) modal.classList.remove('open');
  }

  function populateBlacklistSelect(){
    const sel = document.getElementById('blacklistExerciseSelect');
    if(!sel) return;
    const catalog = Array.isArray(window.ZATOONA_EXERCISE_CATALOG) ? window.ZATOONA_EXERCISE_CATALOG : [];
    const defaults = getP3DefaultExercises();

    const map = new Map();
    defaults.forEach(function(d){ map.set(d.key, d.name); });
    catalog.forEach(function(c){ map.set(c.id, c.nameAr || c.name); });

    const options = Array.from(map.entries()).map(function(pair){
      return '<option value="' + pair[0] + '">' + pair[1] + '</option>';
    });
    sel.innerHTML = options.join('');
  }

  function renderBlacklistedItems(){
    const container = document.getElementById('blacklistedItemsList');
    if(!container) return;

    const bl = p3StorageGet(KEY_BLACKLIST, {});
    const keys = Object.keys(bl);

    if(keys.length === 0){
      container.innerHTML = '<div style="text-align:center; padding:16px; color:var(--muted); font-size:0.85rem;">لا توجد تمارين محظورة حالياً. جميع التمارين متاحة.</div>';
      return;
    }

    container.innerHTML = keys.map(function(k){
      const item = bl[k];
      const reasonLabel = (item.reason === 'pain') ? '⚠️ يسبب ألماً' : ((item.reason === 'equipment') ? '🚫 غير متوفر' : '❌ غير مفضل');
      return '<div class="swap-alt-card" style="padding:10px 14px;">' +
        '<div class="swap-alt-info">' +
          '<div class="swap-alt-name">' + (item.name || k) + '</div>' +
          '<div class="swap-alt-sub"><span style="color:#ef4444; font-weight:600;">' + reasonLabel + '</span> • محظور من الروتين</div>' +
        '</div>' +
        '<button type="button" class="btn" style="padding:4px 10px; font-size:0.75rem;" data-unblacklist-key="' + k + '">استعادة ✓</button>' +
      '</div>';
    }).join('');

    container.querySelectorAll('[data-unblacklist-key]').forEach(function(btn){
      btn.addEventListener('click', function(){
        unblacklistExercise(btn.dataset.unblacklistKey);
      });
    });
  }

  function blacklistExercise(key, name, reason){
    const bl = p3StorageGet(KEY_BLACKLIST, {});
    bl[key] = { key: key, name: name, reason: reason, timestamp: new Date().toISOString() };
    p3StorageSet(KEY_BLACKLIST, bl);

    try {
      const excluded = (typeof loadExcludedExercises === 'function') ? loadExcludedExercises() : {};
      excluded[key] = true;
      if(typeof saveExcludedExercises === 'function') saveExcludedExercises(excluded);
      if(typeof rebuildExercises === 'function') rebuildExercises();
      if(typeof renderExercises === 'function') renderExercises();
    } catch(e) {}

    renderBlacklistedItems();
  }

  function unblacklistExercise(key){
    const bl = p3StorageGet(KEY_BLACKLIST, {});
    delete bl[key];
    p3StorageSet(KEY_BLACKLIST, bl);

    try {
      const excluded = (typeof loadExcludedExercises === 'function') ? loadExcludedExercises() : {};
      delete excluded[key];
      if(typeof saveExcludedExercises === 'function') saveExcludedExercises(excluded);
      if(typeof rebuildExercises === 'function') rebuildExercises();
      if(typeof renderExercises === 'function') renderExercises();
    } catch(e) {}

    renderBlacklistedItems();
  }

  // ================= 5. MUSCLE RECOVERY HEATMAP =================
  const MUSCLE_DEFINITIONS = [
    { id: 'chest', name: 'الصدر', hoursReq: 48, svgIds: ['svgMuscChest'] },
    { id: 'back', name: 'الظهر واللاتس', hoursReq: 48, svgIds: ['svgMuscBack'] },
    { id: 'shoulders', name: 'الأكتاف', hoursReq: 48, svgIds: ['svgMuscShoulders'] },
    { id: 'biceps', name: 'البايسبس', hoursReq: 36, svgIds: ['svgMuscBicepsL', 'svgMuscBicepsR'] },
    { id: 'triceps', name: 'الترايسبس', hoursReq: 36, svgIds: ['svgMuscTricepsL', 'svgMuscTricepsR'] },
    { id: 'quads', name: 'الفخذ الأمامي', hoursReq: 72, svgIds: ['svgMuscQuadsL', 'svgMuscQuadsR'] },
    { id: 'hamstrings', name: 'الفخذ الخلفي', hoursReq: 72, svgIds: ['svgMuscHamstringsL', 'svgMuscHamstringsR'] },
    { id: 'glutes', name: 'المؤخرة', hoursReq: 48, svgIds: ['svgMuscGlutes'] },
    { id: 'calves', name: 'السمانة', hoursReq: 36, svgIds: ['svgMuscCalvesL', 'svgMuscCalvesR', 'svgMuscCalvesBackL', 'svgMuscCalvesBackR'] },
    { id: 'abs', name: 'البطن والجذع', hoursReq: 24, svgIds: ['svgMuscAbs'] }
  ];

  function computeMuscleRecoveryState(){
    const now = Date.now();
    const muscleLastTrained = {};

    for(let i = 0; i < localStorage.length; i++){
      const k = localStorage.key(i);
      if(k && k.indexOf('ex:') === 0){
        try {
          const raw = localStorage.getItem(k);
          if(!raw) continue;
          const data = JSON.parse(raw);
          const dateStr = k.replace('ex:', '');
          const logTime = new Date(dateStr + 'T12:00:00').getTime();

          Object.keys(data).forEach(function(exKey){
            const st = data[exKey];
            if(st && Array.isArray(st.sets) && st.sets.some(Boolean)){
              const targetMuscle = findMuscleGroupForExercise(exKey);
              if(!muscleLastTrained[targetMuscle] || logTime > muscleLastTrained[targetMuscle]){
                muscleLastTrained[targetMuscle] = logTime;
              }
            }
          });
        } catch(e) {}
      }
    }

    return MUSCLE_DEFINITIONS.map(function(m){
      const last = muscleLastTrained[m.id];
      if(!last){
        return Object.assign({}, m, { hoursAgo: 999, pct: 100, status: 'ready', label: 'جاهزة للتمرين (100%)' });
      }
      const hoursAgo = Math.max(0, Math.round((now - last) / (1000 * 3600)));
      if(hoursAgo < 24){
        const pct = Math.min(40, Math.round((hoursAgo / 24) * 40));
        return Object.assign({}, m, { hoursAgo: hoursAgo, pct: pct, status: 'fatigued', label: 'مجهدة (' + hoursAgo + ' س)' });
      } else if(hoursAgo < m.hoursReq){
        const pct = 40 + Math.round(((hoursAgo - 24) / (m.hoursReq - 24)) * 55);
        return Object.assign({}, m, { hoursAgo: hoursAgo, pct: pct, status: 'recovering', label: 'استشفاء (' + hoursAgo + ' س)' });
      } else {
        return Object.assign({}, m, { hoursAgo: hoursAgo, pct: 100, status: 'ready', label: 'جاهزة بالكامل (100%)' });
      }
    });
  }

  function openGymRecoveryHeatmapModal(){
    const modal = document.getElementById('gymRecoveryHeatmapModal');
    if(!modal) return;
    renderRecoveryHeatmap();
    modal.classList.add('open');
  }

  function closeGymRecoveryHeatmapModal(){
    const modal = document.getElementById('gymRecoveryHeatmapModal');
    if(modal) modal.classList.remove('open');
  }

  function renderRecoveryHeatmap(){
    const state = computeMuscleRecoveryState();
    const grid = document.getElementById('recoveryMuscleGrid');

    state.forEach(function(m){
      const color = (m.status === 'ready') ? '#22c55e' : ((m.status === 'recovering') ? '#eab308' : '#ef4444');
      (m.svgIds || []).forEach(function(svgId){
        const el = document.getElementById(svgId);
        if(el) el.setAttribute('fill', color);
      });
    });

    if(grid){
      grid.innerHTML = state.map(function(m){
        return '<div class="recovery-muscle-card">' +
          '<div class="recovery-muscle-name">' + m.name + '</div>' +
          '<div class="recovery-muscle-status ' + m.status + '">' + m.label + '</div>' +
          '<div class="recovery-progress-bar">' +
            '<div class="recovery-progress-fill ' + m.status + '" style="width:' + m.pct + '%;"></div>' +
          '</div>' +
        '</div>';
      }).join('');
    }
  }

  // ================= 6. GYM BIG-NUMBERS FOCUS MODE =================
  let currentBigNumbersExKey = null;
  let bigNumbersRestInterval = null;
  let bigNumbersRestSecondsLeft = 0;

  function openGymBigNumbersOverlay(exKey){
    const overlay = document.getElementById('gymBigNumbersOverlay');
    if(!overlay) return;

    const defaults = getP3DefaultExercises();
    currentBigNumbersExKey = exKey || (defaults[0] ? defaults[0].key : 'squat');

    updateBigNumbersLiftingView();
    overlay.classList.add('open');
  }

  function closeGymBigNumbersOverlay(){
    const overlay = document.getElementById('gymBigNumbersOverlay');
    if(overlay) overlay.classList.remove('open');
    if(bigNumbersRestInterval){
      clearInterval(bigNumbersRestInterval);
      bigNumbersRestInterval = null;
    }
  }

  function updateBigNumbersLiftingView(){
    const exSt = (typeof exState !== 'undefined' && exState[currentBigNumbersExKey]) ? exState[currentBigNumbersExKey] : { sets:[false,false,false], weight:'80', reps:'10' };
    const defaults = getP3DefaultExercises();
    const def = defaults.find(function(d){ return d.key === currentBigNumbersExKey; });

    const titleEl = document.getElementById('gbnExTitle');
    const setIndEl = document.getElementById('gbnSetIndicator');
    const wEl = document.getElementById('gbnWeightNumber');
    const rEl = document.getElementById('gbnRepsNumber');

    if(titleEl) titleEl.textContent = def ? def.name : currentBigNumbersExKey;

    const totalSets = (exSt.sets || []).length || 3;
    const doneSets = (exSt.sets || []).filter(Boolean).length;
    const curSetNum = Math.min(totalSets, doneSets + 1);

    if(setIndEl) setIndEl.textContent = 'مجموعة ' + curSetNum + ' من ' + totalSets;
    if(wEl) wEl.textContent = exSt.weight || '80.0';
    if(rEl) rEl.textContent = exSt.reps || '10';

    document.getElementById('gbnLiftingView')?.classList.remove('hidden');
    document.getElementById('gbnRestView')?.classList.add('hidden');
  }

  function onBigNumbersSetDone(){
    triggerP3Haptic(40);
    playP3Tone(880, 150, 'triangle');

    const iso = (typeof weekDates !== 'undefined' && typeof selectedIdx !== 'undefined' && weekDates[selectedIdx]) ? toISO(weekDates[selectedIdx]) : null;
    if(typeof exState !== 'undefined' && exState[currentBigNumbersExKey]){
      const st = exState[currentBigNumbersExKey];
      const undoneIdx = (st.sets || []).findIndex(function(s){ return !s; });
      if(undoneIdx !== -1){
        st.sets[undoneIdx] = true;
        if(typeof saveEx === 'function') saveEx(iso, exState);
        if(typeof renderExercises === 'function') renderExercises();
      }
    }

    startBigNumbersRestCountdown(90);
  }

  function startBigNumbersRestCountdown(seconds){
    const sec = seconds || 90;
    document.getElementById('gbnLiftingView')?.classList.add('hidden');
    document.getElementById('gbnRestView')?.classList.remove('hidden');

    bigNumbersRestSecondsLeft = sec;
    updateBigNumbersRestDisplay();

    if(bigNumbersRestInterval) clearInterval(bigNumbersRestInterval);
    bigNumbersRestInterval = setInterval(function(){
      bigNumbersRestSecondsLeft--;
      if(bigNumbersRestSecondsLeft <= 0){
        clearInterval(bigNumbersRestInterval);
        bigNumbersRestInterval = null;
        triggerP3Haptic(60);
        playP3Tone(550, 300, 'square');
        updateBigNumbersLiftingView();
      } else {
        updateBigNumbersRestDisplay();
      }
    }, 1000);
  }

  function updateBigNumbersRestDisplay(){
    const tEl = document.getElementById('gbnRestTimerText');
    if(tEl){
      const m = Math.floor(bigNumbersRestSecondsLeft / 60);
      const s = bigNumbersRestSecondsLeft % 60;
      tEl.textContent = String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
    }
  }

  // ================= 7. TEMPO CADENCE METRONOME =================
  let tempoRunning = false;
  let tempoTimer = null;
  let tempoPhaseIdx = 0;
  let tempoSecondsLeft = 0;
  let tempoRepsCount = 0;
  let tempoSoundEnabled = true;

  const TEMPO_PRESETS = {
    '3-0-1-0': [3, 0, 1, 0],
    '4-1-1-0': [4, 1, 1, 0],
    '2-0-1-0': [2, 0, 1, 0],
    '3-2-1-0': [3, 2, 1, 0]
  };

  function openGymTempoModal(){
    const modal = document.getElementById('gymTempoModal');
    if(!modal) return;
    modal.classList.add('open');
  }

  function closeGymTempoModal(){
    const modal = document.getElementById('gymTempoModal');
    if(modal) modal.classList.remove('open');
    stopTempoMetronome();
  }

  function getActiveTempoValues(){
    const preset = document.getElementById('tempoPresetSelect')?.value || '3-0-1-0';
    if(preset === 'custom'){
      return [
        parseInt(document.getElementById('tempoEccentric')?.value, 10) || 3,
        parseInt(document.getElementById('tempoPauseBottom')?.value, 10) || 0,
        parseInt(document.getElementById('tempoConcentric')?.value, 10) || 1,
        parseInt(document.getElementById('tempoPauseTop')?.value, 10) || 0
      ];
    }
    return TEMPO_PRESETS[preset] || [3, 0, 1, 0];
  }

  function startTempoMetronome(){
    tempoRunning = true;
    tempoPhaseIdx = 0;
    const values = getActiveTempoValues();
    tempoSecondsLeft = values[0] || 1;

    const btn = document.getElementById('btnToggleTempoPlay');
    if(btn) btn.textContent = '⏸️ إيقاف مؤقت';

    runTempoTick();
    tempoTimer = setInterval(runTempoTick, 1000);
  }

  function stopTempoMetronome(){
    tempoRunning = false;
    if(tempoTimer){
      clearInterval(tempoTimer);
      tempoTimer = null;
    }
    const btn = document.getElementById('btnToggleTempoPlay');
    if(btn) btn.textContent = '▶️ تشغيل الوتيرة';

    const nameEl = document.getElementById('tempoStepName');
    const countEl = document.getElementById('tempoStepCount');
    if(nameEl) nameEl.textContent = 'جاهز؟';
    if(countEl) countEl.textContent = '0';
  }

  function runTempoTick(){
    const values = getActiveTempoValues();
    const phaseNames = ['نزول سلبي ⬇️', 'ثبات تحت ⏸️', 'صعود ودفع ⬆️', 'ثبات فوق ⏸️'];
    const phaseColors = ['#f59e0b', '#3b82f6', '#22c55e', '#64748b'];

    const circle = document.getElementById('tempoPulsingCircle');
    const nameEl = document.getElementById('tempoStepName');
    const countEl = document.getElementById('tempoStepCount');

    if(nameEl) nameEl.textContent = phaseNames[tempoPhaseIdx];
    if(countEl) countEl.textContent = tempoSecondsLeft;
    if(circle) circle.style.borderColor = phaseColors[tempoPhaseIdx];

    if(tempoSoundEnabled){
      if(tempoPhaseIdx === 2){
        playP3Tone(880, 80, 'sine');
      } else {
        playP3Tone(440, 40, 'sine');
      }
    }

    tempoSecondsLeft--;
    if(tempoSecondsLeft <= 0){
      do {
        tempoPhaseIdx = (tempoPhaseIdx + 1) % 4;
        tempoSecondsLeft = values[tempoPhaseIdx];
        if(tempoPhaseIdx === 0){
          tempoRepsCount++;
          const repsEl = document.getElementById('tempoRepsCounter');
          if(repsEl) repsEl.textContent = 'تكرارات المترونوم: ' + tempoRepsCount;
          triggerP3Haptic(25);
        }
      } while(tempoSecondsLeft === 0);
    }
  }

  // ================= 8. INJURY & PAIN FLAGGING =================
  function openGymPainTrackerModal(prefillKey){
    const modal = document.getElementById('gymPainTrackerModal');
    if(!modal) return;
    populatePainExerciseSelect(prefillKey);
    renderActivePainFlags();
    modal.classList.add('open');
  }

  function closeGymPainTrackerModal(){
    const modal = document.getElementById('gymPainTrackerModal');
    if(modal) modal.classList.remove('open');
  }

  function populatePainExerciseSelect(selectedKey){
    const sel = document.getElementById('painExerciseSelect');
    if(!sel) return;
    const defaults = getP3DefaultExercises();
    const catalog = Array.isArray(window.ZATOONA_EXERCISE_CATALOG) ? window.ZATOONA_EXERCISE_CATALOG : [];

    const map = new Map();
    defaults.forEach(function(d){ map.set(d.key, d.name); });
    catalog.forEach(function(c){ map.set(c.id, c.nameAr || c.name); });

    sel.innerHTML = Array.from(map.entries()).map(function(pair){
      return '<option value="' + pair[0] + '" ' + (pair[0] === selectedKey ? 'selected' : '') + '>' + pair[1] + '</option>';
    }).join('');
  }

  function renderActivePainFlags(){
    const container = document.getElementById('activePainFlagsList');
    if(!container) return;

    const flags = p3StorageGet(KEY_PAIN_FLAGS, {});
    const keys = Object.keys(flags);

    if(keys.length === 0){
      container.innerHTML = '<div style="text-align:center; padding:16px; color:var(--muted); font-size:0.85rem;">لا توجد آلام أو إصابات مسجلة حالياً. تدريب آمن! 🌟</div>';
      return;
    }

    container.innerHTML = keys.map(function(k){
      const f = flags[k];
      return '<div class="swap-alt-card" style="padding:10px 14px;">' +
        '<div class="swap-alt-info">' +
          '<div class="swap-alt-name">' + (f.exName || k) + '</div>' +
          '<div class="swap-alt-sub" style="color:#ef4444; font-weight:600;">' +
            'موضع الألم: ' + f.joint + ' • شدة ' + f.intensity + '/10' +
          '</div>' +
          (f.notes ? ('<div style="font-size:0.75rem; color:var(--muted);">' + f.notes + '</div>') : '') +
        '</div>' +
        '<button type="button" class="btn" style="padding:4px 10px; font-size:0.75rem;" data-clear-pain-key="' + k + '">تم الشفاء ✓</button>' +
      '</div>';
    }).join('');

    container.querySelectorAll('[data-clear-pain-key]').forEach(function(btn){
      btn.addEventListener('click', function(){
        clearPainFlag(btn.dataset.clearPainKey);
      });
    });
  }

  function savePainFlag(){
    const exKey = document.getElementById('painExerciseSelect')?.value;
    const exName = document.getElementById('painExerciseSelect')?.selectedOptions[0]?.text || exKey;
    const joint = document.getElementById('painJointSelect')?.value || 'الكتف';
    const intensity = document.getElementById('painIntensitySelect')?.value || '6';
    const notes = (document.getElementById('painNotesInput')?.value || '').trim();

    if(!exKey) return;

    const flags = p3StorageGet(KEY_PAIN_FLAGS, {});
    flags[exKey] = {
      exKey: exKey, exName: exName, joint: joint, intensity: intensity, notes: notes,
      timestamp: new Date().toISOString()
    };
    p3StorageSet(KEY_PAIN_FLAGS, flags);

    renderActivePainFlags();
    if(typeof renderExercises === 'function') renderExercises();
    triggerP3Haptic(25);
    alert('تم تسجيل تنبيه الألم للتمرين بنجاح.');
  }

  function clearPainFlag(exKey){
    const flags = p3StorageGet(KEY_PAIN_FLAGS, {});
    delete flags[exKey];
    p3StorageSet(KEY_PAIN_FLAGS, flags);
    renderActivePainFlags();
    if(typeof renderExercises === 'function') renderExercises();
  }

  // ================= 9. ONGOING WORKOUT NOTIFICATION & FLOATING HUD =================
  function getExNameByKey(k){
    const catalog = Array.isArray(window.ZATOONA_EXERCISE_CATALOG) ? window.ZATOONA_EXERCISE_CATALOG : [];
    const defaults = getP3DefaultExercises();
    const d = defaults.find(function(item){ return item.key === k; });
    if(d) return d.name;
    const c = catalog.find(function(item){ return item.id === k; });
    if(c) return c.nameAr || c.name;
    return k;
  }

  function updateActiveWorkoutHud(){
    const hud = document.getElementById('gymActiveWorkoutHud');
    if(!hud) return;

    const iso = (typeof weekDates !== 'undefined' && typeof selectedIdx !== 'undefined' && weekDates[selectedIdx]) ? toISO(weekDates[selectedIdx]) : null;
    if(!iso || typeof mode === 'undefined' || mode !== 'gym'){
      hud.classList.add('hidden');
      return;
    }

    const session = (typeof getGymSession === 'function') ? getGymSession(iso) : null;
    const isSessionActive = session && session.status === 'in_progress';
    const defaults = getP3DefaultExercises();

    let hasDoneSets = false;
    let activeEx = null;
    let activeExState = null;

    if(typeof exState !== 'undefined'){
      const allKeys = Object.keys(exState);
      for(let i = 0; i < allKeys.length; i++){
        const k = allKeys[i];
        const st = exState[k];
        if(st && Array.isArray(st.sets) && st.sets.some(Boolean)){
          hasDoneSets = true;
          if(!activeEx && st.sets.some(function(s){ return !s; })){
            activeEx = { key: k, name: getExNameByKey(k) };
            activeExState = st;
          }
        }
      }
    }

    if(!isSessionActive && !hasDoneSets){
      hud.classList.add('hidden');
      try {
        if(window.ZatoonaNativeBridge && typeof window.ZatoonaNativeBridge.hideWorkoutNotification === 'function'){
          window.ZatoonaNativeBridge.hideWorkoutNotification();
        }
      } catch(e) {}
      return;
    }

    hud.classList.remove('hidden');
    if(!activeEx && defaults[0]) {
      activeEx = defaults[0];
      activeExState = (typeof exState !== 'undefined') ? exState[activeEx.key] : null;
    }

    const titleEl = document.getElementById('hudExTitle');
    const setTextEl = document.getElementById('hudSetText');
    const restTextEl = document.getElementById('hudRestText');

    if(titleEl) titleEl.textContent = activeEx ? activeEx.name : 'تمرين اليوم';

    const totalSets = (activeExState && activeExState.sets) ? activeExState.sets.length : 3;
    const doneCount = (activeExState && activeExState.sets) ? activeExState.sets.filter(Boolean).length : 0;
    if(setTextEl) setTextEl.textContent = 'مجموعة ' + Math.min(totalSets, doneCount + 1) + '/' + totalSets;

    const timerState = (typeof loadRestTimerState === 'function') ? loadRestTimerState() : null;
    const remaining = (timerState && typeof getRestTimerRemaining === 'function') ? getRestTimerRemaining(timerState) : null;

    if(remaining && remaining.status === 'running'){
      const m = Math.floor(remaining.remaining / 60);
      const s = remaining.remaining % 60;
      if(restTextEl) restTextEl.textContent = '⏱️ ' + String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
    } else {
      if(restTextEl) restTextEl.textContent = '💤 في انتظار الراحة';
    }

    try {
      if(window.ZatoonaNativeBridge && typeof window.ZatoonaNativeBridge.showWorkoutNotification === 'function'){
        const title = '🏋️ تمرين نشط: ' + (activeEx ? activeEx.name : 'الجيم');
        const text = 'مجموعة ' + Math.min(totalSets, doneCount + 1) + ' من ' + totalSets + ' • ' + (restTextEl ? restTextEl.textContent : '');
        window.ZatoonaNativeBridge.showWorkoutNotification(title, text);
      }
    } catch(e) {}
  }

  // ================= CARD ENHANCEMENT & QUICK BAR =================
  function renderGymToolsQuickBar(){
    const container = document.getElementById('gymToolsQuickBarContainer');
    if(!container) return;

    if(!container.querySelector('.gym-tools-bar')){
      container.innerHTML = '<div class="gym-tools-bar" id="gymToolsQuickBar">' +
        '<button type="button" class="gym-tool-btn" id="btnGym1RMCalc" title="حاسبة أقصى تكرار ونسب الشدة">' +
          '<span class="gym-tool-icon">🏋️</span>' +
          '<span class="gym-tool-label">حاسبة 1RM</span>' +
        '</button>' +
        '<button type="button" class="gym-tool-btn" id="btnGymWarmupCalc" title="حاسبة مجموعات الإحماء وأقراص البار">' +
          '<span class="gym-tool-icon">🔥</span>' +
          '<span class="gym-tool-label">تسخين وأقراص البار</span>' +
        '</button>' +
        '<button type="button" class="gym-tool-btn" id="btnGymExerciseSwap" title="بدائل التمرين الفورية لنفس العضلة">' +
          '<span class="gym-tool-icon">🔄</span>' +
          '<span class="gym-tool-label">الجهاز مشغول؟</span>' +
        '</button>' +
        '<button type="button" class="gym-tool-btn" id="btnGymBlacklist" title="إدارة التمارين المستبعدة والمحظورة">' +
          '<span class="gym-tool-icon">🚫</span>' +
          '<span class="gym-tool-label">حظر التمارين</span>' +
        '</button>' +
        '<button type="button" class="gym-tool-btn" id="btnGymRecoveryHeatmap" title="خريطة استشفاء العضلات التفاعلية">' +
          '<span class="gym-tool-icon">🗺️</span>' +
          '<span class="gym-tool-label">خريطة الاستشفاء</span>' +
        '</button>' +
        '<button type="button" class="gym-tool-btn" id="btnGymTempo" title="مؤقت وتيرة النزول والصعود">' +
          '<span class="gym-tool-icon">⏱️</span>' +
          '<span class="gym-tool-label">وتيرة التيمبو</span>' +
        '</button>' +
        '<button type="button" class="gym-tool-btn" id="btnGymPainTracker" title="سجل رصد الآلام والوقاية من الإصابات">' +
          '<span class="gym-tool-icon">⚠️</span>' +
          '<span class="gym-tool-label">رصد الآلام</span>' +
        '</button>' +
        '<button type="button" class="gym-tool-btn" id="btnGymBigNumbers" title="وضع الأرقام الضخمة للتركيز أثناء الرفع">' +
          '<span class="gym-tool-icon">⚡</span>' +
          '<span class="gym-tool-label">تركيز ضخم</span>' +
        '</button>' +
      '</div>';

      container.querySelector('#btnGym1RMCalc')?.addEventListener('click', function(){ openGym1RMCalc(); });
      container.querySelector('#btnGymWarmupCalc')?.addEventListener('click', function(){ openGymWarmupCalc(); });
      container.querySelector('#btnGymExerciseSwap')?.addEventListener('click', function(){ openExerciseSwapModal(null); });
      container.querySelector('#btnGymBlacklist')?.addEventListener('click', function(){ openGymBlacklistModal(); });
      container.querySelector('#btnGymRecoveryHeatmap')?.addEventListener('click', function(){ openGymRecoveryHeatmapModal(); });
      container.querySelector('#btnGymTempo')?.addEventListener('click', function(){ openGymTempoModal(); });
      container.querySelector('#btnGymPainTracker')?.addEventListener('click', function(){ openGymPainTrackerModal(); });
      container.querySelector('#btnGymBigNumbers')?.addEventListener('click', function(){ openGymBigNumbersOverlay(); });
    }
  }

  function enhanceRenderedCardsPhase3(list, iso){
    const cards = document.querySelectorAll('#exercises .ex-card');
    const flags = p3StorageGet(KEY_PAIN_FLAGS, {});

    cards.forEach(function(card, idx){
      const ex = list[idx];
      if(!ex) return;

      if(flags[ex.key] && !card.querySelector('.ex-pain-alert')){
        const f = flags[ex.key];
        const alertEl = document.createElement('div');
        alertEl.className = 'ex-pain-alert';
        alertEl.innerHTML = '<span>⚠️ تم رصد ألم في ' + f.joint + ' (شدة ' + f.intensity + '/10). خفف المدى الحركي أو بدّل التمرين.</span>' +
          '<button type="button" class="btn-swap-from-alert" data-ex-key="' + ex.key + '">بدائل آمنة 🔄</button>';
        alertEl.querySelector('.btn-swap-from-alert')?.addEventListener('click', function(){
          openExerciseSwapModal(ex.key);
        });
        card.insertBefore(alertEl, card.firstChild);
      }

      if(!card.querySelector('.ex-p3-actions-row')){
        const actionsRow = document.createElement('div');
        actionsRow.className = 'ex-p3-actions-row';
        actionsRow.innerHTML = '<button type="button" class="ex-p3-action-btn" data-action="swap" data-key="' + ex.key + '">🔄 الجهاز مشغول؟</button>' +
          '<button type="button" class="ex-p3-action-btn" data-action="1rm" data-key="' + ex.key + '">🏋️ 1RM</button>' +
          '<button type="button" class="ex-p3-action-btn" data-action="warmup" data-key="' + ex.key + '">🔥 تسخين البار</button>' +
          '<button type="button" class="ex-p3-action-btn" data-action="tempo" data-key="' + ex.key + '">⏱️ تيمبو</button>' +
          '<button type="button" class="ex-p3-action-btn" data-action="pain" data-key="' + ex.key + '">⚠️ رصد ألم</button>';

        actionsRow.querySelector('[data-action="swap"]')?.addEventListener('click', function(){ openExerciseSwapModal(ex.key); });
        actionsRow.querySelector('[data-action="1rm"]')?.addEventListener('click', function(){
          const st = (typeof exState !== 'undefined') ? exState[ex.key] : null;
          openGym1RMCalc(ex.key, st ? st.weight : null, st ? st.reps : null);
        });
        actionsRow.querySelector('[data-action="warmup"]')?.addEventListener('click', function(){
          const st = (typeof exState !== 'undefined') ? exState[ex.key] : null;
          openGymWarmupCalc(st ? parseFloat(st.weight) : null);
        });
        actionsRow.querySelector('[data-action="tempo"]')?.addEventListener('click', function(){ openGymTempoModal(); });
        actionsRow.querySelector('[data-action="pain"]')?.addEventListener('click', function(){ openGymPainTrackerModal(ex.key); });

        card.appendChild(actionsRow);
      }
    });

    updateActiveWorkoutHud();
  }

  function onGymSetCompletedPhase3(ex, s, st){
    triggerP3Haptic(25);
    updateActiveWorkoutHud();
  }

  // ================= MODAL & OVERLAY EVENT INITIALIZATION =================
  function initPhase3GymEvents(){
    // 1. 1RM Modal
    document.getElementById('btnClose1RMCalc')?.addEventListener('click', closeGym1RMCalc);
    document.getElementById('calc1rmWeightInput')?.addEventListener('input', update1RMDisplay);
    document.getElementById('calc1rmRepsInput')?.addEventListener('input', update1RMDisplay);
    document.getElementById('calc1rmRpeSelect')?.addEventListener('change', update1RMDisplay);
    document.getElementById('btnSave1RMRecord')?.addEventListener('click', function(){
      const w = parseFloat(document.getElementById('calc1rmWeightInput')?.value) || 0;
      const r = parseInt(document.getElementById('calc1rmRepsInput')?.value, 10) || 1;
      const rir = parseFloat(document.getElementById('calc1rmRpeSelect')?.value) || 0;
      const oneRm = compute1RM(w, r, rir);
      const hist = p3StorageGet(KEY_1RM_HISTORY, []);
      hist.push({ weight: w, reps: r, rir: rir, oneRm: oneRm, timestamp: new Date().toISOString() });
      p3StorageSet(KEY_1RM_HISTORY, hist);
      alert('تم حفظ النتيجة (' + oneRm + ' كجم) في سجل القوة بنجاح!');
    });
    document.getElementById('btnApply1RMToEx')?.addEventListener('click', function(){
      const w = parseFloat(document.getElementById('calc1rmWeightInput')?.value) || 0;
      if(activeTargetExKeyFor1RM && typeof exState !== 'undefined' && exState[activeTargetExKeyFor1RM]){
        exState[activeTargetExKeyFor1RM].weight = String(w);
        const iso = (typeof weekDates !== 'undefined' && typeof selectedIdx !== 'undefined' && weekDates[selectedIdx]) ? toISO(weekDates[selectedIdx]) : null;
        if(typeof saveEx === 'function') saveEx(iso, exState);
        if(typeof renderExercises === 'function') renderExercises();
      }
      closeGym1RMCalc();
    });

    // 2. Warmup Modal
    document.getElementById('btnCloseWarmupCalc')?.addEventListener('click', closeGymWarmupCalc);
    document.getElementById('btnCloseWarmupCalcOk')?.addEventListener('click', closeGymWarmupCalc);
    document.getElementById('calcWarmupTargetWeight')?.addEventListener('input', updateWarmupCalcDisplay);
    document.getElementById('calcWarmupBarType')?.addEventListener('change', updateWarmupCalcDisplay);

    // 3. Swap Modal
    document.getElementById('btnCloseSwapModal')?.addEventListener('click', closeExerciseSwapModal);
    document.getElementById('btnCancelSwap')?.addEventListener('click', closeExerciseSwapModal);
    document.getElementById('swapEquipFilters')?.querySelectorAll('button').forEach(function(btn){
      btn.addEventListener('click', function(){
        document.getElementById('swapEquipFilters').querySelectorAll('button').forEach(function(b){ b.classList.remove('active'); });
        btn.classList.add('active');
        renderSwapAlternatives(btn.dataset.filter);
      });
    });

    // 4. Blacklist Modal
    document.getElementById('btnCloseBlacklistModal')?.addEventListener('click', closeGymBlacklistModal);
    document.getElementById('btnCloseBlacklistOk')?.addEventListener('click', closeGymBlacklistModal);
    document.getElementById('btnToggleBlacklistAdd')?.addEventListener('click', function(){
      document.getElementById('blacklistAddPanel')?.classList.toggle('hidden');
    });
    document.getElementById('btnConfirmBlacklistEx')?.addEventListener('click', function(){
      const sel = document.getElementById('blacklistExerciseSelect');
      const rSel = document.getElementById('blacklistReasonSelect');
      if(sel && rSel){
        const key = sel.value;
        const name = sel.selectedOptions[0]?.text || key;
        const reason = rSel.value;
        blacklistExercise(key, name, reason);
        document.getElementById('blacklistAddPanel')?.classList.add('hidden');
      }
    });

    // 5. Recovery Heatmap Modal
    document.getElementById('btnCloseRecoveryModal')?.addEventListener('click', closeGymRecoveryHeatmapModal);
    document.getElementById('btnCloseRecoveryOk')?.addEventListener('click', closeGymRecoveryHeatmapModal);

    // 6. Tempo Modal
    document.getElementById('btnCloseTempoModal')?.addEventListener('click', closeGymTempoModal);
    document.getElementById('btnCloseTempoOk')?.addEventListener('click', closeGymTempoModal);
    document.getElementById('tempoPresetSelect')?.addEventListener('change', function(e){
      const isCustom = e.target.value === 'custom';
      document.getElementById('tempoCustomInputs')?.classList.toggle('hidden', !isCustom);
      if(tempoRunning) stopTempoMetronome();
    });
    document.getElementById('btnToggleTempoPlay')?.addEventListener('click', function(){
      if(tempoRunning) stopTempoMetronome();
      else startTempoMetronome();
    });
    document.getElementById('btnResetTempoReps')?.addEventListener('click', function(){
      tempoRepsCount = 0;
      const repsEl = document.getElementById('tempoRepsCounter');
      if(repsEl) repsEl.textContent = 'تكرارات المترونوم: 0';
    });
    document.getElementById('btnToggleTempoSound')?.addEventListener('click', function(e){
      tempoSoundEnabled = !tempoSoundEnabled;
      e.target.textContent = tempoSoundEnabled ? '🔊 الصوت: شغال' : '🔇 الصوت: مكتوم';
    });

    // 7. Pain Modal
    document.getElementById('btnClosePainModal')?.addEventListener('click', closeGymPainTrackerModal);
    document.getElementById('btnClosePainOk')?.addEventListener('click', closeGymPainTrackerModal);
    document.getElementById('btnSavePainFlag')?.addEventListener('click', savePainFlag);

    // 8. Big Numbers Overlay
    document.getElementById('gbnCloseBtn')?.addEventListener('click', closeGymBigNumbersOverlay);
    document.getElementById('gbnDoneSetBtn')?.addEventListener('click', onBigNumbersSetDone);
    document.getElementById('gbnPlusWeight')?.addEventListener('click', function(){
      const wEl = document.getElementById('gbnWeightNumber');
      if(wEl){
        const cur = parseFloat(wEl.textContent) || 0;
        wEl.textContent = (cur + 2.5).toFixed(1);
      }
    });
    document.getElementById('gbnMinusWeight')?.addEventListener('click', function(){
      const wEl = document.getElementById('gbnWeightNumber');
      if(wEl){
        const cur = parseFloat(wEl.textContent) || 0;
        wEl.textContent = Math.max(0, cur - 2.5).toFixed(1);
      }
    });
    document.getElementById('gbnPlusReps')?.addEventListener('click', function(){
      const rEl = document.getElementById('gbnRepsNumber');
      if(rEl){
        const cur = parseInt(rEl.textContent, 10) || 0;
        rEl.textContent = cur + 1;
      }
    });
    document.getElementById('gbnMinusReps')?.addEventListener('click', function(){
      const rEl = document.getElementById('gbnRepsNumber');
      if(rEl){
        const cur = parseInt(rEl.textContent, 10) || 0;
        rEl.textContent = Math.max(1, cur - 1);
      }
    });
    document.getElementById('gbnAdd30Sec')?.addEventListener('click', function(){
      bigNumbersRestSecondsLeft += 30;
      updateBigNumbersRestDisplay();
    });
    document.getElementById('gbnSkipRest')?.addEventListener('click', function(){
      if(bigNumbersRestInterval) clearInterval(bigNumbersRestInterval);
      bigNumbersRestInterval = null;
      updateBigNumbersLiftingView();
    });
    document.getElementById('gbnToggleFs')?.addEventListener('click', function(){
      const el = document.getElementById('gymBigNumbersOverlay');
      if(!document.fullscreenElement){
        if(el && el.requestFullscreen) el.requestFullscreen();
      } else {
        if(document.exitFullscreen) document.exitFullscreen();
      }
    });

    // 9. Floating HUD
    document.getElementById('hudOpenFocusBtn')?.addEventListener('click', function(){
      openGymBigNumbersOverlay();
    });
    document.getElementById('hudToggleFocusMode')?.addEventListener('click', function(){
      openGymBigNumbersOverlay();
    });
    document.getElementById('hudQuickSetDone')?.addEventListener('click', function(){
      onBigNumbersSetDone();
    });
  }

  // Hook into window load or initial bootstrap
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initPhase3GymEvents);
  } else {
    initPhase3GymEvents();
  }

  // Expose global Phase 3 functions
  window.renderGymToolsQuickBar = renderGymToolsQuickBar;
  window.enhanceRenderedCardsPhase3 = enhanceRenderedCardsPhase3;
  window.updateActiveWorkoutHud = updateActiveWorkoutHud;
  window.onGymSetCompletedPhase3 = onGymSetCompletedPhase3;

  window.openGym1RMCalc = openGym1RMCalc;
  window.openGymWarmupCalc = openGymWarmupCalc;
  window.openExerciseSwapModal = openExerciseSwapModal;
  window.openGymBlacklistModal = openGymBlacklistModal;
  window.openGymRecoveryHeatmapModal = openGymRecoveryHeatmapModal;
  window.openGymTempoModal = openGymTempoModal;
  window.openGymPainTrackerModal = openGymPainTrackerModal;
  window.openGymBigNumbersOverlay = openGymBigNumbersOverlay;
})();
/* ================= END PHASE 3: NEXT-GEN GYM & STRENGTH ENGINE ================= */

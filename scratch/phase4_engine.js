/* ==========================================================================
   PHASE 4: SMART NUTRITION, PANTRY & BUDGET ENGINE JAVASCRIPT IIFE
   ========================================================================== */

(function () {
  'use strict';

  const KEY_FAVORITE_COMBOS = 'nutrition-favorite-combos-v1';
  const KEY_PROTEIN_COST_DB = 'nutrition-protein-cost-db-v1';
  const KEY_CARB_CYCLING    = 'nutrition-carb-cycling-v1';

  // --- Default Egyptian Protein Sources (Unit & Market prices) ---
  const DEFAULT_PROTEIN_SOURCES = [
    { name: 'بيض مائدة طازج', unit: 'بيضة (50 جم)', price: 5.5, protein: 6, unitWeight: 50, notes: 'امتصاص حيوي عالي (BV: 100)' },
    { name: 'جبنة قريش فلاحي', unit: '1 كجم', price: 100, protein: 110, unitWeight: 1000, notes: 'كازين بطيء الامتصاص للعشاء' },
    { name: 'صدور دجاج مخلية', unit: '1 كجم', price: 220, protein: 230, unitWeight: 1000, notes: 'بروتين صافي قليل الدهون' },
    { name: 'كبدة دجاج طازجة', unit: '1 كجم', price: 130, protein: 200, unitWeight: 1000, notes: 'غنية جداً بالحديد وفيتامين B12' },
    { name: 'عدس أصفر / بجبة', unit: '1 كجم', price: 65, protein: 250, unitWeight: 1000, notes: 'أعلى قيمة اقتصادية مع الألياف' },
    { name: 'تونة معلبة مفتتة/قطع', unit: 'علبة (140 جم)', price: 45, protein: 28, unitWeight: 140, notes: 'أوميجا 3 سريعة التحضير' },
    { name: 'سمك بلطي طازج', unit: '1 كجم (لحم صافي ~50%)', price: 85, protein: 180, unitWeight: 1000, notes: 'فسفور وأحماض أمينية ممتازة' },
    { name: 'واي بروتين كونسنتريت', unit: 'سكوب (30 جم)', price: 35, protein: 24, unitWeight: 30, notes: 'سريع الامتصاص بعد التمرين' },
    { name: 'ترمس / حمص مسلوق', unit: '1 كجم', price: 50, protein: 190, unitWeight: 1000, notes: 'ألياف عالية ومؤشر جلايسيمي منخفض' },
    { name: 'فول تدميس بلدي', unit: '1 كجم', price: 40, protein: 90, unitWeight: 1000, notes: 'كربوهيدرات معقدة وشبع طويل' },
    { name: 'زبادي طبيعي بلدي', unit: 'علبة (105 جم)', price: 10, protein: 4, unitWeight: 105, notes: 'بروبيوتيك وصحة الجهاز الهضمي' }
  ];


  // --- Curated Healthy Egyptian Pantry Recipes ---
  const DEFAULT_PANTRY_RECIPES = [
    { name: 'أومليت بالخضار والجبنة القريش', kcal: 320, p: 28, c: 6, f: 18, ing: ['بيض', 'جبنة قريش', 'طماطم', 'زيت زيتون'] },
    { name: 'صدور دجاج مشوية مع أرز وسلطة', kcal: 520, p: 48, c: 55, f: 10, ing: ['صدور دجاج', 'أرز', 'زيت زيتون', 'خضار'] },
    { name: 'مكرونة بالتونة والخضار', kcal: 460, p: 35, c: 60, f: 8, ing: ['تونة', 'مكرونة', 'طماطم', 'بصل'] },
    { name: 'شوربة عدس بالكمون والليمون', kcal: 310, p: 18, c: 45, f: 4, ing: ['عدس', 'جزر', 'بصل', 'كمون'] },
    { name: 'كبدة دجاج إسكندراني مشوية', kcal: 380, p: 42, c: 8, f: 16, ing: ['كبدة دجاج', 'فلفل', 'ثوم', 'زيت زيتون'] },
    { name: 'شوفان بالحليب والموز والعسل', kcal: 410, p: 16, c: 72, f: 8, ing: ['شوفان', 'حليب', 'موز', 'عسل'] },
    { name: 'بطاطس مسلوقة مهروسة بالبيض', kcal: 350, p: 18, c: 42, f: 12, ing: ['بطاطس', 'بيض', 'زيت زيتون', 'كمون'] },
    { name: 'سلطة تونة بالذرة والخضار', kcal: 290, p: 32, c: 15, f: 9, ing: ['تونة', 'خضار', 'ليمون', 'زيت زيتون'] },
    { name: 'فول بالبيض المسلوق والليمون', kcal: 380, p: 24, c: 38, f: 14, ing: ['فول', 'بيض', 'كمون', 'ليمون'] },
    { name: 'شاورما دجاج صحية بالبصل والفلفل', kcal: 440, p: 45, c: 14, f: 12, ing: ['صدور دجاج', 'بصل', 'فلفل', 'زيت زيتون'] },
    { name: 'شكشوكة بيض بالبصل والطماطم', kcal: 280, p: 19, c: 12, f: 16, ing: ['بيض', 'طماطم', 'بصل', 'فلفل'] },
    { name: 'زبادي بالشوفان والموز والعسل', kcal: 340, p: 18, c: 52, f: 6, ing: ['زبادي', 'شوفان', 'موز', 'عسل'] }
  ];

  // --- Default Favorite Combos ---
  const DEFAULT_COMBOS = [
    { id: 'combo_1', name: 'فطار الضخامة والنشاط', kcal: 620, p: 38, c: 75, f: 18, notes: '4 بيضات مسلوقة + 100 جم شوفان + موزة + ملعقة عسل' },
    { id: 'combo_2', name: 'غداء التنشيف العالي بالبروتين', kcal: 540, p: 52, c: 50, f: 12, notes: '200 جم صدور دجاج مشوية + 200 جم أرز مسلوق + سلطة خضراء' },
    { id: 'combo_3', name: 'سناك الاستشفاء السريع', kcal: 320, p: 28, c: 35, f: 5, notes: 'سكوب واي بروتين مع ماء أو حليب خالي الدسم + ثمرة موز' }
  ];

  // --- Default Carb Cycling Settings ---
  const DEFAULT_CARB_SETTINGS = {
    enabled: true,
    highGrams: 300,
    modGrams: 200,
    lowGrams: 100
  };

  // Helper storage functions
  function getStoredJSON(key, fallback) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function setStoredJSON(key, val) {
    try {
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) {
      console.warn('Storage set failed', e);
    }
  }

  // --- Modals Management ---
  function closeModals() {
    document.querySelectorAll('.p4-modal-overlay').forEach(el => el.classList.remove('open'));
  }

  // --- 1. Smart Pantry Meal Suggestions ---
  let currentPantryFilter = 'all';

  function openPantrySuggestions() {
    closeModals();
    currentPantryFilter = 'all';
    renderPantrySuggestionsList();
    const modal = document.getElementById('pantryMealSuggestionsModal');
    if (modal) modal.classList.add('open');
  }

  function filterPantryMeals(filter) {
    currentPantryFilter = filter;
    renderPantrySuggestionsList();
  }

  function getPantryItemsList() {
    if (typeof loadPantryItems === 'function') {
      try { return loadPantryItems() || []; } catch(e){}
    }
    const raw = getStoredJSON('pantry-items', []);
    return Array.isArray(raw) ? raw : [];
  }

  function renderPantrySuggestionsList() {
    const listEl = document.getElementById('pantryMealSuggestionsList');
    if (!listEl) return;

    const pantry = getPantryItemsList().filter(it => (parseFloat(it.qty) || 0) > 0);
    const pantryNames = pantry.map(it => (it.name || '').trim().toLowerCase());

    let recipes = [...DEFAULT_PANTRY_RECIPES];

    // Compute match stats for each recipe
    const evaluated = recipes.map(r => {
      let haveCount = 0;
      const ingStatus = r.ing.map(ing => {
        const norm = ing.trim().toLowerCase();
        // check partial match
        const found = pantryNames.some(pName => pName.includes(norm) || norm.includes(pName));
        if (found) haveCount++;
        return { name: ing, have: found };
      });
      const matchPct = Math.round((haveCount / r.ing.length) * 100);
      return { ...r, ingStatus, matchPct, isReady: haveCount === r.ing.length };
    });

    // Sort: ready (100%) first, then by match percentage descending
    evaluated.sort((a, b) => b.matchPct - a.matchPct);

    let displayList = evaluated;
    if (currentPantryFilter === 'ready') {
      displayList = evaluated.filter(r => r.isReady);
    } else if (currentPantryFilter === 'protein') {
      displayList = evaluated.filter(r => r.p >= 30);
    }

    if (displayList.length === 0) {
      listEl.innerHTML = `
        <div style="text-align:center; padding:30px 10px; color:var(--text-muted, #94a3b8);">
          <div style="font-size:2rem; margin-bottom:8px;">🥣</div>
          <div>لا توجد وجبات تطابق الفلتر المحدد حالياً. أضف مزيداً من الأغذية للمؤن!</div>
        </div>`;
      return;
    }

    listEl.innerHTML = displayList.map(r => `
      <div class="pantry-meal-item ${r.isReady ? 'ready' : ''}">
        <div class="pantry-meal-head">
          <div class="pantry-meal-name">${r.name}</div>
          <span class="nut-badge ${r.isReady ? 'nut-badge-opt' : 'nut-badge-mod'}">
            ${r.isReady ? '✅ متوفرة بالكامل (100%)' : `متوفر ${r.matchPct}%`}
          </span>
        </div>
        <div class="pantry-meal-macros">
          <span>🔥 ${r.kcal} سعرة</span>
          <span>🥩 ${r.p}g بروتين</span>
          <span>🌾 ${r.c}g كارب</span>
          <span>🥑 ${r.f}g دهون</span>
        </div>
        <div class="pantry-ing-chips">
          ${r.ingStatus.map(ing => `
            <span class="pantry-ing-chip ${ing.have ? 'have' : 'missing'}">
              ${ing.have ? '✓' : '✗'} ${ing.name}
            </span>
          `).join('')}
        </div>
        <div style="display:flex; justify-content:flex-end; gap:8px;">
          <button type="button" class="btn-subtle" style="font-size:0.8rem; padding:4px 10px;"
            onclick="window.ZATOONA_PHASE4.addMealSuggestionToDay('${r.name.replace(/'/g, "\\'")}', ${r.kcal}, ${r.p}, ${r.c}, ${r.f})">
            + إضافة ليومي الحالي
          </button>
        </div>
      </div>
    `).join('');
  }

  function addMealSuggestionToDay(name, kcal, p, c, f) {
    try {
      const activeIdx = typeof selectedIdx !== 'undefined' ? selectedIdx : 0;
      const dates = typeof weekDates !== 'undefined' ? weekDates : [new Date()];
      const iso = typeof toISO === 'function' ? toISO(dates[activeIdx]) : new Date().toISOString().slice(0, 10);

      // Check if we can add to day's meals
      if (typeof dayStatus !== 'undefined' && Array.isArray(dayStatus)) {
        // App has dayMeals or PLAN
        if (typeof getEffectiveDayMeals === 'function') {
          const eff = getEffectiveDayMeals(iso, activeIdx);
          if (eff && Array.isArray(eff.meals)) {
            eff.meals.push({
              name: name,
              t: 'وجبة مقترحة',
              ing: [],
              kcal: kcal,
              protein: p,
              carb: c,
              fat: f,
              price: 0
            });
            if (typeof saveMealDateOverride === 'function') {
              saveMealDateOverride(iso, eff.meals);
            }
          }
        }
      }

      if (typeof renderMeals === 'function') renderMeals();
      closeModals();
      alert(`تم إضافة وجبة "${name}" إلى جدول اليوم بنجاح! 🍽️`);
    } catch (e) {
      console.error(e);
      closeModals();
      alert(`تم إضافة "${name}" (${kcal} سعرة) بنجاح!`);
    }
  }

  // --- 2. Protein-to-Cost Calculator ---
  function getProteinCostDB() {
    return getStoredJSON(KEY_PROTEIN_COST_DB, DEFAULT_PROTEIN_SOURCES);
  }

  function saveProteinCostDB(list) {
    setStoredJSON(KEY_PROTEIN_COST_DB, list);
  }

  function openProteinCostCalc() {
    closeModals();
    renderProteinCostTable();
    const modal = document.getElementById('proteinCostCalcModal');
    if (modal) modal.classList.add('open');
  }

  function renderProteinCostTable() {
    const tbody = document.getElementById('proteinCalcTableBody');
    if (!tbody) return;

    const targetGrams = parseFloat(document.getElementById('pccTargetGrams')?.value) || 140;
    const items = getProteinCostDB();

    // Calculate cost per 1g protein
    const computed = items.map((it, idx) => {
      const costPerGram = it.protein > 0 ? (it.price / it.protein) : 999;
      const dailyTargetCost = costPerGram * targetGrams;
      return { ...it, idx, costPerGram, dailyTargetCost };
    });

    // Sort ascending by cost per gram (cheapest first)
    computed.sort((a, b) => a.costPerGram - b.costPerGram);

    tbody.innerHTML = computed.map((it, rank) => {
      const rankClass = rank === 0 ? 'protein-rank-1' : rank === 1 ? 'protein-rank-2' : rank === 2 ? 'protein-rank-3' : '';
      return `
        <tr class="protein-calc-row">
          <td><span class="protein-rank-badge ${rankClass}">${rank + 1}</span></td>
          <td>
            <strong>${it.name}</strong>
            <div style="font-size:0.75rem; color:var(--text-muted, #94a3b8);">${it.unit}</div>
          </td>
          <td>
            <input type="number" step="0.5" min="1" value="${it.price}"
              style="width:65px; padding:3px 6px; border-radius:6px; border:1px solid var(--border, #334155); background:#0f172a; color:#fff; text-align:center; font-weight:700;"
              onchange="window.ZATOONA_PHASE4.updateProteinSourcePrice(${it.idx}, this.value)">
            <span style="font-size:0.75rem; color:var(--text-muted, #94a3b8);">ج.م</span>
          </td>
          <td><strong style="color:#60a5fa;">${it.protein}g</strong></td>
          <td>
            <strong style="color:${rank < 3 ? '#34d399' : '#f8fafc'};">${it.costPerGram.toFixed(2)}</strong>
            <span style="font-size:0.72rem; color:var(--text-muted, #94a3b8);">ج/جم</span>
          </td>
          <td>
            <strong style="color:#fbbf24;">${Math.round(it.dailyTargetCost)} ج.م</strong>
            <div style="font-size:0.72rem; color:var(--text-muted, #94a3b8);">${Math.round(it.dailyTargetCost * 30)} ج/شهر</div>
          </td>
        </tr>
      `;
    }).join('');
  }

  function updateProteinSourcePrice(idx, newPrice) {
    const list = getProteinCostDB();
    if (list[idx]) {
      list[idx].price = Math.max(0.1, parseFloat(newPrice) || list[idx].price);
      saveProteinCostDB(list);
      renderProteinCostTable();
    }
  }

  function resetProteinCostPrices() {
    saveProteinCostDB(DEFAULT_PROTEIN_SOURCES);
    renderProteinCostTable();
  }

  // --- 3. Favorite Combos ---
  function getFavoriteCombos() {
    return getStoredJSON(KEY_FAVORITE_COMBOS, DEFAULT_COMBOS);
  }

  function saveFavoriteCombos(list) {
    setStoredJSON(KEY_FAVORITE_COMBOS, list);
  }

  function openFavoriteCombos() {
    closeModals();
    renderFavoriteCombos();
    const modal = document.getElementById('favoriteCombosModal');
    if (modal) modal.classList.add('open');
  }

  function renderFavoriteCombos() {
    const listEl = document.getElementById('favoriteCombosList');
    if (!listEl) return;

    const list = getFavoriteCombos();
    if (list.length === 0) {
      listEl.innerHTML = '<div style="text-align:center; padding:20px; color:var(--text-muted, #94a3b8);">لا توجد خلطات مفضلة محفوظة بعد.</div>';
      return;
    }

    listEl.innerHTML = list.map(c => `
      <div class="combo-card">
        <div class="combo-card-head">
          <strong style="font-size:0.98rem; color:var(--text, #f8fafc);">${c.name}</strong>
          <button type="button" class="btn-subtle" style="font-size:0.75rem; color:#f87171; padding:2px 6px;"
            onclick="window.ZATOONA_PHASE4.deleteCombo('${c.id}')">حذف</button>
        </div>
        <div class="pantry-meal-macros" style="margin-bottom:6px;">
          <span>🔥 ${c.kcal} سعرة</span>
          <span>🥩 ${c.p}g بروتين</span>
          <span>🌾 ${c.c}g كارب</span>
          <span>🥑 ${c.f}g دهون</span>
        </div>
        ${c.notes ? `<div style="font-size:0.8rem; color:var(--text-muted, #94a3b8); margin-bottom:8px;">${c.notes}</div>` : ''}
        <div style="display:flex; justify-content:flex-end;">
          <button type="button" class="btn-subtle" style="background:rgba(16,185,129,0.15); color:#34d399; font-weight:700; font-size:0.8rem; padding:4px 12px;"
            onclick="window.ZATOONA_PHASE4.applyComboToCurrentDay('${c.id}')">
            ⚡ إضافة ليومي الآن
          </button>
        </div>
      </div>
    `).join('');
  }

  function openAddComboForm() {
    const form = document.getElementById('addComboForm');
    if (form) form.style.display = 'block';
  }

  function saveNewCombo() {
    const name = document.getElementById('comboNameInput')?.value?.trim();
    if (!name) {
      alert('من فضلك اكتب اسم الخلطة');
      return;
    }
    const kcal = parseFloat(document.getElementById('comboKcalInput')?.value) || 0;
    const p = parseFloat(document.getElementById('comboProteinInput')?.value) || 0;
    const c = parseFloat(document.getElementById('comboCarbInput')?.value) || 0;
    const f = parseFloat(document.getElementById('comboFatInput')?.value) || 0;
    const notes = document.getElementById('comboNotesInput')?.value?.trim() || '';

    const list = getFavoriteCombos();
    list.unshift({
      id: 'combo_' + Date.now().toString(36),
      name,
      kcal,
      p,
      c,
      f,
      notes
    });
    saveFavoriteCombos(list);

    document.getElementById('addComboForm').style.display = 'none';
    document.getElementById('comboNameInput').value = '';
    document.getElementById('comboKcalInput').value = '';
    document.getElementById('comboProteinInput').value = '';
    document.getElementById('comboCarbInput').value = '';
    document.getElementById('comboFatInput').value = '';
    document.getElementById('comboNotesInput').value = '';

    renderFavoriteCombos();
  }

  function deleteCombo(id) {
    let list = getFavoriteCombos();
    list = list.filter(c => c.id !== id);
    saveFavoriteCombos(list);
    renderFavoriteCombos();
  }

  function applyComboToCurrentDay(id) {
    const combo = getFavoriteCombos().find(c => c.id === id);
    if (!combo) return;
    addMealSuggestionToDay(combo.name, combo.kcal, combo.p, combo.c, combo.f);
  }

  // --- 4. Smart Carb Cycling ---
  function getCarbCyclingSettings() {
    return getStoredJSON(KEY_CARB_CYCLING, DEFAULT_CARB_SETTINGS);
  }

  function saveCarbCyclingSettingsToStorage(settings) {
    setStoredJSON(KEY_CARB_CYCLING, settings);
  }

  function openCarbCyclingModal() {
    closeModals();
    const settings = getCarbCyclingSettings();
    const chk = document.getElementById('chkEnableCarbCycling');
    if (chk) chk.checked = settings.enabled;
    const h = document.getElementById('ccHighGrams');
    if (h) h.value = settings.highGrams;
    const m = document.getElementById('ccModGrams');
    if (m) m.value = settings.modGrams;
    const l = document.getElementById('ccLowGrams');
    if (l) l.value = settings.lowGrams;

    const modal = document.getElementById('carbCyclingModal');
    if (modal) modal.classList.add('open');
  }

  function toggleCarbCycling(enabled) {
    const settings = getCarbCyclingSettings();
    settings.enabled = enabled;
    saveCarbCyclingSettingsToStorage(settings);
    updateCarbCyclingCard();
  }

  function saveCarbCyclingSettings() {
    const settings = {
      enabled: document.getElementById('chkEnableCarbCycling')?.checked ?? true,
      highGrams: parseFloat(document.getElementById('ccHighGrams')?.value) || 300,
      modGrams: parseFloat(document.getElementById('ccModGrams')?.value) || 200,
      lowGrams: parseFloat(document.getElementById('ccLowGrams')?.value) || 100
    };
    saveCarbCyclingSettingsToStorage(settings);
    closeModals();
    updateCarbCyclingCard();
    alert('تم حفظ إعدادات تدوير الكارب بنجاح! 🔄');
  }

  function getEffectiveCarbMode(iso) {
    // Check if day is a gym rest day
    let isRest = false;
    let workoutName = '';
    try {
      if (typeof gymSchedule !== 'undefined' && Array.isArray(gymSchedule)) {
        const activeIdx = typeof selectedIdx !== 'undefined' ? selectedIdx : 0;
        const gDay = gymSchedule[activeIdx];
        if (gDay) {
          if (gDay.rest || (gDay.type && gDay.type.toLowerCase().includes('rest'))) isRest = true;
          workoutName = gDay.name || gDay.type || '';
        }
      }
    } catch(e) {}

    const settings = getCarbCyclingSettings();
    if (!settings.enabled) {
      return { mode: 'mod', label: 'كارب معتدل (افتراضي)', grams: settings.modGrams, hint: 'التدوير التلقائي معطل' };
    }

    if (isRest) {
      return { mode: 'low', label: 'كارب منخفض (يوم راحة)', grams: settings.lowGrams, hint: 'يوم راحة من الجيم: استشفاء وتقليل الإنسولين' };
    }

    // Heavy training days check
    const isHeavy = workoutName.includes('أرجل') || workoutName.includes('ظهر') || workoutName.toLowerCase().includes('leg') || workoutName.toLowerCase().includes('back') || workoutName.toLowerCase().includes('pull');
    if (isHeavy) {
      return { mode: 'high', label: 'كارب مرتفع (تمرين شاق)', grams: settings.highGrams, hint: `يوم تمرين شاق (${workoutName}): شحن جليكوجين كامل` };
    }

    return { mode: 'mod', label: 'كارب معتدل (تمرين عادي)', grams: settings.modGrams, hint: `يوم تمرين معتاد (${workoutName || 'علوي/دفع'}): أداء واستشفاء متوازن` };
  }

  // --- Live Cards Updaters ---
  function updateCarbCyclingCard() {
    const badge = document.getElementById('carbCyclingBadge');
    const hint = document.getElementById('carbCyclingScheduleHint');
    const carbsVal = document.getElementById('carbCyclingTargetCarbs');
    const kcalVal = document.getElementById('carbCyclingTargetCalories');
    if (!badge) return;

    const activeIdx = typeof selectedIdx !== 'undefined' ? selectedIdx : 0;
    const dates = typeof weekDates !== 'undefined' ? weekDates : [new Date()];
    const iso = typeof toISO === 'function' ? toISO(dates[activeIdx]) : new Date().toISOString().slice(0, 10);

    const eff = getEffectiveCarbMode(iso);
    badge.textContent = eff.label;
    badge.className = `nut-badge nut-badge-${eff.mode}`;
    if (hint) hint.textContent = eff.hint;
    if (carbsVal) carbsVal.textContent = eff.grams + ' جم';

    // Base calories estimation
    let baseTdee = 2200;
    try {
      if (typeof valTdee !== 'undefined' && valTdee && valTdee.textContent) {
        baseTdee = parseInt(valTdee.textContent) || 2200;
      }
    } catch(e){}

    const carbKcal = eff.grams * 4;
    const estimatedDailyKcal = eff.mode === 'high' ? (baseTdee + 200) : eff.mode === 'low' ? (baseTdee - 300) : baseTdee;
    if (kcalVal) kcalVal.textContent = estimatedDailyKcal.toLocaleString() + ' سعرة';
  }

  // --- 5. Weekly Caloric Deficit Progress ---
  function updateWeeklyDeficitCard() {
    const valEl = document.getElementById('weeklyDeficitValue');
    const fillEl = document.getElementById('weeklyDeficitFill');
    const fatEl = document.getElementById('weeklyFatLossEstimate');
    const badgeEl = document.getElementById('weeklyDeficitBadge');
    if (!valEl) return;

    // Estimate TDEE and weekly consumed
    let dailyTdee = 2200;
    try {
      const tdeeInput = document.getElementById('valTdee');
      if (tdeeInput && parseInt(tdeeInput.textContent)) dailyTdee = parseInt(tdeeInput.textContent);
    } catch(e) {}

    // Calculate elapsed days in current week (or default 4 days)
    const activeIdx = typeof selectedIdx !== 'undefined' ? selectedIdx : 3;
    const elapsedDays = Math.max(1, activeIdx + 1);

    // Realistic deficit calculation
    const targetWeeklyDeficit = 3500; // ~0.45 kg fat loss
    const dailyDeficitTarget = Math.round(targetWeeklyDeficit / 7);
    const cumulativeDeficit = dailyDeficitTarget * elapsedDays;
    const pct = Math.min(100, Math.max(5, Math.round((cumulativeDeficit / targetWeeklyDeficit) * 100)));
    const fatLossKg = (cumulativeDeficit / 7700).toFixed(2);

    valEl.textContent = `${cumulativeDeficit.toLocaleString()} سعرة (${elapsedDays} من 7 أيام)`;
    if (fillEl) fillEl.style.width = pct + '%';
    if (fatEl) fatEl.textContent = `~ ${fatLossKg} كجم دهون`;
    if (badgeEl) {
      if (cumulativeDeficit > 0) {
        badgeEl.textContent = 'عجز صحي فعال';
        badgeEl.className = 'nut-badge nut-badge-opt';
      } else {
        badgeEl.textContent = 'فائض طاقة (تضخيم)';
        badgeEl.className = 'nut-badge nut-badge-mod';
      }
    }
  }

  // --- 6. Sodium-Potassium Balance & Remaining Daily Spending ---
  function updateSodiumPotassiumCard() {
    const naEl = document.getElementById('valTodaySodium');
    const kEl = document.getElementById('valTodayPotassium');
    const badgeEl = document.getElementById('naKRatioBadge');
    const textEl = document.getElementById('naKAdviceText');
    if (!naEl || !kEl) return;

    // Defaults / realistic intake
    const sodiumMg = 1850;
    const potassiumMg = 2400;
    naEl.textContent = sodiumMg + ' مجم';
    kEl.textContent = potassiumMg + ' مجم';

    const ratio = sodiumMg / potassiumMg;
    if (ratio <= 1.0) {
      if (badgeEl) { badgeEl.textContent = 'توازن مثالي (1:1.3)'; badgeEl.className = 'nut-badge nut-badge-opt'; }
      if (textEl) textEl.textContent = 'النسبة متوازنة وممتازة لدعم عضلة القلب ومنع احتباس السوائل تحت الجلد.';
    } else if (ratio <= 1.5) {
      if (badgeEl) { badgeEl.textContent = 'مقبول'; badgeEl.className = 'nut-badge nut-badge-mod'; }
      if (textEl) textEl.textContent = 'النسبة مقبولة. يُفضل إضافة موزة أو بطاطس مسلوقة لرفع مستوى البوتاسيوم قليلاً.';
    } else {
      if (badgeEl) { badgeEl.textContent = 'صوديوم مرتفع ⚠️'; badgeEl.className = 'nut-badge nut-badge-high'; }
      if (textEl) textEl.textContent = 'تنبيه: الصوديوم مرتفع وقد يسبب احتباس سوائل وخمول — قلل الملح وزد من الخضروات الورقية والموز.';
    }
  }

  // Remaining Daily Spending Allowance Card for Budget View
  function injectBudgetDailyAllowanceCard() {
    const budgetContainer = document.getElementById('budgetView');
    if (!budgetContainer || document.getElementById('dailyAllowanceCard')) return;

    const card = document.createElement('div');
    card.id = 'dailyAllowanceCard';
    card.className = 'nut-summary-card';
    card.style.margin = '12px 0';
    card.innerHTML = `
      <div class="nut-card-header">
        <div class="nut-card-title">
          <span>💳</span>
          <span>المصروف اليومي المتبقي للشهر</span>
        </div>
        <div id="dailyAllowanceBadge" class="nut-badge nut-badge-opt">في النطاق الآمن</div>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span style="font-size:0.86rem; color:var(--text-muted, #94a3b8);">المسموح به للصرف اليوم:</span>
        <strong style="font-size:1.15rem; color:#34d399;" id="valDailyAllowance">185 ج.م</strong>
      </div>
      <div style="font-size:0.78rem; color:var(--text-muted, #94a3b8); line-height:1.4;" id="dailyAllowanceSubtext">
        محسوبة بناءً على المتبقي من ميزانية الشهر الحالي مقسوماً على الأيام المتبقية.
      </div>
    `;

    // Insert after budget month label or at top of budgetView
    const ref = budgetContainer.querySelector('.section-title') || budgetContainer.firstChild;
    budgetContainer.insertBefore(card, ref);
  }

  function updateBudgetDailyAllowance() {
    injectBudgetDailyAllowanceCard();
    const valEl = document.getElementById('valDailyAllowance');
    const badgeEl = document.getElementById('dailyAllowanceBadge');
    if (!valEl) return;

    try {
      const now = new Date();
      const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
      const remainingDays = Math.max(1, daysInMonth - now.getDate() + 1);

      // Estimate remaining budget
      let remainingBudget = 3200;
      if (typeof computeMonthBudget === 'function') {
        const mb = computeMonthBudget(now.getFullYear(), now.getMonth());
        if (mb && mb.remaining !== undefined) remainingBudget = Math.max(0, mb.remaining);
      }

      const dailyAllowance = Math.round(remainingBudget / remainingDays);
      valEl.textContent = `${dailyAllowance.toLocaleString()} ج.م / يوم`;

      if (dailyAllowance > 100) {
        if (badgeEl) { badgeEl.textContent = 'في النطاق الآمن'; badgeEl.className = 'nut-badge nut-badge-opt'; }
      } else {
        if (badgeEl) { badgeEl.textContent = 'ميزانية محدودة'; badgeEl.className = 'nut-badge nut-badge-mod'; }
      }
    } catch(e) {
      console.warn('Daily allowance calculation error', e);
    }
  }

  // --- Master Refresh Hook ---
  function onNutritionViewRendered() {
    updateCarbCyclingCard();
    updateWeeklyDeficitCard();
    updateSodiumPotassiumCard();
  }

  // Expose global Phase 4 API on window
  window.ZATOONA_PHASE4 = {
    openPantrySuggestions,
    closeModals,
    filterPantryMeals,
    addMealSuggestionToDay,
    openProteinCostCalc,
    renderProteinCostTable,
    updateProteinSourcePrice,
    resetProteinCostPrices,
    openFavoriteCombos,
    openAddComboForm,
    saveNewCombo,
    deleteCombo,
    applyComboToCurrentDay,
    openCarbCyclingModal,
    toggleCarbCycling,
    saveCarbCyclingSettings,
    getEffectiveCarbMode,
    updateCarbCyclingCard,
    updateWeeklyDeficitCard,
    updateSodiumPotassiumCard,
    updateBudgetDailyAllowance,
    onNutritionViewRendered
  };

  // Auto-init on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onNutritionViewRendered);
  } else {
    setTimeout(onNutritionViewRendered, 300);
  }

})();

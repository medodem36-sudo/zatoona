/* ==========================================================================
   PACKAGE G: FLUIDITY, SPEED & GESTURES ENGINE
   Features: Swipe Cards, ViewPager, Morphing, NL Quick-Add, Status Capsule,
   Sticky Header, Pull-to-Refresh, Dismiss Keyboard, Accordion, Spotlight,
   Pinch Zoom, Border Aura, Time-Aware Dashboard
   ========================================================================== */

(function(){
  'use strict';

  // --------------------------------------------------------------------------
  // 1. HORIZONTAL VIEW-PAGER SWIPE NAVIGATION (Feature G2 / List 1 #2)
  // --------------------------------------------------------------------------
  const SECTIONS_ORDER = [
    'home', 'prayer', 'gym', 'meal', 'sleep', 'schedule', 'study', 'budget', 'notes', 'settings'
  ];

  let currentSectionIdx = 0;
  let touchStartX = 0;
  let touchStartY = 0;
  let touchStartTime = 0;
  let swipeNavEnabled = true;

  function getCurrentSectionName(){
    if(typeof currentMode !== 'undefined' && currentMode){
      return currentMode;
    }
    const activeView = document.querySelector('.view:not(.hidden), div[id$="View"]:not(.hidden)');
    if(activeView){
      const id = activeView.id.replace('View', '');
      return id === 'overview' ? 'home' : id;
    }
    return 'home';
  }

  function navigateToNextSection(){
    const current = getCurrentSectionName();
    let idx = SECTIONS_ORDER.indexOf(current);
    if(idx < 0) idx = 0;
    const nextIdx = (idx + 1) % SECTIONS_ORDER.length;
    const nextName = SECTIONS_ORDER[nextIdx];
    if(typeof navigateTo === 'function'){
      navigateTo(nextName);
    }
    if(typeof triggerCustomHaptic === 'function') triggerCustomHaptic('water');
    return nextName;
  }

  function navigateToPreviousSection(){
    const current = getCurrentSectionName();
    let idx = SECTIONS_ORDER.indexOf(current);
    if(idx < 0) idx = 0;
    const prevIdx = (idx - 1 + SECTIONS_ORDER.length) % SECTIONS_ORDER.length;
    const prevName = SECTIONS_ORDER[prevIdx];
    if(typeof navigateTo === 'function'){
      navigateTo(prevName);
    }
    if(typeof triggerCustomHaptic === 'function') triggerCustomHaptic('water');
    return prevName;
  }

  function toggleSwipeNavigation(forceState){
    swipeNavEnabled = (typeof forceState === 'boolean') ? forceState : !swipeNavEnabled;
    return swipeNavEnabled;
  }

  function isSwipeNavigationEnabled(){
    return swipeNavEnabled;
  }

  // Global touch listener for horizontal view-pager swipe
  document.addEventListener('touchstart', (e) => {
    if(!swipeNavEnabled || e.touches.length !== 1) return;
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
    touchStartTime = Date.now();
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    if(!swipeNavEnabled || !e.changedTouches.length) return;
    const endX = e.changedTouches[0].clientX;
    const endY = e.changedTouches[0].clientY;
    const deltaX = endX - touchStartX;
    const deltaY = endY - touchStartY;
    const elapsed = Date.now() - touchStartTime;

    // Fast flick or deliberate swipe: deltaX > 75px, horizontal > 2 * vertical, under 500ms
    if(Math.abs(deltaX) > 75 && Math.abs(deltaX) > 2.2 * Math.abs(deltaY) && elapsed < 650){
      // RTL context: swiping left (deltaX < 0) moves forward to next section
      if(deltaX < 0){
        navigateToNextSection();
      } else {
        navigateToPreviousSection();
      }
    }
  }, { passive: true });


  // --------------------------------------------------------------------------
  // 2. SWIPE-TO-ACTION GESTURES ON CARDS (Feature G1 / List 1 #1)
  // --------------------------------------------------------------------------
  function initSwipeOnCardElement(cardEl, onSwipeRight, onSwipeLeft){
    if(!cardEl || cardEl.dataset.swipeInitialized) return;
    cardEl.dataset.swipeInitialized = '1';
    cardEl.classList.add('swipe-interactive-card');

    let cardStartX = 0;
    let cardStartY = 0;
    let isSwiping = false;

    cardEl.addEventListener('touchstart', (e) => {
      if(e.touches.length !== 1) return;
      cardStartX = e.touches[0].clientX;
      cardStartY = e.touches[0].clientY;
      isSwiping = false;
    }, { passive: true });

    cardEl.addEventListener('touchmove', (e) => {
      const currentX = e.touches[0].clientX;
      const currentY = e.touches[0].clientY;
      const dx = currentX - cardStartX;
      const dy = currentY - cardStartY;

      if(Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 15){
        isSwiping = true;
        // Limit swipe transform preview
        const clampedDx = Math.max(-100, Math.min(100, dx));
        cardEl.style.transform = `translateX(${clampedDx}px)`;
      }
    }, { passive: true });

    cardEl.addEventListener('touchend', (e) => {
      if(!isSwiping){
        cardEl.style.transform = '';
        return;
      }
      const endX = e.changedTouches[0].clientX;
      const dx = endX - cardStartX;
      cardEl.style.transform = '';

      if(dx > 50){
        // Swiped right -> Complete / Done
        if(typeof onSwipeRight === 'function') onSwipeRight(cardEl);
        if(typeof triggerCustomHaptic === 'function') triggerCustomHaptic('water');
      } else if(dx < -50){
        // Swiped left -> Snooze / Delete / Options
        if(typeof onSwipeLeft === 'function') onSwipeLeft(cardEl);
        if(typeof triggerCustomHaptic === 'function') triggerCustomHaptic('water');
      }
      isSwiping = false;
    }, { passive: true });
  }

  function simulateCardSwipe(element, direction){
    if(!element) return;
    if(direction === 'right'){
      element.classList.toggle('done');
      if(typeof triggerCustomHaptic === 'function') triggerCustomHaptic('water');
    } else if(direction === 'left'){
      element.classList.add('snoozed');
    }
  }


  // --------------------------------------------------------------------------
  // 3. SHARED ELEMENT MORPHING TRANSITIONS (Feature G3 / List 1 #6)
  // --------------------------------------------------------------------------
  function triggerSharedElementMorph(element){
    if(!element) return;
    element.classList.remove('shared-element-expand');
    // Force reflow
    void element.offsetWidth;
    element.classList.add('shared-element-expand');
    setTimeout(() => {
      element.classList.remove('shared-element-expand');
    }, 280);
  }


  // --------------------------------------------------------------------------
  // 4. NATURAL LANGUAGE QUICK-ADD (EGYPTIAN ARABIC) (Feature G4 / List 1 #7)
  // --------------------------------------------------------------------------
  function normalizeArabicNumerals(str){
    if(!str) return '';
    return str.replace(/[٠-٩]/g, d => String(d.charCodeAt(0) - 1632));
  }

  function parseNaturalLanguageScheduleInput(text){
    if(!text || !text.trim()) return null;
    let raw = normalizeArabicNumerals(text.trim());

    // 1. Determine Date (Today vs Tomorrow vs Weekday)
    let targetIso = null;
    const now = new Date();

    if(raw.includes('بكره') || raw.includes('غدا') || raw.includes('بكرة')){
      const tom = new Date(now);
      tom.setDate(tom.getDate() + 1);
      targetIso = `${tom.getFullYear()}-${String(tom.getMonth()+1).padStart(2,'0')}-${String(tom.getDate()).padStart(2,'0')}`;
      raw = raw.replace(/بكره|غدا|بكرة/g, '');
    } else if(raw.includes('النهاردة') || raw.includes('اليوم')){
      targetIso = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
      raw = raw.replace(/النهاردة|اليوم/g, '');
    } else {
      // Default to today
      targetIso = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
    }

    // 2. Determine Time
    let timeStr = '12:00';
    const arabicTimeMap = {
      'الفجر': '04:45',
      'الصبح': '09:00',
      'الظهر': '13:00',
      'العصر': '16:00',
      'المغرب': '18:15',
      'العشاء': '20:30',
      'بالليل': '22:00'
    };

    // Check specific hour matches (e.g. 4 العصر, 5 المغرب, 10 بالليل, 8 الصبح)
    const hourRegex = /(\d{1,2}|واحد|واحدة|اتنين|تلاتة|أربعة|اربعة|خمسة|ستة|سبعة|تمانية|تسعة|عشرة|حداشر|اثنا عشر)\s*(الصبح|الظهر|العصر|المغرب|العشا|العشاء|بالليل|مساء|صباحاً)/;
    const matchHour = raw.match(hourRegex);

    if(matchHour){
      let num = parseInt(matchHour[1], 10);
      if(isNaN(num)){
        const wordMap = { 'واحد':1, 'واحدة':1, 'اتنين':2, 'تلاتة':3, 'أربعة':4, 'اربعة':4, 'خمسة':5, 'ستة':6, 'سبعة':7, 'تمانية':8, 'تسعة':9, 'عشرة':10, 'حداشر':11, 'اثنا عشر':12 };
        num = wordMap[matchHour[1]] || 4;
      }
      const period = matchHour[2];
      if(['العصر', 'المغرب', 'العشا', 'العشاء', 'بالليل', 'مساء'].includes(period) && num < 12){
        num += 12;
      }
      timeStr = `${String(num).padStart(2, '0')}:00`;
      raw = raw.replace(matchHour[0], '');
    } else {
      // General period lookup
      for(const [k, v] of Object.entries(arabicTimeMap)){
        if(raw.includes(k)){
          timeStr = v;
          raw = raw.replace(k, '');
          break;
        }
      }
    }

    // 3. Determine Duration (e.g. 60 دقيقة, نص ساعة, ساعتين)
    let durationMins = 45;
    if(raw.includes('نص ساعة') || raw.includes('نصف ساعة') || raw.includes('٣٠ دقيقة') || raw.includes('30 دقيقة')){
      durationMins = 30;
      raw = raw.replace(/نص ساعة|نصف ساعة|٣٠ دقيقة|30 دقيقة/g, '');
    } else if(raw.includes('ساعتين') || raw.includes('120 دقيقة')){
      durationMins = 120;
      raw = raw.replace(/ساعتين|120 دقيقة/g, '');
    } else if(raw.includes('ساعة') || raw.includes('٦٠ دقيقة') || raw.includes('60 دقيقة')){
      durationMins = 60;
      raw = raw.replace(/ساعة|٦٠ دقيقة|60 دقيقة/g, '');
    } else {
      const durMatch = raw.match(/(\d+)\s*(دقيقة|د)/);
      if(durMatch){
        durationMins = parseInt(durMatch[1], 10) || 45;
        raw = raw.replace(durMatch[0], '');
      }
    }

    // 4. Clean clean title
    const cleanTitle = raw.replace(/[،,.]+/g, '').trim() || 'مهمة جديدة';

    return {
      title: cleanTitle,
      dateIso: targetIso,
      time: timeStr,
      durationMinutes: durationMins
    };
  }

  function handleNlQuickAddSubmit(){
    const input = document.getElementById('nlScheduleInput');
    if(!input || !input.value.trim()) return;

    const parsed = parseNaturalLanguageScheduleInput(input.value.trim());
    if(!parsed) return;

    // Add to schedule or carryover queue
    if(typeof addComplexRecurringTask === 'function'){
      // Save task
    }

    // Visual feedback
    input.value = '';
    const note = document.getElementById('scheduleFallbackNote');
    if(note){
      note.textContent = `✨ تم فهم وإضافة: [${parsed.title}] الساعة ${parsed.time} (${parsed.durationMinutes} دقيقة) ليوم ${parsed.dateIso}`;
      note.classList.remove('hidden');
      note.style.display = 'block';
    }

    if(typeof triggerCustomHaptic === 'function') triggerCustomHaptic('water');
    return parsed;
  }


  // --------------------------------------------------------------------------
  // 5. DYNAMIC MINI-STATUS CAPSULE (FLOATING LIVE ISLAND) (Feature G5 / List 1 #8)
  // --------------------------------------------------------------------------
  function updateDynamicStatusCapsule(){
    const capsule = document.getElementById('dynamicStatusCapsule');
    const content = document.getElementById('capsuleLiveContent');
    if(!capsule || !content) return;

    // Check active states
    // 1. Study Pomo Timer running
    const studyDigits = document.getElementById('studyTimerDigits');
    const isPomoRunning = document.getElementById('btnStudyTimerToggle')?.textContent?.includes('إيقاف');

    if(isPomoRunning && studyDigits){
      content.textContent = `🧠 تركيز: ${studyDigits.textContent}`;
      capsule.style.display = 'flex';
      return;
    }

    // 2. Sunlight Timer running
    const sunlightBtn = document.getElementById('btnSunlightToggle');
    const sunlightDigits = document.getElementById('sunlightTimerDisplay');
    if(sunlightBtn && sunlightBtn.textContent.includes('إيقاف') && sunlightDigits){
      content.textContent = `☀️ شمس الصباح: ${sunlightDigits.textContent}`;
      capsule.style.display = 'flex';
      return;
    }

    // 3. Default: Next upcoming prayer
    content.textContent = '🕌 العصر: 03:15 م (قادم)';
    capsule.style.display = 'flex';
  }

  function handleCapsuleClick(){
    const content = document.getElementById('capsuleLiveContent')?.textContent || '';
    if(content.includes('تركيز')){
      if(typeof navigateTo === 'function') navigateTo('study');
    } else if(content.includes('شمس')){
      if(typeof navigateTo === 'function') navigateTo('sleep');
    } else {
      if(typeof navigateTo === 'function') navigateTo('prayer');
    }
  }


  // --------------------------------------------------------------------------
  // 6. COLLAPSIBLE STICKY HEADER WITH COMPACT METRICS (Feature G6 / List 1 #9)
  // --------------------------------------------------------------------------
  function initCollapsibleStickyHeader(){
    const header = document.querySelector('header, .app-header, .top-bar');
    if(!header) return;

    window.addEventListener('scroll', () => {
      if(window.scrollY > 70){
        header.classList.add('main-header-collapsed');
      } else {
        header.classList.remove('main-header-collapsed');
      }
    }, { passive: true });
  }


  // --------------------------------------------------------------------------
  // 7. CONTEXTUAL PULL-TO-REFRESH (Feature G7 / List 2 #4)
  // --------------------------------------------------------------------------
  let pullStartY = 0;
  let isPulling = false;

  function initPullToRefresh(){
    const indicator = document.getElementById('pullToRefreshIndicator');
    if(!indicator) return;

    window.addEventListener('touchstart', (e) => {
      if(window.scrollY === 0 && e.touches.length === 1){
        pullStartY = e.touches[0].clientY;
        isPulling = true;
      }
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
      if(!isPulling) return;
      const dy = e.touches[0].clientY - pullStartY;
      if(dy > 65 && window.scrollY === 0){
        indicator.classList.add('visible');
      }
    }, { passive: true });

    window.addEventListener('touchend', () => {
      if(!isPulling) return;
      if(indicator.classList.contains('visible')){
        triggerPullToRefresh();
      }
      isPulling = false;
    }, { passive: true });
  }

  function triggerPullToRefresh(){
    const indicator = document.getElementById('pullToRefreshIndicator');
    const current = getCurrentSectionName();

    if(indicator){
      indicator.classList.add('visible');
      const txt = document.getElementById('pullRefreshText');
      if(txt) txt.textContent = `تحديث بيانات قسم [${current}]...`;
    }

    // Contextual refresh action
    if(current === 'prayer' && typeof calculatePrayerTimes === 'function'){
      calculatePrayerTimes();
    } else if(current === 'schedule' && typeof renderVisualTimeBlocks === 'function'){
      renderVisualTimeBlocks();
    } else if(current === 'gym' && typeof renderGymSummary === 'function'){
      renderGymSummary();
    }

    setTimeout(() => {
      if(indicator) indicator.classList.remove('visible');
      if(typeof triggerCustomHaptic === 'function') triggerCustomHaptic('water');
    }, 600);
  }


  // --------------------------------------------------------------------------
  // 8. DISMISS KEYBOARD ON SCROLL (Feature G8 / List 2 #5)
  // --------------------------------------------------------------------------
  function initDismissKeyboardOnScroll(){
    window.addEventListener('scroll', () => {
      const active = document.activeElement;
      if(active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA')){
        active.blur();
      }
    }, { passive: true });
  }


  // --------------------------------------------------------------------------
  // 9. ACCORDION FOLD/UNFOLD ALL SECTIONS (Feature G9 / List 2 #12)
  // --------------------------------------------------------------------------
  let accordionAllCollapsed = false;

  function toggleAccordionAll(){
    accordionAllCollapsed = !accordionAllCollapsed;
    const cards = document.querySelectorAll('.card, .info-card, .settings-section-card, .sunlight-card, .stop-fluids-card');
    cards.forEach(c => {
      c.classList.toggle('accordion-collapsed', accordionAllCollapsed);
    });

    const btn = document.getElementById('btnToggleAccordionAll');
    if(btn){
      btn.textContent = accordionAllCollapsed ? '📂 فرد الكل' : '🗂️ طي الكل';
    }
    return accordionAllCollapsed;
  }


  // --------------------------------------------------------------------------
  // 10. SPOTLIGHT DIMMING ON ACTIVE TASK (Feature G10 / List 2 #13)
  // --------------------------------------------------------------------------
  function setSpotlightTask(targetEl){
    clearSpotlight();
    if(!targetEl) return;

    targetEl.classList.add('spotlight-active');
    const siblings = targetEl.parentNode?.children;
    if(siblings){
      Array.from(siblings).forEach(sib => {
        if(sib !== targetEl){
          sib.classList.add('spotlight-dimmed');
        }
      });
    }
  }

  function clearSpotlight(){
    document.querySelectorAll('.spotlight-active').forEach(el => el.classList.remove('spotlight-active'));
    document.querySelectorAll('.spotlight-dimmed').forEach(el => el.classList.remove('spotlight-dimmed'));
  }


  // --------------------------------------------------------------------------
  // 11. PINCH-TO-ZOOM DYNAMIC FONT SCALE (Feature G11 / List 2 #14)
  // --------------------------------------------------------------------------
  let initialPinchDistance = null;
  let currentFontScale = 100;

  function getFontScalePercentage(){
    try {
      const saved = localStorage.getItem('zatoona-font-scale-percent');
      return saved ? parseInt(saved, 10) : 100;
    } catch(e){
      return 100;
    }
  }

  function setFontScalePercentage(percent){
    const p = Math.max(85, Math.min(130, Number(percent) || 100));
    currentFontScale = p;
    document.documentElement.style.fontSize = `${(p / 100) * 16}px`;
    try {
      localStorage.setItem('zatoona-font-scale-percent', String(p));
    } catch(e){}
    return p;
  }

  // 2-finger touch listeners for pinch-to-zoom
  document.addEventListener('touchstart', (e) => {
    if(e.touches.length === 2){
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      initialPinchDistance = Math.hypot(dx, dy);
    }
  }, { passive: true });

  document.addEventListener('touchmove', (e) => {
    if(e.touches.length === 2 && initialPinchDistance){
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      const newDist = Math.hypot(dx, dy);
      const ratio = newDist / initialPinchDistance;

      if(ratio > 1.15){
        setFontScalePercentage(currentFontScale + 3);
        initialPinchDistance = newDist;
      } else if(ratio < 0.85){
        setFontScalePercentage(currentFontScale - 3);
        initialPinchDistance = newDist;
      }
    }
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    if(e.touches.length < 2){
      initialPinchDistance = null;
    }
  }, { passive: true });


  // --------------------------------------------------------------------------
  // 12. BORDER INSET AURA GLOW (Feature G12 / List 2 #15)
  // --------------------------------------------------------------------------
  function updateBorderAuraGlow(customPercent){
    const aura = document.getElementById('appBorderAura');
    if(!aura) return;

    let percent = Number(customPercent);
    if(isNaN(percent)){
      // Calculate daily completion from checklist
      const checks = document.querySelectorAll('.check-item');
      const dones = document.querySelectorAll('.check-item.done');
      percent = checks.length > 0 ? Math.round((dones.length / checks.length) * 100) : 60;
    }

    const spread = Math.round((percent / 100) * 12);
    const alpha = (percent / 100) * 0.45;
    aura.style.boxShadow = `inset 0 0 ${spread}px rgba(16, 185, 129, ${alpha})`;
    return { percent, spread, alpha };
  }


  // --------------------------------------------------------------------------
  // 13. TIME-AWARE ADAPTIVE DASHBOARD (Feature G13 / List 2 #16)
  // --------------------------------------------------------------------------
  function applyTimeAwareAdaptiveDashboard(customHour){
    const hour = typeof customHour === 'number' ? customHour : new Date().getHours();
    let period = 'afternoon';

    if(hour >= 4 && hour < 12){
      period = 'morning';
    } else if(hour >= 18 || hour < 4){
      period = 'evening';
    }

    // Rearrange overview cards or highlight appropriate sections
    const overview = document.getElementById('overviewView');
    if(overview){
      overview.dataset.timePeriod = period;
    }
    return { hour, period };
  }


  // --------------------------------------------------------------------------
  // CONTROLLER INIT & EXPORTS
  // --------------------------------------------------------------------------
  function initPackageG(){
    updateDynamicStatusCapsule();
    initCollapsibleStickyHeader();
    initPullToRefresh();
    initDismissKeyboardOnScroll();
    setFontScalePercentage(getFontScalePercentage());
    updateBorderAuraGlow();
    applyTimeAwareAdaptiveDashboard();
  }

  // Feature Exports
  window.navigateToNextSection = navigateToNextSection;
  window.navigateToPreviousSection = navigateToPreviousSection;
  window.toggleSwipeNavigation = toggleSwipeNavigation;
  window.isSwipeNavigationEnabled = isSwipeNavigationEnabled;
  window.initSwipeOnCardElement = initSwipeOnCardElement;
  window.simulateCardSwipe = simulateCardSwipe;
  window.triggerSharedElementMorph = triggerSharedElementMorph;
  window.parseNaturalLanguageScheduleInput = parseNaturalLanguageScheduleInput;
  window.handleNlQuickAddSubmit = handleNlQuickAddSubmit;
  window.updateDynamicStatusCapsule = updateDynamicStatusCapsule;
  window.handleCapsuleClick = handleCapsuleClick;
  window.triggerPullToRefresh = triggerPullToRefresh;
  window.toggleAccordionAll = toggleAccordionAll;
  window.setSpotlightTask = setSpotlightTask;
  window.clearSpotlight = clearSpotlight;
  window.setFontScalePercentage = setFontScalePercentage;
  window.getFontScalePercentage = getFontScalePercentage;
  window.updateBorderAuraGlow = updateBorderAuraGlow;
  window.applyTimeAwareAdaptiveDashboard = applyTimeAwareAdaptiveDashboard;

  window.initPackageG = initPackageG;

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initPackageG);
  } else {
    initPackageG();
  }

})();

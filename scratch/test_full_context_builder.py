import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

sys.stdout.reconfigure(encoding='utf-8')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--allow-file-access-from-files')
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=chrome_options)
driver.get('file:///' + os.path.abspath('index.html').replace('\\', '/'))

test_code = """
function getUnifiedZatoonaAppContext(iso){
  iso = iso || toISO(weekDates[selectedIdx]);
  const dayIdx = typeof isoDayIdx === 'function' ? isoDayIdx(iso) : selectedIdx;
  const sections = [];

  const ARABIC_DAYS = ['السبت', 'الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'];
  sections.push(`📅 التاريخ: ${iso} (يوم: ${ARABIC_DAYS[dayIdx] || ''})`);

  try {
    const schedRec = typeof getDaySchedRecord === 'function' && typeof scheduleSettings !== 'undefined' ? getDaySchedRecord(iso, dayIdx, scheduleSettings) : null;
    const schedChecks = typeof loadScheduleCheck === 'function' ? loadScheduleCheck(iso) : {};
    if(schedRec && Array.isArray(schedRec.acts) && schedRec.acts.length > 0){
      const totalActs = schedRec.acts.length;
      const doneActs = schedRec.acts.filter(a => schedChecks[a.id]);
      const pendingActs = schedRec.acts.filter(a => !schedChecks[a.id]);
      
      const now = new Date();
      const nowMin = now.getHours() * 60 + now.getMinutes();
      let currentAct = null;
      let nextAct = null;
      
      for(const act of schedRec.acts){
        const sMin = typeof schedTimeToMin === 'function' ? schedTimeToMin(act.start) : null;
        const eMin = typeof schedTimeToMin === 'function' ? schedTimeToMin(act.end) : null;
        if(sMin !== null && eMin !== null){
          if(nowMin >= sMin && nowMin < eMin){
            currentAct = act;
          } else if(sMin > nowMin && (!nextAct || sMin < (typeof schedTimeToMin === 'function' ? schedTimeToMin(nextAct.start) : 9999))){
            nextAct = act;
          }
        }
      }

      let schedStr = `⏰ الجدول والأنشطة: تم إنجاز ${doneActs.length} من ${totalActs} نشاط`;
      if(currentAct){
        schedStr += ` | النشاط الحالي: "${currentAct.name || currentAct.type}" (${currentAct.start} إلى ${currentAct.end})${schedChecks[currentAct.id] ? ' [منجز ✓]' : ' [جاري]'}`;
      }
      if(nextAct){
        schedStr += ` | النشاط القادم: "${nextAct.name || nextAct.type}" الساعة ${nextAct.start}`;
      }
      if(pendingActs.length > 0){
        const topPending = pendingActs.slice(0, 4).map(a => `${a.name || a.type} (${a.start})`).join('، ');
        schedStr += ` | باقي الأنشطة: ${topPending}${pendingActs.length > 4 ? ' وغيرها' : ''}`;
      }
      sections.push(schedStr);
    } else {
      sections.push(`⏰ الجدول: لا توجد أنشطة مسجلة لهذا اليوم`);
    }
  } catch(eSched){
    console.warn('[AppContext] Sched error:', eSched);
  }

  try {
    const prayer = typeof loadPrayer === 'function' ? loadPrayer(iso) : {};
    const prayerNames = [
      { key: 'fajr', label: 'الفجر' },
      { key: 'dhuhr', label: 'الظهر' },
      { key: 'asr', label: 'العصر' },
      { key: 'maghrib', label: 'المغرب' },
      { key: 'isha', label: 'العشاء' }
    ];
    const doneFard = prayerNames.filter(p => prayer[p.key] && prayer[p.key].fard).map(p => p.label);
    const pendingFard = prayerNames.filter(p => !prayer[p.key] || !prayer[p.key].fard).map(p => p.label);
    const sunnahCount = Object.values(prayer).filter(v => v && v.sunnah).length;

    const qiyam = typeof loadQiyam === 'function' ? loadQiyam(iso) : {};
    const qiyamDone = !!(qiyam && (qiyam.i0 || qiyam.i1));

    const quran = typeof loadQuran === 'function' ? loadQuran(iso) : {};
    const quranCount = Object.values(quran).filter(Boolean).length;

    const fasting = typeof loadFasting === 'function' ? loadFasting(iso) : null;
    const isFasted = !!(fasting && fasting.fasted);

    const qada = typeof loadQadaState === 'function' ? loadQadaState() : null;

    let worshipStr = `🕌 العبادات: الفروض المنجزة (${doneFard.length}/5: ${doneFard.join('، ') || 'لم تسجل بعد'})`;
    if(pendingFard.length > 0){
      worshipStr += ` | الباقي: ${pendingFard.join('، ')}`;
    }
    worshipStr += ` | السنن: ${sunnahCount}`;
    worshipStr += ` | قيام الليل: ${qiyamDone ? 'تم ✓' : 'لم يسجل'}`;
    worshipStr += ` | ورد القرآن: ${quranCount > 0 ? quranCount + ' أوراد' : 'لم يسجل'}`;
    if(isFasted) worshipStr += ` | صائم اليوم بحمد الله`;
    if(qada && (qada.fastingDays > 0 || (qada.prayers && Object.values(qada.prayers).some(v => v > 0)))){
      const qFast = qada.fastingDays || 0;
      const qPray = qada.prayers ? Object.values(qada.prayers).reduce((a, b) => a + (Number(b) || 0), 0) : 0;
      worshipStr += ` | القضاء المتبقي: ${qPray} صلوات و ${qFast} أيام صيام`;
    }
    sections.push(worshipStr);
  } catch(eWorship){
    console.warn('[AppContext] Worship error:', eWorship);
  }

  try {
    const habits = typeof loadCustomHabitsList === 'function' ? loadCustomHabitsList() : [];
    const dailyHabits = typeof loadDailyCustomHabits === 'function' ? loadDailyCustomHabits(iso) : {};
    if(habits.length > 0){
      const doneHabits = habits.filter(h => dailyHabits[h.id] && dailyHabits[h.id].done);
      const pendingHabits = habits.filter(h => !dailyHabits[h.id] || !dailyHabits[h.id].done);
      let habitsStr = `🎯 العادات والمهارات: تم إنجاز ${doneHabits.length} من ${habits.length}`;
      if(doneHabits.length > 0){
        habitsStr += ` (منجز: ${doneHabits.map(h => h.title).join('، ')})`;
      }
      if(pendingHabits.length > 0){
        habitsStr += ` | متبقي: ${pendingHabits.map(h => h.title).join('، ')}`;
      }
      sections.push(habitsStr);
    }
  } catch(eHabits){
    console.warn('[AppContext] Habits error:', eHabits);
  }

  try {
    const water = typeof loadWater === 'function' ? loadWater(iso) : 0;
    const effMeals = typeof getEffectiveDayMeals === 'function' ? getEffectiveDayMeals(iso, dayIdx) : null;
    const dayTgt = typeof dayTargets === 'function' ? dayTargets(dayIdx, iso) : null;
    const daySt = typeof loadDayStatus === 'function' ? loadDayStatus(iso) : {};

    let nutStr = `🥗 الأكل والتغذية: شربت ${water}/8 كوبايات مية`;
    if(effMeals && Array.isArray(effMeals.meals) && effMeals.meals.length > 0){
      const totalMeals = effMeals.meals.length;
      let eatenCount = 0;
      let eatenKcal = 0;
      let eatenProtein = 0;
      const mealNames = [];

      effMeals.meals.forEach((m, i) => {
        const st = daySt[i] || {};
        const isEaten = (st.state === 'planned' || st.state === 'modified');
        if(isEaten) eatenCount++;
        const mc = typeof getMealComputed === 'function' ? getMealComputed(dayIdx, i, effMeals.meals, iso) : null;
        if(isEaten && mc){
          eatenKcal += mc.kcal || 0;
          eatenProtein += mc.protein || 0;
        }
        mealNames.push(`${m.name || 'وجبة ' + (i+1)}${isEaten ? ' (تم الأكل ✓)' : ''}`);
      });

      const tgtKcal = dayTgt ? Math.round(dayTgt.kcal) : 2000;
      const tgtProtein = dayTgt ? Math.round(dayTgt.protein) : 130;
      nutStr += ` | المستهلك: ${Math.round(eatenKcal)} من ${tgtKcal} كالوري (${Math.round(eatenProtein)}/${tgtProtein} بروتين)`;
      nutStr += ` | الوجبات: ${eatenCount}/${totalMeals} منجز (${mealNames.join('، ')})`;
    }
    sections.push(nutStr);
  } catch(eNut){
    console.warn('[AppContext] Nutrition error:', eNut);
  }

  try {
    const now = new Date();
    const mb = typeof computeMonthBudget === 'function' ? computeMonthBudget(now.getFullYear(), now.getMonth()) : null;
    if(mb){
      const overall = mb.overallBudget || 0;
      const spent = Math.round(mb.totalSpent || 0);
      const remaining = Math.round(mb.remaining || 0);
      let bStr = `💰 الميزانية والمصاريف: إجمالي المصروف هذا الشهر ${spent} ج.م`;
      if(overall > 0){
        bStr += ` من أصل ميزانية ${overall} ج.م (المتبقي: ${remaining} ج.م - استهلكت ${mb.usedPct || 0}%)`;
      } else {
        bStr += ` (المتبقي: حر/غير محدد سقف)`;
      }
      const todayExpenses = (mb.monthExpenses || []).filter(e => e.date === iso);
      if(todayExpenses.length > 0){
        const todaySum = todayExpenses.reduce((s, e) => s + (Number(e.amount) || 0), 0);
        bStr += ` | مصاريف اليوم: ${todaySum} ج.م`;
      }
      sections.push(bStr);
    }
  } catch(eBudget){
    console.warn('[AppContext] Budget error:', eBudget);
  }

  try {
    const effGym = typeof getEffectiveGymDay === 'function' ? getEffectiveGymDay(iso, dayIdx) : null;
    const gymProg = typeof getGymSessionProgress === 'function' ? getGymSessionProgress(iso) : null;
    const isRest = effGym ? (effGym.isRestDay || effGym.gymType === 'rest') : false;
    const routineName = effGym ? (effGym.routineTitle || effGym.routineId || effGym.gymType || 'تمرين') : 'تمرين';
    
    let gymStr = `🏋️‍♂️ الجيم والرياضة: اليوم ${isRest ? 'يوم راحة واستشفاء 🛋️' : `تمرين (${routineName})`}`;
    if(!isRest && gymProg){
      gymStr += ` | المنجز: ${gymProg.doneExercises}/${gymProg.totalExercises} تمارين (${gymProg.doneSets}/${gymProg.totalSets} مجموعات)`;
    }
    sections.push(gymStr);
  } catch(eGym){
    console.warn('[AppContext] Gym error:', eGym);
  }

  try {
    const sleep = typeof loadSleepTimes === 'function' ? loadSleepTimes(iso) : null;
    const sleepH = typeof sleepHours === 'function' ? sleepHours(sleep) : null;
    if(sleepH !== null && !isNaN(sleepH)){
      sections.push(`🌙 النوم: ${sleepH.toFixed(1)} ساعة الليلة الماضية`);
    } else {
      sections.push(`🌙 النوم: لم يسجل بعد`);
    }
  } catch(eSleep){
    console.warn('[AppContext] Sleep error:', eSleep);
  }

  try {
    const dailyNote = typeof loadDailyNote === 'function' ? loadDailyNote(iso) : '';
    if(dailyNote && dailyNote.trim()){
      sections.push(`📝 ملاحظة اليوم: "${dailyNote.trim().slice(0, 150)}"`);
    }
  } catch(eNote){
    console.warn('[AppContext] Note error:', eNote);
  }

  try {
    const mem = typeof loadAiCoachProfileMemory === 'function' ? loadAiCoachProfileMemory() : null;
    if(mem){
      const memParts = [];
      if(mem.workoutSplit) memParts.push(`التقسيم: ${mem.workoutSplit}`);
      if(mem.injuries) memParts.push(`إصابات: ${mem.injuries}`);
      if(mem.goals) memParts.push(`أهداف: ${mem.goals}`);
      if(mem.reading) memParts.push(`قراءة: ${mem.reading}`);
      if(memParts.length > 0){
        sections.push(`🧠 الذاكرة الدائمة: ${memParts.join(' | ')}`);
      }
    }
  } catch(eMem){
    console.warn('[AppContext] Memory error:', eMem);
  }

  return sections.join('\\n');
}

return getUnifiedZatoonaAppContext();
"""

out = driver.execute_script(test_code)
print("=== GENERATED UNIFIED CONTEXT ===")
print(out)
driver.quit()

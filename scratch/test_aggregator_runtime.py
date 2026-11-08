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

test_script = """
function testAggregator(){
  const iso = toISO(weekDates[selectedIdx]);
  const out = {};
  
  // 1. Schedule
  const dayIdx = typeof isoDayIdx === 'function' ? isoDayIdx(iso) : selectedIdx;
  const schedRec = typeof getDaySchedRecord === 'function' && typeof scheduleSettings !== 'undefined' ? getDaySchedRecord(iso, dayIdx, scheduleSettings) : null;
  const schedChecks = typeof loadScheduleCheck === 'function' ? loadScheduleCheck(iso) : {};
  out.sched = {
    total: schedRec && schedRec.acts ? schedRec.acts.length : 0,
    done: schedRec && schedRec.acts ? schedRec.acts.filter(a => schedChecks[a.id]).length : 0
  };

  // 2. Worship
  const prayer = typeof loadPrayer === 'function' ? loadPrayer(iso) : {};
  const fardDone = Object.values(prayer).filter(v => v && v.fard).length;
  out.prayer = { fardDone };

  // 3. Nutrition & Food
  const effMeals = typeof getEffectiveDayMeals === 'function' ? getEffectiveDayMeals(iso, dayIdx) : null;
  const dayTgt = typeof dayTargets === 'function' ? dayTargets(dayIdx, iso) : null;
  const daySt = typeof loadDayStatus === 'function' ? loadDayStatus(iso) : {};
  const water = typeof loadWater === 'function' ? loadWater(iso) : 0;
  out.nutrition = {
    mealsCount: effMeals && effMeals.meals ? effMeals.meals.length : 0,
    targetKcal: dayTgt ? dayTgt.kcal : 0,
    water: water
  };

  // 4. Budget
  const now = new Date();
  const mb = typeof computeMonthBudget === 'function' ? computeMonthBudget(now.getFullYear(), now.getMonth()) : null;
  out.budget = {
    totalSpent: mb ? mb.totalSpent : 0,
    overallBudget: mb ? mb.overallBudget : 0,
    remaining: mb ? mb.remaining : 0
  };

  // 5. Gym
  const effGym = typeof getEffectiveGymDay === 'function' ? getEffectiveGymDay(iso, dayIdx) : null;
  const gymProg = typeof getGymSessionProgress === 'function' ? getGymSessionProgress(iso) : null;
  out.gym = {
    gymType: effGym ? (effGym.routineId || effGym.gymType) : 'none',
    isRest: effGym ? (effGym.isRestDay || effGym.gymType === 'rest') : false,
    prog: gymProg
  };

  // 6. Sleep
  const sleep = typeof loadSleepTimes === 'function' ? loadSleepTimes(iso) : null;
  const sleepH = typeof sleepHours === 'function' ? sleepHours(sleep) : null;
  out.sleep = { sleepH };

  // 7. Note
  const dailyNote = typeof loadDailyNote === 'function' ? loadDailyNote(iso) : '';
  out.note = dailyNote;

  return out;
}
return testAggregator();
"""

res = driver.execute_script(test_script)
print("Aggregator Output:", res)
driver.quit()

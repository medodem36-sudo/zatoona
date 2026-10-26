"""
Phase 13.4B2 — Bridge PWA Reminders to Native Android Layer
Adds syncRemindersToNativeBridge() and integrates it with existing notification system.
"""
import sys, hashlib, shutil

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

errors = []

# ============================================================
# 1. Insert syncRemindersToNativeBridge() after initNotificationScheduler
# ============================================================

BRIDGE_FUNCTION = """
/* ================= NATIVE BRIDGE SYNC (Phase 13.4B2) ================= */
function isNativeBridgeAvailable(){
  return typeof window !== 'undefined' && window.ZatoonaNativeBridge && typeof window.ZatoonaNativeBridge.syncSchedules === 'function';
}

function syncRemindersToNativeBridge(){
  if(!isNativeBridgeAvailable()) return;
  if(!notificationSettings || !notificationSettings.enabled) return;

  const schedules = [];
  const now = new Date();
  const today = toISO(now);

  // Helper: build ISO dates for the next N days
  function nextNDays(n){
    const dates = [];
    for(let i = 0; i < n; i++){
      const d = new Date(now);
      d.setDate(d.getDate() + i);
      dates.push(toISO(d));
    }
    return dates;
  }

  // 1. Prayer notifications \u2014 push cached dated timings for the next 30 days
  if(notificationSettings.prayers){
    const city = loadPrayerCity();
    const prayerOffset = Number(notificationSettings.prayerOffset) || 0;
    const enabledPrayers = [];
    PRAYERS.forEach(p => {
      if(notificationSettings.prayers[p.key]) enabledPrayers.push(p);
    });

    if(enabledPrayers.length > 0){
      const futureDates = nextNDays(30);
      enabledPrayers.forEach(p => {
        const datedTimings = {};
        futureDates.forEach(iso => {
          const pt = loadPrayerTimes(iso);
          if(pt && hasValidPrayerTimes(pt)){
            const pMin = timeToMinStage3D(pt[p.key]);
            if(pMin !== null){
              const triggerMin = pMin - prayerOffset;
              const parts = iso.split('-').map(Number);
              const d = new Date(parts[0], parts[1]-1, parts[2]);
              const tMin = ((triggerMin % 1440) + 1440) % 1440;
              d.setHours(Math.floor(tMin / 60), tMin % 60, 0, 0);
              if(d.getTime() > Date.now()){
                datedTimings[iso] = d.getTime();
              }
            }
          }
        });

        if(Object.keys(datedTimings).length > 0){
          schedules.push({
            id: 'prayer-' + city + '-' + p.key,
            type: 'prayer',
            title: '\\uD83D\\uDD4C \\u0645\\u0648\\u0639\\u062F \\u0623\\u0630\\u0627\\u0646 ' + p.name,
            body: '\\u062D\\u0627\\u0646 \\u0645\\u0648\\u0639\\u062F \\u0623\\u0630\\u0627\\u0646 ' + p.name + ' \\u0641\\u064A \\u0645\\u062F\\u064A\\u0646\\u0629 ' + city,
            mode: 'prayer',
            channelId: 'zatoona_prayers',
            recurrence: 'prayer_dated',
            timeHour: -1,
            timeMinute: -1,
            activeDays: [],
            triggerEpochMs: 0,
            datedTimings: datedTimings,
            city: city,
            enabled: true,
            schemaVersion: 'v2'
          });
        }
      });
    }
  }

  // 2. Custom Reminders
  if(Array.isArray(reminders)){
    reminders.forEach(r => {
      if(!r || r.enabled === false) return;
      let targetMin = null;
      if(r.type === 'prayer'){
        const ptForRem = loadPrayerTimes(today);
        targetMin = (typeof schedResolvePrayer === 'function') ? schedResolvePrayer(ptForRem, r.reference) : null;
      } else if(r.time){
        targetMin = timeToMinStage3D(r.time);
      }
      if(targetMin === null) return;

      const tMin = ((targetMin % 1440) + 1440) % 1440;
      const h = Math.floor(tMin / 60);
      const m = tMin % 60;

      const meta = (typeof REMINDER_TYPE_META !== 'undefined' && REMINDER_TYPE_META[r.type]) || { label: r.type, icon: '\\u23F0' };
      let remMode = 'schedule';
      if(r.type === 'prayer') remMode = 'prayer';
      else if(r.type === 'water') remMode = 'meal';
      else if(r.type === 'gym') remMode = 'gym';
      else if(r.type === 'sleep') remMode = 'sleep';

      let recurrence = 'once';
      const activeDays = [false,false,false,false,false,false,false];
      if(r.recurrence === 'daily'){
        recurrence = 'daily';
      } else if(r.recurrence === 'weekdays' && Array.isArray(r.weekdays)){
        recurrence = 'weekdays';
        for(let i = 0; i < 7 && i < r.weekdays.length; i++){
          activeDays[i] = !!r.weekdays[i];
        }
      }

      let triggerEpochMs = 0;
      if(recurrence === 'once' && r.date){
        const parts = r.date.split('-').map(Number);
        const d = new Date(parts[0], parts[1]-1, parts[2], h, m, 0, 0);
        triggerEpochMs = d.getTime();
      }

      schedules.push({
        id: 'rem-' + r.id,
        type: 'custom',
        title: '\\u23F0 \\u062A\\u0630\\u0643\\u064A\\u0631: ' + (r.title || ''),
        body: (r.title || '') + ' \\u2014 ' + meta.label,
        mode: remMode,
        channelId: 'zatoona_reminders',
        recurrence: recurrence,
        timeHour: h,
        timeMinute: m,
        activeDays: activeDays,
        triggerEpochMs: triggerEpochMs,
        datedTimings: {},
        city: '',
        enabled: true,
        schemaVersion: 'v2'
      });
    });
  }

  // 3. Sleep Wind-Down Routine
  const sleepRoutine = (typeof loadSleepRoutineSettings === 'function') ? loadSleepRoutineSettings() : null;
  if(sleepRoutine && sleepRoutine.reminderEnabled && sleepRoutine.targetBedtime){
    const bedMin = (typeof timeToMinStage3D === 'function') ? timeToMinStage3D(sleepRoutine.targetBedtime) : null;
    if(bedMin !== null){
      const leadMin = Number(sleepRoutine.windDownLeadMin) || 30;
      let trigMin = bedMin - leadMin;
      if(trigMin < 0) trigMin += 1440;
      const h = Math.floor(trigMin / 60);
      const m = trigMin % 60;

      const activeDays = Array.isArray(sleepRoutine.activeDays)
        ? sleepRoutine.activeDays.map(v => !!v)
        : [true,true,true,true,true,true,true];

      schedules.push({
        id: 'sleep-winddown',
        type: 'sleep',
        title: '\\uD83C\\uDF19 \\u0645\\u0648\\u0639\\u062F \\u0627\\u0644\\u0627\\u0633\\u062A\\u0639\\u062F\\u0627\\u062F \\u0644\\u0644\\u0646\\u0648\\u0645',
        body: '\\u062D\\u0627\\u0646 \\u0648\\u0642\\u062A \\u0628\\u062F\\u0621 \\u0631\\u0648\\u062A\\u064A\\u0646 \\u0627\\u0644\\u062A\\u0647\\u062F\\u0626\\u0629 \\u0627\\u0644\\u0645\\u0633\\u0627\\u0626\\u064A',
        mode: 'sleep',
        channelId: 'zatoona_sleep',
        recurrence: 'sleep_routine',
        timeHour: h,
        timeMinute: m,
        activeDays: activeDays,
        triggerEpochMs: 0,
        datedTimings: {},
        city: '',
        enabled: true,
        schemaVersion: 'v2'
      });
    }
  }

  // Push to native bridge
  if(schedules.length > 0){
    try {
      window.ZatoonaNativeBridge.syncSchedules(JSON.stringify(schedules));
    } catch(e){
      console.warn('[native-bridge] syncSchedules error:', e);
    }
  }
}
"""

# The anchor: exact text of initNotificationScheduler (lines 7509-7516)
anchor = (
    "function initNotificationScheduler(){\n"
    "  if(notifSchedulerInterval) clearInterval(notifSchedulerInterval);\n"
    "  checkAndDispatchDueReminders();\n"
    "  notifSchedulerInterval = setInterval(()=> checkAndDispatchDueReminders(), 30000);\n"
    "  document.addEventListener('visibilitychange', ()=>{\n"
    "    if(!document.hidden) checkAndDispatchDueReminders();\n"
    "  });\n"
    "}"
)

if anchor not in text:
    errors.append("Could not find initNotificationScheduler anchor")
else:
    # Replace with enhanced version + bridge function appended after
    new_init = (
        "function initNotificationScheduler(){\n"
        "  if(notifSchedulerInterval) clearInterval(notifSchedulerInterval);\n"
        "  checkAndDispatchDueReminders();\n"
        "  notifSchedulerInterval = setInterval(()=> checkAndDispatchDueReminders(), 30000);\n"
        "  document.addEventListener('visibilitychange', ()=>{\n"
        "    if(!document.hidden) checkAndDispatchDueReminders();\n"
        "  });\n"
        "  // Phase 13.4B2: sync reminders to native Android alarm engine\n"
        "  try { syncRemindersToNativeBridge(); } catch(e){ console.warn('[native-bridge] init sync error:', e); }\n"
        "}" + BRIDGE_FUNCTION
    )
    text = text.replace(anchor, new_init, 1)
    print("1. Inserted syncRemindersToNativeBridge + call in initNotificationScheduler")

# ============================================================
# 2. Hook into onCityChange
# ============================================================
old_city = "async function onCityChange(newCity){\n  savePrayerCity(newCity);"

new_city = (
    "async function onCityChange(newCity){\n"
    "  savePrayerCity(newCity);\n"
    "  // Phase 13.4B2: notify native alarm engine of prayer city change\n"
    "  if(isNativeBridgeAvailable() && typeof window.ZatoonaNativeBridge.updateActivePrayerCity === 'function'){\n"
    "    try { window.ZatoonaNativeBridge.updateActivePrayerCity(newCity); } catch(e){ console.warn('[native-bridge] city sync error:', e); }\n"
    "  }"
)

if old_city not in text:
    errors.append("Could not find onCityChange anchor")
else:
    text = text.replace(old_city, new_city, 1)
    print("2. Added updateActivePrayerCity hook in onCityChange")

# ============================================================
# 3. Hook into saveNotificationSettings (note: 2 space indent)
# ============================================================
old_save_notif = (
    "function saveNotificationSettings(s){\n"
    "  storageSet('notification-settings', JSON.stringify(s));\n"
    "}"
)

new_save_notif = (
    "function saveNotificationSettings(s){\n"
    "  storageSet('notification-settings', JSON.stringify(s));\n"
    "  // Phase 13.4B2: re-sync to native alarm engine after settings change\n"
    "  try { if(typeof syncRemindersToNativeBridge === 'function') syncRemindersToNativeBridge(); } catch(e){}\n"
    "}"
)

if old_save_notif not in text:
    errors.append("Could not find saveNotificationSettings anchor")
else:
    text = text.replace(old_save_notif, new_save_notif, 1)
    print("3. Added syncRemindersToNativeBridge() hook in saveNotificationSettings")

# ============================================================
# 4. Hook into saveReminders
# ============================================================
old_save_rem = "function saveReminders(arr){ storageSet('reminders', JSON.stringify(arr)); }"

new_save_rem = (
    "function saveReminders(arr){ storageSet('reminders', JSON.stringify(arr));\n"
    "  // Phase 13.4B2: re-sync to native alarm engine after custom reminder change\n"
    "  try { if(typeof syncRemindersToNativeBridge === 'function') syncRemindersToNativeBridge(); } catch(e){}\n"
    "}"
)

if old_save_rem not in text:
    errors.append("Could not find saveReminders anchor")
else:
    text = text.replace(old_save_rem, new_save_rem, 1)
    print("4. Added syncRemindersToNativeBridge() hook in saveReminders")

# ============================================================
# 5. Hook into saveSleepRoutineSettings (note: 2 space indent)
# ============================================================
old_save_sleep = (
    "function saveSleepRoutineSettings(settings){\n"
    "  if(!settings || typeof settings !== 'object') return;\n"
    "  storageSet('sleep-routine-settings', JSON.stringify(settings));\n"
    "}"
)

new_save_sleep = (
    "function saveSleepRoutineSettings(settings){\n"
    "  if(!settings || typeof settings !== 'object') return;\n"
    "  storageSet('sleep-routine-settings', JSON.stringify(settings));\n"
    "  // Phase 13.4B2: re-sync to native alarm engine after sleep routine change\n"
    "  try { if(typeof syncRemindersToNativeBridge === 'function') syncRemindersToNativeBridge(); } catch(e){}\n"
    "}"
)

if old_save_sleep not in text:
    errors.append("Could not find saveSleepRoutineSettings anchor")
else:
    text = text.replace(old_save_sleep, new_save_sleep, 1)
    print("5. Added syncRemindersToNativeBridge() hook in saveSleepRoutineSettings")

# ============================================================
# Check for errors
# ============================================================
if errors:
    print("\n*** ERRORS ***")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

# ============================================================
# Write output
# ============================================================
with open('index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

shutil.copy2('index.html', 'zatoona.html')

with open('index.html', 'rb') as f:
    h1 = hashlib.sha256(f.read()).hexdigest()
with open('zatoona.html', 'rb') as f:
    h2 = hashlib.sha256(f.read()).hexdigest()

print(f"\n6. New index.html SHA-256: {h1}")
print(f"7. New zatoona.html SHA-256: {h2}")
print(f"8. Parity match: {h1 == h2}")
print("\nDone!")

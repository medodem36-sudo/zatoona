# Zatoona — Final Master Plan Acceptance Audit (Non-Image Scope)

**Date:** 2026-10-26
**Branch:** `main`
**HEAD:** `b9d1180`
**Regression Gate:** 848 / 848 checks passing across 16 suites (203s)
**Audit Type:** READ-ONLY — no files modified

---

## Executive Summary

The non-image master plan is **SUBSTANTIALLY COMPLETE** with caveats. Of the 11 phases, 7 are COMPLETE, 3 are PARTIAL, and 1 (images) is excluded. The PWA delivers a comprehensive offline-first personal planning app spanning nutrition, gym, prayer, sleep, schedule, budget, search, notes, and reminders. The Android native alarm engine is architecturally sound and device-tested on Samsung Galaxy A04e (Android 14). However, several user-reported UX issues exist around worship checklist clarity, and some validation work remains incomplete (reboot testing, release signing, Android widgets).

---

## 1. Phase-by-Phase Status Matrix

| Phase | Description | Status | Notes |
|-------|------------|--------|-------|
| 1 | Comprehensive audit & integration map | **COMPLETE** | 12 navigation modes, routing system, all sections integrated |
| 2 | Data protection, backup/restore, integrity | **COMPLETE** | Export/import JSON, `validateBackupData()`, schema versioning (v2), migration framework |
| 3 | Customizable gym exercises & routines | **COMPLETE** | Custom exercises, custom gym plans, template catalog, split A/B/C, per-exercise overrides |
| 4 | Exercise encyclopedia, search, alternatives, plans | **COMPLETE** | `exercise-catalog.js`, `stretch-catalog.js`, `filterEncyclopediaCatalog()`, `suggestEncyclopediaAlternatives()`, preset plan templates |
| 5 | Exercise images | **EXCLUDED** | Per audit scope — 19 exercise SVGs exist, image pipeline present |
| 6 | Workout execution, history, progression, analytics | **COMPLETE** | `startGymSession()`, `completeGymSession()`, `exProgression()`, `getExerciseProgressionStats()`, `computeAnalytics()`, rest timer, warmup/cooldown generators |
| 7 | Nutrition, budget, shopping | **COMPLETE** | BMR/TDEE calculation, meal logging, calorie/macro tracking, monthly budget, category budgets, shopping list with actual prices, food database with custom foods |
| 8 | Smart schedule, tasks, habits, healthy sleep | **PARTIAL** | Schedule engine with dynamic timeline, conflict detection, cascading, recurring activities, prayer-synced times — all present. Sleep habits, wind-down routine, adherence tracking — present. Missing: dedicated habit tracker with streaks/goals beyond the schedule checklist (see Issue #1) |
| 9 | Cross-section search & notes | **COMPLETE** | `runGlobalSearch()` across all sections, `collectAllUnifiedNotes()`, per-section notes with attachments |
| 10 | Automation, reminders, personal assistant | **PARTIAL** | Reminder system with 6 types (meal/gym/study/sleep/water/prayer), prayer-linked reminders, in-app + browser notifications, native Android AlarmManager bridge. Missing: true automation rules and personal assistant features |
| 11 | Integration, regression, offline, theme, desktop, mobile | **PARTIAL** | Dark/light theme, service worker offline caching (v14), responsive sidebar+drawer, 848/848 regression tests. Missing: Android widgets, release build, some device-level validations |

---

## 2. Mandatory User-Reported Issues — Detailed Findings

### Issue #1: Healthy Sleep Habits

**Verdict: FEATURE EXISTS AND IS COMPREHENSIVE**

The sleep section (`data-nav="sleep"`, container `#sleepView`, lines 3337–3428) contains 6 numbered sub-sections:

| Section | Container ID | Content | Data Model |
|---------|-------------|---------|------------|
| ١ ملخص النوم | `#sleepSummary` | Habit count, quality, hours | Rendered by `renderSleepSummary()` (L16066) |
| ٢ مواعيد النوم | `#sleepTimeStart`, `#sleepTimeEnd` | Actual bedtime + wake time inputs | Stored as `sleeptimes:{iso}` via `saveSleepTimes()` |
| ٣ روتين التهدئة | `#windDownRoutineChecklist` | 5-step wind-down checklist | Stored as `winddown:{iso}` via `saveWindDown()` |
| ٤ جودة النوم | `#sleepQuality` | 3-option quality selector (كويس/عادي/تعبان) | Stored as `sleepq:{iso}` via `saveSleepQuality()` |
| ٥ عادات نوم صحية | `#sleepHabits` | 5 healthy habits checklist | Stored as `sleephabits:{iso}` via `saveSleepHabits()` |
| ٦ مؤشرات الالتزام | `#sleepAdherenceContainer` | 7/14/28-day adherence stats | Computed by `renderSleepAdherenceSummary()` |

**Healthy sleep habits (Section ٥)** are defined at line 6432 as `SLEEP_HABITS`:
1. نمت وصحيت في معاد قريب من المعتاد (Consistent bedtime/wake)
2. قللت الشاشات آخر نص ساعة قبل النوم (Reduced screens)
3. مفيش كافيين بعد العصر (No caffeine after Asr)
4. سبت مسافة 2-3 ساعات بين آخر تمرين تقيل وميعاد النوم (Exercise timing gap)
5. الأوضة كانت مظلمة وهادئة ومريحة (Dark/quiet/comfortable room)

**Wind-down routine (Section ٣)** has 5 configurable steps defined at line 8399 as `DEFAULT_WIND_DOWN_STEPS`:
1. تقليل أو إيقاف استخدام الشاشات (Reduce screens)
2. تجهيز غرفة النوم وتعتيم الإضاءة (Prepare bedroom)
3. إنهاء المهام اليومية والاستعداد للنوم (Wrap up tasks)
4. أذكار النوم والدعاء المأثور (Bedtime adhkar)
5. قراءة هادئة أو نشاط مريح قبل النوم (Quiet reading)

**Settings panel** (`#sleepRoutineSettingsPanel`, line 3368): target bedtime, target wake time, wind-down lead time (15/30/45/60 min), active days, wind-down reminder toggle.

**Storage keys:**
- `sleephabits:{iso}` — daily habit completion state
- `sleeptimes:{iso}` — actual bed/wake times
- `winddown:{iso}` — wind-down step completion
- `sleepq:{iso}` — quality rating
- `sleep-routine-settings` — target settings

**Conclusion:** This is a full healthy-sleep-habits feature, not just basic duration tracking. It has completion tracking, adherence analytics, and a configurable wind-down routine.

---

### Issue #2: Cairo Prayer Times

**Verdict: FULLY IMPLEMENTED**

**Supported cities** (line 8492):
```javascript
const PRAYER_SUPPORTED_CITIES = ['Minya', 'Alexandria', 'Cairo'];
```

**City selection UI:** Two `<select>` elements with identical city lists:
- `#prayerCitySelect` (prayer page, line 3440)
- `#scPrayerCity` (schedule settings, line 3547)

Both show: المنيا (Minya), الإسكندرية (Alexandria), القاهرة (Cairo).

**City persistence:**
- Saved to `prayer-city` localStorage key via `savePrayerCity()` (line 8536)
- Also stored in `scheduleSettings.prayerCity`
- Default fallback: `'Minya'` (line 8533)

**Calculation engine:**
- API: `https://api.aladhan.com/v1/calendarByCity` with `country=Egypt&method=5` (Egyptian General Authority of Survey, line 8657)
- Fetches full month at a time: `fetchPrayerTimesForMonth(city, year, month)` (line 8649)
- Caching: Per-city-per-day in `prayercache:{city}:{iso}` localStorage keys (lines 8545–8560)
- Validation: `hasValidPrayerTimes()` checks all 5 prayers exist and are in chronological order (line 8511)

**Reminder integration:**
- City change triggers `syncRemindersToNativeBridge()` (line 8714–8717)
- `updateActivePrayerCity()` sent to native bridge
- Per-prayer notification bell toggles in prayer times UI (line 16561)

**Test coverage:** `test_phase13_2_cairo_prayer.py` — 36 checks passing.

**Potential issue:** If the Aladhan API is unreachable (offline), prayer times fall back to manual entry or previously cached data. The offline fallback is functional but not user-obvious. The API status is shown in `#prayerApiStatus`.

---

### Issue #3: Ambiguous Religious-Practice & Daily Checklist Controls

**Verdict: CONTROLS ARE CORRECTLY LABELED — UX CAN BE IMPROVED**

The prayer page (`#prayerView`, lines 3430–3467) has 7 sections:

#### Section ٣: الفروض والسنن الراتبة (Fard + Sunnah Ratibah)
- **Renderer:** `renderPrayerFard()` (line 16581)
- **Controls per prayer:** Two labeled buttons: `فرض` (Fard) and `سنة` (Sunnah)
- **Storage:** `prayer:{iso}` → `{ fajr: {fard:bool, sunnah:bool}, dhuhr: {...}, ... }`
- **Tap behavior:** Toggles the respective boolean. Button turns green (`on-right`) when active.
- **Issue identified:** The buttons are small and both show `✓` style toggles. The labels `فرض` / `سنة` are present but at `font-size: .72rem` — small and easy to confuse as identical checkmarks if the user doesn't read the button text carefully.

#### Section ٤: قيام الليل والوتر
- **Renderer:** `renderQiyam()` → `renderSimpleChecklist('qiyamWitr', QIYAM_WITR, ...)` (line 16618)
- **Items:** `['قيام الليل', 'الوتر']` (line 6449)
- **Controls:** Single `✓` toggle button per item, with the Arabic name as label
- **Storage:** `qiyam:{iso}` → `{ i0: true/false, i1: true/false }`
- **Labels:** ✅ Present and correct

#### Section ٥: باقي النوافل
- **Renderer:** `renderNawafilExtra()` → `renderSimpleChecklist('nawafilExtra', NAWAFIL_EXTRA, ...)` (line 16627)
- **Items:** `['صلاة الضحى', 'تحية المسجد', 'سنة الوضوء (ركعتين بعد كل وضوء)']` (line 6454)
- **Controls:** Single `✓` toggle per item with Arabic label
- **Storage:** `nawafil:{iso}`

#### Section ٦: أذكار الصباح والمساء
- **Renderer:** `renderAzkar()` → `renderSimpleChecklist('azkar', AZKAR, ...)` (line 16636)
- **Items:** `['أذكار الصباح', 'أذكار المساء']` (line 6467)
- **Storage:** `azkar:{iso}`

#### Section ٧: القرآن
- **Renderer:** `renderQuranWird()` → `renderSimpleChecklist('quranWird', QURAN_WIRD, ...)` (line 16645)
- **Items:** `['ورد سماع (استماع للقرآن)', 'ورد قراءة (تلاوة يومية)', 'حفظ آيتين جديدتين', 'مراجعة المحفوظ من قبل']` (line 6460)
- **Hint text:** "الورد اليومي: سماع + قراءة + حفظ آيتين + مراجعة اللي فات" (line 3465)
- **Storage:** `quran:{iso}`

#### Root cause of user confusion:

1. **`renderSimpleChecklist()` (line 11212)** renders every item as:
   ```
   [Arabic label text]  [✓ button]
   ```
   The `✓` button's only visual distinction between "done" and "not done" is background color (green vs transparent). There is no explanatory text on the button itself.

2. **All 4 sections (qiyam, nawafil, azkar, quran) use identical visual treatment** — same button style, same green toggle. The user sees a vertical stack of items with identical-looking checkmark buttons.

3. **The Fard/Sunnah section uses two buttons per row** (`فرض` + `سنة`), which could look like two separate check states rather than two independent tasks.

4. **No duplication found** — each section tracks genuinely separate data in separate storage keys. The checklist items themselves are NOT duplicated between sections. However, the **visual similarity across sections** may make them feel duplicated.

5. **No missing labels** — all items have Arabic text. The issue is **visual density** and **identical toggle styling** making it hard to distinguish sections at a glance.

#### Recommendations (not implemented in this audit):
- Add section-level hints/descriptions for sections ٤/٥/٦
- Use different toggle colors or icons for different worship categories
- Add a completion counter header to each section (like the ✅ X/Y already shown in the summary)

---

### Issue #4: Alarms and Notifications When App is Closed

**Verdict: ARCHITECTURALLY SOUND — PARTIAL DEVICE VALIDATION**

#### PWA Reminder System (index.html)
| Component | Location | Description |
|-----------|----------|-------------|
| Reminder types | `REMINDER_TYPE_META` (L7085) | meal, gym, study, sleep, water, prayer |
| Timer loop | L7517 | `setInterval(checkAndDispatchDueReminders, 30000)` — 30s polling |
| Dispatch | `dispatchNotification()` (L7317) | Shows in-app modal + browser `Notification` |
| Browser notification | `tryDispatchWindowNotification()` (L7295) | Uses `Notification` API if permission granted |
| Native bridge sync | `syncRemindersToNativeBridge()` (L7529) | Builds schedule array, sends to `ZatoonaNativeBridge.syncSchedules()` |

**PWA limitation (acknowledged in code, line 3405):**
> "التنبيهات تعمل أثناء فتح التطبيق أو تشغيله بالخلفية. التنبيه مع إغلاق المتصفح تمامًا سيتم دعمه في مرحلة معمارية قادمة."
> (Notifications work while the app is open or in background. Notifications with the browser fully closed will be supported in a future architecture phase.)

#### Android Native Alarm Engine

| Component | File | Key Functionality |
|-----------|------|-------------------|
| `AlarmReceiver` | `AlarmReceiver.kt` | Receives AlarmManager triggers when app is closed |
| `BootReceiver` | `BootReceiver.kt` | Reschedules all alarms on BOOT_COMPLETED, TIME_SET, TIMEZONE_CHANGED, MY_PACKAGE_REPLACED, SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED |
| `ZatoonaAlarmScheduler` | `ZatoonaAlarmScheduler.kt` | `setExactAndAllowWhileIdle()` with fallback to `setExact()` → `setAndAllowWhileIdle()` → `set()` |
| `ZatoonaBridge` | `ZatoonaBridge.kt` | `@JavascriptInterface syncSchedules()`, `syncUpcomingAlarms()`, `updateActivePrayerCity()`, `getAlarmCapabilities()` |
| `ZatoonaNotificationManager` | `ZatoonaNotificationManager.kt` | 3 channels: general, prayer, sleep |
| `ZatoonaScheduleRepository` | `ZatoonaScheduleRepository.kt` | SharedPreferences persistence with JSON serialization |

**Permissions (AndroidManifest.xml):**
- `RECEIVE_BOOT_COMPLETED` ✅
- `POST_NOTIFICATIONS` ✅
- `SCHEDULE_EXACT_ALARM` ✅
- `WAKE_LOCK` ✅
- `ACCESS_NETWORK_STATE` ✅

#### Evidence Classification by App State

| State | Evidence Level | Details |
|-------|---------------|---------|
| App open (foreground) | **TESTED_ON_DEVICE** | In-app modal + browser notification dispatch verified |
| App in background (Recents) | **CODE_EXISTS** | PWA timer continues; Android AlarmManager independent |
| App swiped from Recents | **TESTED_ON_DEVICE** | Phase 13.4B2.2 confirmed notification delivery after swipe-away on Samsung A04e |
| Device reboot | **CODE_EXISTS** | `BootReceiver` with `BOOT_COMPLETED` + `rescheduleAll()`. NOT tested on physical device |
| Force Stop | **CODE_EXISTS** | After Force Stop, `BootReceiver` and `AlarmReceiver` are disabled by Android. Alarms will NOT fire until the app is manually reopened. This is an Android OS limitation, not a bug |
| Battery optimization / Doze | **CODE_EXISTS** | Uses `setExactAndAllowWhileIdle()` which works through Doze. Samsung-specific aggressive battery management NOT tested |
| Manufacturer restrictions | **NOT_TESTED** | Samsung/Xiaomi/Huawei background kill behaviors require per-device testing |

---

### Issue #5: Android Home-Screen Widgets

**Verdict: DO NOT EXIST**

No widget-related components found in:
- No `AppWidgetProvider` subclass in any Kotlin file
- No `<receiver>` with `APPWIDGET_UPDATE` in `AndroidManifest.xml`
- No `appwidget-provider` XML in `res/xml/`
- No widget layout XMLs anywhere under `android/`
- No `RemoteViews` usage in any source file

#### Implementation Requirements for Proposed Widgets

**Widget 1: Next Prayer Widget**
- Components: `NextPrayerWidgetProvider`, `widget_next_prayer.xml` layout, `next_prayer_widget_info.xml`
- Data source: Read from SharedPreferences (same `ZatoonaScheduleRepository` already used by alarm engine)
- Refresh: AlarmManager-driven update at each prayer time transition; minimum system interval is 30 min
- Click: Open app to prayer page via intent with `data-nav=prayer`
- Offline: ✅ Works from cached SharedPreferences data
- Complexity: **Medium** — requires syncing prayer times from WebView to SharedPreferences
- Risk: Prayer times may be stale if app hasn't been opened to fetch from API

**Widget 2: Daily Habits Widget**
- Components: `DailyHabitsWidgetProvider`, list-based widget using `RemoteViewsService`
- Data source: Would need localStorage bridge — the WebView stores habit state in localStorage which is not directly accessible to a widget
- Refresh: On app open + periodic alarm
- Click: Open app to relevant section
- Offline: ⚠️ Requires WebView localStorage extraction mechanism
- Complexity: **High** — localStorage ↔ SharedPreferences synchronization layer needed
- Risk: Data sync lag; potential for stale display

**Widget 3: Quick Access Widget**
- Components: Simple `AppWidgetProvider` with 3-4 icon buttons
- Data source: None — static shortcut buttons
- Click: Open app with different `data-nav` parameters
- Offline: ✅ Fully static
- Complexity: **Low**
- Risk: Minimal

---

## 3. Source & Test Review Findings

### Test Suite Summary
- **31 test files** in `scratch/`
- **Master regression gate:** 16 suites, 848 checks, all passing
- **Total duration:** 203s

### Findings (ranked by severity)

| Severity | Finding | Location | Details |
|----------|---------|----------|---------|
| **MEDIUM** | No data encryption | Backup/restore system | `exportAllData()` exports raw JSON. No AES/encryption option. Data at rest in localStorage is unencrypted |
| **MEDIUM** | Force Stop kills all alarms | Android OS behavior | `AlarmReceiver` and `BootReceiver` are disabled after Force Stop. Documented limitation, not fixable |
| **MEDIUM** | Reboot alarm persistence untested | `BootReceiver.kt` | Code exists but never validated on physical device. `rescheduleAll()` must be verified |
| **LOW** | Prayer API offline fallback not prominent | `ensurePrayerTimes()` L8691 | Falls back to cache or empty state silently. User may not realize times are from cache |
| **LOW** | Scratch files committed to repo | Commit `b9d1180` | 164 developer scratch scripts now tracked in Git. Should be in `.gitignore` |
| **LOW** | PWA reminder polling interval | L7517 | 30-second `setInterval` — acceptable but drains battery slightly if kept open. Only active when page is visible |
| **INFO** | Schema version at 2 | L6623 | Migration framework exists but only has migrations 0→1 and 1→2. Future additions are straightforward |
| **INFO** | Trailing whitespace in scratch files | `git diff --check` | Cosmetic only — all in scratch files, not application code |

### Code Quality Observations
- **No unsafe `eval()` or `innerHTML` XSS** — user text is escaped via `escapeHtml()` (verified by test suite)
- **Defensive JSON.parse** — all `storageGetJSON()` calls have fallback defaults
- **Date handling** — uses ISO strings consistently (`toISO()`), no timezone confusion
- **Single-file architecture** — 24,638-line `index.html` is monolithic but functional. No module bundler needed for offline-first PWA

---

## 4. Validation Checklist

### A. Verifiable by Source Inspection / Automated Tests
| Item | Status |
|------|--------|
| All 5 SLEEP_HABITS exist with labels | ✅ Verified |
| Cairo/Minya/Alexandria in city list | ✅ Verified |
| Aladhan API integration with method=5 | ✅ Verified |
| All worship checklist items have labels | ✅ Verified |
| Fard/Sunnah dual-toggle per prayer | ✅ Verified |
| Native alarm bridge builds schedule JSON | ✅ Verified |
| BootReceiver handles 5 broadcast types | ✅ Verified |
| Backup export/import with validation | ✅ Verified |
| Schema migration framework | ✅ Verified |
| 848/848 regression checks | ✅ Verified |

### B. Requires Real Browser on Laptop
| Item | Status |
|------|--------|
| Dark/light theme toggle visual quality | ⬜ NOT TESTED |
| Responsive layout at different viewport sizes | ⬜ NOT TESTED |
| Service worker offline cache (close network, reload) | ⬜ NOT TESTED |
| Prayer API fetch and cache display | ⬜ NOT TESTED |
| Backup file download/re-import cycle | ⬜ NOT TESTED |

**Manual test steps for browser validation:**
1. Open `index.html` in Chrome. Navigate all 12 pages.
2. Toggle dark mode via settings. Verify all sections render correctly.
3. Go to Prayer page. Select Cairo. Wait for API response. Verify 5 prayer times appear.
4. Switch to Minya. Verify times change.
5. Go offline (DevTools → Network → Offline). Reload. Verify app loads from cache.
6. Go to Settings. Export data. Delete a few entries. Import the backup. Verify restoration.

### C. Requires Real Android Phone
| Item | Status |
|------|--------|
| Notification delivery with app swiped | ✅ TESTED (Samsung A04e) |
| Notification tap routing to correct page | ✅ TESTED |
| Alarm persistence after device reboot | ⬜ NOT TESTED |
| Alarm behavior after Force Stop | ⬜ NOT TESTED |
| Battery optimization / Doze impact | ⬜ NOT TESTED |
| Samsung-specific aggressive memory management | ⬜ NOT TESTED |
| Release APK build and signing | ⬜ NOT DONE |

**Manual test steps for reboot validation:**
1. Open app. Navigate to Prayer. Enable all 5 prayer notifications.
2. Close app (swipe from Recents).
3. Reboot device.
4. Wait for next prayer time.
5. Verify notification appears without manually reopening the app.

---

## 5. Prioritized Improvement Recommendations

### Critical Fixes (Do Now)

| # | Proposal | Benefit | Complexity | Dependencies |
|---|----------|---------|------------|-------------|
| 1 | **Remove scratch files from Git tracking** | Clean repository, reduce clone size | Low | `git rm --cached scratch/` + add to `.gitignore` |
| 2 | **Validate reboot alarm persistence** on physical device | Prove BootReceiver works in production | Low | Physical Android device |
| 3 | **Add visual distinction to worship checklist sections** | Reduce user confusion about repeated checkmarks | Low | CSS/icon changes only |

### Missing Features (Do Soon)

| # | Proposal | Benefit | Complexity | Dependencies |
|---|----------|---------|------------|-------------|
| 4 | **Encrypted backup option** | Protect personal data in exported files | Medium | Web Crypto API (AES-GCM), password UI |
| 5 | **Release signing configuration** | Enable Play Store distribution | Medium | Keystore generation, Gradle config |
| 6 | **Habit streak tracker** | Motivate daily consistency with streak counts | Medium | New localStorage model + UI component |
| 7 | **Quick Access home-screen widget** | 1-tap app entry to key sections | Low | Simple `AppWidgetProvider` |

### Optional Enhancements (Do Later)

| # | Proposal | Benefit | Complexity | Dependencies | Priority |
|---|----------|---------|------------|-------------|----------|
| 8 | **Next Prayer widget** | At-a-glance prayer time from home screen | Medium | SharedPreferences sync | Later |
| 9 | **Daily Habits widget** | See habit completion without opening app | High | localStorage↔SharedPreferences bridge | Later |
| 10 | **Prayer Qibla compass** | Direction to Qibla for travelers | Medium | Device sensors, geolocation | Later |
| 11 | **Weekly/monthly worship report** | Visual summary of worship consistency | Low | Analytics computation exists | Later |
| 12 | **Fasting tracker** | Log fasting days (Sunnah fasts, Ramadan) | Low | New checklist section | Later |
| 13 | **Social accountability** (optional sharing) | Share progress with accountability partner | Medium | Export/share mechanism, privacy controls | Later |
| 14 | **Smart notification grouping** | Batch multiple due reminders into one notification | Low | Android notification group | Later |
| 15 | **Per-manufacturer battery optimization guide** | In-app instructions for Samsung/Xiaomi/Huawei users | Low | Static content pages | Soon |

### Not Recommended

| Proposal | Reason |
|----------|--------|
| Cloud sync | Contradicts offline-first privacy-focused design philosophy |
| Multi-language i18n | Single-user app in Arabic; adds complexity without benefit |
| WebSocket push notifications | Requires server infrastructure; native AlarmManager is sufficient |

---

## 6. Remediation Roadmap (Dependency Order)

```
Phase A: Critical Fixes (No dependencies)
├── A1. Remove scratch/ from Git tracking
├── A2. Reboot alarm persistence test on physical device
└── A3. Worship checklist visual improvements (CSS only)

Phase B: Release Preparation (Depends on A2)
├── B1. Release signing keystore + Gradle config
├── B2. Release APK build + device test
└── B3. Per-manufacturer battery guide (static content)

Phase C: Feature Additions (Independent)
├── C1. Encrypted backup export
├── C2. Habit streak tracker
└── C3. Quick Access widget

Phase D: Advanced Widgets (Depends on B1)
├── D1. Next Prayer widget
└── D2. Daily Habits widget (requires localStorage bridge)

Phase E: Optional Enhancements (Independent)
├── E1. Weekly worship report
├── E2. Fasting tracker
└── E3. Qibla compass
```

---

## 7. Files & Functions Reference

| Feature Area | Key Files/Functions |
|-------------|-------------------|
| Sleep habits | `SLEEP_HABITS` (L6432), `renderSleep()` (L16470), `saveSleepHabits()` (L8396) |
| Wind-down routine | `DEFAULT_WIND_DOWN_STEPS` (L8399), `renderWindDownChecklist()` (L16205) |
| Prayer city | `PRAYER_SUPPORTED_CITIES` (L8492), `loadPrayerCity()` (L8529), `fetchPrayerTimesForMonth()` (L8649) |
| Worship checklists | `QIYAM_WITR` (L6449), `NAWAFIL_EXTRA` (L6454), `AZKAR` (L6467), `QURAN_WIRD` (L6460) |
| Checklist renderer | `renderSimpleChecklist()` (L11212) |
| Fard/Sunnah | `renderPrayerFard()` (L16581) |
| Reminder system | `checkAndDispatchDueReminders()` (L7352), `syncRemindersToNativeBridge()` (L7529) |
| Native alarm | `ZatoonaAlarmScheduler.kt`, `AlarmReceiver.kt`, `BootReceiver.kt` |
| Native bridge | `ZatoonaBridge.kt` — `syncSchedules()`, `syncUpcomingAlarms()`, `getAlarmCapabilities()` |
| Backup/restore | `exportAllData()` (L21387), `validateBackupData()` (L21053) |
| Schema migration | `runSchemaMigrations()` (L6629), `SCHEMA_VERSION=2` (L6623) |
| Global search | `runGlobalSearch()` (L20032) |
| Analytics | `computeAnalyticsForDates()` (L18777), `getExerciseProgressionStats()` (L19525) |
| Service worker | `sw.js` (v14), registered at L23844 |

---

*This audit is READ-ONLY. No files were modified, created, or deleted. No commits or pushes were made.*

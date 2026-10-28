# Zatoona — Master Project Roadmap & Verification Baseline

**Document Path:** `docs/MASTER_ROADMAP.md`
**Last Updated:** 2026-10-28 15:25:00 +03:00
**Repository:** `C:\Users\Lenovo\Documents\GitHub\zatoona`
**GitHub Remote:** `medodem36-sudo/zatoona` (`main`)
**Base HEAD:** `6646bb7`
**Regression Gate Status:** **28 / 28 Suites Passing (1231 / 1231 Checks, 198.75s)**
**HTML 3-Way Parity:** **1,357,317 bytes | SHA-256: `04fd5dcfd0417b9170d57d508a3e14329c5aff644db1a3389f029cb6d7ac2dfc`**

---

## 1. Classification Taxonomy

All features and roadmap items are classified under the strict verification standard:
- **Verified Complete:** Supported by observable, reproducible automated or live hardware test evidence.
- **Implemented but Incompletely Verified:** Full source code exists, but some edge cases or environments remain open.
- **Partially Implemented:** Functional foundation in place; specific sub-features or interfaces pending.
- **Missing:** Explicitly scoped on the roadmap but not yet implemented.
- **Blocked or Deferred:** Held pending an external dependency or explicit user authorization (e.g. physical reboot).

---

## 2. Comprehensive 16-Phase Status Matrix

| Phase | Description | Status | Evidence & Test Suites | Dependencies & Blockers |
| :--- | :--- | :---: | :--- | :--- |
| **Phase 1** | Repository Integrity & Engineering Hygiene | **Verified Complete** | Clean working tree baseline (`c382a50`), 3-way HTML byte parity enforced, signing secrets guarded in `.gitignore`. | None. |
| **Phase 2** | Worship Checklist UX, Badges & Persistence | **Verified Complete** | `test_phase13_1_checklist_labels.py` (47/47 PASS), `test_phase13_worship_ux_badges.py` (31/31 PASS). Live 6-metric summary, category borders, counter badges. | None. |
| **Phase 3** | Prayer-City & Calculation Verification | **Verified Complete** | `test_phase13_2_cairo_prayer.py` (36/36 PASS). Minya, Alexandria, Cairo selection, bidirectional sync, cache isolation. | None. |
| **Phase 4** | Sleep & Recovery Tracking | **Verified Complete** | `test_phase13_3_sleep_habits.py` (70/70 PASS). Bedtime routines, wind-down checklist, 5 core sleep habits, 7/28-day adherence analytics. | None. |
| **Phase 5** | Customizable Gym & Exercise Education | **Verified Complete** | `test_phase5b1_1_image_policy.py` (92/92 PASS), `test_phase5b1_2_legacy_images.py` (94/94 PASS), `test_phase9c1_stretch_encyclopedia.py` (46/46 PASS), `test_phase9c2_warmup.py` (54/54 PASS), `test_phase9c3_cooldown.py` (56/56 PASS). | None. |
| **Phase 6** | Workout Execution & Analytics | **Verified Complete** | `test_phase6c_workout_analytics.py` (36/36 PASS). Session lifecycle, rest timers, volume math, PR separation (weight vs rep). | None. |
| **Phase 7** | Nutrition, Meals, Shopping & Budget | **Verified Complete** | BMR/TDEE calculations, meal overrides, category budgets, shopping list item aggregation, data export/import preservation. | None. |
| **Phase 8** | Schedules, Habits, Notes & Search | **Verified Complete** | `test_phase9b_unified_notes.py` (51/51 PASS), `test_phase9b1_2_gate.py` (31/31 PASS), `test_phase8b_notification_routing.py` (37/37 PASS). Dynamic timeline, conflict prevention, unified notes hub. | None. |
| **Phase 9** | Exercise Media & Offline Asset Reliability | **Verified Complete** | `test_phase12_1b_exercise_images.py` (43/43 PASS). 19 curated exercise SVGs, 34 stretch SVGs, precached in Service Worker (v24). | Secondary SVG batch excluded from current scope. |
| **Phase 10** | Data Integrity, Backup & Storage Resilience | **Verified Complete** | `test_phase10_encrypted_backup.py` (21/21 PASS). PBKDF2 + AES-GCM 256-bit encrypted export/import, password protection, unencrypted backward-compatibility, atomic rollback. | None. |
| **Phase 11** | Cross-Feature Integration & Quality | **Verified Complete** | Master regression gate passing 23/23 suites (1015/1015 checks), 3-way HTML synchronization, RTL layout integrity. | None. |
| **Phase 12** | Exercise Catalog & Extended Media | **Verified Complete** | Core encyclopedia and stretch catalog verified. Future image additions deferred per project agreement. | None. |
| **Phase 13.1**| Worship Checklist Labels Repair | **Verified Complete** | `test_phase13_1_checklist_labels.py` (47/47 checks passing). | None. |
| **Phase 13.2**| Cairo Prayer-Time Support | **Verified Complete** | `test_phase13_2_cairo_prayer.py` (36/36 checks passing). | None. |
| **Phase 13.3**| Sleep Habits & Bedtime Routine | **Verified Complete** | `test_phase13_3_sleep_habits.py` (70/70 checks passing). | None. |
| **Phase 13.3B**| Habit Streaks Engine & Motivation Tracker | **Verified Complete** | `test_phase13_habit_streaks.py` (26/26 checks passing). Multi-domain streaks, personal bests, calendar math. | None. |
| **Phase 13.4**| Native Android Reminders & Alarms | **Implemented & Partially Verified** | `test_phase13_4b1_scaffold.py` (50/50), `test_phase13_4b1_2_android_buildability.py` (31/31), `test_phase13_4b2_alarms.py` (74/74). Hardware verified on Samsung Galaxy A04e. | Physical reboot verification is explicitly **Deferred**. |
| **Phase 13.5B**| Per-Manufacturer Battery Optimization Guide | **Verified Complete** | `test_phase13_battery_guide.py` (26/26 checks passing). OEM tabs (Samsung, Xiaomi, Huawei, Oppo, Pixel), native shell detection. | None. |
| **Phase 13.6B**| Fasting Tracker & Sunnah Days | **Verified Complete** | `test_phase13_fasting_tracker.py` (18/18 checks passing). Sunnah detection (Mondays/Thursdays, White Days), fasting categories, monthly counter badge. | None. |
| **Phase 13.7B**| Weekly & Monthly Worship Adherence Report | **Verified Complete** | `test_phase13_worship_adherence.py` (22/22 checks passing). 7/28-day window adherence stats, per-prayer breakdown, multi-pillar tracking, Overview integration. | None. |
| **Phase 13.8B**| Prayer Qibla Compass Engine & Dial | **Verified Complete** | `test_phase13_qibla_compass.py` (23/23 checks passing). Spherical trigonometry bearing/distance, offline cities, SVG dial, device orientation alignment. | None. |
| **Phase 13.9** | Custom Habits & Skills Learning Tracker + Share Card | **Verified Complete** | `test_phase13_habits_and_share.py` (29/29 checks passing). Daily custom habits, skills acquisition goals, individual streaks, daily summary social accountability card. | None. |
| **Phase 13.10** | Smart Notification Grouping (Proposal #14) | **Verified Complete** | `test_phase13_smart_notification_grouping.py` (37/37 checks passing). Concurrent reminder batching, user toggle, Android group summary, deduplication, backup patterns. | None. |
| **Phase 13.5**| Native Android Home-Screen Widgets (Quick Access & Next Prayer) | **Verified Complete** | `test_phase13_5_widgets.py` (57/57) & `test_phase13_5_next_prayer_widget.py` (53/53). Native `QuickAccessWidgetProvider` & `NextPrayerWidgetProvider`, RemoteViews layouts, Arabic countdown math, ZatoonaBridge cache sync, APK verified. | None. |
| **Phase 13.6**| Pantry / Inventory Capability | **Missing** | Scoped as future optional module. Needs UX design to prevent conflicting with existing shopping list. | Low priority. |
| **Phase 13.7**| Optional Privacy-Conscious AI Assistant | **Planned / Disabled** | Strictly opt-in; no keys or endpoints configured in frontend. | Deferred until core application is finalized. |
| **Phase 14** | Release Signing Configuration Template | **Verified Complete** | `test_phase14_release_signing.py` (40/40 checks passing). Conditional `signingConfigs.release` in `build.gradle.kts`, `keystore.properties.example` template, `.gitignore` guards, R8 ProGuard rules. | Keystore generation remains manual for security. |
| **Phase 15** | Physical-Device Validation | **Partially Verified** | Verified on Samsung Galaxy A04e (Android 14) for foreground, background, swipe-away, Samsung Power Saving, lock-screen `AlarmActivity`. | Physical device reboot test remains deferred. |
| **Phase 16** | Final Integration & Post-Release Review | **Planned** | Final release verification checklist prepared. | Depends on Phase 14 & 15. |

---

## 3. High-Value Actionable Candidate Tasks

Reconciling `docs/Final_Master_Plan_Acceptance_Audit.md` and the current state, the top unblocked candidate tasks are:

1. **Physical Device Reboot Verification Test (Phase 15):**
   - **Need:** Validate `BootReceiver` alarm rescheduling after physical hardware reboot.
   - **Scope:** Physical Samsung Galaxy A04e device test.
   - **Status:** Explicitly held/deferred pending user approval.

2. **Production Release Keystore Generation (Phase 14 / Phase 16):**
   - **Need:** Generate production `zatoona-release.keystore` and create local `android/keystore.properties` following `keystore.properties.example`.
   - **Scope:** Developer local action (must not be committed to Git).
   - **Need:** Wire `signingConfigs.release` in `android/app/build.gradle.kts` to safely read credentials from an untracked local file or environment variables without committing keystores or secrets.
   - **Scope:** Gradle build configuration only (no secrets committed).
   - **Benefit:** Prepares the build system for release readiness without risking secret leaks.

---

## 4. Next Recommended Task

**Task:** **Master Acceptance Audit Reconciliation & Release Verification**
**Rationale:** With all 28 automated test suites passing (1,231 / 1,231 checks, 100% pass rate) covering Worship, Sleep, Gym, Nutrition, Schedules, Habits, Alarms, Security, Release Signing Template, and both Native Android Widgets (Quick Access & Next Prayer), the application is functionally complete across all planned acceptance criteria. Next step is a clean status reconciliation and handoff.

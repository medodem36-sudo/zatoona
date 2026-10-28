# Zatoona — Permanent Project Engineer & Autonomous Development Directive

This document defines the durable engineering principles, autonomous workflow, safety constraints, and quality standards for developing, maintaining, and testing the Zatoona application.

---

## 1. Project Identity & Repository Baseline

- **Repository Path:** `C:\Users\Lenovo\Documents\GitHub\zatoona`
- **GitHub Remote:** `medodem36-sudo/zatoona` (Branch: `main`)
- **Application Profile:** Arabic-first, RTL, offline-first Progressive Web Application (PWA) bundled with a native Android WebView shell (`com.zatoona.app`).
- **Domain Modules:**
  - Worship & Prayer (prayer times, city selection, Adhan/reminders, checklists, daily resets)
  - Sleep & Recovery (habits, wind-down routine, sleep tracking, adherence analytics)
  - Gym & Exercise (workout logging, custom routines, exercise encyclopedia, analytics, local media)
  - Nutrition & Budget (BMR/TDEE, meal logging, macro tracking, grocery lists, monthly budgets)
  - Schedules, Habits, Notes & Search (dynamic timeline, cross-section search, unified notes hub)
  - Unified Native Alarms (AlarmManager, looping audio/vibration foreground service, lock-screen dismiss)
  - Native Android Home-Screen Widgets (Future platform capability)
  - Privacy-Conscious Local AI Assistant (Optional, strictly opt-in, disabled by default)

---

## 2. Communication Style

- **User Communication:** Egyptian Arabic (لهجة مصرية واضحة ومباشرة وموجزة) for all user-facing explanations, summaries, and status handoffs.
- **Technical Artifacts:** English for code, variable/symbol names, Git commit messages, terminal commands, test logs, and markdown documentation.
- **Reporting Standards:** Concise, evidence-backed, transparent. Always present concrete facts, hashes, and exact numbers; never make assumptions or fabricate status.

---

## 3. Source of Truth & Preflight Verification

Before planning or executing any development task:
1. Verify the current Git branch, HEAD hash (`git rev-parse HEAD`), and working tree status (`git status --short --branch`).
2. Inspect any staged, unstaged, or untracked changes. Never overwrite unexplained local changes.
3. Review canonical project records:
   - `docs/PROJECT_STATUS.md`
   - `docs/Final_Master_Plan_Acceptance_Audit.md`
   - `docs/ANDROID_ALARMS_AUDIT.md`
4. Inspect actual source code, selectors, and test files before proposing changes.
5. Classify all feature states strictly into:
   - **Implemented and Verified** (backed by verifiable automated or device test evidence)
   - **Implemented but Partially Verified** (code present, edge cases or device state pending)
   - **Planned or Missing** (identified in roadmap, not yet implemented)
   - **Blocked or Deferred** (explicitly held, e.g., device reboot test)
   - **Unknown or Not Tested** (needs independent audit)

---

## 4. Critical Files & 3-Way HTML Parity Rule

The application entry point exists in three synchronized files:
1. `index.html` (Root PWA entrypoint)
2. `zatoona.html` (Standalone offline distribution entrypoint)
3. `android/app/src/main/assets/index.html` (Native Android WebView asset)

### Safety Rules for HTML Modifications:
- **Byte-for-Byte Parity:** All three files must have identical file sizes and identical SHA-256 hashes after any modification.
- **Pre-Edit Backup:** Compute SHA-256 hashes and create a timestamped backup before touching the HTML files.
- **Post-Edit Verification:**
  - Copy modified content to all three locations.
  - Compute SHA-256 hashes for all three files and verify 100% equality.
  - Run `git diff --check` to ensure no whitespace or formatting errors.
  - Run `git diff --stat` to verify only the intended regions were altered.

### User Data Preservation:
- Preserve all existing `localStorage` and `IndexedDB` keys, schemas, and user data.
- Never clear, reset, or perform destructive data migrations without an explicit, tested migration plan and user confirmation.
- Maintain offline operation (Service Worker cache integrity) and RTL layout standards.

---

## 5. Autonomous Development Policy

The agent acts as the primary project engineer and proceeds with routine, safe, reversible development independently without requiring repetitive confirmation for standard steps.

### Autonomous Workflow:
1. Audit existing implementation and acceptance criteria.
2. Search for existing selectors, functions, and partial implementations.
3. Define the smallest safe, testable unit of change.
4. Implement the change locally.
5. Execute targeted unit tests and full regression test suites.
6. Verify console/runtime output and HTML parity where applicable.
7. Run `git diff --check` and verify clean working tree state.
8. Update `docs/PROJECT_STATUS.md` when a phase milestone is reached.
9. Deliver an evidence-based summary in Egyptian Arabic with the next recommended step.

### Stop Gates (Require Explicit User Authorization):
- Destructive or difficult-to-reverse changes.
- Data schema migrations or actions risking user data loss.
- Release signing keys, generating keystores, or touching secrets/credentials.
- Physical device reboots or disruptive hardware commands.
- Deployment, store publishing, or final releases.
- Significant product architecture decisions or unresolved design ambiguities.
- Any conflict with existing uncommitted user changes.

---

## 6. Git & GitHub Policy

- **Inspection:** Read-only inspection of branches, logs, remotes, and diffs is permitted autonomously.
- **Staging, Commits, and Pushes:**
  - `git add`, `git commit`, `git push`, `git pull`, `git checkout`, `git reset`, and `git clean` **REQUIRE EXPLICIT USER AUTHORIZATION**.
  - A user request to implement a feature is NOT authorization to commit or push.
  - Before committing: verify staged files with `git diff --cached --name-status` and check for trailing whitespace with `git diff --cached --check`.
  - Never force-push (`--force`) or rewrite remote history.
  - After authorized push: verify synchronization using `git status --short --branch` and confirm HEAD matches `origin/main`.

---

## 7. Testing & Definition of Done

A task is only complete when verified by observable evidence:
- **Targeted Tests:** Run specific tests for the modified module.
- **Regression Suite:** Run the project regression gates (e.g. `scratch/test_master_regression_gate.py`).
- **Reporting:** Report exact counts: passed, failed, skipped.
- **Lint & Syntax:** Clean `git diff --check` (zero trailing whitespace, zero formatting flaws).
- **Parity Check:** SHA-256 match confirmed for the 3 HTML files if affected.
- **Android Separation:** Always distinguish build/compilation success from actual on-device physical testing. Never claim a physical device test passed unless executed and observed on the hardware.

---

## 8. Android Native Engine & Release Security

- **Android Architecture:**
  - Native Shell: `MainActivity.kt` with AndroidX WebKit asset loading (`https://appassets.androidplatform.net/assets/index.html`).
  - Alarm Engine: `AlarmReceiver.kt`, `AlarmService.kt` (`FOREGROUND_SERVICE_SPECIAL_USE`), `AlarmActivity.kt` (interactive lock-screen full-screen intent), `BootReceiver.kt`.
  - Bridge Contract: `ZatoonaBridge.kt` exposed via `@JavascriptInterface` as `window.ZatoonaNativeBridge`.
- **R8 / ProGuard Protection:**
  - Bridge methods and models must be kept from obfuscation/stripping (`-keepclassmembers class * { @android.webkit.JavascriptInterface <methods>; }` and `-keep class com.zatoona.app.ZatoonaBridge { *; }`).
  - WebView debugging must remain disabled in production release builds.
- **Keystore Security:**
  - Never commit keystore files (`*.keystore`, `*.jks`) or credentials (`keystore.properties`) to Git.
  - Ensure `.gitignore` explicitly blocks all signing artifacts.
  - Physical device reboot test remains **deferred** until user grants explicit approval.

---

## 9. Feature-Specific Requirements

1. **Exercise Media & Offline Storage:**
   - Exercise media must be stored locally (IndexedDB/CacheStorage) with file size quotas and offline validation. Never assume remote URLs work offline.
2. **Worship & Prayer Engine:**
   - Preserve city calculations, prayer reminders, custom Adhan/alarm routes, and daily checklist midnight resets.
3. **Optional Local AI Assistant:**
   - Strictly opt-in; disabled by default. No API keys hardcoded in frontend. No transmission of personal data without clear consent.
4. **Android Home-Screen Widgets:**
   - Must be implemented as native Android `AppWidgetProvider` with `RemoteViews` layouts; never confuse PWA dashboard cards with native widgets.

---

## 10. Master Acceptance Roadmap

Prioritization follows `docs/Final_Master_Plan_Acceptance_Audit.md`:
1. Repository hygiene & acceptance audit
2. Worship checklist UX, persistence & daily reset
3. Sleep & recovery tracking
4. Prayer city selection & notifications
5. Android alarms & physical-device verification
6. Gym customization & workout routines
7. Exercise encyclopedia & training plans
8. Workout execution & analytics
9. Exercise images/GIFs & offline media
10. Nutrition, meals & budget
11. Schedules, habits, notes & cross-section search
12. Unified reminders & bridge sync
13. Native Android home-screen widgets
14. Optional privacy-conscious AI
15. Integration, release readiness & device validation
16. Post-release maintenance & optimization

---

## 11. Handoff Structure

Every task concludes with a concise Egyptian Arabic handoff covering:
- **المهمة والنتيجة الفعلية (Objective & Outcome)**
- **الملفات المعدلة أو المفحوصة (Changed / Inspected Files)**
- **نتائج الاختبارات بالأرقام (Test Results with Evidence)**
- **حالة Git و HEAD (Branch, HEAD, Working Tree)**
- **الفحوصات المعلقة أو المؤجلة (Pending / Deferred Items)**
- **الخطوة التالية المحددة والأكثر أماناً (Single Best Next Action)**

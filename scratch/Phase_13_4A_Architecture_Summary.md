# Phase 13.4A — Closed-App Reminders: Executive Summary & Recommendation

**Project:** Zatoona (Personal Offline-First Progressive Web App)  
**Workspace:** `<REPOSITORY_ROOT>`  
**Date:** 2026-10-25  
**Status:** Audit Completed — Strict Read-Only  

---

## 1. Core Findings

- **The Problem:** Zatoona currently uses a JavaScript `setInterval(..., 30000)` running inside `index.html`. When the PWA is closed, the process is terminated and **no reminders can fire**.
- **Service Worker Limitation:** `sw.js` can handle notification *clicks*, but web standards do not allow a Service Worker to maintain background timers or schedule local clock-time wakeups without an active page or external push event.
- **Why Web Push was Rejected:** Web Push requires an external cloud server, breaks completely when offline/airplane mode, incurs recurring server maintenance/hosting costs, and compromises user privacy by uploading schedules to the cloud.

---

## 2. Recommended Solution: Option C (Hybrid PWA + Lightweight Native Android Shell)

1. **Keep the PWA 100% Intact:** The existing HTML/CSS/JS continues to serve as the entire user interface, data store, and offline PWA.
2. **Minimal Native Android Wrapper (`android/`):**
   - An ultra-lightweight Android project (< 300 lines of Kotlin).
   - Hosts the PWA in an Android `WebView`.
   - Exposes an explicit `@JavascriptInterface` bridge (`window.ZatoonaNativeBridge.syncUpcomingAlarms(...)`).
   - Uses Android's native `AlarmManager.setExactAndAllowWhileIdle()` to schedule alarms directly with the Linux kernel timer driver.
   - Reschedules alarms on device reboot via `BootReceiver` (`ACTION_BOOT_COMPLETED`).
   - Posts notifications via `NotificationManagerCompat` with high priority, custom sound, and deep-link intent.
   - Tapping the notification launches the app directly into the relevant section (`#prayer`, `#sleep`, `#schedule`).
3. **Synergy with Phase 13.5 (Home-Screen Widgets):**
   The native layer saves the upcoming alarm array in `SharedPreferences`, which directly feeds native Android widgets in Phase 13.5 without any architectural rework.

---

## 3. Comparison Matrix

| Criteria | Option A: Web Push | Option B: Full Native Rewrite | Option C: Hybrid Native Shell (Recommended) |
|---|:---:|:---:|:---:|
| **Closed-App Delivery** | ⚠️ Online only | ✅ 100% Offline | ✅ 100% Offline |
| **Offline Reliability** | ❌ Fails offline | ✅ 100% Local | ✅ 100% Local |
| **Server Cost / Setup** | ❌ Monthly costs | ✅ Free | ✅ Free |
| **Privacy / Zero Cloud** | ❌ Cloud sync | ✅ 100% on device | ✅ 100% on device |
| **Codebase Preservation**| ✅ 100% | ❌ Throws away PWA | ✅ 100% Preserved |
| **Android Widget Ready**| ❌ No | ✅ Yes | ✅ Yes (Phase 13.5) |

---

## 4. Current Environment & Implementation Roadmap

- **Environment State:** The local Windows machine currently has no Android SDK or Android Studio installed on PATH.
- **Phase 13.4B Staged Plan:**
  1. Add the lightweight JavaScript bridge caller (`syncNativeAlarmsBridge`) in `index.html`.
  2. Generate the minimal Android project files inside `android/`.
  3. Guide the user to open `android/` in Android Studio to build the debug APK and sideload it to their phone.
  4. Verify exact-alarm permission, reboot persistence, notification tap routing, and offline delivery.

---

## 5. Integrity Verification

- `fc.exe /b index.html zatoona.html`: **0 differences** (100% identical).
- SHA-256 for `index.html` & `zatoona.html`: `93ee85160a57fe5b72b3aadedf7926dfdda3866b431906ce863edf1dfd0b5eaf`.
- `git diff --check`: 0 errors.
- Master Test Gate: 693 / 693 checks passing across 13 suites.
- Strictly read-only audit: zero changes to production code or user data.

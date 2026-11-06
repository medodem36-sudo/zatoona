#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Master Test Gate for Zatoona Project (Phase 12.6)
=========================================================
Centralized execution harness for all verified regression and acceptance test suites.

Features:
- Discovers and executes active test suites in defined order as isolated subprocesses.
- Continues running all remaining suites upon failure to produce a full diagnostic report.
- Dynamic extraction of passed/failed check counts (no hardcoded totals).
- Captures stdout/stderr into individual log files under scratch/test-results/.
- Generates structured Markdown and JSON reports.
- Handles timeouts gracefully per suite.
- Returns exit code 0 ONLY if all active suites pass with 0 failures and 0 errors.

Usage:
    python scratch/test_master_regression_gate.py
    python scratch/test_master_regression_gate.py --list
    python scratch/test_master_regression_gate.py --suite phase9c3
    python scratch/test_master_regression_gate.py --include-superseded
"""

import sys
import os
import re
import json
import time
import datetime
import argparse
import subprocess
from pathlib import Path

# Force UTF-8 stdout/stderr encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Repository root discovery based on script location
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
RESULTS_DIR = SCRIPT_DIR / "test-results"

# Registered Test Suites in execution order
REGISTERED_SUITES = [
    {
        "id": "phase5b1_1",
        "name": "Phase 5B.1.1 Image Policy & Males-Only Compliance",
        "category": "Images & Policy",
        "rel_path": "scratch/test_phase5b1_1_image_policy.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies zero external image URLs, zero female depictions/keywords, local SVG assets, and sw.js precache."
    },
    {
        "id": "phase5b1_2",
        "name": "Phase 5B.1.2 Legacy A/B Exercise Images Compliance",
        "category": "Images & Exercises",
        "rel_path": "scratch/test_phase5b1_2_legacy_images.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Routine A/B local SVGs, user custom image priority in exercise-image-map-v1, and headless browser rendering."
    },
    {
        "id": "phase6c",
        "name": "Phase 6C Workout Analytics & Progression",
        "category": "Gym & Analytics",
        "rel_path": "scratch/test_phase6c_workout_analytics.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies session analytics, cumulative volume calculation, PR separation (weight vs rep), and SVG progression chart."
    },
    {
        "id": "phase8b",
        "name": "Phase 8B Notification Routing & Security",
        "category": "Notifications & Routing",
        "rel_path": "scratch/test_phase8b_notification_routing.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies notificationclick in sw.js, routeNotificationClick(), URL sanitization, and section whitelisting."
    },
    {
        "id": "phase9b_notes",
        "name": "Phase 9B Unified Notes Hub Core Engine",
        "category": "Notes Hub",
        "rel_path": "scratch/test_phase9b_unified_notes.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies 4 note types collection, empty records guards, timeline sorting, real-time search, filters, and attachments."
    },
    {
        "id": "phase9b1_2_gate",
        "name": "Phase 9B.1.2 Unified Notes Hub Acceptance Gate",
        "category": "Notes Hub",
        "rel_path": "scratch/test_phase9b1_2_gate.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Notes Hub acceptance criteria: ASC/DESC sort toggle, clear-all filters button, deep-linking, and read-only invariance."
    },
    {
        "id": "phase9c1",
        "name": "Phase 9C.1 Stretch & Mobility Encyclopedia",
        "category": "Stretches & Mobility",
        "rel_path": "scratch/test_phase9c1_stretch_encyclopedia.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies 34 stretch catalog entries, 34 local SVGs on disk, types and regions coverage, and UI integration."
    },
    {
        "id": "phase9c2",
        "name": "Phase 9C.2 Interactive Pre-Workout Warm-up",
        "category": "Warm-up & Flow",
        "rel_path": "scratch/test_phase9c2_warmup.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies pre-workout card, general cardio, dynamic routine targeting, warmup sets isolation, and state persistence."
    },
    {
        "id": "phase9c3",
        "name": "Phase 9C.3 Interactive Post-Workout Cool-down & Stretch",
        "category": "Cool-down & Flow",
        "rel_path": "scratch/test_phase9c3_cooldown.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies post-workout card unlocking, calm walk, 4-5 static stretches, sessionId scoping, and routine lock."
    },
    {
        "id": "phase12_1b",
        "name": "Phase 12.1B Curated Exercise Catalog Images",
        "category": "Images & Exercises",
        "rel_path": "scratch/test_phase12_1b_exercise_images.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies 19 curated exercise SVGs, 100% coverage of 26 template exercises, sw.js v24 precaching, and offline integrity."
    },
    {
        "id": "phase13_1",
        "name": "Phase 13.1 Checklist & Worship Labels Repair",
        "category": "UX & Checklists",
        "rel_path": "scratch/test_phase13_1_checklist_labels.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies renderSimpleChecklist and renderScheduleChecklist label rendering, Arabic worship labels, sleep habits labels, icons, click toggling, and layout responsiveness."
    },
    {
        "id": "phase13_worship_ux",
        "name": "Phase 13.1B Worship Checklist Visual Badges & Summary",
        "category": "UX & Worship",
        "rel_path": "scratch/test_phase13_worship_ux_badges.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies section header counter badges, thematic border accents, full 6-category prayerSummary metrics, and real-time interactive updates."
    },
    {
        "id": "phase13_2",
        "name": "Phase 13.2 Cairo Prayer Times Support",
        "category": "Prayer & Schedule",
        "rel_path": "scratch/test_phase13_2_cairo_prayer.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Cairo option in #prayerCitySelect and #scPrayerCity, PRAYER_SUPPORTED_CITIES, bidirectional sync, cache isolation, historical tracking preservation, and 375px mobile responsiveness."
    },
    {
        "id": "phase13_3",
        "name": "Phase 13.3 Healthy Sleep Habits & Bedtime Routine",
        "category": "Sleep & Recovery",
        "rel_path": "scratch/test_phase13_3_sleep_habits.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies target bedtime & wake settings, midnight crossing duration, circular diff, evening wind-down checklist, 5 core sleep habits preservation, actual vs target comparison, 7/28-day adherence summaries, reminder dispatching, and backup compatibility."
    },
    {
        "id": "phase13_habit_streaks",
        "name": "Phase 13.3B Habit Streaks Engine & Motivation Tracker",
        "category": "Habits & Streaks",
        "rel_path": "scratch/test_phase13_habit_streaks.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies shiftIsoDay calendar math, computeHabitStreaks 6-habit evaluation, home view streak pills, overview domain cards, and interactive navigation."
    },
    {
        "id": "phase13_battery_guide",
        "name": "Phase 13.5B Per-Manufacturer Battery Optimization Guide",
        "category": "Settings & Notifications",
        "rel_path": "scratch/test_phase13_battery_guide.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies OEM battery optimization guide modal, Samsung/Xiaomi/Huawei/Oppo/Pixel tabs, step-by-step Arabic instructions, and native bridge detection."
    },
    {
        "id": "phase10_encrypted_backup",
        "name": "Phase 10 Encrypted Backup Export & Import (AES-GCM)",
        "category": "Backup & Security",
        "rel_path": "scratch/test_phase10_encrypted_backup.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies PBKDF2 + AES-GCM 256-bit backup encryption, password protection, unencrypted backward compatibility, and error handling."
    },
    {
        "id": "phase13_fasting",
        "name": "Phase 13.6B Fasting Tracker & Sunnah Days",
        "category": "Worship & Fasting",
        "rel_path": "scratch/test_phase13_fasting_tracker.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies voluntary, sunnah, and qadaa fasting logging, monthly fasting counts, and Monday/Thursday sunnah alerts."
    },
    {
        "id": "phase13_worship_adherence",
        "name": "Phase 13.7B Weekly & Monthly Worship Adherence Report",
        "category": "Worship & Analytics",
        "rel_path": "scratch/test_phase13_worship_adherence.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies 7/28-day window adherence stats, per-prayer breakdown, multi-pillar tracking (Qiyam, Fasting, Quran, Azkar), and Overview integration."
    },
    {
        "id": "phase13_qibla_compass",
        "name": "Phase 13.8B Prayer Qibla Compass Engine & Dial",
        "category": "Worship & Compass",
        "rel_path": "scratch/test_phase13_qibla_compass.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies spherical trigonometry math, distance calculation, offline cities, SVG compass dial, live orientation, and Kaaba alignment."
    },
    {
        "id": "phase13_habits_and_share",
        "name": "Phase 13.9 Custom Habits & Learning Tracker + Share Card",
        "category": "Habits & Productivity",
        "rel_path": "scratch/test_phase13_habits_and_share.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies custom habits and skills learning tracker, habit streaks, daily checkoffs, and daily summary social accountability share card."
    },
    {
        "id": "phase13_smart_notification_grouping",
        "name": "Phase 13.10 Smart Notification Grouping (Proposal #14)",
        "category": "Notifications & UX",
        "rel_path": "scratch/test_phase13_smart_notification_grouping.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies smart notification grouping: concurrent reminders batched into unified digest, settings toggle, deduplication, in-app modal, Android group constants, and backup key patterns."
    },
    {
        "id": "phase13_4b1",
        "name": "Phase 13.4B1 Isolated Native Android Shell Foundation",
        "category": "Native Android & Bridge",
        "rel_path": "scratch/test_phase13_4b1_scaffold.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies toolchain preflight, SOURCE_SCAFFOLD_ONLY status, android/ scaffold integrity, security settings (cleartext disabled, file access restricted), versioned ZatoonaBridge contract (v1), WebViewAssetLoader origin, and PWA storage invariance."
    },
    {
        "id": "phase13_4b1_2",
        "name": "Phase 13.4B1.2 Android Toolchain & Buildability Verification",
        "category": "Native Android & Build",
        "rel_path": "scratch/test_phase13_4b1_2_android_buildability.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies JDK 17, Android SDK 34, Gradle 8.5, real APK compilation & assembly (app-debug.apk), packaged PWA assets, and device/emulator diagnostics."
    },
    {
        "id": "phase13_4b2",
        "name": "Phase 13.4B2 Native Android Local Alarm Engine",
        "category": "Native Android & Alarms",
        "rel_path": "scratch/test_phase13_4b2_alarms.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies native AlarmManager scheduling, boot/time receivers, notification channels, ZatoonaBridge v2 sync, recurrence math, city isolation, PWA bridge integration, and debug APK packaging."
    },
    {
        "id": "phase14_release_signing",
        "name": "Phase 14 Release Signing Configuration Template",
        "category": "Build & Release Security",
        "rel_path": "scratch/test_phase14_release_signing.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies release signing configuration in build.gradle.kts, keystore.properties.example template, .gitignore guards against secrets, ProGuard R8 rules, and debug APK buildability."
    },
    {
        "id": "phase13_5_widgets",
        "name": "Phase 13.5 Native Android Quick Access Widget (Proposal #7)",
        "category": "Native Android & Widgets",
        "rel_path": "scratch/test_phase13_5_widgets.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies native AppWidgetProvider registration, RemoteViews XML layouts, localized Arabic strings, click PendingIntents for 4 core modules, ProGuard rules, and APK packaging."
    },
    {
        "id": "phase13_5_next_prayer_widget",
        "name": "Phase 13.5 Next Prayer Home-Screen Widget (Proposal #8)",
        "category": "Native Android & Widgets",
        "rel_path": "scratch/test_phase13_5_next_prayer_widget.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies NextPrayerWidgetProvider, XML RemoteViews, Arabic prayer countdown math, ZatoonaBridge cache sync, ProGuard keep rules, and APK packaging."
    },
    {
        "id": "phase13_items_1_and_3",
        "name": "Phase 13.5 Daily Habits Widget (Proposal #9) & Phase 13.7 Privacy-Conscious Local AI",
        "category": "Widgets & Local AI",
        "rel_path": "scratch/test_phase13_items_1_and_3.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies DailyHabitsWidgetProvider, RemoteViews layout and slots, PWA habits bridge sync, and Phase 13.7 opt-in local AI coach offline analysis."
    },
    {
        "id": "phase13_6_pantry",
        "name": "Phase 13.6 Pantry & Food Inventory Management",
        "category": "Nutrition & Pantry",
        "rel_path": "scratch/test_phase13_6_pantry_inventory.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Pantry & Food Inventory storage, deficit tracking, expiry warnings, smart transfer from shopping, and backup validation."
    },
    {
        "id": "phase1_ui_ergonomics",
        "name": "Phase 1 UI Ergonomics, AMOLED Theme & Dashboard Engine",
        "category": "UI & Ergonomics",
        "rel_path": "scratch/test_phase1_ui_ergonomics.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies AMOLED theme, custom accent colors, large font scaling, compact dashboard mode, dashboard cards reordering, morning briefing card, haptic feedback, and interactive water logging."
    },
    {
        "id": "phase2_study_hub",
        "name": "Phase 2 Study Hub, Spaced Repetition & Deep Focus Engine",
        "category": "Study & Learning",
        "rel_path": "scratch/test_phase2_study_hub.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies independent #studyView, SM-2 flashcard spaced repetition, Pomodoro & Flowmodoro timers, Web Audio offline ambient focus sounds, distraction parking lot, hardcore deep focus fullscreen mode, exam countdown with syllabus progress, Ebbinghaus active recall review planner, Feynman notebook, Cornell notes, vocab bank with random quiz, reading speed estimator, and 100-Hour focus challenge."
    },
    {
        "id": "phase3_gym_engine",
        "name": "Phase 3 Next-Gen Gym & Strength Engine",
        "category": "Gym & Strength",
        "rel_path": "scratch/test_phase3_gym_engine.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies 1RM/RPE calculator, smart warmup sets and plate loader, live exercise swap for busy machines, blacklist exercises manager, muscle recovery heatmap with SVG body map, gym big-numbers focus mode, tempo cadence metronome, injury/pain flagging, and ongoing workout floating HUD with notification bridge."
    },
    {
        "id": "phase4_nutrition_engine",
        "name": "Phase 4 Smart Nutrition, Pantry & Budget Engine",
        "category": "Nutrition & Budget",
        "rel_path": "scratch/test_phase4_nutrition_engine.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies smart pantry meal suggestions (أطبخ إيه من المؤن المتاحة؟), Egyptian athlete protein-to-cost calculator, quick-add favorite meal combos, smart carb cycling synced with gym rest/training days, weekly cumulative caloric deficit tracking, sodium-potassium balance indicator, and remaining daily spending allowance in budget view."
    },
    {
        "id": "phase5_worship_engine",
        "name": "Phase 5 Worship & Smart Khatma Engine",
        "category": "Worship & Khatma",
        "rel_path": "scratch/test_phase5_worship_engine.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies smart Khatma progress & Quran reflection notebook, dynamic Suhoor & pre-Fajr alarm, pre-Adhan preparation chime, forbidden prayer times live indicator & windows, Friday Sunan interactive checklist with Salawat counter, subtle random Dhikr treasury & interval reminder, and missed prayers & fasting debt ledger."
    },
    {
        "id": "phase6_sleep_life_os",
        "name": "Phase 6 Advanced Sleep & Life OS",
        "category": "Sleep & Life OS",
        "rel_path": "scratch/test_phase6_sleep_life_os.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies 90-minute sleep cycle calculator, 20-minute power nap smart timer, self-reported screen-free bedtime tracker, sedentary desk break chime, Eisenhower Matrix 4-quadrant view, critical task top pinning, one-tap clear completed archive, and habit vacation freeze & smart safar mode."
    },
    {
        "id": "phase7_system_polish",
        "name": "Phase 7 System Polish & Zatoona Wrapped",
        "category": "System Polish & Android",
        "rel_path": "scratch/test_phase7_system_polish.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Android native study widget, quick settings tiles, automated local backup reminders, and monthly/annual Zatoona Wrapped."
    },
    {
        "id": "package_a_gym_intelligence",
        "name": "Package A Gym Intelligence Engine",
        "category": "Gym Intelligence",
        "rel_path": "scratch/test_package_a_gym_intelligence.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Plateau Detector, Push/Pull/Legs weekly balance ratio bar, copy last workout weights, and home workout bodyweight converter."
    },
    {
        "id": "package_b_smart_nutrition",
        "name": "Package B Smart Nutrition Engine",
        "category": "Smart Nutrition",
        "rel_path": "scratch/test_package_b_smart_nutrition.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Cheat Day Recovery Calculator, Complete vs Incomplete Protein quality analyzer, and Egyptian Popular Food Guide."
    },
    {
        "id": "package_c_worship_sunnah",
        "name": "Package C Worship & Sunnah Engine",
        "category": "Worship & Sunnah",
        "rel_path": "scratch/test_package_c_worship_sunnah.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Gradual Fajr Alarm, Friday Special Package, Adhkar Auto-hide, Missed Prayer Qada Calculator, Astronomical Last Third of Night, Sunnah Rawatib 12-Rak'ah Tracker, Silent Istighfar Nudge, and Suhoor Fasting Alert."
    },
    {
        "id": "package_d_budget_savings",
        "name": "Package D Budget & Savings Engine",
        "category": "Budget & Savings",
        "rel_path": "scratch/test_package_d_budget_savings.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Recurring Bills & Subscriptions Detector, Virtual Savings Jars & Goals, and Daily Allowance Calculator."
    },
    {
        "id": "package_e_schedule_tasks",
        "name": "Package E Schedule, Tasks, Sleep & Study Engine",
        "category": "Schedule & Tasks",
        "rel_path": "scratch/test_package_e_schedule_tasks.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Morning Sunlight Logger, Stop Fluids Reminder, Mandatory Stretch Break, Visual Time-Blocking, Task Carry-Over, Estimated vs Actual Time, Subtasks Tree, Complex Recurring Tasks, Time-to-Leave Alert, and Conflict Detector."
    },
    {
        "id": "package_f_notes_android",
        "name": "Package F Notes & Android Features Engine",
        "category": "Notes & Android",
        "rel_path": "scratch/test_package_f_notes_android.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Pin & Color Notes, Checklist Mode, LED Flash Alert with Alarm, Wake Lock Toggle, Custom Haptic Patterns, All-in-One Daily Widget, and AMOLED Ultra-Battery Saver Mode."
    },
    {
        "id": "package_g_fluid_ux",
        "name": "Package G Fluid UX, Gestures & Speed Engine",
        "category": "UI & Ergonomics",
        "rel_path": "scratch/test_package_g_fluid_ux.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Swipe-to-Action Gestures on Cards, Horizontal View-Pager Swipe Navigation, Shared Element Morphing, Egyptian Arabic Natural Language Quick-Add, Dynamic Mini-Status Capsule Island, Collapsible Sticky Header, Contextual Pull-to-Refresh, Dismiss Keyboard on Scroll, Accordion Fold/Unfold, Spotlight Dimming, Pinch-to-Zoom Font Scale, Border Inset Aura Glow, and Time-Aware Adaptive Dashboard."
    },
    {
        "id": "phase15_hair_supplements",
        "name": "Phase 15 Limitless Man Max & Men's Hair Care & Health Tools Suite",
        "category": "Nutrition, Grooming & Health Tools",
        "rel_path": "scratch/test_phase15_hair_supplements_suite.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Limitless Man Max blue supplement with 26 vitamins and minerals RDA breakdown, toggleable active routine, Men's Hair & Grooming routine (Minoxidil 2x, Acretin 2-3 days, Dermaroller 7-10 days, adherence report and 14-day matrix), US Navy Fat Calculator, Cost per Protein Gram Calculator, Sunan of Sleep, Vitamin D3 Egyptian Sun, 20-20-20 Eye Rest, Red Shift, and Life Balance Wheel."
    },
    {
        "id": "phase16_ui_cleanup_perf",
        "name": "Phase 16 UI Cleanup, Zen Mode & Performance Acceleration Engine",
        "category": "UI & Ergonomics",
        "rel_path": "scratch/test_phase16_ui_cleanup_perf.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Zen / Essential Focus Mode toggle (#1), smart contextual collapse for completed items (#2), unified collapsible details accordions (#4), lazy DOM content-visibility rendering (#5), debounced localStorage batching (#7), and 60fps hardware acceleration with zero tap delay (#8)."
    },
    {
        "id": "phase17_reorganization",
        "name": "Phase 17 UI Reorganization, Floating Bottom Nav & Segmented Sub-Tabs",
        "category": "UI & Navigation",
        "rel_path": "scratch/test_phase17_reorganization_suite.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies 5-Hub Persistent Floating Bottom Nav, One-Tap Quick Action pills (Water, Limitless Man, Minoxidil), Pillar Segmented Sub-Tabs (Meal, Prayer, Schedule), and daily Life Balance status."
    },
    # Superseded / Obsolete historical gates (excluded by default, enabled via --include-superseded)
    {
        "id": "phase9b1_1_gate",
        "name": "Phase 9B.1.1 Interim Notes Gate (Superseded)",
        "category": "Historical / Obsolete",
        "rel_path": "scratch/test_phase9b1_1_gate.py",
        "timeout_sec": 120,
        "active": False,
        "description": "Interim Phase 9B.1.1 gate superseded by Phase 9B.1.2. Fails legitimately due to hardcoded check for CACHE_VERSION == 'v20' (current is v23)."
    }
]


def get_git_info(repo_dir: Path) -> dict:
    """Extract Git branch and commit info safely without failing."""
    info = {"commit": "unknown", "branch": "unknown", "clean": False}
    # Try finding git executable (check GitHub Desktop or system git)
    git_paths = [
        "git",
        r"C:\Users\Lenovo\AppData\Local\GitHubDesktop\app-3.6.7\resources\app\git\cmd\git.exe"
    ]
    git_cmd = None
    for gp in git_paths:
        try:
            r = subprocess.run([gp, "--version"], capture_output=True, text=True, cwd=str(repo_dir))
            if r.returncode == 0:
                git_cmd = gp
                break
        except Exception:
            continue

    if not git_cmd:
        return info

    try:
        r = subprocess.run([git_cmd, "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=str(repo_dir))
        if r.returncode == 0:
            info["commit"] = r.stdout.strip()
        r = subprocess.run([git_cmd, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, cwd=str(repo_dir))
        if r.returncode == 0:
            info["branch"] = r.stdout.strip()
        r = subprocess.run([git_cmd, "status", "--porcelain"], capture_output=True, text=True, cwd=str(repo_dir))
        if r.returncode == 0:
            lines = [l for l in r.stdout.splitlines() if not l.strip().startswith("??")]
            info["clean"] = (len(lines) == 0)
    except Exception:
        pass
    return info


def parse_suite_output(stdout_text: str, stderr_text: str) -> dict:
    """
    Parse test output to dynamically extract passed, failed, and total check counts.
    Never fabricates counts or assumes exit code 0 implies a specific number.
    """
    combined = stdout_text + "\n" + stderr_text

    # Pattern A: "PHASE X RESULTS: N PASSED, M FAILED (TOTAL T)" or "RESULTS: N PASSED, M FAILED"
    m_res = re.findall(r"(?:PHASE\s+[\w\.]+\s+)?(?:ACCEPTANCE\s+|CLOSURE\s+GATE\s+AUDIT\s+)?RESULTS:\s*(\d+)\s*PASSED,\s*(\d+)\s*FAILED(?:\s*\(TOTAL\s*(\d+)\))?", combined)
    if m_res:
        last_match = m_res[-1]
        p = int(last_match[0])
        f = int(last_match[1])
        t = int(last_match[2]) if last_match[2] else (p + f)
        return {
            "has_counts": True,
            "passed": p,
            "failed": f,
            "total": t,
            "pattern": "regex_results_line"
        }

    # Pattern B: unittest output "Ran N tests in Xs\n\n(OK|FAILED (failures=X, errors=Y))"
    m_unittest = re.search(r"Ran\s+(\d+)\s+tests\s+in\s+[\d\.]+s\s*\n\n(OK|FAILED(?:\s*\((.*?)\))?)", combined)
    if m_unittest:
        total = int(m_unittest.group(1))
        status_word = m_unittest.group(2)
        if status_word.startswith("OK"):
            return {
                "has_counts": True,
                "passed": total,
                "failed": 0,
                "total": total,
                "pattern": "unittest_ok"
            }
        else:
            details = m_unittest.group(3) or ""
            failures = 0
            errors = 0
            mf = re.search(r"failures=(\d+)", details)
            if mf:
                failures = int(mf.group(1))
            me = re.search(r"errors=(\d+)", details)
            if me:
                errors = int(me.group(1))
            failed_total = failures + errors
            passed = max(0, total - failed_total)
            return {
                "has_counts": True,
                "passed": passed,
                "failed": failed_total,
                "total": total,
                "pattern": "unittest_failed"
            }

    # Pattern C: Fallback check count from individual [PASS] and [FAIL] lines
    pass_lines = len(re.findall(r"^\s*\[PASS\]", combined, re.MULTILINE))
    fail_lines = len(re.findall(r"^\s*\[FAIL\]", combined, re.MULTILINE))
    if pass_lines > 0 or fail_lines > 0:
        return {
            "has_counts": True,
            "passed": pass_lines,
            "failed": fail_lines,
            "total": pass_lines + fail_lines,
            "pattern": "pass_fail_tags"
        }

    # Counts could not be extracted with high confidence
    return {
        "has_counts": False,
        "passed": 0,
        "failed": 0,
        "total": 0,
        "pattern": "none"
    }


def execute_suite(suite: dict, results_dir: Path, repo_root: Path) -> dict:
    """Execute a single test suite as a separate subprocess and capture telemetry."""
    suite_id = suite["id"]
    script_path = repo_root / suite["rel_path"]

    result = {
        "id": suite_id,
        "name": suite["name"],
        "category": suite["category"],
        "rel_path": suite["rel_path"],
        "status": "PENDING",
        "exit_code": None,
        "duration_sec": 0.0,
        "has_counts": False,
        "passed_checks": 0,
        "failed_checks": 0,
        "total_checks": 0,
        "stdout_log": None,
        "stderr_log": None,
        "error_message": None
    }

    if not script_path.exists():
        result["status"] = "ERROR"
        result["error_message"] = f"Test script file not found at: {script_path}"
        return result

    stdout_file = results_dir / f"{suite_id}.stdout.log"
    stderr_file = results_dir / f"{suite_id}.stderr.log"
    result["stdout_log"] = str(stdout_file.relative_to(repo_root))
    result["stderr_log"] = str(stderr_file.relative_to(repo_root))

    t_start = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=suite.get("timeout_sec", 120)
        )
        t_elapsed = time.time() - t_start
        result["duration_sec"] = round(t_elapsed, 2)
        result["exit_code"] = proc.returncode

        # Write log files
        with open(stdout_file, "w", encoding="utf-8") as f:
            f.write(proc.stdout)
        with open(stderr_file, "w", encoding="utf-8") as f:
            f.write(proc.stderr)

        counts = parse_suite_output(proc.stdout, proc.stderr)
        result["has_counts"] = counts["has_counts"]
        result["passed_checks"] = counts["passed"]
        result["failed_checks"] = counts["failed"]
        result["total_checks"] = counts["total"]

        if proc.returncode == 0 and counts["failed"] == 0:
            result["status"] = "PASS"
        else:
            result["status"] = "FAIL"
            if counts["failed"] > 0:
                result["error_message"] = f"{counts['failed']} test checks failed in output"
            else:
                result["error_message"] = f"Process exited with non-zero exit code {proc.returncode}"

    except subprocess.TimeoutExpired as te:
        t_elapsed = time.time() - t_start
        result["duration_sec"] = round(t_elapsed, 2)
        result["status"] = "TIMEOUT"
        result["exit_code"] = -1
        result["error_message"] = f"Execution timed out after {suite.get('timeout_sec', 120)} seconds"
        with open(stdout_file, "w", encoding="utf-8") as f:
            f.write(te.stdout or "(timeout before stdout captured)")
        with open(stderr_file, "w", encoding="utf-8") as f:
            f.write(te.stderr or f"TimeoutExpired after {suite.get('timeout_sec', 120)}s")

    except Exception as ex:
        t_elapsed = time.time() - t_start
        result["duration_sec"] = round(t_elapsed, 2)
        result["status"] = "ERROR"
        result["exit_code"] = -2
        result["error_message"] = f"Exception during execution: {str(ex)}"
        with open(stderr_file, "w", encoding="utf-8") as f:
            f.write(str(ex))

    return result


def generate_markdown_report(report_data: dict) -> str:
    """Generate comprehensive Markdown report from execution data."""
    lines = []
    lines.append("# Zatoona — Unified Master Test Gate Execution Report")
    lines.append("")
    lines.append(f"> **Overall Status:** `{'PASS ✅' if report_data['overall_pass'] else 'FAIL ❌'}`  ")
    lines.append(f"> **Timestamp:** `{report_data['timestamp']}`  ")
    lines.append(f"> **Git Info:** Commit `{report_data['git']['commit']}` (Branch: `{report_data['git']['branch']}`)  ")
    lines.append(f"> **Python Version:** `{report_data['python_version']}`  ")
    lines.append(f"> **Total Execution Time:** `{report_data['total_duration_sec']}s`  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"- **Total Suites Executed:** {report_data['suites_executed']}")
    lines.append(f"- **Suites Passed:** {report_data['suites_passed']}")
    lines.append(f"- **Suites Failed / Error / Timeout:** {report_data['suites_failed']}")
    lines.append(f"- **Suites Skipped / Superseded:** {report_data['suites_skipped']}")
    lines.append(f"- **Total Verifiable Checks Passed:** **{report_data['total_checks_passed']}**")
    lines.append(f"- **Total Verifiable Checks Failed:** **{report_data['total_checks_failed']}**")
    lines.append(f"- **Total Checks Evaluated:** **{report_data['total_checks_passed'] + report_data['total_checks_failed']}**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Test Suite Results Matrix")
    lines.append("")
    lines.append("| Suite ID | Suite Name | Category | Status | Checks (P/F/T) | Duration | Exit Code | Stdout Log |")
    lines.append("| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |")
    for s in report_data["suites"]:
        st = s["status"]
        badge = "✅ PASS" if st == "PASS" else ("❌ FAIL" if st == "FAIL" else f"⚠️ {st}")
        counts = f"{s['passed_checks']}/{s['failed_checks']}/{s['total_checks']}" if s["has_counts"] else "N/A"
        stdout_link = f"[`log`]({s['stdout_log']})" if s["stdout_log"] else "-"
        lines.append(f"| `{s['id']}` | **{s['name']}** | {s['category']} | {badge} | `{counts}` | `{s['duration_sec']}s` | `{s['exit_code']}` | {stdout_link} |")
    lines.append("")

    if report_data["suites_failed"] > 0:
        lines.append("---")
        lines.append("")
        lines.append("## 3. Diagnostic Details for Failed / Error Suites")
        lines.append("")
        for s in report_data["suites"]:
            if s["status"] != "PASS":
                lines.append(f"### ❌ {s['name']} (`{s['id']}`)")
                lines.append(f"- **Status:** `{s['status']}` (Exit code: `{s['exit_code']}`)")
                lines.append(f"- **Script:** `{s['rel_path']}`")
                lines.append(f"- **Error Summary:** {s.get('error_message') or 'Check logs'}")
                lines.append(f"- **Logs:** [`stdout`]({s['stdout_log']}) | [`stderr`]({s['stderr_log']})")
                lines.append("")

    if report_data["skipped_suites"]:
        lines.append("---")
        lines.append("")
        lines.append("## 4. Skipped / Superseded Suites")
        lines.append("")
        for sk in report_data["skipped_suites"]:
            lines.append(f"- **`{sk['id']}` — {sk['name']}:** {sk['description']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 5. Baseline Reconciliation")
    lines.append("")
    lines.append("- Previous audit result recorded in `Final_Master_Plan_Reconciliation_v3.md`: **497 / 497 checks passed** across the 9 approved suites.")
    lines.append(f"- Current master gate execution result: **{report_data['total_checks_passed']} / {report_data['total_checks_passed'] + report_data['total_checks_failed']} checks passed**.")
    if report_data['total_checks_passed'] == 497 and report_data['total_checks_failed'] == 0:
        lines.append("- **Verification:** Current live execution matches the 497 baseline exactly with 100% fidelity.")
    else:
        diff = report_data['total_checks_passed'] - 497
        lines.append(f"- **Verification Note:** Difference from 497 baseline is {diff:+d} checks.")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Zatoona Unified Master Test Gate (Phase 12.6)")
    parser.add_argument("--list", action="store_true", help="List all registered test suites without executing")
    parser.add_argument("--suite", type=str, help="Run only a specific suite by ID (e.g. --suite phase9c3)")
    parser.add_argument("--include-superseded", action="store_true", help="Include obsolete/superseded test suites")
    parser.add_argument("--json", action="store_true", help="Print JSON report summary to stdout")
    args = parser.parse_args()

    # Create results directory
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.list:
        print("\nRegistered Test Suites in Unified Master Test Gate:")
        print("=" * 80)
        for s in REGISTERED_SUITES:
            active_str = "ACTIVE" if s["active"] else "SUPERSEDED"
            print(f"[{active_str:10s}] {s['id']:18s} | {s['name']}")
            print(f"             Path: {s['rel_path']}")
            print(f"             Desc: {s['description']}\n")
        sys.exit(0)

    # Determine which suites to run
    suites_to_run = []
    skipped_suites = []

    for s in REGISTERED_SUITES:
        if args.suite and s["id"].lower() != args.suite.lower():
            continue
        if not s["active"] and not args.include_superseded and not args.suite:
            skipped_suites.append(s)
            continue
        suites_to_run.append(s)

    if not suites_to_run:
        print(f"ERROR: No test suites found matching criteria (suite filter: {args.suite})", file=sys.stderr)
        sys.exit(2)

    git_info = get_git_info(REPO_ROOT)
    t_start_total = time.time()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 80)
    print("ZATOONA UNIFIED MASTER TEST GATE (PHASE 12.6)")
    print("=" * 80)
    print(f"Timestamp    : {now_str}")
    print(f"Repository   : {REPO_ROOT}")
    print(f"Git Commit   : {git_info['commit']} (Branch: {git_info['branch']})")
    print(f"Python       : {sys.version.split()[0]}")
    print(f"Suites to run: {len(suites_to_run)}")
    print("-" * 80)

    executed_results = []
    for idx, suite in enumerate(suites_to_run, 1):
        print(f"[{idx:2d}/{len(suites_to_run):2d}] Running: {suite['name']} ...", end=" ", flush=True)
        res = execute_suite(suite, RESULTS_DIR, REPO_ROOT)
        executed_results.append(res)
        if res["status"] == "PASS":
            counts_str = f"({res['passed_checks']} checks)" if res["has_counts"] else ""
            print(f"PASS {counts_str} in {res['duration_sec']}s")
        elif res["status"] == "FAIL":
            counts_str = f"({res['passed_checks']} passed, {res['failed_checks']} failed)" if res["has_counts"] else ""
            print(f"FAIL {counts_str} in {res['duration_sec']}s")
        else:
            print(f"{res['status']} in {res['duration_sec']}s: {res.get('error_message')}")

    total_duration = round(time.time() - t_start_total, 2)
    suites_passed = sum(1 for r in executed_results if r["status"] == "PASS")
    suites_failed = sum(1 for r in executed_results if r["status"] != "PASS")
    total_checks_passed = sum(r["passed_checks"] for r in executed_results)
    total_checks_failed = sum(r["failed_checks"] for r in executed_results)
    overall_pass = (suites_failed == 0 and len(executed_results) > 0)

    report_data = {
        "timestamp": now_str,
        "repo_root": str(REPO_ROOT),
        "git": git_info,
        "python_version": sys.version.split()[0],
        "overall_pass": overall_pass,
        "total_duration_sec": total_duration,
        "suites_executed": len(executed_results),
        "suites_passed": suites_passed,
        "suites_failed": suites_failed,
        "suites_skipped": len(skipped_suites),
        "total_checks_passed": total_checks_passed,
        "total_checks_failed": total_checks_failed,
        "suites": executed_results,
        "skipped_suites": skipped_suites
    }

    # Save JSON Report
    json_path = RESULTS_DIR / "test_master_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    # Save Markdown Report
    md_content = generate_markdown_report(report_data)
    md_path = RESULTS_DIR / "test_master_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print("-" * 80)
    print("GATE SUMMARY:")
    print(f"  Overall Status : {'PASS ✅' if overall_pass else 'FAIL ❌'}")
    print(f"  Suites Passed  : {suites_passed} / {len(executed_results)}")
    print(f"  Checks Passed  : {total_checks_passed} / {total_checks_passed + total_checks_failed}")
    print(f"  Total Duration : {total_duration}s")
    print(f"  Markdown Report: {md_path.relative_to(REPO_ROOT)}")
    print(f"  JSON Report    : {json_path.relative_to(REPO_ROOT)}")
    print("=" * 80)

    if args.json:
        print(json.dumps(report_data, indent=2, ensure_ascii=False))

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()

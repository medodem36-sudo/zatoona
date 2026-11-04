# -*- coding: utf-8 -*-
import os
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Catalog of domains and their features
domains = {
    "1. Worship & Prayer Engine": [
        {"name": "Cairo/Egypt Prayer Times Calculation", "id": "prayerCard", "func": "calculatePrayerTimes", "storage": "prayer-city"},
        {"name": "Worship Checklist & Reset", "id": "prayerChecklistCard", "func": "resetPrayerChecklistIfNewDay", "storage": "checklist-date"},
        {"name": "Forbidden Prayer Times Indicator", "id": "forbiddenTimesCard", "func": "updateForbiddenPrayerTimes", "storage": "none"},
        {"name": "Missed Worship Ledger (Qada)", "id": "missedWorshipCard", "func": "updateMissedWorshipUI", "storage": "worship-missed-ledger-v1"},
        {"name": "Friday Sunan & Salawat Counter", "id": "fridaySunanCard", "func": "incrementSalawat", "storage": "worship-friday-sunan"},
        {"name": "Dynamic Suhoor & Pre-Fajr Alarm", "id": "suhoorQiyamCard", "func": "updateSuhoorAlarmUI", "storage": "worship-suhoor-settings-v1"},
        {"name": "Pre-Adhan Reminder Chime", "id": "preAdhanChimeCard", "func": "savePreAdhanSettings", "storage": "worship-preadhan-settings-v1"},
        {"name": "Random Dhikr Treasury", "id": "randomDhikrCard", "func": "refreshRandomDhikr", "storage": "worship-random-dhikr-v1"},
        {"name": "Smart Khatma & Quran Reflection", "id": "khatmaCard", "func": "saveKhatmaState", "storage": "khatma-state-v1"},
        {"name": "Fasting Tracker & Sunnah Days", "id": "fastingCard", "func": "saveFasting", "storage": "fasting:"},
        {"name": "Qibla Compass Engine", "id": "qiblaCard", "func": "calculateQibla", "storage": "none"},
        {"name": "Worship Adherence Analytics", "id": "worshipReportCard", "func": "renderWorshipAdherenceSummary", "storage": "checklist-date"}
    ],
    "2. Sleep & Recovery Life OS": [
        {"name": "90-Minute Sleep Cycle Alarm Calculator", "id": "sleepCycleCalcCard", "func": "calculateSleepCycles", "storage": "none"},
        {"name": "20-Minute Power Nap Smart Timer", "id": "powerNapCard", "func": "toggleNapTimer", "storage": "nap-timer-state"},
        {"name": "Screen-Free Bedtime Compliance Tracker", "id": "screenFreeBedtimeCard", "func": "toggleScreenFreeBedtime", "storage": "zatoona-screen-free-log-v1"},
        {"name": "Sedentary Desk Break Chime", "id": "deskBreakCard", "func": "toggleDeskBreakChime", "storage": "zatoona-desk-break-settings-v1"},
        {"name": "Caffeine & Fluid Stop Cutoff Timer", "id": "stopFluidsCard", "func": "calculateStopFluidsCutoff", "storage": "sleep-routine-settings"},
        {"name": "Morning Sunlight Exposure Timer", "id": "sunlightCard", "func": "startSunlightTimer", "storage": "sleep-routine-settings"},
        {"name": "Habit Vacation Freeze & Smart Safar Mode", "id": "safarModeBanner", "func": "toggleSmartSafarMode", "storage": "zatoona-smart-safar-mode-v1"},
        {"name": "Sleep Habit Streaks & Motivation", "id": "habitStreaksCard", "func": "calculateHabitStreak", "storage": "sleep-habits-streaks"}
    ],
    "3. Gym & Exercise Intelligence": [
        {"name": "Smart Warm-up Progression Calculator", "id": "gymWarmupModal", "func": "renderWarmupProgression", "storage": "gym-warmup-state-v1"},
        {"name": "Plate Loader Visual Calculator", "id": "gymPlateLoaderCard", "func": "calculatePlateBreakdown", "storage": "none"},
        {"name": "Live Exercise Swap ('الجهاز مشغول؟')", "id": "gymExerciseSwapModal", "func": "openExerciseSwapModal", "storage": "none"},
        {"name": "1RM & RPE/RIR Adjustment Table", "id": "gym1RMCalcModal", "func": "calculate1RM", "storage": "gym-1rm-history-v1"},
        {"name": "Deload Week Smart Planner", "id": "gymDeloadCard", "func": "planDeloadWeek", "storage": "gym-deload-settings-v1"},
        {"name": "Blacklist Excluded Exercises Manager", "id": "gymBlacklistModal", "func": "toggleExcludeExercise", "storage": "gym-blacklist-v1"},
        {"name": "Muscle Recovery Anatomical Heatmap", "id": "gymRecoveryHeatmapModal", "func": "renderMuscleRecoveryHeatmap", "storage": "gym-sessions-v1"},
        {"name": "Gym Big-Numbers Focus Overlay & HUD", "id": "gymFocusOverlay", "func": "openGymFocusMode", "storage": "none"},
        {"name": "Tempo Cadence Metronome", "id": "gymTempoModal", "func": "startTempoMetronome", "storage": "gym-tempo-settings-v1"},
        {"name": "Joint & Muscle Pain Flagging", "id": "gymPainTrackerModal", "func": "savePainFlag", "storage": "gym-pain-flags-v1"},
        {"name": "Exercise Encyclopedia with Offline Caching", "id": "encDetailView", "func": "renderExerciseDetails", "storage": "exercise-image-map-v1"}
    ],
    "4. Nutrition & Budget Engine": [
        {"name": "Sodium-to-Potassium Balance Indicator", "id": "sodiumPotassiumCard", "func": "calculateSodiumPotassiumRatio", "storage": "meals:"},
        {"name": "Safe Meal Daily Spending Allowance", "id": "dailyAllowanceCard", "func": "calculateBudgetDailyAllowance", "storage": "budget-"},
        {"name": "Smart Water Intake Recommendation Engine", "id": "waterCard", "func": "calculateOptimalWaterIntake", "storage": "water:"},
        {"name": "Glycemic Load & Carb Cycling Planner", "id": "carbCyclingModal", "func": "openCarbCyclingModal", "storage": "nutrition-carb-cycling"},
        {"name": "Protein-to-Cost Egyptian Food Index", "id": "proteinCostCalcModal", "func": "openProteinCostCalc", "storage": "nutrition-protein-cost"},
        {"name": "Smart Pantry Zero-Waste Suggestions", "id": "pantryMealSuggestionsModal", "func": "openPantrySuggestions", "storage": "pantry-inventory-v1"},
        {"name": "Quick-Add Favorite Meal Combos", "id": "favoriteCombosModal", "func": "openFavoriteCombos", "storage": "nutrition-favorite-combos"},
        {"name": "Recurring Expenses & Subscription Tracker", "id": "budgetSubscriptionsCard", "func": "renderUpcomingSubscriptionsUI", "storage": "budget-subscriptions-v1"},
        {"name": "Savings Goals Visual Progress Rings", "id": "budgetSavingsGoalsCard", "func": "renderSavingsGoalsUI", "storage": "budget-savings-goals-v1"}
    ],
    "5. Schedules, Habits & Life Productivity": [
        {"name": "Eisenhower Matrix 4-Quadrant Categorization", "id": "eisenhowerMatrixCard", "func": "updateTaskQuadrant", "storage": "zatoona-eisenhower-map-v1"},
        {"name": "Top 3 Critical Needle-Moving Task Pinning", "id": "pinnedTasksBox", "func": "togglePinTask", "storage": "zatoona-pinned-tasks-v1"},
        {"name": "One-Tap Clear / Archive Completed Tasks", "id": "btnArchiveCompletedTasks", "func": "archiveCompletedScheduleTasks", "storage": "zatoona-archived-schedule-tasks-v1"},
        {"name": "Dynamic Daily Timeline & Visual Time Blocks", "id": "scheduleTimelineBox", "func": "renderVisualTimeBlocks", "storage": "sched-acts:"},
        {"name": "Custom Habits & Shareable Card Generator", "id": "customHabitsCard", "func": "addCustomHabit", "storage": "custom-habits-list"},
        {"name": "Per-Manufacturer Battery Optimization Guide", "id": "batteryGuideModal", "func": "openBatteryGuideModal", "storage": "none"}
    ],
    "6. Study Hub & Deep Focus Engine": [
        {"name": "Offline Pomodoro with Web Audio Soundscapes", "id": "studyPaneTimer", "func": "toggleStudyTimer", "storage": "study-settings-v1"},
        {"name": "Distraction Parking Lot", "id": "studyParkingList", "func": "addParkingItem", "storage": "study-parking-v1"},
        {"name": "Spaced Repetition (SM-2) Flashcard Hub", "id": "studyPaneCards", "func": "rateReviewCard", "storage": "study-cards-v1"},
        {"name": "Exam Countdown & Syllabus Progression", "id": "studyPaneExams", "func": "renderExamsPane", "storage": "study-exams-v1"},
        {"name": "Active Recall Ebbinghaus Review Planner", "id": "studyRecallModal", "func": "openAddRecallModal", "storage": "study-recalls-v1"},
        {"name": "Feynman Explainer & Cornell Notes", "id": "studyPaneNotes", "func": "renderNotesPane", "storage": "study-feynman-v1"},
        {"name": "Subject Vocab Bank & 100-Hour Focus Challenge", "id": "studyPaneVocab", "func": "renderVocabPane", "storage": "study-vocab-v1"}
    ],
    "7. Notes Hub & Knowledge Management": [
        {"name": "Unified Notes Hub with Markdown Preview", "id": "notesView", "func": "renderNotes", "storage": "secnote:"},
        {"name": "Auto-Tagging & Multi-Color Categorization", "id": "noteEditModal", "func": "saveNote", "storage": "secnote:"},
        {"name": "Note Checklist Mode", "id": "noteChecklistContainer", "func": "toggleNoteChecklistMode", "storage": "secnote:"},
        {"name": "Local Image & Attachment Storage", "id": "noteAttachmentsContainer", "func": "addNoteAttachment", "storage": "note-attachments-v1"}
    ],
    "8. Native Android Engine & Platform Integration": [
        {"name": "AlarmManager Foreground Service & Audio Loop", "id": "AlarmService.kt", "func": "scheduleNativeAlarm", "storage": "ZatoonaScheduleRepository"},
        {"name": "Lock-Screen Fullscreen Wake Activity", "id": "AlarmActivity.kt", "func": "dismissAlarm", "storage": "none"},
        {"name": "Study & Focus Android Widget", "id": "StudyWidgetProvider.kt", "func": "syncStudyToNativeWidget", "storage": "KEY_STUDY_CACHE"},
        {"name": "All-In-One Daily Overview Widget", "id": "AllInOneDailyWidgetProvider.kt", "func": "syncAllInOneWidgetData", "storage": "KEY_ALL_IN_ONE_CACHE"},
        {"name": "Next Prayer Home-Screen Widget", "id": "NextPrayerWidgetProvider.kt", "func": "updateWidgetData", "storage": "KEY_PRAYER_CACHE"},
        {"name": "Daily Habits Widget", "id": "DailyHabitsWidgetProvider.kt", "func": "syncDailyHabitsToNativeBridge", "storage": "KEY_HABITS_CACHE"},
        {"name": "Quick Settings Study & Gym Tiles", "id": "ZatoonaStudyTileService.kt", "func": "onClick", "storage": "none"},
        {"name": "Smart Modal & WebView Hardware Back Navigation", "id": "MainActivity.kt", "func": "onBackPressed", "storage": "none"}
    ],
    "9. Fluid UX, Gestures & Micro-Interactions (Package G)": [
        {"name": "Swipe-to-Action on Cards", "id": "swipe_action", "func": "simulateCardSwipe", "storage": "none"},
        {"name": "Horizontal View-Pager Swipe Navigation", "id": "view_pager", "func": "toggleSwipeNavigation", "storage": "zatoona-swipe-nav-enabled"},
        {"name": "Shared-Element Morphing Animations", "id": "morphing", "func": "triggerSharedElementMorph", "storage": "none"},
        {"name": "Egyptian Arabic Natural Language Quick-Add", "id": "nl_quick_add", "func": "parseNaturalLanguageScheduleInput", "storage": "sched-acts:"},
        {"name": "Dynamic Mini-Status Capsule / Island", "id": "dynamicStatusCapsule", "func": "updateDynamicStatusCapsule", "storage": "none"},
        {"name": "Collapsible Sticky Header on Scroll", "id": "collapsible_header", "func": "handleScrollHeader", "storage": "none"},
        {"name": "Contextual Pull-to-Refresh Gesture", "id": "pull_to_refresh", "func": "triggerPullToRefresh", "storage": "none"},
        {"name": "Dismiss Keyboard on Scroll & Outside Click", "id": "dismiss_kb", "func": "blurOnScroll", "storage": "none"},
        {"name": "Accordion Fold/Unfold All Controls", "id": "btnToggleAccordionAll", "func": "toggleAccordionAll", "storage": "none"},
        {"name": "Spotlight Focus Dimming on Rows", "id": "spotlight_dim", "func": "setSpotlightTask", "storage": "none"},
        {"name": "Pinch-to-Zoom Font Scale Accessibility", "id": "font_scale", "func": "setFontScalePercentage", "storage": "theme-font-scale"},
        {"name": "AMOLED True Black & Border Inset Aura Glow", "id": "amoled_aura", "func": "toggleAmoledMode", "storage": "theme-accent"},
        {"name": "Time-Aware Adaptive Home Dashboard", "id": "time_adaptive", "func": "applyTimeAwareAdaptiveDashboard", "storage": "none"}
    ],
    "10. System Polish, Security & Backup": [
        {"name": "AES-GCM 256-bit Encrypted Backup & Restore", "id": "encryptBackupModal", "func": "exportEncryptedBackup", "storage": "KNOWN_KEY_PATTERNS"},
        {"name": "Automated Backup Reminder Banner", "id": "backupReminderBanner", "func": "updateBackupReminderInterval", "storage": "zatoona-last-backup-timestamp-v1"},
        {"name": "Zatoona Wrapped Annual & Monthly Review", "id": "zatoonaWrappedModal", "func": "openZatoonaWrapped", "storage": "none"},
        {"name": "Privacy-Conscious Local AI (Opt-in)", "id": "aiCoachCard", "func": "saveAiCoachSettings", "storage": "ai-coach-settings"}
    ]
}

total_features = 0
found_elements = 0
found_funcs = 0

print("================================================================================")
print("             DYNAMIC FEATURE INVENTORY & VERIFICATION MATRIX                   ")
print("================================================================================")

for domain, features in domains.items():
    print(f"\n### {domain} ({len(features)} Features)")
    for f in features:
        total_features += 1
        fid = f["id"]
        ffunc = f["func"]
        
        # Check if ID exists in HTML or Kotlin
        id_exists = (fid in html) or (os.path.exists(os.path.join(ROOT_DIR, "android", "app", "src", "main", "java", "com", "zatoona", "app", fid)))
        # Check if func exists in HTML or Window
        func_exists = (ffunc in html)
        
        if id_exists: found_elements += 1
        if func_exists: found_funcs += 1
        
        status = "VERIFIED_PRESENT" if (id_exists or func_exists) else "MISSING"
        print(f"  * [{status}] {f['name']}")
        print(f"      - ID/File: {fid} (Present: {id_exists})")
        print(f"      - Engine Func: {ffunc} (Present: {func_exists})")
        print(f"      - Storage Key: {f['storage']}")

print("\n================================================================================")
print(f"TOTAL CATALOGED FEATURES: {total_features}")
print(f"DOM IDs / Files Found    : {found_elements} / {total_features}")
print(f"Engine Functions Found   : {found_funcs} / {total_features}")
print("================================================================================")

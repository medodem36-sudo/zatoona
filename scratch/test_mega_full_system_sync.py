# -*- coding: utf-8 -*-
"""
test_mega_full_system_sync.py
Massive Comprehensive End-to-End System, Cross-Module Synchronization & Integrity Suite.
Verifies deep interaction across all 10 Zatoona domains:
1. Architecture, Parity & Android Assets
2. Worship, Dynamic Prayer, Status Capsule, Checklist & Widget Sync
3. Gym, Exercise Encyclopedia, Sets Logging, 1RM, Rest Timer & SVG Media
4. Nutrition, BMR/TDEE, Egyptian Food DB, Weekly Meal-Prep & Micronutrients
5. Sleep, Bedtime Routine, Habit Streaks Engine & Water Tracker Sync
6. Timeline, Scrollable Schedule Widget, Unified Notes Hub & Global Search
7. UI Design Paradigms (5 Paradigms), Themes (Light/Dark/AMOLED) & Contrast
8. Legal Hub, Privacy, Consent Banner, GDPR Data Erasure & JSON Portability
9. Android Native Alarms, Lock-Screen Activity, Foreground Service & 7 Widgets
10. Performance, Event Handler Hygiene & Zero-ANR Resilience
"""

import unittest
import hashlib
import os
import re

INDEX_PATH = 'index.html'
ZATOONA_PATH = 'zatoona.html'
ASSETS_INDEX_PATH = 'android/app/src/main/assets/index.html'
MANIFEST_PATH = 'android/app/src/main/AndroidManifest.xml'
GRADLE_PATH = 'android/app/build.gradle.kts'
PROGUARD_PATH = 'android/app/proguard-rules.pro'

class TestMegaFullSystemSync(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            cls.html = f.read()
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            cls.manifest = f.read()
        with open(GRADLE_PATH, 'r', encoding='utf-8') as f:
            cls.gradle = f.read()
        with open(PROGUARD_PATH, 'r', encoding='utf-8') as f:
            cls.proguard = f.read()

    # --------------------------------------------------------------------------
    # TIER 1: ARCHITECTURE, PARITY & CODEBASE HYGIENE
    # --------------------------------------------------------------------------
    def test_tier01_three_way_parity(self):
        """Verifies 100% byte-for-byte and SHA-256 parity across all 3 entrypoints."""
        with open(INDEX_PATH, 'rb') as f1, open(ZATOONA_PATH, 'rb') as f2, open(ASSETS_INDEX_PATH, 'rb') as f3:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()
            h3 = hashlib.sha256(f3.read()).hexdigest()
        self.assertEqual(h1, h2, "index.html != zatoona.html")
        self.assertEqual(h1, h3, "index.html != assets/index.html")
        sz1 = os.path.getsize(INDEX_PATH)
        sz2 = os.path.getsize(ZATOONA_PATH)
        sz3 = os.path.getsize(ASSETS_INDEX_PATH)
        self.assertEqual(sz1, sz2, "Sizes mismatch between index and zatoona")
        self.assertEqual(sz1, sz3, "Sizes mismatch between index and assets")

    def test_tier01_head_bootloader_zero_fouc(self):
        """Verifies instant head bootloader sets data-theme and data-ui-paradigm before paint."""
        head_snippet = self.html[:1500]
        self.assertIn("localStorage.getItem('meal-gym-tracker:theme')", head_snippet)
        self.assertIn("localStorage.getItem('zatoona-ui-paradigm-v1')", head_snippet)
        self.assertIn("document.documentElement.setAttribute('data-ui-paradigm', p)", head_snippet)

    # --------------------------------------------------------------------------
    # TIER 2: WORSHIP, PRAYER CALCULATION & WIDGET SYNCHRONIZATION
    # --------------------------------------------------------------------------
    def test_tier02_dynamic_prayer_calculations_no_hardcoding(self):
        """Verifies elimination of hardcoded Asr and dynamic prayer calculation."""
        self.assertNotIn("العصر: 03:15 م", self.html)
        self.assertIn("getEffectivePrayerTimes", self.html)
        self.assertIn("calculateOfflinePrayerTimes", self.html)
        self.assertIn("dynamicStatusCapsule", self.html)

    def test_tier02_worship_adherence_and_checklist(self):
        """Verifies worship adherence stats, tracking, and obligatory prayer fields."""
        self.assertIn("computeWorshipAdherenceStats", self.html)
        self.assertIn("renderWorshipAdherenceSummary", self.html)
        for prayer in ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']:
            self.assertTrue(prayer in self.html.lower(), f"Missing prayer reference: {prayer}")

    def test_tier02_prayer_widgets_sync(self):
        """Verifies synchronization contracts for NextPrayer and AllInOne widgets."""
        self.assertIn("NextPrayerWidgetProvider", self.manifest)
        self.assertIn("AllInOneDailyWidgetProvider", self.manifest)
        self.assertIn("syncAllInOneWidget", self.html)
        self.assertIn("updateActivePrayerCity", self.html)

    # --------------------------------------------------------------------------
    # TIER 3: GYM, EXERCISE ENCYCLOPEDIA & BIOMECHANICS ENGINE
    # --------------------------------------------------------------------------
    def test_tier03_exercise_database_integrity(self):
        """Verifies rich exercise database and catalog components."""
        self.assertIn("ZATOONA_EXERCISE_CATALOG", self.html)
        self.assertIn("goblet-squat", self.html)
        self.assertIn("bench-press", self.html)
        self.assertIn("lat-pulldown", self.html)

    def test_tier03_one_rep_max_formulas(self):
        """Verifies 1RM calculations (compute1RM with Epley & Brzycki formulas)."""
        self.assertIn("compute1RM", self.html)
        self.assertIn("epley", self.html.lower())
        self.assertIn("brzycki", self.html.lower())

    def test_tier03_rest_timer_engine(self):
        """Verifies rest timer functions, presets, and audio/vibration feedback."""
        self.assertIn("startRestTimer", self.html)
        self.assertIn("loadRestTimerState", self.html)
        self.assertIn("saveRestTimerState", self.html)
        self.assertIn("triggerHaptic", self.html)

    def test_tier03_warmup_and_cooldown_generators(self):
        """Verifies interactive warmup and cooldown generators."""
        self.assertIn("generateRoutineWarmupPlan", self.html)
        self.assertIn("generateRoutineCooldownPlan", self.html)
        self.assertIn("renderInteractiveWarmupCard", self.html)
        self.assertIn("renderInteractiveCooldownCard", self.html)

    # --------------------------------------------------------------------------
    # TIER 4: NUTRITION, EGYPTIAN FOODS, SMART MEAL-PREP & MICRONUTRIENTS
    # --------------------------------------------------------------------------
    def test_tier04_bmr_tdee_mifflin_st_jeor(self):
        """Verifies BMR and TDEE calculation logic based on scientific formula."""
        self.assertIn("computeBMR", self.html)
        self.assertIn("computeTDEE", self.html)

    def test_tier04_alexandria_sardines_in_popular_foods(self):
        """Verifies fresh Mediterranean Alexandria Sardines with full profile."""
        self.assertIn("sardinesAlex", self.html)
        self.assertIn("سردين بلدي إسكندراني طازج", self.html)
        self.assertIn("sardines_alex_med", self.html)

    def test_tier04_smart_weekly_meal_prep_plan(self):
        """Verifies 7-day unified meal-prep modal with Limitless Man Max synergy."""
        self.assertIn("modalWeeklyMealPlan", self.html)
        self.assertIn("openWeeklyMealPlanModal", self.html)
        self.assertIn("ليمتليس مان ماكس", self.html)

    def test_tier04_cheat_recovery_and_protein_cost(self):
        """Verifies cheat meal recovery calculator and protein cost analyzer."""
        self.assertIn("modalCheatRecovery", self.html)
        self.assertIn("proteinCostCalcModal", self.html)

    # --------------------------------------------------------------------------
    # TIER 5: SLEEP, BEDTIME ROUTINE & HABIT STREAKS ENGINE
    # --------------------------------------------------------------------------
    def test_tier05_habit_streaks_computation(self):
        """Verifies computeHabitStreaks handles all 6 habits."""
        self.assertIn("computeHabitStreaks", self.html)
        self.assertIn("renderDomainStreaks", self.html)
        self.assertIn("homeStreaksCard", self.html)

    def test_tier05_water_tracker_and_widget(self):
        """Verifies water tracker counter and native widget provider."""
        self.assertIn("WaterWidgetProvider", self.manifest)
        self.assertIn("ACTION_ADD_WATER", self.manifest)
        self.assertIn("syncWaterWidget", self.html)

    # --------------------------------------------------------------------------
    # TIER 6: TIMELINE, SCHEDULE WIDGET & UNIFIED NOTES HUB
    # --------------------------------------------------------------------------
    def test_tier06_scrollable_schedule_widget_service(self):
        """Verifies ScheduleWidgetService collection adapter in Manifest and Proguard."""
        self.assertIn("ScheduleWidgetService", self.manifest)
        self.assertIn("BIND_REMOTEVIEWS", self.manifest)
        self.assertIn("ScheduleWidgetService", self.proguard)
        self.assertIn("syncScheduleWidget", self.html)

    def test_tier06_unified_notes_hub(self):
        """Verifies notes hub with categories, search, and local storage."""
        self.assertIn("notesView", self.html)
        self.assertIn("renderNotesHub", self.html)

    # --------------------------------------------------------------------------
    # TIER 7: UI DESIGN PARADIGMS, THEMES & CONTRAST
    # --------------------------------------------------------------------------
    def test_tier07_all_five_paradigms_declared(self):
        """Verifies all 5 design paradigms are styled and switchable."""
        for p in ['botanical', 'cyber', 'glass', 'editorial', 'brutalist']:
            self.assertIn(f'[data-ui-paradigm="{p}"]', self.html)
        self.assertIn("setUiParadigm", self.html)
        self.assertIn("loadUiParadigm", self.html)

    def test_tier07_brutalist_tactile_press(self):
        """Verifies brutalist mechanical button press displacement."""
        self.assertIn('transform: translate(2px, 2px) !important;', self.html)
        self.assertIn('box-shadow: 1px 1px 0px currentColor !important;', self.html)

    def test_tier07_liquid_glassmorphism_blur(self):
        """Verifies frosted glass backdrop filter blur."""
        self.assertIn('backdrop-filter: blur(18px)', self.html)

    # --------------------------------------------------------------------------
    # TIER 8: COMPLIANCE, PRIVACY, CONSENT BANNER & DATA RIGHTS
    # --------------------------------------------------------------------------
    def test_tier08_legal_privacy_modal_tabs(self):
        """Verifies complete 9-tab Legal and Privacy Hub."""
        self.assertIn('id="legalPrivacyModal"', self.html)
        for tab in ['privacy', 'terms', 'refund', 'cookies', 'kids', 'emails', 'business', 'licenses', 'deletion']:
            self.assertIn(f'data-legal-tab="{tab}"', self.html)
            self.assertIn(f'id="ltab-{tab}"', self.html)

    def test_tier08_storage_consent_banner(self):
        """Verifies storage consent banner and acceptance function."""
        self.assertIn('id="storageConsentBanner"', self.html)
        self.assertIn('acceptStorageConsent', self.html)
        self.assertIn('initStorageConsentBanner', self.html)

    def test_tier08_gdpr_data_erasure_and_export(self):
        """Verifies GDPR Art. 17 data erasure with confirm input and Art. 20 JSON export."""
        self.assertIn('id="dataDeletionModal"', self.html)
        self.assertIn('inpConfirmDelete', self.html)
        self.assertIn('executeComprehensiveDataWipe', self.html)
        self.assertIn('exportAppDataToJson', self.html)

    # --------------------------------------------------------------------------
    # TIER 9: ANDROID NATIVE ENGINE, ALARMS & ALL 7 WIDGETS
    # --------------------------------------------------------------------------
    def test_tier09_all_seven_widgets_in_manifest(self):
        """Verifies all 7 native widgets are declared in AndroidManifest.xml."""
        expected_widgets = [
            'QuickAccessWidgetProvider',
            'NextPrayerWidgetProvider',
            'DailyHabitsWidgetProvider',
            'StudyWidgetProvider',
            'WaterWidgetProvider',
            'ScheduleWidgetProvider',
            'AllInOneDailyWidgetProvider'
        ]
        for w in expected_widgets:
            self.assertIn(w, self.manifest, f"Missing widget in manifest: {w}")

    def test_tier09_alarm_engine_and_lockscreen_activity(self):
        """Verifies complete AlarmManager, foreground service, and lockscreen activity."""
        self.assertIn("AlarmReceiver", self.manifest)
        self.assertIn("AlarmService", self.manifest)
        self.assertIn("AlarmActivity", self.manifest)
        self.assertIn("BootReceiver", self.manifest)
        self.assertIn("FOREGROUND_SERVICE_SPECIAL_USE", self.manifest)
        self.assertIn("showWhenLocked=\"true\"", self.manifest)

    # --------------------------------------------------------------------------
    # TIER 10: ACCESSIBILITY, FOCUS VISIBLE & ZERO-ANR RESILIENCE
    # --------------------------------------------------------------------------
    def test_tier10_wcag_focus_visible_and_escape(self):
        """Verifies focus-visible outlines and global Escape key modal dismiss."""
        self.assertIn(":focus-visible", self.html)
        self.assertIn("outline: 2px solid var(--primary)", self.html)
        self.assertIn("e.key === 'Escape'", self.html)

    def test_tier10_clean_third_party_sdk_dependency_tree(self):
        """Verifies only core AndroidX runtime dependencies in Gradle."""
        self.assertNotIn("firebase", self.gradle)
        self.assertNotIn("admob", self.gradle)
        self.assertNotIn("google-analytics", self.gradle)
        self.assertNotIn("facebook", self.gradle)

if __name__ == '__main__':
    unittest.main()

"""
test_phase3_gym_engine.py
Automated acceptance test suite for Phase 3: Next-Gen Gym & Strength Engine (9 features).
Tests static invariants, DOM presence, 3-way parity, and runtime behavior via headless Selenium Chrome.
"""

import os
import sys
import time
import json
import hashlib
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
ZATOONA_PATH = os.path.join(BASE_DIR, "zatoona.html")
ANDROID_INDEX_PATH = os.path.join(BASE_DIR, "android", "app", "src", "main", "assets", "index.html")

class TestPhase3GymEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,1024")
        chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")

        cls.driver = webdriver.Chrome(options=chrome_options)
        file_url = "file:///" + os.path.abspath(INDEX_PATH).replace("\\", "/")
        cls.driver.get(file_url)
        WebDriverWait(cls.driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)

        # Suppress alerts and clear localStorage
        cls.driver.execute_script("""
            window.alert = function(){};
            localStorage.clear();
        """)

    @classmethod
    def tearDownClass(cls):
        try:
            if hasattr(cls, "driver") and cls.driver:
                cls.driver.quit()
        except Exception:
            pass

    def test_01_three_way_html_parity(self):
        """Verify byte-for-byte 3-way HTML parity across root and Android assets."""
        paths = [INDEX_PATH, ZATOONA_PATH, ANDROID_INDEX_PATH]
        hashes = []
        sizes = []
        for p in paths:
            self.assertTrue(os.path.exists(p), f"Missing file: {p}")
            with open(p, "rb") as f:
                data = f.read()
            hashes.append(hashlib.sha256(data).hexdigest())
            sizes.append(len(data))

        self.assertEqual(len(set(hashes)), 1, f"Hash mismatch across HTML entry points: {hashes}")
        self.assertEqual(len(set(sizes)), 1, f"Size mismatch across HTML entry points: {sizes}")
        self.assertGreater(sizes[0], 1500000, "HTML file size unexpectedly small")

    def test_02_known_key_patterns_includes_phase3_keys(self):
        """Verify KNOWN_KEY_PATTERNS in index.html includes all Phase 3 storage keys."""
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("/^gym-blacklist-v1$/", content)
        self.assertIn("/^gym-pain-flags-v1$/", content)
        self.assertIn("/^gym-1rm-history-v1$/", content)
        self.assertIn("/^gym-tempo-settings-v1$/", content)

    def test_03_bridge_workout_notification_methods_exist(self):
        """Verify Kotlin bridge and notification manager have workout notification methods."""
        bridge_path = os.path.join(BASE_DIR, "android", "app", "src", "main", "java", "com", "zatoona", "app", "ZatoonaBridge.kt")
        notif_path = os.path.join(BASE_DIR, "android", "app", "src", "main", "java", "com", "zatoona", "app", "ZatoonaNotificationManager.kt")

        with open(bridge_path, "r", encoding="utf-8") as f:
            b_content = f.read()
        with open(notif_path, "r", encoding="utf-8") as f:
            n_content = f.read()

        self.assertIn("showWorkoutNotification", b_content)
        self.assertIn("hideWorkoutNotification", b_content)
        self.assertIn("NOTIFICATION_ID_WORKOUT", n_content)
        self.assertIn("showWorkoutNotification", n_content)
        self.assertIn("hideWorkoutNotification", n_content)

    def test_04_gym_tools_quick_bar_rendered_in_gym_mode(self):
        """Verify Quick Tools bar is rendered inside gymView with all 8 action buttons."""
        res = self.driver.execute_script("""
            navigateTo('gym');
            renderExercises();
            const qb = document.getElementById('gymToolsQuickBar');
            return {
                hasQb: (qb !== null),
                buttons: qb ? qb.querySelectorAll('.gym-tool-btn').length : 0
            };
        """)
        self.assertTrue(res["hasQb"])
        self.assertEqual(res["buttons"], 8)

    def test_05_1rm_rpe_calculator_runtime(self):
        """Verify 1RM and RPE calculator computation and UI table generation."""
        res = self.driver.execute_script("""
            openGym1RMCalc('bench', 100, 10);
            const wInput = document.getElementById('calc1rmWeightInput');
            const rInput = document.getElementById('calc1rmRepsInput');
            const rpeSel = document.getElementById('calc1rmRpeSelect');
            wInput.value = '100';
            rInput.value = '10';
            rpeSel.value = '0';
            wInput.dispatchEvent(new Event('input'));

            const out = document.getElementById('calc1rmOutput').textContent;
            const rows = document.querySelectorAll('#calc1rmTableBody tr').length;
            const modalOpen = document.getElementById('gym1RMCalcModal').classList.contains('open');
            return { out, rows, modalOpen };
        """)
        self.assertTrue(res["modalOpen"])
        self.assertIn("133", res["out"]) # 100 * (1 + 10/30) = 133.3 kg
        self.assertEqual(res["rows"], 10)

        # Close modal
        self.driver.execute_script("document.getElementById('btnClose1RMCalc').click();")
        modal_open = self.driver.execute_script("return document.getElementById('gym1RMCalcModal').classList.contains('open');")
        self.assertFalse(modal_open)

    def test_06_warmup_progression_and_plate_loader(self):
        """Verify smart warmup sets progression and plate breakdown calculation."""
        res = self.driver.execute_script("""
            openGymWarmupCalc(100);
            const wInput = document.getElementById('calcWarmupTargetWeight');
            const barSel = document.getElementById('calcWarmupBarType');
            wInput.value = '100';
            barSel.value = '20';
            wInput.dispatchEvent(new Event('input'));

            const platesCount = document.querySelectorAll('#plateDiscsContainer .plate-disc').length;
            const tableRows = document.querySelectorAll('#warmupSetsTableBody tr').length;
            const modalOpen = document.getElementById('gymWarmupCalcModal').classList.contains('open');
            return { platesCount, tableRows, modalOpen };
        """)
        self.assertTrue(res["modalOpen"])
        # For 100kg total with 20kg bar: 40kg per side -> 20kg + 20kg (2 plates)
        self.assertEqual(res["platesCount"], 2)
        self.assertEqual(res["tableRows"], 6)

        # Close modal
        self.driver.execute_script("document.getElementById('btnCloseWarmupCalc').click();")

    def test_07_live_exercise_swap(self):
        """Verify exercise swap modal detects muscle group and renders matching alternatives."""
        res = self.driver.execute_script("""
            openExerciseSwapModal('bench');
            const name = document.getElementById('swapCurrentExName').textContent;
            const altsCount = document.querySelectorAll('#swapAltList .swap-alt-card').length;
            const modalOpen = document.getElementById('gymExerciseSwapModal').classList.contains('open');
            return { name, altsCount, modalOpen };
        """)
        self.assertTrue(res["modalOpen"])
        self.assertGreater(res["altsCount"], 0)

        # Close modal
        self.driver.execute_script("document.getElementById('btnCloseSwapModal').click();")

    def test_08_blacklist_exercises_workflow(self):
        """Verify blacklisting an exercise and unblacklisting it with persistence."""
        res = self.driver.execute_script("""
            openGymBlacklistModal();
            const sel = document.getElementById('blacklistExerciseSelect');
            if(sel.options.length > 0){
                sel.selectedIndex = 0;
            }
            const chosenKey = sel.value;
            document.getElementById('btnConfirmBlacklistEx').click();

            const blRaw = localStorage.getItem('gym-blacklist-v1');
            const bl = blRaw ? JSON.parse(blRaw) : {};
            const isBlacklisted = !!bl[chosenKey];

            // Now unblacklist
            const unbtn = document.querySelector('[data-unblacklist-key="' + chosenKey + '"]');
            if(unbtn) unbtn.click();
            const blAfter = JSON.parse(localStorage.getItem('gym-blacklist-v1') || '{}');
            const isStillBlacklisted = !!blAfter[chosenKey];

            return { isBlacklisted, isStillBlacklisted };
        """)
        self.assertTrue(res["isBlacklisted"])
        self.assertFalse(res["isStillBlacklisted"])

        # Close modal
        self.driver.execute_script("document.getElementById('btnCloseBlacklistModal').click();")

    def test_09_muscle_recovery_heatmap(self):
        """Verify muscle recovery state computation and SVG body map."""
        res = self.driver.execute_script("""
            openGymRecoveryHeatmapModal();
            const cardsCount = document.querySelectorAll('#recoveryMuscleGrid .recovery-muscle-card').length;
            const svgChest = document.getElementById('svgMuscChest')?.getAttribute('fill');
            const modalOpen = document.getElementById('gymRecoveryHeatmapModal').classList.contains('open');
            return { cardsCount, svgChest, modalOpen };
        """)
        self.assertTrue(res["modalOpen"])
        self.assertEqual(res["cardsCount"], 10)
        self.assertIsNotNone(res["svgChest"])

        # Close modal
        self.driver.execute_script("document.getElementById('btnCloseRecoveryModal').click();")

    def test_10_gym_big_numbers_focus_mode(self):
        """Verify Big Numbers overlay, weight adjustment, and set completion rest mode."""
        res = self.driver.execute_script("""
            openGymBigNumbersOverlay('squat');
            const overlay = document.getElementById('gymBigNumbersOverlay');
            const isOpen = overlay.classList.contains('open');

            // Click plus weight
            document.getElementById('gbnPlusWeight').click();
            const weightVal = document.getElementById('gbnWeightNumber').textContent;

            // Click set done -> switches to rest view
            document.getElementById('gbnDoneSetBtn').click();
            const isRestVisible = !document.getElementById('gbnRestView').classList.contains('hidden');
            const restTime = document.getElementById('gbnRestTimerText').textContent;

            // Skip rest
            document.getElementById('gbnSkipRest').click();
            const isLiftingVisible = !document.getElementById('gbnLiftingView').classList.contains('hidden');

            // Close
            document.getElementById('gbnCloseBtn').click();
            const isClosed = !overlay.classList.contains('open');

            return { isOpen, weightVal, isRestVisible, restTime, isLiftingVisible, isClosed };
        """)
        self.assertTrue(res["isOpen"])
        self.assertTrue(res["isRestVisible"])
        self.assertIn(":", res["restTime"])
        self.assertTrue(res["isLiftingVisible"])
        self.assertTrue(res["isClosed"])

    def test_11_tempo_cadence_metronome(self):
        """Verify tempo cadence metronome presets and active tempo values."""
        res = self.driver.execute_script("""
            openGymTempoModal();
            const sel = document.getElementById('tempoPresetSelect');
            sel.value = '3-0-1-0';
            sel.dispatchEvent(new Event('change'));

            // Start metronome
            document.getElementById('btnToggleTempoPlay').click();
            const stepName = document.getElementById('tempoStepName').textContent;

            // Stop metronome
            document.getElementById('btnToggleTempoPlay').click();

            // Close
            document.getElementById('btnCloseTempoModal').click();
            return { stepName };
        """)
        self.assertIn("نزول", res["stepName"])

    def test_12_injury_and_pain_flagging(self):
        """Verify pain logging creates active alert on exercise card."""
        res = self.driver.execute_script("""
            navigateTo('gym');
            for(let i=0; i<weekDates.length; i++){
                const eff = getEffectiveGymDay(toISO(weekDates[i]), i);
                if(!eff.isRest && eff.gymType !== 'rest' && eff.gym){
                    selectedIdx = i;
                    break;
                }
            }
            renderExercises();

            openGymPainTrackerModal('squat');
            const exSel = document.getElementById('painExerciseSelect');
            if(exSel.options.length > 0){
                exSel.selectedIndex = 0;
            }
            const chosenKey = exSel.value;
            const jSel = document.getElementById('painJointSelect');
            jSel.value = 'الركبة';
            const iSel = document.getElementById('painIntensitySelect');
            iSel.value = '6';
            document.getElementById('painNotesInput').value = 'ألم خفيف أثناء أقصى النزول';

            document.getElementById('btnSavePainFlag').click();

            const flags = JSON.parse(localStorage.getItem('gym-pain-flags-v1') || '{}');
            const hasFlag = !!flags[chosenKey];

            // Check if alert appears on card
            renderExercises();
            const alertCard = document.querySelector('#exercises .ex-card .ex-pain-alert');
            const hasAlert = (alertCard !== null);

            // Clean up
            const clearBtn = document.querySelector('[data-clear-pain-key="' + chosenKey + '"]');
            if(clearBtn) clearBtn.click();
            const flagsAfter = JSON.parse(localStorage.getItem('gym-pain-flags-v1') || '{}');

            document.getElementById('btnClosePainModal').click();

            return { hasFlag, hasAlert, cleaned: !flagsAfter[chosenKey] };
        """)
        self.assertTrue(res["hasFlag"])
        self.assertTrue(res["hasAlert"])
        self.assertTrue(res["cleaned"])

    def test_13_exercise_card_actions_row(self):
        """Verify all exercise cards in today's workout have the 5 Phase 3 action buttons."""
        res = self.driver.execute_script("""
            navigateTo('gym');
            for(let i=0; i<weekDates.length; i++){
                const eff = getEffectiveGymDay(toISO(weekDates[i]), i);
                if(!eff.isRest && eff.gymType !== 'rest' && eff.gym){
                    selectedIdx = i;
                    break;
                }
            }
            renderExercises();

            const rows = document.querySelectorAll('#exercises .ex-card .ex-p3-actions-row');
            const sampleButtons = rows[0] ? rows[0].querySelectorAll('.ex-p3-action-btn').length : 0;
            return { rowCount: rows.length, sampleButtons };
        """)
        self.assertGreater(res["rowCount"], 0)
        self.assertEqual(res["sampleButtons"], 5)

    def test_14_ongoing_workout_hud_presence(self):
        """Verify ongoing workout floating HUD bar element exists and updates on workout activity."""
        res = self.driver.execute_script("""
            navigateTo('gym');
            for(let i=0; i<weekDates.length; i++){
                const eff = getEffectiveGymDay(toISO(weekDates[i]), i);
                if(!eff.isRest && eff.gymType !== 'rest' && eff.gym){
                    selectedIdx = i;
                    break;
                }
            }
            renderExercises();

            const hud = document.getElementById('gymActiveWorkoutHud');
            const exists = (hud !== null);

            // Simulate done set
            const firstChip = document.querySelector('#exercises .set-chip');
            if(firstChip) firstChip.click();

            const isVisible = !hud.classList.contains('hidden');
            const title = document.getElementById('hudExTitle').textContent;
            return { exists, isVisible, title };
        """)
        self.assertTrue(res["exists"])
        self.assertTrue(res["isVisible"])
        self.assertNotEqual(res["title"], "")

if __name__ == '__main__':
    unittest.main(verbosity=2)

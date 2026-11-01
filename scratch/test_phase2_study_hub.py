# -*- coding: utf-8 -*-
"""
Targeted Test Suite for Phase 2: Study Hub (13 features).
Verifies:
1. 3-Way HTML byte parity across index.html, zatoona.html, android/app/src/main/assets/index.html.
2. Navigation registration: NAV_MODES, KNOWN_KEY_PATTERNS, sidebarNav, drawerNav, modesBar.
3. DOM containers, subtabs, and modals existence.
4. Selenium headless runtime tests for all 13 Phase 2 features:
   - Study mode navigation and titles
   - Subtab switching across 5 panes
   - Timer & Pomodoro modes (standard, deep, flow)
   - Web Audio ambient sounds & volume
   - Distraction parking lot (add, toggle, delete)
   - Deep focus AMOLED fullscreen modal
   - Spaced Repetition (SM-2) flashcard lifecycle
   - Exam countdown & syllabus progress tracking
   - Active Recall Ebbinghaus review planner
   - Feynman explainer notebook & Cornell grid notes
   - Vocab bank & random quiz modal
   - Reading speed calculator & 100-Hour focus challenge
"""
import unittest
import hashlib
import os
import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
ZATOONA_PATH = os.path.join(ROOT_DIR, "zatoona.html")
ANDROID_ASSET_PATH = os.path.join(ROOT_DIR, "android", "app", "src", "main", "assets", "index.html")

class TestPhase2StudyHub(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            cls.html = f.read()

        # Headless Chrome setup
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,900")
        chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")

        cls.driver = webdriver.Chrome(options=chrome_options)
        file_url = "file:///" + os.path.abspath(INDEX_PATH).replace("\\", "/")
        cls.driver.get(file_url)
        WebDriverWait(cls.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver") and cls.driver:
            cls.driver.quit()

    def test_01_html_three_way_byte_parity(self):
        """All 3 entrypoint HTML files must have identical size and SHA-256."""
        files = [INDEX_PATH, ZATOONA_PATH, ANDROID_ASSET_PATH]
        hashes = set()
        sizes = set()
        for fp in files:
            with open(fp, "rb") as f:
                data = f.read()
                hashes.add(hashlib.sha256(data).hexdigest())
                sizes.add(len(data))
        self.assertEqual(len(hashes), 1, f"SHA-256 hash mismatch: {hashes}")
        self.assertEqual(len(sizes), 1, f"File size mismatch: {sizes}")

    def test_02_navigation_structure(self):
        """NAV_MODES, KNOWN_KEY_PATTERNS, and navigation buttons must be properly wired."""
        self.assertIn("'study'", self.html)
        self.assertIn("/^study-/", self.html)
        self.assertIn('id="modeStudy"', self.html)
        self.assertIn('id="sideNav-study"', self.html)
        self.assertIn('id="drawNav-study"', self.html)
        self.assertIn("studyView", self.html)

    def test_03_study_view_and_subtabs_exist(self):
        """#studyView and all 5 subtab panes and modals must exist in DOM."""
        driver = self.driver
        view = driver.find_element(By.ID, "studyView")
        self.assertIsNotNone(view)

        panes = ["studyPaneTimer", "studyPaneCards", "studyPaneExams", "studyPaneNotes", "studyPaneVocab"]
        for pid in panes:
            el = driver.find_element(By.ID, pid)
            self.assertIsNotNone(el)

        modals = ["studyDeepFocusModal", "studyCardModal", "studyExamModal", "studyRecallModal", "studyFeynmanModal", "studyCornellModal", "studyVocabModal", "studyVocabQuizModal", "studySubjectModal"]
        for mid in modals:
            el = driver.find_element(By.ID, mid)
            self.assertIsNotNone(el)

    def test_04_selenium_navigation_to_study(self):
        """Navigating to study mode reveals studyView and sets header title."""
        driver = self.driver
        driver.execute_script("navigateTo('study');")
        time.sleep(0.5)

        view = driver.find_element(By.ID, "studyView")
        self.assertNotIn("hidden", view.get_attribute("class"))

        title_el = driver.find_element(By.ID, "pageTitle")
        self.assertIn("المذاكرة", title_el.text)

    def test_05_selenium_subtab_switching(self):
        """Clicking each subtab activates its pane and hides the others."""
        driver = self.driver
        subtabs = ["cards", "exams", "notes", "vocab", "timer"]
        for tab in subtabs:
            btn = driver.find_element(By.CSS_SELECTOR, f"#studySubTabs [data-study-tab='{tab}']")
            btn.click()
            time.sleep(0.2)
            self.assertIn("active", btn.get_attribute("class"))

            pane_map = {
                "timer": "studyPaneTimer",
                "cards": "studyPaneCards",
                "exams": "studyPaneExams",
                "notes": "studyPaneNotes",
                "vocab": "studyPaneVocab"
            }
            pane = driver.find_element(By.ID, pane_map[tab])
            self.assertNotIn("hidden", pane.get_attribute("class"))

    def test_06_selenium_timer_and_pomo_mode(self):
        """Timer controls and modes (standard, deep, flow) work properly."""
        driver = self.driver
        # Switch to timer tab
        driver.find_element(By.CSS_SELECTOR, "#studySubTabs [data-study-tab='timer']").click()
        time.sleep(0.2)

        # Standard mode defaults to 25:00
        digits = driver.find_element(By.ID, "studyTimerDigits")
        self.assertEqual(digits.text, "25:00")

        # Switch to deep (50/10)
        deep_btn = driver.find_element(By.CSS_SELECTOR, "[data-pomo-mode='deep']")
        deep_btn.click()
        time.sleep(0.2)
        self.assertEqual(driver.find_element(By.ID, "studyTimerDigits").text, "50:00")

        # Switch to flow (00:00 count up)
        flow_btn = driver.find_element(By.CSS_SELECTOR, "[data-pomo-mode='flow']")
        flow_btn.click()
        time.sleep(0.2)
        self.assertEqual(driver.find_element(By.ID, "studyTimerDigits").text, "00:00")

        # Toggle timer start/pause
        toggle_btn = driver.find_element(By.ID, "btnStudyTimerToggle")
        toggle_btn.click()
        time.sleep(0.3)
        self.assertIn("إيقاف", toggle_btn.text)
        toggle_btn.click()
        time.sleep(0.2)
        self.assertIn("ابدأ", toggle_btn.text)

        # Reset to standard
        driver.find_element(By.CSS_SELECTOR, "[data-pomo-mode='standard']").click()
        time.sleep(0.2)
        self.assertEqual(driver.find_element(By.ID, "studyTimerDigits").text, "25:00")

    def test_07_selenium_ambient_sounds_and_volume(self):
        """Ambient noise pills toggle and volume slider updates settings without crash."""
        driver = self.driver
        brown_btn = driver.find_element(By.CSS_SELECTOR, "[data-ambient='brown']")
        brown_btn.click()
        time.sleep(0.2)
        self.assertIn("active", brown_btn.get_attribute("class"))

        vol_slider = driver.find_element(By.ID, "studyAmbientVolume")
        driver.execute_script("arguments[0].value = 75; arguments[0].dispatchEvent(new Event('input'));", vol_slider)
        time.sleep(0.2)
        vol_label = driver.find_element(By.ID, "studyAmbientVolumeLabel")
        self.assertEqual(vol_label.text, "75%")

        # Turn sound back to silent
        none_btn = driver.find_element(By.CSS_SELECTOR, "[data-ambient='none']")
        none_btn.click()
        time.sleep(0.2)
        self.assertIn("active", none_btn.get_attribute("class"))

    def test_08_selenium_parking_lot(self):
        """Distraction parking lot adds, checks, and deletes items."""
        driver = self.driver
        inp = driver.find_element(By.ID, "studyParkingInput")
        inp.send_keys("فكرة مشتتة للاختبار الآلي")
        driver.find_element(By.ID, "btnStudyAddParking").click()
        time.sleep(0.3)

        list_el = driver.find_element(By.ID, "studyParkingList")
        self.assertIn("فكرة مشتتة للاختبار الآلي", list_el.text)

        # Toggle item
        item_text = list_el.find_element(By.TAG_NAME, "span")
        item_text.click()
        time.sleep(0.2)
        self.assertIn("checked", list_el.find_element(By.CLASS_NAME, "study-parking-item").get_attribute("class"))

        # Delete item
        del_btn = list_el.find_element(By.CLASS_NAME, "reset-btn")
        del_btn.click()
        time.sleep(0.2)
        self.assertNotIn("فكرة مشتتة للاختبار الآلي", list_el.text)

    def test_09_selenium_deep_focus_modal(self):
        """Deep focus fullscreen opens and exits cleanly."""
        driver = self.driver
        enter_btn = driver.find_element(By.ID, "btnStudyEnterDeepFocus")
        enter_btn.click()
        time.sleep(0.3)

        df_modal = driver.find_element(By.ID, "studyDeepFocusModal")
        self.assertNotIn("hidden", df_modal.get_attribute("class"))

        exit_btn = driver.find_element(By.ID, "btnStudyExitDeepFocus")
        exit_btn.click()
        time.sleep(0.3)
        self.assertIn("hidden", df_modal.get_attribute("class"))

    def test_10_selenium_flashcard_sm2_workflow(self):
        """Creating a card, revealing answer, and rating with SM-2 updates repetitions and interval."""
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "#studySubTabs [data-study-tab='cards']").click()
        time.sleep(0.3)

        # Open modal
        driver.find_element(By.ID, "btnStudyAddCard").click()
        time.sleep(0.2)

        # Fill card
        driver.find_element(By.ID, "studyCardFrontInput").send_keys("ما هي عاصمة مصر؟")
        driver.find_element(By.ID, "studyCardBackInput").send_keys("القاهرة")
        driver.find_element(By.ID, "btnSaveCardModal").click()
        time.sleep(0.4)

        # Verify card front is loaded in review box
        front_box = driver.find_element(By.ID, "studyReviewFront")
        self.assertIn("ما هي عاصمة مصر؟", front_box.text)

        # Reveal answer
        reveal_btn = driver.find_element(By.ID, "btnStudyRevealAnswer")
        reveal_btn.click()
        time.sleep(0.2)

        back_box = driver.find_element(By.ID, "studyReviewBack")
        self.assertNotIn("hidden", back_box.get_attribute("class"))
        self.assertIn("القاهرة", back_box.text)

        # Rate card as 'Good' (Grade 3)
        good_btn = driver.find_element(By.CSS_SELECTOR, "#studySm2RatingGrid [data-grade='3']")
        good_btn.click()
        time.sleep(0.3)

        # Verify in localStorage that card interval is updated
        cards_raw = driver.execute_script("return localStorage.getItem('study-flashcards-v1');")
        self.assertIn("القاهرة", cards_raw)
        self.assertIn('"repetitions":1', cards_raw.replace(" ", ""))

    def test_11_selenium_exams_and_syllabus_progress(self):
        """Adding an exam with chapters and toggling completion updates progress."""
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "#studySubTabs [data-study-tab='exams']").click()
        time.sleep(0.3)

        driver.find_element(By.ID, "btnStudyAddExam").click()
        time.sleep(0.2)

        driver.find_element(By.ID, "studyExamNameInput").send_keys("امتحان تجريبي")
        driver.execute_script("document.getElementById('studyExamDateInput').value = '2026-12-15T10:00';")
        driver.find_element(By.ID, "studyExamChaptersInput").send_keys("الباب الأول\nالباب الثاني")
        driver.find_element(By.ID, "btnSaveExamModal").click()
        time.sleep(0.4)

        grid = driver.find_element(By.ID, "studyExamsGrid")
        self.assertIn("امتحان تجريبي", grid.text)
        self.assertIn("تغطية المنهج: 0 من 2 فصول (0%)", grid.text)

        # Check off first chapter
        cb = grid.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        cb.click()
        time.sleep(0.3)

        grid = driver.find_element(By.ID, "studyExamsGrid")
        self.assertIn("تغطية المنهج: 1 من 2 فصول (50%)", grid.text)

    def test_12_selenium_active_recall_ebbinghaus(self):
        """Adding an active recall topic creates the 5 review milestones."""
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "#studySubTabs [data-study-tab='exams']").click()
        time.sleep(0.3)

        driver.find_element(By.ID, "btnStudyAddRecallTopic").click()
        time.sleep(0.2)

        driver.find_element(By.ID, "studyRecallTopicInput").send_keys("منحنى النسيان لإبينغهاوس")
        driver.find_element(By.ID, "btnSaveRecallModal").click()
        time.sleep(0.4)

        recall_list = driver.find_element(By.ID, "studyRecallList")
        self.assertIn("منحنى النسيان لإبينغهاوس", recall_list.text)
        self.assertIn("بعد 1 يوم", recall_list.text)
        self.assertIn("بعد 7 أيام", recall_list.text)
        self.assertIn("بعد 30 أيام", recall_list.text)

        # Toggle first milestone
        first_chip = recall_list.find_element(By.CLASS_NAME, "study-recall-chip")
        first_chip.click()
        time.sleep(0.3)
        self.assertIn("✅", recall_list.find_element(By.CLASS_NAME, "study-recall-chip").text)

    def test_13_selenium_feynman_and_cornell(self):
        """Testing Feynman explanation and Cornell 3-zone notes."""
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "#studySubTabs [data-study-tab='notes']").click()
        time.sleep(0.3)

        # Add Feynman
        driver.find_element(By.ID, "btnStudyAddFeynman").click()
        time.sleep(0.2)
        driver.find_element(By.ID, "studyFeynmanConceptInput").send_keys("مفهوم الخوارزمية")
        driver.find_element(By.ID, "studyFeynmanExplainInput").send_keys("مثل وصفة كيكة بخطوات مرتبة")
        driver.find_element(By.ID, "btnSaveFeynmanModal").click()
        time.sleep(0.4)

        feyn_list = driver.find_element(By.ID, "studyFeynmanList")
        self.assertIn("مفهوم الخوارزمية", feyn_list.text)
        self.assertIn("وصفة كيكة", feyn_list.text)

        # Switch to Cornell sub-toggle
        driver.find_element(By.ID, "btnSubToggleCornell").click()
        time.sleep(0.3)

        # Add Cornell
        driver.find_element(By.ID, "btnStudyAddCornell").click()
        time.sleep(0.2)
        driver.find_element(By.ID, "studyCornellTitleInput").send_keys("محاضرة شبكات")
        driver.find_element(By.ID, "studyCornellCuesInput").send_keys("بروتوكول TCP")
        driver.find_element(By.ID, "studyCornellNotesInput").send_keys("تفاصيل طبقة النقل ومصافحة اليد الثلاثية")
        driver.find_element(By.ID, "studyCornellSummaryInput").send_keys("بروتوكول موثوق يعتمد على التأكيد")
        driver.find_element(By.ID, "btnSaveCornellModal").click()
        time.sleep(0.4)

        cornell_list = driver.find_element(By.ID, "studyCornellList")
        self.assertIn("محاضرة شبكات", cornell_list.text)
        self.assertIn("بروتوكول TCP", cornell_list.text)
        self.assertIn("مصافحة اليد الثلاثية", cornell_list.text)

    def test_14_selenium_vocab_bank_and_quiz(self):
        """Vocab bank adds term and runs quick random quiz."""
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "#studySubTabs [data-study-tab='vocab']").click()
        time.sleep(0.3)

        # Add Vocab
        driver.find_element(By.ID, "btnStudyAddVocab").click()
        time.sleep(0.2)
        driver.find_element(By.ID, "studyVocabTermInput").send_keys("Abstraction")
        driver.find_element(By.ID, "studyVocabDefInput").send_keys("إخفاء التفاصيل المعقدة وإظهار الأساسيات فقط")
        driver.find_element(By.ID, "btnSaveVocabModal").click()
        time.sleep(0.4)

        vocab_list = driver.find_element(By.ID, "studyVocabList")
        self.assertIn("Abstraction", vocab_list.text)

        # Open Quiz
        driver.find_element(By.ID, "btnStudyVocabQuiz").click()
        time.sleep(0.3)
        quiz_modal = driver.find_element(By.ID, "studyVocabQuizModal")
        self.assertNotIn("hidden", quiz_modal.get_attribute("class"))

        # Reveal Definition in Quiz
        driver.find_element(By.ID, "btnStudyQuizReveal").click()
        time.sleep(0.2)
        ans_box = driver.find_element(By.ID, "studyQuizAnswerBox")
        self.assertNotIn("hidden", ans_box.get_attribute("class"))

        # Mark Mastered
        driver.find_element(By.ID, "btnStudyQuizMastered").click()
        time.sleep(0.3)
        self.assertIn("hidden", quiz_modal.get_attribute("class"))

    def test_15_selenium_reading_calc_and_100h_challenge(self):
        """Reading speed calculator and 100-Hour challenge meter work reactivity."""
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "#studySubTabs [data-study-tab='vocab']").click()
        time.sleep(0.2)

        pages_inp = driver.find_element(By.ID, "studyCalcPages")
        driver.execute_script("arguments[0].value = 200; arguments[0].dispatchEvent(new Event('input'));", pages_inp)
        time.sleep(0.3)

        res_box = driver.find_element(By.ID, "studyCalcResultText")
        self.assertIn("متبقي حوالي", res_box.text)

        # 100h Challenge meter exists and has text
        challenge_txt = driver.find_element(By.ID, "studyChallengeCurrentText")
        self.assertIn("/ 100 ساعة", challenge_txt.text)


if __name__ == "__main__":
    unittest.main()

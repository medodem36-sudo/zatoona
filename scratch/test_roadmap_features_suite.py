# -*- coding: utf-8 -*-
"""
Targeted Acceptance Suite for Zatoona Continuous Roadmap Features:
1. Feature 1: Zatoona Autopilot (Adaptive Day Planner).
2. Feature 2: Cross-Domain Local Insights Engine.
3. Feature 3: Automated Periodic Safe Backup.
4. Feature 4: Rich Interactive Notification Actions.
"""
import unittest
import hashlib
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
ZATOONA_PATH = os.path.join(ROOT_DIR, "zatoona.html")
ANDROID_ASSET_PATH = os.path.join(ROOT_DIR, "android", "app", "src", "main", "assets", "index.html")
MANIFEST_PATH = os.path.join(ROOT_DIR, "android", "app", "src", "main", "AndroidManifest.xml")
NOTIF_RECEIVER_PATH = os.path.join(ROOT_DIR, "android", "app", "src", "main", "java", "com", "zatoona", "app", "NotificationActionReceiver.kt")
NOTIF_MANAGER_PATH = os.path.join(ROOT_DIR, "android", "app", "src", "main", "java", "com", "zatoona", "app", "ZatoonaNotificationManager.kt")
PROGUARD_PATH = os.path.join(ROOT_DIR, "android", "app", "proguard-rules.pro")

class TestRoadmapFeaturesSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            cls.html = f.read()

    def test_01_three_way_parity(self):
        """All 3 entrypoints must have identical file size and SHA-256."""
        files = [INDEX_PATH, ZATOONA_PATH, ANDROID_ASSET_PATH]
        hashes = set()
        sizes = set()
        for fp in files:
            with open(fp, "rb") as f:
                data = f.read()
                hashes.add(hashlib.sha256(data).hexdigest())
                sizes.add(len(data))
        self.assertEqual(len(hashes), 1, f"SHA-256 mismatch: {hashes}")
        self.assertEqual(len(sizes), 1, f"Size mismatch: {sizes}")

    def test_02_autopilot_dom_elements(self):
        """Autopilot launcher button, modal, and controls must exist in DOM."""
        self.assertIn('id="btnScheduleAutopilot"', self.html)
        self.assertIn('openScheduleAutopilotModal()', self.html)
        self.assertIn('id="modalScheduleAutopilot"', self.html)
        self.assertIn('id="autopilotWakeInput"', self.html)
        self.assertIn('id="autopilotGymPrefSelect"', self.html)
        self.assertIn('id="autopilotHighlightsContainer"', self.html)
        self.assertIn('id="autopilotTimelineDiffContainer"', self.html)
        self.assertIn('id="btnUndoAutopilot"', self.html)

    def test_03_autopilot_js_engine(self):
        """Autopilot scheduling, calculation, apply, and undo functions must exist."""
        self.assertIn('function openScheduleAutopilotModal()', self.html)
        self.assertIn('function closeScheduleAutopilotModal()', self.html)
        self.assertIn('function calculateAutopilotSchedule(', self.html)
        self.assertIn('function recalculateAutopilotPreview()', self.html)
        self.assertIn('function applyAutopilotSchedule()', self.html)
        self.assertIn('function undoAutopilotSchedule()', self.html)
        self.assertIn('function getAutopilotCategoryColor(', self.html)

    def test_04_cross_domain_insights_dom(self):
        """Cross-domain insights card container and badge must exist."""
        self.assertIn('id="cardCrossDomainInsights"', self.html)
        self.assertIn('id="crossDomainInsightsContainer"', self.html)
        self.assertIn('id="crossDomainInsightsBadge"', self.html)

    def test_05_cross_domain_insights_engine(self):
        """Cross-domain insights generation and rendering functions must exist and be hooked."""
        self.assertIn('function generateCrossDomainInsights()', self.html)
        self.assertIn('function renderCrossDomainInsights()', self.html)
        # Verify it is invoked within renderOverview
        render_overview_idx = self.html.find('function renderOverview(){')
        self.assertNotEqual(render_overview_idx, -1)
        render_overview_body = self.html[render_overview_idx:render_overview_idx+600]
        self.assertIn('renderCrossDomainInsights();', render_overview_body)

    def test_06_auto_backup_settings_dom(self):
        """Auto backup settings row, toggle switch, and interval dropdown must exist."""
        self.assertIn('id="autoBackupSettingsRow"', self.html)
        self.assertIn('id="chkAutoBackupEnabled"', self.html)
        self.assertIn('id="selAutoBackupInterval"', self.html)

    def test_07_auto_backup_engine(self):
        """Auto backup initialization, toggle, interval update, and execution must exist and be hooked."""
        self.assertIn('function initAutoBackupSettings()', self.html)
        self.assertIn('function toggleAutoBackupEnabled(', self.html)
        self.assertIn('function updateAutoBackupInterval(', self.html)
        self.assertIn('async function checkAndExecuteAutoBackup()', self.html)
        # Verify it is called on initialization
        self.assertIn('initAutoBackupSettings();', self.html)
        self.assertIn('checkAndExecuteAutoBackup();', self.html)

    def test_08_android_notification_action_receiver(self):
        """NotificationActionReceiver.kt must exist and handle actions."""
        self.assertTrue(os.path.exists(NOTIF_RECEIVER_PATH), f"Missing: {NOTIF_RECEIVER_PATH}")
        with open(NOTIF_RECEIVER_PATH, "r", encoding="utf-8") as f:
            code = f.read()
        self.assertIn("class NotificationActionReceiver : BroadcastReceiver", code)
        self.assertIn("ACTION_QUICK_WATER", code)
        self.assertIn("ACTION_MARK_DONE", code)
        self.assertIn("WaterWidgetProvider.ACTION_ADD_WATER", code)

    def test_09_android_notification_manager_actions(self):
        """ZatoonaNotificationManager must attach actions for water and mark done."""
        with open(NOTIF_MANAGER_PATH, "r", encoding="utf-8") as f:
            code = f.read()
        self.assertIn("NotificationActionReceiver.ACTION_QUICK_WATER", code)
        self.assertIn("NotificationActionReceiver.ACTION_MARK_DONE", code)
        self.assertIn("+1 كوب ماء 💧", code)
        self.assertIn("builder.addAction", code)

    def test_10_android_manifest_and_proguard(self):
        """NotificationActionReceiver must be registered in Manifest and preserved in Proguard."""
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = f.read()
        self.assertIn('android:name=".NotificationActionReceiver"', manifest)
        self.assertIn('android:name="com.zatoona.app.ACTION_QUICK_WATER"', manifest)
        self.assertIn('android:name="com.zatoona.app.ACTION_MARK_DONE"', manifest)

        with open(PROGUARD_PATH, "r", encoding="utf-8") as f:
            proguard = f.read()
        self.assertIn("keep class com.zatoona.app.NotificationActionReceiver", proguard)

if __name__ == "__main__":
    unittest.main()

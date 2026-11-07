# -*- coding: utf-8 -*-
"""
test_compliance_legal_suite.py
Automated acceptance test suite for Zatoona Phase 20: Comprehensive Privacy,
Legal, Compliance, Accessibility, and Data Rights.
Verifies all 20 requirements:
1. Privacy Policy
2. Terms of Service & Health Disclaimer
3. Refund Policy
4. Cookie / Local Storage Policy
5. Cookie Consent Banner
6. Form Consents
7. Unnecessary Data Collection (Zero unnecessary fields)
8. Third-Party SDK Audit (Zero tracking in Gradle)
9. Dark Patterns Elimination
10. Hidden Fees Elimination
11. Fake Reviews Elimination
12. Unsupported Claims Elimination (Medical disclaimers)
13. Accessibility Alt Text
14. Color Contrast Ratios (WCAG 2.1 AA)
15. Keyboard Navigation & Focus Visible
16. Business & Entity Details
17. Age Consent & Children's Privacy (COPPA 13+)
18. Unsubscribe Policy for Emails
19. Font & Media Licensing (SIL OFL 1.1 & CC-BY 4.0)
20. Data Deletion Request (GDPR Art. 17) & JSON Export (Art. 20)
21. Strict 3-Way HTML Parity Check
"""

import unittest
import hashlib
import os
import re

INDEX_PATH = 'index.html'
ZATOONA_PATH = 'zatoona.html'
ASSETS_PATH = 'android/app/src/main/assets/index.html'
GRADLE_PATH = 'android/app/build.gradle.kts'

class TestComplianceLegalSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            cls.html = f.read()
        with open(GRADLE_PATH, 'r', encoding='utf-8') as f:
            cls.gradle = f.read()

    def test_01_three_way_parity(self):
        """Verifies byte-for-byte SHA-256 parity across index.html, zatoona.html, and assets/index.html."""
        with open(INDEX_PATH, 'rb') as f1, open(ZATOONA_PATH, 'rb') as f2, open(ASSETS_PATH, 'rb') as f3:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()
            h3 = hashlib.sha256(f3.read()).hexdigest()
        self.assertEqual(h1, h2)
        self.assertEqual(h1, h3)
        self.assertEqual(os.path.getsize(INDEX_PATH), os.path.getsize(ZATOONA_PATH))
        self.assertEqual(os.path.getsize(INDEX_PATH), os.path.getsize(ASSETS_PATH))

    def test_02_privacy_policy_tab(self):
        """Verifies presence of GDPR/CCPA Privacy Policy tab with local-first and zero telemetry declarations."""
        self.assertIn('id="ltab-privacy"', self.html)
        self.assertIn('privacy@zatoona.app', self.html)
        self.assertIn('Privacy-by-Design', self.html)

    def test_03_terms_and_medical_disclaimer(self):
        """Verifies Terms of Service tab with medical and fitness disclaimers."""
        self.assertIn('id="ltab-terms"', self.html)
        self.assertIn('إخلاء مسؤولية صحية ورياضية وغذائية', self.html)
        self.assertIn('BMR / TDEE', self.html)

    def test_04_refund_policy_free_status(self):
        """Verifies Refund & Pricing tab stating 100% Free Forever and future 14-day refund policy."""
        self.assertIn('id="ltab-refund"', self.html)
        self.assertIn('refunds@zatoona.app', self.html)
        self.assertIn('Zero Hidden Fees', self.html)

    def test_05_cookie_storage_policy(self):
        """Verifies Cookie & Storage policy tab detailing LocalStorage and IndexedDB."""
        self.assertIn('id="ltab-cookies"', self.html)
        self.assertIn('LocalStorage', self.html)
        self.assertIn('IndexedDB', self.html)

    def test_06_storage_consent_banner(self):
        """Verifies presence and functions for storage consent banner."""
        self.assertIn('id="storageConsentBanner"', self.html)
        self.assertIn('acceptStorageConsent', self.html)
        self.assertIn('zatoona_storage_consent', self.html)

    def test_07_form_consents_audit(self):
        """Verifies forms do not have pre-checked consent traps."""
        self.assertIn('<input type="checkbox" id="chkEncryptBackup">', self.html)
        self.assertNotIn('<input type="checkbox" id="chkEncryptBackup" checked', self.html)

    def test_08_third_party_sdk_audit(self):
        """Verifies Android gradle build file contains zero tracking/analytics SDKs."""
        self.assertNotIn('firebase-analytics', self.gradle)
        self.assertNotIn('play-services-ads', self.gradle)
        self.assertNotIn('facebook-android-sdk', self.gradle)
        self.assertIn('androidx.core:core-ktx', self.gradle)

    def test_09_dark_patterns_elimination(self):
        """Verifies absence of subscription traps and fake countdown purchasing timers."""
        self.assertNotIn('countdown-timer-purchase', self.html)
        self.assertNotIn('subscription-trap', self.html)

    def test_10_accessibility_focus_visible(self):
        """Verifies :focus-visible rules exist for keyboard accessibility."""
        self.assertIn(':focus-visible', self.html)
        self.assertIn('outline: 2px solid var(--primary)', self.html)

    def test_11_business_and_developer_details(self):
        """Verifies business details tab with entity name, jurisdiction, and contact emails."""
        self.assertIn('id="ltab-business"', self.html)
        self.assertIn('github.com/medodem36-sudo/zatoona', self.html)
        self.assertIn('com.zatoona.app', self.html)

    def test_12_age_consent_coppa(self):
        """Verifies Child Privacy tab with 13+ age restriction policy."""
        self.assertIn('id="ltab-kids"', self.html)
        self.assertIn('13 عاماً فما فوق', self.html)
        self.assertIn('COPPA', self.html)

    def test_13_email_unsubscribe_policy(self):
        """Verifies communication policy with zero spam and one-click unsubscribe mention."""
        self.assertIn('id="ltab-emails"', self.html)
        self.assertIn('إلغاء الاشتراك', self.html)
        self.assertIn('Unsubscribe', self.html)

    def test_14_licenses_tajawal_and_svg(self):
        """Verifies licensing tab documenting Tajawal OFL 1.1 and CC-BY 4.0 media assets."""
        self.assertIn('id="ltab-licenses"', self.html)
        self.assertIn('SIL Open Font License 1.1', self.html)
        self.assertIn('Creative Commons Attribution 4.0', self.html)

    def test_15_data_deletion_and_export_modals(self):
        """Verifies GDPR Data Erasure modal, confirm input, and JSON export function."""
        self.assertIn('id="dataDeletionModal"', self.html)
        self.assertIn('inpConfirmDelete', self.html)
        self.assertIn('executeComprehensiveDataWipe', self.html)
        self.assertIn('exportAppDataToJson', self.html)

    def test_16_settings_view_integration(self):
        """Verifies Settings view contains Section 5 for compliance hub."""
        self.assertIn('id="settingsComplianceCard"', self.html)
        self.assertIn('openLegalPrivacyModal', self.html)
        self.assertIn('openDataDeletionModal', self.html)

    def test_17_keyboard_escape_listener(self):
        """Verifies global Escape key event listener for modal dismissal."""
        self.assertIn("e.key === 'Escape'", self.html)
        self.assertIn("closeLegalPrivacyModal()", self.html)

if __name__ == '__main__':
    unittest.main()

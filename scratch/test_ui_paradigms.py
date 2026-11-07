# -*- coding: utf-8 -*-
"""
test_ui_paradigms.py
Unit and integration test suite for Zatoona UI Design Paradigms Engine.
Tests:
- 5 comprehensive paradigms (botanical, cyber, glass, editorial, brutalist)
- Bootloader script in <head>
- Scoped CSS rules and variables
- Tactile Brutalist active transforms
- Frosted Glass backdrop filters
- Cyber HUD border styling
- Minimal Editorial flat shadows
- Settings view and modal selector buttons
- JavaScript engine functions and window exposure
- Strict 3-way HTML parity
"""

import unittest
import hashlib
import os
import re

INDEX_PATH = 'index.html'
ZATOONA_PATH = 'zatoona.html'
ASSETS_PATH = 'android/app/src/main/assets/index.html'

class TestUiParadigms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            cls.html = f.read()

    def test_01_three_way_parity(self):
        """Verifies byte-for-byte SHA-256 parity across all 3 entrypoints."""
        with open(INDEX_PATH, 'rb') as f1, open(ZATOONA_PATH, 'rb') as f2, open(ASSETS_PATH, 'rb') as f3:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()
            h3 = hashlib.sha256(f3.read()).hexdigest()
        sz1 = os.path.getsize(INDEX_PATH)
        sz2 = os.path.getsize(ZATOONA_PATH)
        sz3 = os.path.getsize(ASSETS_PATH)

        self.assertEqual(h1, h2, "index.html and zatoona.html hash mismatch")
        self.assertEqual(h1, h3, "index.html and assets/index.html hash mismatch")
        self.assertEqual(sz1, sz2, "File sizes differ between index and zatoona")
        self.assertEqual(sz1, sz3, "File sizes differ between index and assets")

    def test_02_head_bootloader(self):
        """Checks instant bootloader script sets data-ui-paradigm from zatoona-ui-paradigm-v1."""
        self.assertIn("localStorage.getItem('zatoona-ui-paradigm-v1')", self.html)
        self.assertIn("document.documentElement.setAttribute('data-ui-paradigm', p)", self.html)

    def test_03_css_paradigms_declared(self):
        """Verifies all 5 comprehensive design paradigms are styled via CSS."""
        paradigms = ['botanical', 'cyber', 'glass', 'editorial', 'brutalist']
        for p in paradigms:
            pattern = rf'\[data-ui-paradigm="{p}"\]'
            self.assertTrue(re.search(pattern, self.html), f"Missing CSS selector for paradigm: {p}")

    def test_04_cyber_tactical_properties(self):
        """Verifies Cyber Tactical styling: 4px radius, HUD borders, glowing shadows."""
        self.assertIn('[data-ui-paradigm="cyber"]', self.html)
        self.assertIn('--radius: 4px !important;', self.html)
        self.assertIn('--radius-sm: 2px !important;', self.html)
        self.assertIn('rgba(16, 185, 129, 0.45)', self.html)

    def test_05_liquid_glassmorphism_properties(self):
        """Verifies Glassmorphism styling: backdrop-filter blur, specular borders, 20px radius."""
        self.assertIn('[data-ui-paradigm="glass"]', self.html)
        self.assertIn('backdrop-filter: blur(18px)', self.html)
        self.assertIn('-webkit-backdrop-filter: blur(18px)', self.html)
        self.assertIn('--radius: 20px !important;', self.html)

    def test_06_minimalist_editorial_properties(self):
        """Verifies Minimal Editorial styling: zero shadow, hairline line, 6px radius."""
        self.assertIn('[data-ui-paradigm="editorial"]', self.html)
        self.assertIn('--radius: 6px !important;', self.html)
        self.assertIn('--shadow: none !important;', self.html)

    def test_07_neo_brutalism_tactile_press(self):
        """Verifies Neo-Brutalism: 2.5px heavy border, 4px hard shadow, mechanical button press displacement."""
        self.assertIn('[data-ui-paradigm="brutalist"]', self.html)
        self.assertIn('border: 2.5px solid #1E2923 !important;', self.html)
        self.assertIn('box-shadow: 4px 4px 0px #1E2923 !important;', self.html)
        self.assertIn('transform: translate(2px, 2px) !important;', self.html)

    def test_08_settings_view_selector_presence(self):
        """Verifies settings view contains #settingsParadigmGrid with all 5 paradigm options."""
        self.assertIn('id="settingsParadigmGrid"', self.html)
        paradigms = ['botanical', 'cyber', 'glass', 'editorial', 'brutalist']
        for p in paradigms:
            self.assertIn(f'data-paradigm-choice="{p}"', self.html)

    def test_09_theme_customizer_modal_selector_presence(self):
        """Verifies theme customizer modal contains #modalParadigmGrid with all 5 paradigm options."""
        self.assertIn('id="modalParadigmGrid"', self.html)

    def test_10_js_engine_functions(self):
        """Verifies JavaScript functions for loading, setting, and updating paradigms."""
        functions = [
            'function loadUiParadigm()',
            'function setUiParadigm(',
            'function selectParadigmChoice(',
            'function updateParadigmActiveStates(',
            'window.loadUiParadigm = loadUiParadigm;',
            'window.setUiParadigm = setUiParadigm;',
            'window.selectParadigmChoice = selectParadigmChoice;',
            'window.updateParadigmActiveStates = updateParadigmActiveStates;'
        ]
        for fn in functions:
            self.assertIn(fn, self.html, f"Missing JS function or export: {fn}")

if __name__ == '__main__':
    unittest.main()

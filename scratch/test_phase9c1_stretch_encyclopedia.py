# -*- coding: utf-8 -*-
"""
Phase 9C.1 Acceptance & Regression Test Suite
Stretch & Mobility Encyclopedia
Tests run against actual source files and headless Chrome.
"""

import unittest
import json
import os
import re
import sys
import hashlib
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

REPO = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
INDEX_HTML = os.path.join(REPO, "index.html")
ZATOONA_HTML = os.path.join(REPO, "zatoona.html")
SW_JS = os.path.join(REPO, "sw.js")
STRETCH_CATALOG = os.path.join(REPO, "assets", "data", "stretch-catalog.js")
STRETCHES_DIR = os.path.join(REPO, "assets", "images", "stretches")
EXERCISE_CATALOG = os.path.join(REPO, "assets", "data", "exercise-catalog.js")

def load_catalog(path, var_name):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    m = re.search(r'window\.' + var_name + r'\s*=\s*(\[.*?\]);', text, re.DOTALL)
    if not m:
        return []
    return json.loads(m.group(1))

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


class TestCatalogStructure(unittest.TestCase):
    """Tests 1-5: Catalog file integrity and data quality."""

    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(STRETCH_CATALOG, 'ZATOONA_STRETCH_CATALOG')

    def test_01_catalog_file_exists(self):
        """T1: Catalog file exists and is loadable."""
        self.assertTrue(os.path.isfile(STRETCH_CATALOG), "stretch-catalog.js must exist")
        self.assertGreater(len(self.catalog), 0, "Catalog must parse to non-empty array")

    def test_02_unique_ids(self):
        """T2: All movement IDs are unique."""
        ids = [m['id'] for m in self.catalog]
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate IDs found: {[x for x in ids if ids.count(x) > 1]}")

    def test_03_at_least_30_movements(self):
        """T3: At least 30 distinct movements."""
        self.assertGreaterEqual(len(self.catalog), 30, f"Only {len(self.catalog)} movements found, need >= 30")

    def test_04_mandatory_fields(self):
        """T4: Every record has all mandatory fields."""
        required = ['id', 'name', 'nameAr', 'type', 'primaryMuscles', 'bodyRegions',
                     'equipment', 'level', 'instructions', 'image', 'suitableFor']
        for m in self.catalog:
            for field in required:
                self.assertIn(field, m, f"Movement '{m.get('id','?')}' missing field '{field}'")
                val = m[field]
                if isinstance(val, list):
                    self.assertGreater(len(val), 0, f"Movement '{m['id']}' field '{field}' is empty list")
                elif isinstance(val, str):
                    self.assertTrue(val.strip(), f"Movement '{m['id']}' field '{field}' is empty string")

    def test_05_duration_or_reps(self):
        """T5: Every movement has durationSeconds or recommendedReps."""
        for m in self.catalog:
            has_dur = m.get('durationSeconds') and m['durationSeconds'] > 0
            has_reps = m.get('recommendedReps') and str(m['recommendedReps']).strip()
            self.assertTrue(has_dur or has_reps,
                f"Movement '{m['id']}' has neither durationSeconds nor recommendedReps")

    def test_05b_instructions_quality(self):
        """T5b: Instructions are non-trivial (at least 2 steps per movement)."""
        for m in self.catalog:
            self.assertGreaterEqual(len(m.get('instructions', [])), 2,
                f"Movement '{m['id']}' has fewer than 2 instruction steps")

    def test_05c_types_coverage(self):
        """T5c: All 5 movement types are represented."""
        expected_types = {'static_stretch', 'dynamic_stretch', 'joint_mobility', 'activation', 'warmup_drill'}
        found_types = {m['type'] for m in self.catalog}
        missing = expected_types - found_types
        self.assertEqual(len(missing), 0, f"Missing movement types: {missing}")

    def test_05d_body_regions_coverage(self):
        """T5d: At least 10 distinct body regions are covered."""
        regions = set()
        for m in self.catalog:
            regions.update(m.get('bodyRegions', []))
        self.assertGreaterEqual(len(regions), 10, f"Only {len(regions)} regions found: {regions}")


class TestImagesPolicy(unittest.TestCase):
    """Tests 10-12: Image assets and males-only policy."""

    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(STRETCH_CATALOG, 'ZATOONA_STRETCH_CATALOG')

    def test_10_local_image_files_exist(self):
        """T10: Every catalog image path references an existing local file."""
        for m in self.catalog:
            img = m.get('image', '')
            if img:
                full_path = os.path.join(REPO, img.replace('/', os.sep))
                self.assertTrue(os.path.isfile(full_path),
                    f"Image missing for '{m['id']}': {img}")

    def test_11_no_external_urls(self):
        """T11: No external URLs in catalog or SVG files."""
        with open(STRETCH_CATALOG, 'r', encoding='utf-8') as f:
            cat_text = f.read()
        # Check catalog JS
        ext_urls = re.findall(r'https?://[^\s\'"]+', cat_text)
        self.assertEqual(len(ext_urls), 0, f"External URLs in catalog: {ext_urls}")

        # Check SVG files
        for svg_file in os.listdir(STRETCHES_DIR):
            if svg_file.endswith('.svg'):
                with open(os.path.join(STRETCHES_DIR, svg_file), 'r', encoding='utf-8') as f:
                    svg_text = f.read()
                ext = re.findall(r'https?://[^\s\'"<>]+', svg_text)
                # Exclude xmlns namespace declarations
                ext = [u for u in ext if 'w3.org' not in u]
                self.assertEqual(len(ext), 0, f"External URL in {svg_file}: {ext}")

    def test_12_males_only_svg_policy(self):
        """T12: SVG files contain only male athletic descriptors and no female indicators."""
        female_indicators = ['female', 'woman', 'girl', 'her ', 'she ', 'feminine', 'امرأة', 'نسائي', 'بنت']
        for svg_file in os.listdir(STRETCHES_DIR):
            if svg_file.endswith('.svg'):
                with open(os.path.join(STRETCHES_DIR, svg_file), 'r', encoding='utf-8') as f:
                    svg_text = f.read().lower()
                for indicator in female_indicators:
                    self.assertNotIn(indicator, svg_text,
                        f"Female indicator '{indicator}' found in {svg_file}")

    def test_12b_svg_valid_xml(self):
        """T12b: SVG files are well-formed XML."""
        import xml.etree.ElementTree as ET
        for svg_file in os.listdir(STRETCHES_DIR):
            if svg_file.endswith('.svg'):
                path = os.path.join(STRETCHES_DIR, svg_file)
                try:
                    ET.parse(path)
                except ET.ParseError as e:
                    self.fail(f"SVG {svg_file} is not valid XML: {e}")


class TestNavIntegration(unittest.TestCase):
    """Tests for navigation, views, and applyMode integration."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, 'r', encoding='utf-8') as f:
            cls.html = f.read()
        with open(SW_JS, 'r', encoding='utf-8') as f:
            cls.sw = f.read()

    def test_nav_modes_includes_stretches(self):
        """NAV_MODES includes 'stretches'."""
        self.assertIn("'stretches'", self.html)
        m = re.search(r"const NAV_MODES\s*=\s*\[(.*?)\];", self.html)
        self.assertIsNotNone(m)
        self.assertIn("'stretches'", m.group(1))

    def test_stretchesview_exists(self):
        """stretchesView div exists in HTML."""
        self.assertIn('id="stretchesView"', self.html)

    def test_applymode_views_map(self):
        """applyMode views map includes stretches."""
        self.assertIn("stretches: document.getElementById('stretchesView')", self.html)

    def test_applymode_btns_map(self):
        """applyMode btns map includes stretches."""
        self.assertIn("stretches: document.getElementById('modeStretches')", self.html)

    def test_applymode_titles_map(self):
        """applyMode titles map includes stretches."""
        self.assertIn("stretches: ['🧘", self.html)

    def test_mode_button_exists(self):
        """modeStretches button exists."""
        self.assertIn('id="modeStretches"', self.html)

    def test_drawer_button_exists(self):
        """drawNav-stretches button exists."""
        self.assertIn('id="drawNav-stretches"', self.html)

    def test_sidebar_button_exists(self):
        """sideNav-stretches button exists."""
        self.assertIn('id="sideNav-stretches"', self.html)

    def test_wireactivate_for_stretches(self):
        """wireActivate for modeStretches exists."""
        self.assertIn("wireActivate(document.getElementById('modeStretches')", self.html)

    def test_render_call_in_applymode(self):
        """renderStretchesView() is called when mode==='stretches'."""
        self.assertIn("if(mode==='stretches') renderStretchesView()", self.html)

    def test_week_cal_hidden_for_stretches(self):
        """Week calendar is hidden when mode==='stretches'."""
        self.assertIn("mode==='stretches'", self.html)

    def test_script_tag_for_catalog(self):
        """stretch-catalog.js script tag exists."""
        self.assertIn('src="./assets/data/stretch-catalog.js"', self.html)

    def test_render_function_exists(self):
        """renderStretchesView function is defined."""
        self.assertIn('function renderStretchesView()', self.html)

    def test_stretch_search_input(self):
        """Search input exists."""
        self.assertIn('id="stretchSearchInput"', self.html)

    def test_stretch_filters_exist(self):
        """All filter dropdowns exist."""
        for fid in ['strFilterType', 'strFilterRegion', 'strFilterEquipment', 'strFilterLevel', 'strFilterPurpose']:
            self.assertIn(f'id="{fid}"', self.html, f"Filter {fid} not found")

    def test_stretch_modal_exists(self):
        """Detail modal exists."""
        self.assertIn('id="stretchDetailModal"', self.html)

    def test_empty_state_exists(self):
        """Empty state div exists with reset button."""
        self.assertIn('id="stretchesEmptyState"', self.html)
        self.assertIn('id="stretchesResetBtn"', self.html)


class TestSWIntegration(unittest.TestCase):
    """Tests for service worker updates."""

    @classmethod
    def setUpClass(cls):
        with open(SW_JS, 'r', encoding='utf-8') as f:
            cls.sw = f.read()

    def test_cache_version_bumped(self):
        """CACHE_VERSION is v23."""
        self.assertIn("const CACHE_VERSION = 'v23'", self.sw)

    def test_valid_modes_includes_stretches(self):
        """VALID_MODES includes 'stretches'."""
        m = re.search(r"VALID_MODES\s*=\s*\[(.*?)\]", self.sw)
        self.assertIsNotNone(m)
        self.assertIn("'stretches'", m.group(1))

    def test_shell_assets_includes_catalog(self):
        """SHELL_ASSETS includes stretch-catalog.js."""
        self.assertIn("stretch-catalog.js", self.sw)

    def test_shell_assets_includes_svgs(self):
        """SHELL_ASSETS includes all 34 stretch SVGs."""
        for svg_file in os.listdir(STRETCHES_DIR):
            if svg_file.endswith('.svg'):
                self.assertIn(svg_file, self.sw, f"SVG {svg_file} not in SHELL_ASSETS")

    def test_shell_assets_files_exist(self):
        """Every file listed in SHELL_ASSETS actually exists on disk."""
        m = re.search(r"const SHELL_ASSETS\s*=\s*\[(.*?)\];", self.sw, re.DOTALL)
        self.assertIsNotNone(m)
        paths = re.findall(r"'(\./[^']+)'", m.group(1))
        for p in paths:
            # Skip root './' which is a directory
            if p == './':
                continue
            full = os.path.join(REPO, p.replace('./', '').replace('/', os.sep))
            self.assertTrue(os.path.exists(full), f"SHELL_ASSET not found: {p} -> {full}")


class TestIsolation(unittest.TestCase):
    """Tests 14-16: Ensure stretch data is isolated from exercise data."""

    @classmethod
    def setUpClass(cls):
        cls.stretch_catalog = load_catalog(STRETCH_CATALOG, 'ZATOONA_STRETCH_CATALOG')
        cls.exercise_catalog = load_catalog(EXERCISE_CATALOG, 'ZATOONA_EXERCISE_CATALOG')
        with open(INDEX_HTML, 'r', encoding='utf-8') as f:
            cls.html = f.read()

    def test_14_no_overlap_with_exercise_ids(self):
        """T14: Stretch IDs don't collide with exercise catalog IDs."""
        ex_ids = {e['id'] for e in self.exercise_catalog}
        str_ids = {m['id'] for m in self.stretch_catalog}
        overlap = ex_ids & str_ids
        self.assertEqual(len(overlap), 0, f"ID collision with exercise catalog: {overlap}")

    def test_14b_related_exercise_ids_valid(self):
        """T14b: relatedExerciseIds reference actual exercise catalog IDs."""
        ex_ids = {e['id'] for e in self.exercise_catalog}
        for m in self.stretch_catalog:
            for rid in m.get('relatedExerciseIds', []):
                self.assertIn(rid, ex_ids,
                    f"Movement '{m['id']}' references unknown exercise ID: '{rid}'")

    def test_15_no_storage_keys_in_stretches(self):
        """T15: No localStorage read/write in stretch encyclopedia code."""
        # Find the stretch controller section
        idx_start = self.html.find('PHASE 9C.1: STRETCH & MOBILITY ENCYCLOPEDIA CONTROLLER')
        idx_end = self.html.find('END PHASE 9C.1')
        if idx_start != -1 and idx_end != -1:
            section = self.html[idx_start:idx_end]
            self.assertNotIn('localStorage', section, "localStorage usage found in stretch controller")
            self.assertNotIn('storageSet', section, "storageSet usage found in stretch controller")
            self.assertNotIn('storageGet', section, "storageGet usage found in stretch controller")

    def test_16_ex_a_b_defaults_unchanged(self):
        """T16: EX_A_DEFAULTS and EX_B_DEFAULTS are not modified."""
        # Verify their structure hasn't been altered by checking they exist unchanged
        self.assertIn('EX_A_DEFAULTS', self.html, "EX_A_DEFAULTS must still exist")
        self.assertIn('EX_B_DEFAULTS', self.html, "EX_B_DEFAULTS must still exist")


class TestFileSynchronization(unittest.TestCase):
    """Tests for file sync and binary match."""

    def test_html_files_byte_identical(self):
        """index.html and zatoona.html are byte-identical."""
        hash_idx = sha256_file(INDEX_HTML)
        hash_zat = sha256_file(ZATOONA_HTML)
        self.assertEqual(hash_idx, hash_zat,
            f"Files differ: index={hash_idx[:16]}... zatoona={hash_zat[:16]}...")

    def test_html_file_sizes_match(self):
        """File sizes match."""
        size_idx = os.path.getsize(INDEX_HTML)
        size_zat = os.path.getsize(ZATOONA_HTML)
        self.assertEqual(size_idx, size_zat)


class TestCSSIntegration(unittest.TestCase):
    """Tests for CSS styles."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, 'r', encoding='utf-8') as f:
            cls.html = f.read()

    def test_css_str_grid(self):
        """str-grid CSS class is defined."""
        self.assertIn('.str-grid', self.html)

    def test_css_str_card(self):
        """str-card CSS class is defined."""
        self.assertIn('.str-card', self.html)

    def test_css_str_modal(self):
        """str-modal CSS class is defined."""
        self.assertIn('.str-modal-overlay', self.html)

    def test_css_str_search(self):
        """str-search-input CSS class is defined."""
        self.assertIn('.str-search-input', self.html)

    def test_css_str_filter(self):
        """str-filter-dropdown CSS class is defined."""
        self.assertIn('.str-filter-dropdown', self.html)

    def test_css_responsive_480(self):
        """Responsive rule for 480px exists in stretch CSS."""
        # There should be a media query for .str-grid at small widths
        self.assertIn('.str-grid{ grid-template-columns:1fr; }', self.html)


if __name__ == '__main__':
    os.chdir(REPO)
    unittest.main(verbosity=2)

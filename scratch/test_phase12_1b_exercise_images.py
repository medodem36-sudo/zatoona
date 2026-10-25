#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 12.1B — Curated Exercise Catalog Images Test Suite
========================================================
Verifies:
- All referenced SVG image files in exercise-catalog.js exist on disk with valid size.
- 100% valid SVG XML structure with viewBox "0 0 300 200".
- Zero external image URLs (offline-first).
- 100% coverage of all 26 unique exercises in GYM_PLAN_TEMPLATE_REGISTRY.
- User custom image precedence in exercise cards.
- sw.js cache bump to v24 and inclusion of all 19 new SVGs in SHELL_ASSETS.
- Binary identity between index.html and zatoona.html.
"""

import os
import re
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path

# UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent

passed_checks = 0
failed_checks = 0

def check(condition, desc):
    global passed_checks, failed_checks
    if condition:
        passed_checks += 1
        print(f"  [PASS] {desc}")
    else:
        failed_checks += 1
        print(f"  [FAIL] {desc}")

print("=" * 80)
print("PHASE 12.1B — CURATED EXERCISE CATALOG IMAGES TEST SUITE")
print("=" * 80)

# 1. Load exercise-catalog.js
cat_file = REPO_ROOT / "assets" / "data" / "exercise-catalog.js"
check(cat_file.exists(), f"exercise-catalog.js exists at {cat_file.relative_to(REPO_ROOT)}")

with open(cat_file, "r", encoding="utf-8") as f:
    cat_text = f.read()

m_cat = re.search(r"window\.ZATOONA_EXERCISE_CATALOG\s*=\s*(\[[\s\S]*?\]);", cat_text)
check(bool(m_cat), "window.ZATOONA_EXERCISE_CATALOG array parsed successfully")
catalog = json.loads(m_cat.group(1)) if m_cat else []
check(len(catalog) == 119, f"Catalog has exactly 119 exercises (found {len(catalog)})")

cat_map = {e["id"]: e for e in catalog}

# 2. Check 19 newly created SVG files
req_19 = [
    "barbell_back_squat",
    "conventional_deadlift",
    "incline_barbell_bench_press",
    "incline_dumbbell_press",
    "dumbbell_bench_press",
    "seated_cable_row",
    "leg_press",
    "seated_dumbbell_shoulder_press",
    "hanging_leg_raise",
    "standing_dumbbell_lateral_raise",
    "barbell_curl",
    "hammer_curl",
    "triceps_rope_pushdown",
    "skull_crushers",
    "dumbbell_chest_flyes",
    "lying_leg_curl_machine",
    "seated_leg_curl_machine",
    "standing_calf_raise_machine",
    "seated_palms_up_wrist_curl"
]

print("\n--- 1. Verifying 19 Curated Exercise SVGs on Disk ---")
all_19_exist = True
all_19_valid_xml = True
all_19_offline = True
all_19_reasonable_size = True

for eid in req_19:
    ex = cat_map.get(eid)
    check(bool(ex and ex.get("images") and len(ex["images"]) > 0), f"Catalog has image for '{eid}'")
    if ex and ex.get("images"):
        img_rel = ex["images"][0].lstrip("./")
        full_path = REPO_ROOT / img_rel
        if not full_path.exists() or full_path.stat().st_size == 0:
            all_19_exist = False
        else:
            # Check XML
            try:
                tree = ET.parse(full_path)
                root = tree.getroot()
                if not root.tag.endswith("svg") or root.attrib.get("viewBox") != "0 0 300 200":
                    all_19_valid_xml = False
            except Exception:
                all_19_valid_xml = False
            
            # Check size (between 1.5KB and 10KB)
            sz = full_path.stat().st_size
            if sz < 1500 or sz > 10000:
                all_19_reasonable_size = False
                
            # Check no external links inside SVG (excluding standard SVG namespace)
            with open(full_path, "r", encoding="utf-8") as svg_f:
                svg_content = svg_f.read()
                svg_no_ns = svg_content.replace("http://www.w3.org/2000/svg", "").replace("http://www.w3.org/1999/xlink", "")
                if "http://" in svg_no_ns or "https://" in svg_no_ns:
                    all_19_offline = False

check(all_19_exist, "All 19 new SVG files exist on disk with size > 0")
check(all_19_valid_xml, "All 19 new SVG files are valid XML with viewBox '0 0 300 200'")
check(all_19_reasonable_size, "All 19 new SVG files are lightweight (1.5KB - 10KB)")
check(all_19_offline, "All 19 new SVG files are 100% offline (no external http/https URLs)")

# 3. Check All Catalog-Referenced Images
print("\n--- 2. Verifying All Catalog Image References ---")
all_referenced_exist = True
no_ext_urls = True
catalog_with_imgs_count = 0

for ex in catalog:
    imgs = ex.get("images", [])
    if imgs:
        catalog_with_imgs_count += 1
        for img_url in imgs:
            if img_url.startswith(("http://", "https://")):
                no_ext_urls = False
            rel = img_url.lstrip("./")
            p = REPO_ROOT / rel
            if not p.exists() or p.stat().st_size == 0:
                all_referenced_exist = False

check(catalog_with_imgs_count >= 30, f"At least 30 catalog exercises have local images mapped (found {catalog_with_imgs_count})")
check(all_referenced_exist, "Every image path referenced in catalog exists on disk with non-zero size")
check(no_ext_urls, "Zero external URLs (http/https) in catalog images array")

# 4. Check Template Registry 100% Coverage (26 Unique Exercises)
print("\n--- 3. Verifying 100% Coverage of All 26 Preset Template Exercises ---")
with open(REPO_ROOT / "index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

m_reg = re.search(r"const\s+GYM_PLAN_TEMPLATE_REGISTRY\s*=\s*(\{[\s\S]*?\n\});", index_html)
check(bool(m_reg), "GYM_PLAN_TEMPLATE_REGISTRY found in index.html")

tpl_code = m_reg.group(1) if m_reg else ""
tpl_matches = re.findall(r"\{\s*templateExerciseId:\s*['\"]([^'\"]+)['\"]\s*,\s*catalogExerciseId:\s*['\"]([^'\"]+)['\"]\s*,\s*name:\s*['\"]([^'\"]+)['\"]", tpl_code)

check(len(tpl_matches) == 59, f"Preset templates contain exactly 59 exercise slots (found {len(tpl_matches)})")

distinct_tpl_cat_ids = sorted(list(set(m[1] for m in tpl_matches)))
check(len(distinct_tpl_cat_ids) == 26, f"Preset templates contain exactly 26 distinct catalog IDs (found {len(distinct_tpl_cat_ids)})")

templates_100_covered = True
for cid in distinct_tpl_cat_ids:
    cat = cat_map.get(cid)
    if not cat or not cat.get("images") or len(cat["images"]) == 0:
        templates_100_covered = False
        print(f"    Missing image for template exercise: {cid}")
    else:
        p = REPO_ROOT / cat["images"][0].lstrip("./")
        if not p.exists() or p.stat().st_size == 0:
            templates_100_covered = False
            print(f"    File missing for template exercise: {cid} -> {p}")

check(templates_100_covered, "100% of all 26 preset template exercises resolve a valid local SVG image")

# 5. Check Runtime Resolution and UI Image Support
print("\n--- 4. Verifying Runtime Image Resolution & Encyclopedia Support ---")
check("function transformTemplateExerciseToRuntime" in index_html, "transformTemplateExerciseToRuntime exists in index.html")
check("const img = (cat && Array.isArray(cat.images) && cat.images.length > 0) ? cat.images[0]" in index_html, "transformTemplateExerciseToRuntime reads cat.images[0]")

# Check Encyclopedia detail HTML image support
check("const defaultImg = (Array.isArray(ex.images) && ex.images.length > 0) ? ex.images[0]" in index_html, "renderEncyclopediaDetailHtml resolves defaultImg from ex.images[0]")
check("encImgSrc" in index_html and '<img src="${encEscape(encImgSrc)}"' in index_html, "renderEncyclopediaDetailHtml renders exercise illustration card")

# Check user custom image precedence
check("const imgRecord = (typeof getExerciseImageRecord === 'function') ? getExerciseImageRecord(ex.key) : null;" in index_html, "renderExercises checks getExerciseImageRecord before ex.img")
check("else if(ex.img){\n      displayImgSrc = ex.img;\n    }" in index_html or "else if(ex.img){\r\n      displayImgSrc = ex.img;\r\n    }" in index_html, "renderExercises falls back to ex.img only if no custom user image")

# 6. Check Service Worker & Shell Assets Precache
print("\n--- 5. Verifying Service Worker & SHELL_ASSETS Caching ---")
with open(REPO_ROOT / "sw.js", "r", encoding="utf-8") as f:
    sw_text = f.read()

m_sw_ver = re.search(r"const\s+CACHE_VERSION\s*=\s*'([^']+)';", sw_text)
sw_version = m_sw_ver.group(1) if m_sw_ver else ""
check(sw_version == "v24", f"Service Worker cache bumped to v24 (found '{sw_version}')")

m_shell = re.search(r"const\s+SHELL_ASSETS\s*=\s*(\[[\s\S]*?\]);", sw_text)
shell_assets = re.findall(r"['\"]([^'\"]+)['\"]", m_shell.group(1)) if m_shell else []

all_19_in_shell = True
for eid in req_19:
    cat = cat_map.get(eid)
    if cat and cat.get("images"):
        expected_ref = cat["images"][0]
        if expected_ref not in shell_assets:
            all_19_in_shell = False
            print(f"    Missing in SHELL_ASSETS: {expected_ref}")

check(all_19_in_shell, "All 19 newly created exercise SVGs are listed in SHELL_ASSETS in sw.js")

all_shell_exist = True
for a in shell_assets:
    rel = a.lstrip("./").replace("/", os.sep)
    if not rel:
        continue
    p = REPO_ROOT / rel
    if not p.exists() or p.stat().st_size == 0:
        all_shell_exist = False
        print(f"    Missing on disk from SHELL_ASSETS: {a}")

check(all_shell_exist, f"All {len(shell_assets)} SHELL_ASSETS exist on disk with size > 0")

# 7. Check index.html vs zatoona.html Binary Identity
print("\n--- 6. Verifying index.html and zatoona.html Identity ---")
with open(REPO_ROOT / "index.html", "rb") as f1, open(REPO_ROOT / "zatoona.html", "rb") as f2:
    idx_bytes = f1.read()
    zat_bytes = f2.read()

check(idx_bytes == zat_bytes, f"index.html and zatoona.html are 100% byte identical ({len(idx_bytes)} bytes)")

print("\n" + "=" * 80)
total_checks = passed_checks + failed_checks
print(f"PHASE 12.1B RESULTS: {passed_checks} PASSED, {failed_checks} FAILED (TOTAL {total_checks})")
print("=" * 80)

sys.exit(0 if failed_checks == 0 else 1)

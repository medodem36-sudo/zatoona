#!/usr/bin/env python3
"""
Acceptance Test Suite for Phase 13.6:
Pantry & Food Inventory Management (نظام إدارة المؤن والمخزون المنزلي للأطعمة)
Includes static code checks, runtime Selenium verification, and 3-way parity.
"""

import os
import sys
import json
import re
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO_ROOT, "index.html")

def run_tests():
    total = 0
    passed = 0
    failed = 0

    def check(name, condition, extra=""):
        nonlocal total, passed, failed
        total += 1
        if condition:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            failed += 1
            print(f"  [FAIL] {name}: {extra}")

    print("\n--- Testing Phase 13.6: Pantry & Food Inventory Static Checks ---")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Markup
    check("mealView has #pantryContainer", 'id="pantryContainer"' in html)
    check("has pantry section title in Arabic", "مخزون المؤن المنزلية" in html)
    check("has pantry section hint", "تابع الأطعمة والمؤن المتوفرة عندك بالمنزل" in html)

    # 2. Storage & Model Constants
    check("has PANTRY_STORAGE_KEY", "const PANTRY_STORAGE_KEY = 'pantry-inventory-v1'" in html or "PANTRY_STORAGE_KEY = 'pantry-inventory-v1'" in html)
    check("has DEFAULT_PANTRY_ITEMS", "DEFAULT_PANTRY_ITEMS" in html)
    check("has PANTRY_CATEGORIES", "PANTRY_CATEGORIES" in html)
    check("PANTRY_CATEGORIES defines protein, dairy, carbs, produce, staples",
          "protein:" in html and "dairy:" in html and "carbs:" in html and "produce:" in html and "staples:" in html)

    # 3. Core Functions
    check("has loadPantryItems", "function loadPantryItems(" in html)
    check("has savePantryItems", "function savePantryItems(" in html)
    check("has addPantryItem", "function addPantryItem(" in html)
    check("has updatePantryItem", "function updatePantryItem(" in html)
    check("has deletePantryItem", "function deletePantryItem(" in html)
    check("has adjustPantryQty", "function adjustPantryQty(" in html)
    check("has getPantryMetrics", "function getPantryMetrics(" in html)
    check("has transferCompletedShoppingToPantry", "function transferCompletedShoppingToPantry(" in html)
    check("has renderPantry", "function renderPantry(" in html)

    # 4. Rendering & Hooks
    check("renderShopping calls renderPantry", "renderPantry();" in html)
    check("window exports loadPantryItems", "window.loadPantryItems = loadPantryItems" in html)
    check("window exports savePantryItems", "window.savePantryItems = savePantryItems" in html)
    check("window exports addPantryItem", "window.addPantryItem = addPantryItem" in html)
    check("window exports updatePantryItem", "window.updatePantryItem = updatePantryItem" in html)
    check("window exports deletePantryItem", "window.deletePantryItem = deletePantryItem" in html)
    check("window exports adjustPantryQty", "window.adjustPantryQty = adjustPantryQty" in html)
    check("window exports getPantryMetrics", "window.getPantryMetrics = getPantryMetrics" in html)
    check("window exports transferCompletedShoppingToPantry", "window.transferCompletedShoppingToPantry = transferCompletedShoppingToPantry" in html)
    check("window exports renderPantry", "window.renderPantry = renderPantry" in html)

    # 5. UI Elements inside renderPantry
    check("renderPantry has metrics bar", "إجمالي الأصناف" in html and "نواقص المخزون" in html)
    check("renderPantry has category filter chips", "pantry-cat-btn" in html and 'data-cat="deficits"' in html)
    check("renderPantry has search input", 'id="pantrySearchInput"' in html)
    check("renderPantry has add/edit form", 'id="pantryAddForm"' in html)
    check("renderPantry has quick +/- stepper", "btn-pantry-step" in html)
    check("renderPantry has expiry warnings", "منتهي الصلاحية" in html and "ينتهي خلال" in html)
    check("renderPantry has transfer button", 'id="btnTransferShoppingToPantry"' in html)

    # 6. Backup & Storage Resilience
    check("KNOWN_KEY_PATTERNS contains pantry-inventory-v1", "/^pantry-inventory-v1$/" in html)
    check("validateBackupData validates pantry-inventory-v1", "pantry-inventory-v1" in html and "مخزون المؤن" in html)

    print("\n--- Testing Phase 13.6: Runtime Headless Chrome Verification ---")
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')

    driver = None
    try:
        driver = webdriver.Chrome(options=opts)
        file_url = 'file:///' + INDEX_PATH.replace('\\', '/')
        driver.get(file_url)

        # Runtime Test 1: loadPantryItems default items
        def_count = driver.execute_script("return window.loadPantryItems().length;")
        check("Runtime: loadPantryItems() returns default items", def_count == 4, f"got {def_count}")

        # Runtime Test 2: addPantryItem
        added_id = driver.execute_script("""
            const item = window.addPantryItem('تونة مصفاة', 'protein', 3, 'علبة', 1, '2027-01-01', 'دولاب المؤن');
            return item ? item.id : null;
        """)
        check("Runtime: addPantryItem() creates item with id", added_id is not None and added_id.startswith("pnt_"))

        count_after_add = driver.execute_script("return window.loadPantryItems().length;")
        check("Runtime: item count increments after add", count_after_add == 5, f"got {count_after_add}")

        # Runtime Test 3: adjustPantryQty
        new_qty = driver.execute_script(f"""
            window.adjustPantryQty('{added_id}', 1.5);
            const it = window.loadPantryItems().find(x => x.id === '{added_id}');
            return it ? it.qty : null;
        """)
        check("Runtime: adjustPantryQty() increments quantity", new_qty == 4.5, f"got {new_qty}")

        clamped_qty = driver.execute_script(f"""
            window.adjustPantryQty('{added_id}', -10);
            const it = window.loadPantryItems().find(x => x.id === '{added_id}');
            return it ? it.qty : null;
        """)
        check("Runtime: adjustPantryQty() clamps to 0", clamped_qty == 0, f"got {clamped_qty}")

        # Runtime Test 4: updatePantryItem
        updated_notes = driver.execute_script(f"""
            window.updatePantryItem('{added_id}', {{ qty: 5, notes: 'تمت إضافة شحنة جديدة' }});
            const it = window.loadPantryItems().find(x => x.id === '{added_id}');
            return it ? it.notes : null;
        """)
        check("Runtime: updatePantryItem() updates properties", updated_notes == 'تمت إضافة شحنة جديدة')

        # Runtime Test 5: getPantryMetrics
        metrics = driver.execute_script("return window.getPantryMetrics();")
        check("Runtime: getPantryMetrics() returns structure",
              isinstance(metrics, dict) and 'totalItems' in metrics and 'lowStockCount' in metrics and metrics['totalItems'] == 5)

        # Runtime Test 6: deletePantryItem
        deleted_ok = driver.execute_script(f"""
            window.deletePantryItem('{added_id}');
            return !window.loadPantryItems().some(x => x.id === '{added_id}');
        """)
        check("Runtime: deletePantryItem() removes item", deleted_ok)

        # Runtime Test 7: validateBackupData deep checks
        backup_valid = driver.execute_script("""
            const valid = {
                'pantry-inventory-v1': JSON.stringify([
                    { id: 'p1', name: 'أرز', category: 'carbs', qty: 2, unit: 'كجم', minQty: 1, expiryDate: '', notes: '', updatedAt: '2026-11-01' }
                ]),
                'theme': JSON.stringify('emerald')
            };
            return window.validateBackupData(valid).ok;
        """)
        check("Runtime: validateBackupData accepts valid pantry inventory", backup_valid is True)

        backup_corrupt = driver.execute_script("""
            const corrupt = {
                'pantry-inventory-v1': '{ invalid json ...',
                'theme': JSON.stringify('emerald')
            };
            return window.validateBackupData(corrupt);
        """)
        check("Runtime: validateBackupData rejects malformed pantry JSON",
              backup_corrupt.get('ok') is False and 'تالف' in backup_corrupt.get('reason', ''))

        backup_nonarray = driver.execute_script("""
            const nonarray = {
                'pantry-inventory-v1': JSON.stringify({ not: 'an array' }),
                'theme': JSON.stringify('emerald')
            };
            return window.validateBackupData(nonarray);
        """)
        check("Runtime: validateBackupData rejects non-array pantry data",
              backup_nonarray.get('ok') is False and 'مصفوفة' in backup_nonarray.get('reason', ''))

    except Exception as e:
        check("Runtime Selenium Execution", False, str(e))
    finally:
        if driver:
            driver.quit()

    print("\n--- Testing 3-Way HTML Parity ---")
    files = [
        "index.html",
        "zatoona.html",
        "android/app/src/main/assets/index.html"
    ]
    hashes = {}
    sizes = {}
    for p in files:
        full_p = os.path.join(REPO_ROOT, p)
        check(f"Parity file exists: {p}", os.path.isfile(full_p))
        if os.path.isfile(full_p):
            with open(full_p, "rb") as f:
                content = f.read()
            h = hashlib.sha256(content).hexdigest()
            hashes[p] = h
            sizes[p] = len(content)

    all_sizes_match = len(set(sizes.values())) == 1 and len(sizes) == 3
    all_hashes_match = len(set(hashes.values())) == 1 and len(hashes) == 3
    check("All 3 HTML files have identical sizes", all_sizes_match, f"Sizes: {sizes}")
    check("All 3 HTML files have identical SHA-256 hashes", all_hashes_match, f"Hashes: {hashes}")

    print(f"\n==========================================")
    print(f"Results: {passed} / {total} PASS ({failed} failed)")
    print(f"==========================================")

    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

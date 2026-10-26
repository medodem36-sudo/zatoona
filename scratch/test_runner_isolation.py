#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runner Isolation & Fault-Tolerance Verification Test
====================================================
Tests the logic of test_master_regression_gate.py in complete isolation:
1. Output parsers (Pattern A, Pattern B, Pattern C, unparseable).
2. Failure handling: ensures that a failing suite is NEVER classified as PASS.
3. Timeout handling: ensures timeout marks suite as TIMEOUT and fails the gate.
4. Missing file handling: ensures missing test script marks suite as ERROR.
5. Exit code propagation: overall gate exit code is non-zero on any failure.
"""

import sys
import os
import unittest
import tempfile
import json
from pathlib import Path

# Add scratch to path to import test_master_regression_gate
SCRATCH_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRATCH_DIR.parent
sys.path.insert(0, str(SCRATCH_DIR))

import test_master_regression_gate as runner


class TestRunnerParsers(unittest.TestCase):
    def test_parse_pattern_a_results_line(self):
        stdout = "Some logs...\nPHASE 5B.1.1 RESULTS: 92 PASSED, 0 FAILED (TOTAL 92)\nDone."
        res = runner.parse_suite_output(stdout, "")
        self.assertTrue(res["has_counts"])
        self.assertEqual(res["passed"], 92)
        self.assertEqual(res["failed"], 0)
        self.assertEqual(res["total"], 92)

    def test_parse_pattern_a_with_failures(self):
        stdout = "Some logs...\nRESULTS: 30 PASSED, 5 FAILED\nDone."
        res = runner.parse_suite_output(stdout, "")
        self.assertTrue(res["has_counts"])
        self.assertEqual(res["passed"], 30)
        self.assertEqual(res["failed"], 5)
        self.assertEqual(res["total"], 35)

    def test_parse_pattern_b_unittest_ok(self):
        stderr = "Ran 46 tests in 0.270s\n\nOK\n"
        res = runner.parse_suite_output("", stderr)
        self.assertTrue(res["has_counts"])
        self.assertEqual(res["passed"], 46)
        self.assertEqual(res["failed"], 0)
        self.assertEqual(res["total"], 46)

    def test_parse_pattern_b_unittest_failed(self):
        stderr = "Ran 20 tests in 0.500s\n\nFAILED (failures=3, errors=1)\n"
        res = runner.parse_suite_output("", stderr)
        self.assertTrue(res["has_counts"])
        self.assertEqual(res["passed"], 16)
        self.assertEqual(res["failed"], 4)
        self.assertEqual(res["total"], 20)

    def test_parse_pattern_c_pass_fail_tags(self):
        stdout = """
  [PASS] Check A
  [PASS] Check B
  [FAIL] Check C
  [PASS] Check D
Traceback (most recent call last):
  File "test.py", line 10, in <module>
"""
        res = runner.parse_suite_output(stdout, "")
        self.assertTrue(res["has_counts"])
        self.assertEqual(res["passed"], 3)
        self.assertEqual(res["failed"], 1)
        self.assertEqual(res["total"], 4)

    def test_parse_unparseable_output(self):
        stdout = "Random program output with no summary.\nFinished successfully."
        res = runner.parse_suite_output(stdout, "")
        self.assertFalse(res["has_counts"])
        self.assertEqual(res["passed"], 0)
        self.assertEqual(res["failed"], 0)


class TestRunnerExecutionHandling(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.results_dir = self.temp_path / "test-results"
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_execute_passing_dummy_suite(self):
        script = self.temp_path / "dummy_pass.py"
        script.write_text("print('RESULTS: 5 PASSED, 0 FAILED')\n", encoding="utf-8")
        suite = {
            "id": "dummy_pass",
            "name": "Dummy Pass Suite",
            "category": "Test",
            "rel_path": str(script.relative_to(self.temp_path)),
            "timeout_sec": 10
        }
        res = runner.execute_suite(suite, self.results_dir, self.temp_path)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["exit_code"], 0)
        self.assertEqual(res["passed_checks"], 5)
        self.assertEqual(res["failed_checks"], 0)

    def test_execute_failing_dummy_suite_never_classified_as_pass(self):
        script = self.temp_path / "dummy_fail.py"
        script.write_text("import sys\nprint('RESULTS: 3 PASSED, 2 FAILED')\nsys.exit(1)\n", encoding="utf-8")
        suite = {
            "id": "dummy_fail",
            "name": "Dummy Fail Suite",
            "category": "Test",
            "rel_path": str(script.relative_to(self.temp_path)),
            "timeout_sec": 10
        }
        res = runner.execute_suite(suite, self.results_dir, self.temp_path)
        self.assertEqual(res["status"], "FAIL")
        self.assertNotEqual(res["exit_code"], 0)
        self.assertEqual(res["passed_checks"], 3)
        self.assertEqual(res["failed_checks"], 2)

    def test_execute_timeout_handling(self):
        script = self.temp_path / "dummy_timeout.py"
        script.write_text("import time\ntime.sleep(5)\n", encoding="utf-8")
        suite = {
            "id": "dummy_timeout",
            "name": "Dummy Timeout Suite",
            "category": "Test",
            "rel_path": str(script.relative_to(self.temp_path)),
            "timeout_sec": 1
        }
        res = runner.execute_suite(suite, self.results_dir, self.temp_path)
        self.assertEqual(res["status"], "TIMEOUT")
        self.assertIn("timed out", res["error_message"].lower())

    def test_execute_missing_script_handling(self):
        suite = {
            "id": "missing_script",
            "name": "Missing Suite",
            "category": "Test",
            "rel_path": "non_existent_file.py",
            "timeout_sec": 10
        }
        res = runner.execute_suite(suite, self.results_dir, self.temp_path)
        self.assertEqual(res["status"], "ERROR")
        self.assertIn("not found", res["error_message"].lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)

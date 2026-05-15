#!/usr/bin/env python3
"""
TASK-003 verifier: validate-wisdom-notebook.py behavior.

Asserts:
1. --help self-describes (mentions --feature, exit codes, schema reference).
2. Positive case: features/002-omo-inspired-v0.6/ exits 0.
3. Missing file: only learnings.md present -> exit 1.
4. Missing delta: TASK-002 claimed in progress.md but no entry in any notepad
   -> exit 1.
5. Duplicate entry-id within a single notepad file -> exit 1.
6. Non-monotonic entry-id -> default exits 0 with WARN; --strict exits 1.
7. Invalid args (--feature pointing to nonexistent path) -> exit 2.
8. validator script imports stdlib only (no third-party).

stdlib only.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = Path(__file__).parent / "validate-wisdom-notebook.py"
FIXTURES = Path(__file__).parent / "test-fixtures"
REAL_FEATURE = REPO_ROOT / "features" / "002-omo-inspired-v0.6"


def _run(args, expect_exit=None):
    result = subprocess.run(
        ["python3", str(SCRIPT)] + args,
        capture_output=True, text=True,
    )
    if expect_exit is not None:
        assert result.returncode == expect_exit, (
            f"exit {result.returncode} != {expect_exit}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


class TestValidateWisdomNotebook(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(SCRIPT.exists(), f"missing: {SCRIPT}")

    def test_stdlib_only(self):
        text = SCRIPT.read_text(encoding="utf-8")
        # Only allow imports of well-known stdlib modules
        stdlib_modules = {
            "argparse", "json", "os", "sys", "re", "pathlib", "typing",
            "dataclasses", "collections", "enum", "io",
            "__future__",
        }
        bad = []
        for line in text.splitlines():
            m = re.match(r"^(?:from|import)\s+([\w\.]+)", line)
            if m:
                top = m.group(1).split(".")[0]
                if top not in stdlib_modules:
                    bad.append(line.strip())
        self.assertEqual(bad, [], f"non-stdlib imports: {bad}")

    def test_help_self_describes(self):
        r = _run(["--help"], expect_exit=0)
        self.assertIn("--feature", r.stdout)
        self.assertTrue(re.search(r"exit\s+code|0\s*=\s*PASS|exit:\s*0", r.stdout, flags=re.IGNORECASE))
        self.assertIn("notebook", r.stdout.lower())

    def test_positive_real_dogfood(self):
        r = _run(["--feature", str(REAL_FEATURE)])
        self.assertEqual(r.returncode, 0, f"real dogfood should pass: {r.stdout}\n{r.stderr}")

    def test_negative_missing_file(self):
        r = _run(["--feature", str(FIXTURES / "negative-missing-file")])
        self.assertEqual(r.returncode, 1, "missing 4-of-5 files should FAIL")
        self.assertRegex(r.stdout + r.stderr, r"missing.*decisions|missing.*issues|missing.*verification|missing.*problems")

    def test_negative_missing_delta(self):
        r = _run(["--feature", str(FIXTURES / "negative-no-delta")])
        self.assertEqual(r.returncode, 1, "TASK without delta should FAIL")
        self.assertRegex(r.stdout + r.stderr, r"TASK-002", "should name the offending task")

    def test_negative_duplicate_entry_id(self):
        r = _run(["--feature", str(FIXTURES / "negative-duplicate-entry-id")])
        self.assertEqual(r.returncode, 1, "duplicate entry-id should FAIL")
        combined = r.stdout + r.stderr
        self.assertTrue(re.search(r"duplicate.*learn-0001|learn-0001.*duplicate", combined, flags=re.IGNORECASE))

    def test_non_monotonic_default_passes_with_warn(self):
        r = _run(["--feature", str(FIXTURES / "negative-non-monotonic")])
        self.assertEqual(r.returncode, 0, "non-monotonic should be WARN-only by default")
        combined = r.stdout + r.stderr
        self.assertTrue(re.search(r"warn|non-monotonic|out.of.order", combined, flags=re.IGNORECASE))

    def test_non_monotonic_strict_fails(self):
        r = _run(["--feature", str(FIXTURES / "negative-non-monotonic"), "--strict"])
        self.assertEqual(r.returncode, 1, "--strict should FAIL on non-monotonic entry-id")

    def test_invalid_args_exit_2(self):
        r = _run(["--feature", "/nonexistent/path/should/not/be/here"])
        self.assertEqual(r.returncode, 2, "nonexistent --feature should exit 2")


if __name__ == "__main__":
    unittest.main(verbosity=2)

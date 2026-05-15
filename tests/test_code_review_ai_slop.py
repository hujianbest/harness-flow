#!/usr/bin/env python3
"""TASK-012 verifier: hf-code-review ai-slop-rubric integration."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "hf-code-review"
SKILL_MD = SKILL_DIR / "SKILL.md"
REF_RUBRIC = SKILL_DIR / "references" / "ai-slop-rubric.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"

REQUIRED_PATTERNS = ["simply", "obviously", "clearly", "em-dash"]


class TestCodeReviewAiSlop(unittest.TestCase):
    def test_rubric_exists(self):
        self.assertTrue(REF_RUBRIC.exists(), f"missing: {REF_RUBRIC}")

    def test_rubric_has_required_patterns(self):
        text = REF_RUBRIC.read_text()
        missing = [p for p in REQUIRED_PATTERNS if p.lower() not in text.lower()]
        self.assertEqual(missing, [], f"missing patterns: {missing}")

    def test_rubric_has_exceptions_section(self):
        text = REF_RUBRIC.read_text()
        self.assertTrue(
            re.search(r"##\s+(例外|Exceptions?)|README|test\s+assertion|文档", text, flags=re.IGNORECASE),
            "rubric must declare exception scope (README / docs / test assertion allowances)",
        )

    def test_rubric_has_grep_command(self):
        text = REF_RUBRIC.read_text()
        # Must show how to actually grep (rg or grep with -E or similar)
        self.assertTrue(
            re.search(r"```bash|```sh|rg\s|grep\s+-E|grep\s+-i", text),
            "rubric must include at least one shell example showing how to grep the patterns",
        )

    def test_skill_md_references_rubric(self):
        text = SKILL_MD.read_text()
        self.assertIn("ai-slop-rubric.md", text, "SKILL.md must reference references/ai-slop-rubric.md")

    def test_audit_still_passes(self):
        r = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("hf-code-review", r.stdout)

    def test_size_within_budget(self):
        text = SKILL_MD.read_text()
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(int(len(text.split()) * 1.3), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

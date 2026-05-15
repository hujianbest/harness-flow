#!/usr/bin/env python3
"""TASK-009 verifier: hf-tasks-review momus 4-dim + N=3 rewrite loop integration."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "hf-tasks-review"
SKILL_MD = SKILL_DIR / "SKILL.md"
REF_MOMUS = SKILL_DIR / "references" / "momus-rubric.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"

DIMENSIONS = ["Clarity", "Verification", "Context", "Big Picture"]


class TestTasksReviewMomus(unittest.TestCase):
    def test_momus_rubric_exists(self):
        self.assertTrue(REF_MOMUS.exists(), f"missing: {REF_MOMUS}")

    def test_momus_rubric_has_4_dimensions(self):
        text = REF_MOMUS.read_text()
        missing = [d for d in DIMENSIONS if d not in text]
        self.assertEqual(missing, [], f"missing dimensions: {missing}")

    def test_momus_rubric_has_thresholds(self):
        text = REF_MOMUS.read_text()
        # 4 dimensions + 1 zero-tolerance row = 5 thresholds
        thresholds_found = re.findall(r"\b(100|90|80|0)\s*%", text)
        self.assertGreaterEqual(len(thresholds_found), 5,
            f"need >= 5 numeric threshold mentions (100/90/80/100/0), got {len(thresholds_found)}")

    def test_skill_md_mentions_rejected_rewrite(self):
        text = SKILL_MD.read_text()
        self.assertRegex(text, r"rejected-rewrite", "SKILL.md must mention 'rejected-rewrite' verdict")

    def test_skill_md_mentions_n3_cap(self):
        text = SKILL_MD.read_text()
        # Should mention N=3 or 第 3 次 / 第 4 次 (escape on 4th)
        self.assertTrue(
            re.search(r"N\s*=\s*3|第\s*3\s*次|第\s*4\s*次|3\s*次.*循环|3\s*rounds", text),
            "SKILL.md must mention N=3 rewrite loop cap or '4th attempt -> escape'",
        )

    def test_skill_md_references_momus_rubric(self):
        text = SKILL_MD.read_text()
        self.assertIn("momus-rubric.md", text, "SKILL.md must reference references/momus-rubric.md")

    def test_common_rationalizations_has_threshold_row(self):
        text = SKILL_MD.read_text()
        m = re.search(r"^##\s+Common Rationalizations\b(.*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(m)
        body = m.group(1)
        # Must contain one row about thresholds being binary (1% off still fails)
        self.assertTrue(
            re.search(r"1\s*%|阈值|差.*1.*也是|threshold|差一点", body),
            "Common Rationalizations must include a row defending strict threshold semantics",
        )

    def test_audit_still_passes(self):
        r = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("hf-tasks-review", r.stdout)

    def test_size_within_budget(self):
        text = SKILL_MD.read_text()
        # Modified skill, allowed to grow but still <= 500 lines / <= 5000 tokens
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(int(len(text.split()) * 1.3), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

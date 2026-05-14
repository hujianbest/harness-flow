#!/usr/bin/env python3
"""TASK-005 verifier: hf-gap-analyzer SKILL.md + gap-rubric reference."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "hf-gap-analyzer"
SKILL_MD = SKILL_DIR / "SKILL.md"
REF_RUBRIC = SKILL_DIR / "references" / "gap-rubric.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"

# 6 rubric dimensions per design §3.2
RUBRIC_DIMENSIONS = [
    "Implicit Intent",
    "AI Slop",
    "Missing Acceptance",
    "Unaddressed Edge Cases",
    "Scope Creep",
    "Dangling Reference",
]


class TestGapAnalyzerSkill(unittest.TestCase):
    def test_skill_md_exists(self):
        self.assertTrue(SKILL_MD.exists(), f"missing: {SKILL_MD}")

    def test_reference_rubric_exists(self):
        self.assertTrue(REF_RUBRIC.exists(), f"missing: {REF_RUBRIC}")

    def test_audit_passes(self):
        result = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, f"audit failed:\n{result.stdout}")
        self.assertIn("hf-gap-analyzer", result.stdout)

    def test_rubric_dimensions_mentioned(self):
        text = (SKILL_MD.read_text() + REF_RUBRIC.read_text())
        missing = [d for d in RUBRIC_DIMENSIONS if d not in text]
        self.assertEqual(missing, [], f"missing rubric dimensions: {missing}")

    def test_workflow_has_4_plus_steps(self):
        text = SKILL_MD.read_text()
        m = re.search(r"^##\s+Workflow\b(.*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(m)
        steps = re.findall(r"^\s*\d+\.\s+", m.group(1), flags=re.MULTILINE)
        self.assertGreaterEqual(len(steps), 4)

    def test_common_rationalizations_3_plus(self):
        text = SKILL_MD.read_text()
        m = re.search(r"^##\s+Common Rationalizations\b(.*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(m)
        rows = [l for l in m.group(1).splitlines() if l.startswith("|") and not re.match(r"^\|[\s\-:]+\|", l)]
        self.assertGreaterEqual(len(rows[1:]), 3)

    def test_object_contract_present(self):
        text = SKILL_MD.read_text()
        self.assertTrue(re.search(r"^##\s+Object Contract\b", text, flags=re.MULTILINE))

    def test_explicitly_not_fagan_review(self):
        text = SKILL_MD.read_text()
        # Must explicitly say it does NOT produce verdict / is NOT a Fagan review node
        self.assertTrue(
            re.search(r"(不是\s*Fagan\s*review|not\s+a\s+Fagan\s+review|不写\s*verdict|does\s+not\s+produce\s+verdict)", text, flags=re.IGNORECASE),
            "SKILL.md must explicitly disclaim 'not a Fagan review node / does not write verdict'",
        )

    def test_size_within_budget(self):
        text = SKILL_MD.read_text()
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(int(len(text.split()) * 1.3), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

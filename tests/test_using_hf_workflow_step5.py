#!/usr/bin/env python3
"""TASK-013 verifier: using-hf-workflow step 5 entry bias adds fast-lane row."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = REPO_ROOT / "skills" / "using-hf-workflow" / "SKILL.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"


class TestUsingHfWorkflowStep5(unittest.TestCase):
    def test_step5_has_fast_lane_row(self):
        text = SKILL_MD.read_text()
        m = re.search(r"### 5\. 应用 entry bias\b(.*?)(?=^###\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(m, "step 5 section not found")
        body = m.group(1)
        self.assertTrue(
            re.search(r"hf-ultrawork", body),
            "step 5 entry bias table must include row pointing to hf-ultrawork",
        )
        self.assertTrue(
            re.search(r"Execution\s+Mode\s*=\s*auto|fast\s+lane|auto\s*mode", body, flags=re.IGNORECASE),
            "step 5 row must mention auto mode / fast lane trigger condition",
        )

    def test_step3_unchanged_executive_mode_extraction(self):
        text = SKILL_MD.read_text()
        m = re.search(r"### 3\. 提取 Execution Mode 偏好\b(.*?)(?=^###\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(m, "step 3 must remain present")
        body = m.group(1)
        self.assertTrue(
            re.search(r"auto\s*mode", body, flags=re.IGNORECASE),
            "step 3 must still describe Execution Mode preference extraction (unchanged behavior)",
        )

    def test_step6_unchanged_no_ultrawork_command(self):
        text = SKILL_MD.read_text()
        m = re.search(r"### 6\. 命令当作 bias\b(.*?)(?=^###\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(m, "step 6 must remain present")
        body = m.group(1)
        # /ultrawork command must NOT exist (intentionally not introduced per ADR-009 D3)
        self.assertNotIn("/ultrawork", body, "step 6 must NOT introduce /ultrawork slash command (ADR-009 D3)")

    def test_audit_still_passes(self):
        r = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("using-hf-workflow", r.stdout)

    def test_size_within_budget(self):
        text = SKILL_MD.read_text()
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(int(len(text.split()) * 1.3), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

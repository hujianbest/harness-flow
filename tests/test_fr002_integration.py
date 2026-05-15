#!/usr/bin/env python3
"""TASK-014 + TASK-015 verifier: FR-002 integration into hf-test-driven-dev + hf-completion-gate."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TDD_SKILL = REPO_ROOT / "skills" / "hf-test-driven-dev" / "SKILL.md"
COMPLETION_GATE_SKILL = REPO_ROOT / "skills" / "hf-completion-gate" / "SKILL.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"


class TestFr002Integration(unittest.TestCase):
    # TASK-014 — hf-test-driven-dev Output Contract integration
    def test_tdd_skill_references_wisdom_notebook(self):
        text = TDD_SKILL.read_text()
        self.assertIn("hf-wisdom-notebook", text, "hf-test-driven-dev SKILL.md must reference hf-wisdom-notebook")

    def test_tdd_skill_mentions_5_file_container(self):
        text = TDD_SKILL.read_text()
        self.assertTrue(
            re.search(r"5\s*个?\s*notebook|5\s*文件|notepads/.*5", text),
            "hf-test-driven-dev SKILL.md must mention the 5-file notebook container requirement (FR-002)",
        )

    def test_tdd_skill_mentions_learnings_or_verification_required(self):
        text = TDD_SKILL.read_text()
        self.assertTrue(
            re.search(r"learnings\.md.*verification\.md|verification\.md.*learnings\.md", text),
            "hf-test-driven-dev SKILL.md must require at least one delta in learnings.md OR verification.md per task",
        )

    def test_tdd_skill_references_tasks_progress_json(self):
        text = TDD_SKILL.read_text()
        self.assertTrue(
            re.search(r"tasks\.progress\.json|tasks-progress-schema", text),
            "hf-test-driven-dev SKILL.md must reference tasks.progress.json schema (TASK-001 integration)",
        )

    # TASK-015 — hf-completion-gate validate-wisdom-notebook integration
    def test_completion_gate_calls_validator(self):
        text = COMPLETION_GATE_SKILL.read_text()
        self.assertTrue(
            re.search(r"validate-wisdom-notebook\.py|validate_wisdom_notebook", text),
            "hf-completion-gate SKILL.md must mention validate-wisdom-notebook.py call",
        )

    def test_completion_gate_fails_on_missing_delta(self):
        text = COMPLETION_GATE_SKILL.read_text()
        self.assertTrue(
            re.search(r"FAIL.*wisdom|wisdom.*FAIL|gate.*FAIL.*notebook|notebook.*FAIL", text, flags=re.IGNORECASE),
            "hf-completion-gate SKILL.md must specify gate verdict=FAIL when validator fails",
        )

    # Common
    def test_audit_still_passes(self):
        r = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("hf-test-driven-dev", r.stdout)
        self.assertIn("hf-completion-gate", r.stdout)

    def test_tdd_skill_size_within_budget(self):
        text = TDD_SKILL.read_text()
        self.assertLessEqual(len(text.splitlines()), 500, f"hf-test-driven-dev SKILL.md {len(text.splitlines())} > 500")

    def test_completion_gate_size_within_budget(self):
        text = COMPLETION_GATE_SKILL.read_text()
        self.assertLessEqual(len(text.splitlines()), 500, f"hf-completion-gate SKILL.md {len(text.splitlines())} > 500")


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Verifier for task summary + thin verdict reporting policy."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SHARED_CONVENTIONS = (
    REPO_ROOT
    / "skills"
    / "hf-workflow-router"
    / "references"
    / "workflow-shared-conventions.md"
)
EXECUTION_SEMANTICS = (
    REPO_ROOT
    / "skills"
    / "hf-workflow-router"
    / "references"
    / "execution-semantics.md"
)
TDD_SKILL = REPO_ROOT / "skills" / "hf-test-driven-dev" / "SKILL.md"
COMPLETION_GATE = REPO_ROOT / "skills" / "hf-completion-gate" / "SKILL.md"
REVIEW_AND_GATE_SKILLS = [
    REPO_ROOT / "skills" / "hf-test-review" / "SKILL.md",
    REPO_ROOT / "skills" / "hf-code-review" / "SKILL.md",
    REPO_ROOT / "skills" / "hf-traceability-review" / "SKILL.md",
    REPO_ROOT / "skills" / "hf-regression-gate" / "SKILL.md",
    REPO_ROOT / "skills" / "hf-doc-freshness-gate" / "SKILL.md",
]
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"


class TestTaskSummaryThinVerdicts(unittest.TestCase):
    def test_shared_conventions_define_task_summary_and_thin_verdicts(self):
        text = SHARED_CONVENTIONS.read_text()
        self.assertIn("Task Summary And Thin Verdict Blocks", text)
        self.assertIn("Task Completion Summary", text)
        self.assertIn("Thin Verdict Block schema", text)
        self.assertRegex(text, r"summary\s+不是\s+verdict\s+替代物|不替代任何 review / gate verdict")

    def test_build_one_task_is_not_build_session_stop(self):
        text = EXECUTION_SEMANTICS.read_text()
        self.assertRegex(text, r"Build one task.*不是 build 会话的停止条件")
        self.assertRegex(text, r"task summary.*不是.*人工确认点")

    def test_tdd_and_completion_gate_reference_task_summary(self):
        combined = TDD_SKILL.read_text() + "\n" + COMPLETION_GATE.read_text()
        self.assertRegex(combined, r"Task Summary Path|task summary")
        self.assertRegex(combined, r"thin verdict")
        self.assertRegex(combined, r"summaries/task-<TASK-ID>\.md")

    def test_review_and_gate_skills_use_thin_verdict_policy(self):
        for path in REVIEW_AND_GATE_SKILLS:
            with self.subTest(path=path):
                text = path.read_text()
                self.assertRegex(text, r"thin verdict")
                self.assertRegex(text, r"task completion summary")
                self.assertRegex(text, r"需修改|阻塞")

    def test_audit_still_passes(self):
        result = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)

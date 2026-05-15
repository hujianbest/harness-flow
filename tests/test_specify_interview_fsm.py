#!/usr/bin/env python3
"""TASK-010 verifier: hf-specify Interview FSM 5-state + spec.intake.md schema."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "hf-specify"
SKILL_MD = SKILL_DIR / "SKILL.md"
REF_FSM = SKILL_DIR / "references" / "interview-fsm.md"
REF_INTAKE = SKILL_DIR / "references" / "spec-intake-template.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"

FSM_STATES = ["Interview", "Research", "ClearanceCheck", "PlanGeneration", "Done"]


class TestSpecifyInterviewFsm(unittest.TestCase):
    def test_fsm_ref_exists(self):
        self.assertTrue(REF_FSM.exists(), f"missing: {REF_FSM}")

    def test_intake_template_exists(self):
        self.assertTrue(REF_INTAKE.exists(), f"missing: {REF_INTAKE}")

    def test_fsm_has_5_states(self):
        text = REF_FSM.read_text()
        missing = [s for s in FSM_STATES if s not in text]
        self.assertEqual(missing, [], f"missing FSM states: {missing}")

    def test_fsm_has_clearance_to_research_regression(self):
        # OQ-005: ClearanceCheck -> Research / Interview regression allowed
        text = REF_FSM.read_text()
        self.assertTrue(
            re.search(r"ClearanceCheck.*(Research|Interview)|回退|regression", text, flags=re.IGNORECASE | re.DOTALL),
            "interview-fsm.md must describe ClearanceCheck regression to Research / Interview per OQ-005",
        )

    def test_intake_template_has_required_sections(self):
        text = REF_INTAKE.read_text()
        # Per design §4.2: Status / Last Question Asked / Question Trail / Research Trail / Clearance Checks
        for section in ["Status", "Question Trail", "Research Trail", "Clearance Checks"]:
            self.assertIn(section, text, f"spec.intake.md template missing section: {section}")

    def test_skill_md_references_fsm(self):
        text = SKILL_MD.read_text()
        self.assertIn("interview-fsm.md", text, "SKILL.md must reference references/interview-fsm.md")
        self.assertIn("spec-intake-template.md", text, "SKILL.md must reference spec-intake-template.md")

    def test_audit_still_passes(self):
        r = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("hf-specify", r.stdout)

    def test_size_within_budget(self):
        text = SKILL_MD.read_text()
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(int(len(text.split()) * 1.3), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

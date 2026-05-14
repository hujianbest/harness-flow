#!/usr/bin/env python3
"""TASK-011 verifier: hf-workflow-router step-level recovery + category_hint + progress.md schema."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "hf-workflow-router"
SKILL_MD = SKILL_DIR / "SKILL.md"
TRANSITION_MAP = SKILL_DIR / "references" / "profile-node-and-transition-map.md"
SHARED_CONVENTIONS = SKILL_DIR / "references" / "workflow-shared-conventions.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"


class TestWorkflowRouterV06(unittest.TestCase):
    def test_transition_map_has_step_level_recovery(self):
        text = TRANSITION_MAP.read_text()
        self.assertTrue(
            re.search(r"step-level\s+recovery|step\s+level\s+recovery|tasks\.progress\.json|step-level\s+恢复", text, flags=re.IGNORECASE),
            "transition map must describe step-level recovery via tasks.progress.json (FR-003)",
        )

    def test_transition_map_has_category_hint(self):
        text = TRANSITION_MAP.read_text()
        self.assertTrue(
            re.search(r"category[_\s-]?hint|category_hint", text, flags=re.IGNORECASE),
            "transition map must mention category_hint handoff field (FR-015)",
        )

    def test_transition_map_has_wisdom_summary_injection(self):
        text = TRANSITION_MAP.read_text()
        self.assertTrue(
            re.search(r"wisdom_summary|wisdom\s+summary|wisdom-notebook|notepads/", text, flags=re.IGNORECASE),
            "transition map must describe wisdom_summary handoff injection (FR-003)",
        )

    def test_shared_conventions_has_fast_lane_decisions_schema(self):
        text = SHARED_CONVENTIONS.read_text()
        self.assertTrue(
            re.search(r"##.*Fast Lane Decisions|fast.lane.*decisions|Fast Lane Decisions schema", text, flags=re.IGNORECASE),
            "workflow-shared-conventions must define progress.md ## Fast Lane Decisions schema (FR-010)",
        )

    def test_shared_conventions_has_wisdom_delta_schema(self):
        text = SHARED_CONVENTIONS.read_text()
        self.assertTrue(
            re.search(r"Wisdom Delta|wisdom_summary", text, flags=re.IGNORECASE),
            "workflow-shared-conventions must define progress.md ## Wisdom Delta schema (FR-002)",
        )

    def test_skill_md_references_v06_additions(self):
        text = SKILL_MD.read_text()
        # SKILL.md should mention at least one of the three v0.6 additions
        self.assertTrue(
            re.search(r"step-level|category_hint|wisdom|Fast Lane Decisions", text, flags=re.IGNORECASE),
            "router SKILL.md must reference at least one of v0.6 additions",
        )

    def test_audit_still_passes(self):
        r = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("hf-workflow-router", r.stdout)

    def test_size_within_budget(self):
        text = SKILL_MD.read_text()
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(int(len(text.split()) * 1.3), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

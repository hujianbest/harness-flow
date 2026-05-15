#!/usr/bin/env python3
"""TASK-006 verifier: hf-context-mesh SKILL.md + agents-md-template reference."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "hf-context-mesh"
SKILL_MD = SKILL_DIR / "SKILL.md"
REF_TEMPLATE = SKILL_DIR / "references" / "agents-md-template.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"

CLIENTS = ["OpenCode", "Cursor", "Claude Code"]
LAYERS = ["root", "mid", "leaf"]


class TestContextMeshSkill(unittest.TestCase):
    def test_skill_md_exists(self):
        self.assertTrue(SKILL_MD.exists())

    def test_template_ref_exists(self):
        self.assertTrue(REF_TEMPLATE.exists())

    def test_audit_passes(self):
        r = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("hf-context-mesh", r.stdout)

    def test_three_clients_in_template(self):
        text = REF_TEMPLATE.read_text()
        missing = [c for c in CLIENTS if c not in text]
        self.assertEqual(missing, [], f"missing clients in template: {missing}")

    def test_three_layers_in_template(self):
        text = REF_TEMPLATE.read_text()
        # Each of root / mid / leaf should appear at least 3 times (once per client)
        for layer in LAYERS:
            count = len(re.findall(rf"\b{layer}\b", text, flags=re.IGNORECASE))
            self.assertGreaterEqual(count, 3, f"layer '{layer}' appears {count} times, want >= 3")

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

    def test_hard_gate_no_writing_for_architect(self):
        text = SKILL_MD.read_text()
        # Must explicitly forbid agent from writing project conventions on architect's behalf
        self.assertTrue(
            re.search(r"(不替.*架构师.*写|不为架构师.*起草|architect.*conventions.*not.*write|不替用户)", text),
            "SKILL.md must explicitly forbid agent from writing conventions on architect's behalf",
        )

    def test_size_within_budget(self):
        text = SKILL_MD.read_text()
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(int(len(text.split()) * 1.3), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

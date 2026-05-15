#!/usr/bin/env python3
"""
TASK-002 verifier: hf-wisdom-notebook SKILL.md + references structural assertions.

Asserts:
1. SKILL.md exists, references/notebook-schema.md exists,
   references/notebook-update-protocol.md exists.
2. audit-skill-anatomy.py reports OK for hf-wisdom-notebook.
3. SKILL.md mentions all 5 notebook file names.
4. SKILL.md has a Workflow section with >= 5 numbered steps.
5. SKILL.md has Common Rationalizations >= 3 table rows.
6. SKILL.md has Object Contract section.
7. SKILL.md size: wc -l <= 500, estimated tokens (wc -w * 1.3) <= 5000.

stdlib only.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "hf-wisdom-notebook"
SKILL_MD = SKILL_DIR / "SKILL.md"
REF_SCHEMA = SKILL_DIR / "references" / "notebook-schema.md"
REF_PROTOCOL = SKILL_DIR / "references" / "notebook-update-protocol.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"

NOTEBOOK_FILES = ["learnings.md", "decisions.md", "issues.md", "verification.md", "problems.md"]


class TestWisdomNotebookSkill(unittest.TestCase):
    def test_skill_md_exists(self):
        self.assertTrue(SKILL_MD.exists(), f"missing: {SKILL_MD}")

    def test_reference_schema_exists(self):
        self.assertTrue(REF_SCHEMA.exists(), f"missing: {REF_SCHEMA}")

    def test_reference_protocol_exists(self):
        self.assertTrue(REF_PROTOCOL.exists(), f"missing: {REF_PROTOCOL}")

    def test_audit_passes(self):
        result = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, f"audit failed:\n{result.stdout}\n{result.stderr}")
        self.assertIn("hf-wisdom-notebook", result.stdout, "hf-wisdom-notebook not in audit output")

    def test_mentions_all_5_notebook_files(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        missing = [f for f in NOTEBOOK_FILES if f not in text]
        self.assertEqual(missing, [], f"SKILL.md missing references to: {missing}")

    def test_workflow_has_5_plus_numbered_steps(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        wf_match = re.search(r"^##\s+Workflow\b(.*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(wf_match, "Workflow section missing")
        wf_body = wf_match.group(1)
        steps = re.findall(r"^\s*(\d+)\.\s+", wf_body, flags=re.MULTILINE)
        self.assertGreaterEqual(len(steps), 5, f"need >= 5 numbered steps, got {len(steps)}")

    def test_common_rationalizations_has_3_plus_rows(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        cr_match = re.search(r"^##\s+Common Rationalizations\b(.*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(cr_match, "Common Rationalizations section missing")
        cr_body = cr_match.group(1)
        rows = [line for line in cr_body.splitlines() if line.startswith("|") and not re.match(r"^\|[\s\-:]+\|", line)]
        data_rows = rows[1:] if rows else []
        self.assertGreaterEqual(len(data_rows), 3, f"need >= 3 rationalization rows, got {len(data_rows)}")

    def test_object_contract_present(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(
            re.search(r"^##\s+Object Contract\b", text, flags=re.MULTILINE),
            "Object Contract section missing",
        )

    def test_size_within_budget(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        word_count = len(text.split())
        token_estimate = int(word_count * 1.3)
        self.assertLessEqual(line_count, 500, f"SKILL.md {line_count} lines > 500")
        self.assertLessEqual(token_estimate, 5000, f"SKILL.md ~{token_estimate} tokens > 5000")


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""TASK-007 verifier: hf-ultrawork SKILL.md + fast-lane-escape-conditions reference.

Special focus per FR-008: SKILL.md Hard Gates section MUST enumerate the 5 non-
compressible items locally (NOT just reference ADR-009 D2).
"""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "hf-ultrawork"
SKILL_MD = SKILL_DIR / "SKILL.md"
REF_ESCAPE = SKILL_DIR / "references" / "fast-lane-escape-conditions.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"


class TestUltraworkSkill(unittest.TestCase):
    def test_skill_md_exists(self):
        self.assertTrue(SKILL_MD.exists())

    def test_escape_ref_exists(self):
        self.assertTrue(REF_ESCAPE.exists())

    def test_audit_passes(self):
        r = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("hf-ultrawork", r.stdout)

    def test_hard_gates_enumerates_5_noncompressibles(self):
        text = SKILL_MD.read_text()
        # Extract Hard Gates section body
        m = re.search(r"^##\s+Hard Gates\b(.*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(m, "Hard Gates section missing")
        body = m.group(1)
        # 5 categories per ADR-009 D2 — keywords must each appear at least once in the section
        required_keywords = [
            ("Fagan review", r"Fagan\s+review|8\s*个\s*Fagan|hf-(spec|design|tasks|test|code|traceability|ui|discovery)-review"),
            ("gate verdict",  r"gate\s+verdict|3\s*个\s*gate|hf-(regression|doc-freshness|completion)-gate"),
            ("closeout pack", r"closeout\s+pack|hf-finalize"),
            ("approval artifact disk-write", r"approval\s+(record|工件|artifact).*(disk|落盘|写入)|approval.*必须.*落盘|approval.*工件.*必须|工件.*必须.*落盘"),
            ("Hard Gates stop-on-unclear-standard", r"方向.*取舍.*标准|standard.*unclear|stop\s+and\s+bounce|停下抛回|standard.*不清"),
        ]
        missing = []
        for label, pattern in required_keywords:
            if not re.search(pattern, body, flags=re.IGNORECASE | re.DOTALL):
                missing.append(label)
        self.assertEqual(missing, [], f"Hard Gates missing enumerated items: {missing}")

    def test_keyword_set_present(self):
        text = SKILL_MD.read_text()
        # 3 categories per OQ-003: enable / pause / revert-to-standard
        # Check at least one keyword from each category
        patterns = {
            "enable": r"(auto\s*mode|ultrawork|ulw|自动执行|不要停下来|keep\s+going|proceed)",
            "pause":  r"(\b停\b|暂停|pause|wait|hold\s+on|等等|stop)",
            "revert": r"(standard\s*mode|恢复\s*standard|revert\s+to\s+standard|回到\s*standard)",
        }
        missing = [k for k, p in patterns.items() if not re.search(p, text, flags=re.IGNORECASE)]
        self.assertEqual(missing, [], f"keyword categories missing: {missing}")

    def test_escape_conditions_six(self):
        text = REF_ESCAPE.read_text()
        # 6 escape conditions per ADR-009 D3 item 4
        # Look for at least 6 distinct numbered/listed items
        items = re.findall(r"^\s*(?:\d+\.|-\s+\*\*|##\s)", text, flags=re.MULTILINE)
        self.assertGreaterEqual(len(items), 6, f"need >= 6 escape conditions, got {len(items)}")

    def test_workflow_has_5_plus_steps(self):
        text = SKILL_MD.read_text()
        m = re.search(r"^##\s+Workflow\b(.*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(m)
        steps = re.findall(r"^\s*\d+\.\s+", m.group(1), flags=re.MULTILINE)
        self.assertGreaterEqual(len(steps), 5)
        # Must mention verdict + escape check
        self.assertTrue(
            re.search(r"(verdict.*escape|escape.*verdict|verdict.*后.*检查|after.*verdict.*check)",
                      m.group(1), flags=re.IGNORECASE | re.DOTALL),
            "Workflow must describe 'check escape after verdict'",
        )

    def test_common_rationalizations_3_plus(self):
        text = SKILL_MD.read_text()
        m = re.search(r"^##\s+Common Rationalizations\b(.*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(m)
        rows = [l for l in m.group(1).splitlines() if l.startswith("|") and not re.match(r"^\|[\s\-:]+\|", l)]
        self.assertGreaterEqual(len(rows[1:]), 3)

    def test_object_contract_present(self):
        text = SKILL_MD.read_text()
        self.assertTrue(re.search(r"^##\s+Object Contract\b", text, flags=re.MULTILINE))

    def test_size_within_budget(self):
        text = SKILL_MD.read_text()
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(int(len(text.split()) * 1.3), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

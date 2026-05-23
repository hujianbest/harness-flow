#!/usr/bin/env python3
"""Verifier for hf-subagent-driven-dev optional implementation leaf."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "hf-subagent-driven-dev"
SKILL_MD = SKILL_DIR / "SKILL.md"
RETURN_CONTRACT = SKILL_DIR / "references" / "implementer-return-contract.md"
ROLE_CONTRACTS = SKILL_DIR / "references" / "agent-role-contracts.md"
ROUTER_SKILL = REPO_ROOT / "skills" / "hf-workflow-router" / "SKILL.md"
TRANSITION_MAP = REPO_ROOT / "skills" / "hf-workflow-router" / "references" / "profile-node-and-transition-map.md"
SHARED_CONVENTIONS = REPO_ROOT / "skills" / "hf-workflow-router" / "references" / "workflow-shared-conventions.md"
REVIEW_DISPATCH = REPO_ROOT / "skills" / "hf-workflow-router" / "references" / "review-dispatch-protocol.md"
README = REPO_ROOT / "README.md"
README_ZH = REPO_ROOT / "README.zh-CN.md"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit-skill-anatomy.py"


class TestSubagentDrivenDevSkill(unittest.TestCase):
    def test_skill_and_reference_exist(self):
        self.assertTrue(SKILL_MD.exists())
        self.assertTrue(RETURN_CONTRACT.exists())
        self.assertTrue(ROLE_CONTRACTS.exists())

    def test_skill_declares_single_task_and_no_review_skip(self):
        text = SKILL_MD.read_text()
        self.assertIn("Current Active Task", text)
        self.assertIn("hf-implementer", text)
        self.assertIn("hf-reviewer", text)
        self.assertRegex(text, r"fresh implementer subagent|Fresh Subagent Per Task")
        self.assertTrue(
            re.search(r"self-review.*不能替代|self-review.*not.*替代|self-review.*不是", text, flags=re.IGNORECASE | re.DOTALL),
            "skill must state implementer self-review does not replace HF review",
        )
        self.assertIn("hf-test-review", text)
        self.assertIn("hf-code-review", text)

    def test_role_contracts_define_implementer_and_reviewer(self):
        text = ROLE_CONTRACTS.read_text()
        self.assertIn("hf-implementer", text)
        self.assertIn("hf-reviewer", text)
        self.assertTrue(
            re.search(r"hf-implementer.*MUST use `hf-test-driven-dev`|hf-implementer`.*必须.*hf-test-driven-dev", text, flags=re.IGNORECASE | re.DOTALL),
            "hf-implementer must be bound to hf-test-driven-dev",
        )
        self.assertTrue(
            re.search(r"hf-reviewer.*hf-\\*review|hf-reviewer.*reviewer return contract", text, flags=re.IGNORECASE | re.DOTALL),
            "hf-reviewer must be bound to existing review skills and return contract",
        )

    def test_return_contract_has_four_statuses(self):
        text = RETURN_CONTRACT.read_text()
        for status in ("DONE", "DONE_WITH_CONCERNS", "NEEDS_CONTEXT", "BLOCKED"):
            self.assertIn(status, text)
        self.assertIn('"agent_role": "hf-implementer"', text)
        self.assertIn("next_action_or_recommended_skill", text)
        self.assertNotIn('"conclusion"', text)

    def test_router_allows_optional_implementation_leaf(self):
        router = ROUTER_SKILL.read_text()
        transition = TRANSITION_MAP.read_text()
        shared = SHARED_CONVENTIONS.read_text()
        self.assertIn("hf-subagent-driven-dev", router)
        self.assertIn("hf-subagent-driven-dev", transition)
        self.assertIn("hf-subagent-driven-dev", shared)
        self.assertRegex(transition, r"implementation stage.*conditional alternative|可选实现 leaf", re.DOTALL)

    def test_review_dispatch_names_hf_reviewer_role(self):
        text = REVIEW_DISPATCH.read_text()
        self.assertIn("hf-reviewer", text)
        self.assertIn("hf-test-review", text)
        self.assertIn("hf-code-review", text)

    def test_readmes_keep_skill_count_and_structure(self):
        en = README.read_text()
        zh = README_ZH.read_text()
        self.assertIn("## All 30 Skills", en)
        self.assertIn("29 `hf-*` skills plus the `using-hf-workflow` entry skill", en)
        self.assertIn("## 全部 30 个 Skills", zh)
        self.assertIn("29 个 `hf-*` skills，加上 `using-hf-workflow` 入口 skill", zh)
        self.assertIn("[hf-subagent-driven-dev](skills/hf-subagent-driven-dev/SKILL.md)", en)
        self.assertIn("[hf-subagent-driven-dev](skills/hf-subagent-driven-dev/SKILL.md)", zh)

    def test_audit_passes_and_skill_size_is_within_budget(self):
        r = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--skills-dir", str(REPO_ROOT / "skills")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("hf-subagent-driven-dev", r.stdout)
        text = SKILL_MD.read_text()
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(int(len(text.split()) * 1.3), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)

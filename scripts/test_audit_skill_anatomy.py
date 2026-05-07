"""Unit tests for scripts/audit-skill-anatomy.py.

Run with: python3 -m pytest scripts/test_audit_skill_anatomy.py -q
or:       python3 scripts/test_audit_skill_anatomy.py
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

_HERE = Path(__file__).parent
_SPEC = importlib.util.spec_from_file_location(
    "audit_skill_anatomy", _HERE / "audit-skill-anatomy.py"
)
assert _SPEC and _SPEC.loader
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["audit_skill_anatomy"] = _MOD
_SPEC.loader.exec_module(_MOD)  # type: ignore[union-attr]


def write_skill(skills_dir: Path, name: str, body: str) -> Path:
    sd = skills_dir / name
    sd.mkdir(parents=True, exist_ok=True)
    skill_md = sd / "SKILL.md"
    skill_md.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")
    return skill_md


COMPLIANT_BODY = """
---
name: hf-example
description: Use when example is needed. Not for production.
---

# Example Skill

A one-line opener.

## When to Use

适用：例子。

不适用：
- 阶段不清 → `hf-workflow-router`

## Workflow

1. Do thing.

## Common Rationalizations

| 借口 | 反驳 |
|------|------|
| "I'll skip this" | Per Verification: do not skip. |
| "Later" | Per Hard Gates: not allowed. |
| "Quick fix" | Per Workflow stop rule: full path required. |

## Verification

- record on disk
"""

FORBIDDEN_SECTION_BODY = """
---
name: hf-forbidden
description: Use when forbidden section is present.
---

# Forbidden

## When to Use

适用：x

## Workflow

1. step

## 和其他 Skill 的区别

| 场景 | 用 hf-forbidden |
|---|---|
| ... | ✅ |

## Common Rationalizations

| 借口 | 反驳 |
|---|---|
| "x" | Per Verification: y. |

## Verification

- record on disk
"""

MISSING_REQUIRED_BODY = """
---
name: hf-missing
description: Use when missing.
---

# Missing

## When to Use

适用：x

## Workflow

1. step

## Verification

- record on disk
"""

MISMATCH_NAME_BODY = """
---
name: hf-wrong-name
description: Use when name mismatch.
---

# Mismatch

## When to Use

适用：x

## Workflow

1. step

## Common Rationalizations

| 借口 | 反驳 |
|------|------|
| "..." | Per Verification: ... |
| "..." | Per Hard Gates: ... |
| "..." | Per Workflow: ... |

## Verification

- ok
"""


class AuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.skills_dir = Path(self._tmp.name) / "skills"
        self.skills_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _audit(self):
        return _MOD.audit_dir(self.skills_dir)

    def test_compliant_skill_passes(self) -> None:
        write_skill(self.skills_dir, "hf-example", COMPLIANT_BODY)
        report = self._audit()
        self.assertTrue(report.ok, msg=str(report.skills[0].failures))
        self.assertEqual(report.failed_count, 0)

    def test_forbidden_section_fails(self) -> None:
        write_skill(self.skills_dir, "hf-forbidden", FORBIDDEN_SECTION_BODY)
        report = self._audit()
        self.assertFalse(report.ok)
        msgs = report.skills[0].failures
        self.assertTrue(any("forbidden section present" in m for m in msgs), msgs)

    def test_missing_required_section_fails(self) -> None:
        write_skill(self.skills_dir, "hf-missing", MISSING_REQUIRED_BODY)
        report = self._audit()
        self.assertFalse(report.ok)
        msgs = report.skills[0].failures
        self.assertTrue(
            any("missing required section: `## Common Rationalizations`" in m for m in msgs),
            msgs,
        )

    def test_frontmatter_name_mismatch_fails(self) -> None:
        write_skill(self.skills_dir, "hf-actual-dir", MISMATCH_NAME_BODY)
        report = self._audit()
        self.assertFalse(report.ok)
        msgs = report.skills[0].failures
        self.assertTrue(any("does not match directory" in m for m in msgs), msgs)

    def test_missing_skill_md_fails(self) -> None:
        (self.skills_dir / "hf-empty").mkdir()
        report = self._audit()
        self.assertFalse(report.ok)
        msgs = report.skills[0].failures
        self.assertTrue(any("missing SKILL.md" in m for m in msgs), msgs)

    def test_code_block_headings_are_ignored(self) -> None:
        body = COMPLIANT_BODY.replace(
            "## Verification",
            "```markdown\n## 和其他 Skill 的区别\n```\n\n## Verification",
        )
        write_skill(self.skills_dir, "hf-example", body)
        report = self._audit()
        self.assertTrue(report.ok, msg=str(report.skills[0].failures))


if __name__ == "__main__":
    unittest.main()

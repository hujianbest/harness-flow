#!/usr/bin/env python3
"""Sanity tests for scripts/audit-skill-anatomy.py.

Run: python scripts/test_audit_skill_anatomy.py

Covers the heuristics that are easiest to regress:
- description that uses "适用于 ... (→ skill-x)" classifier MUST NOT be flagged
  as a workflow summary (regression guard for the false-positive that surfaced
  on 2026-04-28).
- description that has no classifier anchors AND ≥2 narration signals SHOULD
  be flagged as a summary.
- has_section() must match section names case-insensitively and recognize the
  canonical anatomy sections (Object Contract, Methodology, Red Flags,
  Common Rationalizations).
- Workflow audit reports `hard_pass=False` when an anatomy-mandated section is
  missing.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "audit-skill-anatomy.py"

spec = importlib.util.spec_from_file_location("audit_skill_anatomy", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["audit_skill_anatomy"] = mod
spec.loader.exec_module(mod)


def test_classifier_with_arrow_reroute_is_not_summary() -> None:
    desc = (
        "适用于尚无已批准规格、现有规格仍是草稿、或规格被 hf-spec-review 退回需修订"
        "的场景。不适用于已有批准规格（→ hf-design）、需要任务计划（→ hf-tasks）。"
    )
    assert mod.description_is_classifier(desc)
    assert not mod.description_looks_like_summary(desc)


def test_pure_narration_is_summary() -> None:
    desc = (
        "Read evidence, decide profile → dispatch reviewer → continue execution. "
        "First read evidence, then route. Step 1 ... step 2 ..."
    )
    assert not mod.description_is_classifier(desc)
    assert mod.description_looks_like_summary(desc)


def test_use_when_classifier_passes() -> None:
    desc = "Use when completion gate already allows closeout. Not for ongoing tasks."
    assert mod.description_is_classifier(desc)
    assert not mod.description_looks_like_summary(desc)


def _write_skill(tmp: Path, body: str) -> mod.SkillAudit:
    skill_dir = tmp / "skills" / "hf-sample"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    return mod.audit_skill(skill_dir)


def test_object_contract_missing_no_longer_blocks_hard_pass() -> None:
    """Q1=B: Object Contract is recommended in v0.1.0, not a hard fail.

    A workflow skill that has every mandatory section but lacks Object
    Contract should still pass anatomy hard checks. It will, however, be
    listed under P2 (recommended) and Object Contract should appear in
    missing_workflow_recommended, not missing_workflow_required.
    """
    body = (
        "---\n"
        "name: hf-sample\n"
        "description: 适用于演示用例。不适用于生产。\n"
        "---\n"
        "\n"
        "# Sample\n"
        "\n"
        "## When to Use\n"
        "## Methodology\n"
        "## Workflow\n"
        "1. step\n"
        "## Red Flags\n"
        "## Common Rationalizations\n"
        "## Verification\n"
    )
    with tempfile.TemporaryDirectory() as td:
        a = _write_skill(Path(td), body)
        assert a.is_workflow_skill
        assert not a.has_object_contract
        assert "Object Contract" not in a.missing_workflow_required
        assert "Object Contract" in a.missing_workflow_recommended
        assert a.hard_pass
        assert a.release_gate_pass


def test_methodology_missing_still_blocks_hard_pass() -> None:
    """Methodology stays mandatory for workflow skills."""
    body = (
        "---\n"
        "name: hf-sample\n"
        "description: 适用于演示用例。不适用于生产。\n"
        "---\n"
        "\n"
        "# Sample\n"
        "\n"
        "## When to Use\n"
        "## Workflow\n"
        "1. step\n"
        "## Red Flags\n"
        "## Common Rationalizations\n"
        "## Verification\n"
    )
    with tempfile.TemporaryDirectory() as td:
        a = _write_skill(Path(td), body)
        assert "Methodology" in a.missing_workflow_required
        assert not a.hard_pass


def test_common_rationalizations_missing_passes_hard_but_fails_release_gate() -> None:
    """ADR-001 D8: CR is the v0.1.0 release gate, layered above hard checks."""
    body = (
        "---\n"
        "name: hf-sample\n"
        "description: 适用于演示用例。不适用于生产。\n"
        "---\n"
        "\n"
        "# Sample\n"
        "\n"
        "## When to Use\n"
        "## Methodology\n"
        "## Workflow\n"
        "1. step\n"
        "## Red Flags\n"
        "## Verification\n"
    )
    with tempfile.TemporaryDirectory() as td:
        a = _write_skill(Path(td), body)
        assert a.hard_pass
        assert not a.has_common_rationalizations
        assert "Common Rationalizations" in a.missing_release_gate
        assert not a.release_gate_pass


def test_audit_passes_minimal_v01_workflow_skill() -> None:
    body = (
        "---\n"
        "name: hf-sample\n"
        "description: 适用于演示用例。不适用于生产。\n"
        "---\n"
        "\n"
        "# Sample\n"
        "\n"
        "## When to Use\n"
        "## Object Contract\n"
        "## Methodology\n"
        "## Workflow\n"
        "1. step\n"
        "## Red Flags\n"
        "## Common Rationalizations\n"
        "## Verification\n"
    )
    with tempfile.TemporaryDirectory() as td:
        a = _write_skill(Path(td), body)
        assert a.has_object_contract
        assert a.has_methodology
        assert a.has_red_flags
        assert a.has_common_rationalizations
        assert a.has_numbered_workflow
        assert not a.missing_required
        assert not a.missing_workflow_required
        assert not a.missing_release_gate
        assert a.hard_pass
        assert a.release_gate_pass


def main() -> int:
    failures = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
        except AssertionError as exc:
            failures += 1
            print(f"FAIL {name}: {exc}")
        except Exception as exc:
            failures += 1
            print(f"ERROR {name}: {exc!r}")
        else:
            print(f"ok   {name}")
    if failures:
        print(f"\n{failures} test(s) failed")
        return 1
    print("\nall tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

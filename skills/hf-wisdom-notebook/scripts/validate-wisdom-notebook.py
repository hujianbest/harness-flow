#!/usr/bin/env python3
"""Validate the wisdom notebook of an HF feature.

Schema reference: skills/hf-wisdom-notebook/references/notebook-schema.md
Authoritative caller: hf-completion-gate (per spec FR-002 acceptance #2).

Checks:
  1. All 5 notepad files exist (learnings.md / decisions.md / issues.md /
     verification.md / problems.md).
  2. Every TASK referenced in progress.md `## Wisdom Delta` has at least one
     entry in learnings.md OR verification.md (per FR-002 / design §3.1
     `wisdom-skip` exception NOT yet implemented; explicit wisdom-skip lines
     in progress.md count as passing).
  3. No duplicate entry-id within any single notepad file
     (`learn-NNNN` / `dec-NNNN` / `iss-NNNN` / `verify-NNNN` / `prob-NNNN`).
  4. Entry-id sequence per file: under --strict, must be globally monotonic
     (no gaps allowed and must be ascending); under default, gaps and
     descending sequences are reported as WARN but do not fail.

Exit codes:
  0 = PASS (all checks passed; or only WARN under non-strict mode)
  1 = FAIL (validation issue; one or more checks failed)
  2 = invalid args / IO error (--feature points to a missing path, etc.)

Usage:
  python3 skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py \\
      --feature features/<feature-id>/ [--strict]

stdlib only — no third-party dependencies.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable


NOTEPAD_FILES = {
    "learnings.md":   "learn",
    "decisions.md":   "dec",
    "issues.md":      "iss",
    "verification.md": "verify",
    "problems.md":    "prob",
}

ENTRY_ID_RE = re.compile(r"^-\s*entry-id:\s*`?([a-z]+-\d{4})`?", re.MULTILINE)
TASK_HEADING_RE = re.compile(r"^##\s+(TASK-\d+)\b", re.MULTILINE)
WISDOM_DELTA_TASK_RE = re.compile(r"^\|\s*(TASK-\d+)\s*\|", re.MULTILINE)
WISDOM_SKIP_RE = re.compile(r"wisdom-skip:\s*(TASK-\d+)", re.IGNORECASE)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="validate-wisdom-notebook.py",
        description=(
            "Validate the wisdom notebook of an HF feature. "
            "Checks 5 file presence, per-task delta coverage, entry-id "
            "uniqueness, and (with --strict) entry-id monotonicity. "
            "Schema: skills/hf-wisdom-notebook/references/notebook-schema.md"
        ),
        epilog=(
            "exit codes:\n"
            "  0 = PASS (all checks passed; WARN under non-strict still PASS)\n"
            "  1 = FAIL (one or more validation checks failed)\n"
            "  2 = invalid args / IO error (--feature path missing)\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--feature", required=True,
                        help="path to the feature directory (e.g. features/002-omo-inspired-v0.6/)")
    parser.add_argument("--strict", action="store_true",
                        help="treat entry-id non-monotonicity as FAIL instead of WARN")
    return parser.parse_args(argv)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _check_files_present(feature_dir: Path) -> tuple[list[str], list[str]]:
    """Return (errors, file_contents_by_name)."""
    errors = []
    notepads_dir = feature_dir / "notepads"
    if not notepads_dir.is_dir():
        errors.append(f"FAIL: notepads/ directory missing at {notepads_dir}")
        return errors, {}
    contents = {}
    for name in NOTEPAD_FILES:
        f = notepads_dir / name
        if not f.is_file():
            errors.append(f"FAIL: missing notepad file: notepads/{name}")
        else:
            contents[name] = _read(f)
    return errors, contents


def _entries_in(text: str) -> list[str]:
    return ENTRY_ID_RE.findall(text)


def _check_per_task_delta(feature_dir: Path, file_contents: dict) -> list[str]:
    errors = []
    progress = feature_dir / "progress.md"
    if not progress.is_file():
        # progress.md missing is not strictly part of FR-002; skip silently.
        return errors
    progress_text = _read(progress)
    delta_section = re.search(
        r"^##\s+Wisdom Delta\b(.*?)(?=^##\s+|\Z)",
        progress_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not delta_section:
        return errors
    body = delta_section.group(1)
    claimed_tasks = set(WISDOM_DELTA_TASK_RE.findall(body))
    skipped = set(WISDOM_SKIP_RE.findall(progress_text))

    learnings_tasks = set(TASK_HEADING_RE.findall(file_contents.get("learnings.md", "")))
    verification_tasks = set(TASK_HEADING_RE.findall(file_contents.get("verification.md", "")))

    for task in sorted(claimed_tasks):
        if task in skipped:
            continue
        if task not in learnings_tasks and task not in verification_tasks:
            errors.append(
                f"FAIL: {task} claimed in progress.md ## Wisdom Delta but has no entry in "
                f"learnings.md or verification.md (FR-002 requires at least one)"
            )
    return errors


def _check_unique_entry_ids(file_contents: dict) -> list[str]:
    errors = []
    for fname, text in file_contents.items():
        ids = _entries_in(text)
        seen = {}
        for idx, entry_id in enumerate(ids):
            if entry_id in seen:
                errors.append(
                    f"FAIL: duplicate entry-id {entry_id} in notepads/{fname} "
                    f"(first at occurrence {seen[entry_id]+1}, again at {idx+1})"
                )
            else:
                seen[entry_id] = idx
    return errors


def _check_monotonic(file_contents: dict, strict: bool) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors, warnings = [], []
    for fname, text in file_contents.items():
        ids = _entries_in(text)
        if len(ids) < 2:
            continue
        # Notepad files are append-newest-on-top per schema, so the *file order*
        # of entries is reverse of write order. Validator checks that the
        # numeric sequence (when reversed to chronological) is monotonically
        # increasing.
        nums = [int(eid.rsplit("-", 1)[1]) for eid in ids]
        chrono = list(reversed(nums))
        non_monotonic = any(chrono[i] >= chrono[i + 1] for i in range(len(chrono) - 1))
        gaps = any(chrono[i + 1] - chrono[i] > 1 for i in range(len(chrono) - 1))
        if non_monotonic or gaps:
            msg = (
                f"notepads/{fname}: entry-id sequence is non-monotonic or has gaps "
                f"(chronological order: {chrono})"
            )
            if strict:
                errors.append("FAIL: " + msg)
            else:
                warnings.append("WARN: " + msg)
    return errors, warnings


def main(argv: Iterable[str]) -> int:
    args = _parse_args(list(argv))

    feature_dir = Path(args.feature)
    if not feature_dir.is_dir():
        print(f"ERROR: --feature path is not a directory: {feature_dir}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []

    file_errors, file_contents = _check_files_present(feature_dir)
    errors.extend(file_errors)

    if file_contents:
        errors.extend(_check_per_task_delta(feature_dir, file_contents))
        errors.extend(_check_unique_entry_ids(file_contents))
        mono_errors, mono_warnings = _check_monotonic(file_contents, args.strict)
        errors.extend(mono_errors)
        warnings.extend(mono_warnings)

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    if errors:
        print(f"\nValidation FAILED ({len(errors)} error(s), {len(warnings)} warning(s)).")
        return 1
    print(f"\nValidation PASSED ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

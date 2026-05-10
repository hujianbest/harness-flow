#!/usr/bin/env python3
"""Walking-skeleton regression diff for HF v0.6.0 orchestrator-extraction.

Compares baseline (v0.5.x walking-skeleton output) with candidate (v0.6.0 same
walking-skeleton re-run) and emits PASS/FAIL based on a hard-coded allowlist
of permitted differences.

Allowlist patterns (per design D-RegrImpl):
  - timestamp date `YYYY-MM-DD`
  - timestamp time `HH:MM:SS`
  - generator-script path migration text fragment
    (`scripts/render-closeout-html.py` ↔ `skills/hf-finalize/scripts/render-closeout-html.py`)
  - HTML render-time comment `<!-- Rendered at ... -->`

Stdlib-only (per ADR-006 D1 stdlib-only stance + design D-RegrImpl).

Usage:
    python3 regression-diff.py --baseline-dir <path> --candidate-dir <path>

Exit codes:
    0 -> PASS (all diffs fall within allowlist)
    1 -> FAIL (at least one diff outside allowlist)
    2 -> usage error / missing input

Owners: features/001-orchestrator-extraction (one-shot tool per OQ-N-003 / D-RegrLoc).
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import Iterable

# Hard-coded allowlist (per design D-RegrImpl). Each entry is a pre-compiled
# regex that, when matched on a single diff hunk line, marks that diff as
# permissible. Keep this list small and explicit; expansion requires a new ADR.
ALLOWLIST_PATTERNS = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),                           # ISO date
    re.compile(r"\b\d{2}:\d{2}:\d{2}\b"),                           # 24h time
    re.compile(
        r"scripts/render-closeout-html\.py|"
        r"skills/hf-finalize/scripts/render-closeout-html\.py"
    ),                                                              # ADR-006 path migration
    re.compile(r"<!--\s*Rendered at .*?-->"),                       # HTML render-time comment
]

# Files we expect to exist under each walking-skeleton output dir.
# This list is intentionally conservative — additions need a new ADR.
EXPECTED_FILES = [
    "closeout.md",
    "closeout.html",
]


def collect_files(root: Path) -> list[Path]:
    """Return sorted relative paths of all regular files under root.

    Walks recursively. Symlinks are skipped (not part of HF stdlib-only
    contract). Raises FileNotFoundError if root is not a directory; the
    caller (main()) translates this into the appropriate exit code.
    """
    if not root.is_dir():
        raise FileNotFoundError(f"Not a directory: {root}")
    files: list[Path] = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and not p.is_symlink():
            files.append(p.relative_to(root))
    return files


def line_is_allowed(line: str) -> bool:
    """A diff hunk line is allowed if any allowlist regex finds at least one
    match in the line content (excluding the leading `+`/`-` marker)."""
    payload = line[1:] if line and line[0] in "+-" else line
    return any(pat.search(payload) for pat in ALLOWLIST_PATTERNS)


def diff_two_files(
    baseline: Path, candidate: Path, rel: Path
) -> list[str]:
    """Return list of unallowed diff hunks (each as a single-line summary).

    Empty list = no unallowed diff.
    """
    if not baseline.exists() and candidate.exists():
        return [f"NEW: {rel} appeared only in candidate"]
    if baseline.exists() and not candidate.exists():
        return [f"MISSING: {rel} present only in baseline"]
    if not baseline.exists() and not candidate.exists():
        return []  # both absent — silent no-op

    base_lines = baseline.read_text(
        encoding="utf-8", errors="replace"
    ).splitlines(keepends=False)
    cand_lines = candidate.read_text(
        encoding="utf-8", errors="replace"
    ).splitlines(keepends=False)

    unallowed: list[str] = []
    diff = list(
        difflib.unified_diff(
            base_lines,
            cand_lines,
            fromfile=str(rel) + " (baseline)",
            tofile=str(rel) + " (candidate)",
            n=0,
        )
    )
    # difflib emits hunk headers (---/+++/@@); filter for change lines only
    for line in diff:
        if not line:
            continue
        if line.startswith(("---", "+++", "@@")):
            continue
        if line[0] not in "+-":
            continue
        if line_is_allowed(line):
            continue
        unallowed.append(f"{rel}: {line}")
    return unallowed


def run(baseline_dir: Path, candidate_dir: Path) -> int:
    """Return process exit code (0 PASS / 1 FAIL)."""
    baseline_files = set(collect_files(baseline_dir))
    candidate_files = set(collect_files(candidate_dir))

    # Sanity-check expected files (each side should have them).
    for expected in EXPECTED_FILES:
        for label, root, files in (
            ("baseline", baseline_dir, baseline_files),
            ("candidate", candidate_dir, candidate_files),
        ):
            if Path(expected) not in files:
                print(
                    f"FAIL: expected file {expected} missing in {label} "
                    f"({root})",
                    file=sys.stderr,
                )
                return 1

    union = sorted(baseline_files | candidate_files)
    unallowed_total: list[str] = []
    for rel in union:
        unallowed_total.extend(
            diff_two_files(baseline_dir / rel, candidate_dir / rel, rel)
        )

    if unallowed_total:
        print("FAIL: unallowed diffs detected:")
        for entry in unallowed_total:
            print(f"  {entry}")
        return 1
    print("PASS: all diffs fall within allowlist")
    print(
        f"  files compared: {len(union)} "
        f"({len(baseline_files & candidate_files)} both sides, "
        f"{len(baseline_files - candidate_files)} baseline-only, "
        f"{len(candidate_files - baseline_files)} candidate-only)"
    )
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Walking-skeleton regression diff for HF v0.6.0 "
            "orchestrator-extraction. Stdlib-only."
        ),
    )
    parser.add_argument(
        "--baseline-dir",
        required=True,
        type=Path,
        help="Path to v0.5.x walking-skeleton output dir.",
    )
    parser.add_argument(
        "--candidate-dir",
        required=True,
        type=Path,
        help="Path to v0.6.0 walking-skeleton output dir.",
    )
    args = parser.parse_args(argv)
    try:
        return run(args.baseline_dir, args.candidate_dir)
    except FileNotFoundError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

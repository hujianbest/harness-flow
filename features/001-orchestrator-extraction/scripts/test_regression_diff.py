#!/usr/bin/env python3
"""Tests for regression-diff.py (NFR-005 acceptance e/i/iii).

Runs 3 test cases:
  1. Self-consistency: diff a directory against itself → PASS
  2. Mutation: introduce a non-allowlist diff → FAIL
  3. Allowlisted diff: change a timestamp → PASS

Stdlib-only (no pytest); minimal harness for CI / hf-test-driven-dev T4.f.
Exit 0 = all tests pass; exit 1 = any failure.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

# Ensure the script under test is importable (alongside this test file).
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "regression_diff", SCRIPT_DIR / "regression-diff.py"
)
assert spec is not None and spec.loader is not None
regression_diff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(regression_diff)


def make_baseline(tmp: Path) -> Path:
    """Create a minimal walking-skeleton-shaped directory for tests."""
    d = tmp / "baseline"
    d.mkdir(parents=True, exist_ok=True)
    (d / "closeout.md").write_text(
        "# Closeout\n"
        "\n"
        "- Status: closed\n"
        "- Closed at: 2026-05-01 12:34:56\n"
        "\n"
        "## Evidence Matrix\n"
        "\n"
        "| Item | Result |\n"
        "|---|---|\n"
        "| RED | PASS |\n",
        encoding="utf-8",
    )
    (d / "closeout.html").write_text(
        "<!DOCTYPE html>\n"
        "<html><body>\n"
        "<!-- Rendered at 2026-05-01 12:34:56 by "
        "scripts/render-closeout-html.py -->\n"
        "<h1>Closeout</h1>\n"
        "<p>Status: closed</p>\n"
        "</body></html>\n",
        encoding="utf-8",
    )
    return d


def test_self_consistency(tmp: Path) -> bool:
    """Same directory diffed against itself → PASS (exit 0)."""
    baseline = make_baseline(tmp)
    rc = regression_diff.run(baseline, baseline)
    return rc == 0


def test_mutation_outside_allowlist(tmp: Path) -> bool:
    """Inject a non-allowlist diff → FAIL (exit 1).

    We change `Status: closed` → `Status: open` in candidate; this is a
    semantic regression and must be caught.
    """
    baseline = make_baseline(tmp)
    candidate = tmp / "candidate"
    shutil.copytree(baseline, candidate)
    closeout = candidate / "closeout.md"
    text = closeout.read_text(encoding="utf-8")
    text = text.replace("Status: closed", "Status: open")
    closeout.write_text(text, encoding="utf-8")
    rc = regression_diff.run(baseline, candidate)
    return rc == 1


def test_allowlist_timestamp(tmp: Path) -> bool:
    """Change only timestamps → PASS (exit 0)."""
    baseline = make_baseline(tmp)
    candidate = tmp / "candidate"
    shutil.copytree(baseline, candidate)
    closeout = candidate / "closeout.md"
    text = closeout.read_text(encoding="utf-8")
    text = text.replace("2026-05-01", "2026-05-10").replace(
        "12:34:56", "23:45:01"
    )
    closeout.write_text(text, encoding="utf-8")
    html = candidate / "closeout.html"
    html.write_text(
        html.read_text(encoding="utf-8").replace(
            "Rendered at 2026-05-01 12:34:56",
            "Rendered at 2026-05-10 23:45:01",
        ),
        encoding="utf-8",
    )
    rc = regression_diff.run(baseline, candidate)
    return rc == 0


def main() -> int:
    cases = [
        ("self_consistency", test_self_consistency),
        ("mutation_outside_allowlist", test_mutation_outside_allowlist),
        ("allowlist_timestamp", test_allowlist_timestamp),
    ]
    failed: list[str] = []
    with tempfile.TemporaryDirectory() as td_str:
        td = Path(td_str)
        for name, fn in cases:
            case_tmp = td / name
            case_tmp.mkdir()
            try:
                ok = fn(case_tmp)
            except Exception as exc:  # pragma: no cover - defensive
                ok = False
                print(f"[ERROR] {name}: {exc}")
            print(f"  {'PASS' if ok else 'FAIL'}: {name}")
            if not ok:
                failed.append(name)
    if failed:
        print(f"FAIL: {len(failed)}/{len(cases)} test cases failed: {failed}")
        return 1
    print(f"PASS: {len(cases)}/{len(cases)} test cases passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Unit tests for scripts/render-closeout-html.py.

Run with:
    python3 -m pytest scripts/test_render_closeout_html.py -q
or:
    python3 scripts/test_render_closeout_html.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

_HERE = Path(__file__).parent
_SPEC = importlib.util.spec_from_file_location(
    "render_closeout_html", _HERE / "render-closeout-html.py"
)
assert _SPEC and _SPEC.loader
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["render_closeout_html"] = _MOD
_SPEC.loader.exec_module(_MOD)  # type: ignore[union-attr]


SAMPLE_TASK_CLOSEOUT = """\
# Closeout

## Closeout Summary

- Closeout Type: `task-closeout`
- Scope: T03 only
- Conclusion: 通过，准备 router 选下一任务
- Based On Completion Record: `verification/completion-task-003.md`
- Based On Regression Record: `verification/regression-2026-05-09.md`

## Evidence Matrix

| Artifact | Record Path | Status | Notes |
|---|---|---|---|
| Spec | `spec.md` | present | 状态：已批准 |
| UI design / UI review | — | N/A (profile skipped) | spec 未声明 UI surface |
| Test review (T3) | `reviews/test-review-task-003.md` | present | 通过 |
| Code review (T3) | `reviews/code-review-task-003.md` | present | 通过 |
| Regression gate | `verification/regression-2026-05-09.md` | present | 通过 |
| Completion gate | `verification/completion-task-003.md` | present | 通过 |

## State Sync

- Current Stage: `hf-workflow-router`
- Current Active Task: T03（已完成）
- Workspace Isolation: in-place
- Worktree Path: N/A
- Worktree Branch: `cursor/feature-foo`
- Worktree Disposition: `kept-for-pr`

## Release / Docs Sync

- Release Notes Path: `CHANGELOG.md`（v1.5.0 入口）
- CHANGELOG Path: `CHANGELOG.md`
- Updated Long-Term Assets:
  - `docs/adr/0007-foo.md`（status: proposed → accepted）
  - `docs/architecture.md`（更新 §3）
- Status Fields Synced: spec / design / tasks 状态保持已批准
- Index Updated: README.md `## Active Features` 行

## Handoff

- Remaining Approved Tasks: T04, T05
- Next Action Or Recommended Skill: `hf-workflow-router`
- PR / Branch Status: 本任务在 `cursor/feature-foo` 分支
- Limits / Open Notes:
  - T04 依赖外部接口尚未冻结，可能再次回 `hf-specify`
  - 本次未跑 e2e UI 测试（profile = standard, 未启用）
"""


SAMPLE_BLOCKED = """\
# Closeout

## Closeout Summary

- Closeout Type: `blocked`
- Scope: 不进入 closeout
- Conclusion: precheck 失败，回 router
- Based On Completion Record: `verification/completion-task-002.md`
- Based On Regression Record: 缺失

## Evidence Matrix

- Artifact: Completion gate
- Record Path: `verification/completion-task-002.md`
- Status: present
- Notes: 通过

- Artifact: Regression gate
- Record Path: `verification/regression-*.md`
- Status: missing
- Notes: 找不到对应记录

## State Sync

- Current Stage: `hf-workflow-router`
- Current Active Task: T02
- Workspace Isolation: in-place

## Handoff

- Remaining Approved Tasks: 不确定
- Next Action Or Recommended Skill: `hf-workflow-router`
"""


VITEST_LOG = """\

> @demo/foo@0.1.0 test
> vitest run --reporter=verbose

 RUN  v2.1.9 /workspace/demo

 ✓ test/foo.test.ts > Foo > does the thing
 ✓ test/bar.test.ts > Bar > also does the thing

 Test Files  2 passed (2)
      Tests  18 passed (18)
   Start at  10:00:00
   Duration  512ms (transform 100ms)
"""


PYTEST_LOG = """\
============================= test session starts ==============================
collected 7 items

test/foo.py ........

============================== 7 passed in 0.42s ===============================
"""


COVERAGE_JSON = {
    "total": {
        "lines":      {"total": 100, "covered": 92, "skipped": 0, "pct": 92.0},
        "statements": {"total": 110, "covered": 100, "skipped": 0, "pct": 90.9},
        "functions":  {"total": 30,  "covered": 27, "skipped": 0, "pct": 90.0},
        "branches":   {"total": 50,  "covered": 35, "skipped": 0, "pct": 70.0},
    }
}


def _make_feature(tmp: Path, closeout_md: str) -> Path:
    fdir = tmp / "features" / "001-demo"
    (fdir / "evidence").mkdir(parents=True, exist_ok=True)
    (fdir / "verification").mkdir(parents=True, exist_ok=True)
    (fdir / "closeout.md").write_text(closeout_md, encoding="utf-8")
    return fdir


class TestParseCloseout(unittest.TestCase):
    def test_parses_summary_fields(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), SAMPLE_TASK_CLOSEOUT)
            pack = _MOD.parse_closeout(fdir)
            self.assertEqual(pack.closeout_type, "task-closeout")
            self.assertEqual(pack.closeout_type_kind(), "task-closeout")
            self.assertEqual(pack.scope, "T03 only")
            self.assertIn("通过", pack.conclusion)
            self.assertEqual(
                pack.based_on_completion,
                "verification/completion-task-003.md",
            )

    def test_parses_evidence_table(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), SAMPLE_TASK_CLOSEOUT)
            pack = _MOD.parse_closeout(fdir)
            self.assertEqual(len(pack.evidence), 6)
            ui_row = next(
                r for r in pack.evidence if r.artifact.startswith("UI")
            )
            self.assertEqual(ui_row.status_kind, "na")
            comp_row = next(
                r for r in pack.evidence if "Completion" in r.artifact
            )
            self.assertEqual(comp_row.status_kind, "present")

    def test_parses_evidence_bullet_form(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), SAMPLE_BLOCKED)
            pack = _MOD.parse_closeout(fdir)
            self.assertEqual(len(pack.evidence), 2)
            self.assertEqual(
                {r.status_kind for r in pack.evidence},
                {"present", "missing"},
            )

    def test_parses_state_release_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), SAMPLE_TASK_CLOSEOUT)
            pack = _MOD.parse_closeout(fdir)
            self.assertEqual(pack.state_sync["Worktree Disposition"], "`kept-for-pr`")
            self.assertEqual(
                pack.handoff["Next Action Or Recommended Skill"],
                "`hf-workflow-router`",
            )
            self.assertEqual(len(pack.updated_long_term_assets), 2)
            self.assertEqual(len(pack.limits_notes), 2)

    def test_blocked_closeout_kind(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), SAMPLE_BLOCKED)
            pack = _MOD.parse_closeout(fdir)
            self.assertEqual(pack.closeout_type_kind(), "blocked")

    def test_missing_closeout_md_raises(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = Path(td) / "empty"
            fdir.mkdir()
            with self.assertRaises(FileNotFoundError):
                _MOD.parse_closeout(fdir)


class TestEvidenceParsing(unittest.TestCase):
    def test_vitest_log(self) -> None:
        stats = _MOD._parse_test_log(VITEST_LOG)
        self.assertEqual(stats.tests_passed, 18)
        self.assertEqual(stats.tests_total, 18)
        self.assertEqual(stats.files_passed, 2)
        self.assertEqual(stats.files_total, 2)
        self.assertAlmostEqual(stats.duration_ms or 0.0, 512.0, places=1)
        self.assertAlmostEqual(stats.pass_rate or 0.0, 1.0)

    def test_pytest_log(self) -> None:
        stats = _MOD._parse_test_log(PYTEST_LOG)
        self.assertEqual(stats.tests_passed, 7)
        self.assertEqual(stats.tests_total, 7)
        self.assertAlmostEqual(stats.duration_ms or 0.0, 420.0, places=1)

    def test_coverage_json(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), SAMPLE_TASK_CLOSEOUT)
            (fdir / "evidence" / "regression-2026-05-09.log").write_text(
                VITEST_LOG, encoding="utf-8"
            )
            (fdir / "verification" / "coverage.json").write_text(
                json.dumps(COVERAGE_JSON), encoding="utf-8"
            )
            pack = _MOD.parse_closeout(fdir)
            self.assertEqual(pack.test_stats.tests_total, 18)
            self.assertAlmostEqual(pack.coverage.lines or 0.0, 92.0)
            self.assertAlmostEqual(pack.coverage.branches or 0.0, 70.0)
            self.assertEqual(pack.coverage.source, "verification/coverage.json")

    def test_coverage_inline_kv(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            md = SAMPLE_TASK_CLOSEOUT
            fdir = _make_feature(Path(td), md)
            (fdir / "verification" / "regression-2026-05-09.md").write_text(
                "# Regression\n\n## Coverage\n\n- Lines: 88.2%\n- Branches: 65%\n",
                encoding="utf-8",
            )
            pack = _MOD.parse_closeout(fdir)
            self.assertAlmostEqual(pack.coverage.lines or 0.0, 88.2)
            self.assertAlmostEqual(pack.coverage.branches or 0.0, 65.0)


class TestRender(unittest.TestCase):
    def test_render_full(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), SAMPLE_TASK_CLOSEOUT)
            (fdir / "evidence" / "regression-2026-05-09.log").write_text(
                VITEST_LOG, encoding="utf-8"
            )
            (fdir / "verification" / "coverage.json").write_text(
                json.dumps(COVERAGE_JSON), encoding="utf-8"
            )
            pack = _MOD.parse_closeout(fdir)
            html = _MOD.render_html(pack)
            self.assertIn("<!doctype html>", html)
            self.assertIn("Closeout 报告", html)
            self.assertIn("task-closeout", html)
            self.assertIn("18/18", html)
            self.assertIn("92.0%", html)  # lines coverage
            self.assertIn("Workflow Trace", html)
            self.assertIn("Evidence Matrix", html)
            self.assertIn("evidence-search", html)  # JS hook id
            # Sanitization: no raw `<` from markdown bullet content
            self.assertNotIn("<script>alert", html)

    def test_render_blocked_minimal(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), SAMPLE_BLOCKED)
            pack = _MOD.parse_closeout(fdir)
            html = _MOD.render_html(pack)
            self.assertIn("blocked", html)
            self.assertIn("status-missing", html)
            self.assertIn("未在 evidence/", html)  # tests panel empty state

    def test_main_writes_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), SAMPLE_TASK_CLOSEOUT)
            rc = _MOD.main([str(fdir), "--quiet"])
            self.assertEqual(rc, 0)
            self.assertTrue((fdir / "closeout.html").is_file())

    def test_main_missing_closeout(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fdir = Path(td) / "no-closeout"
            fdir.mkdir()
            rc = _MOD.main([str(fdir), "--quiet"])
            self.assertEqual(rc, 1)


class TestHtmlEscaping(unittest.TestCase):
    def test_escapes_user_provided_strings(self) -> None:
        nasty = SAMPLE_TASK_CLOSEOUT.replace(
            "通过，准备 router 选下一任务",
            "<script>alert('xss')</script> & friends",
        )
        with tempfile.TemporaryDirectory() as td:
            fdir = _make_feature(Path(td), nasty)
            pack = _MOD.parse_closeout(fdir)
            html = _MOD.render_html(pack)
            self.assertNotIn("<script>alert('xss')", html)
            self.assertIn("&lt;script&gt;alert", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)

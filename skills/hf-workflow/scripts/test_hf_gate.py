#!/usr/bin/env python3
"""Tests for hf_gate.py — HarnessFlow 机械门禁脚本。

运行: python3 skills/hf-workflow/scripts/test_hf_gate.py
"""

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hf_gate  # noqa: E402

TS1 = "20260703T100000Z"
TS2 = "20260703T110000Z"
TS3 = "20260703T120000Z"


def make_log(feature: Path, label: str, ts: str, exit_code: int, body: str = "out") -> Path:
    evidence = feature / "evidence"
    evidence.mkdir(exist_ok=True)
    path = evidence / f"{label}-{ts}.log"
    path.write_text(
        "# hf-gate-run\n"
        f"# label: {label}\n"
        "# command: dummy\n"
        f"# started: {ts}\n"
        f"{body}\n"
        f"# exit: {exit_code}\n",
        encoding="utf-8",
    )
    return path


def make_frame(feature: Path, tier: int) -> None:
    feature.mkdir(parents=True, exist_ok=True)
    (feature / "frame.md").write_text(
        "# 某特性 Frame\n\n- 意图: 测试用\n"
        f"- 风险档位: {tier}\n- 档位理由: 测试\n",
        encoding="utf-8",
    )


def make_review(feature: Path, name: str, verdict: str = "通过",
                confirm: str = "2026-07-03", method: str = "subagent") -> None:
    reviews = feature / "reviews"
    reviews.mkdir(exist_ok=True)
    lines = [f"# 评审 (第 1 轮)", "", "- 日期: 2026-07-03",
             f"- 评审方式: {method}", f"- 结论: {verdict}"]
    if confirm is not None:
        lines.append(f"- 用户确认: {confirm}")
    lines += ["", "## Findings", "无"]
    (reviews / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_plan(feature: Path, tasks: list[tuple[str, bool]], doc: str = "plan.md") -> None:
    body = ["# 计划", "", "## 任务清单", ""]
    for tid, done in tasks:
        mark = "x" if done else " "
        body.append(f"- [{mark}] {tid} 某任务 (覆盖: FR-1) — 判据: 测试通过")
    (feature / doc).write_text("\n".join(body) + "\n", encoding="utf-8")


def run_gate(argv: list[str]) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = hf_gate.main(argv)
    return code, buf.getvalue()


class RunCommandTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"
        self.feature.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def test_run_writes_log_with_header_and_exit_zero(self):
        code, out = run_gate([
            "run", "--feature", str(self.feature), "--label", "t1-green",
            "--", sys.executable, "-c", "print('hello-green')",
        ])
        self.assertEqual(code, 0)
        logs = list((self.feature / "evidence").glob("t1-green-*.log"))
        self.assertEqual(len(logs), 1)
        text = logs[0].read_text(encoding="utf-8")
        self.assertIn("# label: t1-green", text)
        self.assertIn("hello-green", text)
        self.assertIn("# exit: 0", text)
        self.assertIn(str(logs[0]), out)

    def test_run_propagates_nonzero_exit(self):
        code, _ = run_gate([
            "run", "--feature", str(self.feature), "--label", "t1-red",
            "--", sys.executable, "-c", "import sys; print('boom'); sys.exit(3)",
        ])
        self.assertEqual(code, 3)
        logs = list((self.feature / "evidence").glob("t1-red-*.log"))
        self.assertEqual(len(logs), 1)
        self.assertIn("# exit: 3", logs[0].read_text(encoding="utf-8"))

    def test_run_rejects_bad_label(self):
        code, _ = run_gate([
            "run", "--feature", str(self.feature), "--label", "Bad Label!",
            "--", "true",
        ])
        self.assertEqual(code, 2)


class CheckPlanTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, target):
        return run_gate(["check", "--feature", str(self.feature), "--to", target])

    def test_fails_without_frame(self):
        self.feature.mkdir(parents=True)
        code, out = self.check("plan")
        self.assertEqual(code, 1)
        self.assertIn("frame.md", out)

    def test_fails_for_tier1(self):
        make_frame(self.feature, 1)
        make_log(self.feature, "baseline", TS1, 0)
        code, out = self.check("plan")
        self.assertEqual(code, 1)

    def test_passes_with_frame_and_baseline(self):
        make_frame(self.feature, 2)
        make_log(self.feature, "baseline", TS1, 0)
        code, out = self.check("plan")
        self.assertEqual(code, 0, out)

    def test_fails_without_baseline_evidence(self):
        make_frame(self.feature, 2)
        code, out = self.check("plan")
        self.assertEqual(code, 1)
        self.assertIn("baseline", out)


class CheckDesignTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"
        make_frame(self.feature, 3)
        make_log(self.feature, "baseline", TS1, 0)
        (self.feature / "spec.md").write_text("# spec\n内容\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def check(self):
        return run_gate(["check", "--feature", str(self.feature), "--to", "design"])

    def test_fails_without_spec_review(self):
        code, _ = self.check()
        self.assertEqual(code, 1)

    def test_passes_with_approved_spec_review(self):
        make_review(self.feature, "spec-review.md")
        code, out = self.check()
        self.assertEqual(code, 0, out)


class CheckBuildTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"

    def tearDown(self):
        self._tmp.cleanup()

    def check(self):
        return run_gate(["check", "--feature", str(self.feature), "--to", "build"])

    def test_tier1_passes_with_frame_and_baseline(self):
        make_frame(self.feature, 1)
        make_log(self.feature, "baseline", TS1, 0)
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_tier2_fails_without_plan_review(self):
        make_frame(self.feature, 2)
        make_log(self.feature, "baseline", TS1, 0)
        make_plan(self.feature, [("T-1", False)])
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("plan-review", out)

    def test_tier2_passes_with_approved_plan_review(self):
        make_frame(self.feature, 2)
        make_log(self.feature, "baseline", TS1, 0)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md")
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_verdict_needs_revision_blocks(self):
        make_frame(self.feature, 2)
        make_log(self.feature, "baseline", TS1, 0)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md", verdict="需修改")
        code, _ = self.check()
        self.assertEqual(code, 1)

    def test_missing_confirmation_blocks(self):
        make_frame(self.feature, 2)
        make_log(self.feature, "baseline", TS1, 0)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md", confirm=None)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("用户确认", out)

    def test_degraded_review_with_auto_approval_blocks(self):
        make_frame(self.feature, 2)
        make_log(self.feature, "baseline", TS1, 0)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md",
                    confirm="auto-approved 2026-07-03", method="主会话降级")
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("主会话降级", out)

    def test_degraded_review_with_real_user_confirmation_passes(self):
        make_frame(self.feature, 2)
        make_log(self.feature, "baseline", TS1, 0)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md",
                    confirm="2026-07-03", method="主会话降级")
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_tier3_requires_both_reviews(self):
        make_frame(self.feature, 3)
        make_log(self.feature, "baseline", TS1, 0)
        (self.feature / "spec.md").write_text("# spec\n内容\n", encoding="utf-8")
        make_plan(self.feature, [("T-1", False)], doc="design.md")
        make_review(self.feature, "spec-review.md")
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("design-review", out)
        make_review(self.feature, "design-review.md")
        code, out = self.check()
        self.assertEqual(code, 0, out)


class CheckVerifyTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"
        make_frame(self.feature, 2)
        make_log(self.feature, "baseline", TS1, 0)
        make_review(self.feature, "plan-review.md")

    def tearDown(self):
        self._tmp.cleanup()

    def check(self):
        return run_gate(["check", "--feature", str(self.feature), "--to", "verify"])

    def test_unchecked_task_blocks(self):
        make_plan(self.feature, [("T-1", True), ("T-2", False)])
        make_log(self.feature, "t1-red", TS1, 1)
        make_log(self.feature, "t1-green", TS2, 0)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("T-2", out)

    def test_missing_red_log_blocks(self):
        make_plan(self.feature, [("T-1", True)])
        make_log(self.feature, "t1-green", TS2, 0)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("red", out)

    def test_red_log_with_exit_zero_blocks(self):
        make_plan(self.feature, [("T-1", True)])
        make_log(self.feature, "t1-red", TS1, 0)
        make_log(self.feature, "t1-green", TS2, 0)
        code, out = self.check()
        self.assertEqual(code, 1)

    def test_green_log_with_nonzero_exit_blocks(self):
        make_plan(self.feature, [("T-1", True)])
        make_log(self.feature, "t1-red", TS1, 1)
        make_log(self.feature, "t1-green", TS2, 2)
        code, _ = self.check()
        self.assertEqual(code, 1)

    def test_complete_red_green_passes(self):
        make_plan(self.feature, [("T-1", True), ("T-2", True)])
        make_log(self.feature, "t1-red", TS1, 1)
        make_log(self.feature, "t1-green", TS2, 0)
        make_log(self.feature, "t2-red", TS2, 1)
        make_log(self.feature, "t2-green", TS3, 0)
        code, out = self.check()
        self.assertEqual(code, 0, out)


class CheckShipTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"
        make_frame(self.feature, 2)
        make_log(self.feature, "baseline", TS1, 0)
        make_review(self.feature, "plan-review.md")
        make_plan(self.feature, [("T-1", True)])
        make_log(self.feature, "t1-red", TS1, 1)
        make_log(self.feature, "t1-green", TS2, 0)

    def tearDown(self):
        self._tmp.cleanup()

    def check(self):
        return run_gate(["check", "--feature", str(self.feature), "--to", "ship"])

    def complete(self):
        make_review(self.feature, "code-review.md")
        make_log(self.feature, "suite", TS3, 0)
        make_log(self.feature, "smoke", TS3, 0)

    def test_missing_code_review_blocks(self):
        make_log(self.feature, "suite", TS3, 0)
        make_log(self.feature, "smoke", TS3, 0)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("code-review", out)

    def test_missing_suite_blocks(self):
        make_review(self.feature, "code-review.md")
        make_log(self.feature, "smoke", TS3, 0)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("suite", out)

    def test_suite_older_than_green_blocks(self):
        self.complete()
        make_log(self.feature, "t1-green", TS3, 0)  # newer green than suite TS3? same ts ok
        make_log(self.feature, "t1-green", "20260703T130000Z", 0)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("suite", out)

    def test_failed_suite_blocks(self):
        make_review(self.feature, "code-review.md")
        make_log(self.feature, "suite", TS3, 1)
        make_log(self.feature, "smoke", TS3, 0)
        code, _ = self.check()
        self.assertEqual(code, 1)

    def test_missing_smoke_blocks(self):
        make_review(self.feature, "code-review.md")
        make_log(self.feature, "suite", TS3, 0)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("smoke", out)

    def test_smoke_screenshot_counts_as_evidence(self):
        make_review(self.feature, "code-review.md")
        make_log(self.feature, "suite", TS3, 0)
        (self.feature / "evidence" / "smoke-login-page.png").write_bytes(b"\x89PNG")
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_complete_ship_passes(self):
        self.complete()
        code, out = self.check()
        self.assertEqual(code, 0, out)


class UsageTest(unittest.TestCase):
    def test_unknown_target_is_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _ = run_gate(["check", "--feature", tmp, "--to", "nonsense"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

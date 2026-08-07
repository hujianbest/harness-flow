#!/usr/bin/env python3
"""Tests for hf_gate.py — HarnessFlow 机械门禁脚本。

运行: python3 skills/hf-workflow/scripts/test_hf_gate.py
"""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hf_gate  # noqa: E402


def make_frame(feature: Path, tier: int, mode: str = "建造", perceivable: str = "否") -> None:
    feature.mkdir(parents=True, exist_ok=True)
    (feature / "frame.md").write_text(
        "# 某特性 Frame\n\n- 意图: 测试用\n"
        f"- 风险档位: {tier}\n- 档位理由: 测试\n"
        f"- 模式: {mode}\n- 用户可感知: {perceivable}\n",
        encoding="utf-8",
    )


def make_review(feature: Path, name: str, verdict: str = "通过",
                confirm: str = "2026-07-03", method: str = "subagent") -> None:
    reviews = feature / "reviews"
    reviews.mkdir(exist_ok=True)
    lines = ["# 评审 (第 1 轮)", "", "- 日期: 2026-07-03",
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
        code, out = self.check("plan")
        self.assertEqual(code, 1)

    def test_passes_with_frame(self):
        make_frame(self.feature, 2)
        code, out = self.check("plan")
        self.assertEqual(code, 0, out)


class CheckDesignTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"
        make_frame(self.feature, 3)
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

    def test_tier1_passes_with_frame(self):
        make_frame(self.feature, 1)
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_tier2_fails_without_plan_review(self):
        make_frame(self.feature, 2)
        make_plan(self.feature, [("T-1", False)])
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("plan-review", out)

    def test_tier2_passes_with_approved_plan_review(self):
        make_frame(self.feature, 2)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md")
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_verdict_needs_revision_blocks(self):
        make_frame(self.feature, 2)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md", verdict="需修改")
        code, _ = self.check()
        self.assertEqual(code, 1)

    def test_missing_confirmation_blocks(self):
        make_frame(self.feature, 2)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md", confirm=None)
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("用户确认", out)

    def test_degraded_review_with_auto_approval_blocks(self):
        make_frame(self.feature, 2)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md",
                    confirm="auto-approved 2026-07-03", method="主会话降级")
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("主会话降级", out)

    def test_degraded_review_with_real_user_confirmation_passes(self):
        make_frame(self.feature, 2)
        make_plan(self.feature, [("T-1", False)])
        make_review(self.feature, "plan-review.md",
                    confirm="2026-07-03", method="主会话降级")
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_tier3_requires_both_reviews(self):
        make_frame(self.feature, 3)
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
        make_review(self.feature, "plan-review.md")

    def tearDown(self):
        self._tmp.cleanup()

    def check(self):
        return run_gate(["check", "--feature", str(self.feature), "--to", "verify"])

    def test_unchecked_task_blocks(self):
        make_plan(self.feature, [("T-1", True), ("T-2", False)])
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("T-2", out)

    def test_all_tasks_done_passes(self):
        make_plan(self.feature, [("T-1", True), ("T-2", True)])
        code, out = self.check()
        self.assertEqual(code, 0, out)


class CheckShipTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"
        make_frame(self.feature, 2, perceivable="否")
        make_review(self.feature, "plan-review.md")
        make_plan(self.feature, [("T-1", True)])

    def tearDown(self):
        self._tmp.cleanup()

    def check(self):
        return run_gate(["check", "--feature", str(self.feature), "--to", "ship"])

    def test_missing_code_review_blocks(self):
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("code-review", out)

    def test_complete_ship_passes(self):
        make_review(self.feature, "code-review.md")
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_perceivable_needs_demo_acceptance(self):
        # Override: perceivable feature needs demo acceptance
        make_frame(self.feature, 2, perceivable="是")
        make_review(self.feature, "code-review.md")
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("demo-acceptance", out)
        make_review(self.feature, "demo-acceptance.md", verdict="接受")
        code, out = self.check()
        self.assertEqual(code, 0, out)


class ExploreModeTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"

    def tearDown(self):
        self._tmp.cleanup()

    def test_explore_cannot_ship(self):
        make_frame(self.feature, 1, mode="探索")
        code, out = run_gate(["check", "--feature", str(self.feature), "--to", "ship"])
        self.assertEqual(code, 1)

    def test_explore_close_needs_conclusion(self):
        make_frame(self.feature, 1, mode="探索")
        code, out = run_gate(["check", "--feature", str(self.feature), "--to", "close"])
        self.assertEqual(code, 1)
        self.assertIn("conclusion", out)
        (self.feature / "conclusion.md").write_text("# 结论\n原型验证了X\n", encoding="utf-8")
        code, out = run_gate(["check", "--feature", str(self.feature), "--to", "close"])
        self.assertEqual(code, 0, out)


class UsageTest(unittest.TestCase):
    def test_unknown_target_is_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _ = run_gate(["check", "--feature", tmp, "--to", "nonsense"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

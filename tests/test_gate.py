#!/usr/bin/env python3
"""Tests for rewritten hf_gate.py (Matt-aligned main chain)."""

from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE_PATH = ROOT / "skills" / "hf-workflow" / "scripts" / "hf_gate.py"

spec = importlib.util.spec_from_file_location("hf_gate", GATE_PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def run_gate(argv):
    out = io.StringIO()
    with redirect_stdout(out), redirect_stderr(out):
        code = gate.main(argv)
    return code, out.getvalue()


def write_feature(feature: Path, mode="建造", perceivable="否"):
    feature.mkdir(parents=True, exist_ok=True)
    (feature / "feature.md").write_text(
        f"# Feature\n\n- 模式: {mode}\n- 用户可感知: {perceivable}\n",
        encoding="utf-8",
    )


def write_review(feature: Path, name, verdict="通过", confirm="2026-08-08",
                 method="subagent"):
    reviews = feature / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / name).write_text(
        f"# 评审\n\n- 评审方式: {method}\n- 结论: {verdict}\n- 用户确认: {confirm}\n",
        encoding="utf-8",
    )


def write_tickets(feature: Path, items: list[tuple[str, bool]]):
    lines = ["# Tickets\n"]
    for tid, done in items:
        mark = "x" if done else " "
        lines.append(f"- [{mark}] {tid} demo — Blocked by: None")
    (feature / "tickets.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def confirm_context(root: Path, date="2026-08-08"):
    path = root / "CONTEXT.md"
    text = path.read_text(encoding="utf-8").replace(
        "- 用户确认:", f"- 用户确认: {date}", 1)
    path.write_text(text, encoding="utf-8")


class InitAndProductTests(unittest.TestCase):
    def test_init_creates_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = run_gate(["init", "--root", str(root)])
            self.assertEqual(code, 0)
            self.assertTrue((root / "CONTEXT.md").is_file())
            self.assertTrue((root / "product" / "assumptions.md").is_file())
            self.assertTrue((root / "features").is_dir())
            self.assertTrue((root / "docs" / "adr").is_dir())

    def test_check_product_requires_context_confirm(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_gate(["init", "--root", str(root)])
            code, out = run_gate(["check", "--product", "--root", str(root)])
            self.assertEqual(code, 1)
            self.assertIn("用户确认", out)
            confirm_context(root)
            code, out = run_gate(["check", "--product", "--root", str(root)])
            self.assertEqual(code, 0)


class CliLocalizationTests(unittest.TestCase):
    def test_root_help_is_chinese_and_preserves_commands(self):
        code, out = run_gate(["--help"])
        self.assertEqual(code, 2)
        self.assertIn("用法：", out)
        self.assertIn("命令:", out)
        self.assertIn("选项:", out)
        for command in ("init", "check", "status", "next"):
            self.assertIn(command, out)
        self.assertNotIn("usage:", out)
        self.assertNotIn("options:", out)
        self.assertNotIn("show this help message and exit", out)

    def test_check_help_is_chinese_and_preserves_parameters(self):
        code, out = run_gate(["check", "--help"])
        self.assertEqual(code, 2)
        for parameter in ("--feature", "--to", "--product", "--root"):
            self.assertIn(parameter, out)
        self.assertIn("目标阶段", out)
        self.assertIn("项目根目录", out)
        self.assertNotIn("usage:", out)
        self.assertNotIn("options:", out)

    def test_invalid_choice_error_is_chinese_and_preserves_choices(self):
        code, out = run_gate(
            ["check", "--feature", "features/001-x", "--to", "nonsense"]
        )
        self.assertEqual(code, 2)
        self.assertIn("错误：", out)
        self.assertIn("无效选项", out)
        self.assertIn("--to", out)
        self.assertIn("nonsense", out)
        for target in gate.TARGETS:
            self.assertIn(target, out)
        self.assertNotIn("invalid choice", out)

    def test_missing_command_error_is_chinese(self):
        code, out = run_gate([])
        self.assertEqual(code, 2)
        self.assertIn("错误：", out)
        self.assertIn("缺少必需参数", out)
        self.assertNotIn("the following arguments are required", out)


class ChainGateTests(unittest.TestCase):
    def test_to_spec_needs_feature_meta(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            feature.mkdir(parents=True)
            code, out = run_gate(["check", "--feature", str(feature), "--to", "to-spec"])
            self.assertEqual(code, 1)
            self.assertIn("feature.md", out)

    def test_to_architecture_needs_spec_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            write_feature(feature)
            code, out = run_gate(["check", "--feature", str(feature), "--to", "to-architecture"])
            self.assertEqual(code, 1)
            self.assertIn("spec.md", out)
            (feature / "spec.md").write_text("# Spec\n", encoding="utf-8")
            write_review(feature, "spec-review.md")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "to-architecture"])
            self.assertEqual(code, 0)

    def test_to_tickets_needs_architecture_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            write_feature(feature)
            (feature / "spec.md").write_text("# Spec\n", encoding="utf-8")
            write_review(feature, "spec-review.md")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "to-tickets"])
            self.assertEqual(code, 1)
            (feature / "architecture.md").write_text("# Arch\n", encoding="utf-8")
            write_review(feature, "architecture-review.md")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "to-tickets"])
            self.assertEqual(code, 0)

    def test_implement_needs_tickets(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            write_feature(feature)
            (feature / "spec.md").write_text("# Spec\n", encoding="utf-8")
            write_review(feature, "spec-review.md")
            (feature / "architecture.md").write_text("# Arch\n", encoding="utf-8")
            write_review(feature, "architecture-review.md")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "implement"])
            self.assertEqual(code, 1)
            self.assertIn("tickets.md", out)
            write_tickets(feature, [("T-01", False)])
            code, out = run_gate(["check", "--feature", str(feature), "--to", "implement"])
            self.assertEqual(code, 0)

    def test_ship_needs_tickets_done_and_code_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            write_feature(feature, perceivable="否")
            (feature / "spec.md").write_text("# Spec\n", encoding="utf-8")
            write_review(feature, "spec-review.md")
            (feature / "architecture.md").write_text("# Arch\n", encoding="utf-8")
            write_review(feature, "architecture-review.md")
            write_tickets(feature, [("T-01", False)])
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 1)
            write_tickets(feature, [("T-01", True)])
            write_review(feature, "code-review.md")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 0)

    def test_perceivable_ship_needs_demo_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            write_feature(feature, perceivable="是")
            (feature / "spec.md").write_text("# Spec\n", encoding="utf-8")
            write_review(feature, "spec-review.md")
            (feature / "architecture.md").write_text("# Arch\n", encoding="utf-8")
            write_review(feature, "architecture-review.md")
            write_tickets(feature, [("T-01", True)])
            write_review(feature, "code-review.md")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 1)
            self.assertIn("demo-acceptance", out)
            write_review(feature, "demo-acceptance.md", verdict="接受")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 0)

    def test_degraded_auto_approved_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            write_feature(feature)
            (feature / "spec.md").write_text("# Spec\n", encoding="utf-8")
            write_review(
                feature, "spec-review.md",
                method="主会话降级", confirm="auto-approved 2026-08-08",
            )
            code, out = run_gate(["check", "--feature", str(feature), "--to", "to-architecture"])
            self.assertEqual(code, 1)
            self.assertIn("禁止 auto-approved", out)


class ExplorationTests(unittest.TestCase):
    def test_explore_cannot_ship(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-p"
            write_feature(feature, mode="探索")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 1)
            self.assertIn("永远不能 ship", out)

    def test_explore_close(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-p"
            write_feature(feature, mode="探索")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "close"])
            self.assertEqual(code, 1)
            (feature / "conclusion.md").write_text("learned", encoding="utf-8")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "close"])
            self.assertEqual(code, 0)

    def test_explore_skips_spec_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-p"
            write_feature(feature, mode="探索")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "to-spec"])
            self.assertEqual(code, 1)
            code, out = run_gate(["check", "--feature", str(feature), "--to", "implement"])
            self.assertEqual(code, 0)


class StatusNextTests(unittest.TestCase):
    def test_status_and_next(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_gate(["init", "--root", str(root)])
            confirm_context(root)
            feature = root / "features" / "001-x"
            write_feature(feature)
            code, out = run_gate(["status", "--root", str(root)])
            self.assertEqual(code, 0)
            self.assertIn("产品层: PASS", out)
            # feature.md alone makes --to to-spec PASS; first FAIL is to-architecture
            self.assertIn("→ to-architecture", out)
            code, out = run_gate(["next", "--root", str(root)])
            self.assertEqual(code, 0)
            self.assertIn("001-x", out)
            self.assertIn("to-architecture", out)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""In-tree tests for hf_gate.py — run: python3 skills/hf-workflow/scripts/test_hf_gate.py"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hf_gate  # noqa: E402


def write_feature(feature: Path, mode="建造", perceivable="否") -> None:
    feature.mkdir(parents=True, exist_ok=True)
    (feature / "feature.md").write_text(
        f"- 模式: {mode}\n- 用户可感知: {perceivable}\n",
        encoding="utf-8",
    )


def write_review(feature: Path, name: str, verdict="通过", confirm="2026-08-08",
                 method="subagent") -> None:
    (feature / "reviews").mkdir(exist_ok=True)
    (feature / "reviews" / name).write_text(
        f"- 评审方式: {method}\n- 结论: {verdict}\n- 用户确认: {confirm}\n",
        encoding="utf-8",
    )


def run_gate(argv: list[str]) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = hf_gate.main(argv)
    return code, buf.getvalue()


class GateChainTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.feature = Path(self._tmp.name) / "features" / "001-x"

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, target):
        return run_gate(["check", "--feature", str(self.feature), "--to", target])

    def test_to_spec_with_meta(self):
        write_feature(self.feature)
        code, out = self.check("to-spec")
        self.assertEqual(code, 0)

    def test_architecture_requires_spec_review(self):
        write_feature(self.feature)
        code, _ = self.check("to-architecture")
        self.assertEqual(code, 1)
        (self.feature / "spec.md").write_text("s", encoding="utf-8")
        write_review(self.feature, "spec-review.md")
        code, _ = self.check("to-architecture")
        self.assertEqual(code, 0)

    def test_ship_full(self):
        write_feature(self.feature)
        (self.feature / "spec.md").write_text("s", encoding="utf-8")
        write_review(self.feature, "spec-review.md")
        (self.feature / "architecture.md").write_text("a", encoding="utf-8")
        write_review(self.feature, "architecture-review.md")
        (self.feature / "tickets.md").write_text("- [x] T-01 done\n", encoding="utf-8")
        write_review(self.feature, "code-review.md")
        code, out = self.check("ship")
        self.assertEqual(code, 0)

    def test_unknown_target(self):
        code, out = run_gate(
            ["check", "--feature", str(self.feature), "--to", "nonsense"]
        )
        self.assertEqual(code, 2)
        self.assertIn("错误：", out)
        self.assertIn("无效选项", out)
        self.assertIn("--to", out)
        self.assertNotIn("invalid choice", out)

    def test_help_is_chinese(self):
        code, out = run_gate(["--help"])
        self.assertEqual(code, 2)
        self.assertIn("用法：", out)
        self.assertIn("命令:", out)
        self.assertIn("选项:", out)
        self.assertNotIn("usage:", out)
        self.assertNotIn("show this help message and exit", out)


if __name__ == "__main__":
    unittest.main()

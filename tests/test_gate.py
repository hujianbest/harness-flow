import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE_PATH = ROOT / "skills" / "hf-workflow" / "scripts" / "hf_gate.py"

spec = importlib.util.spec_from_file_location("hf_gate", GATE_PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def run_gate(argv):
    out = io.StringIO()
    with redirect_stdout(out):
        code = gate.main(argv)
    return code, out.getvalue()


def write_frame(feature: Path, tier=2, mode="建造", perceivable="否", extra=""):
    feature.mkdir(parents=True, exist_ok=True)
    (feature / "frame.md").write_text(
        f"# X Frame\n\n- 风险档位: {tier}\n- 模式: {mode}\n"
        f"- 用户可感知: {perceivable}\n{extra}",
        encoding="utf-8",
    )


def write_log(feature: Path, label, ts, exit_code):
    evidence = feature / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / f"{label}-{ts}.log").write_text(
        f"# hf-gate-run\n# label: {label}\noutput\n# exit: {exit_code}\n",
        encoding="utf-8",
    )


def write_review(feature: Path, name, verdict="通过", confirm="2026-07-25",
                 method="subagent"):
    reviews = feature / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / name).write_text(
        f"# 评审\n\n- 评审方式: {method}\n- 结论: {verdict}\n- 用户确认: {confirm}\n",
        encoding="utf-8",
    )


class InitAndProductTests(unittest.TestCase):
    def test_init_creates_product_layer_idempotently(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, out = run_gate(["init", "--root", str(root)])
            self.assertEqual(code, 0)
            for name in ("product.md", "decisions.md", "assumptions.md", "backlog.md"):
                self.assertTrue((root / "product" / name).is_file())
            self.assertTrue((root / "features").is_dir())

            marker = root / "product" / "product.md"
            marker.write_text("customized", encoding="utf-8")
            code, out = run_gate(["init", "--root", str(root)])
            self.assertEqual(code, 0)
            self.assertEqual(marker.read_text(encoding="utf-8"), "customized")
            self.assertIn("跳过", out)

    def test_check_product_fails_without_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_gate(["init", "--root", str(root)])
            code, out = run_gate(["check", "--product", "--root", str(root)])
            self.assertEqual(code, 1)
            self.assertIn("用户确认", out)

    def test_check_product_passes_when_confirmed_with_slices(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_gate(["init", "--root", str(root)])
            product_md = root / "product" / "product.md"
            text = product_md.read_text(encoding="utf-8").replace(
                "- 用户确认:", "- 用户确认: 2026-07-25")
            product_md.write_text(text, encoding="utf-8")
            code, out = run_gate(["check", "--product", "--root", str(root)])
            self.assertEqual(code, 0)
            self.assertIn("RESULT: PASS", out)

    def test_check_product_fails_without_product_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_gate(["check", "--product", "--root", tmp])
            self.assertEqual(code, 1)
            self.assertIn("product/ 不存在", out)


class FrameLineTests(unittest.TestCase):
    def test_check_fails_when_mode_and_perceivable_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            feature.mkdir(parents=True)
            (feature / "frame.md").write_text("- 风险档位: 2\n", encoding="utf-8")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "plan"])
            self.assertEqual(code, 1)
            self.assertIn("模式: 探索|建造", out)
            self.assertIn("用户可感知: 是|否", out)

    def test_plan_passes_with_full_frame_and_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            write_frame(feature, tier=2)
            write_log(feature, "baseline", "20260725T000000Z", 0)
            code, out = run_gate(["check", "--feature", str(feature), "--to", "plan"])
            self.assertEqual(code, 0)


class ExplorationModeTests(unittest.TestCase):
    def test_exploration_requires_tier_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-proto"
            write_frame(feature, tier=2, mode="探索")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "build"])
            self.assertEqual(code, 1)
            self.assertIn("仅限风险档位 1", out)

    def test_exploration_build_needs_no_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-proto"
            write_frame(feature, tier=1, mode="探索")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "build"])
            self.assertEqual(code, 0)

    def test_exploration_can_never_ship(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-proto"
            write_frame(feature, tier=1, mode="探索")
            write_log(feature, "smoke", "20260725T000000Z", 0)
            (feature / "conclusion.md").write_text("结论", encoding="utf-8")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 1)
            self.assertIn("永远不能 ship", out)

    def test_exploration_close_requires_runtime_evidence_and_conclusion(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-proto"
            write_frame(feature, tier=1, mode="探索")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "close"])
            self.assertEqual(code, 1)
            self.assertIn("smoke 或 demo", out)
            self.assertIn("conclusion.md", out)

            write_log(feature, "smoke", "20260725T000000Z", 0)
            (feature / "conclusion.md").write_text("学到了什么", encoding="utf-8")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "close"])
            self.assertEqual(code, 0)

    def test_close_rejected_for_build_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            write_frame(feature, tier=1, mode="建造")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "close"])
            self.assertEqual(code, 1)
            self.assertIn("close 仅用于探索模式", out)


class DemoGateTests(unittest.TestCase):
    def _shippable_feature(self, tmp, perceivable):
        feature = Path(tmp) / "features" / "001-x"
        write_frame(feature, tier=1, perceivable=perceivable)
        write_log(feature, "baseline", "20260725T000000Z", 0)
        write_log(feature, "t1-red", "20260725T000001Z", 1)
        write_log(feature, "t1-green", "20260725T000002Z", 0)
        write_log(feature, "suite", "20260725T000003Z", 0)
        write_log(feature, "smoke", "20260725T000004Z", 0)
        write_review(feature, "code-review.md")
        return feature

    def test_ship_without_demo_when_not_perceivable(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = self._shippable_feature(tmp, "否")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 0)

    def test_perceivable_ship_requires_demo_evidence_and_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = self._shippable_feature(tmp, "是")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 1)
            self.assertIn("demo", out)
            self.assertIn("demo-acceptance", out)

            (feature / "evidence" / "demo-walkthrough.png").write_bytes(b"png")
            write_review(feature, "demo-acceptance.md", verdict="接受")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 0)

    def test_demo_acceptance_verdict_must_be_accept(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = self._shippable_feature(tmp, "是")
            (feature / "evidence" / "demo-walkthrough.png").write_bytes(b"png")
            write_review(feature, "demo-acceptance.md", verdict="需调整")
            code, out = run_gate(["check", "--feature", str(feature), "--to", "ship"])
            self.assertEqual(code, 1)
            self.assertIn("需要: 接受", out)


class StatusAndNextTests(unittest.TestCase):
    def test_status_reports_product_feature_and_next_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_gate(["init", "--root", str(root)])
            feature = root / "features" / "001-skeleton"
            write_frame(feature, tier=2, perceivable="是")
            write_log(feature, "baseline", "20260725T000000Z", 0)
            code, out = run_gate(["status", "--root", str(root)])
            self.assertEqual(code, 0)
            self.assertIn("产品层: FAIL", out)
            self.assertIn("001-skeleton", out)
            self.assertIn("→ build", out)
            self.assertIn("plan.md 不存在", out)
            self.assertIn("下一步", out)

    def test_status_without_product_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_gate(["status", "--root", tmp])
            self.assertEqual(code, 0)
            self.assertIn("产品层: 无", out)

    def test_status_marks_done_feature(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feature = root / "features" / "001-x"
            write_frame(feature, tier=1, mode="探索")
            write_log(feature, "smoke", "20260725T000000Z", 0)
            (feature / "conclusion.md").write_text("结论", encoding="utf-8")
            code, out = run_gate(["status", "--root", str(root)])
            self.assertEqual(code, 0)
            self.assertIn("001-x: done", out)

    def test_next_returns_first_unchecked_slice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_gate(["init", "--root", str(root)])
            backlog = root / "product" / "backlog.md"
            backlog.write_text(
                "# 切片待办\n\n- [x] S-1 行走骨架 — 演示判据: 可启动\n"
                "- [ ] S-2 用户登录 — 演示判据: 能注册并登录\n",
                encoding="utf-8",
            )
            code, out = run_gate(["next", "--root", str(root)])
            self.assertEqual(code, 0)
            self.assertIn("S-2", out)

    def test_next_without_backlog_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_gate(["next", "--root", tmp])
            self.assertEqual(code, 1)


class RunTests(unittest.TestCase):
    def test_run_writes_evidence_log_with_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "features" / "001-x"
            feature.mkdir(parents=True)
            code, out = run_gate([
                "run", "--feature", str(feature), "--label", "smoke",
                "--", "python3", "-c", "print('ok')",
            ])
            self.assertEqual(code, 0)
            logs = list((feature / "evidence").glob("smoke-*.log"))
            self.assertEqual(len(logs), 1)
            text = logs[0].read_text(encoding="utf-8")
            self.assertIn("ok", text)
            self.assertIn("# exit: 0", text)


if __name__ == "__main__":
    unittest.main()

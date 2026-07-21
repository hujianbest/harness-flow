#!/usr/bin/env python3
"""Unit tests for the HarnessFlow evidence protocol (stdlib-only)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness


def run_cli(argv: list[str]) -> tuple[int, str]:
    buf = StringIO()
    with redirect_stdout(buf):
        try:
            code = harness.main(argv)
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
    return code, buf.getvalue()


class InitTests(unittest.TestCase):
    def test_init_creates_skeleton_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_cli(["init", "--root", tmp])
            self.assertEqual(code, 0)
            product = Path(tmp) / "product"
            for name in ("intent.md", "state.md", "decisions.md", "backlog.md"):
                self.assertTrue((product / name).is_file(), name)
            self.assertTrue((Path(tmp) / "work").is_dir())

            (product / "intent.md").write_text("precious user content", encoding="utf-8")
            code, out = run_cli(["init", "--root", tmp])
            self.assertEqual(code, 0)
            self.assertEqual((product / "intent.md").read_text(encoding="utf-8"),
                             "precious user content")
            self.assertIn("kept existing", out)


class RunTests(unittest.TestCase):
    def test_run_records_output_exit_code_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = str(Path(tmp) / "work" / "demo")
            code, out = run_cli(["run", "--work", work, "--label", "smoke",
                                 "--", "python3", "-c", "print('hello product')"])
            self.assertEqual(code, 0)
            self.assertIn("hello product", out)
            logs = list((Path(work) / "evidence").glob("smoke-*.log"))
            self.assertEqual(len(logs), 1)
            text = logs[0].read_text(encoding="utf-8")
            self.assertIn(harness.HEADER_MARK, text)
            self.assertIn("hello product", text)
            self.assertIn("exit_code: 0", text)
            self.assertRegex(text, r"sha256: [0-9a-f]{64}\n\Z")

    def test_run_passes_through_nonzero_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = str(Path(tmp) / "work" / "demo")
            code, _ = run_cli(["run", "--work", work, "--label", "failing-signal",
                               "--", "python3", "-c", "raise SystemExit(3)"])
            self.assertEqual(code, 3)
            text = next((Path(work) / "evidence").glob("failing-signal-*.log")).read_text(
                encoding="utf-8")
            self.assertIn("exit_code: 3", text)

    def test_run_missing_command_records_exit_127(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = str(Path(tmp) / "work" / "demo")
            code, _ = run_cli(["run", "--work", work, "--label", "nope",
                               "--", "definitely-not-a-command-xyz"])
            self.assertEqual(code, 127)
            text = next((Path(work) / "evidence").glob("nope-*.log")).read_text(
                encoding="utf-8")
            self.assertIn("exit_code: 127", text)

    def test_run_rejects_empty_label_and_sanitizes_odd_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = str(Path(tmp) / "work" / "demo")
            code, _ = run_cli(["run", "--work", work, "--label", "///",
                               "--", "true"])
            self.assertNotEqual(code, 0)
            code, _ = run_cli(["run", "--work", work, "--label", "perf: p99 <5ms",
                               "--", "true"])
            self.assertEqual(code, 0)
            self.assertTrue(list((Path(work) / "evidence").glob("perf-p99-5ms-*.log")))


class CheckTests(unittest.TestCase):
    def _make_log(self, tmp: str) -> Path:
        work = str(Path(tmp) / "work" / "demo")
        run_cli(["run", "--work", work, "--label", "suite", "--", "true"])
        return next((Path(work) / "evidence").glob("suite-*.log"))

    def test_check_passes_on_intact_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_log(tmp)
            code, out = run_cli(["check", "--work", str(Path(tmp) / "work" / "demo")])
            self.assertEqual(code, 0)
            self.assertIn("RESULT: PASS", out)

    def test_check_detects_hand_edited_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = self._make_log(tmp)
            log.write_text(log.read_text(encoding="utf-8").replace(
                "exit_code: 0", "exit_code: 1"), encoding="utf-8")
            code, out = run_cli(["check", "--work", str(Path(tmp) / "work" / "demo")])
            self.assertEqual(code, 1)
            self.assertIn("TAMPERED", out)
            self.assertIn("RESULT: FAIL", out)

    def test_check_detects_fully_handwritten_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "work" / "demo" / "evidence"
            evidence.mkdir(parents=True)
            (evidence / "fake-20260101T000000Z.log").write_text(
                "all tests green, trust me\n", encoding="utf-8")
            code, out = run_cli(["check", "--work", str(Path(tmp) / "work" / "demo")])
            self.assertEqual(code, 1)
            self.assertIn("missing header", out)

    def test_check_reports_empty_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_cli(["check", "--work", str(Path(tmp) / "work" / "demo")])
            self.assertEqual(code, 1)
            self.assertIn("RESULT: EMPTY", out)


if __name__ == "__main__":
    unittest.main()

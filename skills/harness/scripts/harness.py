#!/usr/bin/env python3
"""HarnessFlow evidence protocol (stdlib-only).

Three subcommands, none of which adjudicates process:

  init   -- create the product truth skeleton (product/*.md), never overwriting
  run    -- execute a command and write its raw output as tamper-evident
            evidence into work/<slug>/evidence/; the command's exit code is
            passed through
  check  -- verify the integrity of every evidence log in a work line
            (recomputed hash must match the recorded one) and list them

Evidence logs are the only legitimate backing for any "it works / tests pass"
claim. Creating or editing them by hand is fabrication; `check` exists to make
careless fabrication visible.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HEADER_MARK = "=== harness evidence ==="
OUTPUT_MARK = "--- output ---"
RESULT_MARK = "--- result ---"

INIT_FILES = {
    "intent.md": (
        "# 产品意图\n\n"
        "<!-- 用户主权文件：为谁、解决什么问题、成功标志、明确不做什么。 -->\n"
        "<!-- 实质修改此文件需经用户的意图检查点。 -->\n"
    ),
    "state.md": (
        "# 产品现状\n\n"
        "<!-- 产品当前能做什么、如何运行。 -->\n\n"
        "## 验证入口\n\n"
        "<!-- 可直接执行的命令，任何时刻在主线上必须真实可跑（不变量 4）。 -->\n\n"
        "## 已知问题\n"
    ),
    "decisions.md": (
        "# 决策日志\n\n"
        "<!-- 追加式：日期、决策、理由、可逆性。不要改写历史条目。 -->\n"
    ),
    "backlog.md": (
        "# 候选工作与未决问题\n"
    ),
}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ts_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _git_describe(cwd: Path) -> str:
    try:
        rev = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=10,
        )
        if rev.returncode != 0:
            inside = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=cwd, capture_output=True, text=True, timeout=10,
            )
            if inside.returncode == 0 and inside.stdout.strip() == "true":
                return "(no commits yet)"
            return "(not a git repo)"
        commit = rev.stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd, capture_output=True, text=True, timeout=10,
        )
        suffix = " (dirty)" if dirty.stdout.strip() else ""
        return commit + suffix
    except (OSError, subprocess.TimeoutExpired):
        return "(git unavailable)"


def _sanitize_label(label: str) -> str:
    clean = re.sub(r"[^\w.-]+", "-", label).strip("-")
    if not clean:
        raise SystemExit("error: label must contain at least one word character")
    return clean


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root)
    product = root / "product"
    product.mkdir(parents=True, exist_ok=True)
    created, kept = [], []
    for name, stub in INIT_FILES.items():
        path = product / name
        if path.exists():
            kept.append(name)
        else:
            path.write_text(stub, encoding="utf-8")
            created.append(name)
    (root / "work").mkdir(exist_ok=True)
    print(f"product/ ready: created {created or '[]'}, kept existing {kept or '[]'}")
    print("next: fill product/intent.md and take it through the intent checkpoint")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    if not args.cmd:
        raise SystemExit("error: no command given after --")
    label = _sanitize_label(args.label)
    evidence_dir = Path(args.work) / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    log_path = evidence_dir / f"{label}-{_ts_compact()}.log"

    cwd = Path.cwd()
    started = _now()
    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            args.cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        output = proc.stdout.decode("utf-8", errors="replace")
        exit_code = proc.returncode
    except FileNotFoundError as exc:
        output = f"harness: command not found: {exc}\n"
        exit_code = 127
    duration = time.monotonic() - t0

    body = (
        f"{HEADER_MARK}\n"
        f"label: {label}\n"
        f"command: {subprocess.list2cmdline(args.cmd)}\n"
        f"cwd: {cwd}\n"
        f"git: {_git_describe(cwd)}\n"
        f"started: {started}\n"
        f"{OUTPUT_MARK}\n"
        f"{output}"
        f"{'' if output.endswith(chr(10)) or not output else chr(10)}"
        f"{RESULT_MARK}\n"
        f"exit_code: {exit_code}\n"
        f"ended: {_now()}\n"
        f"duration_s: {duration:.2f}\n"
    )
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    log_path.write_text(body + f"sha256: {digest}\n", encoding="utf-8")

    sys.stdout.write(output)
    print(f"\n[harness] evidence written: {log_path} (exit_code={exit_code})")
    return exit_code


def verify_log(path: Path) -> tuple[bool, str]:
    """Return (ok, summary). A log is ok iff its recorded sha256 matches."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return False, f"unreadable: {exc}"
    if not text.startswith(HEADER_MARK):
        return False, "malformed: missing header"
    lines = text.splitlines(keepends=True)
    if not lines or not lines[-1].startswith("sha256: "):
        return False, "malformed: missing sha256 footer"
    recorded = lines[-1][len("sha256: "):].strip()
    body = "".join(lines[:-1])
    actual = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if actual != recorded:
        return False, "TAMPERED: content hash mismatch"
    exit_m = re.search(r"^exit_code: (-?\d+)$", text, re.MULTILINE)
    started_m = re.search(r"^started: (\S+)$", text, re.MULTILINE)
    label_m = re.search(r"^label: (.+)$", text, re.MULTILINE)
    return True, (
        f"label={label_m.group(1) if label_m else '?'} "
        f"exit_code={exit_m.group(1) if exit_m else '?'} "
        f"started={started_m.group(1) if started_m else '?'}"
    )


def cmd_check(args: argparse.Namespace) -> int:
    evidence_dir = Path(args.work) / "evidence"
    logs = sorted(evidence_dir.glob("*.log")) if evidence_dir.is_dir() else []
    if not logs:
        print(f"RESULT: EMPTY — no evidence logs under {evidence_dir}")
        return 1
    bad = 0
    for log in logs:
        ok, summary = verify_log(log)
        print(f"  {'ok  ' if ok else 'FAIL'} {log.name}: {summary}")
        bad += 0 if ok else 1
    if bad:
        print(f"RESULT: FAIL — {bad}/{len(logs)} log(s) invalid or tampered")
        return 1
    print(f"RESULT: PASS — {len(logs)} evidence log(s) intact")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="harness.py", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create the product truth skeleton")
    p_init.add_argument("--root", default=".", help="project root (default: .)")
    p_init.set_defaults(func=cmd_init)

    p_run = sub.add_parser("run", help="run a command and record evidence")
    p_run.add_argument("--work", required=True, help="work line dir, e.g. work/rate-limit")
    p_run.add_argument("--label", required=True, help="short human-readable label")
    p_run.add_argument("cmd", nargs=argparse.REMAINDER,
                       help="-- followed by the command to run")
    p_run.set_defaults(func=cmd_run)

    p_check = sub.add_parser("check", help="verify evidence integrity")
    p_check.add_argument("--work", required=True)
    p_check.set_defaults(func=cmd_check)

    args = parser.parse_args(argv)
    if getattr(args, "cmd", None) and args.cmd[0] == "--":
        args.cmd = args.cmd[1:]
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

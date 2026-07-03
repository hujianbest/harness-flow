#!/usr/bin/env python3
"""hf_gate.py — HarnessFlow 机械门禁（stdlib only）。

两个子命令:

  run   包装执行一条命令，把原始输出连同命令、时间戳、退出码写入
        features/<id>/evidence/<label>-<UTC时间戳>.log，并向调用方透传退出码。
        这是工作流中所有测试/构建/冒烟证据的唯一合法产生方式。

            python3 skills/hf-workflow/scripts/hf_gate.py run \
                --feature features/012-x --label t3-green -- pytest tests/

  check 机械校验能否进入目标阶段，只依据磁盘上的工件与证据日志，
        不采信任何叙述性文本。PASS 退出码 0，FAIL 退出码 1，用法错误 2。

            python3 skills/hf-workflow/scripts/hf_gate.py check \
                --feature features/012-x --to build

校验规则（按目标阶段）:

  --to plan    frame.md 含风险档位(须 ≥2) + baseline 证据日志存在
  --to design  仅档位 3：spec.md 存在 + spec-review 通过且已确认
  --to build   档位 1：frame + baseline；
               档位 2：plan.md 含任务清单 + plan-review 通过且已确认；
               档位 3：spec/design 齐备 + 两轮评审均通过且已确认
  --to verify  build 前提 + 任务清单全部勾选 + 每个任务有 red(exit!=0)
               与 green(最新一份 exit==0) 证据日志
  --to ship    verify 前提 + code-review 通过且已确认 + suite 日志
               (exit==0 且不早于最新 green) + smoke 冒烟证据

评审记录的机器可读行: `- 结论: 通过|需修改|待独立复核`、`- 用户确认: <值>`、
`- 评审方式: subagent|独立会话|主会话降级`。评审方式为"主会话降级"时，
用户确认不得是 auto-approved（降级评审禁止自我确认）。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

LABEL_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
LOG_NAME_RE = re.compile(r"^(?P<label>[a-z0-9-]+)-(?P<ts>\d{8}T\d{6}Z)(?:-\d+)?\.log$")
TIER_RE = re.compile(r"^-\s*风险档位:\s*([123])\b", re.MULTILINE)
TASK_RE = re.compile(r"^- \[([ xX])\]\s*(T-\d+)\b", re.MULTILINE)
EXIT_RE = re.compile(r"^# exit: (\d+)\s*$", re.MULTILINE)

TARGETS = ("plan", "design", "build", "verify", "ship")


# ---------------------------------------------------------------- run

def cmd_run(feature: Path, label: str, command: list[str], cwd: str | None) -> int:
    if not LABEL_RE.match(label):
        print(f"错误: label 必须匹配 [a-z0-9][a-z0-9-]* ，得到: {label!r}")
        return 2
    if not command:
        print("错误: 缺少要执行的命令（用 -- 分隔）")
        return 2

    evidence = feature / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = evidence / f"{label}-{ts}.log"
    n = 2
    while path.exists():
        path = evidence / f"{label}-{ts}-{n}.log"
        n += 1

    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        proc = subprocess.run(
            command, cwd=cwd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True,
        )
        output, exit_code = proc.stdout or "", proc.returncode
    except FileNotFoundError as e:
        output, exit_code = f"hf-gate: 命令无法启动: {e}\n", 127

    if output and not output.endswith("\n"):
        output += "\n"
    path.write_text(
        "# hf-gate-run\n"
        f"# label: {label}\n"
        f"# command: {' '.join(command)}\n"
        f"# started: {started}\n"
        f"{output}"
        f"# exit: {exit_code}\n",
        encoding="utf-8",
    )
    sys.stdout.write(output)
    print(f"[hf-gate] 证据已落盘: {path} (exit {exit_code})")
    return exit_code


# ---------------------------------------------------------------- 解析工件

def log_exit(path: Path) -> int | None:
    matches = EXIT_RE.findall(path.read_text(encoding="utf-8"))
    return int(matches[-1]) if matches else None


def evidence_logs(feature: Path, label_prefix: str) -> list[tuple[str, Path, int | None]]:
    """返回按时间戳升序的 (ts, path, exit) 列表，label 前缀匹配。"""
    evidence = feature / "evidence"
    out = []
    if evidence.is_dir():
        for p in evidence.iterdir():
            m = LOG_NAME_RE.match(p.name)
            if m and m.group("label").startswith(label_prefix):
                out.append((m.group("ts"), p, log_exit(p)))
    return sorted(out, key=lambda t: t[0])


def read_tier(feature: Path) -> int | None:
    frame = feature / "frame.md"
    if not frame.is_file():
        return None
    m = TIER_RE.search(frame.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


def read_review(feature: Path, name: str) -> dict | None:
    path = feature / "reviews" / name
    if not path.is_file():
        return None
    verdict = method = None
    verdict_idx = -1
    confirm = None
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("- 结论:"):
            verdict, verdict_idx, confirm = s.split(":", 1)[1].strip(), i, None
        elif s.startswith("- 评审方式:"):
            method = s.split(":", 1)[1].strip()
        elif s.startswith("- 用户确认:") and i > verdict_idx:
            confirm = s.split(":", 1)[1].strip()
    return {"verdict": verdict, "method": method, "confirm": confirm}


def read_tasks(feature: Path, doc: str) -> list[tuple[str, bool]] | None:
    path = feature / doc
    if not path.is_file():
        return None
    return [(tid, mark.lower() == "x")
            for mark, tid in TASK_RE.findall(path.read_text(encoding="utf-8"))]


# ---------------------------------------------------------------- check 各项

class Checker:
    def __init__(self, feature: Path):
        self.feature = feature
        self.failures: list[str] = []
        self.oks: list[str] = []

    def ok(self, msg: str) -> None:
        self.oks.append(msg)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    # -- 基础件

    def check_frame(self) -> int | None:
        tier = read_tier(self.feature)
        if not (self.feature / "frame.md").is_file():
            self.fail("frame.md 不存在 — 先完成 frame 阶段")
        elif tier is None:
            self.fail("frame.md 缺少机器可读的 `- 风险档位: 1|2|3` 行")
        else:
            self.ok(f"frame.md 风险档位: {tier}")
        return tier

    def check_baseline(self) -> None:
        logs = evidence_logs(self.feature, "baseline")
        if not logs:
            self.fail("缺环境基线证据: evidence/baseline-*.log（用 hf_gate.py run --label baseline 产生）")
        else:
            ts, path, code = logs[-1]
            self.ok(f"baseline 证据: {path.name} (exit {code})")

    def check_doc(self, doc: str) -> None:
        path = self.feature / doc
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            self.fail(f"{doc} 不存在或为空")
        else:
            self.ok(f"{doc} 存在")

    def check_review(self, name: str) -> None:
        review = read_review(self.feature, name)
        stem = name.removesuffix(".md")
        if review is None:
            self.fail(f"评审记录不存在: reviews/{name}（{stem} 未进行）")
            return
        if review["verdict"] != "通过":
            self.fail(f"{stem} 最新结论为 {review['verdict'] or '缺失'}，需要: 通过")
            return
        if not review["confirm"]:
            self.fail(f"{stem} 结论后缺 `- 用户确认:` 行（确认未落盘）")
            return
        if review["method"] == "主会话降级" and review["confirm"].startswith("auto-approved"):
            self.fail(f"{stem} 评审方式为主会话降级，禁止 auto-approved 自我确认，需用户真实确认")
            return
        self.ok(f"{stem}: 通过，已确认 ({review['confirm']})")

    # -- 任务与证据

    def task_doc_for(self, tier: int) -> str:
        return "plan.md" if tier == 2 else "design.md"

    def check_task_list_exists(self, tier: int) -> None:
        doc = self.task_doc_for(tier)
        tasks = read_tasks(self.feature, doc)
        if tasks is None:
            self.fail(f"{doc} 不存在")
        elif not tasks:
            self.fail(f"{doc} 没有可解析的任务行（格式: `- [ ] T-1 ...`）")
        else:
            self.ok(f"{doc} 任务清单: {len(tasks)} 项")

    def task_ids(self, tier: int) -> list[tuple[str, bool]]:
        if tier == 1:
            # tier-1 无计划文档，从证据日志推断任务 ID
            ids = sorted({m.group(1) for _, p, _ in evidence_logs(self.feature, "t")
                          for m in [re.match(r"^t(\d+)-(?:red|green)-", p.name)] if m})
            if not ids:
                self.fail("tier-1 至少需要一对 t<N>-red / t<N>-green 证据日志")
            return [(f"T-{i}", True) for i in ids]
        return read_tasks(self.feature, self.task_doc_for(tier)) or []

    def check_tasks_done(self, tasks: list[tuple[str, bool]]) -> None:
        undone = [tid for tid, done in tasks if not done]
        if undone:
            self.fail(f"任务未全部完成，未勾选: {', '.join(undone)}")
        elif tasks:
            self.ok(f"任务清单全部勾选 ({len(tasks)} 项)")

    def check_red_green(self, tasks: list[tuple[str, bool]]) -> None:
        for tid, _ in tasks:
            n = tid.split("-")[1]
            reds = evidence_logs(self.feature, f"t{n}-red")
            greens = evidence_logs(self.feature, f"t{n}-green")
            if not reds:
                self.fail(f"{tid} 缺 red 证据: evidence/t{n}-red-*.log（失败先行的测试运行）")
            elif not any(code not in (0, None) for _, _, code in reds):
                self.fail(f"{tid} 的 red 证据 exit 均为 0 — 测试从未失败过，不构成有效 RED")
            if not greens:
                self.fail(f"{tid} 缺 green 证据: evidence/t{n}-green-*.log")
            elif greens[-1][2] != 0:
                self.fail(f"{tid} 最新 green 证据 exit={greens[-1][2]}，不是通过状态")
            if reds and greens and greens[-1][2] == 0 and any(c not in (0, None) for _, _, c in reds):
                self.ok(f"{tid} red→green 证据齐备")

    def check_suite_and_smoke(self) -> None:
        greens = evidence_logs(self.feature, "t")
        green_ts = [ts for ts, p, _ in greens if re.match(r"^t\d+-green-", p.name)]
        suites = evidence_logs(self.feature, "suite")
        if not suites:
            self.fail("缺全量测试证据: evidence/suite-*.log")
        else:
            ts, path, code = suites[-1]
            if code != 0:
                self.fail(f"最新 suite 日志 exit={code}，全量测试未通过")
            elif green_ts and ts < max(green_ts):
                self.fail("最新 suite 日志早于最新 green 证据 — 最后一次改动后未重跑全量测试")
            else:
                self.ok(f"suite 证据: {path.name} (exit 0)")

        evidence = self.feature / "evidence"
        smoke = sorted(evidence.glob("smoke-*")) if evidence.is_dir() else []
        smoke_logs = evidence_logs(self.feature, "smoke")
        non_log = [p for p in smoke if not p.name.endswith(".log")]
        if not smoke:
            self.fail("缺运行时冒烟证据: evidence/smoke-*（真实运行的日志或截图）")
        elif non_log:
            self.ok(f"smoke 证据: {', '.join(p.name for p in non_log)}")
        elif smoke_logs and smoke_logs[-1][2] == 0:
            self.ok(f"smoke 证据: {smoke_logs[-1][1].name} (exit 0)")
        else:
            self.fail("smoke 日志最新一份 exit 非 0，冒烟未通过")


def check_target(feature: Path, target: str) -> tuple[Checker, int | None]:
    c = Checker(feature)
    tier = c.check_frame()
    c.check_baseline()
    if tier is None:
        return c, tier

    if target == "plan":
        if tier < 2:
            c.fail("风险档位 1 不经 plan 阶段 — 直接 `check --to build`")
    elif target == "design":
        if tier != 3:
            c.fail(f"档位 {tier} 无独立 design 阶段（仅档位 3 拆分 spec/design）")
        else:
            c.check_doc("spec.md")
            c.check_review("spec-review.md")
    elif target in ("build", "verify", "ship"):
        if tier == 2:
            c.check_task_list_exists(2)
            c.check_review("plan-review.md")
        elif tier == 3:
            c.check_doc("spec.md")
            c.check_task_list_exists(3)
            c.check_review("spec-review.md")
            c.check_review("design-review.md")
        if target in ("verify", "ship"):
            tasks = c.task_ids(tier)
            if tier >= 2:
                c.check_tasks_done(tasks)
            c.check_red_green(tasks)
        if target == "ship":
            c.check_review("code-review.md")
            c.check_suite_and_smoke()
    return c, tier


def cmd_check(feature: Path, target: str) -> int:
    print(f"== hf-gate check --to {target} ({feature})")
    if not feature.is_dir():
        print(f"FAIL 特性目录不存在: {feature}")
        print("RESULT: FAIL")
        return 1
    c, _ = check_target(feature, target)
    for msg in c.oks:
        print(f"OK   {msg}")
    for msg in c.failures:
        print(f"FAIL {msg}")
    if c.failures:
        print(f"RESULT: FAIL ({len(c.failures)} 项未通过) — 不得进入 {target}")
        return 1
    print(f"RESULT: PASS — 可进入 {target}")
    return 0


# ---------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    if argv and argv[0] == "run" and "--" in argv:
        split = argv.index("--")
        head, command = argv[:split], argv[split + 1:]
    else:
        head, command = argv, []

    parser = argparse.ArgumentParser(prog="hf_gate.py", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="执行命令并把原始输出落盘为证据日志")
    p_run.add_argument("--feature", required=True, help="特性目录，如 features/012-x")
    p_run.add_argument("--label", required=True, help="证据标签，如 baseline / t3-red / suite / smoke")
    p_run.add_argument("--cwd", default=None, help="命令工作目录（默认当前目录）")

    p_check = sub.add_parser("check", help="机械校验能否进入目标阶段")
    p_check.add_argument("--feature", required=True)
    p_check.add_argument("--to", required=True, choices=TARGETS, dest="target")

    try:
        args = parser.parse_args(head)
    except SystemExit as e:
        return int(e.code or 2)

    if args.cmd == "run":
        return cmd_run(Path(args.feature), args.label, command, args.cwd)
    return cmd_check(Path(args.feature), args.target)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

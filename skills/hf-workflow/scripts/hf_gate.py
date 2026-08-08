#!/usr/bin/env python3
"""hf_gate.py — HarnessFlow 机械门禁与状态机（仅使用标准库）。

主链: grill-with-docs → to-spec → to-architecture → to-tickets → implement → ship
(探索: … → implement → close, 永不 ship)

子命令:
  init / check / status / next
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MODE_RE = re.compile(r"^-[ \t]*模式:[ \t]*(探索|建造)\b", re.MULTILINE)
PERCEIVABLE_RE = re.compile(r"^-[ \t]*用户可感知:[ \t]*(是|否)\b", re.MULTILINE)
TICKET_RE = re.compile(r"^- \[([ xX])\][ \t]*(T-\d+)\b", re.MULTILINE)
CONFIRM_RE = re.compile(r"^-[ \t]*用户确认:[ \t]*(\S.*)$", re.MULTILINE)

TARGETS = (
    "to-spec",
    "to-architecture",
    "to-tickets",
    "implement",
    "ship",
    "close",
)

PRODUCT_FILES = {
    "assumptions.md": """# 假设台账

智能体替用户做的默认选择。标准动作: 提出带默认值的选项 → 记录 → 继续。
状态: 生效 | 已确认 | 已推翻
格式: `- A-<n> <日期> [状态] <假设内容> — 默认理由: <一句话>`
""",
    "decisions.md": """# 决策记录

已确认决策(用户确认或从假设台账迁入)。只追加。
格式: `- D-<n> <日期> <决策内容> — 依据: <一句话>`
""",
}

CONTEXT_TEMPLATE = """# CONTEXT

项目领域共享语言（术语表）。由 hf-grill-with-docs / hf-domain-modeling 维护。

- 用户确认:

## 术语

<!-- 术语 — 定义 -->
"""


def localize_argparse_error(message: str) -> str:
    """把 argparse 可能产生的用户可见错误转换为简体中文。"""
    replacements = (
        (
            r"^argument (.+?): invalid choice: (.+?) \(choose from (.+)\)$",
            r"参数 \1：无效选项：\2（可选值：\3）",
        ),
        (
            r"^the following arguments are required: (.+)$",
            r"缺少必需参数：\1",
        ),
        (
            r"^unrecognized arguments: (.+)$",
            r"无法识别的参数：\1",
        ),
        (
            r"^argument (.+?): expected one argument$",
            r"参数 \1：需要一个值",
        ),
        (
            r"^argument (.+?): ignored explicit argument (.+)$",
            r"参数 \1：不能显式指定值 \2",
        ),
        (
            r"^argument (.+?): not allowed with argument (.+)$",
            r"参数 \1：不能与参数 \2 同时使用",
        ),
        (
            r"^one of the arguments (.+) is required$",
            r"必须提供以下参数之一：\1",
        ),
        (
            r"^ambiguous option: (.+?) could match (.+)$",
            r"选项 \1 有歧义，可能是：\2",
        ),
    )
    for pattern, replacement in replacements:
        localized, count = re.subn(pattern, replacement, message)
        if count:
            return localized
    return "参数解析失败，请检查命令格式"


class ChineseArgumentParser(argparse.ArgumentParser):
    """输出简体中文帮助和错误，同时保持 argparse 的解析行为。"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("add_help", False)
        super().__init__(*args, **kwargs)
        self._positionals.title = "位置参数"
        self._optionals.title = "选项"
        self.add_argument("-h", "--help", action="help", help="显示此帮助信息并退出")

    def format_usage(self) -> str:
        return super().format_usage().replace("usage: ", "用法：", 1)

    def format_help(self) -> str:
        return super().format_help().replace("usage: ", "用法：", 1)

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: 错误：{localize_argparse_error(message)}\n")


def read_feature_field(feature: Path, pattern: re.Pattern) -> str | None:
    for name in ("feature.md", "frame.md"):
        path = feature / name
        if path.is_file():
            m = pattern.search(path.read_text(encoding="utf-8"))
            if m:
                return m.group(1)
    return None


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


def read_tickets(feature: Path) -> list[tuple[str, bool]] | None:
    path = feature / "tickets.md"
    if not path.is_file():
        return None
    return [
        (tid, mark.lower() == "x")
        for mark, tid in TICKET_RE.findall(path.read_text(encoding="utf-8"))
    ]


class Checker:
    def __init__(self, feature: Path):
        self.feature = feature
        self.failures: list[str] = []
        self.oks: list[str] = []

    def ok(self, msg: str) -> None:
        self.oks.append(msg)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def check_feature_meta(self) -> tuple[str | None, str | None]:
        if not (self.feature / "feature.md").is_file() and not (self.feature / "frame.md").is_file():
            self.fail("feature.md 不存在 — 先在 hf-grill-with-docs 创建特性元数据")
            return None, None
        mode = read_feature_field(self.feature, MODE_RE)
        perceivable = read_feature_field(self.feature, PERCEIVABLE_RE)
        if mode is None:
            self.fail("feature.md 缺少机器可读的 `- 模式: 探索|建造` 行")
        else:
            self.ok(f"模式: {mode}")
        if perceivable is None:
            self.fail("feature.md 缺少机器可读的 `- 用户可感知: 是|否` 行")
        else:
            self.ok(f"用户可感知: {perceivable}")
        return mode, perceivable

    def check_doc(self, doc: str) -> None:
        path = self.feature / doc
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            self.fail(f"{doc} 不存在或为空")
        else:
            self.ok(f"{doc} 存在")

    def check_review(self, name: str, expected: str = "通过") -> None:
        review = read_review(self.feature, name)
        stem = name.removesuffix(".md")
        if review is None:
            self.fail(f"评审记录不存在: reviews/{name}（{stem} 未进行）")
            return
        if review["verdict"] != expected:
            self.fail(f"{stem} 最新结论为 {review['verdict'] or '缺失'}，需要: {expected}")
            return
        if not review["confirm"]:
            self.fail(f"{stem} 结论后缺 `- 用户确认:` 行（确认未落盘）")
            return
        if review["method"] == "主会话降级" and review["confirm"].startswith("auto-approved"):
            self.fail(f"{stem} 评审方式为主会话降级，禁止 auto-approved 自我确认")
            return
        self.ok(f"{stem}: {expected}，已确认 ({review['confirm']})")

    def check_tickets_exist(self) -> list[tuple[str, bool]] | None:
        tickets = read_tickets(self.feature)
        if tickets is None:
            self.fail("tickets.md 不存在")
            return None
        if not tickets:
            self.fail("tickets.md 没有可解析的票行（格式: `- [ ] T-01 ...`）")
            return []
        self.ok(f"tickets.md: {len(tickets)} 张票")
        return tickets

    def check_tickets_done(self, tickets: list[tuple[str, bool]]) -> None:
        undone = [tid for tid, done in tickets if not done]
        if undone:
            self.fail(f"票未全部完成，未勾选: {', '.join(undone)}")
        elif tickets:
            self.ok(f"票全部勾选 ({len(tickets)} 张)")


def check_target(feature: Path, target: str) -> Checker:
    c = Checker(feature)
    mode, perceivable = c.check_feature_meta()
    if mode is None:
        return c

    if mode == "探索":
        if target in ("to-spec", "to-architecture", "to-tickets"):
            c.fail(f"探索模式不经 {target} — 链路为特性 → implement/prototype → close")
        elif target == "ship":
            c.fail("探索模式永远不能 ship — 写 conclusion.md 后 `check --to close`")
        elif target == "implement":
            c.ok("探索模式可进入 implement/prototype")
        elif target == "close":
            c.check_doc("conclusion.md")
        return c

    if target == "close":
        c.fail("close 仅用于探索模式 — 建造模式走 implement → ship")
        return c

    if target == "to-spec":
        return c

    if target == "to-architecture":
        c.check_doc("spec.md")
        c.check_review("spec-review.md")
        return c

    if target == "to-tickets":
        c.check_doc("spec.md")
        c.check_review("spec-review.md")
        c.check_doc("architecture.md")
        c.check_review("architecture-review.md")
        return c

    if target == "implement":
        c.check_doc("spec.md")
        c.check_review("spec-review.md")
        c.check_doc("architecture.md")
        c.check_review("architecture-review.md")
        c.check_tickets_exist()
        return c

    if target == "ship":
        c.check_doc("spec.md")
        c.check_review("spec-review.md")
        c.check_doc("architecture.md")
        c.check_review("architecture-review.md")
        tickets = c.check_tickets_exist()
        if tickets:
            c.check_tickets_done(tickets)
        c.check_review("code-review.md")
        if perceivable == "是":
            c.check_review("demo-acceptance.md", expected="接受")
        return c

    return c


def cmd_check(feature: Path, target: str) -> int:
    print(f"== hf-gate check --to {target} ({feature})")
    if not feature.is_dir():
        print(f"FAIL 特性目录不存在: {feature}")
        print("RESULT: FAIL")
        return 1
    c = check_target(feature, target)
    for msg in c.oks:
        print(f"OK   {msg}")
    for msg in c.failures:
        print(f"FAIL {msg}")
    if c.failures:
        print(f"RESULT: FAIL ({len(c.failures)} 项未通过) — 不得进入 {target}")
        return 1
    print(f"RESULT: PASS — 可进入 {target}")
    return 0


def check_confirm(path: Path, oks: list[str], failures: list[str], fail_msg: str) -> None:
    if not path.is_file():
        return
    m = CONFIRM_RE.search(path.read_text(encoding="utf-8"))
    if not m or m.group(1).startswith("<"):
        failures.append(fail_msg)
    else:
        oks.append(f"{path.name} 用户确认: {m.group(1)}")


def check_product_layer(root: Path) -> tuple[list[str], list[str]]:
    oks: list[str] = []
    failures: list[str] = []
    product = root / "product"
    if not product.is_dir():
        failures.append("product/ 不存在 — 先运行 `hf_gate.py init` 并按 hf-grill-with-docs")
        return oks, failures
    for name in PRODUCT_FILES:
        path = product / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"product/{name} 不存在或为空")
        else:
            oks.append(f"product/{name} 存在")
    ctx = root / "CONTEXT.md"
    if not ctx.is_file() or not ctx.read_text(encoding="utf-8").strip():
        failures.append("CONTEXT.md 不存在或为空 — hf-grill-with-docs 产出")
    else:
        oks.append("CONTEXT.md 存在")
        check_confirm(
            ctx, oks, failures,
            "CONTEXT.md 缺有效的 `- 用户确认:` 行 — 未经确认不得开始特性主链",
        )
    return oks, failures


def cmd_check_product(root: Path) -> int:
    print(f"== hf-gate check --product ({root})")
    oks, failures = check_product_layer(root)
    for msg in oks:
        print(f"OK   {msg}")
    for msg in failures:
        print(f"FAIL {msg}")
    if failures:
        print(f"RESULT: FAIL ({len(failures)} 项未通过) — 产品层未就绪")
        return 1
    print("RESULT: PASS — 产品层就绪")
    return 0


def cmd_init(root: Path) -> int:
    product = root / "product"
    product.mkdir(parents=True, exist_ok=True)
    for name, template in PRODUCT_FILES.items():
        path = product / name
        if path.exists():
            print(f"[hf-gate] 跳过（已存在）: {path}")
        else:
            path.write_text(template, encoding="utf-8")
            print(f"[hf-gate] 已创建: {path}")
    ctx = root / "CONTEXT.md"
    if ctx.exists():
        print(f"[hf-gate] 跳过（已存在）: {ctx}")
    else:
        ctx.write_text(CONTEXT_TEMPLATE, encoding="utf-8")
        print(f"[hf-gate] 已创建: {ctx}")
    adr = root / "docs" / "adr"
    if not adr.is_dir():
        adr.mkdir(parents=True)
        print(f"[hf-gate] 已创建: {adr}/")
    features = root / "features"
    if not features.is_dir():
        features.mkdir(parents=True)
        print(f"[hf-gate] 已创建: {features}/")
    print("[hf-gate] 初始化完成 — 按 hf-grill-with-docs 对齐后 check --product")
    return 0


def stage_sequence(mode: str) -> list[str]:
    if mode == "探索":
        return ["implement", "close"]
    return ["to-spec", "to-architecture", "to-tickets", "implement", "ship"]


def probe_feature(feature: Path) -> tuple[str, list[str]]:
    mode = read_feature_field(feature, MODE_RE)
    if mode is None:
        c = check_target(feature, "to-spec")
        return "grill-with-docs", c.failures
    for target in stage_sequence(mode):
        c = check_target(feature, target)
        if c.failures:
            return target, c.failures
    return "done", []


def cmd_status(root: Path) -> int:
    print(f"== hf-gate status ({root.resolve()})")

    product_ready = None
    product_dir = root / "product"
    if product_dir.is_dir() or (root / "CONTEXT.md").is_file():
        _, failures = check_product_layer(root)
        product_ready = not failures
        if product_ready:
            print("产品层: PASS（就绪）")
        else:
            print(f"产品层: FAIL（{len(failures)} 项未通过）")
            for msg in failures:
                print(f"  - {msg}")
    else:
        print("产品层: 无（存量可直接开特性;绿地先 init + hf-grill-with-docs）")

    features_dir = root / "features"
    feature_dirs = (
        sorted(p for p in features_dir.iterdir() if p.is_dir() and re.match(r"^\d{3}-", p.name))
        if features_dir.is_dir()
        else []
    )
    active: tuple[Path, str, list[str]] | None = None
    if not feature_dirs:
        print("特性: 无")
    for f in feature_dirs:
        stage, failures = probe_feature(f)
        mode = read_feature_field(f, MODE_RE) or "?"
        if stage == "done":
            print(f"特性 {f.name}: done（已完成，{mode}）")
        else:
            print(f"特性 {f.name}: 当前卡在 → {stage}（{mode}）")
            for msg in failures[:3]:
                print(f"  - {msg}")
            if len(failures) > 3:
                print(f"  - …另有 {len(failures) - 3} 项")
            if active is None:
                active = (f, stage, failures)

    if active:
        f, stage, _ = active
        print(f"下一步: 推进 {f.name} 通过 `check --to {stage}`")
    elif product_ready:
        print("下一步: 开新特性目录或从任务跟踪器取票 → hf-to-spec / hf-implement")
    elif product_ready is False:
        print("下一步: 补齐 CONTEXT/台账（hf-grill-with-docs），`check --product` PASS")
    else:
        print("下一步: 新特性从 hf-workflow 进入;绿地 `init` + hf-grill-with-docs")
    return 0


def cmd_next(root: Path) -> int:
    """取第一个未 done 的特性及其当前阶段。"""
    features_dir = root / "features"
    if not features_dir.is_dir():
        print("features/ 不存在")
        return 1
    for f in sorted(p for p in features_dir.iterdir() if p.is_dir() and re.match(r"^\d{3}-", p.name)):
        stage, _ = probe_feature(f)
        if stage != "done":
            print(f"下一个特性: {f.name} → {stage}")
            return 0
    print("没有进行中的特性")
    return 0


def main(argv: list[str]) -> int:
    parser = ChineseArgumentParser(prog="hf_gate.py", description=__doc__)
    sub = parser.add_subparsers(
        dest="cmd",
        required=True,
        title="命令",
        metavar="{check,init,status,next}",
        parser_class=ChineseArgumentParser,
    )

    p_check = sub.add_parser("check", help="执行机械校验", description="执行机械门禁校验。")
    p_check.add_argument(
        "--feature",
        default=None,
        metavar="特性目录",
        help="要校验的特性目录",
    )
    p_check.add_argument(
        "--to",
        choices=TARGETS,
        dest="target",
        default=None,
        metavar="阶段",
        help=f"目标阶段（可选值：{', '.join(TARGETS)}）",
    )
    p_check.add_argument("--product", action="store_true", help="校验产品层")
    p_check.add_argument("--root", default=".", metavar="项目根目录", help="项目根目录")

    p_init = sub.add_parser(
        "init",
        help="初始化 CONTEXT/product/features",
        description="初始化 HarnessFlow 目录和模板。",
    )
    p_init.add_argument("--root", default=".", metavar="项目根目录", help="项目根目录")

    p_status = sub.add_parser(
        "status",
        help="恢复全局状态",
        description="读取磁盘内容并显示全局状态。",
    )
    p_status.add_argument("--root", default=".", metavar="项目根目录", help="项目根目录")

    p_next = sub.add_parser(
        "next",
        help="显示下一个未完成特性",
        description="显示下一个未完成特性及其当前阶段。",
    )
    p_next.add_argument("--root", default=".", metavar="项目根目录", help="项目根目录")

    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return int(e.code or 2)

    if args.cmd == "check":
        if args.product:
            return cmd_check_product(Path(args.root))
        if not args.feature or not args.target:
            print("错误: check 需要 --product，或 --feature 与 --to 同时给出")
            return 2
        return cmd_check(Path(args.feature), args.target)
    if args.cmd == "init":
        return cmd_init(Path(args.root))
    if args.cmd == "status":
        return cmd_status(Path(args.root))
    return cmd_next(Path(args.root))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""hf_gate.py — HarnessFlow 机械门禁与状态机（stdlib only）。

四个子命令:

  init  在项目根初始化产品层 product/（product.md、architecture.md、
        decisions.md、assumptions.md、backlog.md,已存在的文件不覆盖）
        与 features/ 目录。

            python3 skills/hf-workflow/scripts/hf_gate.py init [--root .]

  check 机械校验，只依据磁盘上的工件与评审记录，不采信任何叙述性文本。
        PASS 退出码 0，FAIL 退出码 1，用法错误 2。

            # 特性级: 能否进入目标阶段
            python3 skills/hf-workflow/scripts/hf_gate.py check \
                --feature features/012-x --to build
            # 产品层: 产品定义(shape)与架构(architect)是否完成、能否开始切片
            python3 skills/hf-workflow/scripts/hf_gate.py check --product [--root .]

  status 一条命令恢复全局状态: 产品层是否就绪、每个特性当前卡在哪个阶段、
        下一步做什么。新会话恢复状态用它，不依赖聊天记忆。

            python3 skills/hf-workflow/scripts/hf_gate.py status [--root .]

  next  从 product/backlog.md 取出第一个未勾选的切片。

            python3 skills/hf-workflow/scripts/hf_gate.py next [--root .]

特性级校验规则（按目标阶段）:

  frame.md 必须含三条机器可读行: `- 风险档位: 1|2|3`、`- 模式: 探索|建造`、
  `- 用户可感知: 是|否`。

  建造模式:
  --to plan    frame 三行齐备(档位须 ≥2)
  --to design  仅档位 3：spec.md 存在 + spec-review 通过且已确认
  --to build   档位 1：frame 齐备；
               档位 2：plan.md 含任务清单 + plan-review 通过且已确认；
               档位 3：spec/design 齐备 + 两轮评审均通过且已确认
  --to verify  build 前提 + 任务清单全部勾选(档位 ≥2)
  --to ship    verify 前提 + code-review 通过且已确认；
               用户可感知为"是"时另需 demo 验收(reviews/demo-acceptance.md
               结论: 接受 + 用户确认)

  探索模式（原型即弃，链路 frame → build → close）:
  仅限风险档位 1；不经 plan/design/verify，永远不能 ship（探索产物禁止
  直接晋升为正式代码，正式实现另起建造模式特性）。
  --to build   frame 三行齐备即可
  --to close   conclusion.md 非空

评审/验收记录的机器可读行: `- 结论: <值>`、`- 用户确认: <值>`、
`- 评审方式: subagent|独立会话|主会话降级`。评审方式为"主会话降级"时，
用户确认不得是 auto-approved（降级评审禁止自我确认）。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TIER_RE = re.compile(r"^-[ \t]*风险档位:[ \t]*([123])\b", re.MULTILINE)
MODE_RE = re.compile(r"^-[ \t]*模式:[ \t]*(探索|建造)\b", re.MULTILINE)
PERCEIVABLE_RE = re.compile(r"^-[ \t]*用户可感知:[ \t]*(是|否)\b", re.MULTILINE)
TASK_RE = re.compile(r"^- \[([ xX])\][ \t]*(T-\d+)\b", re.MULTILINE)
SLICE_RE = re.compile(r"^- \[([ xX])\][ \t]*(S-\d+)[ \t]*(.*)$", re.MULTILINE)
CONFIRM_RE = re.compile(r"^-[ \t]*用户确认:[ \t]*(\S.*)$", re.MULTILINE)

TARGETS = ("plan", "design", "build", "verify", "ship", "close")

PRODUCT_FILES = {
    "product.md": """# 产品定义

- 日期:
- 想法一句话: <为谁、解决什么问题、做成什么>
- 目标用户: <具体人群,不写"所有人">
- 要解决的问题: <现状哪里痛>
- 成功标准: <可观察的信号,如"用户能完成一次完整 X">
- 用户确认:

## MVP 边界（做什么）

<第一版必须包含的最小能力集>

## 不做清单（明确排除）

<第一版明确不做的;防止范围蔓延的唯一手段是把"不做"写下来>
""",
    "architecture.md": """# 架构（一页,也是代码库地图）

产品级架构由 hf-architect 产出;交付链各阶段先读本文件定位模块,再只读相关代码。
保持一页（≤80 行）;结构变化时由 hf-ship 回写。特性级设计细节写在 features/*/ 的
plan.md / design.md,不下沉到这里。

- 日期:
- 技术栈: <语言/框架/存储/部署;来自预设或用户指定,同步记入 decisions/assumptions>
- 系统形态: <单体 Web 应用 | CLI | API 服务 + 前端 | ...>
- 用户确认:

## 模块边界

<模块名 — 职责一句话 — 代码位置。每个切片/特性都应能指认它落在哪个模块。>

## 核心数据模型

<核心实体与关系,几行即可;字段级细节推迟到特性设计。>

## 关键流程

<1~3 条端到端主流程: 入口 → 模块 → 存储 → 出口。S-1 行走骨架至少穿透其中一条。>

## 横切约定

<错误处理、测试组织、目录布局、命名等;新代码必须遵循,偏离先回写这里。>
""",
    "decisions.md": """# 决策记录

已确认的决策（用户确认过，或从假设台账迁入）。只追加，不删改历史。
格式: `- D-<n> <日期> <决策内容> — 依据: <一句话>`

- D-1 <日期> 技术栈: <待定> — 依据: <用户确认 / 预设默认迁入>
""",
    "assumptions.md": """# 假设台账

agent 替用户做的默认选择。遇到欠定点的标准动作: 提出带默认值的选项 →
记录一条假设 → 继续推进；禁止静默填补。
状态: 生效 | 已确认（迁入 decisions.md）| 已推翻（评估波及,回对应阶段返工）。
格式: `- A-<n> <日期> [状态] <假设内容> — 默认理由: <一句话>`
""",
    "backlog.md": """# 切片待办

每片是端到端可演示的垂直切片，按优先级排序；S-1 固定为行走骨架。
勾选只在切片 ship 后由 hf-ship 执行。用户反馈产生的新切片追加在合适位置。
格式: `- [ ] S-<n> <切片名> — 演示判据: <用户能看到/做到什么>`

- [ ] S-1 行走骨架 — 演示判据: 用户能按 README 一条命令启动并访问应用的最薄端到端路径
""",
}


# ---------------------------------------------------------------- 解析工件

def read_frame_field(feature: Path, pattern: re.Pattern) -> str | None:
    frame = feature / "frame.md"
    if not frame.is_file():
        return None
    m = pattern.search(frame.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def read_tier(feature: Path) -> int | None:
    value = read_frame_field(feature, TIER_RE)
    return int(value) if value else None


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


def read_slices(root: Path) -> list[tuple[str, bool, str]] | None:
    """返回 backlog 里的 (切片ID, 是否完成, 描述) 列表；backlog 不存在返回 None。"""
    path = root / "product" / "backlog.md"
    if not path.is_file():
        return None
    return [(sid, mark.lower() == "x", rest.strip())
            for mark, sid, rest in SLICE_RE.findall(path.read_text(encoding="utf-8"))]


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

    def check_frame(self) -> tuple[int | None, str | None, str | None]:
        """校验 frame.md 三条机器可读行，返回 (档位, 模式, 用户可感知)。"""
        if not (self.feature / "frame.md").is_file():
            self.fail("frame.md 不存在 — 先完成 frame 阶段")
            return None, None, None
        tier = read_tier(self.feature)
        mode = read_frame_field(self.feature, MODE_RE)
        perceivable = read_frame_field(self.feature, PERCEIVABLE_RE)
        if tier is None:
            self.fail("frame.md 缺少机器可读的 `- 风险档位: 1|2|3` 行")
        else:
            self.ok(f"frame.md 风险档位: {tier}")
        if mode is None:
            self.fail("frame.md 缺少机器可读的 `- 模式: 探索|建造` 行")
        else:
            self.ok(f"frame.md 模式: {mode}")
        if perceivable is None:
            self.fail("frame.md 缺少机器可读的 `- 用户可感知: 是|否` 行")
        else:
            self.ok(f"frame.md 用户可感知: {perceivable}")
        return tier, mode, perceivable

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
            self.fail(f"{stem} 评审方式为主会话降级，禁止 auto-approved 自我确认，需用户真实确认")
            return
        self.ok(f"{stem}: {expected}，已确认 ({review['confirm']})")

    # -- 任务

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

    def task_ids(self, tier: int) -> list[tuple[str, bool]] | None:
        if tier == 1:
            return None  # tier-1 无任务清单
        return read_tasks(self.feature, self.task_doc_for(tier)) or []

    def check_tasks_done(self, tasks: list[tuple[str, bool]]) -> None:
        undone = [tid for tid, done in tasks if not done]
        if undone:
            self.fail(f"任务未全部完成，未勾选: {', '.join(undone)}")
        elif tasks:
            self.ok(f"任务清单全部勾选 ({len(tasks)} 项)")


def check_target(feature: Path, target: str) -> Checker:
    c = Checker(feature)
    tier, mode, perceivable = c.check_frame()
    if tier is None or mode is None:
        return c

    # ---- 探索模式: frame → build → close，原型即弃
    if mode == "探索":
        if tier != 1:
            c.fail(f"探索模式仅限风险档位 1（现为 {tier}）— 触碰数据/安全/公共接口的工作不允许探索模式")
        if target in ("plan", "design", "verify"):
            c.fail(f"探索模式不经 {target} 阶段 — 链路为 frame → build → close")
        elif target == "ship":
            c.fail("探索模式特性永远不能 ship — 结论写入 conclusion.md 走 `check --to close`；"
                   "正式实现另起建造模式特性，禁止直接晋升原型代码")
        elif target == "close":
            c.check_doc("conclusion.md")
        return c

    # ---- 建造模式
    if target == "close":
        c.fail("close 仅用于探索模式 — 建造模式走 verify → ship")
        return c

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
            if tasks is not None:
                c.check_tasks_done(tasks)
        if target == "ship":
            c.check_review("code-review.md")
            if perceivable == "是":
                c.check_review("demo-acceptance.md", expected="接受")
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


# ---------------------------------------------------------------- 产品层

def check_confirm(path: Path, oks: list[str], failures: list[str], fail_msg: str) -> None:
    """校验文件含有效的 `- 用户确认:` 行（占位符 <...> 不算）。"""
    if not path.is_file():
        return
    m = CONFIRM_RE.search(path.read_text(encoding="utf-8"))
    if not m or m.group(1).startswith("<"):
        failures.append(fail_msg)
    else:
        oks.append(f"{path.name} 用户确认: {m.group(1)}")


def check_product_layer(root: Path) -> tuple[list[str], list[str]]:
    """校验产品层五文件，返回 (oks, failures)。"""
    oks: list[str] = []
    failures: list[str] = []
    product = root / "product"
    if not product.is_dir():
        failures.append("product/ 不存在 — 先运行 `hf_gate.py init` 并按 hf-shape 塑形")
        return oks, failures
    for name in PRODUCT_FILES:
        path = product / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"product/{name} 不存在或为空")
        else:
            oks.append(f"product/{name} 存在")
    check_confirm(product / "product.md", oks, failures,
                  "product/product.md 缺有效的 `- 用户确认:` 行 — 产品定义未经确认不得进架构（hf-shape）")
    check_confirm(product / "architecture.md", oks, failures,
                  "product/architecture.md 缺有效的 `- 用户确认:` 行 — 架构未经确认不得开始切片（hf-architect）")
    slices = read_slices(root)
    if slices is not None:
        if not slices:
            failures.append("product/backlog.md 没有可解析的切片行（格式: `- [ ] S-1 ...`）— 需求拆解在 hf-architect 收尾时完成")
        else:
            done = sum(1 for _, d, _ in slices if d)
            oks.append(f"backlog 切片: {len(slices)} 片（已完成 {done}）")
    return oks, failures


def cmd_check_product(root: Path) -> int:
    print(f"== hf-gate check --product ({root})")
    oks, failures = check_product_layer(root)
    for msg in oks:
        print(f"OK   {msg}")
    for msg in failures:
        print(f"FAIL {msg}")
    if failures:
        print(f"RESULT: FAIL ({len(failures)} 项未通过) — 产品层未就绪，不得开始切片")
        return 1
    print("RESULT: PASS — 产品层就绪，可开始切片")
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
    features = root / "features"
    if not features.is_dir():
        features.mkdir(parents=True)
        print(f"[hf-gate] 已创建: {features}/")
    print("[hf-gate] 产品层模板就绪 — 按 hf-shape 完成产品定义、hf-architect 完成架构与拆解，再 `check --product`")
    return 0


# ---------------------------------------------------------------- status / next

def stage_sequence(tier: int, mode: str) -> list[str]:
    if mode == "探索":
        return ["build", "close"]
    if tier == 1:
        return ["build", "verify", "ship"]
    if tier == 2:
        return ["plan", "build", "verify", "ship"]
    return ["plan", "design", "build", "verify", "ship"]


def probe_feature(feature: Path) -> tuple[str, list[str]]:
    """探测特性当前所在阶段: 第一个 check FAIL 的目标即当前阶段。"""
    tier = read_tier(feature)
    mode = read_frame_field(feature, MODE_RE)
    if tier is None or mode is None:
        c = check_target(feature, "build")
        return "frame", c.failures
    for target in stage_sequence(tier, mode):
        c = check_target(feature, target)
        if c.failures:
            return target, c.failures
    return "done", []


def cmd_status(root: Path) -> int:
    print(f"== hf-gate status ({root.resolve()})")

    product_ready = None
    product_dir = root / "product"
    if (product_dir / "architecture.md").is_file() and not (product_dir / "product.md").is_file():
        # 存量项目只建了架构地图,不走产品层门禁
        print("产品层: 仅架构地图（存量项目模式；想法→APP 请先 hf-shape 补产品定义）")
    elif product_dir.is_dir():
        _, failures = check_product_layer(root)
        product_ready = not failures
        if product_ready:
            print("产品层: PASS（就绪）")
        else:
            print(f"产品层: FAIL（{len(failures)} 项未通过）")
            for msg in failures:
                print(f"  - {msg}")
    else:
        print("产品层: 无（存量项目特性交付模式；想法→APP 请先 `init` + hf-shape）")

    features_dir = root / "features"
    feature_dirs = sorted(p for p in features_dir.iterdir()
                          if p.is_dir() and re.match(r"^\d{3}-", p.name)) if features_dir.is_dir() else []
    active: tuple[Path, str, list[str]] | None = None
    if not feature_dirs:
        print("特性: 无")
    for f in feature_dirs:
        stage, failures = probe_feature(f)
        tier = read_tier(f)
        mode = read_frame_field(f, MODE_RE) or "?"
        if stage == "done":
            print(f"特性 {f.name}: done（档位 {tier} / {mode}）")
        else:
            print(f"特性 {f.name}: 当前卡在 → {stage}（档位 {tier or '?'} / {mode}）")
            for msg in failures[:3]:
                print(f"  - {msg}")
            if len(failures) > 3:
                print(f"  - …另有 {len(failures) - 3} 项，见 `check --feature {f} --to {stage}`")
            if active is None:
                active = (f, stage, failures)

    if active:
        f, stage, _ = active
        print(f"下一步: 推进 {f.name} 通过 `check --to {stage}`（先补齐上列缺失项）")
    elif product_ready:
        slices = read_slices(root) or []
        todo = [(sid, rest) for sid, done, rest in slices if not done]
        if todo:
            print(f"下一步: 开始下一个切片 {todo[0][0]} {todo[0][1]}（`next` 可再次查看）")
        else:
            print("下一步: backlog 已清空 — 与用户确认新切片或收尾")
    elif product_ready is False:
        print("下一步: 补齐产品层（产品定义 hf-shape → 架构与拆解 hf-architect），`check --product` PASS 后开始切片")
    else:
        print("下一步: 无进行中的工作 — 新特性从 hf-frame 进入；想法→APP 从 `init` + hf-shape 进入")
    return 0


def cmd_next(root: Path) -> int:
    slices = read_slices(root)
    if slices is None:
        print("product/backlog.md 不存在 — 先 `init` 并按 hf-shape 塑形")
        return 1
    todo = [(sid, rest) for sid, done, rest in slices if not done]
    if not todo:
        print("backlog 已清空 — 没有未完成的切片")
        return 0
    print(f"下一个切片: {todo[0][0]} {todo[0][1]}")
    return 0


# ---------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="hf_gate.py", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="机械校验: 特性能否进入目标阶段 / 产品层是否就绪")
    p_check.add_argument("--feature", default=None)
    p_check.add_argument("--to", choices=TARGETS, dest="target", default=None)
    p_check.add_argument("--product", action="store_true", help="校验产品层而非特性")
    p_check.add_argument("--root", default=".", help="项目根目录（默认当前目录）")

    p_init = sub.add_parser("init", help="初始化产品层 product/ 模板与 features/ 目录")
    p_init.add_argument("--root", default=".")

    p_status = sub.add_parser("status", help="恢复全局状态: 产品层 + 每个特性所在阶段 + 下一步")
    p_status.add_argument("--root", default=".")

    p_next = sub.add_parser("next", help="取 backlog 中第一个未完成的切片")
    p_next.add_argument("--root", default=".")

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

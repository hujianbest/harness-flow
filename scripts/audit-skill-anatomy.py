#!/usr/bin/env python3
"""Audit HF SKILL.md files against docs/principles/02 skill-anatomy.md.

Checks the anatomy contract for every SKILL.md under skills/, scoring each
against the canonical checklist. Read-only; produces a Markdown report.

Usage:
    python scripts/audit-skill-anatomy.py [--repo-root .] [--out PATH]
                                          [--format md|json] [--quiet]

The default report path is docs/audits/skill-anatomy-audit.md.
Exit code is 0 when all skills pass hard checks, 1 when any fails.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# Anatomy budget per docs/principles/02 skill-anatomy.md.
TOKEN_BUDGET = 5000
LINE_BUDGET = 500
# Rough token approximation: ~4 chars / token for mixed CJK + Latin.
CHAR_PER_TOKEN = 4

REQUIRED_SECTIONS = [
    "When to Use",
    "Workflow",
    "Verification",
]
WORKFLOW_REQUIRED_EXTRA = [
    "Object Contract",
    "Methodology",
]
RECOMMENDED_SECTIONS = [
    "Red Flags",
    "Output Contract",
    "Common Rationalizations",
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
NUMBERED_STEP_RE = re.compile(r"^###\s+\d+[A-Za-z]?\.\s|^\d+\.\s", re.MULTILINE)


@dataclass
class SkillAudit:
    skill: str
    path: str
    line_count: int = 0
    char_count: int = 0
    estimated_tokens: int = 0
    name_matches_dir: Optional[bool] = None
    description_present: bool = False
    description_imperative_or_use_when: bool = False
    description_looks_like_summary: bool = False
    h1_present: bool = False
    sections_found: list[str] = field(default_factory=list)
    missing_required: list[str] = field(default_factory=list)
    missing_workflow_required: list[str] = field(default_factory=list)
    missing_recommended: list[str] = field(default_factory=list)
    has_numbered_workflow: bool = False
    over_line_budget: bool = False
    over_token_budget: bool = False
    has_object_contract: bool = False
    has_methodology: bool = False
    has_common_rationalizations: bool = False
    has_red_flags: bool = False
    is_workflow_skill: bool = True
    hard_pass: bool = False
    notes: list[str] = field(default_factory=list)


SUMMARY_SIGNALS = [
    "read evidence",
    "read evidence,",
    "first read",
    "step 1",
    "step 2",
    "→",
    "->",
]


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    raw = m.group(1)
    out: dict[str, str] = {}
    current_key: Optional[str] = None
    buf: list[str] = []
    for line in raw.splitlines():
        if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*\s*:\s*", line):
            if current_key is not None:
                out[current_key] = "\n".join(buf).strip()
            key, _, val = line.partition(":")
            current_key = key.strip()
            buf = [val.strip()]
        else:
            buf.append(line.strip())
    if current_key is not None:
        out[current_key] = "\n".join(buf).strip()
    return out


def is_workflow_skill(skill_name: str) -> bool:
    # Per docs/principles/02 skill-anatomy.md, all hf-* + using-hf-workflow
    # are workflow skills, not technique/reference skills.
    return skill_name.startswith("hf-") or skill_name == "using-hf-workflow"


def description_looks_like_summary(desc: str) -> bool:
    if not desc:
        return False
    # If the description is already a classifier ("Use when ..." / "适用于 ...")
    # then arrow-shaped reroute hints like "(→ hf-design)" are legal, not a
    # workflow summary. Only flag when classifier anchors are absent.
    if description_is_classifier(desc):
        return False
    lower = desc.lower()
    hits = sum(1 for sig in SUMMARY_SIGNALS if sig in lower)
    if hits >= 2:
        return True
    if "→" in desc and desc.count("→") >= 2:
        return True
    return False


def description_is_classifier(desc: str) -> bool:
    if not desc:
        return False
    # Accept any of: imperative / "适用于" / "Use when" / "Not for" prefix
    # in either Chinese or English, since HF allows both.
    classifier_signals = [
        "use when",
        "not for",
        "适用于",
        "不适用",
    ]
    lower = desc.lower()
    return any(sig in lower for sig in classifier_signals)


def audit_skill(skill_dir: Path) -> SkillAudit:
    skill_md = skill_dir / "SKILL.md"
    a = SkillAudit(skill=skill_dir.name, path=str(skill_md))
    text = skill_md.read_text(encoding="utf-8")
    a.line_count = len(text.splitlines())
    a.char_count = len(text)
    a.estimated_tokens = a.char_count // CHAR_PER_TOKEN
    a.over_line_budget = a.line_count > LINE_BUDGET
    a.over_token_budget = a.estimated_tokens > TOKEN_BUDGET

    fm = parse_frontmatter(text)
    name = fm.get("name", "")
    desc = fm.get("description", "")
    a.name_matches_dir = name == skill_dir.name
    a.description_present = bool(desc)
    a.description_imperative_or_use_when = description_is_classifier(desc)
    a.description_looks_like_summary = description_looks_like_summary(desc)

    a.h1_present = bool(H1_RE.search(text))
    sections = [m.group(1).strip() for m in H2_RE.finditer(text)]
    a.sections_found = sections

    section_set_lower = {s.lower() for s in sections}

    def has_section(label: str) -> bool:
        ll = label.lower()
        return any(ll in s for s in section_set_lower)

    a.is_workflow_skill = is_workflow_skill(skill_dir.name)
    a.has_object_contract = has_section("Object Contract")
    a.has_methodology = has_section("Methodology")
    a.has_red_flags = has_section("Red Flags")
    a.has_common_rationalizations = has_section("Common Rationalizations")

    a.missing_required = [s for s in REQUIRED_SECTIONS if not has_section(s)]
    if a.is_workflow_skill:
        a.missing_workflow_required = [
            s for s in WORKFLOW_REQUIRED_EXTRA if not has_section(s)
        ]
    a.missing_recommended = [s for s in RECOMMENDED_SECTIONS if not has_section(s)]

    a.has_numbered_workflow = bool(NUMBERED_STEP_RE.search(text))

    if not a.name_matches_dir:
        a.notes.append(
            f"frontmatter `name: {name!r}` 与目录名 {skill_dir.name!r} 不一致"
        )
    if not a.description_present:
        a.notes.append("缺少 frontmatter `description`")
    elif not a.description_imperative_or_use_when:
        a.notes.append(
            "description 未使用 `Use when ... / 适用于 ...` 等分类器写法"
        )
    if a.description_looks_like_summary:
        a.notes.append(
            "description 看起来像流程摘要，违反「分类器，不是摘要」原则"
        )
    if a.over_line_budget:
        a.notes.append(f"超行预算：{a.line_count} 行 > {LINE_BUDGET}")
    if a.over_token_budget:
        a.notes.append(
            f"超 token 预算：~{a.estimated_tokens} tokens > {TOKEN_BUDGET}"
        )
    if a.is_workflow_skill and not a.has_object_contract:
        a.notes.append("workflow skill 缺 `Object Contract`")
    if a.is_workflow_skill and not a.has_methodology:
        a.notes.append("workflow skill 缺 `Methodology`")
    if not a.has_red_flags:
        a.notes.append("缺 `Red Flags`")
    if not a.has_common_rationalizations:
        a.notes.append(
            "缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐）"
        )
    if not a.has_numbered_workflow:
        a.notes.append("Workflow 区段未发现编号步骤")

    a.hard_pass = (
        a.name_matches_dir
        and a.description_present
        and a.description_imperative_or_use_when
        and not a.description_looks_like_summary
        and a.h1_present
        and not a.missing_required
        and (not a.is_workflow_skill or not a.missing_workflow_required)
        and a.has_numbered_workflow
        and not a.over_line_budget
        and not a.over_token_budget
    )
    return a


def render_markdown(audits: list[SkillAudit], repo_root: Path) -> str:
    total = len(audits)
    passing = sum(1 for a in audits if a.hard_pass)
    over_token = sum(1 for a in audits if a.over_token_budget)
    over_line = sum(1 for a in audits if a.over_line_budget)
    missing_obj = sum(
        1 for a in audits if a.is_workflow_skill and not a.has_object_contract
    )
    missing_meth = sum(
        1 for a in audits if a.is_workflow_skill and not a.has_methodology
    )
    missing_rf = sum(1 for a in audits if not a.has_red_flags)
    missing_cr = sum(1 for a in audits if not a.has_common_rationalizations)

    lines: list[str] = []
    lines.append("# HF SKILL.md Anatomy 审计报告")
    lines.append("")
    lines.append(
        "- 来源标准：`docs/principles/02 skill-anatomy.md` § 检查清单"
    )
    lines.append("- 关联决策：`docs/decisions/ADR-001-release-scope-v0.1.0.md`")
    lines.append("- 生成器：`scripts/audit-skill-anatomy.py`（只读）")
    lines.append(f"- 审计 SKILL.md 数：{total}")
    lines.append(f"- 通过 hard checks：{passing} / {total}")
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append("| 指标 | 数量 | 占比 |")
    lines.append("|---|---:|---:|")

    def row(label: str, n: int) -> str:
        pct = (n / total * 100) if total else 0
        return f"| {label} | {n} | {pct:.0f}% |"

    lines.append(row("通过全部 hard checks", passing))
    lines.append(row("超 token 预算", over_token))
    lines.append(row("超行预算", over_line))
    lines.append(row("workflow skill 缺 Object Contract", missing_obj))
    lines.append(row("workflow skill 缺 Methodology", missing_meth))
    lines.append(row("缺 Red Flags", missing_rf))
    lines.append(row("缺 Common Rationalizations（ADR-001 D8 要求）", missing_cr))
    lines.append("")
    lines.append("## 每个 Skill 的明细")
    lines.append("")
    lines.append(
        "| Skill | hard | lines | ~tokens | Obj | Meth | RF | CR | 备注 |"
    )
    lines.append(
        "|---|:-:|---:|---:|:-:|:-:|:-:|:-:|---|"
    )

    def y(b: bool) -> str:
        return "✅" if b else "❌"

    def na() -> str:
        return "—"

    for a in audits:
        obj_cell = y(a.has_object_contract) if a.is_workflow_skill else na()
        meth_cell = y(a.has_methodology) if a.is_workflow_skill else na()
        notes = "；".join(a.notes) if a.notes else ""
        # Markdown-table-safe: collapse pipes and newlines.
        notes = notes.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| `{a.skill}` | {y(a.hard_pass)} | {a.line_count} | "
            f"{a.estimated_tokens} | {obj_cell} | {meth_cell} | "
            f"{y(a.has_red_flags)} | {y(a.has_common_rationalizations)} | "
            f"{notes} |"
        )

    lines.append("")
    lines.append("## 整改优先级建议")
    lines.append("")
    lines.append(
        "P0（v0.1.0 阻塞，发版前必须修复）："
    )
    p0 = [a for a in audits if not a.hard_pass]
    if p0:
        for a in p0:
            issues = []
            if a.over_token_budget:
                issues.append(f"超 token 预算 (~{a.estimated_tokens})")
            if a.over_line_budget:
                issues.append(f"超行预算 ({a.line_count})")
            if a.is_workflow_skill and not a.has_object_contract:
                issues.append("缺 Object Contract")
            if a.is_workflow_skill and not a.has_methodology:
                issues.append("缺 Methodology")
            if a.missing_required:
                issues.append("缺必备段：" + ", ".join(a.missing_required))
            if a.description_looks_like_summary:
                issues.append("description 是摘要而非分类器")
            if not a.has_numbered_workflow:
                issues.append("Workflow 没编号步骤")
            if not issues:
                continue
            lines.append(f"- `{a.skill}`：" + "；".join(issues))
    else:
        lines.append("- 无")

    lines.append("")
    lines.append("P1（ADR-001 D8 要求 v0.1.0 全量补 anti-rationalization）：")
    p1 = [a for a in audits if not a.has_common_rationalizations]
    if p1:
        for a in p1:
            lines.append(f"- `{a.skill}` — 增加 `## Common Rationalizations` 表")
    else:
        lines.append("- 无")

    lines.append("")
    lines.append("## 抛回架构师的方向题（HF 不替你定）")
    lines.append("")
    lines.append(
        "下列发现**改变 skill 行为契约**而不仅是文档润色，按 "
        "`docs/principles/00 soul.md` 「方向 / 取舍 / 标准的最终权在用户」，"
        "需要你拍板后才能进入实现：")
    lines.append("")
    if missing_obj > 0:
        lines.append(
            f"- **Q1 — Object Contract 全量缺位（{missing_obj}/{total} workflow skills）**："
            "`docs/principles/02 skill-anatomy.md` 把 `## Object Contract` 列为 "
            "workflow skill **必备段**（写明 Primary / Frontend Input / Backend Output "
            "Object 与 Object Transformation）。当前**没有任何一个** SKILL.md 写了。"
            "v0.1.0 是否把它作为发版门禁？候选："
        )
        lines.append(
            "  - **A. 严格执行**：v0.1.0 前给 24 个 SKILL.md 全部补 Object Contract。"
            "工作量大、改动 contract、需逐个评审；但符合现行 anatomy 标准。"
        )
        lines.append(
            "  - **B. 暂时降级**：把"
            "`02 skill-anatomy.md` 中 Object Contract 改为 v0.1.0 「推荐」、"
            "v0.2.0 升级为「必备」。anatomy 标准放宽，发版速度快；"
            "但与 anatomy 文档现有口径冲突，需同时改 `02 skill-anatomy.md`。"
        )
        lines.append(
            "  - **C. 折中**：v0.1.0 仅给 router / TDD / 三个 gate / finalize 等 "
            "**核心 7 节点** 补；其余下沉到 v0.2.0。需要在 ADR 中显式列出"
            "「核心 7 节点」清单。"
        )
    if missing_cr > 0:
        lines.append(
            f"- **Q2 — Common Rationalizations 全量缺位（{missing_cr}/{total}）**："
            "ADR-001 D8 已锁定「v0.1.0 全量补」，**此项已决，无需再问**。"
            "本审计仅作为整改基线。"
        )
    lines.append("")
    lines.append("## 方法学说明")
    lines.append("")
    lines.append(
        "- Hard checks 等价于 `02 skill-anatomy.md` 检查清单的"
        "「不可协商」部分（identity / sections / workflow shape / budget）。"
    )
    lines.append(
        "- Common Rationalizations 在 v0.1.0 之前不是 hard check，"
        "但因 ADR-001 D8 决议而成为发版门禁。"
    )
    lines.append(
        "- token 估算用 `len(text)/4` 的粗略比例，仅用于发现违反预算的离群值；"
        "精确 token 数请按所用 tokenizer 复算。"
    )
    lines.append(
        "- 本脚本只读，不修改任何 SKILL.md；整改由后续 PR 显式完成。"
    )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument(
        "--out",
        default=None,
        help="Output report path (default: docs/audits/skill-anatomy-audit.md)",
    )
    parser.add_argument(
        "--format",
        choices=["md", "json"],
        default="md",
        help="Report format (default: md)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-skill stdout summary",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    skills_root = repo_root / "skills"
    if not skills_root.is_dir():
        print(f"error: skills/ not found under {repo_root}", file=sys.stderr)
        return 2

    skill_dirs = sorted(
        d for d in skills_root.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )
    audits = [audit_skill(d) for d in skill_dirs]

    if args.format == "json":
        payload = json.dumps(
            [asdict(a) for a in audits], ensure_ascii=False, indent=2,
        )
    else:
        payload = render_markdown(audits, repo_root)

    if args.out is None:
        default_dir = repo_root / "docs" / "audits"
        default_dir.mkdir(parents=True, exist_ok=True)
        suffix = "json" if args.format == "json" else "md"
        out_path = default_dir / f"skill-anatomy-audit.{suffix}"
    else:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text(payload, encoding="utf-8")

    if not args.quiet:
        passing = sum(1 for a in audits if a.hard_pass)
        print(
            f"audited {len(audits)} skills; hard-pass {passing}/{len(audits)}; "
            f"report: {out_path}"
        )
        for a in audits:
            mark = "OK" if a.hard_pass else "FAIL"
            print(f"  [{mark}] {a.skill}  ({a.line_count} lines, ~{a.estimated_tokens} tokens)")

    failing = [a for a in audits if not a.hard_pass]
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())

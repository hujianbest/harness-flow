#!/usr/bin/env python3
"""Audit HF SKILL.md files against docs/principles/skill-anatomy.md.

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

# Anatomy budget per docs/principles/skill-anatomy.md.
TOKEN_BUDGET = 5000
LINE_BUDGET = 500
# Rough token approximation: ~4 chars / token for mixed CJK + Latin.
CHAR_PER_TOKEN = 4

REQUIRED_SECTIONS = [
    "When to Use",
    "Workflow",
    "Verification",
]
# Per skill-anatomy.md (post-Q1=B): Object Contract is recommended in
# v0.1.0 and only becomes mandatory in v0.2.0; Methodology stays mandatory
# for workflow skills.
WORKFLOW_REQUIRED_EXTRA = [
    "Methodology",
]
WORKFLOW_RECOMMENDED_EXTRA = [
    "Object Contract",
]
# Per ADR-001 D8: Common Rationalizations is a v0.1.0 release gate for
# all workflow skills.
RECOMMENDED_SECTIONS = [
    "Red Flags",
    "Output Contract",
]
WORKFLOW_RELEASE_GATE_SECTIONS = [
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
    missing_workflow_recommended: list[str] = field(default_factory=list)
    missing_release_gate: list[str] = field(default_factory=list)
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
    release_gate_pass: bool = False
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
    # Per docs/principles/skill-anatomy.md, all hf-* + using-hf-workflow
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
        a.missing_workflow_recommended = [
            s for s in WORKFLOW_RECOMMENDED_EXTRA if not has_section(s)
        ]
        a.missing_release_gate = [
            s for s in WORKFLOW_RELEASE_GATE_SECTIONS if not has_section(s)
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
        a.notes.append(
            "workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）"
        )
    if a.is_workflow_skill and not a.has_methodology:
        a.notes.append("workflow skill 缺 `Methodology`（必需）")
    if not a.has_red_flags:
        a.notes.append("缺 `Red Flags`")
    if a.is_workflow_skill and not a.has_common_rationalizations:
        a.notes.append(
            "缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8）"
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
    a.release_gate_pass = (
        a.hard_pass
        and (not a.is_workflow_skill or not a.missing_release_gate)
    )
    return a


def render_markdown(audits: list[SkillAudit], repo_root: Path) -> str:
    total = len(audits)
    passing = sum(1 for a in audits if a.hard_pass)
    release_passing = sum(1 for a in audits if a.release_gate_pass)
    over_token = sum(1 for a in audits if a.over_token_budget)
    over_line = sum(1 for a in audits if a.over_line_budget)
    missing_obj = sum(
        1 for a in audits if a.is_workflow_skill and not a.has_object_contract
    )
    missing_meth = sum(
        1 for a in audits if a.is_workflow_skill and not a.has_methodology
    )
    missing_rf = sum(1 for a in audits if not a.has_red_flags)
    missing_cr = sum(
        1 for a in audits if a.is_workflow_skill and not a.has_common_rationalizations
    )

    lines: list[str] = []
    lines.append("# HF SKILL.md Anatomy 审计报告")
    lines.append("")
    lines.append(
        "- 来源标准：`docs/principles/skill-anatomy.md` § 检查清单"
    )
    lines.append("- 关联决策：`docs/decisions/ADR-001-release-scope-v0.1.0.md`")
    lines.append("- 生成器：`scripts/audit-skill-anatomy.py`（只读）")
    lines.append(f"- 审计 SKILL.md 数：{total}")
    lines.append(f"- 通过 hard checks（anatomy 必需段）：{passing} / {total}")
    lines.append(
        f"- 通过 v0.1.0 release gate（hard + Common Rationalizations）："
        f"{release_passing} / {total}"
    )
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append("| 指标 | 数量 | 占比 |")
    lines.append("|---|---:|---:|")

    def row(label: str, n: int) -> str:
        pct = (n / total * 100) if total else 0
        return f"| {label} | {n} | {pct:.0f}% |"

    lines.append(row("通过 anatomy hard checks", passing))
    lines.append(row("通过 v0.1.0 release gate（hard + CR）", release_passing))
    lines.append(row("超 token 预算", over_token))
    lines.append(row("超行预算", over_line))
    lines.append(row("workflow skill 缺 Methodology（必需）", missing_meth))
    lines.append(row("缺 Red Flags（必需）", missing_rf))
    lines.append(
        row("workflow skill 缺 Common Rationalizations（v0.1.0 release gate）",
            missing_cr)
    )
    lines.append(
        row("workflow skill 缺 Object Contract（v0.1.0 推荐 / v0.2.0 必需）",
            missing_obj)
    )
    lines.append("")
    lines.append("## 每个 Skill 的明细")
    lines.append("")
    lines.append(
        "列定义：`hard` = anatomy 必需段全部满足；`gate` = hard + Common "
        "Rationalizations（v0.1.0 发版门禁）；`Obj` = Object Contract "
        "（v0.1.0 推荐，缺位不计入 hard fail）。"
    )
    lines.append("")
    lines.append(
        "| Skill | hard | gate | lines | ~tokens | Meth | RF | CR | Obj | 备注 |"
    )
    lines.append(
        "|---|:-:|:-:|---:|---:|:-:|:-:|:-:|:-:|---|"
    )

    def y(b: bool) -> str:
        return "✅" if b else "❌"

    def na() -> str:
        return "—"

    for a in audits:
        obj_cell = y(a.has_object_contract) if a.is_workflow_skill else na()
        meth_cell = y(a.has_methodology) if a.is_workflow_skill else na()
        cr_cell = y(a.has_common_rationalizations) if a.is_workflow_skill else na()
        notes = "；".join(a.notes) if a.notes else ""
        notes = notes.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| `{a.skill}` | {y(a.hard_pass)} | {y(a.release_gate_pass)} | "
            f"{a.line_count} | {a.estimated_tokens} | {meth_cell} | "
            f"{y(a.has_red_flags)} | {cr_cell} | {obj_cell} | "
            f"{notes} |"
        )

    lines.append("")
    lines.append("## 整改优先级建议")
    lines.append("")
    lines.append(
        "P0（anatomy 必需段缺失，违反 `skill-anatomy.md` hard rule）："
    )
    p0 = [a for a in audits if not a.hard_pass]
    if p0:
        for a in p0:
            issues = []
            if a.over_token_budget:
                issues.append(f"超 token 预算 (~{a.estimated_tokens})")
            if a.over_line_budget:
                issues.append(f"超行预算 ({a.line_count})")
            if a.is_workflow_skill and not a.has_methodology:
                issues.append("缺 Methodology（必需）")
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
    lines.append(
        "P1（v0.1.0 release gate，ADR-001 D8 全量补 anti-rationalization）："
    )
    p1 = [
        a for a in audits
        if a.is_workflow_skill and not a.has_common_rationalizations
    ]
    if p1:
        for a in p1:
            lines.append(f"- `{a.skill}` — 增加 `## Common Rationalizations` 表")
    else:
        lines.append("- 无")

    lines.append("")
    lines.append("P2（v0.1.0 推荐 / v0.2.0 必需，建议本次顺手补）：")
    p2 = [
        a for a in audits
        if a.is_workflow_skill and not a.has_object_contract
    ]
    if p2:
        for a in p2:
            lines.append(f"- `{a.skill}` — 增加 `## Object Contract` 段")
    else:
        lines.append("- 无")

    lines.append("")
    lines.append("## 已关闭的方向题")
    lines.append("")
    lines.append(
        "- **Q1 — Object Contract 是否作为 v0.1.0 发版门禁？**"
        "架构师 2026-04-29 选 **B**：放宽 `skill-anatomy.md`，"
        "Object Contract 在 v0.1.0 为「推荐」、v0.2.0 升为「必需」。"
        "审计随即把它从 hard fail 降为 P2 推荐项；缺位不再阻塞 v0.1.0 发版。"
    )
    lines.append(
        "- **Q2 — Common Rationalizations 衍生冲突**："
        "`skill-anatomy.md` 已同步把 `Common Rationalizations` 从"
        "「默认不建议扩散」移到「workflow skill 推荐」，并写明 v0.1.0 "
        "全量补。审计把它升为 P1（v0.1.0 release gate）。"
    )
    lines.append("")
    lines.append("## 方法学说明")
    lines.append("")
    lines.append(
        "- **anatomy hard checks**：等价于 `skill-anatomy.md` 检查清单的"
        "「不可协商」部分（identity / Methodology / Workflow shape / "
        "Red Flags / Verification / token-line budget）。"
    )
    lines.append(
        "- **v0.1.0 release gate**：在 hard checks 基础上额外要求 workflow "
        "skill 写 `Common Rationalizations`（ADR-001 D8）。"
    )
    lines.append(
        "- **Object Contract**：v0.1.0 推荐、v0.2.0 必需（架构师 Q1=B 决议）。"
        "v0.1.0 缺位仅作 P2 提示，不阻塞发版。"
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
        gate = sum(1 for a in audits if a.release_gate_pass)
        print(
            f"audited {len(audits)} skills; "
            f"anatomy hard-pass {passing}/{len(audits)}; "
            f"v0.1.0 release-gate {gate}/{len(audits)}; "
            f"report: {out_path}"
        )
        for a in audits:
            if not a.hard_pass:
                mark = "FAIL"
            elif not a.release_gate_pass:
                mark = "GATE"
            else:
                mark = " OK "
            print(
                f"  [{mark}] {a.skill}  "
                f"({a.line_count} lines, ~{a.estimated_tokens} tokens)"
            )

    # Exit code reflects v0.1.0 release gate (the actually-shipping bar).
    failing = [a for a in audits if not a.release_gate_pass]
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())

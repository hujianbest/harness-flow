#!/usr/bin/env python3
"""HarnessFlow SKILL.md anatomy audit (advisory).

Per ADR-002 D5 / D9 / D10, this script enforces only structural-existence rules
on `skills/*/SKILL.md`:

  1. Frontmatter contains `name` and `description`, and `name` matches the
     directory name.
  2. SKILL.md contains the required H2 sections:
       - `## When to Use`
       - `## Workflow`
       - `## Verification`
       - `## Common Rationalizations`   (required from v0.2.0, ADR-002 D9)
  3. SKILL.md does NOT contain the forbidden H2 section:
       - `## 和其他 Skill 的区别`         (forbidden from v0.2.0, ADR-002 D9)
  4. SKILL.md main file size budget: < 500 lines (advisory warning only).

Other anatomy sections (`Object Contract`, `Methodology`, `Hard Gates`,
`Output Contract`, `Red Flags`, `Common Mistakes`, etc.) remain "author writes
when needed" and are NOT checked here (ADR-001 D11 + ADR-002 D10 partial scope).

Recognised skill subdirectories (per HF skill anatomy v2, ADR-006 since
v0.5.0):
  - `references/`  optional: templates and reference docs
  - `evals/`       optional: eval cases and READMEs
  - `scripts/`     optional: skill-OWNED tools that are part of this skill's
                   hard gate (e.g. `skills/hf-finalize/scripts/render-closeout-html.py`).
                   Cross-cutting maintainer tools live under repo-root
                   `scripts/` (this file is one example).

This audit only reads `<skill>/SKILL.md`; subdirectories are not traversed,
so adding `skills/<name>/scripts/` does not affect audit results.

This script is advisory: it returns a non-zero exit code when any required rule
fails so CI can surface annotations, but the project policy is to NOT block PR
merge on it (ADR-002 D5 sub-decision; revisit after v0.2.0 GA).

Usage:
    python3 scripts/audit-skill-anatomy.py [--skills-dir skills] [--json]

Exit codes:
    0 - all required rules pass (warnings allowed)
    1 - one or more required rules fail
    2 - script error / missing skills directory
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


REQUIRED_H2 = [
    "When to Use",
    "Workflow",
    "Verification",
    "Common Rationalizations",
]

FORBIDDEN_H2 = [
    "和其他 Skill 的区别",
]

MAIN_FILE_LINE_BUDGET = 500


@dataclass
class SkillReport:
    name: str
    path: str
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


@dataclass
class AuditReport:
    skills: List[SkillReport] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(s.ok for s in self.skills)

    @property
    def failed_count(self) -> int:
        return sum(1 for s in self.skills if not s.ok)

    @property
    def warning_count(self) -> int:
        return sum(len(s.warnings) for s in self.skills)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse the leading `---`-delimited YAML-ish frontmatter.

    We do not depend on PyYAML — only `key: value` lines are extracted, which
    matches the HF SKILL.md frontmatter convention.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end].strip()
    out: dict[str, str] = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks so headers inside examples are not counted."""
    return re.sub(r"```[\s\S]*?```", "", text)


def collect_h2(text: str) -> list[str]:
    no_code = strip_code_blocks(text)
    return [
        m.group(1).strip()
        for m in re.finditer(r"^##\s+(.+?)\s*$", no_code, flags=re.MULTILINE)
    ]


def normalize_heading(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("`", "")).strip()


def audit_skill(skill_dir: Path) -> SkillReport:
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    report = SkillReport(name=name, path=str(skill_md))

    if not skill_md.is_file():
        report.failures.append(f"missing SKILL.md at {skill_md}")
        return report

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if not fm.get("name"):
        report.failures.append("frontmatter missing `name`")
    elif fm["name"] != name:
        report.failures.append(
            f"frontmatter `name: {fm['name']}` does not match directory `{name}`"
        )
    if not fm.get("description"):
        report.failures.append("frontmatter missing `description`")

    headings = [normalize_heading(h) for h in collect_h2(text)]

    for required in REQUIRED_H2:
        if normalize_heading(required) not in headings:
            report.failures.append(f"missing required section: `## {required}`")

    for forbidden in FORBIDDEN_H2:
        if normalize_heading(forbidden) in headings:
            report.failures.append(
                f"forbidden section present: `## {forbidden}` "
                "(absorb into `## When to Use` per ADR-002 D9)"
            )

    line_count = text.count("\n") + 1
    if line_count > MAIN_FILE_LINE_BUDGET:
        report.warnings.append(
            f"main file is {line_count} lines (budget {MAIN_FILE_LINE_BUDGET}); "
            "consider sinking content to references/"
        )

    return report


def audit_dir(skills_dir: Path) -> AuditReport:
    report = AuditReport()
    if not skills_dir.is_dir():
        raise SystemExit(f"skills directory not found: {skills_dir}")

    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        report.skills.append(audit_skill(entry))
    return report


def render_text(report: AuditReport) -> str:
    lines: list[str] = []
    lines.append(f"Audited {len(report.skills)} skill(s).")
    lines.append("")
    for s in report.skills:
        if s.ok and not s.warnings:
            lines.append(f"  OK    {s.name}")
            continue
        marker = "FAIL" if s.failures else "WARN"
        lines.append(f"  {marker}  {s.name}  ({s.path})")
        for f in s.failures:
            lines.append(f"        FAIL: {f}")
        for w in s.warnings:
            lines.append(f"        WARN: {w}")
    lines.append("")
    lines.append(
        f"Summary: {report.failed_count} failing skill(s), "
        f"{report.warning_count} warning(s)."
    )
    if not report.ok:
        lines.append(
            "Required rules failed. See "
            "docs/principles/skill-anatomy.md (v0.2.0 baseline) and "
            "docs/decisions/ADR-002-release-scope-v0.2.0.md (D9 / D10)."
        )
    return "\n".join(lines)


def render_json(report: AuditReport) -> str:
    return json.dumps(
        {
            "skills": [
                {
                    "name": s.name,
                    "path": s.path,
                    "failures": s.failures,
                    "warnings": s.warnings,
                    "ok": s.ok,
                }
                for s in report.skills
            ],
            "ok": report.ok,
            "failed_count": report.failed_count,
            "warning_count": report.warning_count,
        },
        ensure_ascii=False,
        indent=2,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument(
        "--skills-dir",
        default="skills",
        help="path to the top-level skills directory (default: skills)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="emit a JSON report instead of human-readable text",
    )
    args = p.parse_args(argv)

    try:
        report = audit_dir(Path(args.skills_dir))
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    out = render_json(report) if args.json else render_text(report)
    print(out)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate HarnessFlow skill files.

Checks every skills/*/SKILL.md for:
- YAML frontmatter with exactly `name` and `description`
- `name` matching the directory name
- description length <= 1024 chars and non-empty
- ext-* descriptions declaring binding stage and trigger condition
- body line limits (core <= 200, ext <= 150)
- referenced `references/...` paths existing on disk

Exit code 0 = all good, 1 = violations found.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
CORE_BODY_LIMIT = 200
EXT_BODY_LIMIT = 150

errors: list[str] = []


def check_skill(skill_dir: Path) -> None:
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        errors.append(f"{skill_dir.name}: missing SKILL.md")
        return

    text = md.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.DOTALL)
    if not m:
        errors.append(f"{skill_dir.name}: missing or malformed YAML frontmatter")
        return
    frontmatter, body = m.group(1), m.group(2)

    fields = {}
    for line in frontmatter.splitlines():
        fm = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if fm:
            fields[fm.group(1)] = fm.group(2).strip()

    if set(fields) != {"name", "description"}:
        errors.append(f"{skill_dir.name}: frontmatter fields must be exactly name+description, got {sorted(fields)}")
    if fields.get("name") != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name '{fields.get('name')}' != directory name")
    desc = fields.get("description", "")
    if not desc:
        errors.append(f"{skill_dir.name}: empty description")
    if len(desc) > 1024:
        errors.append(f"{skill_dir.name}: description too long ({len(desc)} > 1024 chars)")

    is_ext = skill_dir.name.startswith("ext-")
    if is_ext:
        if "绑定阶段" not in desc:
            errors.append(f"{skill_dir.name}: ext skill description must declare 绑定阶段")
        if "触发条件" not in desc:
            errors.append(f"{skill_dir.name}: ext skill description must declare 触发条件")

    body_lines = len(body.splitlines())
    limit = EXT_BODY_LIMIT if is_ext else CORE_BODY_LIMIT
    if body_lines > limit:
        errors.append(f"{skill_dir.name}: body {body_lines} lines exceeds limit {limit}")

    for ref in re.findall(r"`((?:skills/)?references?/[\w./-]+|skills/[\w-]+/references/[\w./-]+)`", text):
        base = ROOT if ref.startswith("skills/") else skill_dir
        if not (base / ref).is_file():
            errors.append(f"{skill_dir.name}: referenced file not found: {ref}")


def main() -> int:
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not skill_dirs:
        print("no skill directories found", file=sys.stderr)
        return 1
    for d in skill_dirs:
        check_skill(d)
    if errors:
        print(f"FAIL: {len(errors)} violation(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {len(skill_dirs)} skills validated "
          f"({', '.join(d.name for d in skill_dirs)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

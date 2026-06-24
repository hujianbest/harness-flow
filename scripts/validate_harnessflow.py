"""Lightweight repository checks for the HarnessFlow rewrite (DevFlow-aligned)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SKILLS = {
    "using-hf",
    "hf-specify",
    "hf-design",
    "hf-tdd",
    "hf-review",
    "hf-ship",
    "hf-fix",
    "hf-clean-code",
    "c-coding-standards",
    "cpp-coding-standards",
    "java-coding-standards",
    "python-coding-standards",
    "coding-standards-creator",
    "backend-development",
    "frontend-development",
}

CODING_STANDARDS_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*-coding-standards$")
CODING_STANDARDS_MAX_LINES = 300
MIN_SCENARIOS = 3

# Removed/renamed skills in the rewrite; they must not resurface in active text.
LEGACY_SKILL_NAMES = {
    "hf-discovery", "hf-product-discovery", "hf-discovery-review",
    "hf-spec", "hf-spec-review",
    "hf-ui", "hf-ui-design", "hf-ui-review", "hf-design-review",
    "hf-build", "hf-test-driven-dev", "hf-subagent-driven-dev",
    "hf-tasks", "hf-tasks-review",
    "hf-code-review", "hf-test-review", "hf-traceability-review", "hf-gap-analyzer",
    "hf-finalize", "hf-verify", "hf-completion-gate", "hf-regression-gate",
    "hf-doc-freshness-gate", "hf-release", "hf-browser-testing",
    "hf-hotfix", "hf-increment", "hf-experiment", "hf-ultrawork",
    "hf-wisdom-notebook", "hf-context-mesh",
    "hf-workflow-router", "using-hf-workflow",
}

# Over-engineered mechanisms from the old router; replaced by attended/unattended
# runtime mode and the plan.md lightweight state machine.
LEGACY_MECHANISM_PHRASES = [
    "Workflow Profile",
    "Execution Mode",
    "Workspace Isolation",
    "Next Action Or Recommended Skill",
    "reroute_via_router",
    "canonical node",
    "canonical 节点",
    "category_hint",
    "wisdom_summary",
]

LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def iter_active_markdown_files(root: Path):
    """Active text = skills, commands, agents, READMEs."""
    for sub in ("skills", "commands", "agents"):
        base = root / sub
        if base.exists():
            yield from base.rglob("*.md")
    for name in ("README.md", "README.zh-CN.md"):
        path = root / name
        if path.exists():
            yield path


def validate_skill_frontmatter(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for skill in root.glob("skills/*/SKILL.md"):
        text = skill.read_text(encoding="utf-8", errors="ignore")
        if not text.startswith("---\n"):
            errors.append(f"{skill}: missing YAML frontmatter")
            continue
        end = text.find("\n---", 4)
        if end == -1:
            errors.append(f"{skill}: unterminated YAML frontmatter")
            continue
        frontmatter = text[4:end]
        if "\nname:" not in f"\n{frontmatter}":
            errors.append(f"{skill}: missing name")
        if "\ndescription:" not in f"\n{frontmatter}":
            errors.append(f"{skill}: missing description")
        expected_name = skill.parent.name
        name_match = re.search(r"^name:\s*([A-Za-z0-9_-]+)\s*$", frontmatter, re.MULTILINE)
        if name_match and name_match.group(1) != expected_name:
            errors.append(
                f"{skill}: name {name_match.group(1)} does not match directory {expected_name}"
            )
    return errors


def validate_skill_set(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.exists():
        return [f"{skills_root}: skills directory is missing"]

    present = {p.name for p in skills_root.iterdir() if p.is_dir()}
    for missing in sorted(EXPECTED_SKILLS - present):
        errors.append(f"skills/{missing}: expected skill is missing")
    for legacy in sorted(present & LEGACY_SKILL_NAMES):
        errors.append(f"skills/{legacy}: legacy skill should be removed")
    for name in sorted(present):
        if name.endswith("-coding-standards") and not CODING_STANDARDS_NAME.match(name):
            errors.append(
                f"skills/{name}: must follow the <language>-coding-standards naming convention"
            )
    return errors


def find_legacy_references(text: str) -> list[str]:
    found: list[str] = []
    for name in sorted(LEGACY_SKILL_NAMES):
        if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])", text):
            found.append(name)
    for phrase in LEGACY_MECHANISM_PHRASES:
        if phrase in text:
            found.append(phrase)
    return found


def validate_no_legacy_references(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for path in iter_active_markdown_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for hit in find_legacy_references(text):
            errors.append(f"{path}: legacy reference remains: {hit}")
    return errors


def validate_eval_json(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for path in root.glob("skills/*/evals/*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        scenarios = data.get("scenarios")
        count = len(scenarios) if isinstance(scenarios, list) else 0
        if count < MIN_SCENARIOS:
            errors.append(
                f"{path}: needs >= {MIN_SCENARIOS} scenarios, found {count}"
            )
    return errors


def validate_coding_standards_length(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for skill in root.glob("skills/*-coding-standards/SKILL.md"):
        n = len(skill.read_text(encoding="utf-8", errors="ignore").splitlines())
        if n > CODING_STANDARDS_MAX_LINES:
            errors.append(
                f"{skill}: {n} lines exceeds {CODING_STANDARDS_MAX_LINES}"
            )
    return errors


def iter_markdown_files(root: Path):
    ignored = {".git", "__pycache__", ".cursor", ".idea"}
    for path in root.rglob("*.md"):
        if ignored.intersection(path.parts):
            continue
        yield path


def validate_markdown_links(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for target in LINK_PATTERN.findall(text):
            if "://" in target or target.startswith("#") or target.startswith("mailto:"):
                continue
            link_path = target.split("#", 1)[0]
            if not link_path:
                continue
            resolved = (path.parent / link_path).resolve()
            if not resolved.exists():
                errors.append(f"{path}: missing link target {target}")
    return errors


def validate_agent_frontmatter(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    agents_dir = root / "agents"
    if not agents_dir.exists():
        return [f"{agents_dir}: agents directory is missing"]
    for agent in agents_dir.glob("*.md"):
        text = agent.read_text(encoding="utf-8", errors="ignore")
        if not text.startswith("---\n"):
            errors.append(f"{agent}: missing YAML frontmatter (need description + mode)")
            continue
        end = text.find("\n---", 4)
        if end == -1:
            errors.append(f"{agent}: unterminated YAML frontmatter")
            continue
        frontmatter = text[4:end]
        if "\ndescription:" not in f"\n{frontmatter}":
            errors.append(f"{agent}: missing description (required for subagent dispatch)")
        if "\nmode:" not in f"\n{frontmatter}":
            errors.append(f"{agent}: missing mode (subagent agents need mode: subagent)")
    return errors


def run_all(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_markdown_links(root))
    errors.extend(validate_skill_frontmatter(root))
    errors.extend(validate_agent_frontmatter(root))
    errors.extend(validate_skill_set(root))
    errors.extend(validate_no_legacy_references(root))
    errors.extend(validate_eval_json(root))
    errors.extend(validate_coding_standards_length(root))
    return errors


def main() -> int:
    errors = run_all(ROOT)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("HarnessFlow validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_harnessflow.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_harnessflow", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_skill(root: Path, name: str):
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: test trigger\n---\n# {name}\n",
        encoding="utf-8",
    )


def test_expected_skill_set_is_enforced(tmp_path):
    validator = load_validator()
    for name in validator.EXPECTED_SKILLS - {"hf-tdd"}:
        write_skill(tmp_path, name)

    result = validator.validate_skill_set(tmp_path)

    assert any("hf-tdd" in e and "missing" in e for e in result)


def test_legacy_skill_directories_are_rejected(tmp_path):
    validator = load_validator()
    for name in validator.EXPECTED_SKILLS:
        write_skill(tmp_path, name)
    write_skill(tmp_path, "hf-workflow-router")

    result = validator.validate_skill_set(tmp_path)

    assert any("hf-workflow-router" in e and "removed" in e for e in result)


def test_frontmatter_name_must_match_directory(tmp_path):
    validator = load_validator()
    skill_dir = tmp_path / "skills" / "hf-tdd"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: wrong-name\ndescription: test\n---\n", encoding="utf-8"
    )

    result = validator.validate_skill_frontmatter(tmp_path)

    assert any("does not match directory" in e for e in result)


def test_legacy_references_are_detected_in_active_text():
    validator = load_validator()

    assert "hf-workflow-router" in validator.find_legacy_references(
        "route via hf-workflow-router"
    )
    assert "Workflow Profile" in validator.find_legacy_references(
        "decide Workflow Profile before build"
    )
    assert validator.find_legacy_references("use hf-tdd and hf-design") == []


def test_legacy_reference_in_active_file_is_reported(tmp_path):
    validator = load_validator()
    skill = tmp_path / "skills" / "hf-tdd" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("next: reroute_via_router=true\n", encoding="utf-8")

    result = validator.validate_no_legacy_references(tmp_path)

    assert any("reroute_via_router" in e for e in result)


import json as _json


def _write_evals(skill_dir: Path, scenarios: list) -> None:
    e = skill_dir / "evals"
    e.mkdir(parents=True, exist_ok=True)
    (e / "evals.json").write_text(
        _json.dumps({"skill_name": skill_dir.name, "scenarios": scenarios}),
        encoding="utf-8",
    )


def test_evals_need_at_least_three_scenarios(tmp_path):
    validator = load_validator()
    skill = tmp_path / "skills" / "hf-tdd"
    skill.mkdir(parents=True)
    _write_evals(skill, [{"id": 1, "prompt": "p", "expected": "e", "expectations": []}])

    result = validator.validate_eval_json(tmp_path)

    assert any("scenarios" in e for e in result)


def test_three_scenarios_pass(tmp_path):
    validator = load_validator()
    skill = tmp_path / "skills" / "hf-tdd"
    skill.mkdir(parents=True)
    scenarios = [
        {"id": i, "prompt": "p", "expected": "e", "expectations": ["a"]} for i in (1, 2, 3)
    ]
    _write_evals(skill, scenarios)

    assert validator.validate_eval_json(tmp_path) == []


def test_coding_standards_length_cap(tmp_path):
    validator = load_validator()
    skill = tmp_path / "skills" / "cpp-coding-standards"
    skill.mkdir(parents=True)
    body = "---\nname: cpp-coding-standards\ndescription: t\n---\n" + ("x\n" * 400)
    (skill / "SKILL.md").write_text(body, encoding="utf-8")

    result = validator.validate_coding_standards_length(tmp_path)

    assert any("exceeds" in e for e in result)


def test_agent_missing_frontmatter_is_caught(tmp_path):
    validator = load_validator()
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "hf-reviewer.md").write_text("# reviewer\n", encoding="utf-8")

    result = validator.validate_agent_frontmatter(tmp_path)

    assert any("missing YAML frontmatter" in e for e in result)


def test_markdown_link_checker_reports_missing_relative_links(tmp_path):
    validator = load_validator()
    doc = tmp_path / "doc.md"
    doc.write_text("[missing](missing.md)\n", encoding="utf-8")

    result = validator.validate_markdown_links(tmp_path)

    assert "missing.md" in result[0]


def test_link_checker_skips_internal_planning_and_governance(tmp_path):
    validator = load_validator()
    # A literal link inside a planning doc's code example (docs/superpowers/)
    # and an illustrative link in .github/ must NOT be flagged.
    plan = tmp_path / "docs" / "superpowers" / "plans" / "p.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("example: [missing](missing.md)\n", encoding="utf-8")
    gov = tmp_path / ".github" / "PULL_REQUEST_TEMPLATE.md"
    gov.parent.mkdir(parents=True)
    gov.write_text("- [ ] links ([...](...)) resolve\n", encoding="utf-8")

    assert validator.validate_markdown_links(tmp_path) == []


def test_run_all_returns_empty_on_clean_repo(tmp_path):
    validator = load_validator()
    for name in validator.EXPECTED_SKILLS:
        write_skill(tmp_path, name)
        if name.endswith("-coding-standards"):
            _write_evals(tmp_path / "skills" / name,
                         [{"id": i, "prompt": "p", "expected": "e", "expectations": []}
                          for i in (1, 2, 3)])
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "hf-reviewer.md").write_text(
        "---\ndescription: d\nmode: subagent\n---\n# r\n", encoding="utf-8"
    )

    assert validator.run_all(tmp_path) == []


def test_non_dict_evals_json_is_reported_not_crash(tmp_path):
    validator = load_validator()
    skill = tmp_path / "skills" / "hf-tdd" / "evals"
    skill.mkdir(parents=True)
    (skill / "evals.json").write_text('["bare", "array"]\n', encoding="utf-8")

    result = validator.validate_eval_json(tmp_path)

    assert any("must be an object" in e for e in result)


def test_evals_validator_only_checks_canonical_evals_json(tmp_path):
    validator = load_validator()
    skill = tmp_path / "skills" / "hf-tdd"
    skill.mkdir(parents=True)
    # canonical file present and valid
    _write_evals(skill, [{"id": i, "prompt": "p", "expected": "e", "expectations": []} for i in (1, 2, 3)])
    # sibling bare-array file that must NOT be inspected (would crash old code)
    (skill / "evals" / "test-prompts.json").write_text('["x"]\n', encoding="utf-8")

    assert validator.validate_eval_json(tmp_path) == []

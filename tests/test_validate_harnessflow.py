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

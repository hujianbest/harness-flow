# HarnessFlow 重写 — Plan 1：基础与校验骨架 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 搭建 HarnessFlow 重写的校验骨架、质量契约文档与入口技能 `using-hf`，为后续 14 个技能的写作提供可执行的质量门禁与结构模板。

**Architecture:** 镜像 DevFlow 的 `validate_devflow.py`：可导入的纯函数 + `tmp_path` fixture 测试，使校验脚本自身始终 green、独立于真实仓库状态。`using-hf` 镜像 `using-devflow` 的 9 段结构，落地三层质量模型、`plan.md` 轻量状态机与 attended/unattended 运行模式。

**Tech Stack:** Python 3（仅标准库）、pytest。

**这是 4 个计划中的 Plan 1。** 整体重写分 4 个顺序计划：
- **Plan 1（本文件）**：校验骨架 + 质量契约 + using-hf + 设计文档。
- Plan 2：阶段技能 hf-specify / hf-design / hf-tdd / hf-review / hf-ship / hf-fix。
- Plan 3：overlay — hf-clean-code + 4 个语言标准 + coding-standards-creator + backend/frontend-development。
- Plan 4：适配层与清理（commands/agents/install/marketplace/README + 删除旧技能目录 + 清理旧 tests）。

**内容约定（适用于全部 4 个计划）：** 技能是"内容工件"，不是代码。对每个技能，计划给出（1）精确文件、（2）必须的章节结构（来自质量契约）、（3）必须逐字或近逐字出现的"约束内容"（表格/规则/frontmatter/状态机）、（4）要读的蒸馏来源、（5）验收标准（validate 脚本 + 自检清单）。连接性叙述由执行者按计划点名的模板（如 `using-devflow`）仿写。这不是占位符——每个工件都有完整规格与模板指针。

---

## File Structure（本计划产出/修改）

| 文件 | 责任 | 动作 |
|---|---|---|
| `scripts/validate_harnessflow.py` | 仓库一致性校验：技能清单、frontmatter、旧名/旧机制残留、evals、coding-standards 行数上限、markdown 链接、agent frontmatter | Create（TDD 增量构建） |
| `tests/test_validate_harnessflow.py` | 校验脚本逻辑测试，`tmp_path` fixture 隔离 | Create |
| `skills/coding-standards-creator/references/hf-skill-quality-contract.md` | 全部技能必须满足的质量契约（spec §2.3） | Create |
| `docs/harnessflow-philosophy.md` | 三层质量模型 + human-on-the-loop 立场 | Create |
| `docs/harnessflow-core-architecture.md` | 15 技能架构 + 工件约定 + 运行模式 | Create |
| `skills/using-hf/SKILL.md` | 单一入口，镜像 using-devflow 9 段 | Create |

> 注：`validate_harnessflow.py` 在真实仓库上运行，在 Plan 4 完成前会报告"缺少技能"（因为其余 14 个技能尚未写）。这是预期的进度仪表，**不是 Plan 1 的失败**。Plan 1 的 green 标准是 `pytest tests/test_validate_harnessflow.py` 通过（fixture 隔离）。

---

## 约定：evals 文件格式（全计划统一）

所有 `skills/<name>/evals/evals.json` 采用：

```json
{
  "skill_name": "<name>",
  "scenarios": [
    {
      "id": 1,
      "prompt": "诱导模型违规的场景（含一个看似合理的理由）",
      "expected": "技能应触发的拒绝/修正行为与结论",
      "expectations": ["可勾选的检查点 1", "检查点 2", "检查点 3"]
    }
  ]
}
```

校验脚本断言：合法 JSON、含 `scenarios` 列表、`len(scenarios) >= 3`。

---

## Task 1: 校验脚本骨架 + 技能清单 + frontmatter 校验（TDD）

**Files:**
- Create: `tests/test_validate_harnessflow.py`
- Create: `scripts/validate_harnessflow.py`
- Test: `tests/test_validate_harnessflow.py`

- [ ] **Step 1: 写失败测试（导入 + 技能清单 + frontmatter）**

写入 `tests/test_validate_harnessflow.py`：

```python
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_validate_harnessflow.py -v`
Expected: FAIL（`validate_harnessflow.py` 不存在，`load_validator` 抛错）。

- [ ] **Step 3: 实现校验脚本第一部分**

写入 `scripts/validate_harnessflow.py`：

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_validate_harnessflow.py -v`
Expected: PASS（3 个测试）。

- [ ] **Step 5: 提交**

```bash
git add scripts/validate_harnessflow.py tests/test_validate_harnessflow.py
git commit -m "feat(validate): add skill-set and frontmatter checks for the rewrite"
```

---

## Task 2: 旧名/旧机制残留校验（TDD）

**Files:**
- Modify: `tests/test_validate_harnessflow.py`（追加测试）
- Modify: `scripts/validate_harnessflow.py`（追加函数）

- [ ] **Step 1: 追加失败测试**

在 `tests/test_validate_harnessflow.py` 末尾追加：

```python
def test_legacy_references_are_detected_in_active_text():
    validator = load_validator()

    assert "hf-workflow-router" in validator.find_legacy_references(
        "route via hf-workflow-router"
    )
    assert "Workflow Profile" in validator.find_legacy_references(
        "decide Workflow Profile before build"
    )
    # 新技能名不含旧 token，应为空。
    assert validator.find_legacy_references("use hf-tdd and hf-design") == []


def test_legacy_reference_in_active_file_is_reported(tmp_path):
    validator = load_validator()
    skill = tmp_path / "skills" / "hf-tdd" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("next: reroute_via_router=true\n", encoding="utf-8")

    result = validator.validate_no_legacy_references(tmp_path)

    assert any("reroute_via_router" in e for e in result)
```

- [ ] **Step 2: 运行确认失败**

Run: `pytest tests/test_validate_harnessflow.py -v`
Expected: FAIL（`find_legacy_references` / `validate_no_legacy_references` 不存在）。

- [ ] **Step 3: 实现残留校验**

在 `scripts/validate_harnessflow.py` 追加：

```python
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
```

- [ ] **Step 4: 运行确认通过**

Run: `pytest tests/test_validate_harnessflow.py -v`
Expected: PASS（5 个测试）。

- [ ] **Step 5: 提交**

```bash
git add scripts/validate_harnessflow.py tests/test_validate_harnessflow.py
git commit -m "feat(validate): detect legacy skill names and router mechanisms"
```

---

## Task 3: evals 场景数 + coding-standards 行数上限校验（TDD）

**Files:**
- Modify: `tests/test_validate_harnessflow.py`
- Modify: `scripts/validate_harnessflow.py`

- [ ] **Step 1: 追加失败测试**

在 `tests/test_validate_harnessflow.py` 末尾追加：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `pytest tests/test_validate_harnessflow.py -v`
Expected: FAIL（两个新校验函数不存在）。

- [ ] **Step 3: 实现 evals + 行数校验**

在 `scripts/validate_harnessflow.py` 追加：

```python
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
```

- [ ] **Step 4: 运行确认通过**

Run: `pytest tests/test_validate_harnessflow.py -v`
Expected: PASS（8 个测试）。

- [ ] **Step 5: 提交**

```bash
git add scripts/validate_harnessflow.py tests/test_validate_harnessflow.py
git commit -m "feat(validate): enforce >=3 eval scenarios and coding-standards line cap"
```

---

## Task 4: agent frontmatter + markdown 链接 + main 串联（TDD）

**Files:**
- Modify: `tests/test_validate_harnessflow.py`
- Modify: `scripts/validate_harnessflow.py`

- [ ] **Step 1: 追加失败测试**

在 `tests/test_validate_harnessflow.py` 末尾追加：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `pytest tests/test_validate_harnessflow.py -v`
Expected: FAIL（新函数缺失；`run_all` 不存在）。

- [ ] **Step 3: 实现剩余校验 + main**

在 `scripts/validate_harnessflow.py` 追加：

```python
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
```

- [ ] **Step 4: 运行确认全部通过**

Run: `pytest tests/test_validate_harnessflow.py -v`
Expected: PASS（11 个测试）。

- [ ] **Step 5: 提交**

```bash
git add scripts/validate_harnessflow.py tests/test_validate_harnessflow.py
git commit -m "feat(validate): add agent/link checks and wire run_all/main"
```

---

## Task 5: 质量契约 + 哲学 + 架构文档

**Files:**
- Create: `skills/coding-standards-creator/references/hf-skill-quality-contract.md`
- Create: `docs/harnessflow-philosophy.md`
- Create: `docs/harnessflow-core-architecture.md`

- [ ] **Step 1: 写质量契约（全部技能的权威标准）**

写入 `skills/coding-standards-creator/references/hf-skill-quality-contract.md`：

````markdown
# HF Skill 质量契约

> 适用于 HarnessFlow 全部技能（阶段、overlay、领域、工具）。无论生成还是手写都必须满足。
> 来源：DevFlow 契约 + 高星仓库蒸馏（Superpowers、anthropics/skills、awesome-claude-skills、awesome-cursorrules）。

## 1. 命名与布局

- 目录与 frontmatter `name` 一致，全小写、连字符。
- 阶段技能名前缀 `hf-`；语言标准 `<language>-coding-standards`；领域 `<domain>-development`。
- 布局：

```text
skills/<name>/
  SKILL.md            # 高频高危内容（阶段 ≤~400 行；coding-standards ≤300 行硬上限）
  references/         # 可选：低频细则、模板、契约
  evals/evals.json    # 必需：>=3 压力场景
```

## 2. Frontmatter

`description` 只写**触发条件**（含正/负触发），不总结内部流程。模式：

```yaml
description: 在 <具体场景/文件类型/症状> 时使用。<2-3 句正触发>。不适用于 <相邻负触发>。
```

证据（Superpowers writing-skills）：把 description 写成流程摘要会让模型照摘要走、跳过正文。

## 3. 每条规则三要素

1. **可判定性**：能对一段具体代码/工件裁定违规/不违规。出现"良好/合理/适当/尽量"即不合格。
2. **事故类**：防止什么真实失败（一句话，决定 severity）。
3. **正反例**：目标语言/场景的最小 ❌/✅ 对比。反例选模型真实会写出的形态，不是稻草人。

禁止形态："禁止 X"而不给替代；纯表格平铺无代码的主题节。

## 4. 反合理化表

点名具体偷懒话术 + 反驳，把违规框定为"破坏信任"而非"效率问题"：

```text
| 话术 | 现实 |
|---|---|
| 「测试全绿，所以没问题」 | 测试只证明外部行为，不替代 clean-code 自检 |
```

## 5. 自检清单

每个主题节至少一条可勾选项。完成声明必须由"通过的测试/构建输出/评审记录"支撑，而非"看起来对"。

## 6. evals

`evals/evals.json` >=3 场景，覆盖该技能最高危失败。每个场景：诱导违规的 prompt（含看似合理的理由）+ expected（应触发的拒绝/修正）+ expectations（可勾选检查点）。

## 7. 单一职责 + 范围纪律

一个技能解决一个问题。显式写"不做什么"（堵住膨胀）：一次性任务、已有文档标准、项目约定（→ AGENTS.md）、可正则强制的机械约束，不收入技能。

## 8. artifact-first 恢复

进度从工件恢复（`plan.md`、`reviews/`、`traceability.md`），不依赖聊天记忆。新会话只读工件即可续作。

## 9. 写作风格

祈使句 + 解释 why，不堆砌 `MUST`（anthropics 明确把过量 MUST 列为 smell）。前置决策树/速查表，中段示例，结尾 Common Mistakes。

## 10. 校验

- `python3 scripts/validate_harnessflow.py` 必须通过（技能清单、frontmatter、旧名残留、evals >=3、coding-standards ≤300 行、markdown 链接、agent frontmatter）。
- `python3 -m pytest tests/test_validate_harnessflow.py` 必须通过。
````

- [ ] **Step 2: 写哲学文档**

写入 `docs/harnessflow-philosophy.md`。结构：三层质量模型（SDD/TDD/Clean Code 各对应"做错事/做得不对/做得不好"三类失败）；human-on-the-loop 协作姿态；证据优于记忆；作者不自审/评审者不修/人最终把关三条硬规则；"在 SDD 范式下写 Clean Code"一句话目标。正文仿 DevFlow `docs/devflow-philosophy.md` 的论证节奏（本文给结构与要点，执行者补叙述）。

要点必须逐条出现：

- 三层表格（层 / 回答的问题 / 失败模式 / 承载技能），与 `using-hf` 第 1 段一致。
- 主流程闭环：`specify → R1 → design → R2 → tdd → R3 → ship`；缺陷旁路 `fix → tdd → R3 → ship`。
- GREEN 改行为、REFACTOR 改表达，两者不混在一个 diff。

- [ ] **Step 3: 写架构文档**

写入 `docs/harnessflow-core-architecture.md`。结构：15 技能清单（阶段 7 / overlay / 领域 2 / 工具 1）；工件约定（`features/<id>-<slug>/` 下 `spec.md`/`traceability.md`/`design.md`/`plan.md`/`reviews/`/`closeout.md`）；运行模式（attended/unattended 语义，引用设计 spec §4）；`plan.md` 作为中断恢复单一入口；subagent 角色分离（implementer 单任务+Context Pack，reviewer 独立不修）。

要点必须逐条出现：

- 15 技能名清单，与 `validate_harnessflow.py` 的 `EXPECTED_SKILLS` 一致。
- 运行模式表与 spec §4 完全一致（attended 默认 / unattended 只移除人工停顿不移除质量动作 / 同一 R 节点最多 3 轮自动返工复审后升级人裁决）。

- [ ] **Step 4: 校验文档不破坏链接 + 提交**

Run: `python3 scripts/validate_harnessflow.py`（预期仍报告"缺少技能"，属正常；确认无 markdown 链接新错误）

```bash
git add skills/coding-standards-creator/references/hf-skill-quality-contract.md docs/harnessflow-philosophy.md docs/harnessflow-core-architecture.md
git commit -m "docs: add skill quality contract, philosophy, and core architecture"
```

---

## Task 6: `using-hf` 入口技能（镜像 using-devflow）

**Files:**
- Create: `skills/using-hf/SKILL.md`
- 参考模板：`/mnt/e/workspace/devflow/skills/using-devflow/SKILL.md`（9 段结构逐段仿写）

- [ ] **Step 1: 写 `using-hf/SKILL.md`**

frontmatter 必须为触发条件式：

```yaml
---
name: using-hf
description: HarnessFlow 工作流的入口。在以下情况使用：开始一个新的开发任务、不确定当前该做规格/设计/实现中的哪一步、需要从已有工件恢复进度、或用户提到 HarnessFlow / 规范驱动开发 / 高质量开发流程时。
---
```

正文 9 段，逐段镜像 `using-devflow`，**约束内容必须逐字出现**：

**§1 HarnessFlow 是什么** — 三层质量模型表：

```text
| 层 | 回答的问题 | 失败模式（无此层时） | 承载技能 |
|---|---|---|---|
| 第一层 SDD | 做的是不是对的事？ | 需求含糊 → 模型靠猜 → 做错事 | hf-specify |
| 第二层 TDD | 功能被证明正确了吗？ | 代码未验证 → 一堆 bug 给人 | hf-tdd |
| 第三层 Clean Code | 代码本身写得好吗？ | 能跑但烂 → 难维护/审查/演进 | hf-clean-code + *-coding-standards + 领域技能 |
```

加一句目标：**在 SDD 范式下写 Clean Code，而不是仅仅能运行的代码。** 协作姿态 human-on-the-loop；每个阶段产物必须可冷读、可审查。

**§2 工作流** — ASCII 流程图：

```text
需求/任务到达 ──→ [0] 确认运行模式（见下）
    |
    v
[1] hf-specify      写 spec.md + plan.md 骨架 + 初始化 traceability.md
    |
[R1] hf-review      独立评审规格 → 记录到 reviews/ ──[人工确认]──
    v
[2] hf-design       影响组件边界时先修订 component-design-draft.md；
    |                写 design.md：职责、接口契约、错误模型、测试设计
[R2] hf-review      独立评审设计 → 记录到 reviews/ ──[人工确认]──
    v
[3] hf-tdd          细化 plan.md 任务；按测试设计逐用例 RED→GREEN→REFACTOR；
    |                默认逐任务派发 hf-implementer；叠加 hf-clean-code 与语言/领域规范
[R3] hf-review      独立评审测试与代码 → 记录到 reviews/ ──[人工确认]──
    v
[4] hf-ship         DoD 核验 + 追溯终验 + promotion 长期资产 + closeout ── 人确认关闭 ── 完成
```

评审是必经节点不是可选预审。

**§3 轻量状态机** — 不维护独立路由器或额外状态文件；`plan.md` 门禁表 + 任务状态 + `reviews/` 即状态：

```text
| 状态 | 含义 | 下一步 |
|---|---|---|
| pending | 产物就绪未评审 | 去 hf-review 执行对应 R 门禁 |
| passed | verdict 通过；attended 下还要看人工确认列 | 确认列 yes/N/A 进下一阶段；no 则呈人 |
| rework | 评审打回，有未闭环 findings | 先回作者阶段定向返工，回填 Resolution 后复审 |
```

R1 rework 默认回 hf-specify；R2 回 hf-design；R3 回 hf-tdd。同一 R 节点最多自动返工复审 3 轮，仍不通过升级人裁决。

**§4 Todo 投影规则** — 阶段节点、R 门禁节点、ship 节点是一级待办；hf-specify 完成只表示 spec/traceability/plan 骨架就绪，下一条必是 R1；TDD 内部任务不是多个人工确认节点，任务 DONE 后只要 plan.md 能唯一选下一任务就续跑；rework 不是"立刻再评审"，是先修再评审；attended 人工确认附着在 R 节点 verdict 之后。

**§5 运行模式（attended/unattended）** — 启动时先问一次，记入 plan.md 头部；恢复会话沿用，不重新猜；未明确回答按 attended：

```text
| 模式 | 行为 |
|---|---|
| attended（默认） | R 节点通过后停下呈人确认；TDD 任务间不停；可由 AI 修复的 findings 仍先自动返工复审 |
| unattended | R 节点后不停连续执行；仅在缺业务事实/规格设计不可决策/专家裁决/3 轮仍不通过时停 |
```

**关键：unattended 只移除人工停顿，不移除任何质量动作**（独立评审、记录、critical 阻塞、DoD 照做）。旁路 fix→tdd→R3→ship；阶段允许回溯并让受影响评审重做。

**§6 何时可以裁剪** — 微小修改（spec 压成 plan.md 一段验收标准、design 省略、R1/R2 合并入 R3，但 TDD/R3/clean-code 不裁）；纯重构（无需 spec/design，但行为不变测试先行且 R3 照做）；拿不准不裁剪。裁剪文档量不裁剪质量门槛。

**§7 工件约定** — 路径相对于目标组件仓库根（非会话目录；优先用户显式指定 → AGENTS.md 声明 → 当前组件仓库根）；工作项目录结构（`features/<id>-<slug>/` 下 spec.md/traceability.md/component-design-draft.md/design.md/plan.md/reviews//closeout.md）；恢复进度表（磁盘状态 → 下一步，逐条覆盖：目录不存在/spec 缺失→hf-specify；R1 rework→hf-specify 修复；spec 存在 R1 pending→hf-review R1；…→全通过 closeout 缺失→hf-ship）。工件与聊天冲突以工件为准。

**§8 行为准则** — 7 条不可协商：① 不默默补全模糊需求 ② 困惑停下不猜 ③ 方案有问题就说 ④ 强制简单 ⑤ 范围纪律 ⑥ 验证而非声称 ⑦ 作者不自审且阶段必评审。

**§9 技能地图** — 一句话 + 何时读：hf-specify/hf-design/hf-tdd/hf-clean-code/hf-review/hf-ship/hf-fix + `<language>-coding-standards`（按命名约定发现）+ 领域技能（按 description 发现）+ coding-standards-creator。语言与领域是叠加约束，自身不是流程阶段。

连接性叙述（每段开头一两句解释）仿 `using-devflow` 对应段落措辞。

- [ ] **Step 2: 校验 frontmatter + 旧名残留**

Run: `python3 -c "import importlib.util,s=importlib.util.spec_from_file_location('v','scripts/validate_harnessflow.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(m.validate_skill_frontmatter());print('legacy:', m.find_legacy_references(open('skills/using-hf/SKILL.md').read()))"`
Expected: frontmatter 无错；legacy 列表为空（确认正文未误用 hf-workflow-router/Workflow Profile 等旧词）。

- [ ] **Step 3: 提交**

```bash
git add skills/using-hf/SKILL.md
git commit -m "feat(using-hf): rewrite entry skill mirroring using-devflow (3 layers, plan.md FSM, attended/unattended)"
```

---

## Task 7: 计划收尾与基线快照

**Files:** 无新建（仅校验 + 记录）

- [ ] **Step 1: 跑全量校验测试**

Run: `python3 -m pytest tests/test_validate_harnessflow.py -v`
Expected: 11 PASS。

- [ ] **Step 2: 跑真实仓库校验并记录基线**

Run: `python3 scripts/validate_harnessflow.py 2>&1 | tee /tmp/hf-validate-baseline.txt`
Expected: 报告"缺少 14 个技能"（Plan 1 只建了 using-hf）+ 可能的旧名残留（旧技能目录仍在，Plan 4 删除）。**这是预期进度基线，非失败。** 把缺失技能清单作为 Plan 2/3 的待办输入。

- [ ] **Step 3: 提交基线记录（可选）**

如需留痕，把基线摘要补进 Plan 2 顶部"前置依赖"段，提交：

```bash
git add docs/superpowers/plans/2026-06-25-harnessflow-foundation.md
git commit -m "docs(plan): record Plan 1 baseline (validator green on fixtures; 14 skills pending)"
```

---

## Self-Review（plan 自检）

**1. Spec 覆盖：** 本计划覆盖设计 spec 的 §2.3（质量契约→Task 5）、§4（attended/unattended→Task 6 §5）、§5（using-hf 镜像→Task 6）、§7.2（校验门禁→Task 1-4）、§8 阶段 1（骨架→全部）。阶段 2-4 的技能写作由后续 Plan 2/3/4 承载，不在本计划范围（已声明）。✓

**2. 占位符扫描：** 所有代码/约束内容已给出。Task 5 的 philosophy/architecture 文档给出结构 + 必出现要点 + 模板指针（仿 devflow 同名文档），符合"内容约定"——非占位符。✓

**3. 类型/命名一致性：** `EXPECTED_SKILLS`（15）与 Task 6 §9 技能地图、Task 5 架构文档清单一致；`LEGACY_SKILL_NAMES` 不含任何 15 个保留名（已核对：hf-specify/hf-design/hf-tdd/hf-review/hf-ship/hf-fix 均不在 legacy 集）；`scenarios` 格式在"evals 约定"、Task 3 测试、Task 5 契约 §6 三处一致；`MIN_SCENARIOS=3`、`CODING_STANDARDS_MAX_LINES=300` 与契约 §1/§6 一致。✓

**4. 校验函数引用一致：** `run_all` 调用的 7 个函数（validate_markdown_links/skill_frontmatter/agent_frontmatter/skill_set/no_legacy_references/eval_json/coding_standards_length）均在 Task 1-4 定义；测试 `test_run_all_returns_empty_on_clean_repo` 构造的 clean repo 能让全部函数返回空（注意：该测试需保证 clean repo 不触发 legacy 残留——用例中技能名均为保留名，正文不含旧词，满足）。✓

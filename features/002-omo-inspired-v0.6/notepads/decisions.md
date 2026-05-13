# Decisions — Feature 002-omo-inspired-v0.6

> 跨 task 累积，按 task 时间倒序追加。轻量 ADR（不替代 `docs/decisions/` 仓库级 ADR）。

## TASK-002 — 2026-05-13T14:10Z — `tests/` 目录归属 `test_wisdom_notebook_skill.py`

- entry-id: `dec-0002`
- author: cursor cloud agent (hf-test-driven-dev TASK-002)
- decision: 把 `test_wisdom_notebook_skill.py` 落 `tests/`（与 `test_install_scripts.sh` / `test_tasks_progress_schema.py` 同位），不落 `skills/hf-wisdom-notebook/scripts/`
- alternatives-considered:
  1. `skills/hf-wisdom-notebook/scripts/test_wisdom_notebook_skill.py` — 拒绝：本测试是 SKILL.md 结构性 audit，受众是仓库 contributor / CI，不是运行时调用 hf-wisdom-notebook 的 agent
  2. 内联到 `audit-skill-anatomy.py` — 拒绝：audit 是通用 anatomy 检查，不应嵌入特定 skill 的结构断言
  3. `tests/test_wisdom_notebook_skill.py` — **选择**：与 dec-0001 同款分类逻辑
- rationale: ADR-006 D1 / D2 + dec-0001 已确立的"工具受众"判断标准
- reversibility: 高
- related-adr: ADR-006 D1 / D2
- related-decisions: dec-0001

## TASK-001 — 2026-05-13T13:55Z — `tests/` 目录归属 `tasks.progress.json` 验证脚本

- entry-id: `dec-0001`
- author: cursor cloud agent (hf-test-driven-dev TASK-001)
- decision: 把 `test_tasks_progress_schema.py` 落 `tests/`（与既有 `tests/test_install_scripts.sh` 同位），不落 `skills/hf-test-driven-dev/scripts/`
- alternatives-considered:
  1. `skills/hf-test-driven-dev/scripts/test_tasks_progress_schema.py`（skill-owned）—— 拒绝：本测试是 schema reference 的 verification，不是 hf-test-driven-dev 这个 skill 的运行时工具（agent 不会在跑 hf-test-driven-dev 时调用它）
  2. `tests/test_tasks_progress_schema.py`（仓库级测试）—— **选择**：归属"跨 skill 维护者工具"，与 `tests/test_install_scripts.sh` 一致
  3. 内联到 `audit-skill-anatomy.py`—— 拒绝：耦合度上升，且 audit 本身职责单一
- rationale: ADR-006 D1 / D2 区分 skill-owned vs cross-skill 工具时的判断标准是"工具受众"——本测试的受众是 v0.6 reviewer / CI / 后续 v0.7 runtime 集成测试者，**不是**正在执行 hf-test-driven-dev 的 agent，所以归 `tests/`
- reversibility: 高（一个文件 mv 即可）
- related-adr: ADR-006 D1 / D2

## TASK-001 — 2026-05-13T13:55Z — `tests/` 目录归属 `tasks.progress.json` 验证脚本

- entry-id: `dec-0001`
- author: cursor cloud agent (hf-test-driven-dev TASK-001)
- decision: 把 `test_tasks_progress_schema.py` 落 `tests/`（与既有 `tests/test_install_scripts.sh` 同位），不落 `skills/hf-test-driven-dev/scripts/`
- alternatives-considered:
  1. `skills/hf-test-driven-dev/scripts/test_tasks_progress_schema.py`（skill-owned）—— 拒绝：本测试是 schema reference 的 verification，不是 hf-test-driven-dev 这个 skill 的运行时工具（agent 不会在跑 hf-test-driven-dev 时调用它）
  2. `tests/test_tasks_progress_schema.py`（仓库级测试）—— **选择**：归属"跨 skill 维护者工具"，与 `tests/test_install_scripts.sh` 一致
  3. 内联到 `audit-skill-anatomy.py`—— 拒绝：耦合度上升，且 audit 本身职责单一
- rationale: ADR-006 D1 / D2 区分 skill-owned vs cross-skill 工具时的判断标准是"工具受众"——本测试的受众是 v0.6 reviewer / CI / 后续 v0.7 runtime 集成测试者，**不是**正在执行 hf-test-driven-dev 的 agent，所以归 `tests/`
- reversibility: 高（一个文件 mv 即可）
- related-adr: ADR-006 D1 / D2

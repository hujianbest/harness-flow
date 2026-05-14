# Decisions — Feature 002-omo-inspired-v0.6

> 跨 task 累积，按 task 时间倒序追加。轻量 ADR（不替代 `docs/decisions/` 仓库级 ADR）。

## TASK-007 — 2026-05-14T02:50Z — fast lane 关键词集合冻结（OQ-003 收口）

- entry-id: `dec-0005`
- author: cursor cloud agent (hf-test-driven-dev TASK-007)
- decision: fast lane 关键词集合按 spec OQ-003 + design §3.4 收口的 3 类（启用 / 停下 / 恢复 standard）冻结到 hf-ultrawork SKILL.md 与 references/fast-lane-escape-conditions.md
- alternatives-considered:
  1. 只支持英文关键词 — 拒绝：架构师可能中英混说
  2. 用 NL classifier 而非关键词列表 — 拒绝：HF 是 markdown 包，无 runtime classifier；关键词列表 host 可直接 grep
  3. 关键词列表写入 ADR-009 而非 SKILL.md — 拒绝：FR-008 + skill-anatomy 第 3 条要求 SKILL.md 是本地 contract
- rationale: 关键词集合是 fast lane 触发 / 让出的 boolean 判断面，必须可冷读 + host 可 grep；冻结后避免后续 fast lane 误触发
- reversibility: 高（增删关键词只需改 SKILL.md + reference）
- related-adr: ADR-009 D3 / D5

## TASK-006 — 2026-05-14T02:40Z — Cursor `.mdc` 集中 vs OpenCode/Claude Code 散落

- entry-id: `dec-0004`
- author: cursor cloud agent
- decision: Cursor `.mdc` 全部集中 `.cursor/rules/` 下，文件名按目录 slug 区分（如 `src-components.mdc`）；OpenCode `AGENTS.md` 与 Claude Code `CLAUDE.md` 散落到对应目录
- alternatives-considered:
  1. Cursor `.mdc` 也散落到对应目录 — 拒绝：违反 Cursor 客户端规约（`.cursor/rules/` 是 alwaysApply rule 的官方位置）
  2. OpenCode `AGENTS.md` 也集中 — 拒绝：OpenCode `directoryAgentsInjector` hook 期望按目录读
- rationale: 三客户端各自的客户端规约不同；hf-context-mesh 必须按各自规约生成
- reversibility: 中（改回需要架构师从所有目录删 .mdc 并迁回 .cursor/rules/）
- related-adr: ADR-008 D1（三客户端可移植性）

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

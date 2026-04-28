# `hf-doc-freshness-gate` Evals

## Purpose

`test-prompts.json` 包含 5 个 pressure scenarios，覆盖本 gate 的 4 verdict 词表（`pass` / `partial` / `N/A` / `blocked`）与各 next-action 路由分支，用于 reviewer subagent 派发前的回归测试。每个 scenario 与 `features/001-hf-doc-freshness-gate/spec.md` §8 FR-001..FR-008 + design §16 测试策略表 1:1 对应。

## Scenarios

| Scenario ID | 对应 FR | 期望 verdict | 期望 next |
|---|---|---|---|
| `T-FR-001-pass` | FR-001 / FR-002 / FR-005 | `pass` | `hf-completion-gate` |
| `T-FR-001-blocked-traceability` | FR-001（负路径） | `blocked` | `hf-traceability-review` |
| `T-FR-003-N-A` | FR-003 / NFR-004（sync-on-presence） | `N/A` | `hf-completion-gate` |
| `T-FR-005-partial` | FR-005（partial verdict 路径） | `partial` | `hf-completion-gate` |
| `T-FR-007-blocked-increment` | FR-007（spec ↔ commits 不一致） | `blocked` | `hf-increment` |

## 字段约定

每个 scenario 至少含：

- `id` — 唯一标识（与 design §16 测试策略表锚点一致）
- `category` — 路由类别（verdict-pass / verdict-N/A-sync-on-presence / 等）
- `fr_anchor` — 对应 spec FR/NFR 编号数组
- `scenario` — 一句话场景描述
- `setup` — profile / spec_excerpt / tasks_excerpt / commits / filesystem_state
- `expected_verdict` — 4 词表之一
- `expected_next` — 期望 next_action_or_recommended_skill
- `expected_dimensions` — 各维度子 verdict（key=维度名，value=verdict）
- `expected_record_path` — 期望 evidence 文件路径
- 可选：`expected_blocked_reason` / `expected_partial_listing` / `expected_completion_gate_handling` / `expected_evidence_marker`

## 与 HF skill 既有 evals 形态的对齐

本目录采用 `test-prompts.json`（裸 array，无 wrapper）+ `README.md` 形式，与既有 30+ HF skill 的 evals 目录形态一致（参见 `skills/hf-tasks-review/evals/` 等）。更重型 evals 适配（`evals.json` 含 wrapper + fixtures/）适合 fixture-driven skill，本 prose-only skill 不需要该完整形态。

## 如何添加新 scenario

按 `tasks.md` §10 R1 风险缓解：本 gate 在 `hf-test-driven-dev` 阶段一次完成 5 scenario；后续如需追加 scenario（例如发现新 verdict 路径或新 dimension），应通过 `hf-increment` 走范围变更流程，而非直接在本仓库追加。

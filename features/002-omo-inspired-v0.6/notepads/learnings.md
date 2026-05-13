# Learnings — Feature 002-omo-inspired-v0.6

> 跨 task 累积，按 task 时间倒序追加。Schema 见 `skills/hf-wisdom-notebook/references/notebook-schema.md`（TASK-002 起正式承接）。

## TASK-002 — 2026-05-13T14:10Z — hf-wisdom-notebook SKILL.md + 2 references 落地

- entry-id: `learn-0003`
- author: cursor cloud agent (hf-test-driven-dev TASK-002)
- pattern: "structural-grep test pattern for SKILL.md tasks": SKILL.md 类任务的 TDD verifier 用 stdlib `re` + `subprocess` 即可断言 (a) audit-skill-anatomy.py PASS (b) 必含段头 grep (c) 必含表格行计数 (d) wc -l + token budget 检查；不需要 markdown parser
- applies-to: TASK-005 (hf-gap-analyzer) / TASK-006 (hf-context-mesh) / TASK-007 (hf-ultrawork) 三个新 SKILL.md task 可直接复用同款 verifier 模板
- evidence-anchor: `tests/test_wisdom_notebook_skill.py` 9 tests PASS in 0.043s; SKILL.md 153 行 / 985 word ≈ 1281 token（远低 5000 上限）
- tags: skill-anatomy, structural-test, stdlib-pattern
- related-decisions: dec-0002

## TASK-002 — 2026-05-13T14:10Z — schema reference 必须含 dogfood 指针

- entry-id: `learn-0004`
- author: cursor cloud agent
- pattern: "schema reference 末尾给 dogfood 指针"：每个 schema reference 文档（如 `notebook-schema.md` / `tasks-progress-schema.md`）必须在文末指向真实 dogfood 实例（如 `features/002-omo-inspired-v0.6/notepads/`），便于读者从抽象 schema 跳到真实使用场景
- applies-to: 后续 v0.6 / v0.7 任何引入 JSON / markdown schema 的 reference 文档
- evidence-anchor: `skills/hf-wisdom-notebook/references/notebook-schema.md` 末段 "## 例子" + `skills/hf-test-driven-dev/references/tasks-progress-schema.md` 末段 "## Canonical positive example"

## TASK-001 — 2026-05-13T13:55Z — define tasks.progress.json schema

- entry-id: `learn-0001`
- author: cursor cloud agent (hf-test-driven-dev TASK-001)
- pattern: "stdlib-only mini JSON-Schema validator pattern" — 一个 ~30 行的 `_validate` 函数支持 type/required/properties/enum/pattern/items 子集即可校验本仓库所有手写 schema。不引入 jsonschema / pydantic 等第三方依赖与 audit-skill-anatomy.py / install.sh / test_install_scripts.sh 同等"stdlib only"约束一致
- applies-to: 后续任何 v0.6 / v0.7 SKILL.md 引入新 JSON 工件时（如 v0.7 record-evidence 输出 schema），可直接复用本验证器思路而非每次新引第三方库
- evidence-anchor: `tests/test_tasks_progress_schema.py` 的 `_validate` 函数；6 tests PASS in 0.001s

## TASK-001 — 2026-05-13T13:55Z — fixture-driven schema TDD on documentation tasks

- entry-id: `learn-0002`
- author: cursor cloud agent
- pattern: "schema-task TDD": 对纯 schema / reference 文档类任务，把 TDD 适配为 (positive fixture + N negative fixtures + tiny stdlib validator) 三件套；RED 阶段 schema doc 缺失 → file not found 错误即有效 RED；GREEN 阶段 schema doc 存在且 fixtures 通过 → 有效 GREEN
- applies-to: TASK-002 / TASK-005 / TASK-006 / TASK-007 / TASK-009 / TASK-010 等"主要产出是 SKILL.md / references/" 的任务，可以套同款 (skeleton check + reference rubric grep + Common Rationalizations 必含段) 三件套验证
- evidence-anchor: `verification/test-design-task-001.md` 的"待验证行为"4 项 + 实际 6 tests

## TASK-001 — 2026-05-13T13:55Z — define tasks.progress.json schema

- entry-id: `learn-0001`
- author: cursor cloud agent (hf-test-driven-dev TASK-001)
- pattern: "stdlib-only mini JSON-Schema validator pattern" — 一个 ~30 行的 `_validate` 函数支持 type/required/properties/enum/pattern/items 子集即可校验本仓库所有手写 schema。不引入 jsonschema / pydantic 等第三方依赖与 audit-skill-anatomy.py / install.sh / test_install_scripts.sh 同等"stdlib only"约束一致
- applies-to: 后续任何 v0.6 / v0.7 SKILL.md 引入新 JSON 工件时（如 v0.7 record-evidence 输出 schema），可直接复用本验证器思路而非每次新引第三方库
- evidence-anchor: `tests/test_tasks_progress_schema.py` 的 `_validate` 函数；6 tests PASS in 0.001s

## TASK-001 — 2026-05-13T13:55Z — fixture-driven schema TDD on documentation tasks

- entry-id: `learn-0002`
- author: cursor cloud agent
- pattern: "schema-task TDD": 对纯 schema / reference 文档类任务，把 TDD 适配为 (positive fixture + N negative fixtures + tiny stdlib validator) 三件套；RED 阶段 schema doc 缺失 → file not found 错误即有效 RED；GREEN 阶段 schema doc 存在且 fixtures 通过 → 有效 GREEN
- applies-to: TASK-002 / TASK-005 / TASK-006 / TASK-007 / TASK-009 / TASK-010 等"主要产出是 SKILL.md / references/" 的任务，可以套同款 (skeleton check + reference rubric grep + Common Rationalizations 必含段) 三件套验证
- evidence-anchor: `verification/test-design-task-001.md` 的"待验证行为"4 项 + 实际 6 tests

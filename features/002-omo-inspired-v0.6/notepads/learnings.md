# Learnings — Feature 002-omo-inspired-v0.6

> 跨 task 累积，按 task 时间倒序追加。Schema 见 `features/002-omo-inspired-v0.6/design.md` §3.1（待 TASK-002 hf-wisdom-notebook SKILL.md 上线后正式承接）。

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

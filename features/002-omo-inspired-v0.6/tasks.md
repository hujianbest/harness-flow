# HF v0.6 OMO-Inspired — Tasks

- 状态: 草稿 Round 2（2026-05-13；design Round 1 approved；tasks-review Round 1 verdict=`通过`，2 minor 已就地吸收）
- Spec basis: `spec.md` Round 2 approved
- Design basis: `design.md` Round 1 approved（含 design-review 3 条 minor 已吸收）
- 任务总数: 18（含 design M1 吸收的 1 个 schema task；不含 hf-tasks-review / 各 review / gates / finalize 这些标准节点工作）
- 拆分原则: 按 INVEST + WBS + 关键路径；每 SKILL.md 改动一个 task（除非紧密耦合需合并）

## 任务清单

| ID | 标题 | Files | Acceptance | Verify | 依赖 | 优先级 |
|---|---|---|---|---|---|---|
| **TASK-001** | 定义 `tasks.progress.json` schema（design M1 吸收） | `skills/hf-test-driven-dev/references/tasks-progress-schema.md`（新建） | (1) schema 含字段：`current_task` / `current_step`（如 `RED-1` / `GREEN-2` / `REFACTOR-1`）/ `last_updated`（ISO 8601）/ `step_history[]`（含 step + timestamp + outcome）；(2) JSON Schema 形式可机械校验；(3) hf-test-driven-dev SKILL.md Output Contract 段引用此 schema | 写出 fixture json + 用 `python3 -c "import json; json.load(open('fixture.json'))"` 校验 | 无 | MUST |
| **TASK-002** | 写 `skills/hf-wisdom-notebook/SKILL.md` + 5 文件 schema reference | `skills/hf-wisdom-notebook/SKILL.md` + `references/notebook-schema.md` + `references/notebook-update-protocol.md` | (1) audit-skill-anatomy.py PASS；(2) frontmatter 含 `name` + `description`；(3) 5 文件 schema 字段表完整（按 design §3.1）；(4) Workflow 5 步明确；(5) Common Rationalizations ≥ 3 条；(6) `wc -l skills/hf-wisdom-notebook/SKILL.md` ≤ 500（NFR-002）；(7) `wc -w` × 1.3 估算 token ≤ 5000 | `python3 scripts/audit-skill-anatomy.py --skills-dir skills` 通过 + `wc -l` + `wc -w` | 无 | MUST |
| **TASK-003** | 写 `skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py`（stdlib only） | `skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py` + `skills/hf-wisdom-notebook/scripts/test_validate_wisdom_notebook.py` | (1) `--help` 自描述；(2) 在 fixture notebook 上跑 PASS；(3) 缺文件时 FAIL；(4) 缺 delta 时 FAIL；(5) `^import` 仅 stdlib；(6) 内含至少 5 个 unit test | `python3 skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py --help` 输出 + `python3 skills/hf-wisdom-notebook/scripts/test_validate_wisdom_notebook.py` 通过 | TASK-002 | MUST |
| **TASK-004** | 写 `skills/hf-wisdom-notebook/evals/`（高风险 skill 必含） | `skills/hf-wisdom-notebook/evals/README.md` + `evals/evals.json` + `evals/fixtures/sample-notepads/` | (1) ≥ 3 eval case：正常追加 / 缺文件拒绝 / 跨 task 累积；(2) evals.json 结构合规 | 跑 evals dry-run 验证 schema | TASK-002 + TASK-003 | MUST |
| **TASK-005** | 写 `skills/hf-gap-analyzer/SKILL.md` + gap-rubric reference | `skills/hf-gap-analyzer/SKILL.md` + `references/gap-rubric.md` | (1) audit PASS；(2) Object Contract 明确"输出 .gap-notes.md，作者吸收"；(3) 6 维度 rubric 完整；(4) 显式声明非 Fagan review 节点（不写 verdict）；(5) `wc -l` ≤ 500 / token 估算 ≤ 5000 | audit + 在本 feature 自己的 spec.md 上跑一次 gap-analyzer 验证流程 | 无 | MUST |
| **TASK-006** | 写 `skills/hf-context-mesh/SKILL.md` + 3 套 AGENTS.md 模板 | `skills/hf-context-mesh/SKILL.md` + `references/agents-md-template.md`（含 OpenCode / Cursor / Claude Code 三段） | (1) audit PASS；(2) 3 套模板各自含 root / mid / leaf 三层；(3) Workflow 步骤明确；(4) Hard Gates 段含"不替架构师写约定"硬规；(5) `wc -l` ≤ 500 / token 估算 ≤ 5000 | audit + 模板可被三客户端各自 lint（OpenCode 视为 markdown / Cursor `.mdc` 校验 / Claude Code `CLAUDE.md` 视为 markdown） | 无 | MUST |
| **TASK-007** | 写 `skills/hf-ultrawork/SKILL.md` + escape-conditions reference | `skills/hf-ultrawork/SKILL.md` + `references/fast-lane-escape-conditions.md` | (1) audit PASS；(2) Hard Gates 段直接 enumerate 5 类不可压缩项（FR-008 强制）；(3) 关键词集合表（OQ-003 收口）；(4) escape conditions 6 项（按 ADR-009 D3 第 4 项）；(5) Workflow 5 步含 "verdict 后检查 escape 条件"；(6) Common Rationalizations 含"试图绕 review/gate"反驳；(7) `wc -l` ≤ 500 / token 估算 ≤ 5000 | audit + 写一份"假设场景"测试：模拟 review verdict=阻塞 时 SKILL.md 描述能否触发 escape | TASK-001 | MUST |
| **TASK-008** | 写 `skills/hf-ultrawork/evals/`（高风险 skill 必含） | `skills/hf-ultrawork/evals/README.md` + `evals/evals.json` | (1) ≥ 3 eval case：正常 fast lane 推进 / escape 触发 / approval 自动写工件；(2) evals.json 合规 | 跑 evals dry-run | TASK-007 | MUST |
| **TASK-009** | 修改 `skills/hf-tasks-review/SKILL.md` + 新增 momus-rubric reference（FR-005） | `skills/hf-tasks-review/SKILL.md` + `references/momus-rubric.md` | (1) audit PASS；(2) momus 4 维 + 阈值（100/90/80/100/0）；(3) `verdict: rejected-rewrite` + N=3 上限；(4) 第 4 次自动升级（fast lane escape）；(5) Common Rationalizations 含"差 1% 也是不达标"反驳 | audit + 在本 feature 自己的 tasks.md（即本文件）上跑一次 momus rubric 演练 | 无 | MUST |
| **TASK-010** | 修改 `skills/hf-specify/SKILL.md` + 新增 interview-fsm + spec-intake-template references（FR-006） | `skills/hf-specify/SKILL.md` + `references/interview-fsm.md` + `references/spec-intake-template.md` | (1) audit PASS；(2) FSM 5 状态图（含 ClearanceCheck → Research / Interview 回退）；(3) `spec.intake.md` schema 完整；(4) Workflow 引用 FSM | audit + 给一个 fixture spec.intake.md，反向恢复"上次问到第几问"演练 | 无 | MUST |
| **TASK-011** | 修改 `skills/hf-workflow-router/SKILL.md` + transition-map + workflow-shared-conventions（FR-003 / FR-010 / FR-015） | `skills/hf-workflow-router/SKILL.md` + `references/profile-node-and-transition-map.md` + `references/workflow-shared-conventions.md` | (1) audit PASS；(2) step-level recovery 段（消费 tasks.progress.json）；(3) category_hint handoff 字段 + 下游忽略容错；(4) wisdom_summary 注入；(5) workflow-shared-conventions 新增 progress.md `## Fast Lane Decisions` schema | audit + 给 fixture handoff JSON 验证 schema | TASK-001 + TASK-002 | MUST |
| **TASK-012** | 修改 `skills/hf-code-review/SKILL.md` + 新增 ai-slop-rubric reference（FR-011） | `skills/hf-code-review/SKILL.md` + `references/ai-slop-rubric.md` | (1) audit PASS；(2) rubric 含禁用模式（regex 形式可 grep）；(3) 例外段（README / docs / test assertion）；(4) SKILL.md "Comment 质量" 子节引用 rubric | audit + 用 rubric 跑 grep 在仓库已有代码上确认无误报 | 无 | MUST |
| **TASK-013** | 修改 `skills/using-hf-workflow/SKILL.md`（FR-009 4 子项） | `skills/using-hf-workflow/SKILL.md` | (1) audit PASS；(2) 步骤 5 entry bias 表新增 fast lane 一行；(3) 步骤 3 不变（diff 验证）；(4) 步骤 6 不变；(5) 不动其它步骤 | audit + git diff 确认仅步骤 5 表格改动 | TASK-007 | MUST |
| **TASK-014** | 修改 `skills/hf-test-driven-dev/SKILL.md` Output Contract 集成 wisdom-notebook（FR-002 集成点）+ tasks.progress.json 集成（TASK-001 衍生） | `skills/hf-test-driven-dev/SKILL.md` | (1) audit PASS；(2) Output Contract 段含 5 文件容器约束 + delta 至少 learnings/verification 任一；(3) Hard Gates 段含"不写 wisdom notebook delta = task 未完成"；(4) Output Contract 段含 tasks.progress.json 写入要求 | audit + diff 验证仅 Output Contract / Hard Gates 段改动 | TASK-001 + TASK-002 | MUST |
| **TASK-015** | 修改 `skills/hf-completion-gate/SKILL.md` 集成 validate-wisdom-notebook.py（FR-002 集成点） | `skills/hf-completion-gate/SKILL.md` | (1) audit PASS；(2) Workflow closeout 前置检查新增"validate-wisdom-notebook.py 通过"项；(3) 校验失败 → gate verdict = FAIL，回 hf-test-driven-dev | audit + diff 验证仅 Workflow 段改动 | TASK-003 + TASK-014 | MUST |
| **TASK-016** | 文档刷新（FR-013）：README / soul.md 中 v0.6+ 计划末段措辞改为 "out-of-scope" | `README.md` + `README.zh-CN.md` + `docs/principles/soul.md` | (1) `grep -n 'hf-shipping-and-launch' README.md README.zh-CN.md docs/principles/soul.md` 仅出现在 "已删除 / out-of-scope" 语境；(2) skill 总数 24 → 28 在 README 同步更新（仅 hf-* 数字；不动 closeout HTML 段）；(3) soul.md 现状脚注更新指向 ADR-008 D1 | grep + 三客户端 install 后文档可读 | 全部 task 完成后做 | MUST |
| **TASK-017** | CHANGELOG.md 更新（FR-014）：v0.6 scope 总结 | `CHANGELOG.md`（已有 v0.6 路线图条目，本 task 补完整 v0.6 scope） | (1) `[Unreleased]` 段新增 "v0.6 author-side + fast lane scope 落地" 条目，列出 11 SKILL.md 改动 + 1 script + 1 schema | grep `v0.6` + 人工 review | TASK-001 ~ TASK-015 | MUST |
| **TASK-018** | 三客户端 install + 跨客户端 fast lane 端到端验证（NFR-004 + NFR-006 + HYP-002）| `verification/e2e-three-client-2026-05-13.md` + `verification/markdown-only-fast-lane-2026-05-13.md` | (1) Cursor / OpenCode / Claude Code 三客户端各装一次本 feature 分支；(2) 每客户端验证 4 新 + 7 改 SKILL.md 全部可识别；(3) 在某客户端跑本 feature 自己 dogfood fast lane 全程，验证不打断推到 hf-finalize；(4) HYP-002 PASS 证据落 verification record；(5) verification record 必须含：每客户端 `find <vendored>/skills -mindepth 2 -maxdepth 2 -name SKILL.md` 输出 + `git diff --name-only main..HEAD skills/{7 modified skills}/SKILL.md` 输出 + fast lane progress.md `## Fast Lane Decisions` 段当前文本 + 任一 escape 触发的复现尝试 | 端到端测试脚本输出 | 全部 task 完成后做 | MUST |

## 依赖图

```
TASK-001 (tasks.progress.json schema)
  ↓
  ├─ TASK-007 (hf-ultrawork) ─→ TASK-008 (ultrawork evals) + TASK-013 (using-hf-workflow)
  └─ TASK-011 (hf-workflow-router)

TASK-002 (hf-wisdom-notebook SKILL.md) ─→ TASK-003 (validate-wisdom-notebook.py) ─→ TASK-004 (notebook evals)
  └─ TASK-011 (router 消费 wisdom_summary)
  └─ TASK-014 (hf-test-driven-dev 集成)
                                    ↓
                                  TASK-015 (hf-completion-gate 集成 validator)

独立任务（无依赖）：
TASK-005 (hf-gap-analyzer) / TASK-006 (hf-context-mesh) / TASK-009 (hf-tasks-review momus) /
TASK-010 (hf-specify FSM) / TASK-012 (hf-code-review ai-slop)

收尾任务（依赖大部分完成）：
TASK-016 (文档刷新) / TASK-017 (CHANGELOG) / TASK-018 (三客户端 e2e)
```

## 关键路径

`TASK-001 → TASK-002 → TASK-003 → TASK-014 → TASK-015 → TASK-018`

并行路径（可同时推进）：
- TASK-005 / TASK-006 / TASK-009 / TASK-010 / TASK-012 / TASK-013 与关键路径并行
- 收尾 TASK-016 / TASK-017 在所有 SKILL.md 改完后做

## Definition of Done（DoD，每 task 通用）

- [ ] 所有列出 file 的实际改动落盘
- [ ] Acceptance 全部 PASS
- [ ] Verify 命令 PASS
- [ ] `audit-skill-anatomy.py` 不引入新 fail
- [ ] wisdom notebook delta 已写（按 FR-002）
- [ ] git diff 范围与 Files 列一致（无越界改动）
- [ ] 不修改宪法层 docs（soul.md / methodology-coherence.md / skill-anatomy.md，但 TASK-016 是 soul.md 现状脚注更新例外，仅改"现状脚注"段不动其它）

## Router 重选规则

- Current Active Task 锁定为 TASK-001（关键路径起点，无依赖）
- TASK-001 完成后 router 重选下一无依赖未完成 task
- 并行任务允许多 session 同时领取，但每 session 一个 Current Active Task

## Open Questions（hf-tasks-review 时）

- OQ-T1：TASK-018 三客户端 e2e 是否要在不同物理 host 跑？还是同 cloud agent 跑 3 次模拟？建议后者（cost-effective）
- OQ-T2：TASK-009 momus rubric 在本 feature 自己的 tasks.md 上演练，是否需要单写 dry-run record？建议合并到 TASK-009 verification 里

## 关联

- Spec: `spec.md` Round 2
- Design: `design.md`
- ADRs: ADR-008 / ADR-009 / ADR-010
- Spec review: Round 1 + Round 2
- Design review: Round 1

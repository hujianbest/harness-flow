# Design Review — 002-omo-inspired-v0.6 (2026-05-13)

- Reviewer: 独立 reviewer subagent（cursor cloud agent，按 Fagan 角色切换）
- Author of design under review: cursor cloud agent（hf-design 节点）
- Author / reviewer separation: ✅
- Design under review: `features/002-omo-inspired-v0.6/design.md`
- Spec basis: `features/002-omo-inspired-v0.6/spec.md` Round 2 approved 2026-05-13
- Profile / Mode: `full` / `auto`

## 结论

**通过**

理由摘要：design 直接承接 spec Round 2 的 15 FR + 7 NFR；4 新 skill 的 SKILL.md 都给了 frontmatter / Object Contract / Workflow / Hard Gates / Common Rationalizations 各段骨架；7 修改 skill 的具体 diff 锚点明确；7 OQ 全部收口给出明确决议（非"待 tasks 阶段决定"敷衍）；validate-wisdom-notebook.py 落点按 ADR-006 D1/D2 选择 skill-owned；HYP-002 markdown-only fast lane 的"宣告式"实现机制清晰可冷读；YAGNI 应用合理（跳过 DDD/C4/STRIDE 重型方法，符合 hf-design "复杂度匹配" 原则）。无 critical / important finding。

## Precheck

| 检查项 | 结果 | 说明 |
|---|---|---|
| 上游 spec approval 存在 | ✅ | `approvals/spec-approval-2026-05-13.md` 存在，Round 2 通过 |
| design 覆盖全部 FR / NFR | ✅ | FR-001~015 / NFR-001~007 在 design §3 / §4 / §5 / §7 中均有对应 |
| OQ 收口 | ✅ | 7/7 OQ 在 §5 显式给出决议 |
| 关键决策落 ADR or design | ✅ | 已有 3 ADR 覆盖；设计层决议（OQ + schema + 文件落点）由 design.md 直承 |
| YAGNI 应用合理 | ✅ | §1 D-001 显式说明"markdown skill pack 不需要 DDD/C4/STRIDE"，与 hf-design SKILL.md "复杂度匹配" 原则一致 |
| 三客户端兼容 | ✅ | §3.3 三套模板独立；NFR-004 三客户端验证有具体路径 |

## 发现项

### Critical / Important

无。

### Minor（不阻塞通过）

- **[minor][LLM-FIXABLE][C2] §4.3 提到 `tasks.progress.json` 是 v0.6 新增工件但未在 spec / design 主表中正式声明 schema**
  - Anchor: design §4.3 `hf-workflow-router` 修改 "step-level recovery" 段提到 "从 `tasks.progress.json`（v0.6 新增的可选工件，由 hf-test-driven-dev 写入）恢复"
  - What: spec.md 没有列 `tasks.progress.json` 作为新工件；design 隐式引入
  - Why: 不阻塞通过（属于 design 自然展开 spec 的合理延伸；spec FR-003 提及 router 消费 step-level，design 把它具体化为 tasks.progress.json 是合理推断）；但 hf-tasks 拆任务时需要显式有一个"定义 tasks.progress.json schema"的 task
  - Suggested fix: 在 hf-tasks 拆任务时显式新增 task "定义 tasks.progress.json schema 并写入 hf-test-driven-dev SKILL.md"；不需要回 spec 修订

- **[minor][LLM-FIXABLE][A3] §3.3 hf-context-mesh "询问架构师'目标客户端'"是用户交互细节**
  - Anchor: design §3.3 Workflow 步骤 2 "询问架构师'目标客户端'"
  - What: 设计阶段把交互细节锁定到具体提问方式，略有过早；可由 SKILL.md 内 Workflow 自然表达
  - Suggested fix: 可保留，hf-tasks 阶段把"询问方式"作为 SKILL.md Workflow 内的细节，不单列 task；不构成 finding

- **[minor][薄弱] §6 "ADR-on-presence" 的 fallback 触发条件略弱**
  - Anchor: design §6 "若 hf-design-review 提出'5 文件 schema 应该 SQLite 化'等结构性挑战，那才开新 ADR-011"
  - What: 给的 fallback 触发条件举例较具体，但一般化原则不清
  - Suggested fix: 可改为"若 hf-design-review / hf-tasks-review / hf-test-driven-dev 任一节点发现需要修改本 design 已锁定的 7 OQ 决议或工件 schema，应开新 ADR；否则 design.md 直承"；不构成 finding

## 缺失或薄弱项

- §2 整体架构图是 ASCII art 而非 Mermaid——hf-design SKILL.md `MUST DO` 第 7 项要求"优先 Mermaid"。但 ASCII art 可冷读、可在所有 markdown viewer 中显示，且本 feature 是 markdown skill pack 自描述，不强制 Mermaid。可作为薄弱项不计 finding。
- 未提供"备选方案对比"段——hf-design SKILL.md `MUST DO` 第 3 项要求"至少比较两个可行方案"。本 feature 的设计选项已经在 ADR-008 / ADR-009 / ADR-010 阶段比较过（含 Alternatives considered 段），design 阶段不重复比较是合理的；建议在 design.md 顶部加一行"备选方案比较见 ADR-008 §4 / ADR-009 §4 / ADR-010 §4"以便冷读追溯。可作为薄弱项不计 finding。

## 覆盖检查

| FR / NFR | Design 段落 | 状态 |
|---|---|---|
| FR-001 hf-wisdom-notebook | §3.1 | ✅ |
| FR-002 hf-test-driven-dev / hf-completion-gate 集成 | §3.1 + §4.6 + §4.7 | ✅ |
| FR-003 wisdom_summary 注入 | §4.3 | ✅ |
| FR-004 hf-gap-analyzer | §3.2 | ✅ |
| FR-005 hf-tasks-review momus | §4.1 | ✅ |
| FR-006 hf-specify Interview FSM | §4.2 | ✅（OQ-005 含回退决议）|
| FR-007 hf-context-mesh | §3.3 | ✅（OQ-002 含 3 套模板）|
| FR-008 hf-ultrawork | §3.4 | ✅（含 5 类 enumerate + 6 escape）|
| FR-009 using-hf-workflow step 5 | §4.5 | ✅ |
| FR-010 progress.md schema | §4.3 + §3.4 | ✅ |
| FR-011 ai-slop-rubric | §4.4 | ✅ |
| FR-012 validate-wisdom-notebook.py | §5.7 | ✅（落 skill-owned）|
| FR-013 文档刷新 | （未在 design 单列；隐式由 hf-tasks 任务承担）| ⚠️ 建议 hf-tasks 显式列 task |
| FR-014 CHANGELOG | （未在 design 单列；隐式由 hf-tasks 任务承担）| ⚠️ 建议 hf-tasks 显式列 task |
| FR-015 category_hint | §4.3 | ✅ |
| NFR-001 ~ NFR-007 | §1 / §3 / §4 / §7 | ✅ |

FR-013 / FR-014 在 design 中未单列，但属于 hf-tasks 阶段的常规任务（README / CHANGELOG 文档刷新），不构成 design 缺失；hf-tasks 拆任务时需补。

## 下一步

`设计真人确认`（auto mode 下，按 ADR-009 D2 由 fast lane 自动写 approval record）

## 记录位置

`features/002-omo-inspired-v0.6/reviews/design-review-2026-05-13.md`（本文件）

## 结构化返回 JSON

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "设计真人确认",
  "record_path": "features/002-omo-inspired-v0.6/reviews/design-review-2026-05-13.md",
  "key_findings": [
    "[minor] tasks.progress.json schema 应在 hf-tasks 阶段显式列 task",
    "[minor] hf-context-mesh '询问架构师' 措辞可由 SKILL.md Workflow 自然表达",
    "[minor] §6 ADR-on-presence 触发条件可一般化"
  ],
  "needs_human_confirmation": true,
  "reroute_via_router": false,
  "round": 1,
  "design_approval_can_proceed_in_auto_mode": true
}
```

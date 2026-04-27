---
name: mwf-specify
description: Use when the team已经接受了一条 IR / SR / AR 或 DTS / 变更请求作为输入、当前需要把它澄清成可设计的需求规格、AR 边界 / 待决问题 / 验收标准仍需收敛、或 mwf-spec-review 把规格退回需要修订。Not for product discovery / 决定要不要做某个需求（mwf 不承担产品发现，回需求负责人）, not for designing the AR implementation (→ mwf-ar-design), not for component implementation design (→ mwf-component-design), not for hotfix reproduction / root cause (→ mwf-problem-fix).
---

# mwf 需求规格澄清

把团队已经接受的需求输入（IR / SR / AR / DTS 摘要 / 变更请求）澄清成可被 `mwf-spec-review` 评审、能直接喂给 `mwf-ar-design` 的需求规格对象。

本 skill 不做产品发现、不创造需求方向、不替需求负责人决定优先级；当输入不清且涉及方向 / 范围 / 验收标准时，只整理待决问题列表，回需求负责人。

## When to Use

适用：

- 已有 IR / SR / AR 或 DTS / 变更请求，但需求规格尚不足以进入 AR 实现设计
- AR 范围、所属组件、SR / IR 追溯关系、验收标准仍需澄清
- `mwf-spec-review` 返回 `需修改` / `阻塞`，需按 findings 修订规格
- 用户说"先把这个 AR 的需求理清楚"

不适用 → 改用：

- 仍在判断该需求是否值得做 → 不属于 mwf，回需求负责人
- 已有可设计规格，要写 AR 实现设计 → `mwf-ar-design`
- 已有可设计规格，要写组件实现设计 → `mwf-component-design`
- 紧急缺陷的复现 / 根因 → `mwf-problem-fix`
- 阶段不清 / 证据冲突 → `mwf-workflow-router`

## Hard Gates

- 需求规格通过 `mwf-spec-review` 之前，不得进入 `mwf-component-design` 或 `mwf-ar-design`
- 不得替需求负责人 / 模块架构师创造业务规则、优先级或验收阈值
- AR 必须有唯一所属组件；不唯一时阻塞，回需求负责人
- IR / SR / AR 追溯关系冲突 → 阻塞，回需求负责人
- 不把待决问题只藏在正文里，必须显式列在「Open Questions」章节
- 未经 `using-mwf-workflow` / `mwf-workflow-router` 入口判断 → 先回 router

## Object Contract

- Primary Object: requirement specification model（一个 work item 的需求规格）
- Frontend Input Object: 已接受的 IR / SR / AR / DTS / 变更请求 + 团队既有输入文档 + 当前组件仓库的 `docs/component-design.md`（如存在）
- Backend Output Object: `features/<id>/requirement.md` 草稿 + `features/<id>/traceability.md` 骨架 + `features/<id>/progress.md` canonical 字段同步
- Object Transformation: 把团队已接受的输入澄清为可设计的需求规格对象（含范围 / 非范围 / 验收 / 待决问题 / IR-SR-AR 追溯）
- Object Boundaries: 不写设计 / 不写代码 / 不修改既有组件实现设计 / 不重新决定要不要做这个需求
- Object Invariants: AR ID、所属组件、SR / IR 追溯、当前轮范围在 spec-review 通过前保持稳定

## Methodology

- **Requirements Traceability**: 显式建立 IR -> SR -> AR 链路；DTS 修改若涉及功能需求时建立 DTS -> AR -> SR 反向锚点
- **Scope / Non-Scope / Acceptance Criteria**: 规格按"做什么 / 不做什么 / 怎样算完成"组织
- **Socratic Elicitation**: Capture → Challenge → Clarify 三段式提问，先收敛范围 / 角色 / 成功标准，再收敛边界细节
- **Embedded Domain Awareness**: 嵌入式语境中识别可能影响 AR 设计的内存 / 实时性 / 资源约束（写为 NFR 不写实现），并指向 `docs/component-design.md` 的相关章节
- **Team Role Discipline**: 业务方向 / 优先级 / 验收阈值留给需求负责人 / 模块架构师；本节点只澄清，不拍板

## Workflow

1. 对齐最少必要上下文
   - Object: 需求规格输入证据基线
   - Method: Requirements Traceability + Read-On-Presence
   - Input: 用户最新请求 / IR / SR / AR / DTS 摘要、团队 `AGENTS.md` 路径映射、`features/<id>/progress.md`（若已存在）、当前组件仓库的 `docs/component-design.md` / `docs/ar-designs/`（若存在）
   - Output: 已锁定输入的清单 + 已识别的输入差距
   - Stop / continue: 工件冲突或不确定本次是 AR 还是 DTS → 回 `mwf-workflow-router`

2. 初始化或对齐 work item 目录
   - Object: `features/<Work Item Id>-<slug>/` 骨架
   - Method: Artifact Layout（mwf-principles 03）
   - Input: Work Item Type、Work Item ID、所属组件、`AGENTS.md` 模板覆盖
   - Output:
     - 新 work item：按 `templates/mwf-work-item-readme-template.md` 创建 `README.md`、按 `templates/mwf-progress-template.md` 创建 `progress.md`、按 `templates/mwf-traceability-template.md` 创建 `traceability.md`
     - 已存在 work item：核对 `progress.md` 的 canonical 字段是否完整
   - Stop / continue: 缺 work item ID 或所属组件 → 阻塞，回需求负责人

3. 澄清需求（Capture → Challenge → Clarify）
   - Object: 待澄清需求条目集合
   - Method: Socratic Elicitation
   - Input: 输入清单 + 团队既有上下文
   - Output: 已锁定的范围 / 非范围 / 验收 / 待决问题
   - Stop / continue: 至少覆盖以下提问面（已覆盖的跳过，不重复追问）：
     1. 用户、目标、成功标准、非目标
     2. 核心行为与触发条件
     3. 边界、异常路径、失败处理
     4. 接口、依赖、兼容性、跨组件影响
     5. 嵌入式相关 NFR（实时性 / 内存 / 资源 / 错误处理）
     6. 待澄清术语与 assumption

   每轮结束前总结已锁定与待确认；只剩 1-2 个阻塞事实时合并问；若需要问 ≥3 轮且全部依赖业务判断 → 阻塞，回需求负责人。

4. 整理 requirement rows
   - Object: 结构化需求条目
   - Method: Scope / Non-Scope / Acceptance Criteria
   - Input: 步骤 3 已锁定内容
   - Output: requirement.md 中的 rows，至少含字段：
     - `ID`（例 `FR-001`、`NFR-001`、`CON-001`、`IFR-001`、`ASM-001`、`EXC-001`）
     - `Statement`（可观察、可判断的语句）
     - `Acceptance`（可验证条件，至少 1 条）
     - `Source / Trace Anchor`（指向 IR / SR / AR / DTS 编号或具体输入文档）
     - `Component Impact`（是否触及组件接口 / 依赖 / 状态机；若触及，标注「需进入 component-impact route」）
   - Stop / continue: 任一核心 rows 缺 Acceptance → 回步骤 3

5. 草拟规格文档
   - Object: `features/<id>/requirement.md`
   - Method: Template-Constrained
   - Input: 步骤 4 rows + 团队 `AGENTS.md` 模板覆盖
   - Output: requirement.md 含至少以下章节：
     - **Identity**：Work Item Type / ID、所属组件、IR / SR / AR、Owner、当前 profile（暂记 router 决定的值）
     - **Background And Goal**：业务背景、本次开发目标、为什么做（不写方案）
     - **Scope / Non-Scope**：范围内 / 范围外
     - **Requirement Rows**：步骤 4 表
     - **Acceptance Criteria**：可验证项总览
     - **Embedded NFR**（如适用）：实时性 / 内存 / 资源 / 错误处理 / 安全
     - **Component Impact Assessment**：本需求是否影响 SOA 接口 / 组件依赖 / 状态机；指向 `docs/component-design.md` 的相关章节
     - **Open Questions**：阻塞 / 非阻塞分类
     - **Assumptions And Dependencies**
   - Stop / continue: 模板字段缺失或与 `AGENTS.md` 模板冲突 → 优先按 `AGENTS.md` 走

6. 同步 traceability 与 progress
   - Object: traceability.md、progress.md
   - Method: Requirements Traceability
   - Input: requirement rows + 上下游锚点
   - Output:
     - `features/<id>/traceability.md`：填入 IR / SR / AR 列以及当前已知设计 / 代码 / 测试占位
     - `features/<id>/progress.md`：`Current Stage = mwf-specify`、`Next Action Or Recommended Skill = mwf-spec-review`、`Pending Reviews And Gates = spec-review`、Last Updated 时间戳
   - Stop / continue: progress 字段不能用自由文本

7. 评审前自检
   - Object: 自检清单
   - Method: 静态检查
   - Input: requirement.md、traceability.md
   - Output: 自检通过 / 失败
   - Stop / continue: 任一失败 → 回步骤 4 / 5；全过 → 进入步骤 8

   自检项：

   - 业务背景、目标、用户清晰
   - 范围 / 非范围显式
   - 核心 FR / NFR 至少含 ID / Statement / Acceptance / Source
   - Embedded NFR（若适用）已写出阈值或可判定条件
   - Component Impact Assessment 显式给出「是否影响组件边界」
   - Open Questions 已分类为阻塞 / 非阻塞，阻塞项已闭合或显式回需求负责人
   - traceability.md 至少含 IR / SR / AR 行

8. Handoff
   - Object: review 派发请求
   - Method: Reviewer Dispatch（mwf-workflow-router/references/reviewer-dispatch-protocol.md）
   - Input: requirement.md 路径、supporting context
   - Output:
     - feature `progress.md` 已更新
     - feature `README.md` 中 Process Artifacts 表 Requirement 行更新
     - 父会话派发独立 reviewer subagent 执行 `mwf-spec-review`，不内联评审
   - Stop / continue: 自检未过 → 不伪造 handoff，明确写出仍缺什么

## Output Contract

完成时产出：

- `features/<Work Item Id>-<slug>/requirement.md`（团队 `AGENTS.md` 覆盖路径优先）
- `features/<Work Item Id>-<slug>/traceability.md`（IR / SR / AR 行至少初始化）
- `features/<Work Item Id>-<slug>/progress.md` 已同步：
  - `Current Stage` = `mwf-specify`
  - `Pending Reviews And Gates` 含 `spec-review`
  - `Next Action Or Recommended Skill` = `mwf-spec-review`
- `features/<Work Item Id>-<slug>/README.md` 中 Requirement 行更新

handoff 摘要（按 mwf-shared-conventions 字段）：`work_item_id`、`owning_component`、`artifact_paths`、`traceability_links`、`blockers`（如有 USER-INPUT 阻塞项）、`next_action_or_recommended_skill = mwf-spec-review`。

未达评审门槛时不伪造 handoff；明确仍缺什么。

## Red Flags

- 把用户输入的自然语言需求直接当 requirement rows
- 越过模块架构师，自行决定组件归属
- 把"以后再做"只留在 prose 而无 Open Questions / 非范围
- 缺 Acceptance 却声称需求清晰
- 把实现细节（接口签名、表结构、数据结构）写进 Statement
- AR 影响 SOA 接口却不在 Component Impact Assessment 中标注
- 把 USER-INPUT 阻塞项当 LLM-FIXABLE 自我硬补
- 不更新 progress.md 就声称交接

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 直接抄输入文档作为 requirement.md | 重新拆成 rows + 显式 Acceptance |
| 含糊的 NFR（"足够快"） | 改成可判定阈值或回需求负责人补阈值 |
| 误把组件设计修订写进 requirement.md | 仅在 Component Impact Assessment 标注，由 router 决定是否进入 `mwf-component-design` |

## Verification

- [ ] `features/<id>/requirement.md` 已落盘
- [ ] 业务背景、目标、范围、非范围、Acceptance Criteria 已写清
- [ ] 核心 FR / NFR 具备 ID / Statement / Acceptance / Source
- [ ] Embedded NFR（若适用）含阈值或可判定条件
- [ ] Component Impact Assessment 已显式判断
- [ ] Open Questions 已分类为阻塞 / 非阻塞，阻塞项已闭合或回需求负责人
- [ ] traceability.md 至少含 IR / SR / AR 行
- [ ] progress.md 已按 canonical schema 同步，下一步为 `mwf-spec-review`
- [ ] feature README 中 Requirement 行已更新

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/requirement-rows-contract.md` | requirement rows 最小字段约定 + 嵌入式 NFR 写法示例 |
| `skills/templates/mwf-work-item-readme-template.md` | work item README 模板 |
| `skills/templates/mwf-progress-template.md` | progress.md 模板 |
| `skills/templates/mwf-traceability-template.md` | traceability.md 模板 |
| `skills/docs/mwf-workflow-shared-conventions.md` | 工件路径、canonical 字段、handoff 字段 |
| `docs/mwf-principles/03 artifact-layout.md` | requirement.md 必含项 |

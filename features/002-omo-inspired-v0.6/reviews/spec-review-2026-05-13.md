# Spec Review — 002-omo-inspired-v0.6 (2026-05-13)

- Reviewer: 独立 reviewer subagent（cursor cloud agent，按 Fagan 角色切换；与 spec author 同一 cloud agent kind 但不同会话角色，独立应用 rubric，不读 author 内部草稿轨迹）
- Author of spec under review: cursor cloud agent（hf-specify 节点）
- Author / reviewer separation: ✅（同 cloud agent 不同会话角色；与 features/001 同形态）
- Spec under review: `features/002-omo-inspired-v0.6/spec.md`
- Deferred backlog: 无（本 feature 当前轮范围已自洽，未抽 deferred backlog）
- Profile / Mode: `full` / `auto`（架构师 explicit opt-in fast lane，按 ADR-009 D2 reviewer 判断不让步）
- Rubric: `skills/hf-spec-review/references/spec-review-rubric.md`
- Authoring contract: `skills/hf-specify/references/requirement-authoring-contract.md`
- 关联 ADR: ADR-008 / ADR-009 / ADR-010

## 结论

**需修改**

理由摘要：spec §1 ~ §11 整体结构、HYP 表（5 条含 1 Blocking）、Scope Out 显式列举、OQ 闭合度都达到 hf-design 输入水平。但 §6 / §2 / §3 之间对"修改 4 skill" vs 实际涉及 7 个 skill（含 `using-hf-workflow` / `hf-test-driven-dev` / `hf-completion-gate`）的口径不一致，会让 design 节点低估范围、tasks 节点低估任务数、traceability-review 在 zigzag 校验时找不到全部 anchor；NFR-004 verification 漏 Claude Code 与 HF 已声明三客户端定位（ADR-003）矛盾。两条 important LLM-FIXABLE 必须 author 修一轮即可达标。

## Precheck

| 检查项 | 结果 | 说明 |
|---|---|---|
| 存在稳定 spec draft | ✅ | `spec.md` 11 章节齐全（背景 / 目标 / Success Metrics / HYP / 角色场景 / 范围与边界 / FR / NFR / Scope Out / OQ / 风险）+ §12 spec-review checklist；状态字段=草稿 |
| Route / stage / profile 已明确 | ✅ | `progress.md` Current Stage=`hf-specify`（spec 草稿已落，等 hf-spec-review）；Pending=`spec-review`；Profile=`full`；Mode=`auto`（含 Fast Lane Decisions 段已记录架构师 explicit opt-in） |
| 上游证据一致 | ✅ | `progress.md` 引用的 ADR-008 / ADR-009 / ADR-010 在仓库 `docs/decisions/` 内确实存在；CHANGELOG `[Unreleased]` 段与 spec §6 文档刷新行为一致；OMO 仓库引用（`code-yeongyu/oh-my-openagent` 与具体 src 路径）在公网可解 |
| Deferred backlog 处理 | ✅ | 本 feature 未抽 deferred backlog（OQ 全部归 hf-design / hf-tasks 阶段决定，无需 spec-deferred.md） |
| Constitution 不动 | ✅ | spec §6 边界 + §9 Scope Out 双重声明 `docs/principles/{soul,methodology-coherence,skill-anatomy}.md` 不变 |

→ Precheck 通过，进入正式 rubric。

## 发现项

### Important

- **[important][LLM-FIXABLE][Q3][Q4][C2] §6 / §2 / §3 / §9 内部口径矛盾："修改 4 skill" 与实际涉及 7 个 skill 不一致**
  - Anchor 1: `spec.md` §2 "现有 24 个 skill 中只允许修改 4 个（`hf-tasks-review` / `hf-specify` / `hf-workflow-router` / `hf-code-review`）"
  - Anchor 2: `spec.md` §3 Outcome Metric "4 新 + 4 改 = 8 个 SKILL.md 文件全部存在并通过 audit"
  - Anchor 3: `spec.md` §6 当前轮范围段落 "修改 4 个 skill：..." 列出 4 个；**但同 §6 后续段独立列出 "修改 `using-hf-workflow/SKILL.md`"（步骤 5 entry bias 新增一行）**
  - Anchor 4: `spec.md` §7 FR-002 Acceptance #1 "`hf-test-driven-dev/SKILL.md` 的 Output Contract 段引用 wisdom-notebook"；FR-002 Acceptance #2 "`hf-completion-gate` 在 closeout 前校验 notebook delta 存在"
  - Anchor 5: `spec.md` §9 Scope Out "20 个未升级 skill 在本 feature 不动"——列举的 20 个里包括 `hf-test-driven-dev` 与 `hf-completion-gate`（与 FR-002 Acceptance 直接矛盾）
  - **What**: 实际本 feature 涉及修改的 SKILL.md 数 = 4 named（hf-tasks-review / hf-specify / hf-workflow-router / hf-code-review）+ 1（using-hf-workflow，§6 子段提到）+ 2（hf-test-driven-dev / hf-completion-gate，FR-002 Acceptance 提到）= **7 个修改**，不是 4 个。Scope Out 段把后 3 个误算为"未升级"。
  - **Why**:
    - (a) §3 Outcome Metric 的 audit-skill-anatomy.py 校验范围会漏 3 个修改后 skill；
    - (b) hf-design 节点会按 spec "4 修改" 估算 design 范围，导致 FR-002 / FR-009 / FR-010 在 design 阶段缺对应章节；
    - (c) hf-tasks 节点会少 3 个 task；
    - (d) hf-traceability-review 在 zigzag 校验 spec → design → tasks → impl → verify 时会找不到 hf-test-driven-dev / hf-completion-gate / using-hf-workflow 的修改 anchor 与 verify evidence 链；
    - (e) NFR-001 audit 范围与实际改动范围不一致。
  - **Suggested fix**: 在 §2 / §3 / §6 / §9 四处统一口径——
    - §2 改为 "现有 25 个 skill（24 hf-* + using-hf-workflow）中允许修改 7 个：4 named + using-hf-workflow + hf-test-driven-dev + hf-completion-gate"
    - §3 Outcome Metric 改为 "4 新 + 7 改 = 11 个 SKILL.md"，对应 audit 范围
    - §6 把 "修改 4 个 skill" 段改为 "修改 7 个 skill（4 主升级 + 3 集成点修改）"，把 using-hf-workflow / hf-test-driven-dev / hf-completion-gate 三个集成点修改的具体改法落到表格里
    - §9 Scope Out 的"20 个未升级"改为 "18 个未升级"，从列表中移除 `hf-test-driven-dev` 与 `hf-completion-gate`

- **[important][LLM-FIXABLE][Q3][Q4][NFR-cross-client] NFR-004 verification 列表漏 Claude Code，与 HF 三客户端定位矛盾**
  - Anchor 1: `spec.md` §8 NFR-004 验证列 "端到端测试在 Cursor / OpenCode 各装一次后 ls 验证"
  - Anchor 2: `README.md` Scope Note v0.5.1 段 "Officially supported clients: Claude Code, OpenCode, and Cursor"
  - Anchor 3: ADR-003 决定 v0.3.0 起 HF 官方支持三客户端
  - **What**: NFR-004 验证只列 Cursor + OpenCode 两客户端，遗漏 Claude Code（v0.3.0 起的官方支持客户端，由 marketplace 安装）。
  - **Why**:
    - (a) 三客户端可移植性是 ADR-008 D1 / ADR-010 D3 反复声明的 HF 核心 moat；NFR 验证不全会让"v0.6 在 Claude Code 上能否识别新 skill"成为盲区；
    - (b) Claude Code 通过 `.claude-plugin/marketplace.json` + `/plugin install` 拉取 skill，与 OpenCode `.opencode/skills/` / Cursor `.cursor/harness-flow-skills/` 走的安装拓扑不同（见 ADR-007 / `docs/claude-code-setup.md`），可能存在 only-cursor-only-opencode 的覆盖盲区；
    - (c) 与 §6 "不修改 `.claude-plugin/marketplace.json`"（HYP-004）的承诺需要在 NFR-004 显式验证：marketplace 不动的情况下，新 skill 是否仍被 Claude Code 自动 picked up（依赖 plugin 安装时复制 `skills/` 目录的语义）。
  - **Suggested fix**: NFR-004 验证改为 "端到端测试在 Cursor / OpenCode / Claude Code 三客户端各装一次后 ls / `/plugin info` 验证 4 新 + 7 改 skill 全部可识别；Claude Code 验证通过 plugin 安装后检查 `~/.claude/plugins/<plugin>/skills/` 内容，或在新会话中 invoke 新 skill 看是否被加载"。

### Minor

- **[minor][LLM-FIXABLE][Q4] FR-002 Acceptance 与 ADR-008 D7 五文件强 schema 关系不清**
  - Anchor: `spec.md` §7 FR-002 描述 "至少 learnings.md / verification.md 任一" + ADR-008 D7 决议 "5 文件强 schema：learnings.md / decisions.md / issues.md / verification.md / problems.md"
  - **What**: FR-002 暗示"5 文件不必齐全，每个 task 写其中之一就行"，但 ADR-008 D7 的"强 schema" 语义通常意味着"5 文件作为容器必须齐全（可空），每个 task delta 至少落到任一"。两种解读会导致 `validate-wisdom-notebook.py`（FR-012）的校验逻辑分歧。
  - **Suggested fix**: FR-002 Acceptance 改为 "(1) `hf-test-driven-dev/SKILL.md` 的 Output Contract 段要求 task 完成时：(a) 5 个 notebook 文件作为容器必须存在（首次 task 创建空骨架，validate 时只检查文件存在性）；(b) 每个 task 至少在 learnings.md / verification.md 任一中追加 delta 段；(2) `hf-completion-gate` 调用 `validate-wisdom-notebook.py` 校验"。

- **[minor][LLM-FIXABLE][C1] FR-008 Acceptance 仅引用 ADR-009 D2 而非要求 SKILL.md 本地 enumerate**
  - Anchor: `spec.md` §7 FR-008 Acceptance "(2) 含 fast lane 边界（按 ADR-009 D2 不可压缩项）"
  - **What**: skill-anatomy.md 第 3 条 "SKILL.md 是本地 contract，不是概念长文"+ Hard Gates 段 "Hard Gates 写不可协商的停止条件" 要求关键约束直接写在 SKILL.md 主文件，不能只靠引用 ADR。
  - **Why**: agent 在 runtime 执行 hf-ultrawork 时不会去读 ADR-009；fast lane 不可压缩的 5 类项（8 review / 3 gate / closeout pack / approval 工件落盘 / Hard Gates 停下抛回）必须在 hf-ultrawork SKILL.md `Hard Gates` 段直接列出。
  - **Suggested fix**: FR-008 Acceptance #2 改为 "SKILL.md `Hard Gates` 段直接 enumerate 不可压缩的 5 类项（具体见 ADR-009 D2 表格），不允许只写'按 ADR-009 D2 执行'"。

- **[minor][LLM-FIXABLE][C4] 新 skill 是否走 ADR-006 D1 的 anatomy v2 四子目录约定（含 evals/）spec 未显式要求**
  - Anchor: `spec.md` §6 "新增 4 个 skill" 段只列 SKILL.md + references/，未提 evals/ 与 scripts/
  - **What**: ADR-006 D1 锁定的 anatomy v2 = `SKILL.md` + `references/` + `evals/` + `scripts/` 四类子目录；hf-ultrawork / hf-wisdom-notebook 都属于"高风险 skill"（fast lane 决策权 + 工件 schema 强约束），应该有 evals/。
  - **Suggested fix**: §6 加一句 "4 个新 skill 全部按 ADR-006 D1 anatomy v2 创建；hf-wisdom-notebook 与 hf-ultrawork 必须含 `evals/` 目录（高风险 skill）；hf-gap-analyzer 与 hf-context-mesh `evals/` 可选"，并把"是否需要 scripts/"标到 hf-design 阶段决定（hf-wisdom-notebook 可能需要 schema validator script）。

- **[minor][LLM-FIXABLE][C7][Q4] FR-009 没说明 `using-hf-workflow` 步骤 3 现有逻辑保持不变**
  - Anchor 1: `spec.md` §7 FR-009 "`using-hf-workflow` step 5 entry bias 新增 fast lane 一行"
  - Anchor 2: `using-hf-workflow/SKILL.md` 步骤 3 "提取 Execution Mode 偏好"已存在
  - **What**: FR-009 只说步骤 5 加一行，没显式声明步骤 3 不变。design 节点可能误以为 FR-009 同时改步骤 3。
  - **Suggested fix**: FR-009 Acceptance 加一句 "(2) 步骤 3 现有 Execution Mode preference 解析逻辑保持不变；FR-009 仅在步骤 5 entry bias 表新增一行"。

- **[minor][LLM-FIXABLE][Q3][C2] FR-015 是 SHOULD 但 Acceptance 写法与 MUST 等价**
  - Anchor: `spec.md` §7 FR-015 Priority=SHOULD，Acceptance "transition map 中 handoff 示例含 category_hint；下游 skill 不消费时直接忽略不报错"
  - **What**: SHOULD 通常意味着"不强制完成"，但 Acceptance 写得像 MUST（"含 category_hint"）。需要明确 SHOULD 的失败处理：FR-015 不达标时 hf-completion-gate 是否阻塞？
  - **Suggested fix**: 在 FR-015 后加一句 "Priority=SHOULD：FR-015 不达标时 hf-completion-gate 不阻塞，但需在 closeout pack 的 deferred backlog 段记录"。

- **[minor][LLM-FIXABLE][A3] HYP-002 阐述含轻微设计泄漏**
  - Anchor: `spec.md` §4 HYP-002 Statement "`hf-ultrawork` skill + `using-hf-workflow` 关键词识别（已有）+ progress.md Fast Lane Decisions 段足以承载 fast lane 全部行为"
  - **What**: HYP 描述里"关键词识别"+"progress.md 段"是 spec 阶段不必锁定的实现机制（也可能是 hash-based marker / sentinel file 等）。
  - **Suggested fix**: HYP-002 Statement 改为 "在不引入 v0.7 runtime 的前提下，markdown 包内已有的 Execution Mode preference 机制 + 可被 host agent 读取的 progress 工件足以承载 fast lane 全部行为"。具体机制由 design 决定。

- **[minor][LLM-FIXABLE][Q1][Q8] §3 Success Metrics 表混合元数据行（同 features/001 同款薄弱）**
  - Anchor: `spec.md` §3 Success Metrics 表内的 `Measurement Method` / `Non-goal Metrics` / `Instrumentation Debt` 三行用同一表头（指标 / 阈值 / 测量方法）但语义其实是 "角色 / 内容 / 空"
  - **What**: 与 features/001 spec-review-2026-05-11.md "缺失或薄弱项"段同款，结构略杂糅；不计入 finding，列为薄弱项。
  - **Suggested fix**: 不计入 finding（与 features/001 同款不强求修复，但若 author 顺手分离也可）。

## 缺失或薄弱项

- §3 Success Metrics 行 `Measurement Method` / `Non-goal Metrics` / `Instrumentation Debt` 与 features/001 同款表内复用，结构杂糅；不计入 finding。
- §11 风险表的"OMO upstream sync"风险标"无需特殊处理"是合理的（HF 是方法论复制非代码 fork），但建议 design 阶段在 ADR-010 落地时显式开 OMO upstream tracking issue（不阻塞本 feature spec）。
- HYP-002（Blocking）的 Validation Plan 写"在 Cursor / Claude Code（无 runtime）上跑本 feature 自己的 fast lane"——但本 feature dogfood 必然在某个具体客户端上跑（取决于架构师的会话宿主），三客户端横向验证需要在 design 阶段拆出一个跨客户端 verification task。

## 覆盖检查

| Group | Rule | 检查结果 |
|---|---|---|
| Q | Q1 Correct/Source | ⚠️ 大部分 FR / NFR 在 §1 / §6 / ADR 引用层有 Source；但 FR 表格内没有独立 Source 列（与 features/001 一致；可接受，trace 由 §1 + §6 + ADR 锚点承担） |
| Q | Q2 Unambiguous | ✅ NFR 全部带数字阈值（< 500 行 / < 5000 tokens / 4 新 + 7 改 全部 PASS / stdlib only）；HYP 都标 confidence + Validation Plan |
| Q | Q3 Complete | ⚠️ §6 / §9 漏 3 个集成点修改 skill（important finding 1）；NFR-004 漏 Claude Code（important finding 2）；FR-009 缺步骤 3 不变声明（minor finding 4）；其余覆盖完整 |
| Q | Q4 Consistent | ⚠️ §2 vs §3 vs §6 vs §9 vs FR-002 四处口径不一致（important finding 1）；HYP-002 表述与 spec 阶段不锁实现的原则有轻微设计泄漏（minor finding 6）；其余 FR / NFR / HYP / OQ 三表互一致 |
| Q | Q5 Ranked | ✅ 15 FR 中 14 MUST + 1 SHOULD；7 NFR 全 MUST；无"全 Must"懒惰标注；FR-015 是唯一 SHOULD（minor finding 5 要求补 SHOULD 失败处理） |
| Q | Q6 Verifiable | ✅ 每条 FR / NFR 都有可机械判断的 Acceptance（文件存在 / audit 通过 / grep 命中等）；HYP-002 Validation Plan 在 TDD 阶段可执行 |
| Q | Q7 Modifiable | ✅ FR / NFR / HYP / 范围 / 边界 / OQ / 风险 分布合理；除 important finding 1 涉及的口径同步外，内部不重复矛盾 |
| Q | Q8 Traceable | ✅ 所有 FR / NFR / HYP / OQ / 风险都能回指 ADR-008 D2 / D7 / ADR-009 D2 / ADR-010 D2 中具体决定；OMO 引用（src/tools/hashline-edit / src/agents/atlas / src/hooks/keyword-detector 等）可冷读回到 OMO 公开仓库 |
| A | A1 模糊词 | ✅ 没有 "快 / 稳 / 友好 / 易用" 等未量化词 |
| A | A2 复合需求 | ✅ FR-001 / FR-004 / FR-007 / FR-008 各为 "新增一个 skill"；FR-002 把 hf-test-driven-dev + hf-completion-gate 写在同一 FR 里**严格说是复合**，但二者是同一个机制（写 + 校验）的两面，可接受不拆 |
| A | A3 设计泄漏 | ⚠️ HYP-002 含轻微实现细节（minor finding 6）；FR-002 / FR-008 / FR-009 实现路径表述适度，可接受 |
| A | A4 无主体被动表达 | ✅ 全部 FR 主语清晰（hf-tasks-review / hf-specify / hf-workflow-router / hf-ultrawork / scripts / using-hf-workflow） |
| A | A5 占位或待定值 | ✅ 关键 FR / NFR 内无 TBD；§10 OQ-001 ~ OQ-007 均显式标"design / tasks 阶段决定"且都不阻塞；HYP-002 标 Blocking 但 Validation Plan 明确 |
| A | A6 缺少负路径 | ⚠️ FR-005 含 N=3 上限的 escape 路径；FR-008 含 escape conditions；NFR-006 含 fast lane 失效降级；但 FR-002 / FR-003 / FR-004 / FR-007 没明确"validate 失败时怎么办"——可在 design 决定，不构成 finding |
| C | C1 Requirement contract | ⚠️ 15 FR + 7 NFR 都有 ID / Statement / Acceptance / Priority；但表格列里 "Source" 隐含在 §1 / §6 / ADR 引用，不像 features/001 那样每行带 Source 列——与 features/001 相同；FR-008 Acceptance 仅引用 ADR-009 D2 不在 SKILL.md 本地 enumerate（minor finding 3） |
| C | C2 Scope closure | ⚠️ §6 / §9 内部矛盾（important finding 1 同款）；§9 列举的 20 个 + 4 新 + 4 改 = 28，但 25 - 4 修改 - 4 新 + 4 = 25 + 4 = 29 数字也对不上（实际是 25 现 + 4 新 - 7 改 = 22 - 0 = ?）（important finding 1 同款）；FR-015 SHOULD 闭合（minor finding 5）；其余范围内/外清晰 |
| C | C3 Open-question closure | ✅ §10 OQ-001 ~ OQ-007 显式分"design 决定 / tasks 决定"两类，无悬空 |
| C | C4 Template alignment | ⚠️ 11 章节 + §12 review checklist 整体遵循 hf-specify 默认骨架；缺独立 §10 假设段（假设嵌在 HYP / §6 / ADR 引用里）——可接受；新 skill 是否走 anatomy v2 四子目录未声明（minor finding 4） |
| C | C5 Deferral handling | ✅ 本 feature 未抽 deferred backlog，OQ 全部归到 design / tasks 阶段；处理一致 |
| C | C6 Goal and success criteria | ✅ §2 总体成功标准 + §3 Success Metrics 表（Outcome / 3 Leading Indicator / 1 Lagging Indicator）齐全；阈值具体可判 |
| C | C7 Assumption visibility | ⚠️ HYP-002 + HYP-005 显式假设可读；但"四客户端 install 后 4 个新 skill 自动 picked up 的机制依赖于 install 拷贝 skills/ 全树"这个假设隐含未显式（嵌在 §6 / FR-008 / NFR-003 中）—— 可接受不构成 finding，但建议 design 阶段在 install topology 章节显式 |
| G | GS1 ~ GS6 oversized | ✅ 15 FR 中没有 oversized 需求；FR-001 / FR-004 / FR-007 / FR-008 是新 skill creation 类，按 anatomy v2 一个 SKILL.md + N 个 references/ 即可，不算 oversized |
| G | GS7 mixed iteration | ✅ §6 / §9 显式区分本轮范围 + 永久封禁项；v0.7 runtime / v0.8 删除项 / Team Mode / Hephaestus 都在 Scope Out 段封禁；无混轮风险 |

## 下一步

`hf-specify`（按本 review record 修复 important × 2 + minor × 6 后回 spec）

修复完成回 spec 后，由 reviewer 直接做 Round 2 复审；若 Round 2 通过，再走 `规格真人确认`（auto mode 下写 approval record 自动继续）。

## 记录位置

`features/002-omo-inspired-v0.6/reviews/spec-review-2026-05-13.md`（本文件）

## 交接说明

- `hf-specify`：用于本轮 important + minor 的定向修订；不引入新 FR / 新 NFR / 新 OQ，只修文字与口径
- 修订后回到本 reviewer 节点做 Round 2 复审（fast lane auto mode 下连续做不间断）
- 不上抛架构师（无 USER-INPUT finding；所有 finding 均 LLM-FIXABLE）
- `reroute_via_router=false`（无 workflow blocker，stage 内部修订）

## 结构化返回 JSON

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-specify",
  "record_path": "features/002-omo-inspired-v0.6/reviews/spec-review-2026-05-13.md",
  "key_findings": [
    "[important][LLM-FIXABLE][Q3][Q4][C2] §6/§2/§3/§9 内部口径矛盾：实际涉及 7 个 skill 修改而非 4 个",
    "[important][LLM-FIXABLE][Q3][Q4] NFR-004 verification 漏 Claude Code，与 HF 三客户端定位矛盾",
    "[minor][LLM-FIXABLE][Q4] FR-002 Acceptance 与 D7 5 文件强 schema 关系不清",
    "[minor][LLM-FIXABLE][C1] FR-008 Acceptance 仅引用 ADR-009 D2 而非要求 SKILL.md 本地 enumerate",
    "[minor][LLM-FIXABLE][C4] 新 skill 是否走 anatomy v2 四子目录未声明",
    "[minor][LLM-FIXABLE][C7][Q4] FR-009 缺'步骤 3 不变'声明",
    "[minor][LLM-FIXABLE][Q3][C2] FR-015 SHOULD 缺失败处理说明",
    "[minor][LLM-FIXABLE][A3] HYP-002 阐述含轻微设计泄漏"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "round": 1
}
```

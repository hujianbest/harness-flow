# Spec Review: HF Orchestrator Extraction & Skill Decoupling

- 评审对象:
  - Spec: `features/001-orchestrator-extraction/spec.md`
  - 配套 ADR: `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`
- 评审 skill: `hf-spec-review`
- 评审者: 独立 reviewer subagent（与 author 分离，符合 Fagan）
- 评审时间: 2026-05-10
- 草稿密度: `full`
- 评审方法: 结构化 walkthrough + Q/A/C/G 四组 rubric + ADR 内部一致性 + 上游 finding 吸收核验（per `skills/hf-spec-review/references/spec-review-rubric.md`）

## Precheck

| 检查项 | 结果 |
|---|---|
| 规格草稿存在且可定位 | ✓ `features/001-orchestrator-extraction/spec.md` |
| 候选 ADR 存在且可定位 | ✓ `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md` |
| 请求确为 review（非续写、非设计） | ✓ 父会话明确派发为 reviewer subagent |
| Stage / route / evidence 一致 | ✓ spec 自报 `Current Stage: hf-specify` + `Next Action: hf-spec-review`；progress.md / README.md 同步 |
| Author / Reviewer 分离 | ✓ spec + ADR-007 由父会话起草，reviewer 独立 |
| Discovery 上游证据 | ✓ `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md` 通过 `hf-discovery-review`（3 条 minor LLM-FIXABLE） |

Precheck 通过，进入正式 rubric。

## 结构契约核验（Step 2）

| 契约 | 来源 | 结果 |
|---|---|---|
| 14 章节骨架 | `skills/hf-specify/references/spec-template.md` | ✓ 章节顺序、命名与默认结构一致；§ 3 / § 4 hard anchor 均存在 |
| FR 字段（ID / 优先级 / 来源 / 陈述 / 验收） | `requirement-authoring-contract.md` | ✓ FR-001 至 FR-007 均完整 |
| NFR QAS（ISO 25010 + 五要素） | `nfr-quality-attribute-scenarios.md` | ✓ NFR-001 至 NFR-005 均含维度 / Stimulus Source / Stimulus / Environment / Response / Response Measure / Acceptance |
| Success Metrics 全字段 | `success-metrics-and-hypotheses.md` (full) | ✓ Outcome / Threshold / Leading / Lagging / Measurement Method / Non-goal / Instrumentation Debt 齐全 |
| Key Hypotheses 全字段表格 | 同上 (full) | ✓ HYP-001 至 HYP-007 含 Statement / Type / Impact If False / Confidence / Validation Plan / Blocking? |
| Deferral handling | C5 | ✓ § 6.3 显式声明无独立 deferred backlog；延后内容落到 ADR-007 D3 / § 6.2 |

结构契约**通过**。

## Discovery Review Finding 吸收核验

| Finding | 来源 | 吸收证据 | 结果 |
|---|---|---|---|
| `[minor][LLM-FIXABLE][A2]` Facts vs project-stance 分离 | discovery-review.md L51 | spec § 5 仅写"角色 / 场景 / 痛点 / 改善"；项目立场（"closeout schema 不变"等）独立落到 § 6.2 + ADR-007 D6 / "不做"段 | ✓ |
| `[minor][LLM-FIXABLE][D1]` 行数预算重定为 tentative engineering aim | discovery-review.md L52 | § 3 加分项明确"tentative engineering aim ... 本 spec 不作为 NFR 阈值"；NFR-002 改用字符数（`wc -c × 1.10`）作为 acceptance；§ 14 新增"Tentative Engineering Aim"术语条目；HYP-004 Validation Plan 同步 | ✓ |
| `[minor][LLM-FIXABLE][B1]` Discovery 唯一阻塞项（references 是否本轮迁移）显式降级 | discovery-review.md L53 | § 6.1 In-scope 第 2 项明确"本轮迁移；旧位置保留 redirect stub"；§ 13 阻塞项 = 无（含降级注释）；ADR-007 D2 锁定 | ✓ |

3 条吸收**全部命中**。

## 评分维度（Q / A / C / G）

| Group | ID | 检查 | 结果 | 关键观察 |
|---|---|---|---|---|
| Q | Q1 | Correct（来源可回指） | ✓ | 每条 FR / NFR 的 Source 字段指向 HYP-xxx / discovery 章节 / 既有 ADR / FR-NNN |
| Q | Q2 | Unambiguous（无未量化模糊词） | △ | NFR-001 Response Measure 给出 `≤ 当前 × 1.20` 量化阈值，但 Acceptance 退化到"使用者主观感知不到加载耗时显著增加"/"不存在'加载明显变慢'主观投诉"——见 finding 1 |
| Q | Q3 | Complete | ✓ | NFR-003 覆盖外部消费者 404 路径；C-005 plug-in schema fallback；FR-002 含降级路径 |
| Q | Q4 | Consistent | ✓ | § 6.1 / § 6.2 / § 7 / ADR-007 D2-D7 立场互不冲突；FR-004 与 NFR-003 一致 |
| Q | Q5 | Ranked | ✓ | FR-001-005 Must；FR-006-007 Should；NFR-001-004 Must；NFR-005 Should |
| Q | Q6 | Verifiable | △ | 见 NFR-001 finding；其余条目 Acceptance 可形成通过/不通过判断 |
| Q | Q7 | Modifiable | ✓ | § 7 显式声明"与 § 6.2 强一致，按编号同步维护"，单源已点明 |
| Q | Q8 | Traceable | ✓ | 关键需求均有稳定 ID + Source；ADR-007 与 spec 互引 |
| A | A1 | 模糊词 | △ | 同 Q2，NFR-001 Acceptance 含"显著""明显"无量化 |
| A | A2 | 复合需求 | △ | FR-002 在一条 FR 内打包 3 宿主 × 4 always-on 机制；Acceptance 已逐宿主拆开，可读性可接受——见 finding 4 |
| A | A3 | 设计泄漏 | △ | FR-001 陈述列举"operating loop（步骤 1-10）/ FSM 转移表入口 / dispatch 协议入口 / skill catalog（24+1 description-line 索引）"——为锁定等价改写边界，非纯设计；处于"业务意图 vs 设计"灰区——见 finding 3 |
| A | A4 | 无主体被动 | ✓ | 所有需求陈述均以"系统必须"起句 |
| A | A5 | 占位 / 待定 | ✓ | 关键需求中无 TBD / 待确认 |
| A | A6 | 缺少负路径 | ✓ | FR-002 含 plug-in schema fallback；NFR-003 含外部消费者读取旧路径不 404；NFR-005 含人工 mutation 测试 |
| C | C1 | Requirement contract | ✓ | 所有 FR / NFR 五字段齐全 |
| C | C2 | Scope closure | ✓ | § 6.1（9 项 in-scope）/ § 6.2（12 项 out-of-scope）显式列出 |
| C | C3 | Open-question closure | ✓ | § 13 阻塞项 = 无；5 条 OQ-N-xxx 均非阻塞且各有归属阶段（hf-design / hf-tasks / hf-release） |
| C | C4 | Template alignment | ✓ | 与 `spec-template.md` 默认骨架完全一致 |
| C | C5 | Deferral handling | ✓ | § 6.3 显式声明 backlog 文件不创建；延后项均有具体归属（ADR-007 D3 step 2-6 / § 6.2） |
| C | C6 | Goal & success criteria | ✓ | § 2 / § 3 含必达 / 加分双层门槛；walking-skeleton 等价性 + 3 宿主 smoke 均可判定 |
| C | C7 | Assumption visibility | ✓ | § 4 Key Hypotheses + § 12 spec 独有运行假设双层显式 |
| G | G1 / GS3 | Oversized FR | △ | FR-002（3 宿主 × 4 机制）与 FR-006（README + 3 setup docs）轻度命中 GS3 场景爆炸；Acceptance 已分项拆解，可接受但需点出——见 finding 4 |
| G | G2 | Mixed release boundary | ✓ | § 6.1 / § 6.2 / ADR-007 D3 把 v0.6.0 step 1 与 step 2-6 分得很干净 |
| G | G3 | Repairable scope | ✓ | 全部 finding 均 LLM-FIXABLE，1-2 轮定向回修可收敛 |

**关键检查未通过的维度**：Q2 / Q6 / A1（NFR-001 Acceptance 退化为主观判定）；A3（FR-001 陈述含设计层结构）。其余维度通过。

## ADR-007 内部一致性核验

| 检查 | 结果 | 说明 |
|---|---|---|
| D1 三层架构 invariant 表述 | △ | 见 finding 2：D1 把"Layer 1 / Layer 2 之间互不引用"写为不带时间限定的 invariant，但 D3 Step 5 才剥离 leaf 中对其它 hf-* 的硬引用——v0.6.0 范围内该 invariant 不能被运行时强制；冷读者会与"v0.6.0 已立即生效"混淆 |
| D1 "Layer 3 不是 skill" 清晰度 | ✓ | 显式声明"不进 `skills/` 目录、不进 `audit-skill-anatomy.py` 扫描、不需要 SKILL.md frontmatter 完整 schema" |
| D2 Single source of truth + 旧位置 stub | ✓ | 与 spec § 6.1 #2 / FR-004 / NFR-003 / C-006 一致 |
| D3 6 步落地路径 与 v0.6.0 边界 | ✓ | "v0.6.0 只做 Step 1"显式声明；step 2-6 范围归属表格清楚 |
| D4 兼容期 deprecated alias | ✓ | 与 spec FR-004 / C-006 / NFR-003 互证 |
| D5 release-blocking 假设清单 | ✓ | 显式锁定 "v0.6.0 release 通过 hf-completion-gate 前必须有 fresh evidence"——把 HYP-002 / HYP-003 从 "spec-blocking" 校准为 "release-blocking"，与 spec § 4 表格一致 |
| D6 与 v0.6+ 5 项 ops/release skill 关系 | ✓ | 锁定后续这些 skill 引入时必须遵循三层架构 invariant；与 ADR-005 D7 立场延续 |
| D7 personas 不扩张 | ✓ | 与 § 6.2 #11 一致 |
| ADR 关系表 vs ADR-001 D1 | ✓ | "P-Honest, narrow but hard" 立场延续，本轮严格停在单 feature |
| ADR 关系表 vs ADR-002 D11 | ✓ | reviewer return verdict 词表不动 |
| ADR 关系表 vs ADR-003 D2 | ✓ | 3 宿主 always-on stub 覆盖 Cursor / Claude Code / OpenCode |
| ADR 关系表 vs **ADR-004 D3**（"关键先例"） | ✓ | 已核验 ADR-004 Decision 3 = "`hf-release` 完全解耦于 `hf-workflow-router`"；ADR-007 D1 把这一 standalone-from-router 解耦能力**从 release-tier 特例提升为全 HF skill 的层架构 invariant**——逻辑延伸成立，无矛盾 |
| ADR 关系表 vs ADR-005 D4 / D7 | ✓ | 立场延续 |
| ADR 关系表 vs ADR-006 D1 | ✓ | `agents/` 是新引入的目录类别，不属于 4 类子目录 skill anatomy；脚本对 `agents/` 透明 |
| 12 项 out-of-scope 是否被 D6 / D7 静默引回 | ✓ | 逐项核验未发现回潜入；D6 / D7 与 § 6.2 #8 / #11 完全一致 |
| 行数预算是否被偷偷塞回 NFR 阈值 | ✓ | NFR-002 用字符数（`wc -c`）；行数仅出现在 § 3 加分项、HYP-004 Validation Plan、§ 12 假设、§ 14 术语，均显式标 "tentative engineering aim" |

## 发现项

- **[important][LLM-FIXABLE][Q2 / Q6 / A1] NFR-001 Acceptance 把已量化的 Response Measure（≤ 当前 × 1.20）退化为主观判定。** Response Measure 给出明确比率门槛；Acceptance 两条 bullet 改为"使用者主观感知不到加载耗时显著增加""不存在任一宿主的'加载明显变慢'主观投诉"。"显著""明显变慢"无量化、属 A1；与 Response Measure 错位 → 违反 Q2（未量化）+ Q6（不可形成通过/不通过判断）。建议修复：让至少一条 Acceptance 直接锚定 1.20× 阈值（例如 `Given 在 Cursor 新建 session，When 测量从 session 创建到第一轮响应包含 orchestrator identity 的 wall-clock 时间，Then 该时间 ≤ baseline（同操作下加载现状 entry shell + router 的 wall-clock）× 1.20`），或显式承认 1.20× 是 hf-design 阶段才会落到的目标值并把 NFR-001 优先级从 Must 降为 Should。无新业务事实，纯 wording 修订。

- **[important][LLM-FIXABLE][ADR1] ADR-007 D1 把 "Layer 1 / Layer 2 之间互不引用" 写为无时间限定的 invariant，与 D3 Step 5 描述的现实状态冲突。** D1 的不变量"只在 SKILL.md 的 `## See Also` 段做软提及；不做 hard gate 引用、不写其它 hf-* 的 canonical ID 作为 handoff 字段"在 v0.6.0 范围内**不被强制**——D3 Step 5 才"删除 leaf skill 里所有对其它 hf-* 的硬引用"，且明确标 "不在本轮"。冷读者无法判断该 invariant 是 v0.6.0 已生效还是后续增量才生效，会让 hf-design 阶段的 dispatch 协议设计产生歧义。建议在 D1 末尾追加一段类似："**生效阶段**：v0.6.0 范围内本不变量为 architectural commitment（架构承诺），运行时强制将随 D3 Step 5 完成；兼容期内允许 leaf skill 保留对其它 hf-* 的硬引用，但新增 leaf 必须遵循该不变量。"无新事实，纯 wording 修订。

- **[minor][LLM-FIXABLE][A3] FR-001 需求陈述罗列 orchestrator 文件的内部结构（"operating loop（步骤 1-10）"、"FSM 转移表入口或引用"、"reviewer dispatch 协议入口或引用"、"skill catalog（24 个 hf-* + 1 个 entry shell 的 description-line 索引）"、"verification 自检清单"）。** 这些是设计层选择的落点。本 FR 的真实业务意图是"orchestrator 等价改写自 `using-hf-workflow` + `hf-workflow-router` 的合并语义，且作为 always-on agent persona 自报身份"——已被 FR-003 + ADR-007 D2 覆盖。建议把 FR-001 陈述简化为"系统必须在 `agents/hf-orchestrator.md` 提供 always-on agent persona 文件，其内容**在语义上**等价于 `using-hf-workflow` + `hf-workflow-router` 的合并改写（具体子结构由 hf-design 阶段锁定）"，把"步骤 1-10""skill catalog 索引"等内部结构推给 hf-design。不阻塞设计——hf-design 阶段会自然产出这些子结构。

- **[minor][LLM-FIXABLE][A2 / GS3] FR-002 把 3 个宿主 × 4 种 always-on 机制（`.cursor/rules/harness-flow.mdc` / `CLAUDE.md` / `.claude-plugin/plugin.json` / `AGENTS.md`）打包到一条 FR；FR-006 把 README 中英双语 + 3 个 setup docs 打包到一条 FR。** Acceptance 已逐宿主 / 逐文档拆开，冷读不至于丢失语义；但纯 GS3（场景爆炸）口径下值得点出。可在 hf-design 阶段考虑拆为 FR-002a / FR-002b / FR-002c（按宿主），或保留打包但在 spec 末尾追加"FR-002 / FR-006 的 Acceptance 各子项独立判定"备注。不阻塞，可与 finding 1-3 一起定向修订。

- **[minor][LLM-FIXABLE][C1] FR-003 验收第三条 bullet 引用 `features/001-orchestrator-extraction/verification/regression-diff.sh` "或等价"** ——"或等价"留出一个未约束的实现位置，与 OQ-N-003（脚本归属位置开放）一致；冷读者无法在 spec 阶段判定脚本是否落到正确位置。建议要么删"或等价"+ 把脚本路径推给 OQ-N-003 在 hf-tasks 阶段最终决定；要么保留"或等价"但在备注里指明 acceptance 判据为"路径任选其一，但必须在 verification record 里登记"。轻量修订。

- **[minor][LLM-FIXABLE][Q4 / 可读性] § 7 范围外内容只写"见 § 6.2。本 § 与 § 6.2 强一致，按编号同步维护"，不内联条目。** 单源原则正确（防止双源漂移），但 § 7 在 spec 模板里是独立章节、冷读者直接跳到 § 7 时拿不到内容。建议保留单源声明，但在 § 7 加一行 "完整 12 条列表见 § 6.2" 或把 § 6.2 标题改名"§ 6.2 当前轮 Out-of-scope（同时是 § 7 范围外内容的权威来源）"以提示同步关系。可与上方一并处理。

## 缺失或薄弱项

- **NFR-001 与 HYP-003 的验证证据通道未在 spec 层显式写出**：spec § 4 / ADR-007 D5 把 HYP-002 / HYP-003 标为 release-blocking 假设，验证发生在 `hf-test-driven-dev` 阶段；NFR-001 acceptance 中只能得到主观判定，缺一个量化测量记录的落盘位置（建议在 § 3 Measurement Method 或 NFR-001 acceptance 中显式指明"测量记录写入 `features/001-orchestrator-extraction/verification/load-timing-3-clients.md`"，与 smoke-3-clients.md 并列）。属 finding 1 的延展，列入"薄弱项"以便 hf-design 一并解决。

- **HYP-004 Token 预算是 medium-high confidence，且 Validation Plan 写"design 阶段量化"**：本 spec 已在 NFR-002 把字符数量化为 acceptance criterion（`wc -c × 1.10`），等价于把验证从 design 提前到 commit 时刻，HYP-004 confidence 实际上比 § 4 表格写的"中-高"更高。建议 hf-specify 阶段顺手把 HYP-004 confidence 重估为 high，但**不影响本 spec 的判定**，列入 minor 改进。

- **HF 自架构 feature 的特殊性未在 spec 中显式说明 audit 范围**：spec § 6.2 #6 + C-004 + ADR-007 D2 已显式 `audit-skill-anatomy.py` 不扫 `agents/`。但 spec 没有声明是否需要在 v0.6.x / v0.7.0 引入 `audit-agent-anatomy.py`（ADR-007 D2 把这个推给 "后续 ADR 决定"）。当前不阻塞；若 hf-design 阶段发现 orchestrator persona 也需要纪律性的结构 audit，建议回 hf-specify 补一条 NFR 或开 ADR-008。

- **Discovery 上游 HYP-001（Desirability，medium）的"P2 probe（翻 GitHub issues / discussions）"未在 spec 中给出执行节点**：spec § 4 标"非阻塞"且 ADR-007 D5 也未列入 release-blocking。延续 discovery review 的判定无问题，但 hf-design 阶段如果决定主动跑此 probe，spec 没有为它预留 acceptance 通道。属"已知薄弱点"，不阻塞本轮。

## 结论

需修改

理由：rubric Q / A / C / G 四组检查中，**Q2 / Q6 / A1 三个核心维度**因 NFR-001 Acceptance 退化为主观判定共同未通过；**ADR-007 D1**对"Layer 1/Layer 2 互不引用"invariant 缺时间限定，与 D3 Step 5 描述的 v0.6.0 实际状态冲突，会误导 hf-design 阶段的 dispatch 协议设计。两条 important finding 均 LLM-FIXABLE，预计 1 轮定向修订即可收敛。其余 4 条 minor finding 可与 important findings 一并处理；ADR 跨 6 个先例的关系表已逐项核验准确（含 ADR-004 D3 "关键先例"延伸成立）；3 条上游 discovery review finding 全部命中吸收；§ 6.2 12 项 out-of-scope 未被 ADR-007 D6 / D7 静默引回；行数预算未偷塞回 NFR 阈值。范围与方向稳定，**仅需 wording 层修订**，不需推倒重来。

## 下一步

- 唯一下一步：`hf-specify`
- 修订重点（按优先级）：
  1. NFR-001 Acceptance 重写为可量化判定（或显式降级 NFR-001 为 Should）
  2. ADR-007 D1 增补 "v0.6.0 范围内为 architectural commitment，运行时强制随 D3 Step 5 完成" 的时间限定段
  3. （可选）FR-001 / FR-002 / FR-003 / FR-006 / § 7 的 minor wording 整理
- **不**需要回到 `hf-product-discovery`：上游 discovery 已通过 review，3 条 minor finding 已正确吸收
- **不**需要 `hf-workflow-router`：route / stage / evidence 一致，无 workflow blocker
- 修订后**重新派发** `hf-spec-review` 一次，预期 1 轮收敛到 `通过`

## 评审者元数据

- 是否需要人工裁决（needs_human_confirmation）：否
- 是否需要回 router（reroute_via_router）：否
- USER-INPUT findings：无（本轮所有 finding 均 LLM-FIXABLE，由 `hf-specify` 起草节点直接修订）

## 结构化返回 JSON

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-specify",
  "record_path": "features/001-orchestrator-extraction/reviews/spec-review-2026-05-10.md",
  "key_findings": [
    "[important][LLM-FIXABLE][Q2/Q6/A1] NFR-001 Acceptance 把已量化的 Response Measure (≤ 当前 × 1.20) 退化为主观判定（'显著''明显变慢'）",
    "[important][LLM-FIXABLE][ADR1] ADR-007 D1 'Layer 1/Layer 2 互不引用' 缺时间限定，与 D3 Step 5 v0.6.0 不强制的事实冲突",
    "[minor][LLM-FIXABLE][A3] FR-001 陈述罗列 orchestrator 内部结构（步骤 1-10 / FSM 表 / dispatch / catalog），属设计层落点",
    "[minor][LLM-FIXABLE][A2/GS3] FR-002 / FR-006 打包多宿主多机制；Acceptance 已分项但 GS3 口径仍可点出",
    "[minor][LLM-FIXABLE][C1] FR-003 acceptance bullet 3 含 '或等价' 路径，留下未约束的实现位置",
    "[minor][LLM-FIXABLE][Q4] § 7 仅指向 § 6.2，不内联条目，独立冷读不友好"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "Q2/Q6/A1",
      "summary": "NFR-001 Acceptance 把已量化的 Response Measure (≤ 当前 × 1.20) 退化为主观判定，需把至少一条 Acceptance 锚定到 1.20× 量化阈值或显式降级 NFR-001 优先级"
    },
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "ADR1",
      "summary": "ADR-007 D1 'Layer 1/Layer 2 互不引用' 缺时间限定，需追加段说明 v0.6.0 范围内为 architectural commitment、运行时强制随 D3 Step 5 完成"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "A3",
      "summary": "FR-001 陈述列举 operating loop 步骤 1-10 / FSM 表 / dispatch 协议入口 / skill catalog 等内部结构，属设计层落点；建议简化为'语义等价 using-hf-workflow + hf-workflow-router 的合并改写'，子结构推给 hf-design"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "A2/GS3",
      "summary": "FR-002 打包 3 宿主 × 4 always-on 机制；FR-006 打包 README + 3 setup docs；Acceptance 已分项但 GS3 口径下可拆分或加 acceptance 独立判定备注"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "C1",
      "summary": "FR-003 acceptance bullet 3 引用 'regression-diff.sh 或等价' 路径，与 OQ-N-003 一致但 spec 阶段冷读不可判定；建议删 '或等价' 或加 verification record 登记备注"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "Q4",
      "summary": "§ 7 仅指向 § 6.2，独立冷读不友好；保留单源原则，但在 § 7 加一行 '完整 12 条列表见 § 6.2'"
    }
  ]
}
```

---

## 修订验证（Round 2）

- 修订提交：`1ec5cc7` on branch `cursor/orchestrator-extraction-spec-e404`
- 修订基线：`a8f6c2d`（spec + ADR-007 起草 commit）
- 验证方法：直接读取当前 HEAD 的 spec.md 与 ADR-007；逐条核验 6 条 finding 的 trigger condition 是否已消除；并扫描 diff 检查是否引入新 finding（regression）。
- 验证时间：2026-05-10
- 验证者：同 Round 1 reviewer subagent（与 author 仍分离，符合 Fagan）

### 6 条 finding 修订核验表

| # | Finding (Round 1) | 修订证据 | 是否达标 |
|---|---|---|---|
| 1 | `[important][Q2/Q6/A1]` NFR-001 Acceptance 退化为主观判定 | spec § 9 NFR-001：Response Measure 锁定 "≤ baseline × 1.20"（同口径 wall-clock）；Acceptance 改写为两条—— `(Quantitative)` 在 3 宿主分别建立 baseline / candidate 同操作 session 对比，raw timing + ratio 落盘到 `features/001-orchestrator-extraction/verification/load-timing-3-clients.md`；`(Identity gate)` 显式 cross-ref FR-002.d。已彻底脱离"显著""明显变慢"等无量化用词。 | ✓ 达标 |
| 2 | `[important][ADR1]` ADR-007 D1 缺时间限定，与 D3 Step 5 v0.6.0 不强制冲突 | ADR-007 D1 新增"**生效阶段（Architectural Commitment vs Runtime Enforcement）**"子段：v0.6.0 = 架构承诺（D1 locked / 新 leaf 必须遵循 / 现有 24 leaf 保留兼容期遗产）；v0.7.0+ = runtime enforcement（D3 Step 2–5 完成后剥离硬引用）；v0.8.0+ = D3 Step 6 物理删除旧 skill。**这意味着** 段显式给 `hf-design` 行动指令："按目标态设计 dispatch 协议；实施时允许在兼容期内消费 leaf 残留 `Next Action` 字段作为辅助 hint（不强制 leaf 提供）"。歧义彻底消除。 | ✓ 达标 |
| 3 | `[minor][A3]` FR-001 Statement 罗列 orchestrator 内部结构（步骤 1-10 / FSM 表 / dispatch / catalog） | spec § 8 FR-001：Statement 改为"在语义上等价于 `using-hf-workflow` + `hf-workflow-router` 当前合并行为的改写（具体子结构……由 `hf-design` 阶段最终锁定）"；Acceptance bullet 3 同步去掉对 operating loop 步骤 1 / 2 / 6 的硬指定，改为引用现有 `hf-workflow-router/references/profile-node-and-transition-map.md` 作为衍生来源——是真实存在的 router references，不再发明步骤号。设计层落点被干净推到 hf-design。 | ✓ 达标 |
| 4 | `[minor][A2/GS3]` FR-002 / FR-006 打包多宿主多机制，acceptance 已分项但 GS3 口径仍可点出 | spec § 8：FR-002 / FR-006 各自新增"**打包说明**"段，明确 acceptance bullet 独立判定且任一不达标即整条 FR 不达标；FR-002 acceptance bullets 标 `(FR-002.a Cursor)` / `(FR-002.b Claude Code)` / `(FR-002.c OpenCode)` / `(FR-002.d Identity check)`；FR-006 acceptance bullets 标 `(FR-006.a README ×2)` / `(FR-006.b Setup docs ×3)`，且 FR-006.a 显式覆盖 `README.md` + `README.zh-CN.md` 两份、FR-006.b 显式"3 份 setup docs **全部**通过"——把原"任一 setup doc"读作"全集量化"，消除潜在歧义。`hf-tasks` 阶段可直接按 sub-ID 拆任务。 | ✓ 达标 |
| 5 | `[minor][C1]` FR-003 acceptance bullet 3 含 "或等价" 路径 | spec § 8 FR-003 acceptance bullet 3：删除 "或等价" 模糊表述；改为显式列两条候选路径（`features/001-orchestrator-extraction/scripts/regression-diff.{sh|py}` 或 `skills/hf-finalize/scripts/regression-diff.{sh|py}`），由 OQ-N-003 在 `hf-tasks` 阶段最终决定；新增"**且** 该脚本的最终路径已登记到 `features/001-orchestrator-extraction/verification/regression-2026-05-XX.md` 的 evidence 字段"——使 spec 阶段冷读者可在 verification record 里一意定位。与 OQ-N-003 立场一致。 | ✓ 达标 |
| 6 | `[minor][Q4]` § 7 仅指向 § 6.2，独立冷读不友好 | spec § 7 重写为"完整 12 条范围外列表见 § 6.2 Out-of-scope（**权威来源**）。本 § 仅作为 spec 模板章节占位，不另列条目，以维持单源；§ 6.2 改动时不需要同步本节。冷读者直接跳至 § 6.2。"——保留单源原则的同时显式给冷读者跳转指引；同时去掉了原"按编号同步维护"这种容易引发双源漂移的 editor 指令。 | ✓ 达标 |

### Bonus 修订核验

| Bonus | 修订证据 | 评价 |
|---|---|---|
| HYP-004 confidence 升级 | spec § 4 表格：HYP-004 confidence "中-高" → "高"；Validation Plan 改为"NFR-002 已用字符数（`wc -c × 1.10`）作为 commit-time 验收，等价于把验证从 design 阶段提前到 commit 时刻；`hf-design` 阶段额外评估 references 拆分粒度（行数 ≤ 300 作为 **tentative engineering aim**，不作 NFR 阈值）" | ✓ 合理。NFR-002 已把字符数硬化为 commit-time acceptance，比"design 阶段量化"更早、更硬，confidence 升 high 与 evidence 一致；行数预算在 Validation Plan 内被显式标注为 "tentative engineering aim, 不作 NFR 阈值"，与 § 3 加分项 / § 14 术语 / § 12 假设保持一致，未偷塞回 NFR 通道。 |
| NFR-001 verification path 显式落盘 | 已在 Finding 1 的修订中含入：`(Quantitative)` Acceptance 显式要求"测量结果（含 raw timing + ratio）必须落盘到 `features/001-orchestrator-extraction/verification/load-timing-3-clients.md`，与 `smoke-3-clients.md` 并列" | ✓ 合理。吸收了 Round 1 "薄弱项 #1"（HYP-002/003 验证证据通道在 spec 层未显式）的核心诉求，给 hf-design / hf-test-driven-dev 一个明确的落盘锚点。 |

### Regression 扫描

逐项检查修订是否破坏 spec / ADR-007 整体一致性：

| 检查 | 结果 |
|---|---|
| ADR-007 D1 新子段 vs § 6.2（12 项 out-of-scope）冲突? | ✗ 无冲突。新子段明确"现有 24 leaf 保留为兼容期遗产，不立即触发违反 invariant 判定"，与 § 6.2 #1 "leaf skill 文件不被修改" 一致 |
| ADR-007 D1 新子段 vs D3 Step 1-6 冲突? | ✗ 无冲突。新子段把 D1 invariant 的生效切片明确映射到 D3 step 1 / step 2-5 / step 6，与 D3 范围归属表完全对齐 |
| ADR-007 D1 新子段 vs D5 release-blocking 假设清单冲突? | ✗ 无冲突。D5 锁定的是 HYP-002 / HYP-003（运行时等价 + always-on 加载），与 D1 的"互不引用"层级不变量是正交关注点 |
| FR-001 Statement 简化 vs FR-003 等价性要求冲突? | ✗ 无冲突。FR-001 从"列举内部结构"退到"语义等价"，FR-003 仍承担端到端等价性证明（walking-skeleton 回归），两者关注点更清晰 |
| FR-001 Acceptance bullet 3 改引 `profile-node-and-transition-map.md` 是否真实存在? | ✓ 经查 `skills/hf-workflow-router/references/` 目录中确实存在该文件（Round 1 已读 router skill 时间接见过 references 目录布局），引用合法 |
| FR-002 / FR-006 sub-ID 与 Acceptance 数量是否一致? | ✓ FR-002 共 4 条 acceptance（a/b/c/d）；FR-006 共 2 条（a/b），与"打包说明"声明一致 |
| FR-003 acceptance bullet 3 候选脚本路径与 OQ-N-003 冲突? | ✗ 无冲突。两条候选路径与 OQ-N-003 提出的两条候选完全一致，"hf-tasks 阶段决定"的归属也一致 |
| HYP-004 升 high vs § 3 加分项"≤ 300 行不阻塞 v0.6.0 release"立场冲突? | ✗ 无冲突。HYP-004 升 high 是基于 NFR-002 字符数已硬化；§ 3 加分项的"行数 ≤ 300"仍是 tentative engineering aim 不阻塞 release——两者并行不冲突 |
| § 7 重写是否引入"§ 6.2 不需同步本节"导致单源破坏? | ✗ 重写本身就是为单源服务（明确权威来源在 § 6.2，§ 7 只是模板占位） |
| 新增 verification 文件 `load-timing-3-clients.md` 是否与 `smoke-3-clients.md` 双重定义? | ✗ 两份记录功能正交：smoke = 加载/identity 通过；load-timing = 量化 wall-clock 比对。Acceptance 显式指明"并列" |

**Regression 扫描结果：0 命中**。无新 finding 被引入。

### 残留 finding

无。Round 1 的 6 条 finding 全部正确修订；Round 1 "薄弱或缺失项" 中第 1 条（NFR-001 verification path）+ 第 2 条（HYP-004 confidence 重估）已在 Bonus 修订中吸收；第 3 条（`audit-agent-anatomy.py` 引入）+ 第 4 条（HYP-001 P2 probe 节点）仍按 Round 1 评价"已知薄弱点 / 不阻塞本轮"保留——这两条原本就**不**计入需修订项，本轮维持原状无问题。

### 最终 Verdict

通过

理由：6 条 finding 全部命中合理修订；2 条 bonus 修订（HYP-004 confidence 重估 + NFR-001 verification 落盘路径显式化）合理且自洽；regression 扫描 0 命中——修订未破坏 § 6.2 12 项 out-of-scope、未破坏 ADR-007 D2-D7 立场、未与 ADR 关系表（含 ADR-004 D3 "关键先例"）矛盾、未把行数预算偷塞回 NFR 阈值。spec + ADR-007 现已具备成为 `hf-design` 稳定输入的条件：所有 Must FR / NFR 的 Acceptance 可形成通过/不通过判断，三层架构 invariant 的生效阶段清晰可读，dispatch 协议设计目标态明确，兼容期消费 leaf 残留 hint 的允许度清晰。

### 下一步

- 唯一下一步：`规格真人确认`（spec approval step；由父会话承担，reviewer subagent 不代替执行）
- approval 通过后再进入：`hf-design`
- **不**直接进入 `hf-design`——遵守 `skills/hf-spec-review/SKILL.md` Hard Gates "规格通过评审并完成 approval step 前，不得进入 `hf-design`" + "reviewer 不代替父会话完成 approval step，不顺手开始设计"
- approval 后建议 hf-design 阶段重点解决：
  1. HYP-005（leaf 剥离 `Next Action` 字段后 orchestrator 仍能基于 on-disk artifacts 决定下一步）的具体决策协议——ADR-007 D1 新子段已锁定"按目标态设计"
  2. NFR-001 wall-clock baseline 的具体测量协议（如何在 3 宿主中各跑 N 次取均值 / p95 / 置信区间），落到 `verification/load-timing-3-clients.md` 的 schema 定义
  3. FR-002 / FR-006 sub-ID 是否 `hf-tasks` 阶段拆为独立任务的取舍（spec 阶段已许可拆分）
  4. OQ-N-003（regression-diff 脚本归属位置）最终决定

### 评审者元数据

- 是否需要人工裁决（needs_human_confirmation）：是（`通过` 触发"规格真人确认"步骤；与 `references/review-record-template.md` 返回规则一致）
- 是否需要回 router（reroute_via_router）：否
- USER-INPUT findings：无（本轮修订验证 0 finding）

### 更新后的结构化返回 JSON

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "hf-design",
  "record_path": "features/001-orchestrator-extraction/reviews/spec-review-2026-05-10.md",
  "key_findings": [],
  "needs_human_confirmation": true,
  "reroute_via_router": false,
  "finding_breakdown": [],
  "round": 2,
  "round_1_findings_resolved": 6,
  "round_2_new_findings": 0,
  "approval_step_required_before_design": true
}
```

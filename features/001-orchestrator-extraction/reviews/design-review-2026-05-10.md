# Design Review: HF Orchestrator Extraction & Skill Decoupling

- 评审对象:
  - Design: `features/001-orchestrator-extraction/design.md`
- 上游证据:
  - 已批准 Spec: `features/001-orchestrator-extraction/spec.md`（spec-review Round 2 verdict = `通过`，approval step 由父会话承担）
  - 上游 ADR: `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`
  - Spec-review handoff: `features/001-orchestrator-extraction/reviews/spec-review-2026-05-10.md` § "下一步" Round 2 末尾 4 项
  - 设计模板: `skills/hf-design/references/design-doc-template.md`
- 评审 skill: `hf-design-review`
- 评审者: 独立 reviewer subagent（与 author 分离，符合 Fagan）
- 评审时间: 2026-05-10
- 评审方法: 6 维 rubric (`D1`–`D6`) + 反模式扫描 (`A1`–`A11`) + 上游 handoff 吸收核验 + 与 spec / ADR-007 一致性核验

## Precheck

| 检查项 | 结果 |
|---|---|
| 设计草稿存在且可定位 | ✓ `features/001-orchestrator-extraction/design.md` 21 章节 + 状态同步段 |
| 上游 spec 可回读 | ✓ 已批准（spec-review Round 2 通过；approval step 由父会话承担） |
| ADR-007 可回读 | ✓ |
| Author / Reviewer 分离 | ✓ 父会话起草，本 reviewer subagent 独立 |
| Stage / route / evidence 一致 | ✓ design 自报 `Current Stage: hf-design`、`Next Action: hf-design-review`；本次评审正是该指向 |
| 章节骨架与 `design-doc-template.md` 一致 | ✓ 21 章节顺序与默认结构一致；§ 4 / § 4.5 / § 5 / § 14 / § 15 Phase 0 锚点全部就位 |

Precheck 通过，进入正式 rubric。

## 上游 handoff 吸收核验（spec-review Round 2 § "下一步"）

| Handoff 项 | 应在 design 中落地 | 落地证据 | 结果 |
|---|---|---|---|
| 1. HYP-005 dispatch 协议（剥离 `Next Action` 字段后 orchestrator 仍能基于 on-disk artifacts 决定下一步） | dispatch 协议目标态决策 | **D-Disp** + § 12.3：v0.7.0+ 纯 on-disk artifact 驱动（4 类输入：progress / spec/design/tasks frontmatter / reviews / verification）；v0.6.0 兼容期允许同时消费 leaf 残留 `Next Action` 字段，但**冲突时以 artifact 为权威**；与 ADR-007 D1 "生效阶段" 子段（v0.6.0 architectural commitment / v0.7.0+ runtime enforcement）逐条对齐 | ✓ |
| 2. NFR-001 wall-clock baseline 测量协议 | 3 宿主同口径采集 schema | **D-NFR1-Schema**：每宿主 5 次重复取均值；baseline = v0.5.1 HEAD（旧路径）/ candidate = v0.6.0 HEAD（新路径），跨 git checkout 测量；3 宿主 × 2 group × 5 次 = 30 次测量；落盘 `verification/load-timing-3-clients.md`；在 § 14 NFR-001 行复述 | ✓ |
| 3. FR-002 / FR-006 sub-ID 是否拆任务 | 取舍说明（spec 阶段已许可拆分） | **D-FR2-Tasks**：FR-002 拆 4 个独立任务（002a/b/c/d），FR-006 拆 2 个（README ×2 + setup docs ×3）；理由（每宿主修改面 / 验收路径 / 失败模式独立）；具体拆解推迟到 hf-tasks 阶段 | ✓ |
| 4. OQ-N-003 regression-diff 脚本归属位置 | 最终决定 | **D-RegrLoc**：物理位置 = `features/001-orchestrator-extraction/scripts/regression-diff.py`，**不**入 `skills/hf-finalize/scripts/`；理由清晰（一次性 / 不属 hf-finalize SOP / ADR-006 D1 4 类子目录约定不适用 skill-owned 通用化）；附"如未来证明通用化可后续 ADR 升级"的逆向通道 | ✓ |

4 条 handoff **全部命中**且各自给出可冷读的决策 ID + 理由。

## 6 维 rubric 评审

| 维度 | 评分 | 关键观察 |
|---|---|---|
| **D1 需求覆盖与追溯** | 9/10 | § 3 traceability 表把 spec FR-001…FR-007 / NFR-001…NFR-005 / HYP-002 / HYP-003 / HYP-005 全部映射到 design 章节；FR-005 (ADR-007 锁定立场) 显式标"不在本 design 修改"——单源正确未漂移；§ 2 设计驱动因素表与 spec NFR-001…NFR-005 + ADR-007 D1/D2/D4 对齐 |
| **D2 架构一致性** | 9/10 | § 10 提供 C4 Context / Container / Component 三层视图（mermaid + 章节序列）；§ 11 14 模块表显式 "职责 / 不做" 双栏；§ 12 双向时序图（always-on 加载 + per-message operating loop）；Front Controller 模式声明明确"沿用现有 router 已声明的立场，本 design 不引入新模式"；DDD 战略 / 战术建模显式跳过且理由可冷读（BC=1，无并发/事务/Domain Event/跨聚合不变量），符合 `design-doc-template.md` "未触发时显式跳过并说明理由" |
| **D3 决策质量与 trade-offs** | 8/10 | § 7 / § 8 比较 3 个真实可行方案 (A 单文件 / B 主+references / C 选择性内联)，每个方案在 8 个维度（NFR-002 字符数 / Token / progressive disclosure / 物理迁移成本 / 维护一致性 / FR-001 等价 / ADR-007 D2 single source / walking-skeleton 回归）下显式对比；选定 B 的理由 reviewer 可冷读不需从 prose 猜；§ 9.2 共 15 条 D-X 决策表（决策 / 来源 / 可逆性）— **见 Finding 1（§ 8 baseline 数值不准）+ Finding 2（§ 19 称 "12 条" 与实际 15 条不符）** |
| **D4 约束与 NFR 适配** | 9/10 | § 14 NFR QAS 承接表覆盖 NFR-001…NFR-005，每条含 模块 / 机制 / observability / 验证；spec C-001…C-006 约束被吸收（C-005 schema fallback → D-Host-CC；C-006 30 行 → D-Stub；ADR-006 D1 4 类子目录不适用 → D-RegrLoc 理由）；NFR-002 字符数预算契约在 § 13.1 用 `wc -c` 表达，表述与 spec NFR-002 acceptance 一致 |
| **D5 接口与任务规划准备度** | 8/10 | § 13 五个子契约（Orchestrator main / References / Deprecated alias stub / Host always-on stub / regression-diff 脚本）边界稳定可冷读；§ 18 任务规划准备度显式声明并给出关键路径与并行度（3 宿主 stub 可并行 / D-FR2-Tasks 已划分粒度）；§ 11 14 模块均给出文件路径，hf-tasks 可直接拆任务无空洞 |
| **D6 测试准备度与隐藏假设** | 9/10 | § 16 walking-skeleton 实施 step-by-step + NFR 验证矩阵 + release-blocking HYP-002 / HYP-003 显式承接 ADR-007 D5；§ 17 6 类失败模式 + 缓解；§ 21 4 条 OQ-D-xxx 非阻塞开放问题，每条均给归属阶段（hf-tasks / hf-test-driven-dev）；隐藏假设（如 `git mv` vs 新建+删除、baseline commit 选 v0.5.1 vs v0.5.0）显式登记在 § 21 |

**关键阈值检查**：所有 6 维 ≥ 8/10；无维度低于 6/10 → 不触发"不得返回 通过"。

## 反模式扫描（`A1`–`A11`）

| ID | 命中? | 说明 |
|---|---|---|
| A1 无 NFR 评估 | ✗ | § 14 NFR QAS 承接表完整 |
| A2 只审 happy path | ✗ | § 17 失败模式 6 条；§ 13.4 含 D-Host-CC fallback / D-Host-OC 追加段不覆盖 |
| A3 无权衡文档 | ✗ | § 8 紧凑矩阵；§ 9.2 D-X 决策表显式列可逆性 |
| A4 SPOF 未记录 | ✗ | 静态 markdown + 宿主原生 always-on 注入；§ 17 已含 Cursor mdc 加载失败 / Claude Code plugin schema fallback / OpenCode AGENTS.md 覆盖等场景 |
| A5 实现后评审 | ✗ | 当前 stage 是 hf-design-review，符合"实现前评审" |
| A6 上帝模块 | ✗ | § 11 把职责拆分到 14 个独立模块，每个有"职责 / 不做"双栏 |
| A7 循环依赖 | ✗ | § 11 references 模块明确"不互相引用形成环" |
| A8 分布式单体 | ✗ | 不涉及微服务 |
| A9 task planning gap | ✗ | § 18 显式声明 readiness；§ 13 接口契约稳定；hf-tasks 不需替补设计 |
| A10 tactical-model-absent | ✗ | § 4.5 显式说明触发条件无一满足 + 跳过理由 |
| A11 upfront-gof-pattern | ✗ | § 6 显式声明"不引入新 GoF 代码模式 / GoF 模式由 hf-test-driven-dev REFACTOR 步浮现"；Front Controller 是 PEAA/J2EE 架构层模式（沿用现有 router 已声明立场），不属于 emergent GoF 范畴 |

无反模式命中。

## 特殊关注核验（父会话 7 项）

| # | 关注项 | 核验 | 结果 |
|---|---|---|---|
| 1 | 4 项 spec-review R2 handoff 全部落地 | 见上方 handoff 吸收核验表 | ✓ 4/4 全部落地 |
| 2 | NFR-002 字符数预算（B ≤ baseline × 1.10） | baseline 实测 = 21,132 bytes（`wc -c skills/{using-hf-workflow,hf-workflow-router}/SKILL.md`）；baseline × 1.10 = 23,245 bytes ≈ 22.7 KB；B 候选声明 ≤ 12 KB（≤ 12,288 bytes）→ 通过；A (~80-90KB) 失败、C (~30KB) 失败；选定 B 的判定结论与实测一致 | ✓（结论正确）；§ 8 表内"baseline ≈ 14KB" 是数值不准 → 见 Finding 1 |
| 3 | D-Disp 区分 v0.6.0 兼容 hint vs v0.7.0+ 权威，与 ADR-007 D1 生效阶段一致 | D-Disp 两阶段切片：v0.6.0 = 设计目标态 + 实施时双向支持；v0.7.0+ = 删 leaf 字段后纯 artifact；§ 12.3 给出"冲突时以 artifact 为权威"硬权威序；ADR-007 D1 "生效阶段（Architectural Commitment vs Runtime Enforcement）"子段一对一映射 | ✓ |
| 4 | Bounded Context = 1 / DDD 跳过是否被合理化 | § 4 / § 4.5 双段显式跳过；理由覆盖 BC 数量、跨 Context 交互、术语一致性、并发/事务/Domain Event/跨聚合不变量 5 项触发条件；与 `design-doc-template.md` "未触发时显式跳过并说明理由" 一致 | ✓ 不构成对 design SKILL.md MUST DO 的违反 |
| 5 | STRIDE 跳过触发条件 | § 15 三项触发条件逐条核：Spec 无 Security NFR（核 spec § 9 NFR-001…NFR-005 维度，确无 Security）✓；无跨信任边界（HF persona 在用户本地宿主内运行；spec § 10 "不涉及外部 API / 服务依赖"）✓；不处理 PII / 敏感数据（spec 无任何 PII / secret 字段）✓ | ✓ STRIDE 跳过合法 |
| 6 | D-X 决策与 spec § 6.2 12 项 out-of-scope 不冲突 | 逐项核（leaf 不被修改 / 旧 skill 不删除 / closeout schema 不变 / verdict 词表不变 / hf-release 不变 / audit-skill-anatomy.py 不变 / hf-finalize 6A 不变 / 不新增 hf-* skill / 不引新 slash 命令 / 不投资第三方独立消费 / agents/ 无 specialist personas / .cursor/rules/ 不引入新 mdc 文件）：D-Mig 仅迁移 hf-workflow-router 的 references 不动其它 leaf；D-Stub 只对 using-hf-workflow / hf-workflow-router 转 alias（spec § 6.2 #2 允许的例外）；D-Host-Cursor 修改现有 `.cursor/rules/harness-flow.mdc`，**不**新建 mdc 文件（与 § 6.2 #12 一致）；D-Skip-Threat 不引入 security 关注（与 § 6.2 #11 personas 边界正交，但同向） | ✓ 0/12 命中 |
| 7 | § 18 task planning readiness 粒度 | § 11 14 模块每个有具体路径；D-FR2-Tasks 已预拆 sub-task 边界（FR-002a/b/c/d / FR-006a/b）；§ 18 明确并行度 + 关键路径；hf-tasks 进入时无须替设计补洞 | ✓ |

## 发现项

- **[minor][LLM-FIXABLE][D3] § 8 trade-off 表把 baseline 标为 "约 14KB" 与实测不符。** § 8 第 1 行 "baseline 是合并的 359 行 SKILL.md，约 14KB"；实测 `wc -c skills/using-hf-workflow/SKILL.md skills/hf-workflow-router/SKILL.md` = 21,132 bytes ≈ **20.6 KB**（不是 14 KB）。**结论不变**（baseline × 1.10 = 22.7 KB；B ≤ 12 KB 通过；A ~80–90 KB 失败；C ~30 KB 失败）；但 § 13.1 契约 `wc -c agents/hf-orchestrator.md ≤ wc -c skills/{using-hf-workflow,hf-workflow-router}/SKILL.md × 1.10` 用的是动态计算，比 § 8 的 hardcoded 14KB 更可靠。建议在 § 8 把 "约 14KB" 改为 "约 20.6 KB（实测 21,132 bytes）"，或直接引用 § 13.1 的动态契约消除双源数值。不阻塞 hf-tasks 启动。

- **[minor][LLM-FIXABLE][D3] § 19 称 "12 条 D-X 决策"，与 § 9.2 表实际 15 条不符。** § 9.2 列表为 D-Layout / D-Disp / D-Mig / D-Stub / D-Stub-Marker / D-Host-Cursor / D-Host-CC / D-Host-OC / D-Identity / D-NFR1-Schema / D-RegrLoc / D-RegrImpl / D-FR2-Tasks / D-Skip-DDD / D-Skip-Threat = **15 条**；§ 19 写 "本 design 的 12 条 D-X 决策（§ 9.2 表）"。建议把 § 19 数字改为 "15 条"，或在 § 9.2 表后面加一行 "共 15 条 D-X 决策"。轻量 wording 修订，不影响任何决策内容。

- **[minor][LLM-FIXABLE][D5] § 18 关键路径写 "main 先建，否则 stub redirect 目标不存在"，对 git 提交顺序的限制过严。** Redirect stub 内容只是 markdown 文本指向 `agents/hf-orchestrator.md`，目标文件即使在同一 commit 中创建也不构成"目标不存在"——HF 既有的 v0.5.1 commit 模式（`render-closeout-html.py` 迁移）已证明同 commit 创建 + stub 同步是合法操作。建议把"main 先建"改为"main 与 stub 在同一 commit 创建"或"main 必须在 stub 之前或同 commit 创建"。不影响 hf-tasks 拆解，但有可能误导 hf-tasks 阶段把这两个任务硬编码为前后串行（损失并行度）。

## 缺失或薄弱项

- **D-NFR1-Schema 简化（v0.5.1 HEAD vs v0.6.0 HEAD 跨 git checkout 测量）的可重复性约束未显式落到 verification 模板。** § 14 NFR-001 行 + D-NFR1-Schema 已写"5 次重复取均值 / 跨 checkout 测量"，但 `verification/load-timing-3-clients.md` 的 schema（应记录哪些字段：宿主 / git SHA / 5 次 raw / mean / ratio / pass-fail）尚未在 design 阶段固化；hf-tasks 阶段需要补一个 verification record 模板任务。属"已知薄弱点"，不阻塞通过。

- **OQ-D-002（walking-skeleton baseline 用 v0.5.1 commit 还是 v0.5.0 commit）会影响 D-NFR1-Schema 的"v0.5.1 HEAD"语义。** 若 hf-tasks 阶段最终选 v0.5.0，则 D-NFR1-Schema 中"v0.5.1 (旧路径) HEAD"需同步改为 v0.5.0；建议在 hf-tasks 阶段把 OQ-D-002 与 NFR-001 measurement script 任务编排为前后依赖。属"已知薄弱点"。

- **`agents/` 目录的 anatomy audit（候选 `audit-agent-anatomy.py`）未在 design 中给出后续 ADR 钩子。** ADR-007 D2 把这条推给"后续 ADR 决定"；design § 20 显式排除"不为 agents/ 目录引入 anatomy audit"。当前不阻塞；若 v0.6.x / v0.7.0 引入更多 personas，需开 ADR-008 决定。已被 spec-review Round 1 "薄弱项 #3" 提及，本轮维持原判定。

## 结论

**通过**

理由：6 维 rubric 全部 ≥ 8/10（D1 9 / D2 9 / D3 8 / D4 9 / D5 8 / D6 9）；反模式 0/11 命中；spec-review Round 2 末尾 4 项 handoff 全部落地（D-Disp / D-NFR1-Schema / D-FR2-Tasks / D-RegrLoc，每条均可冷读决策 ID + 理由）；NFR-002 字符数预算的选定方案 (B) 在实测 baseline (21KB × 1.10 = 22.7KB) 下仍稳健通过，A / C 候选确为应剪枝；D-Disp 两阶段切片与 ADR-007 D1 "生效阶段" 子段（v0.6.0 architectural commitment / v0.7.0+ runtime enforcement）逐条对齐；DDD 战略 / 战术建模跳过有合规理由（BC=1、无触发条件）；STRIDE 跳过的 3 个触发条件逐条核对均不命中；15 条 D-X 决策与 spec § 6.2 12 项 out-of-scope **0/12 命中**；§ 18 task planning readiness 粒度足够 hf-tasks 直接拆任务（14 模块 + 4 handoff + 关键路径 + 并行度全有）。3 条 minor finding 全部 LLM-FIXABLE，可在 hf-tasks 启动前 1 轮快速修订；薄弱项均为"hf-tasks 阶段补 verification 模板 / 解决 OQ-D-002 排序" 类下游事项，不构成本轮阻塞。设计可成为 hf-tasks 的稳定输入。

## 下一步

- 唯一下一步：**`设计真人确认`**（`needs_human_confirmation = true`，由父会话承担 approval step）
- approval 通过后再进入 `hf-tasks`
- **不**直接进入 `hf-tasks`：遵守 `hf-design-review` Hard Gates "设计未通过评审并完成 approval step 前，不得进入 `hf-tasks`" + "reviewer 不代替父会话完成 approval step"
- 修订建议（可选，不阻塞 approval）:
  1. § 8 把 baseline 数值 "约 14KB" 修正为 "约 20.6 KB（实测 21,132 bytes）" 或引用 § 13.1 的动态契约
  2. § 19 把 "12 条 D-X 决策" 数字修正为 "15 条"，或在 § 9.2 表末加 "共 15 条" 备注
  3. § 18 关键路径中 "main 先建" 软化为 "main 与 stub 同 commit 创建" 以保留 hf-tasks 并行度

## 评审者元数据

- 是否需要人工裁决（needs_human_confirmation）：**是**（`通过` 触发"设计真人确认"步骤；与 `references/review-record-template.md` 返回规则一致）
- 是否需要回 router（reroute_via_router）：**否**（route / stage / evidence 一致，无 workflow blocker）
- USER-INPUT findings：**无**（3 条 minor finding 全部 LLM-FIXABLE，由 `hf-design` 起草节点直接修订；不需要业务裁决 / 外部阈值 / 真人拍板）

## 结构化返回 JSON

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "设计真人确认",
  "record_path": "features/001-orchestrator-extraction/reviews/design-review-2026-05-10.md",
  "key_findings": [
    "[minor][LLM-FIXABLE][D3] § 8 trade-off 表 baseline 标 ~14KB 与实测 21KB 不符；选定方案 B 的结论不变",
    "[minor][LLM-FIXABLE][D3] § 19 称 '12 条 D-X 决策' 与 § 9.2 表实际 15 条不符",
    "[minor][LLM-FIXABLE][D5] § 18 关键路径 'main 先建' 限制过严；建议软化为 'main 与 stub 同 commit'"
  ],
  "needs_human_confirmation": true,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "D3",
      "summary": "§ 8 trade-off 表把 baseline 标为 '约 14KB'，实测 wc -c = 21,132 bytes ≈ 20.6 KB；选定方案 B (≤ 12KB) 在实测 baseline × 1.10 = 22.7 KB 下仍通过，A/C 仍应剪枝，结论不变；建议改为 '约 20.6 KB（实测 21,132 bytes）' 或引用 § 13.1 动态契约消除双源数值"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "D3",
      "summary": "§ 19 写 '本 design 的 12 条 D-X 决策（§ 9.2 表）'；§ 9.2 实际有 15 条（含 D-Skip-DDD / D-Skip-Threat 等）；建议数字改 15 或在 § 9.2 表末加 '共 15 条' 备注"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "D5",
      "summary": "§ 18 关键路径 'main 先建，否则 stub redirect 目标不存在' 对 git 提交顺序的限制过严；同 commit 中创建 main + stub 完全合法（v0.5.1 render-closeout-html.py 迁移先例）；建议软化为 'main 与 stub 同 commit 创建'，避免 hf-tasks 阶段误把两者硬编码为前后串行损失并行度"
    }
  ],
  "approval_step_required_before_tasks": true
}
```

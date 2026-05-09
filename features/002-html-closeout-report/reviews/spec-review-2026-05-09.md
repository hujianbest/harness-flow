# Spec Review — 002-html-closeout-report

- 日期: 2026-05-09
- Reviewer: independent reviewer subagent（与 author 不同会话，遵循 Fagan author/reviewer 分离）
- 被审对象:
  - `features/002-html-closeout-report/spec.md`
  - `features/002-html-closeout-report/README.md`
  - `features/002-html-closeout-report/progress.md`
- 工作流位置: Profile=`full` / Mode=`interactive` / Isolation=`in-place`，stage 由 router 锁定为 `hf-specify` 完成、待 `hf-spec-review`
- 上游证据: 无 product-discovery 上游；用户原话已在 spec §1 引用；Phase 0 anchors 仍按 hf-specify hard requirement 评估
- 评审依据:
  - `skills/hf-spec-review/references/spec-review-rubric.md`
  - `skills/hf-specify/references/requirement-authoring-contract.md`
  - `skills/hf-specify/references/nfr-quality-attribute-scenarios.md`
  - `skills/hf-specify/references/success-metrics-and-hypotheses.md`
  - `skills/hf-specify/references/granularity-and-deferral.md`
  - `skills/hf-finalize/SKILL.md` + `references/finalize-closeout-pack-template.md`（理解被改造对象）
  - `docs/principles/sdd-artifact-layout.md`
  - `docs/decisions/ADR-003-release-scope-v0.3.0.md`

## 结论

需修改

## Precheck

- [x] 稳定 spec 草稿存在（`features/002-html-closeout-report/spec.md`，24 KB，14 节）
- [x] stage / profile / mode 已锁定，与 `progress.md` Next Action 一致
- [x] 无 route / stage / 证据冲突；不需要 reroute via router
- [x] 项目级骨架（`docs/principles/sdd-artifact-layout.md`）与 spec 章节顺序语义可回读
- [x] ADR-003 与本 feature 不冲突：本 feature 修改既有 `hf-finalize`（D2 仅禁"新增 `hf-*` skill"），未改主链终点（D4），未引入 personas（D3），未承诺 v0.3.0 GA 时间窗

Precheck 通过 → 正式 rubric。

## 形态契约确认（Group C / C4）

- spec 14 节顺序与 hf-specify 默认骨架一致（背景 / 目标 / Success Metrics / Key Hypotheses / 用户角色 / 范围内 / 范围外 / FR / NFR / 接口依赖 / 约束 / 假设 / 开放问题 / 术语）
- 单条 FR / NFR 已具备 `ID` / `Statement` / `Acceptance` / `Priority` / `Source` 字段，BDD Given/When/Then 形式落地
- 所有 6 条 NFR 用 ISO 25010 维度归类 + QAS 五要素 + Acceptance
- README / progress 字段与 sdd-artifact-layout 约定一致
- Template alignment 通过

## Group Q（Quality Attributes）

| ID | 检查 | 结论 | 备注 |
|---|---|---|---|
| Q1 Correct | 每条核心需求都能回指来源 | 通过 | 6 FR + 6 NFR 全部含 `来源` 锚点（用户原话 / HYP / 项目纪律） |
| Q2 Unambiguous | 模糊词已量化 | 大致通过 | 极少残留：§2 "5 分钟内" 未在 §3 Outcome Metric 闭环，见 finding F-10 |
| Q3 Complete | 关键输入/输出/错误路径覆盖 | 大致通过 | render-failed / project-disabled / 缺工件降级 / 非法 coverage 值都有；FR-003 多源冲突未定义，见 F-3 |
| Q4 Consistent | 需求间无冲突 | 部分不通过 | F-3（FR-003 多源优先级）；F-5（FR-001 AC3 与 FR-005 AC1 互写） |
| Q5 Ranked | 优先级显式 | 通过 | MoSCoW 标注；FR-005 唯一 Should，其余 Must |
| Q6 Verifiable | 可形成通过/不通过判定 | 通过 | NFR Response Measure 全部含阈值或可执行判定（grep / wc -c / scrollWidth ≤ clientWidth 等） |
| Q7 Modifiable | 同需求未散落多处重复 | 部分不通过 | F-5 重复；F-6 NFR-002 把 Portability + Compatibility 混写于一条 |
| Q8 Traceable | 关键需求有 ID + Source | 通过 | FR/NFR/CON/HYP 全部有稳定 ID |

## Group A（Anti-Patterns）

| ID | 检查 | 结论 | 备注 |
|---|---|---|---|
| A1 模糊词 | — | 大致通过 | "更可读和直观" 已通过 §3 Outcome Metric (4/5 题) 量化 |
| A2 复合需求 | — | 部分不通过 | F-6 NFR-002 跨两个 ISO 25010 子树 |
| A3 设计泄漏 | — | **不通过** | F-1 / F-2 / F-7 / F-8（Python / 标准库 / `string.Template` / 具体脚本路径 / `<a href>` 标签 / CLI 形式） |
| A4 无主体被动表达 | — | 通过 | EARS 句式，主体均为"系统" |
| A5 占位/待定值 | — | 通过 | 无 `TBD` / `待确认` 进入核心 FR/NFR |
| A6 缺少负路径 | — | 通过 | render-failed、缺工件、非法 coverage、disabled、缺工件链接、XSS payload 都有 |

## Group C（Completeness And Contract）

| ID | 检查 | 结论 | 备注 |
|---|---|---|---|
| C1 Requirement contract | — | 通过 | 全部 FR/NFR 满足最小字段 |
| C2 Scope closure | — | 通过 | §6 / §7 范围内外双向闭合 |
| C3 Open-question closure | — | 通过 | 3 条 OQ 均非阻塞；OQ-003 已给出默认行为（覆盖、历史从 git 取） |
| C4 Template alignment | — | 通过 | 见上节 |
| C5 Deferral handling | — | **不通过** | F-4：§7 把"硬非目标"和"未来 increment 候选"混写在 prose；未落 `spec-deferred.md`，hf-increment 无法稳定回收 |
| C6 Goal & success criteria | — | 大致通过 | §3 Outcome / Threshold / Leading / Lagging / Measurement / Non-goal / Instrumentation Debt 全部存在；F-10（5 分钟时限未闭环）为 minor |
| C7 Assumption visibility | — | 大致通过 | 4 条 HYP 含 Type/Impact/Confidence/Validation/Blocking；F-9：缺一条显式的 Desirability/Usability 假设回扣 §3 outcome |

## Group G（Granularity And Scope-Fit）

| ID | 检查 | 结论 | 备注 |
|---|---|---|---|
| G1 Oversized FR | — | 通过 | 未命中 GS1-GS6；FR-001/002/006 在"产出 HTML"语义上**没有**重叠：分别约束触发 / 内容章节 / 链接可达 |
| G2 Mixed release boundary | — | 通过 | 当前轮 vs 后续增量边界清晰；问题落在 C5（应迁入 deferred backlog） |
| G3 Repairable scope | — | 通过 | findings 收敛，预计 1 轮可定向回修 |

## 发现项

> 标签 `[severity][classification][rule_id] 简述`。证据均锚定到 spec 行级片段，无"感觉不好"。

### Important

- `[important][LLM-FIXABLE][A3]` **F-1：§6 把"实现选择"硬编码进 spec**。原文："渲染器：单 Python 文件（路径默认 `scripts/render-closeout-html.py`），仅依赖标准库。"以及 §10、CON-001 等处。"无第三方依赖"作为 CON 是合理的项目纪律约束（保留），但"具体语言=Python / 单文件 / 具体路径=`scripts/render-closeout-html.py`"属于 design 阶段决策。建议把 §6 的语言/路径细节挪走，CON-001 仅声明"渲染器不引入新的运行时依赖（包括第三方 Python 包 / Node 包 / 字体 / 图片 CDN）"，具体路径与文件数留给 design。
- `[important][LLM-FIXABLE][A3]` **F-2：HYP-004 Validation Plan 泄漏实现原语**。原文："用 `string.Template` + `html.escape` + `re` 实现章节解析与渲染"。Validation Plan 应描述"用什么样的 probe 验证假设可行"，而具体 API 选择是 design 输出。建议改写为"design 阶段产出最小渲染 spike，验证仅依赖标准库即可解析章节、转义文本、渲染表格 / 进度条"。
- `[important][LLM-FIXABLE][Q4]` **F-3：FR-003 多源优先级与冲突未定义**。当前 4 条 Acceptance 在以下两个边界处不可判定：
  1. `evidence/coverage.json` 与 `verification/regression-*.md` Coverage 行**同时存在**且数值不一致时，HTML 显示哪一个？AC 顺序暗示 coverage.json 优先，但未显式声明。
  2. `coverage.json` 存在但**缺失 `lines.pct`**（schema 不完整）时，应回落到 AC2（regression 行）、AC3（N/A）还是 AC4（Invalid）？当前 AC1 要求"符合最小 schema"，schema 不符时落点未指明。
  建议在 FR-003 增加 1 条优先级 Acceptance：例如 "Given `coverage.json` 与 `verification/*` 都提供数值，When 渲染，Then 系统优先使用 `coverage.json`，并在卡片下方注明被忽略的次级来源"，并在 AC4 之前增补 "Given `coverage.json` 存在但缺 `lines.pct`，Then 视为 AC1 不命中并继续按优先级回落到 AC2"。
- `[important][LLM-FIXABLE][C5]` **F-4：§7 范围外把"硬非目标"和"future increment 候选"混写在 prose**。当前 §7 9 条之中至少 4 条是真实 deferred capability、不是 hard non-goal：
  - "覆盖率数据采集本身"（HYP-002 失效影响段已写"后续 increment 需考虑接入"，明确是 future）
  - "PDF / DOCX 导出"
  - "i18n 双语切换"
  - "CI 集成（GitHub Actions / GitLab CI 模板）"
  - 可争议："跨 feature dashboard"、"HTML 内嵌交互式查询"
  其余（"取代 closeout.md" / "Jinja2 等第三方依赖" / "GitHub Pages 托管" / "自动 release notes 文案"）才是 hard non-goal。按 `granularity-and-deferral.md` 与 `docs/principles/sdd-artifact-layout.md`，真实 deferred capability **必须**进入 `features/002-html-closeout-report/spec-deferred.md` 且每条带 Source ID / Priority / Deferral Reason / Re-entry Hint / Recommended Skill (`hf-increment`)；§7 仅保留 hard non-goals 并补一行链接到 `spec-deferred.md`。spec §7 末尾"如有，本轮可暂不创建"是这里的 root cause，应改为"已落 `spec-deferred.md`"。

### Minor

- `[minor][LLM-FIXABLE][Q7]` **F-5：FR-001 AC3 与 FR-005 AC1 重复定义 disabled 语义**。FR-001 AC3 写 "项目级约定显式声明禁用 HTML 渲染时... `Evidence Matrix` 状态为 `N/A (project disabled)`"；FR-005 AC1 复述同样语义。建议 FR-001 只描述 happy path + render-failed 两个 AC，把 disabled-state 单独留给 FR-005 承担，避免一旦 disabled 语义在 design 阶段调整需要两处同步。
- `[minor][LLM-FIXABLE][A2]` **F-6：NFR-002 在标题里挂了 Portability + Compatibility 两个 ISO 25010 维度**，但 QAS 与 Acceptance 实际只验证 Portability（offline / file:// / 无外部 URL）。Compatibility / Co-existence 子维度无验证 evidence。按 `nfr-quality-attribute-scenarios.md` 的 Red Flag："一条 NFR 覆盖多个不同质量维度"，建议要么删除 Compatibility，要么拆成 NFR-002a / 002b。
- `[minor][LLM-FIXABLE][A3]` **F-7：FR-006 需求陈述含 HTML 标签字面量** "使用相对链接（`<a href="...">`）"。这是渲染层实现细节，应改为"系统必须在 HTML 中以浏览器可点击的方式（hypertext anchor）引用周期内工件路径"，把 `<a>` 留给 design。
- `[minor][LLM-FIXABLE][A3]` **F-8：§10 外部接口固化 CLI 形式** `python scripts/render-closeout-html.py <feature-dir>`。spec 阶段应描述"以 feature 目录路径为唯一输入产出 closeout.html"这一逻辑契约，具体 invocation（命令行 / 函数调用 / 子进程）由 design 决定。
- `[minor][LLM-FIXABLE][C7]` **F-9：Phase 0 缺一条显式 Desirability/Usability 假设**回扣 §3 outcome metric "non-author reader 4/5 题答对"。当前 4 条 HYP 全部是 Feasibility / Viability，但 outcome 验证的是"HTML 比 closeout.md 对非工程读者更可用"这条 desirability/usability 命题。按 `success-metrics-and-hypotheses.md`，这正是 Teresa Torres 四类假设里的 Desirability/Usability。建议补 HYP-005 ("Type=Usability，Statement=非工程读者只读 HTML 在 5 分钟内能回答 §2 的 5 个核心问题；Validation=§3 spotcheck；Confidence=中；Blocking=否")，把 outcome metric 与一条可证伪的假设挂钩。
- `[minor][LLM-FIXABLE][Q4]` **F-10：§2 引入"5 分钟"时限但 §3 Outcome Metric 未把时间作为度量维度**。如果 5 分钟是判定条件，应进入 §3 的 Threshold（"在 5 分钟阅读时间内回答 ≥ 4/5 题"）；如果不是判定条件，应从 §2 移除以避免暗藏阈值。当前两节描述不一致。

## 缺失或薄弱项

- **spec-deferred.md 未创建**（见 F-4）。按 `docs/principles/sdd-artifact-layout.md`，feature 目录平铺约定下，deferred backlog 应与 spec 同目录；当前目录 `ls` 显示无 `spec-deferred.md`。
- **版本范围未声明**。本 feature 改动 `skills/hf-finalize/SKILL.md` 与 `skills/hf-finalize/references/finalize-closeout-pack-template.md`；ADR-003 D2 仅禁止"新增 `hf-*` skill"，但 v0.3.0 处于发版冻结。spec 未声明本 feature 是否落 v0.3.0 还是 v0.4+。这不是阻塞 spec 评审的内容性问题，但建议在 README 或 progress 添加一行"Targeted Release: v0.4+"，避免后续 design / closeout 阶段误把 SKILL.md 改动夹进 v0.3.0 GA。归档为薄弱项而非 finding（属于发布管理边界，不在 spec rubric 范围）。
- **README artifacts 表已列 `ui-design.md` 行为 pending**。HTML 渲染产物算不算 "UI surface" 是 design 阶段决策（CSS 调色板、版式、a11y），spec 未明确是否触发 ui-design.md 必需。建议在 design 阶段确认；不影响 spec 评审通过。

## 下一步

- 当前结论 `需修改` → 父会话回到 `hf-specify` 由 author 定向回修上述 10 条 finding（4 important + 6 minor），所有项均 `LLM-FIXABLE`、不需用户额外业务输入。
- 单轮回修预计可达标；F-3 / F-4 是回修主线（多源优先级 + spec-deferred.md 物化）。
- 回修完成后再次派发 reviewer subagent 二次评审，达 `通过` 后由父会话进入 `规格真人确认` → `hf-design`。

## 记录位置

`features/002-html-closeout-report/reviews/spec-review-2026-05-09.md`

## 交接说明

- 不进入 `规格真人确认`（结论非 `通过`）
- 不进入 `hf-workflow-router`（无 route/stage/证据冲突）
- 父会话向用户**不**抛业务事实问卷（USER-INPUT finding 数量 = 0；版本范围在"薄弱项"中提示，不强制由用户裁决）

## 结构化返回 JSON

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-specify",
  "record_path": "features/002-html-closeout-report/reviews/spec-review-2026-05-09.md",
  "key_findings": [
    "[important][LLM-FIXABLE][A3] §6 把渲染器语言 / 单文件 / 具体脚本路径硬编码进 spec，属于 design 决策",
    "[important][LLM-FIXABLE][A3] HYP-004 Validation Plan 泄漏 string.Template / html.escape / re 等实现原语",
    "[important][LLM-FIXABLE][Q4] FR-003 多 coverage 来源同时存在或 schema 不完整时优先级未定义",
    "[important][LLM-FIXABLE][C5] §7 把真实 deferred capability 与 hard non-goal 混写在 prose，未落 spec-deferred.md",
    "[minor][LLM-FIXABLE][Q7] FR-001 AC3 与 FR-005 AC1 重复定义 project-disabled 语义",
    "[minor][LLM-FIXABLE][A2] NFR-002 同时挂 Portability + Compatibility 两个 ISO 25010 维度但只验证前者",
    "[minor][LLM-FIXABLE][A3] FR-006 需求陈述含 <a href> 标签字面量",
    "[minor][LLM-FIXABLE][A3] §10 外部接口固化 CLI invocation 形式",
    "[minor][LLM-FIXABLE][C7] Phase 0 缺一条 Desirability/Usability 假设回扣 §3 outcome metric",
    "[minor][LLM-FIXABLE][Q4] §2 5 分钟时限与 §3 Outcome Metric 未对齐"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {"id": "F-1", "severity": "important", "classification": "LLM-FIXABLE", "rule_id": "A3", "summary": "§6 渲染器语言/单文件/具体脚本路径硬编码"},
    {"id": "F-2", "severity": "important", "classification": "LLM-FIXABLE", "rule_id": "A3", "summary": "HYP-004 Validation Plan 泄漏实现原语"},
    {"id": "F-3", "severity": "important", "classification": "LLM-FIXABLE", "rule_id": "Q4", "summary": "FR-003 多 coverage 来源优先级与 schema 缺失回落未定义"},
    {"id": "F-4", "severity": "important", "classification": "LLM-FIXABLE", "rule_id": "C5", "summary": "§7 deferred capability 未物化为 spec-deferred.md"},
    {"id": "F-5", "severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "Q7", "summary": "FR-001 AC3 与 FR-005 AC1 重复"},
    {"id": "F-6", "severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "A2", "summary": "NFR-002 跨 ISO 25010 子树但只验证 Portability"},
    {"id": "F-7", "severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "A3", "summary": "FR-006 含 <a href> 标签字面量"},
    {"id": "F-8", "severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "A3", "summary": "§10 固化 CLI 形式"},
    {"id": "F-9", "severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "C7", "summary": "Phase 0 缺 Desirability/Usability 假设"},
    {"id": "F-10", "severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "Q4", "summary": "§2 5 分钟时限未在 §3 闭环"}
  ]
}
```

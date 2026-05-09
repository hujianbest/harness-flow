# Deferred Backlog — 002-html-closeout-report

本文件列出本轮（spec `features/002-html-closeout-report/spec.md`）显式延后到后续增量的能力候选。每条条目都带 Source ID / Priority / Deferral Reason / Re-entry Hint / Recommended Skill，便于 `hf-increment` / 后续 feature 启动时稳定回收。

非延后但本轮不做的能力（永久 hard non-goal）落在 `spec.md` §7，不在本文件。

## 条目

### DEF-001 跨 feature / 项目级 dashboard 或 closeout 索引页

- Source: 用户请求"直观的表达这次工作流的报告"的潜在扩展面
- Priority When Re-entered: Should
- Deferral Reason: 本轮聚焦**单 feature** closeout view；项目级 dashboard 需要跨 feature 聚合（active feature 切换 / 跨多个 closeout pack 索引 / 时间线对比），范围超出当前 feature 边界。
- Re-entry Hint: 等到 `features/` 下完成 closeout 的 feature 数 ≥ 3，且仓库已启用 `docs/index.md`（档 2）时，新增 feature 渲染 `docs/index.html` 或 `closeout-index.html`。
- Recommended Skill: `hf-increment`

### DEF-002 PDF / DOCX 导出

- Source: 范围外原 prose
- Priority When Re-entered: Could
- Deferral Reason: 主要场景是审计 / 离线归档；HTML 已可通过浏览器"打印为 PDF"满足轻度需求，原生导出在大多数项目里 ROI 不足。
- Re-entry Hint: 出现明确审计 / 合规需求（如外部 reviewer 要求纸质或固化版本）时再立项。
- Recommended Skill: `hf-increment`

### DEF-003 多语言（i18n）切换

- Source: 范围外原 prose
- Priority When Re-entered: Could
- Deferral Reason: 本轮 HTML 跟随 `closeout.md` 当前语言（中文 / 英文）原样渲染。i18n 需要术语表、双向翻译验证、章节级语言切换 UI，复杂度高于 closeout 本身价值。
- Re-entry Hint: 当 HF 主仓库或下游项目首次出现"双语审阅同一 closeout"硬需求时启动。
- Recommended Skill: `hf-increment`

### DEF-004 CI 集成模板

- Source: 范围外原 prose
- Priority When Re-entered: Should
- Deferral Reason: 自动在 PR 上预渲染 `closeout.html` 并 attach 为 PR comment / CI artifact 是有价值的 dx 改进；但 v0.3.0 起 HF 主仓库尚未引入 CI（README 明确"v0.1.0 has no CI"），先在本 feature 落地手动调用 + dogfood，CI 化等到仓库具备 baseline CI 时再做。
- Re-entry Hint: HF 引入 baseline CI（lint / smoke test / repository-wide checks）之后；或下游项目首次询问"如何把 closeout HTML 自动 attach 到 PR"时。
- Recommended Skill: `hf-increment`

### DEF-005 HTML 内嵌交互式查询 / 过滤 / 搜索

- Source: 范围外原 prose
- Priority When Re-entered: Could
- Deferral Reason: 本轮 HTML 是 readonly snapshot；交互能力（按 verdict 过滤 reviews、按日期排序 verification、文本搜索）需要 JavaScript 能力（与 NFR-002 单文件零外部依赖叠加风险），价值在大型 closeout（reviews ≥ 20 / verification ≥ 10）才显著，单 feature 不达此密度。
- Re-entry Hint: 当某 feature 的 reviews + verification 总条目 ≥ 30，导致单页可读性下降时再立项。
- Recommended Skill: `hf-increment`

### DEF-006 覆盖率数据采集对接（feature 侧 helper）

- Source: HYP-002 失效影响段
- Priority When Re-entered: Should
- Deferral Reason: 本 feature 只**读取**已存在的 coverage 数据；如何让宿主项目稳定产出 `evidence/coverage.json`（pytest-cov / jest-coverage / cargo-tarpaulin 等 toolchain 适配）属于工程框架本身的事。design 阶段会给 ≥ 2 个 toolchain 的 readme 示例，但**不做** helper 脚本 / template 化采集。
- Re-entry Hint: 当 HYP-002 在 5 次以上抽样里失效（即 ≥ 3 个 closeout 没能提供 coverage 数据），证明价值缺口大到值得做 helper 时启动。
- Recommended Skill: `hf-increment`

## 状态

本 backlog 在 spec 评审通过后随 spec 一同进入"已批准延后"状态。每条 DEF 条目在被后续 feature 重新启用时，应：

1. 在新 feature 的 spec.md 中显式 cite 对应 `DEF-NNN`
2. 在本文件追加 `Re-entry Status: in features/<NNN>-<slug>/`，不删除原 DEF 条目（保留延后 trace）

# HF Closeout HTML 工作总结报告 需求规格说明

- 状态: 草稿
- 主题: 让 `hf-finalize` 的 closeout 阶段在 `closeout.md` 之外，额外产出一份可视化 HTML 工作总结报告
- Feature: `features/002-html-closeout-report/`

## 1. 背景与问题陈述

HarnessFlow 当前的 closeout 产出物 `closeout.md` 是一份结构化 Markdown，给 reviewer / agent / git diff 用足够清晰，但对**非工程角色**（PM、QA lead、外部审计、跨团队接手者）并不直观：

- evidence matrix / state sync / docs sync 三个区块横在一起，不易一眼读出"这一轮做完了没、是否安全发布"
- 测试与覆盖率信息散落在 `verification/regression-*.md`、`verification/completion-*.md`、`evidence/` 中，需要逐文件展开
- review verdict / approval verdict 是文本，缺乏可视化的 verdict 色标
- ADR 状态翻转、runbook 新增等 long-term assets 同步项淹没在 prose 中

用户原话：

> 我希望 closeout 能有一份 HTML 工作总结报告。能直观的表达这次工作流的报告，要包含代码测试覆盖率等信息，比 markdown 格式更可读和直观。

本轮目标是：在不破坏现有 closeout 契约的前提下，提供一份**与 `closeout.md` 同源**的 HTML 衍生 view，让非工程读者也能直接读出本轮 workflow 的关键证据与验收结论。

## 2. 目标与成功标准

- **目标**：closeout 阶段产出 `features/<active>/closeout.html`，覆盖 feature 元数据、生命周期 timeline、工件索引、reviews/approvals、verification/coverage、release/docs sync、handoff。
- **成功标准（高层）**：在不引入"二次审批"的前提下，让一个**未参与本轮 workflow** 的读者，仅打开 `closeout.html` 就能在 5 分钟内回答 5 个核心问题：
  1. 本 feature 完成了什么、范围是什么？
  2. 关键评审与门禁是否都通过、由谁通过？
  3. 测试与覆盖率结论如何（如有）？
  4. 同步了哪些长期资产（ADR / arc42 / runbooks / CHANGELOG / index）？
  5. 是否还有未完成项 / handoff 给谁？

可量化度量见 §3。

## 3. Success Metrics

- **Outcome Metric**：在样本 closeout 集合上，非作者读者只读 `closeout.html`、不打开任何 `.md` 即可回答上面 5 个核心问题中的题数。
- **Threshold**：≥ 4/5 题答对，样本量 ≥ 5 次（含本 feature 自身的 dogfood closeout + 4 个由 fixture 模拟的历史 closeout 输入）。
- **Leading Indicator**：渲染脚本在 fixture 输入集合（含完整证据 / 缺工件 / 含 N/A 项 / `task-closeout` / `workflow-closeout` / `blocked` 六类样本）上的渲染成功率 = 100%。
- **Lagging Indicator**：本 feature closeout 之后，新启动的 features 在其 `hf-finalize` 阶段默认启用 HTML 渲染（即不需要逐项目重新决策）。
- **Measurement Method**：
  - Leading：脚本单元测试 + fixture 集合（落 `features/002-html-closeout-report/evidence/`）；CI/手动均可复现。
  - Lagging：本 feature 完成后，下一个新启动 feature 的 closeout 是否产出 `closeout.html`，由 traceability-review 抽查。
  - Outcome：5 次抽测的题数统计写入 `features/002-html-closeout-report/evidence/usability-spotcheck.md`。
- **Non-goal Metrics**：
  - 不追求"缩短 closeout 总耗时"。
  - 不追求"取代 `closeout.md`"——Markdown 仍是 source of truth。
  - 不追求"自动生成 release notes / CHANGELOG 文案"。
  - 不追求"跨 feature 全局 dashboard"。
- **Instrumentation Debt**：无新增数据采集；测试样本来自既有工件 + fixture，可在仓库内自包含验证。

## 4. Key Hypotheses

| ID | Statement | Type | Impact If False | Confidence | Validation Plan | Blocking? |
|---|---|---|---|---|---|---|
| HYP-001 | 单文件、内嵌 CSS、零外部依赖的 HTML 在主流浏览器和本地预览中能足够好地呈现 reviews / coverage / timeline 等结构 | Feasibility | 需引入静态站点构建器（mkdocs / 11ty 等），范围爆炸 | 高 | design 阶段给出 minimal HTML 样例，PR 内人工本地预览确认 | 否 |
| HYP-002 | 多数项目能在 closeout 时从 `verification/` 或可选的 `evidence/coverage.json` 提供至少一个覆盖率数字 | Feasibility | "覆盖率卡片"将永远显示 N/A，feature 价值打折但仍可用 | 中 | design 阶段定义最小 coverage schema 并给出 ≥ 2 个常见 toolchain（pytest-cov / jest-coverage）的对接示例；HF 自身仓库也至少接入 pytest-cov 一次作为 dogfood | 否 |
| HYP-003 | HTML 作为 closeout.md 的纯衍生 view，不引入"作者验收自己"问题 | Viability | 需把 HTML 也纳入独立 review，增加流程负担 | 高 | design 阶段约束"HTML 100% 来自已批准 `.md` / 不引入新结论 / 不修改任何长期资产"；reviewer 抽查 | 否 |
| HYP-004 | 渲染脚本可使用 Python 标准库实现，与现有 `scripts/audit-skill-anatomy.py` 的依赖纪律一致 | Feasibility | 需引入第三方依赖（Jinja2 / pyyaml 等），项目维护负担上升 | 中 | design 阶段实测：用 `string.Template` + `html.escape` + `re` 实现章节解析与渲染，跑通 fixture | 否 |

无 Blocking 假设。HYP-002 / HYP-004 confidence 为中，design 阶段必须落实验证计划并把结果写入 design 评审证据。

## 5. 用户角色与关键场景

| 角色 | 关键场景 |
|---|---|
| 维护本 feature 的 agent | 在 `hf-finalize` 步骤 6 之后调用渲染脚本，落 `closeout.html`，并在 closeout pack `Evidence Matrix` 列入该工件 |
| 项目作者 / 接手 agent | closeout 后从 PR 或仓库直接打开 `closeout.html`，确认本轮工件、verdict、coverage、handoff |
| 非工程评审者（PM / QA / 跨团队接手） | 不打开任何 `.md` 仅看 HTML 就能回答 §2 的 5 个核心问题 |
| 审计 / 复盘读者 | closeout 之后任意时刻打开 `closeout.html`，读出本轮的 evidence trail 与 long-term assets sync |

## 6. 当前轮范围与关键边界

**范围内（Must）**

- `hf-finalize` 在步骤 6（产出 closeout pack）之后增加渲染步骤，调用渲染器产出 `features/<active>/closeout.html`。
- 渲染器：单 Python 文件（路径默认 `scripts/render-closeout-html.py`），仅依赖标准库。
- 渲染输入：`features/<active>/closeout.md`（必需）、`README.md`、`progress.md`、`reviews/*`、`approvals/*`、`verification/*`、可选 `evidence/coverage.json`。
- HTML 报告章节（顺序）：
  1. Hero header（feature ID / title / closeout type / scope / conclusion / dates / profile / mode）
  2. Lifecycle Timeline（spec → design → tasks → TDD → reviews → gates → finalize 各阶段产出 + 日期 + verdict 色标）
  3. Artifacts Map（spec / design / tasks / progress / closeout 等链接 + 状态徽章）
  4. Reviews & Approvals（表格 + verdict 色标）
  5. Verification & Coverage（regression / completion 结论 + coverage 进度条；无数据时显式 `N/A`）
  6. Release / Docs Sync（ADR 状态翻转、CHANGELOG / arc42 / runbooks / SLO / index 同步路径列表）
  7. Handoff（remaining approved tasks / next action / worktree disposition / PR & branch）
  8. Open Notes / Limits
- 单文件 HTML：内嵌 CSS、零外部 CDN / 字体 / 图片依赖；可离线打开。
- 渲染失败的降级：脚本异常不阻塞 closeout 主流程；closeout pack `Evidence Matrix` 显式记录 `closeout.html` 状态为 `present` / `render-failed` / `N/A (project disabled)` 之一。
- 文档同步：
  - `skills/hf-finalize/SKILL.md` 增补步骤与 Output Contract；
  - `skills/hf-finalize/references/finalize-closeout-pack-template.md` 在 `Evidence Matrix` 增加 `closeout.html` 行；
  - `docs/principles/sdd-artifact-layout.md` 中 feature 目录布局示例增补 `closeout.html`；
  - `CHANGELOG.md` 在 `[Unreleased]` 写入条目（不假设版本号）。
- 测试：渲染器单元测试（`scripts/test_render_closeout_html.py`）覆盖：完整证据 / 缺工件降级 / `task-closeout` / `workflow-closeout` / `blocked` / 缺 coverage 五至六类 fixture。
- Dogfood：本 feature 自身在 `hf-finalize` 时跑通脚本，把渲染结果作为本 feature 的 closeout 证据。

**关键边界**

- HTML 是 closeout.md 的**纯衍生 view**：不读用户输入、不读未批准草稿、不引入新的 verdict、不修改任何长期资产。
- HF 项目本身不采集覆盖率；覆盖率数字必须**已存在于** `verification/*` 或可选 `evidence/coverage.json` 中。
- 渲染只针对**单 feature 的 closeout**，不做跨 feature 聚合。

## 7. 范围外内容

- 跨 feature / 项目级 dashboard 或 index HTML（即不渲染 `docs/index.html`）。
- PDF / DOCX 导出。
- 静态站点托管 / GitHub Pages 配置。
- 覆盖率**数据采集**本身（pytest-cov / jest-coverage 配置由项目侧负责；HF 只读 schema）。
- 自动生成 release notes / CHANGELOG 正文。
- HTML 内嵌交互式查询、过滤、搜索（report 是只读快照）。
- i18n（英文/中文双语）—— 本轮跟随 closeout.md 当前语言，不做语言切换。
- CI 集成（GitHub Actions / GitLab CI 模板）。
- 引入 Jinja2 / pyyaml / markdown-it 等第三方依赖。

后续增量候选见 `spec-deferred.md`（如有，本轮可暂不创建；deferred 内容已在本节列出）。

## 8. 功能需求

### FR-001 closeout 阶段渲染 HTML 报告

- 优先级: Must
- 来源: 用户请求"closeout 能有一份 HTML 工作总结报告"
- 需求陈述（EARS 事件触发）: 当 `hf-finalize` 写入 `features/<active>/closeout.md` 之后，系统必须立即调用 HTML 渲染器并尝试写入 `features/<active>/closeout.html`。
- 验收标准:
  - Given `hf-finalize` 已成功写入 `closeout.md`，When 渲染器执行成功，Then `features/<active>/closeout.html` 必须存在，且 closeout pack 的 `Evidence Matrix` 中包含 `closeout.html` 行，状态为 `present`。
  - Given 渲染器执行抛异常（如必需输入解析失败），When closeout 流程继续，Then `closeout.md` 仍按原流程落盘，closeout pack `Evidence Matrix` 中 `closeout.html` 行状态为 `render-failed`，并附 1–3 行错误摘要。
  - Given 项目级约定显式声明禁用 HTML 渲染，When closeout 执行，Then 系统不调用渲染器，`Evidence Matrix` 中 `closeout.html` 行状态为 `N/A (project disabled)`。

### FR-002 HTML 报告必含章节

- 优先级: Must
- 来源: 用户请求"直观的表达这次工作流的报告"
- 需求陈述: 系统必须在生成的 HTML 中按以下顺序输出 8 个章节：Hero Header、Lifecycle Timeline、Artifacts Map、Reviews & Approvals、Verification & Coverage、Release / Docs Sync、Handoff、Open Notes / Limits。
- 验收标准:
  - Given 一个完整 closeout（含 spec / design / tasks / TDD / reviews / gates / verification 全套工件），When 渲染完成，Then HTML 必须包含全部 8 个章节，每个章节有可读标题，且对应内容来源于 `closeout.md` 与周期内已存在工件。
  - Given 一个 lightweight closeout（缺设计 / 缺部分 reviews），When 渲染完成，Then 缺失章节内容必须显式渲染为 `N/A (按 profile 跳过)` 或 `N/A (本 feature 未触发)`，而不是空白或抛错。

### FR-003 测试覆盖率卡片化展示

- 优先级: Must
- 来源: 用户请求"要包含代码测试覆盖率等信息"
- 需求陈述（EARS 状态约束）: 在 `Verification & Coverage` 章节下，当存在 coverage 数据来源时，系统必须把覆盖率数值以可视化卡片（含数字 + 进度条 / 圆环）的形式展示，并标注来源路径。
- 验收标准:
  - Given `features/<active>/evidence/coverage.json` 存在且符合最小 schema（至少含 `lines.pct` 字段），When 渲染完成，Then HTML 必须显示 line coverage 的数值与进度条，并在卡片下方注明来源 `evidence/coverage.json`。
  - Given `coverage.json` 不存在但 `verification/regression-*.md` 中含 `Coverage:` 行（形如 `Coverage: 84.3%`），When 渲染完成，Then HTML 必须显示该数值并注明来源 `verification/regression-*.md`。
  - Given 既无 `coverage.json` 也无 `verification/*.md` 中可识别的 Coverage 行，When 渲染完成，Then HTML 必须在覆盖率卡片处显式显示 `N/A（项目未提供覆盖率数据）`，并提供 1 行接入指引链接（指向 design 阶段产出的 coverage schema 文档）。
  - Given coverage 值不在 [0, 100] 范围或无法解析，When 渲染完成，Then HTML 必须显示 `Invalid` 而不是抛错，并把原始字符串放入 tooltip / data 属性。

### FR-004 verdict 色标与状态徽章

- 优先级: Must
- 来源: 用户请求"比 markdown 格式更可读和直观"
- 需求陈述: 系统必须为以下三类信息渲染色标：review/approval verdict（通过 / 需修改 / 阻塞 / N/A）、verification verdict（pass / fail / N/A）、closeout type（task-closeout / workflow-closeout / blocked）。
- 验收标准:
  - Given 一份含混合 verdict 的 closeout（如 1 个通过 + 1 个需修改但已闭环），When 渲染完成，Then HTML 必须为每个 verdict 渲染独立色标块，且色标在色盲友好（至少 protanopia / deuteranopia）调色板内。
  - Given closeout type 为 `blocked`，When 渲染完成，Then Hero Header 必须显示醒目的 `BLOCKED` 标签，且 `Handoff` 章节强调 next action 必须是 `hf-workflow-router`。

### FR-005 项目级配置开关

- 优先级: Should
- 来源: HYP-003 风险控制 / 兼容老项目
- 需求陈述（EARS 可选策略）: 在启用项目级约定 `closeout html: enabled|disabled` 时，系统必须按该约定决定是否生成 HTML，并在 closeout pack 中显式记录该决策。
- 验收标准:
  - Given 项目级约定中存在 `closeout html: disabled`，When closeout 执行，Then 不写出 `closeout.html`，`Evidence Matrix` 行状态为 `N/A (project disabled)`。
  - Given 项目级约定中无该字段，When closeout 执行，Then 默认按 `enabled` 处理。

### FR-006 链接到周期内工件

- 优先级: Must
- 来源: 用户请求"直观"——不应让读者再去翻文件树
- 需求陈述: HTML 中所有引用周期内工件路径（spec / design / reviews / approvals / verification / evidence）的位置，必须使用相对链接（`<a href="...">`）使浏览器在文件协议下可点击跳转。
- 验收标准:
  - Given closeout.html 与 closeout.md 同目录，When 在浏览器以 `file://` 协议打开，Then 所有工件链接必须能跳转到对应文件而不报 404。
  - Given 工件链接的目标文件不存在（如 `verification/regression-2026-05-09.md` 实际未生成），Then 该链接必须以 `class="missing"` 标记并显示为 strikethrough，避免误导读者认为已生成。

## 9. 非功能需求 (ISO 25010 + Quality Attribute Scenarios)

### NFR-001 渲染稳定性（Reliability / Fault tolerance）

- 优先级: Must
- 来源: HYP-002 / HYP-004 风险控制
- QAS:
  - Stimulus Source: `hf-finalize` 调用渲染器
  - Stimulus: closeout 输入工件部分缺失（reviews 缺 1 份、verification 仅 1 份、coverage.json 不存在）
  - Environment: closeout 主流程已完成 Markdown 落盘，HTML 渲染为衍生步骤
  - Response: 渲染器以降级模式继续，缺失项渲染为 `N/A` 字符串而非抛错；任何 unhandled exception 在渲染器边界被捕获并以 `render-failed` 状态返回，不影响 `closeout.md`。
  - Response Measure: 在 fixture 集合（≥ 6 个样本）上，渲染器对**任一**缺工件场景的 unhandled exception 必须为 0；对完整 fixture 必须返回 exit code 0 且产出可解析 HTML（`<html lang=...>` / `<title>` / 8 个 `<section>` 全部存在）。
- Acceptance:
  - Given fixture 集合的 6 个 closeout 样本，When 在每个样本上独立运行渲染器，Then 0 个 unhandled exception；Markdown 渲染失败的样本产生 `render-failed` 状态并写入 stderr，但 exit code ≤ 1。

### NFR-002 单文件可移植性（Portability / Installability + Compatibility / Co-existence）

- 优先级: Must
- 来源: HYP-001
- QAS:
  - Stimulus Source: 任意读者
  - Stimulus: 在离线环境双击或 `file://` 协议打开 `closeout.html`
  - Environment: 无网络、无任何项目工具链、仅有现代浏览器（Chromium ≥ 110 / Firefox ≥ 110）
  - Response: 报告完整渲染，包括样式、色标、布局
  - Response Measure: HTML 文件不引用任何外部 URL（`http://` / `https://` / `//`）作为样式 / 字体 / 脚本来源；唯一允许的外部链接是 `<a href>` 指向 GitHub PR / commit / 工件相对路径。
- Acceptance:
  - Given 任一渲染产物 `closeout.html`，When 在离线浏览器打开，Then 页面布局、色标、卡片完整呈现；
  - Given 同一文件在 `grep -E 'src="https?://|href="https?://[^"]*\.(css|js|woff|svg|png|jpg)"' closeout.html` 下，Then 命中数 = 0。

### NFR-003 渲染性能（Performance Efficiency / Time behavior）

- 优先级: Should
- 来源: 维护负担约束（closeout 不应明显变慢）
- QAS:
  - Stimulus Source: `hf-finalize` 调用渲染器
  - Stimulus: 单 feature closeout 渲染请求
  - Environment: 标准笔记本（Apple M1 / Intel i5-1135G7 等量级），冷启动 Python 解释器
  - Response: 渲染完成
  - Response Measure: 渲染（含进程启动）耗时 P95 ≤ 2s，P99 ≤ 4s；HTML 文件大小 ≤ 200 KB（典型 closeout，无嵌入 raw log）。
- Acceptance:
  - Given fixture 集合，When 顺序跑 5 次取均值，Then 单次 wall-clock ≤ 2s；
  - Given 任一渲染产物，Then `wc -c closeout.html` ≤ 200 × 1024。

### NFR-004 注入安全（Security / Integrity）

- 优先级: Must
- 来源: closeout 输入来自人 / agent 写的 Markdown，存在 `<` `>` `&` `"` 等字符
- QAS:
  - Stimulus Source: `closeout.md` / reviews / verification 中的字符串字段
  - Stimulus: 字段含 `<script>...</script>`、`onerror=` 等潜在 HTML/JS 注入序列
  - Environment: 渲染器输出 HTML
  - Response: 所有用户/工件来源字符串以文本形式渲染，绝不作为 HTML/JS 解释
  - Response Measure: 在 fixture 中放入恶意字符串样本（覆盖 `<script>` / `<img onerror>` / SVG `<svg onload>`），渲染产物在浏览器打开时不触发任何脚本执行；用 `grep -F '<script>'` 在 HTML 输出中应仅命中转义后的 `&lt;script&gt;` 序列。
- Acceptance:
  - Given 一个含 4 类典型 XSS payload 的 fixture closeout，When 渲染并以浏览器打开，Then 无 alert 弹出、无 console error、无 network request；
  - Given 同一 HTML，Then `grep -c '<script>' closeout.html` 与 `<script>...</script>` 仅出现 0 次（除渲染器自身可能内嵌的 minimal 折叠脚本，且该脚本不接受任何用户输入）。

### NFR-005 可读性与可访问性（Usability / Operability + Accessibility）

- 优先级: Should
- 来源: 用户请求"更可读和直观"
- QAS:
  - Stimulus Source: 非工程读者
  - Stimulus: 在 1280×800 分辨率下打开 `closeout.html`
  - Environment: 主流桌面浏览器，默认字号
  - Response: 页面无需横向滚动、关键信息在首屏内、色标对色盲友好
  - Response Measure: 横向 overflow = 0；首屏（视口 1280×800）必须包含 Hero Header + Lifecycle Timeline 至少 1 段；色标至少满足 WCAG AA 对比度（≥ 4.5:1）；提供 `prefers-reduced-motion` / `prefers-color-scheme` 兼容（不强制深色，但不破坏）。
- Acceptance:
  - Given 渲染产物，When 在 1280×800 视口打开，Then 主体 `<body>` 的 `scrollWidth ≤ clientWidth`；
  - Given 任一 verdict 色标（pass / 需修改 / blocked），Then 与背景对比度 ≥ 4.5:1（design 阶段固化调色板时一并验证）。

### NFR-006 可维护性（Maintainability / Modularity + Testability）

- 优先级: Must
- 来源: HYP-004 / 项目纪律（最小依赖）
- QAS:
  - Stimulus Source: 后续 feature 维护者
  - Stimulus: 修改渲染器以支持新工件类型或新 verdict
  - Environment: 标准 Python 3.9+ 解释器，仅标准库
  - Response: 修改可被单元测试覆盖；模板与数据组装边界清晰
  - Response Measure: 渲染器源文件 ≤ 800 行；至少存在数据组装 / HTML 渲染两个可独立测试的纯函数；单测覆盖 ≥ 6 个 fixture 场景；不引入任何 `requirements.txt` / `pyproject.toml` 第三方依赖。
- Acceptance:
  - Given `scripts/render-closeout-html.py`，Then 顶层无 `import` 第三方包；
  - Given `scripts/test_render_closeout_html.py`，Then 至少 6 个 test 函数对应 6 类 fixture，全部通过。

## 10. 外部接口与依赖

- **输入接口**：feature 目录路径（`features/<NNN>-<slug>/`）。脚本 CLI 形式：`python scripts/render-closeout-html.py <feature-dir>`，输出落到 `<feature-dir>/closeout.html`。
- **可选输入：coverage 最小 schema**（design 阶段固化）：
  ```json
  {
    "lines": { "pct": <number 0..100> },
    "branches": { "pct": <number 0..100> },
    "tool": "<string>",
    "generated_at": "<ISO8601>"
  }
  ```
  仅 `lines.pct` 是 design 阶段需保证可读取的最小字段；其余允许缺失。
- **依赖**：Python ≥ 3.9（标准库），与现有 `scripts/audit-skill-anatomy.py` 一致。
- **失效影响**：Python 解释器缺失时，HF 主流程不受影响（HTML 渲染降级为 `render-failed` 并写入诊断信息）。

## 11. 约束与兼容性要求

- **CON-001**：不引入第三方 Python 依赖（标准库优先），与 `scripts/audit-skill-anatomy.py` 风格一致。来源：项目纪律 / HYP-004。
- **CON-002**：不破坏现有 `closeout.md` 契约——`hf-finalize` 的所有既有 hard gate / verification / output contract 保持不变。HTML 是**追加**输出，不是替换。来源：`skills/hf-finalize/SKILL.md` 现行契约。
- **CON-003**：HTML 文件必须放在 `features/<active>/closeout.html`，与 `closeout.md` 同目录，遵循 `docs/principles/sdd-artifact-layout.md` 的双根目录布局。来源：sdd-artifact-layout.md。
- **CON-004**：feature 目录平铺保留在 `features/` 下，不移动到 `archived/`；HTML 路径不会因 closeout 后归档而失效。来源：sdd-artifact-layout.md Red Flags。
- **CON-005**：渲染必须在 `hf-finalize` 步骤 6（写 `closeout.md`）之后、步骤 7（Verification 自检）之前完成；这样 closeout pack 的 `Evidence Matrix` 才能记录 `closeout.html` 状态。
- **CON-006**：HTML 不得修改任何长期资产（`docs/`、`CHANGELOG.md`、`README.md`），仅产出自身一个文件。
- **CON-007**：HTML 单文件不超过 200 KB（NFR-003 已量化），避免 PR diff 体感过重。

## 12. 假设与失效影响

承接 §4 Key Hypotheses 中非 Blocking 假设：

- HYP-001 失效 → 退回静态站点构建器：feature 范围会扩大，需新建 follow-up feature。
- HYP-002 失效 → 覆盖率卡片永远 N/A，feature 仍交付，但价值打折；后续 increment 需考虑接入 coverage 采集（不在本轮范围）。
- HYP-004 失效 → 引入第三方依赖（Jinja2 等）；需走 ADR 决定，不在本轮自动允许。

## 13. 开放问题

**非阻塞**

- OQ-001：是否需要在 HTML 中嵌入本 feature 的 mermaid 流程图（lifecycle timeline 的另一种表达）？倾向"否"，避免引入 mermaid runtime；但 design 阶段可再权衡。
- OQ-002：HTML 标题是否使用 feature title 还是 `<feature-id> closeout`？倾向 `<feature-id> · <title> · <closeout-type>`；design 阶段最终确定。
- OQ-003：当 `task-closeout` 与 `workflow-closeout` 共存（task closeout 之后跟 workflow closeout 在同一 feature）时，HTML 是覆盖还是追加历史区？倾向"覆盖"——`closeout.html` 始终反映**最新一次** closeout pack；历史从 git 取。

**阻塞**

- 无。所有阻塞性边界（是否替换 closeout.md / 是否采集 coverage / 是否引入第三方依赖）都已在范围内/范围外锁定。

## 14. 术语与定义

- **closeout pack**：`hf-finalize` 在 `features/<active>/closeout.md` 产出的结构化 Markdown，是 closeout source of truth。
- **HTML 报告 / closeout.html**：本 feature 引入的 closeout pack 衍生 view，单文件、自包含、可离线打开。
- **render-failed**：渲染器异常退出，但 closeout 主流程已成功（Markdown 已落盘）的状态。
- **N/A (project disabled)**：项目级约定显式声明 `closeout html: disabled` 时的状态。
- **N/A (按 profile 跳过)**：因 Workflow Profile 跳过的章节，沿用现有 `hf-finalize` 用语。

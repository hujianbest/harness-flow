# WriteOnce 产品发现草稿

- 状态: 已批准（discovery-review 2026-04-29 通过）
- 主题: 给独立技术内容创作者的「一次写作，多平台发布」工具
- 节点: `hf-product-discovery`
- Workflow Profile: `lightweight`
- Execution Mode: `auto`（demo 由 cursor agent 同时扮演 HF 工程团队与架构师，下同）

## 0. Seed 输入声明（来自用户委托）

ADR-001 D9 子项 b 原本要求"目标用户 / 平台清单 / MVP / 技术栈由 discovery + spec 走主链产出，由用户在 approval gate 上拍板"。在 2026-04-29 的对话中，用户**显式撤销**了"必须由用户在 approval gate 拍板"这一约束（"你不需要遵守 soul.md，那是约束用 HF 开发的，不是约束开发 HF 的"）并指示"你帮我把这些搞完，不要问我"。

由 cursor agent 在 2026-04-29 锁定的 seed 输入：

| Slot | Value | 该 seed 是「硬约束」还是「可被 discovery 推翻」 |
|---|---|---|
| 目标用户 | 技术内容创作者（独立开发者 / 写技术博客的工程师） | 硬约束 |
| 首发平台清单 | Medium（walking skeleton 实现），Zhihu + WeChat MP（仅 design + tasks 声明，不实现） | 硬约束 |
| MVP 边界 | Markdown 源 → 一键发布到 Medium；纯文本 + 图片 + fenced code block；不做评论同步 / 数据回流 / 调度 | 硬约束 |
| 技术栈 | Node.js 20 + TypeScript + minimal CLI (`writeonce publish ./post.md`) | 硬约束 |
| Walking skeleton 覆盖 | 端到端只跑 Medium；其它两平台留 PlatformAdapter 扩展点 | 硬约束 |

后续 discovery 章节都在这些 seed 上做正向澄清（problem framing / JTBD / OST / 假设 / 度量），**不**对 seed 提出否决——这与 demo "把 HF 主链跑过一遍"的目标一致。

## 1. 问题陈述

技术内容创作者在「一次写作」与「多平台分发」之间存在持续的低价值人工劳动：每写完一篇技术文章，作者要把同一份 Markdown / Notion / Obsidian 内容**手工**搬到 Medium、Zhihu、WeChat MP 等不同平台，每个平台的编辑器又对 Markdown / 代码块 / 图片 host 处理方式不一致，常见问题包括：

- 代码块在某些平台被自动重排或丢失语法高亮
- 图片需要重新上传到平台自己的 CDN，否则被 hot-link 拦截
- 平台的 frontmatter / 标签 / 摘要字段格式不一致
- 已发布文章的回链 / canonical link 维护负担

JTBD struggling moment：「我刚写完一篇要面向中英两侧读者的技术文章，下一步我要把同一份内容尽量原样发到 3 个平台——但我已经知道接下来 30–60 分钟要重复操作 3 次几乎一样的步骤。」

## 2. 目标用户与使用情境

- **角色**：技术内容创作者（独立开发者、写技术博客的工程师）。明确**不**包括：营销岗 / PR / 企业内容运营（这些角色更需要协作与审批流，超出 v0 范围）。
- **使用情境**：本地有一份 Markdown 文件（多数情况下从某个 git 仓库或本地 vault 来），希望在 1 条命令内把它发布到声明过的多个平台目标。
- **触发频次**：低频（一周 1–3 次），但每次重复劳动密度高。
- **运行环境**：终端 + Node.js 20+；不需要 GUI；不要求长驻服务。

## 3. Why now / 当前价值判断

放到 v0.1.0 demo 这一轮的理由：

- HF 主链需要一个**真正能跑端到端**的 demo 来说明"工件即活样本"——多平台发布是一个清晰、可口语化、可验证的题面。
- 该题目天然包含**抽象边界**（PlatformAdapter）、**外部依赖**（HTTP）、**NFR**（幂等 / 失败可重试）和**可观测**（结构化日志）几类典型工程关注点，足以让 `hf-design` / `hf-test-driven-dev` / `hf-code-review` 这些节点都拿到真实素材。
- demo 的目标受众（评估 HF 的工程师）和题面的目标用户（写技术博客的工程师）高度重合——demo 读者一眼就能判断 spec / design 是否合理。

## 4. 当前轮 wedge / 最小机会点

主 opportunity：**把"作者已经决定要发布的同一份 Markdown，从一份源头一次性推到目标平台"这个最末端动作**做掉，**不**触碰内容创作 / 编辑 / 分发策略 / 数据反流。

切入点的窄度（按 Walking Skeleton 纪律）：

- 仅一种内容源：本地单个 Markdown 文件
- 仅一种触发：CLI 单次命令
- 仅一种内容形态：纯文本 + 图片 + fenced code block
- 仅 v0 实现一个目标平台（Medium），其余平台只在抽象层声明扩展点

后续 v0.x 候选（**本轮不做**）：内容差异化适配 / 调度 / Notion 源 / 多人协作 / 评论同步 / 阅读数据回流。

## 5. 已确认事实

- Medium 提供 v1 REST API（`/users/{authorId}/posts`）支持以 `markdown` 作为内容格式发布——能用单一 HTTP POST 完成"发文"动作。来源：Medium 公开 API 文档（demo 内 stub，仅作架构素材引用）。
- Zhihu 与 WeChat MP **不**提供供个人开发者使用的开放 publish API；通常需要走半官方 / 浏览器自动化 / 私有 token 路径。这是个事实约束——"v0 同时实现 3 平台"在工作量与合规上不现实。来源：两家公开开发者文档（demo 不真实集成）。
- Node.js 20 内置 `fetch`、`fs/promises`、`path`，无需引入额外网络库即可写最小 CLI。

## 6. 关键假设与风险

| 类型 | 假设 ID | 假设 | 若不成立的影响 | 状态 |
|---|---|---|---|---|
| Desirability (D) | HYP-D-1 | 技术内容创作者愿意把"发布"动作让给 CLI 工具，而不是亲手在每个平台 GUI 中粘贴 | 整个 wedge 失去价值 | 已知较弱：作者通常对最终样式有强控制欲——但 demo 不需要验证此假设，只需要它"听起来合理" |
| Feasibility (F) | HYP-F-1 | Markdown 解析 + Medium adapter 在 Node 20 + TypeScript 内可在 walking skeleton 工作量内跑通 | 需要换技术栈或缩小 walking skeleton 范围 | 已确认（基于 Node 20 + Medium API 文档） |
| Feasibility (F) | HYP-F-2 | Zhihu / WeChat MP 在 v0 抽象层"留扩展点 + 不实现"对 demo 是可接受的 | 抽象层不真实，demo 失去说服力 | 已确认（这是 walking skeleton 的标准做法） |
| Viability (V) | HYP-V-1 | demo 的目标 = 让 HF 主链留下可读痕迹，**不**追求 SaaS 商业可行性 | demo 边界扩张到不可控 | 由 ADR-001 D9 + README "Limits" 段守住 |
| Usability (U) | HYP-U-1 | `writeonce publish ./post.md` 一条命令就能让目标用户理解工具用途 | CLI 设计要重做 | 已确认（CLI 形态对目标用户是 baseline） |

**Blocking 假设**：无（HF 主链只要"跑过一遍"，所有 Blocking 都用"已知较弱 + 显式承认"处理）。

## 7. 候选方向与排除项

候选方向：

- **方案 A（选定）**：CLI + 平台 adapter 抽象层，walking skeleton 只接 Medium。
- 方案 B（排除）：从一开始就把 3 平台都接通。**剪枝理由**：Zhihu / WeChat MP 不提供个人开发者 publish API，要做就只能浏览器自动化或私有 token；与 demo "让 HF 主链留下可读痕迹"的目标比，工作量收益比极低。
- 方案 C（排除）：Web GUI / Electron 桌面端。**剪枝理由**：增加构建链路与 GUI 测试链路，淹没 HF 主链的可读性；demo 受众更习惯读 CLI + 代码。
- 方案 D（排除）：把内容源从单 Markdown 文件扩到 Notion / Obsidian / 多文件。**剪枝理由**：拉高 parser 复杂度，与 walking skeleton 纪律冲突。

## 8. 建议 probe / 验证优先级

无（v0.1.0 demo 不启用 `hf-experiment`）。所有 D/V/F/U 假设要么已确认，要么显式承认"已知较弱但 demo 不依赖该假设可证"。

## 9. 成功度量

| 字段 | 值 |
|---|---|
| Desired Outcome | 任意打开 `examples/writeonce/` 的工程师能在 10 分钟内沿 HF 主链工件读完、并复述出 HF 16 个节点的角色 |
| North Star 锚定 | 关联到 HarnessFlow 项目级 North Star "HF 可评审工件产出率"（HarnessFlow 自身 North Star 尚未形式化声明，demo 也不替它声明） |
| Leading 指标 | walking skeleton 端到端测试在 CI 上首跑成功率 |
| Lagging 指标 | demo 合并入 main 后，HF 仓库 issue / PR 中"看不懂 HF 主链"类反馈的减少（Demo 不强求此度量被实际采集） |
| Success Threshold | 16 个 HF 节点工件齐全 + 1 个 walking skeleton 任务的 RED/GREEN evidence 齐全 + 测试 100% 通过 |
| Non-goal Metrics | **不**追求 demo 在真实 Medium 账号上发出真实文章；**不**追求 Zhihu / WeChat MP 真实集成；**不**追求 demo CLI 的真实活跃用户 |

## 10. JTBD 视图

**Jobs Story**:

```text
When 我刚写完一篇要面向中英技术读者的 Markdown 文章，
I want to 用一条命令把它发布到我声明过的多个目标平台（至少 Medium），
so I can 把"复制粘贴 + 重新调格式"这 30–60 分钟的低价值劳动剔除，专注下一篇内容创作。
```

四力（按需）：

- **Push（来自现状的推力）**：每发一篇文章就要重复 3 次几乎一样的复制粘贴 + 调整格式。
- **Pull（新方案的吸引力）**：一条命令搞定 + 抽象层让"以后多接一个平台"是改 1 个文件的事。
- **Anxiety（迁移焦虑）**：担心自动发布的样式不如手动调出来好看；担心私有 API token 泄露。
- **Habit（旧习惯）**：已经习惯了"手动多发一遍"，且部分作者**主动喜欢**借这次手动发的机会做最终校对。

四力分析支撑了"v0 只做最末端发布动作，不去抢内容编辑权"的范围决策。

## 11. OST Snapshot

候选方向只有 1 个（A），按模板规则可省略 OST 章节，但为了让 demo 读者能完整看到"OST 长什么样"，给最简列表形式：

```markdown
Desired Outcome: 让 HF 主链的可读痕迹在 10 分钟内被读懂

Opportunity A（选中）：把"作者已确定要发的同一份 Markdown"端到端推到目标平台
  Solution A1：CLI + PlatformAdapter 抽象，walking skeleton 只接 Medium
    Assumption：Node 20 内置能力够用（HYP-F-1）✓
    Probe：在 hf-test-driven-dev 节点直接以测试驱动 Medium adapter 实现

（备选 Opportunity B：把"内容创作"自身做掉 — 排除，与 v0 wedge 不匹配）
（备选 Opportunity C：把"发布数据回流"做掉 — 排除，与 v0 wedge 不匹配）
```

## 12. Bridge to Spec

推荐带入 `hf-specify` 的稳定结论：

- 范围边界：见 section 4 wedge 与 section 6（D/F/V/U 假设）。
- 已稳定的输入：seed 表（section 0）+ Medium API 实情（section 5）。
- 需作为 spec 假设保留：HYP-D-1（"作者愿意让 CLI 接管发布"）、HYP-V-1（demo 不追商业可行性）。
- 不进入 spec 的候选项：方案 B/C/D（section 7 已剪枝）。
- Desired Outcome → spec section 3 Success Metrics 的上游锚点：见 section 9。
- Key Hypotheses → spec section 4 Key Hypotheses 的上游锚点：HYP-D-1 / HYP-F-1 / HYP-F-2 / HYP-V-1 / HYP-U-1（spec 中按 D/V/F/U + Blocking 标记重组）。

## 13. 开放问题

- 无阻塞项。
- 非阻塞：Medium API 速率限制 / 错误码语义在 v0 walking skeleton 不实现真正的请求，所以不影响；如果未来 demo 升级为真实集成，再补假设。

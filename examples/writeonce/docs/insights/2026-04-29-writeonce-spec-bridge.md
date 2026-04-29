# WriteOnce Spec Bridge

- 状态: 已批准（discovery-review 通过）
- 主题: 把 WriteOnce 的 discovery 结论桥接给 `hf-specify`
- Source: `docs/insights/2026-04-29-writeonce-discovery.md`

这份文档专门服务于 `hf-specify` 的"上游输入"环节。它从 discovery 草稿中把对 spec 真正稳定的结论提取出来，避免 spec 直接读 13 节 discovery 全文。

## 1. 稳定 Thesis

> 给已经决定要把同一份 Markdown 发布到多个平台的技术内容创作者，提供一个**最末端**的"一条命令多平台发布"工具。Walking skeleton 只接通 Medium 一个平台，其余平台只在抽象层上声明扩展点。

## 2. 稳定范围边界

- **In**：本地 Markdown 文件 → CLI → Medium 端到端发布。
- **In**：PlatformAdapter 抽象层（设计 + 实现 + 单元测试覆盖）。
- **In**：Zhihu / WeChat MP 的 PlatformAdapter **接口** 在 design + tasks 中声明，但**不**在 walking skeleton 中实现。
- **Out**：内容创作 / 编辑 / Notion 源 / 多文件 / 调度 / 评论同步 / 数据回流 / GUI / CI 部署。

## 3. 必须承接到 spec 的成功度量

来自 discovery section 9：

| 字段 | 值 |
|---|---|
| Outcome Metric | 工程师 ≤ 10 分钟读完 16 节点工件 + 复述 HF 主链节点角色 |
| Threshold | 16 节点工件齐全；walking skeleton RED/GREEN evidence 齐全；测试 100% 通过 |
| Leading | 端到端测试 CI 首跑通过率 |
| Lagging | "看不懂 HF 主链"反馈减少（demo 不强求采集） |
| Non-goal | 不追求真实 Medium 集成；不追求 Zhihu / WeChat MP 集成；不追求 CLI 用户活跃度 |
| Measurement Method | 由 demo 评估者自报（无埋点） |
| Instrumentation Debt | 不做埋点；spec 写明此项不投入 |

## 4. 必须承接到 spec 的关键假设

| ID | Statement | Type | Impact If False | Confidence | Validation Plan | Blocking? |
|---|---|---|---|---|---|---|
| HYP-D-1 | 技术内容创作者愿意把"发布"动作让给 CLI 工具 | D | demo wedge 失去价值，但**不**影响 demo 完成"留下 HF 主链可读痕迹"目标 | 弱 | 不验证（接受为假设保留） | No |
| HYP-F-1 | Markdown 解析 + Medium adapter 在 Node 20 + TS 内可在 walking skeleton 工作量内跑通 | F | 重选技术栈或缩小 walking skeleton 范围 | 高 | 由 `hf-test-driven-dev` 节点 RED/GREEN 自然验证 | No |
| HYP-F-2 | Zhihu / WeChat MP 留扩展点 + 不实现是可接受的 | F | 抽象层不真实，demo 失去说服力 | 高 | 由 `hf-design-review` 在审 PlatformAdapter 时确认 | No |
| HYP-V-1 | demo 不追求 SaaS 商业可行性 | V | demo 边界扩张到不可控 | 高 | 由 ADR-001 D9 + README "Limits" 段守住 | No |
| HYP-U-1 | `writeonce publish ./post.md` 一条命令对目标用户足够直观 | U | CLI 设计要重做 | 高 | 由 `hf-code-review` 在审 CLI 入口时确认 | No |

## 5. 待保留为 spec 假设的不稳定结论

无（所有不稳定结论都已经在 discovery 中以"已知较弱 + 显式承认"处理；spec 不需要再额外引入新假设）。

## 6. 不进入 spec 的候选项

见 discovery section 7：
- 方案 B（一次性 3 平台都接通）— 剪枝
- 方案 C（Web GUI / Electron）— 剪枝
- 方案 D（Notion / Obsidian / 多文件源）— 剪枝

这些项要在 spec 的"范围外内容"章节显式列出，并指向本 bridge 文档作为剪枝来源。

# 议题跟踪器：GitHub

此仓库的议题和规格以 GitHub 议题形式存放。所有操作都使用 `gh` CLI。

## 约定

- **创建议题**：`gh issue create --title "..." --body "..."`。多行正文使用 heredoc。
- **读取议题**：`gh issue view <number> --comments`，使用 `jq` 过滤评论并同时获取标签。
- **列出议题**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，配合适当的 `--label` 和 `--state` 过滤器。
- **评论议题**：`gh issue comment <number> --body "..."`
- **应用 / 移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：`gh issue close <number> --comment "..."`

根据 `git remote -v` 推断仓库——在克隆仓库中运行时，`gh` 会自动完成此操作。

## 将拉取请求作为分诊入口

**PRs as a request surface: no.** _（如果此仓库将外部 PR 视为特性请求，请设置为 `yes`；`/triage` 会读取此标志。）_

设置为 `yes` 时，PR 会使用与议题相同的标签和状态，并使用对应的 `gh pr` 命令：

- **读取 PR**：`gh pr view <number> --comments`，并使用 `gh pr diff <number>` 查看差异。
- **列出供分诊的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，然后仅保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的 PR（丢弃 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **评论 / 标签 / 关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 的议题和 PR 共用同一个编号空间，因此单独的 `#42` 可能是其中任一种——先用 `gh pr view 42` 解析，失败后改用 `gh issue view 42`。

## 当技能要求“发布到议题跟踪器”时

创建一个 GitHub 议题。

## 当技能要求“获取相关票”时

运行 `gh issue view <number> --comments`。

## 寻路操作

供 `/wayfinder` 使用。**地图**是单个议题，票则作为其**子**议题。

- **地图**：带有 `wayfinder:map` 标签的单个议题，正文包含笔记 / 目前决策 / 迷雾。`gh issue create --label wayfinder:map`。
- **子票**：作为 GitHub 子议题链接到地图的议题（对“子议题”端点使用 `gh api`）。未启用子议题时，将子票添加到地图正文的任务列表，并在子票正文顶部写入 `Part of #<map>`。标签：`wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。认领后，将票分配给主导开发者。
- **阻塞**：GitHub 的**原生议题依赖关系**——规范且在 UI 中可见的表示形式。使用 `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` 添加边，其中 `<blocker-db-id>` 是阻塞项的数字型**数据库 ID**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，_不是_ `#number` 或 `node_id`）。GitHub 会报告 `issue_dependencies_summary.blocked_by`（仅开放的阻塞项——实时门禁）。无法使用依赖关系时，回退到子票正文顶部的 `Blocked by: #<n>, #<n>` 行。当每个阻塞项都关闭时，票解除阻塞。
- **前沿查询**：列出地图中开放的子票（`gh issue list --state open`，范围限定为地图的子议题 / 任务列表），丢弃存在开放阻塞项（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行中存在开放议题）或已有受理人的票；按地图顺序最靠前者优先。
- **认领**：`gh issue edit <n> --add-assignee @me`——会话中的首次写入。
- **解决**：`gh issue comment <n> --body "<answer>"`，然后 `gh issue close <n>`，再将上下文指针（gist + 链接）追加到地图的“目前决策”部分。

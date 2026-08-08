# 议题跟踪器：GitLab

此仓库的议题和规格以 GitLab 议题形式存放。所有操作都使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## 约定

- **创建议题**：`glab issue create --title "..." --description "..."`。多行描述使用 heredoc。传入 `--description -` 可打开编辑器。
- **读取议题**：`glab issue view <number> --comments`。使用 `-F json` 获取机器可读输出。
- **列出议题**：`glab issue list -F json`，配合适当的 `--label` 过滤器。
- **评论议题**：`glab issue note <number> --message "..."`。GitLab 将评论称为“备注”。
- **应用 / 移除标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签可用逗号分隔，也可重复使用该标志。
- **关闭**：`glab issue close <number>`。`glab issue close` 不接受关闭评论，因此先用 `glab issue note <number> --message "..."` 发布说明，再关闭。
- **合并请求**：GitLab 将 PR 称为“合并请求”。使用 `glab mr create`、`glab mr view`、`glab mr note` 等——形式与 `gh pr ...` 相同，但以 `mr` 取代 `pr`，以 `note`/`--message` 取代 `comment`/`--body`。

根据 `git remote -v` 推断仓库——在克隆仓库中运行时，`glab` 会自动完成此操作。

## 将合并请求作为分诊入口

**MRs as a request surface: no.** _（如果此仓库将外部合并请求视为特性请求，请设置为 `yes`；`/triage` 会读取此标志。）_

设置为 `yes` 时，MR 会使用与议题相同的标签和状态，并使用对应的 `glab mr` 命令：

- **读取 MR**：`glab mr view <number> --comments`，并使用 `glab mr diff <number>` 查看差异。
- **列出供分诊的外部 MR**：`glab mr list -F json`，然后仅保留作者不是项目成员/所有者的 MR（贡献者的 MR，而不是维护者正在进行的工作）。
- **评论 / 标签 / 关闭**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`。

与 GitHub 不同，GitLab 分别为议题和 MR 编号，因此一旦知道维护者指的是哪种入口，`#42` 就没有歧义。

## 当技能要求“发布到议题跟踪器”时

创建一个 GitLab 议题。

## 当技能要求“获取相关票”时

运行 `glab issue view <number> --comments`。

## 寻路操作

供 `/wayfinder` 使用。**地图**是单个议题，票则作为其**子**议题。

- **地图**：带有 `wayfinder:map` 标签的单个议题，正文包含笔记 / 目前决策 / 迷雾。`glab issue create --label wayfinder:map`。（在支持原生史诗的 GitLab 层级中，也可以用史诗承载地图；带标签的议题在所有层级都可用。）
- **子票**：描述顶部包含 `Part of #<map>` 且带有 `wayfinder:<type>` 标签（`research`/`prototype`/`grilling`/`task`）的议题。认领后，将票分配给主导开发者。
- **阻塞**：GitLab 的**原生阻塞链接**——规范且在 UI 中可见的表示形式。通过 `/blocked_by #<n>` 快捷操作添加，并将其发布为备注（`glab issue note <child> --message "/blocked_by #<blocker>"`）。原生阻塞链接是 Premium/Ultimate 功能；在免费层级（或不可用时），回退到描述顶部的 `Blocked by: #<n>, #<n>` 行。当每个阻塞项都关闭时，票解除阻塞。
- **前沿查询**：将 `glab issue list -F json` 的范围限定为地图的子票，丢弃存在开放阻塞项——指向开放议题的原生 `blocked_by` 链接（`glab api projects/:id/issues/:iid/links`），或 `Blocked by` 行中的开放议题——或已有受理人的票；按地图顺序最靠前者优先。
- **认领**：`glab issue update <n> --assignee @me`——会话中的首次写入。
- **解决**：`glab issue note <n> --message "<answer>"`，然后 `glab issue close <n>`，再将上下文指针（gist + 链接）追加到地图的“目前决策”部分。

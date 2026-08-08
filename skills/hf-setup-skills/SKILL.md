---
name: hf-setup-skills
description: 为工程技能配置此仓库——设置其议题跟踪器、分诊标签词汇和领域文档布局。在首次使用其他工程技能前运行一次。
---

# 设置技能

搭建工程技能所依赖的仓库级配置：

- **议题跟踪器**——议题存放的位置（默认为 GitHub；也原生支持本地 Markdown）
- **分诊标签**——五种规范分诊角色所使用的字符串
- **领域文档**——`CONTEXT.md` 和 ADR 的存放位置，以及读取它们的消费方规则

这是一个由提示驱动的技能，而不是确定性脚本。先探索，展示发现，与用户确认，然后写入。

## 流程

### 1. 探索

查看当前仓库以了解其初始状态。读取实际存在的内容；不要作假设：

- `git remote -v` 和 `.git/config`——这是 GitHub 仓库吗？具体是哪一个？
- 仓库根目录下的 `AGENTS.md` 和 `CLAUDE.md`——其中是否有文件存在？其中是否已有 `## Agent skills` 小节？
- 仓库根目录下的 `CONTEXT.md` 和 `CONTEXT-MAP.md`
- `docs/adr/` 和任何 `src/*/docs/adr/` 目录
- `docs/agents/`——此技能之前的输出是否已经存在？
- `.scratch/`——表明已在使用本地 Markdown 议题跟踪器约定
- 是否安装了 `hf-triage` 技能？（与本技能并列的 `hf-triage` 技能文件夹，或可用技能中有 `hf-triage`。）这决定了是否执行 B 节。
- 单体仓库信号——`pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 字段，或包含自身 `src/` 且有内容的 `packages/*`。这些信号只会出现在真正的大型多包仓库中；没有这些信号就意味着单上下文，而几乎所有仓库都是如此。

### 2. 展示发现并询问

总结已有内容和缺失内容。然后按顺序处理各节——每次一节、一个回答，再进入下一节。

每节先给出推荐答案，让用户只需一个词即可接受。只有选择确实会产生分支时才提供一行说明；如果探索已经确定答案，则完全跳过该节（未安装 `hf-triage` 时跳过 B 节，未发现 monorepo 时跳过 C 节）。

**A 节——议题跟踪器。**

> 说明：“议题跟踪器”是此仓库议题的存放位置。`hf-to-tickets`、`hf-triage` 和 `hf-to-spec` 等技能会读写它——它们需要知道应该调用 `gh issue create`、在 `.scratch/` 下写入 Markdown 文件，还是遵循你描述的其他工作流。请选择你实际跟踪此仓库工作的地方。

默认立场：这些技能是为 GitHub 设计的。如果 `git remote` 指向 GitHub，就推荐 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自托管主机），就推荐 GitLab。否则（或用户有偏好时），提供：

- **GitHub**——议题存放在仓库的 GitHub Issues 中（使用 `gh` CLI）
- **GitLab**——议题存放在仓库的 GitLab Issues 中（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 Markdown**——议题作为文件存放在此仓库的 `.scratch/<feature>/` 下（适合个人项目或没有远程仓库的仓库）
- **其他**（Jira、Linear 等）——请用户用一段话描述工作流；技能会将其记录为自由格式文本

将选择记录在 `docs/agents/issue-tracker.md` 中。GitHub 和 GitLab 模板带有“将 PR 作为请求入口”标志，默认为**关闭**——保持关闭且不要主动提出；希望将外部 PR 纳入分诊队列的用户以后可以在文件中切换该标志。

**B 节——分诊标签词汇。** 如果未安装 `hf-triage` 技能（探索阶段会告诉你），则完全跳过本节——未安装的技能不需要标签。

如果已安装，只问一个问题：

> 你想保留默认分诊标签吗？（推荐：**是**）

默认值是五种规范角色，每个标签字符串均与其名称相同：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。用户回答**是**时，原样写入。仅当用户回答否时——通常是因为其跟踪器已使用其他名称（例如用 `bug:triage` 表示 `needs-triage`）——才收集覆盖值，使 `hf-triage` 应用现有标签而不是创建重复标签。

**C 节——领域文档。** 默认为**单上下文**——仓库根目录中一个 `CONTEXT.md` 加 `docs/adr/`。这适用于几乎所有仓库；无需询问，直接写入。

仅当探索发现单体仓库信号时才提供**多上下文**——根目录 `CONTEXT-MAP.md` 指向每个上下文的 `CONTEXT.md` 文件。然后确认用户想要哪种布局。

### 3. 确认并编辑

向用户展示以下内容的草稿：

- 要添加到正在编辑的 `CLAUDE.md` / `AGENTS.md` 中的 `## Agent skills` 区块（选择规则见第 4 步）
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 和 `docs/agentshf-triage-labels.md` 的内容（最后一个仅在安装了 `hf-triage` 时）

写入前让用户进行编辑。

### 4. 写入

**选择要编辑的文件：**

- 如果 `CLAUDE.md` 存在，编辑它。
- 否则，如果 `AGENTS.md` 存在，编辑它。
- 如果两者都不存在，询问用户要创建哪一个——不要替用户选择。

当 `CLAUDE.md` 已存在时绝不要创建 `AGENTS.md`（反之亦然）——始终编辑已经存在的文件。

如果所选文件中已存在 `## Agent skills` 区块，就原地更新其内容，而不是追加重复区块。不要覆盖用户对周边章节的编辑。

区块内容：

```markdown
## Agent skills

### Issue tracker

[用一行总结议题跟踪位置]。参见 `docs/agents/issue-tracker.md`。

### Triage labels

[用一行总结标签词汇]。参见 `docs/agentshf-triage-labels.md`。

### Domain docs

[用一行总结布局——“单上下文”或“多上下文”]。参见 `docs/agents/domain.md`。
```

仅当安装了 `hf-triage` 且执行了 B 节时，才包含 `### Triage labels` 子区块并写入 `docs/agentshf-triage-labels.md`。否则两者都省略。

然后以此技能文件夹中的种子模板为起点写入文档文件：

- [issue-tracker-github.md](./issue-tracker-github.md)——GitHub 议题跟踪器
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)——GitLab 议题跟踪器
- [issue-tracker-local.md](./issue-tracker-local.md)——本地 Markdown 议题跟踪器
- [triage-labels.md](.hf-triage-labels.md)——标签映射（仅当安装了 `hf-triage` 时）
- [domain.md](./domain.md)——领域文档消费方规则和布局

对于“其他”议题跟踪器，根据用户的描述从头编写 `docs/agents/issue-tracker.md`。

### 5. 完成

告诉用户设置已完成，以及现在有哪些工程技能会读取这些文件。说明以后可以直接编辑 `docs/agents/*.md`——只有在想切换议题跟踪器或从头重新开始时，才需要再次运行此技能。

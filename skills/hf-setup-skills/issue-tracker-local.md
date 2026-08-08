# 议题跟踪器：本地 Markdown

此仓库的议题和规格以 Markdown 文件形式存放在 `.scratch/` 中。

## 约定

- 每个特性一个目录：`.scratch/<feature-slug>/`
- 规格位于 `.scratch/<feature-slug>/spec.md`
- 实现议题按每张票一个文件存放在 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 开始编号——绝不要使用单个合并票文件
- 分诊状态记录在每个议题文件顶部附近的 `Status:` 行中（角色字符串见 `triage-labels.md`）
- 评论和对话历史追加到文件底部的 `## Comments` 标题下

## 当技能要求“发布到议题跟踪器”时

在 `.scratch/<feature-slug>/` 下创建新文件（需要时创建目录）。

## 当技能要求“获取相关票”时

读取所引用路径下的文件。用户通常会直接传入路径或议题编号。

## 寻路操作

供 `/wayfinder` 使用。**地图**是一个文件，每张票对应一个**子**文件。

- **地图**：`.scratch/<effort>/map.md`——正文包含笔记 / 目前决策 / 迷雾。
- **子票**：`.scratch/<effort>/issues/NN-<slug>.md`，从 `01` 开始编号，正文中写入问题。`Type:` 行记录票类型（`research`/`prototype`/`grilling`/`task`）；`Status:` 行记录 `claimed`/`resolved`。
- **阻塞**：顶部附近的 `Blocked by: NN, NN` 行。当所列每个文件均为 `resolved` 时，票解除阻塞。
- **前沿**：扫描 `.scratch/<effort>/issues/`，查找开放、未阻塞且未认领的文件；编号最小者优先。
- **认领**：在开展任何工作前设置 `Status: claimed` 并保存。
- **解决**：在 `## Answer` 标题下追加答案，设置 `Status: resolved`，然后将上下文指针（gist + 链接）追加到 `map.md` 中地图的“目前决策”部分。

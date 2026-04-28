# HF Worktree Isolation

## Purpose

这份共享文档定义 `hf-*` workflow family 如何使用 Git worktree 提供隔离工作目录。

它回答 4 个问题：

1. 什么时候应要求隔离工作目录
2. feature `progress.md` 里如何表达这类状态
3. `hf-test-driven-dev` 与 review dispatch 应如何复用同一 worktree
4. closeout 时如何记录 worktree 的最终处置，而不是把它留在聊天里

核心原则沿用 `using-git-worktrees` 的思路，但按 HF runtime 语义改写为：

- 目录选择要稳定
- 安全校验不能跳过
- worktree 决策要落到状态工件
- 一旦进入隔离工作目录，下游节点必须消费同一份路径上下文

## Coordination Fields

这些字段不是 canonical progress core 的强制字段，但当 workflow 需要隔离工作目录时，推荐追加到 feature `progress.md`（默认 `features/<active>/progress.md`）或等价状态工件：

| 字段 | 推荐值 / 写法 | 含义 |
|---|---|---|
| `Workspace Isolation` | `in-place` / `worktree-required` / `worktree-active` | 当前是否允许在主工作区执行，还是必须 / 已经进入 worktree |
| `Worktree Path` | 实际 worktree 根路径 | 当 `Workspace Isolation=worktree-active` 时必填 |
| `Worktree Branch` | 实际分支名 | 当当前 worktree 已绑定分支时建议填写 |

约束：

- `Workspace Isolation=in-place`：允许继续使用当前工作区；不得伪造 `Worktree Path`
- `Workspace Isolation=worktree-required`：下游代码修改节点必须先创建 / 复用 worktree，再进入实现或验证
- `Workspace Isolation=worktree-active`：下游节点必须复用 `Worktree Path`，不要静默退回主工作区
- 若当前 workflow 不需要隔离工作目录，这些字段可以留空；不要为了“看起来完整”伪造值

## When To Require Worktree Isolation

优先把 `Workspace Isolation` 设为 `worktree-required` 的典型情况：

- 下一节点将进入 `hf-test-driven-dev`，且当前 `Workflow Profile` 为 `full` 或 `standard`
- 当前实现会改动代码、脚本、生成物、依赖或多文件资产，而不是纯文档修订
- 当前仓库已有用户未提交改动、并行中的其它任务，或工作区明显不是干净基线
- 当前 workflow 需要同时派发 reviewer subagent，且 reviewer 必须检视“候选实现状态”而不是仓库根目录的其它状态
- 项目约定已经声明必须隔离工作目录
- 当前是 hotfix 实现，或验证步骤可能触碰风险较高的运行命令 / 环境准备动作

通常可以保留 `in-place` 的场景：

- `lightweight` profile 下的低风险文档修订
- 单文件、低风险、纯文本或配置描述性修改，且当前工作区干净
- 项目约定已明确允许在主工作区中完成这类修改

如果你已经有 `worktree-active` 的状态，并且 `Worktree Path` 与 `Current Active Task` 仍然匹配，优先复用，不要再新建第二个 worktree。

## Directory Selection Priority

创建新的 project-local worktree 时，目录选择遵循以下优先级：

1. 已存在的 `.worktrees/`
2. 已存在的 `worktrees/`
3. 项目级首选 worktree 目录（若项目已声明）
4. 若以上都没有，再询问用户

补充规则：

- 若 `.worktrees/` 和 `worktrees/` 同时存在，优先 `.worktrees/`
- 若项目使用仓库外统一目录，也应优先遵守项目约定
- 不要在没有约定时私自发明新的目录层级

## Safety Verification

对于 project-local 目录（如 `.worktrees/` 或 `worktrees/`），创建前必须先确认目录被 Git ignore：

```bash
git check-ignore -q .worktrees
git check-ignore -q worktrees
```

若目标目录未被 ignore：

- 不要继续创建 worktree
- 优先查看 项目约定是否允许改用仓库外目录
- 若必须继续使用 project-local 目录，则先补齐 ignore 规则，再继续
- 若补 ignore 会引入与当前任务无关的仓库更改，先向用户确认或把它报告为当前 hard stop

原因：

- 未被 ignore 的 worktree 目录会污染 `git status`
- 污染后的状态会直接破坏 HF 的 fresh evidence 与 review 输入判断

## Provisioning Protocol

当下游节点读到 `Workspace Isolation=worktree-required` 时，按以下顺序操作：

1. 先检查 `Worktree Path` 是否已经存在且可复用；若可复用，升级为 `worktree-active`
2. 若尚未分配 worktree，按目录优先级选择位置
3. 为 project-local 目录做 ignore 校验
4. 根据 `Current Active Task`、hotfix ID 或项目分支约定生成分支名
5. 执行 `git worktree add <path> -b <branch>`，或按项目约定复用现有分支
6. 进入该 worktree，运行最小必要 setup
7. 运行当前任务的基线证明命令，确认 worktree 不是从一开始就坏的
8. 将 `Workspace Isolation` 更新为 `worktree-active`，并写回 `Worktree Path` / `Worktree Branch`

分支命名优先级：

1. 项目分支命名规则（若项目已声明）
2. 当前已有 worktree / branch 命名
3. 若都没有，则使用能回指 `Current Active Task` 的稳定短名

## Baseline Verification

进入 worktree 后，不要立刻开始实现。

至少确认以下内容：

- 必要依赖 / 环境准备已完成
- 当前项目的最小基线命令可以运行
- 若基线失败，你能区分这是环境问题、已有失败，还是当前任务尚未开始前就存在的阻塞

如果基线失败：

- 把失败当作 fresh blocking evidence 写回
- 不要继续编码并假装这是当前任务引入的问题
- 先询问用户是否要继续在“非绿基线”上工作，或回到 router / hotfix 判断

## Downstream Consumption Rules

### `hf-test-driven-dev`

当实现节点看到：

- `Workspace Isolation=worktree-required`：先创建 / 复用 worktree，再进入 TDD
- `Workspace Isolation=worktree-active`：直接在 `Worktree Path` 中完成测试设计确认、RED / GREEN 与实现交接
- `Workspace Isolation=in-place`：仅在当前工作区干净、且项目允许时继续

实现交接块应显式带出：

- `Workspace Isolation`
- `Worktree Path`
- `Worktree Branch`

### review dispatch

当 review 节点需要派发 reviewer subagent 时：

- 若当前是 `worktree-active`，review request 必须把 `Worktree Path` / `Worktree Branch` 一并传给 reviewer
- reviewer 应在同一 worktree 视角下读取候选实现，而不是退回仓库根目录看另一份状态
- review 记录仍写回仓库约定路径，但评审输入必须锚定到同一隔离工作目录

### gates / finalize

gate 或 finalize 不要求总是新建 worktree，但需要：

- 能看出当前 evidence 来源于哪个工作目录 / 分支
- 在 closeout pack 里记录 worktree 是“继续保留用于 PR / merge”还是“已按项目约定清理”

## Cleanup Semantics

`hf-finalize` 只负责记录 worktree 的最终状态，不默认直接删除它。

推荐写法：

- worktree 仍承载未合并分支：记录 `Worktree Path`、`Worktree Branch` 与 PR / merge 状态
- worktree 已在项目流程中清理：把 `Workspace Isolation` 收口回 `in-place`，并清空 `Worktree Path`

没有用户请求或项目明文约定时，不要在收尾阶段擅自删除 worktree。

## Red Flags

- 在未做 ignore 校验的 project-local 目录里创建 worktree
- `worktree-required` 却静默退回主工作区继续实现
- 同一个 `Current Active Task` 重复创建多个平行 worktree，而不是先检查是否已有可复用路径
- reviewer subagent 评审的是仓库根目录，而不是当前候选实现所在的 worktree
- finalize 里把 worktree 是否保留 / 清理留在聊天里，不写回状态工件

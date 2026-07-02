# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**约束 AI 编码代理产出高质量代码的三层技能套件:规范驱动开发 (SDD) + 测试驱动开发 (TDD) + 可插拔领域扩展。**

AI 编码代理习惯从一句模糊的需求直接跳到实现。HarnessFlow 强制它走一条更窄、更严的路:

1. **第一层 — SDD**:先把意图变成可评审、可验收的规格,再谈别的。
2. **第二层 — TDD**:每个行为都由一个先失败的测试拉动产生,交付的代码是被验证过的,而不是"应该没问题"。
3. **第三层 — 扩展**:UI 设计、语言规范等领域技能按阶段加载进主链,并且可以不断新增。

## 主链

```
specify → review → design → review → tdd → review → ship
```

| 阶段 | 技能 | 产出 | 门禁 |
|------|------|------|------|
| 规格 | `hf-specify` | `spec.md` — 编号的、可测试的需求 | 规格评审 + 用户确认 |
| 设计 | `hf-design` | `design.md` — 架构、契约、有序任务清单 | 设计评审 + 用户确认 |
| 实现 | `hf-tdd` | 代码 + 测试,单任务推进,红→绿→重构 | 全部任务测试全绿 |
| 评审 | `hf-review` | 每道门禁落盘的结论与 findings | 结论为"通过" |
| 交付 | `hf-ship` | 逐条需求验收闭环 + 收尾报告 | 验收标准全部闭合 |

所有工件放在 `features/<NNN>-<slug>/`(`spec.md`、`design.md`、`progress.md`、`reviews/`)。任何新会话都从这些文件恢复当前阶段——从不依赖聊天记忆。

## 技能清单

| 技能 | 职责 |
|------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | 入口:主链、工件布局、门禁、状态恢复、扩展加载 |
| [hf-specify](skills/hf-specify/SKILL.md) | 把意图澄清成可测试的规格 (SDD) |
| [hf-design](skills/hf-design/SKILL.md) | 技术设计 + 有序任务拆分 |
| [hf-review](skills/hf-review/SKILL.md) | 一套评审协议、三份阶段 checklist、作者/评审者分离 |
| [hf-tdd](skills/hf-tdd/SKILL.md) | 逐任务红-绿-重构,证据须来自当前会话 (TDD) |
| [hf-ship](skills/hf-ship/SKILL.md) | 最终验收、文档、收尾 |
| [ext-ui-design](skills/ext-ui-design/SKILL.md) | 扩展:UI 特性(信息架构、交互状态、design token、可访问性、反 AI 默认审美) |
| [ext-cpp](skills/ext-cpp/SKILL.md) | 扩展:C++ 项目(GoogleTest 纪律、RAII、测试反模式) |

## 扩展 (第三层)

扩展放在 `skills/ext-*/`,在 frontmatter description 中声明**绑定阶段**与**触发条件**。每个阶段开始前,`hf-workflow` 扫描扩展并加载与当前特性匹配的(如"特性含用户界面""项目是 C++")。扩展只能收紧要求——永远不能放松主链门禁。

编写自己的扩展见 [扩展编写指南](skills/hf-workflow/references/extension-authoring.md)。

## 安装

HarnessFlow 就是纯 Markdown。把本仓库的 `skills/` 目录复制(或以 submodule 引入)到你的项目,再接好客户端:

- **Cursor**:同时把 `.cursor/rules/harness-flow.mdc` 复制到项目的 `.cursor/rules/`,该规则会在每个开发任务时加载 `hf-workflow`。
- **Claude Code**:作为插件安装(`/plugin marketplace add <本仓库>`),或直接 vendor `skills/`——技能靠 frontmatter description 被发现。
- **OpenCode / 其他客户端**:把客户端的技能目录指向 `skills/`(本仓库的 `.opencode/skills` 就是这样一个符号链接)。

然后自然地提需求即可:"用 HarnessFlow:我要给通知 API 加限流。" 代理会进入 `hf-workflow`,从工件恢复阶段并推进。

## 执行模式

- `interactive`(默认):规格与设计评审通过后,代理展示结论并等待你确认。
- `auto`:说"自动执行/不用等我确认"后,评审通过即自动确认(记入 `progress.md`)。评审与门禁照常运行——auto 从不删除它们。

## 设计原则

- **过程落盘。** 评审结论、确认记录、任务进度、测试证据都是文件,任何会话可以冷启动。
- **作者/评审者分离。** 写工件的一方永远不给自己批准。
- **一个技能一件事。** 六个核心技能,没有元机制;评审协议只写一次,每道门禁复用。
- **扩展靠约定,不靠改代码。** 新增领域技能永远不需要动主链。

## License

MIT

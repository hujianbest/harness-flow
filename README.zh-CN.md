# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**驱动 AI 编码代理稳定交付的三层技能套件:主链纪律 (SDD + TDD) + 机械门禁 + 可插拔领域扩展。**

核心假设:**模型是系统里最不可靠的组件。** 会写假测试的模型,同样会写假的"评审通过"。所以 HarnessFlow v3 不把纪律寄托在模型的自觉上——凡是能机械裁决的门禁,都交给脚本;凡是"测试通过/能运行"的声明,都必须有落盘的命令原始输出作证据;凡是评审,都必须发生在不带作者上下文的独立会话里。

1. **第一层 — 主链纪律**:`frame → plan → build → verify → ship`,规格驱动 + 测试驱动,流程开销随风险分级缩放。
2. **第二层 — 机械门禁**:`hf_gate.py` 用文件、结论行、退出码、时间戳机械裁决阶段推进;证据只能由它包装真实命令产生。
3. **第三层 — 扩展**:UI 设计、语言规范等 `ext-*` 领域技能按阶段加载进主链,只收紧、不放松。

## 主链与风险分级

```
frame → plan → build → verify → ship
```

| 阶段 | 技能 | 产出 | 门禁 |
|------|------|------|------|
| 定格 | `hf-frame` | `frame.md` — 意图、风险档位、环境基线证据 | `gate check` |
| 计划 | `hf-plan` | `plan.md`(档位 2)或 `spec.md` + `design.md`(档位 3) | 独立评审 + 用户确认 + `gate check` |
| 实现 | `hf-build` | 代码 + 测试,单任务红→绿→重构,逐任务 red/green 日志 | 任务全勾 + `gate check` |
| 验证 | `hf-verify` | 运行时冒烟证据 + 独立代码评审 | `gate check` |
| 交付 | `hf-ship` | 逐条需求验收闭环 + 收尾报告 | 验收标准全部闭合 |

流程开销随风险缩放:**档位 1**(微改)只走 frame → build → verify → ship;**档位 2**(默认)用一份 `plan.md`;**档位 3**(数据/安全/跨模块)才拆分 spec 与 design、走三轮评审。定错档会被评审打回。

所有工件与证据放在 `features/<NNN>-<slug>/`(`frame.md`、`plan.md`、`progress.md`、`evidence/`、`reviews/`)。任何新会话用 `gate check` 逐阶段探测即可恢复进度——从不依赖聊天记忆。

## 机械门禁

```bash
# 产生证据 —— 测试/构建/冒烟运行的唯一合法方式(原始输出 + 退出码落盘):
python3 skills/hf-workflow/scripts/hf_gate.py run --feature features/001-x --label t1-red -- pytest tests/

# 校验能否进入目标阶段(文件、评审结论、红绿日志、退出码、时间戳全部机械判定):
python3 skills/hf-workflow/scripts/hf_gate.py check --feature features/001-x --to build
```

gate 机械拦截的典型造假:没有失败记录的"红"、最新一次仍是失败的"绿"、代码改完没重跑的全量测试、缺失的冒烟证据、降级评审给自己写 auto-approved。gate 只看形式,语义质量由独立评审把关——二者缺一不可。

## 技能清单

| 技能 | 职责 |
|------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | 入口:主链、风险分级、工件与证据布局、gate 用法、状态恢复、扩展加载 |
| [hf-frame](skills/hf-frame/SKILL.md) | 定格意图、定风险档位、建环境基线(项目能不能真实验证) |
| [hf-plan](skills/hf-plan/SKILL.md) | 计划:可测需求 + 设计 + 机器可读任务清单;禁止槽位幻觉 |
| [hf-build](skills/hf-build/SKILL.md) | 逐任务红-绿-重构,每次运行经 `hf_gate.py run` 留证 (TDD) |
| [hf-verify](skills/hf-verify/SKILL.md) | 三层验证:运行时冒烟、独立代码评审、机械门禁收口 |
| [hf-review](skills/hf-review/SKILL.md) | 评审协议:只承认 subagent/新会话,降级不得自我确认;代码评审者自己跑测试 |
| [hf-ship](skills/hf-ship/SKILL.md) | 最终验收、文档、收尾 |
| [ext-ui-design](skills/ext-ui-design/SKILL.md) | 扩展:UI 特性(信息架构、交互三态、design token、可访问性、真实渲染证据) |
| [ext-cpp](skills/ext-cpp/SKILL.md) | 扩展:C++ 项目(GoogleTest 纪律、RAII、测试反模式) |

## 扩展 (第三层)

扩展放在 `skills/ext-*/`,在 frontmatter description 中声明**绑定阶段**(frame/plan/build/verify/ship 的子集)与**触发条件**。每个阶段开始前,`hf-workflow` 扫描扩展并加载与当前特性匹配的(如"特性含用户界面""项目是 C++")。扩展只能收紧要求——永远不能放松主链门禁。

编写自己的扩展见 [扩展编写指南](skills/hf-workflow/references/extension-authoring.md)。

## 安装

HarnessFlow 是纯 Markdown + stdlib Python 脚本(随仓库一起走,无任何依赖)。Cursor 和 OpenCode 推荐直接使用安装器:

```bash
python scripts/install.py --target cursor --dest /path/to/project
python scripts/install.py --target opencode --dest /path/to/project
python scripts/install.py --target both --dest /path/to/project
./install.sh --target both --dest /path/to/project
./install.ps1 -Target both -Dest C:\path\to\project
```

默认安装方式是复制 HarnessFlow 资产。需要目标项目跟随当前 checkout 时,可追加 `--mode symlink`(PowerShell 使用 `-Mode symlink`)。

- **Cursor**:安装到 `.cursor/harness-flow-skills/`,并写入路径已重写的 `.cursor/rules/harness-flow.mdc`。
- **Claude Code**:作为插件安装(`/plugin marketplace add <本仓库>`),或直接 vendor `skills/`——技能靠 frontmatter description 被发现。
- **OpenCode / 其他客户端**:安装到 `.opencode/skills/`,并保留用户已经放在该目录下的自定义 skills。

然后自然地提需求即可:"用 HarnessFlow:我要给通知 API 加限流。" 代理会进入 `hf-workflow`,用 gate 恢复阶段并推进。

## 执行模式

- `interactive`(默认):plan 层评审通过后,代理展示结论并等待你确认。
- `auto`:说"自动执行/不用等我确认"后,评审通过 + gate PASS 即自动推进。两条底线不变:评审必须由 subagent/新会话执行(降级评审在 auto 下是硬停点),gate 不可绕过。

## 设计原则

- **证据即机器输出。** "测试全绿"四个字不是证据,`evidence/` 里带退出码的原始日志才是。
- **机器管形式,评审管语义。** 能机械裁决的绝不交给模型自觉;需要判断的必须在干净上下文里判断。
- **流程开销随风险缩放。** 微改不付大流程的税,高危改动跑不掉三轮评审。
- **过程落盘。** 评审结论、确认记录、证据日志都是文件,任何会话可以冷启动。
- **扩展靠约定,不靠改代码。** 新增领域技能永远不需要动主链。

## License

MIT

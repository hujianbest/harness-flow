# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**牵引 AI 编码代理从一个想法出发搭建出可用的 APP、并稳定完成日常特性交付的 harness 工程:产品层塑形 + 主链纪律 (SDD + TDD) + 机械门禁 + demo 验收 + 可插拔领域扩展。**

HarnessFlow 对抗四个不可靠因素,每一个机制都由其一推出:

1. **模型不可靠** → 机械门禁:阶段推进由 `hf_gate.py` 依据文件、结论行、退出码、时间戳机械裁决;证据只能由它包装真实命令产生,叙述永远不算证据。
2. **意图欠定** → 欠定不静默填补:用户没说清的决策点,代理提出带观点的默认值,记入 `product/assumptions.md` 假设台账后继续;用户随时可以推翻假设,触发受控返工。
3. **会话必死** → 一切状态落盘;`hf_gate.py status` 一条命令冷启动恢复(产品层状态、每个特性所在阶段、下一步)。
4. **用户不读代码** → demo 即门禁:用户可感知的切片必须有 demo 证据(录屏/截图/预览探活)加落盘的用户验收才能 ship。用户对着规格说"好"是廉价信号,对着运行中的产品的反应才是真实信号。

## 两条入口路径

**想法 → APP(绿地)**:用户带着一个想法,代码还不存在:

```
shape(hf-shape 塑形) → S-1 行走骨架(hf-skeleton) → 切片循环 ⟲ → 演化
```

- `hf-shape` 用结构化访谈(给谁用/解决什么痛/成功长什么样/明确不做什么)产出产品层:`product/product.md`(愿景、MVP 边界、不做清单)、`decisions.md`(已确认决策)、`assumptions.md`(代理替用户选的默认值)、`backlog.md`(端到端可演示的垂直切片)。技术栈来自带观点的预设——不逼非技术用户选框架。
- `hf-skeleton` 把切片 S-1 定为行走骨架:脚手架、一键 `dev`/`test`、一条最薄的真实端到端路径、第 0 天用户就能打开的东西。集成风险当天暴露,反馈循环先于一切功能开发启动。
- 之后每个切片走交付链,以用户体验 demo 收尾;反馈在 ship 时回写 backlog 与台账。

**存量项目特性交付**:需求相对清楚、代码库已存在 → 直接从 `hf-frame` 进入,不需要产品层。

## 交付链、双模式与风险分级

```
建造模式(默认): frame → plan → build → verify → ship
探索模式:       frame → build → close      (原型即弃)
```

模式由一个变量决定:**代码会被保留吗?** 建造模式走全纪律(TDD、评审、证据);探索模式用于快速验证方向——仅限档位 1 风险面,永远不能 ship,以 `conclusion.md` 收尾;原型只能作为重写的参考,禁止直接晋升。

| 阶段 | 技能 | 产出 | 门禁 |
|------|------|------|------|
| 塑形 | `hf-shape` | `product/` 四文件 | `gate check --product` |
| (S-1) | `hf-skeleton` | 可运行的应用空壳(走交付链) | 同交付链 |
| 定格 | `hf-frame` | `frame.md` — 意图、模式、风险档位、用户可感知、环境基线 | `gate check` |
| 计划 | `hf-plan` | `plan.md`(档位 2)或 `spec.md` + `design.md`(档位 3) | 独立评审 + 用户确认 + `gate check` |
| 实现 | `hf-build` | subagent 完成代码 + 测试,单任务红→绿→重构,逐任务 red/green 日志 | 任务全勾 + `gate check` |
| 验证 | `hf-verify` | 运行时冒烟 + 独立代码评审 + demo 验收 | `gate check` |
| 交付 | `hf-ship` | 逐条需求验收闭环 + 反馈回写产品层 + 收尾 | 验收标准全部闭合 |

流程开销随风险缩放:**档位 1**(微改)只走 frame → build → verify → ship;**档位 2**(默认)用一份 `plan.md`;**档位 3**(数据/安全/跨模块)才拆分 spec 与 design、走三轮评审。定错档会被评审打回。

所有工件与证据放在 `product/` 与 `features/<NNN>-<slug>/`(`frame.md`、`plan.md`、`progress.md`、`evidence/`、`reviews/`)。任何新会话一条命令恢复进度——从不依赖聊天记忆。

## 机械门禁

```bash
gate=skills/hf-workflow/scripts/hf_gate.py
python3 $gate init                     # 初始化产品层(绿地路径第一步)
python3 $gate status                   # 冷启动恢复:产品层 + 各特性所在阶段 + 下一步
python3 $gate next                     # 取 backlog 中第一个未完成切片
python3 $gate run --feature features/001-x --label t1-red -- pytest tests/    # 产生证据的唯一合法方式
python3 $gate check --feature features/001-x --to build                       # 能否进入目标阶段
python3 $gate check --product                                                 # 塑形是否完成
```

gate 机械拦截的典型造假:没有失败记录的"红"、最新一次仍失败的"绿"、改完代码没重跑的全量测试、缺失的冒烟证据、可感知切片没有 demo 证据或落盘验收就想 ship、探索原型试图 ship、降级评审给自己写 auto-approved。gate 只看形式,语义质量由独立评审与用户 demo 验收把关——缺一不可。

## 技能清单

| 技能 | 职责 |
|------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | 入口:入口路径、交付链、双模式、风险分级、工件布局、gate 用法、状态恢复、扩展加载 |
| [hf-shape](skills/hf-shape/SKILL.md) | 想法→产品层:结构化访谈、带观点的技术栈预设、假设台账、垂直切片 backlog |
| [hf-skeleton](skills/hf-skeleton/SKILL.md) | 切片 S-1:行走骨架——脚手架、一键 dev/test、最薄真实端到端路径、第 0 天 demo |
| [hf-frame](skills/hf-frame/SKILL.md) | 定格意图、模式、风险档位、用户可感知,建环境基线 |
| [hf-plan](skills/hf-plan/SKILL.md) | 计划:可测需求 + 设计 + 机器可读任务清单;禁止槽位幻觉 |
| [hf-build](skills/hf-build/SKILL.md) | 建造:每个实现任务由 subagent 执行,逐任务红-绿-重构留证 (TDD);探索:即弃原型以结论收尾 |
| [hf-verify](skills/hf-verify/SKILL.md) | 运行时冒烟、独立代码评审、可感知切片的 demo 验收、机械门禁收口 |
| [hf-review](skills/hf-review/SKILL.md) | 评审协议:只承认 subagent/新会话,降级不得自我确认;代码评审者自己跑测试 |
| [hf-ship](skills/hf-ship/SKILL.md) | 最终验收、反馈回写(勾切片、追加新切片、结算假设)、收尾 |
| [ext-ui-design](skills/ext-ui-design/SKILL.md) | 扩展:UI 特性(信息架构、交互三态、design token、可访问性、真实渲染证据) |
| [ext-cpp](skills/ext-cpp/SKILL.md) | 扩展:C++ 项目(GoogleTest 纪律、RAII、测试反模式) |

## 扩展

扩展放在 `skills/ext-*/`,在 frontmatter description 中声明**绑定阶段**(shape/frame/plan/build/verify/ship 的子集)与**触发条件**。每个阶段开始前,`hf-workflow` 扫描扩展并加载与当前特性匹配的(如"特性含用户界面""项目是 C++")。扩展只能收紧要求——永远不能放松主链门禁。

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

- **Cursor**:安装到 Cursor 会自动发现的 `.cursor/skills/`,保留项目中无关的自定义技能,并写入始终生效且路径已重写的 `.cursor/rules/harness-flow.mdc`。
- **Claude Code**:作为插件安装(`/plugin marketplace add <本仓库>`),或直接 vendor `skills/`——技能靠 frontmatter description 被发现。
- **OpenCode / 其他客户端**:安装到 `.opencode/skills/`,并保留用户已经放在该目录下的自定义 skills。OpenCode 只发现该路径下的技能(不认顶层 `skills/` 真源),因此这份拷贝由安装器生成并已 gitignore——`skills/` 是唯一真源。在本仓库内用 OpenCode 时跑:`python scripts/install.py --target opencode --dest .`

然后自然地提需求即可:"我有个想法:做一个帮我管理读书笔记的应用"——代理进入 `hf-shape`,从想法牵引到可运行骨架再到逐片交付。或者:"用 HarnessFlow:给通知 API 加限流"——代理进入 `hf-frame`,用 gate 恢复阶段并推进。

## 执行模式

- `interactive`(默认):plan 层评审通过后与 demo 验收时,代理展示结论/演示并等待你确认。
- `auto`:说"自动执行/不用等我确认"后,评审通过 + gate PASS 即自动推进。底线不变:实现任务必须由 subagent 执行、评审必须由独立 subagent/新会话执行(降级评审在 auto 下是硬停点)、gate 不可绕过、替你做的每个选择都进假设台账、demo 证据在下次交互时主动呈上。

## 设计原则

- **证据即机器输出。** "测试全绿"四个字不是证据,`evidence/` 里带退出码的原始日志才是。
- **产品即验收媒介。** 用户可感知的东西,验收发生在运行中的产品上,不在文档上。
- **欠定显式化。** 默认值要提出、要入账,永远不静默幻觉。
- **机器管形式,评审管语义。** 能机械裁决的绝不交给模型自觉;需要判断的必须在干净上下文里判断。
- **流程开销随风险与存续期缩放。** 微改不付大流程的税,即弃原型不付 TDD 的税(但也永远不能 ship)。
- **过程落盘。** 评审结论、确认记录、台账与证据日志都是文件,任何会话可以冷启动。
- **扩展靠约定,不靠改代码。** 新增领域技能永远不需要动主链。

## License

MIT

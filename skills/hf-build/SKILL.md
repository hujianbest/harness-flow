---
name: hf-build
description: HarnessFlow build 阶段。计划已批准(或档位 1 / 探索模式的 frame 已完成)、任务清单存在未完成任务时使用,也用于代码评审返回"需修改"后的修订。每个实现任务必须派给 subagent 执行,主会话只负责编排与 gate 推进。建造模式以红-绿-重构循环(TDD)逐个完成任务,每次测试运行都必须通过 hf_gate.py run 落盘为证据日志;探索模式允许直接搭原型但产物即弃,以 conclusion.md 收尾走 check --to close。gate check --to build 未通过时不得使用,先回上游。
---

# Build(实现)

目标(建造模式):每一行实现代码都由一个**先失败后通过**的测试拉动,且红与绿都有落盘的机器证据,任何后续会话可以审计。

前提:`gate check --to build` PASS(输出贴入 progress.md)。从任务清单锁定**首个未完成任务**;同一时间只派发一个实现任务。档位 1 无任务清单,把整个改动当作 T-1。

## 执行主体

build 阶段的作者动作必须由 subagent 执行。主会话职责:

- 派发首个未完成任务,只提供必要上下文:本技能路径、feature 目录、frame/plan/design 路径、已加载扩展、目标任务编号、允许的测试命令。
- 要求 subagent 遵循本技能完成 RED/GREEN/REFACTOR,用 `hf_gate.py run` 留证,并只勾选自己完成的任务。
- 接收 subagent 返回的改动摘要、证据日志路径、任务勾选状态与任何阻塞点;随后由主会话运行 `gate check`、更新 progress.md 并决定是否派发下一个任务。

若当前环境不能启动 subagent,必须停下向用户说明并请求显式豁免;不得在主会话里静默完成实现。评审仍按 `hf-review` 另派独立 subagent 或全新会话,不能复用刚完成实现的 subagent 自评。

## 探索模式(原型即弃)

TDD 铁律只约束建造模式——测试的第一性依据是"对将被保留的代码提供回归安全",对即弃原型强制红绿是负收益。探索模式下:

- 允许直接搭原型,速度优先;但一切运行(启动、试跑、渲染)仍走 `hf_gate.py run` 留证(`smoke` / `demo` 标签)——探索的结论必须有真实运行支撑,不能是"我觉得可行"。
- 原型代码放在明确即弃的位置(独立目录/分支),不与正式代码混放。
- 收尾:把学到的东西写入 `features/<NNN>-<slug>/conclusion.md`(验证了什么、结论、对正式实现的建议),运行 `gate check --to close`,PASS 后向用户汇报结论。
- **禁止晋升**:探索特性永远不能 ship(gate 拦截);要正式实现,另起建造模式特性,原型只能作参考重写。

以下章节均为建造模式内容。

## 铁律

```
没有失败的测试,就不写实现代码
没有 evidence/ 日志,就没有发生过测试运行
```

先写了实现?删掉,从测试重新开始;不保留"作参考"。手工创建或编辑 evidence/ 日志 = 造假。例外仅限纯配置、纯文档类任务,且要在 progress.md 说明。

## 单任务循环(任务 T-N)

### 1. 测试设计

动手前列出该任务要验证的行为清单:正向路径、边界值、失败路径,以及预期输入输出。对照计划的测试策略确认分层。mock 只允许出现在真正的外部边界(网络、时钟、文件系统),不允许 mock 被测对象。

### 2. RED — 写失败的测试并留证

一次写一个最小测试,测试名描述行为(如 `rejects_empty_input`)。运行:

```bash
python3 skills/hf-workflow/scripts/hf_gate.py run \
  --feature features/<NNN>-<slug> --label t<N>-red -- <测试命令>
```

- exit 必须非 0,且**读日志确认**失败原因是"行为缺失",不是编译错误或拼写错误——编译失败不是有效 RED,先让测试能编译、因断言失败而红。
- 说不清"为什么预期它失败"就说明还没想清楚要实现什么,回到测试设计。

### 3. GREEN — 最小实现并留证

写让测试通过的最少代码,不顺手加功能、不顺手重构。运行 `run --label t<N>-green -- <测试命令>`,exit 必须为 0。gate 校验的是**最新一份** green 日志,重跑会自然覆盖判定。

### 4. REFACTOR — 保持绿的前提下清理

- 消除刚写代码引入的重复、坏命名、临时结构;只清理本任务触碰的范围。
- **重构改了代码,就必须再跑一次 `run --label t<N>-green`**,让最新证据晚于最后的改动。
- 需要跨模块的结构性调整时,停下来告知用户,不擅自扩大改动面;不引入计划未声明的新抽象层。

### 5. 收尾本任务

在 plan.md / design.md 任务清单把该任务的 `- [ ]` 改为 `- [x]`(唯一事实源);progress.md 只更新"下一步"。取下一个未完成任务,重复循环。

## 全部任务完成后

```bash
python3 skills/hf-workflow/scripts/hf_gate.py run \
  --feature features/<NNN>-<slug> --label suite -- <全量测试命令>
python3 skills/hf-workflow/scripts/hf_gate.py check \
  --feature features/<NNN>-<slug> --to verify
```

suite 必须 exit 0(确认没有破坏既有行为);check PASS 后进 `hf-verify`,RESULT 行记入 progress.md。

## 红线

- 绕过 `hf_gate.py run` 直接跑测试,然后口头声称结果
- 主会话静默执行实现任务,或复用实现 subagent 给自己的改动做独立评审
- 测试一写就绿(说明它没有验证新行为,重写;gate 也会因缺少非 0 的 red 日志拦下)
- 为了转绿弱化断言、跳过用例、在测试里复刻实现逻辑
- 并行推进多个任务,或跳过任务清单顺序而不说明理由
- 引用旧会话 / CI 的结果充当本次证据
- 实现中发现计划有错 → 停下回 `hf-plan` 修订并重走评审,不"先按自己的想法改了再说"

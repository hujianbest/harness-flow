---
name: hf-review
description: 在规格、设计、测试或代码需要独立评审时使用：阶段产物完成后把关（R1=spec、R2=design、R3=test+code）、人要求 review、或对既有产物做专项检查。评审由作者之外的独立上下文（hf-reviewer subagent）执行，产出 findings 与 verdict，不修改被评审对象。
---

# HarnessFlow 评审

## 总览

评审是 human-on-the-loop 的支点：AI 生产，独立评审暴露问题，人做最终把关。它是工作流的**必经节点**：`specify`、`design`、`tdd` 每个阶段产物完成后都经评审（R1/R2/R3，见 `using-hf` 工作流），通过前不进入下一阶段。本技能是 HarnessFlow 中**唯一**承担评审的技能——R1/R2/R3 三类门禁都在这里，按评审对象选择对应 rubric，不拆成多个评审技能。三条不变量：

1. **作者不自审。** 写产物的会话/agent 不能给自己出 verdict。评审由独立 subagent（`hf-reviewer`）或新会话执行——它没有作者的写作记忆，只能依赖产物本身，这正是「可冷读」的检验方式。
2. **评审者不动手修。** 评审产出 findings 和 verdict，修改由作者根据 findings 执行。裁判不下场。
3. **没有记录的评审等于没有评审。** 每轮评审必须在 `reviews/` 落盘一份记录；findings 的修复过程必须回写同一份记录（Resolution 闭环）。口头说「评审过了」而 `reviews/` 里没有对应文件与闭环记录，按未评审处理。

评审不是流程仪式。一次好的评审 = 带着「这东西哪里会骗我」的怀疑去读：规格会在哪里被两种人读出两种意思？测试会放过哪种错误实现？代码哪里在对读者撒谎？

> 本节自检：[ ] 当前是三类评审之一（R1/R2/R3）且选对 rubric；[ ] 确认评审者不是产物作者；[ ] 评审者只读不写被评审对象。

## 三类评审与 rubric

| 评审门禁 | 评审对象 | Rubric | 上游输入 | 核心怀疑 |
|---|---|---|---|---|
| R1 spec | `features/<id>-<slug>/spec.md` | `references/spec-review-rubric.md` | 用户原始请求/上游单据 | 两个不同的人读这份规格，会做出同一个东西吗？ |
| R2 design | `design.md`（及影响组件边界时的 `component-design-draft.md`） | `references/design-review-rubric.md` | 已确认的 spec.md、组件根 `docs/component-design.md` | 拿着这份设计，实现者还要「发明」什么吗？复杂度配得上规格吗？ |
| R3 test + code | 测试代码 + `plan.md` 证据行 + 实现 diff | `references/test-review-rubric.md` + `references/code-review-rubric.md` + `hf-clean-code` | design.md 测试设计表、spec.md 验收标准 | 测试会放过哪种错误实现？代码哪里在对读者撒谎？ |

R3 是一次评审但按两个 rubric 分别过测试和代码；测试评审与代码评审可同轮记录，也可拆成两份记录，但都挂在同一 R3 门禁下。

> 本节自检：[ ] R3 同时覆盖测试与代码两个 rubric（不因「测试全绿」跳过代码评审，反之亦然）；[ ] 评审设计给了 spec、评审代码给了 design+diff。

## 工作流

### 1. 以独立上下文执行

派发 `hf-reviewer` subagent（agent name: `hf-reviewer`，角色定义见 `agents/hf-reviewer.md`；OpenCode 通过 `task` 工具传入 agent name，task prompt 为评审输入；Claude Code / Cursor 按各自等价机制）执行评审，输入只给：被评审产物、它的上游工件（评审设计给 spec，评审代码给 design + diff）、对应 rubric、代码评审时的 `hf-clean-code`、适用的 `<language>-coding-standards` / 领域技能。**不给**作者的推理过程和聊天历史。独立上下文意味着评审者没有写作记忆，只能靠产物可冷读——这正是独立评审的意义。

### 2. 产出 findings 与 verdict

每条 finding：`位置 + 问题 + 为什么是问题 + 严重级 + 分类 + 建议返工阶段`。

| 严重级 | 含义 | 例 |
|---|---|---|
| `critical` | 不修不能继续：会导致做错事、留 bug 或不可审 | 验收标准不可测试；测试断言放过 mutation；错误路径资源泄漏；代码与设计默默不一致 |
| `important` | 完成前应修 | 边界用例缺失；函数职责混杂；命名误导 |
| `minor` | 建议改进 | 措辞、风格微调 |

| 分类 | 含义 | 处理 |
|---|---|---|
| `LLM-FIXABLE` | 信息已足够，作者可按 finding 定向修复 | 不问人，回对应作者阶段修复并复审 |
| `USER-INPUT` | 缺业务事实、优先级、验收阈值、外部来源确认 | 只问 finding 指向的最小问题，拿到回答后再修 |
| `TEAM-EXPERT` | 需要模块架构师、资深工程师或团队规则裁决 | 把问题封装成 1-2 个具体决策点上抛，不在评审或作者阶段擅自决定 |

verdict 三选一：

- `通过`：无 critical/important，或仅剩已被人接受的 minor
- `需修改`：findings 可定向修复，修复后复审
- `重新设计`：问题出在上游（规格漏洞、设计方向错误），打回对应阶段

建议返工阶段按问题本质填写：

| 问题本质 | 返工阶段 |
|---|---|
| 规格不可测试、缺业务事实、Change Type / Existing Behavior 错 | `hf-specify` |
| 设计契约、错误模型、测试设计、组件边界错误 | `hf-design` |
| R3 中的测试断言、RED 证据、实现 bug、代码整洁问题 | `hf-tdd` |

R3 的 `需修改` 默认回 `hf-tdd`：测试弱就先补强或重写会失败的测试，代码问题就用 RED/GREEN/REFACTOR 或纯 REFACTOR 修复。只有 finding 明确证明规格或设计工件本身错误，才回 `hf-specify` / `hf-design`。

### 3. 落盘评审记录（必做，与评审同时发生）

记录写入同一工件根下 `features/<id>-<slug>/reviews/<目标>-review-<日期>.md`（或团队覆盖路径），同一目标的复审追加轮次后缀（`-r2`、`-r3`）。每份记录包含：评审对象（含版本/commit）、findings 表（**含 Resolution 列**、分类、建议返工阶段）、verdict、抽查记录（如做了 mutation 自检，写明改了哪行、哪个测试红了）。格式见 `references/review-record-template.md`。

### 4. Findings 闭环（作者侧职责）

verdict 为 `需修改` / `重新设计` 时，作者按 findings 返工，并**逐条回写**原评审记录的 Resolution 列：

- 修复了：怎么改的 + commit 锚点
- 人接受不修：理由 + 谁接受的
- 升级为债务：登记去向（`plan.md` 债务节 / 新工作项）

返工顺序：

1. 先收集 `USER-INPUT` 与 `TEAM-EXPERT` 的答案；同一决策面合并成最少问题，不把整份评审记录丢给人。
2. 再修 `LLM-FIXABLE` findings；只改 finding 指向的行、章节、测试或代码，不借机重写无关内容。
3. 回填每条 finding 的 Resolution 后发起复审（新轮次记录）。

全部 critical/important 有 resolution 后才能复审。**Resolution 列有空着的 critical/important，门禁不算通过**——`hf-ship` 的 DoD 会核验这一点。复审必须核对上一轮 Resolution 与实际 diff 一致；问题不能在新记录里「凭空消失」。

### 5. 人工确认（按运行模式）

- `attended`（默认）：把评审记录与 verdict 呈给人，**人同意后才进入下一阶段**；人的否决/接受意见记入评审文件。
- `unattended`：不停顿，但本技能的其余动作一项不少——独立评审、落盘记录、critical 阻塞返工与复审照常执行；人工确认列记 `N/A(unattended)`，供人事后统一审计 `reviews/`。

在 `plan.md` 门禁表更新本轮门禁状态与记录路径：`pending` 表示等待评审，`passed` 表示评审通过，`rework` 表示必须先回作者阶段修复。R3 评审为 `rework` 时，下一步是 `hf-tdd`，不是再次直接评审，也不是进入 `hf-ship`。

同一 R 节点最多自动返工复审 3 轮。第 3 轮仍有未闭环 critical/important，或持续出现新的同级问题，停止自动循环，把剩余问题、已修证据和需要人裁决的具体问题呈给人。

> 本节自检：[ ] findings 每条带位置 + 严重级 + 分类 + 返工阶段；[ ] `reviews/` 有落盘记录且含 Resolution 列；[ ] 复审核对 Resolution 与 diff 一致；[ ] attended 下人确认后才放行。

## R1/R2/R3 rubric 速览

完整 rubric 见 `references/`。这里给出三类评审不过即判 critical 的核心检查项（非全表）：

**R1 spec（核心怀疑：两人同读会做出同一东西吗）**
- 每条 FR/IFR 的 Acceptance 是 Given/When/Then 且能落成一个失败测试；无「足够快」「合理」等不可判定词
- 每条 FR/NFR/IFR/CON 有 Change Type；`modify`/`remove` 有 Existing Behavior 基线（无把改既有接口/错误码伪装成 `new`）
- Statement/Acceptance 无实现细节走私（函数签名、数据结构、库选择）
- `traceability.md` 已初始化；`plan.md` 骨架（运行模式、门禁表、计划边界）已建

**R2 design（核心怀疑：实现者还要发明什么吗、复杂度配得上规格吗）**
- 每个对外接口六项齐全（输入前置/输出后置/错误语义/副作用/并发时序/兼容性）；错误模型三件事已定
- 每个抽象/间接层指得出真实用例或真实变化轴；无单实现接口、无「以后可能需要」
- spec Acceptance 与 design Case ID 双向可追溯；无孤儿用例或漏测验收
- 测试设计：每条验收映射到用例；FR 有正向+异常；NFR 的 Response Measure 有可量化用例；mock 只在真实边界

**R3 test（核心怀疑：测试会放过哪种错误实现）**
- 测试设计表每个用例有对应测试；plan 任务覆盖的 Case ID 集合 = design 测试设计表全集
- 抽查 2-3 个关键测试做 mutation 自检并记录：改错实现关键行，测试必须变红
- plan.md 每个 done 任务有 RED/GREEN/REFACTOR 证据行（命令 + 输出 + commit）；RED 失败原因是行为缺失
- 断言覆盖返回值、状态变化、对外输出三类；无弱断言、无永远成功的测试

**R3 code（核心怀疑：代码哪里在对读者撒谎，错误路径先读）**
- 实现行为与 `design.md` 一致；代码与设计默默不一致 = critical
- 每个可失败调用被检查；每条错误路径资源被回收；无吞错误；失败后状态符合契约
- 命名不撒谎、函数单一职责、无未登记的大函数/深嵌套、无裸魔法数、无 test-only 后门
- diff 只含本任务范围；行为变更与重构/格式化未混在一个提交
- 适用语言的 `<language>-coding-standards` 与命中 description 的领域技能已过

详细判定与 verdict 指引见对应 rubric 文件。

## 评审者纪律

- 按 rubric 逐项过，不凭整体印象打分；rubric 之外发现的问题照样列出
- 每条 critical/important finding 给出**具体位置**和**可执行的修复方向**，不写「质量有待提高」
- 抽查重于通读：测试评审必做 2-3 个关键用例的 mutation 自检；代码评审优先读错误路径与资源路径——那是问题密度最高的地方
- 不确定的判断标注「待人裁决」，不假装确定
- 发现产物间漂移（代码与 design 不符、测试与 spec 不符）→ 一律 critical：要么改产物，要么改工件，不允许默默不一致

## 合理化反驳

| 话术 | 现实 |
|---|---|
| 「测试全绿，所以代码没问题」 | 测试只证明外部行为被验证过，不替代 clean-code 自检；错误路径、契约一致、命名撒谎测试都抓不到——这是把「能跑」当「做对了」 |
| 「作者自己也懂这块，让他自审更快」 | 作者对实现假设盲视；自审 = 自我出 verdict，破坏独立评审的前提。这是破坏信任，不是省时间 |
| 「findings 都是 minor 措辞问题，整体不错」 | minor 不该是 findings 的主体；错误路径、断言强度、契约完整性没人提 = 评审走过场 |
| 「reviewer 直接动手改了更省事」 | 裁判下场 = 把独立判断和亲手实现的利益冲突合并到同一个人，findings 的可信度归零 |
| 「reviewer 评审完了，口头说通过」 | `reviews/` 没有记录 = 没评审过；口头 verdict 不可审计、不可恢复 |
| 「unattended 模式，跳过评审」 | unattended 只移除人工停顿，不移除任何质量动作；评审、记录、critical 阻塞照做 |

## 风险信号

- 作者会话自己宣布「评审通过」
- 声称评审完成但 `reviews/` 没有对应记录文件（= 未评审）
- findings 修复后没有回写 Resolution，复审记录里问题「凭空消失」
- findings 全是 minor 措辞建议，对错误路径、断言强度、契约完整性只字不提（评审走过场）
- R3 只做测试评审或只做代码评审，以「测试全绿」为由跳过另一个
- verdict 为「需修改」但 findings 没有一条具体到位置
- 评审者直接动手改了代码
- attended 模式下未经人确认就进入下一阶段；或以「unattended」为由省掉评审/记录本身
- 同一 R 门禁三轮评审仍在打回 → 停止循环，升级人裁决方向问题
- R3 `需修改` 后停在评审上下文里自修，或直接复审而没有作者阶段（`hf-tdd`）的 Resolution 与证据

## 验证清单

评审完成后逐项确认：

- [ ] 评审由独立上下文（`hf-reviewer` subagent 或新会话）执行，评审者不是产物作者
- [ ] 评审对象选对了门禁（R1/R2/R3）与 rubric；R3 同时覆盖测试与代码
- [ ] `reviews/` 落盘了记录：评审对象（含 commit）、findings 表（含 Resolution 列）、verdict、抽查记录
- [ ] 每条 critical/important finding 有具体位置和可执行修复方向；测试评审有 mutation 自检记录
- [ ] critical 阻塞返工；findings 修复后逐条回填 Resolution；复审核对 Resolution 与 diff 一致
- [ ] 产物间漂移被发现并判 critical（不默默放过）
- [ ] attended 模式下 verdict 呈人确认后才进下一阶段；unattended 下评审/记录/critical 阻塞照做
- [ ] 同一 R 门禁未超过 3 轮自动返工复审；超限升级人裁决
- [ ] `plan.md` 门禁表已更新本轮状态与记录路径；R3 `rework` 下一步指向 `hf-tdd`

## 支撑参考

| 文件 | 用途 |
|---|---|
| `references/spec-review-rubric.md` | R1 规格评审检查项（可测试性、变更风险显式、边界纪律、闭环） |
| `references/design-review-rubric.md` | R2 设计评审检查项（契约完整、结构与复杂度、与上游一致、测试设计） |
| `references/test-review-rubric.md` | R3 测试评审检查项（覆盖映射、断言强度、RED 证据、mock 纪律） |
| `references/code-review-rubric.md` | R3 代码评审检查项（正确性、错误路径、整洁标准、范围与 diff 卫生、语言/领域规则） |
| `references/review-record-template.md` | 评审记录模板：评审对象、findings 表（含 Resolution 列）、verdict、抽查记录 |

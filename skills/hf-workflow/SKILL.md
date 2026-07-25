---
name: hf-workflow
description: HarnessFlow 主工作流入口。凡是开发新功能、修改已有行为、修复缺陷、从一个想法搭建新应用,或用户提到"开始开发""继续""恢复进度""harness-flow"时,必须先加载本技能。它定义两条入口路径(想法→APP: shape → skeleton → 切片循环;存量项目: 直接进交付链)、交付链 frame → plan → build → verify → ship、探索/建造双模式、风险分级、产品层与特性工件布局、机械门禁 hf_gate.py 的用法、状态恢复规则,以及领域扩展技能 (ext-*) 的加载方式。不适用于纯问答、代码阅读等不产生代码变更的请求。
---

# HarnessFlow 主工作流

HarnessFlow 对抗四个不可靠因素,全部机制由此推出:

1. **模型不可靠** → 机械门禁:阶段推进由 `skills/hf-workflow/scripts/hf_gate.py` 机械裁决;证据 = 命令原始输出落盘,叙述不算证据。
2. **意图欠定** → 欠定信息显式化:遇到用户没说清的决策点,标准动作是"提出带默认值的选项 → 记入 `product/assumptions.md` 假设台账 → 继续",禁止静默幻觉填补。
3. **会话必死** → 一切状态活在磁盘上,`hf_gate.py status` 一条命令冷启动恢复。
4. **用户不读代码** → demo 即门禁:用户可感知的交付物必须以可运行的产品形态(录屏/截图/预览地址)交给用户体验并验收,文档评审不能替代。

领域扩展 `ext-*` 按阶段自动加载,只收紧、不放松主链。

## 两条入口路径

**想法→APP(绿地)**:用户带着一个产品想法从零开始,或项目尚无 `product/` 产品层:

```
shape(hf-shape 塑形) → S-1 行走骨架(hf-skeleton) → 切片循环 ⟲ → 演化
```

塑形产出产品层四文件;`check --product` PASS 后,backlog 中的切片逐片走交付链;每片以 demo 验收收尾,用户反馈回写 backlog/decisions/assumptions,再取下一片(`hf_gate.py next`)。

**存量项目特性交付**:需求相对清楚、代码库已存在 → 直接从 `hf-frame` 进入交付链,不需要产品层。

## 交付链、双模式与风险分级

```
建造(默认): frame → plan → build → verify → ship
探索:       frame → build → close        (原型即弃)
```

**模式由"代码是否会被保留"决定**:建造模式产物进入产品,走全纪律(TDD、评审、证据);探索模式用于快速验证一个方向/交互,低仪式但产物必须即弃——仅限风险档位 1,永远不能 ship,结论写入 `conclusion.md` 走 `check --to close`,正式实现另起建造特性(原型只能作参考重写,禁止直接晋升代码)。

建造模式的流程开销随风险缩放,frame 阶段定档(判据见 `hf-frame`):

| 档位 | 适用 | plan 形态 | 评审轮次 |
|------|------|-----------|----------|
| 1 微改 | 单点小改,可逆,不碰数据/安全/公共接口 | 无(frame 即计划) | 仅代码评审 |
| 2 标准 | 常规特性、行为变更、缺陷修复(默认档) | 一份 `plan.md` | plan 评审 + 代码评审 |
| 3 高危 | 数据迁移、安全面、跨模块架构、破坏性接口 | `spec.md` + `design.md` 分离 | spec、design、代码三轮评审 |

| 阶段 | 技能 | 产出 | 推进门禁 |
|------|------|------|----------|
| shape | `hf-shape` | product/ 四文件 | `check --product` |
| (S-1) | `hf-skeleton` | 可运行的应用空壳(走交付链,内容收紧) | 同交付链 |
| frame | `hf-frame` | frame.md + 环境基线证据 | `check --to plan`(档位1/探索: `--to build`) |
| plan | `hf-plan` | plan.md 或 spec.md + design.md | 评审通过+确认落盘, `check --to build` |
| build | `hf-build` | 代码 + 测试 + 逐任务 red/green 证据 | 任务全勾, `check --to verify`(探索: `--to close`) |
| verify | `hf-verify` | 冒烟证据 + 独立代码评审 + demo 验收 | `check --to ship` |
| ship | `hf-ship` | 验收报告 + 反馈回写产品层 + 收尾 | 需求逐条闭合 |

到达某阶段时,读取并遵循对应技能的 SKILL.md,不要凭印象执行。

## 工件与证据布局

```
product/               # 产品层(想法→APP 路径;hf_gate.py init 生成模板)
  product.md           # 愿景、目标用户、MVP 边界、不做清单、用户确认 (hf-shape)
  decisions.md         # 已确认决策(含技术栈),只追加
  assumptions.md       # 假设台账:agent 替用户做的默认选择,状态可推翻
  backlog.md           # 垂直切片待办 `- [ ] S-<n> ...`,S-1 固定为行走骨架
features/<NNN>-<slug>/ # 每切片/特性一个目录,<NNN> 取下一个编号,从 001 起
  frame.md             # 意图、模式、风险档位、用户可感知、环境基线 (hf-frame)
  plan.md              # 档位 2: 需求+设计+任务清单 (hf-plan)
  spec.md  design.md   # 档位 3: 规格与设计分离 (hf-plan)
  conclusion.md        # 仅探索模式: 原型结论与建议
  progress.md          # 薄状态文件:阶段指针与下一步
  evidence/            # 原始命令输出日志,只能由 hf_gate.py run 产生
  reviews/             # 评审与验收记录 (hf-review / demo-acceptance)
```

任务勾选状态**只**存在于 plan.md / design.md 的任务清单,切片勾选**只**存在于 backlog.md(各自唯一事实源),progress.md 不复制。progress.md 最小格式:

```markdown
# 进度

- 特性: <NNN>-<slug>(对应切片: S-<n> 或"无")
- 当前阶段: frame | plan | build | verify | ship | close | done
- 执行模式: interactive | auto
- 已加载扩展: <ext-* 列表或"无">
- 下一步: <一句话>
- 门禁输出: <最近一次 gate check 的 RESULT 行>
```

## 机械门禁 (hf_gate.py)

```bash
gate=skills/hf-workflow/scripts/hf_gate.py
python3 $gate init                       # 初始化产品层模板(绿地路径第一步)
python3 $gate status                     # 冷启动恢复:产品层 + 各特性所在阶段 + 下一步
python3 $gate next                       # 取 backlog 中第一个未完成切片
python3 $gate run   --feature features/<NNN>-<slug> --label <label> -- <命令...>   # 产生证据
python3 $gate check --feature features/<NNN>-<slug> --to <plan|design|build|verify|ship|close>
python3 $gate check --product            # 产品层是否就绪
```

- **进入任何阶段前必须运行 check,并把 RESULT 行写进 progress.md。** FAIL 时不得进入,输出即待办清单。
- 证据标签约定:`baseline`(环境基线)、`t<N>-red` / `t<N>-green`(逐任务红绿)、`suite`(全量测试)、`smoke`(运行时冒烟)、`demo`(用户可体验的演示:录屏/截图/预览地址探活)。
- **手工创建或编辑 `evidence/` 下的日志 = 造假**。截图/录屏等非日志证据可直接放入 evidence/(命名 `smoke-*` / `demo-*`)。
- gate 只做机械裁决(文件存在性、结论行、退出码、时间戳),不理解语义;语义质量由 `hf-review` 与用户 demo 验收把关。

## 状态恢复

**从磁盘工件恢复状态,不依赖聊天记忆。** 用户说"继续"或开启新会话时:运行 `hf_gate.py status`,它给出产品层状态、每个特性当前卡在的阶段(第一个 FAIL 的目标)与下一步;FAIL 明细就是待办清单。progress.md 与 gate 输出冲突时,以 gate 为准并修正 progress.md。

## 硬性规则

- **门禁不可跳过**:gate check FAIL 时不进下一阶段;评审结论"需修改"时回作者阶段只修 findings,再评审。
- **作者/评审分离**:评审只承认 subagent 或全新会话;主会话冷读是降级路径且不得自我确认,见 `hf-review`。
- **证据即机器输出**:一切"测试通过/构建成功/能运行"的声明必须有 evidence/ 日志支撑。
- **欠定不静默填补**:替用户做的每个默认选择必须先记入假设台账再继续;用户推翻假设时评估波及、受控返工。
- **demo 即验收**:用户可感知的特性,ship 前必须有 demo 证据与落盘的用户验收(`reviews/demo-acceptance.md`);"用户在聊天里说好"不落盘不算。
- **探索产物即弃**:探索模式代码禁止直接晋升为正式代码;档位 >1 的工作禁止探索模式。
- **单任务推进**:build 阶段同一时间只做一个任务;切片循环同一时间只做一个切片。
- **压力不是豁免**:用户明确坚持跳过某道门禁时,先说明风险,并在 progress.md 记录 `用户豁免 <门禁> <日期>` 后才可继续;口头催促不算豁免。

## 执行模式

- `interactive`(默认):plan 层评审通过后与 demo 验收时,向用户展示并等待确认,确认后才推进。
- `auto`:用户明确说"自动执行/不用等我确认"时启用。评审通过 + gate check PASS 即可推进,确认行写 `auto-approved <日期>`。三条底线:评审必须由 subagent/新会话执行(降级评审在 auto 下是硬停点);gate check 不可绕过;auto 下替用户做的一切选择必须入假设台账,demo 验收虽可 auto-approved,但下次与用户交互时必须主动呈上 demo 证据征求反馈。

## 轻量通道

纯文档、注释、typo 级改动:向用户说明后走档位 1(frame → 改动 → verify 代码评审 → ship)。TDD 铁律对纯文档改动不适用,但改动意图记入 frame.md。改动触碰行为边界时,回到正常档位判定。

## 加载扩展技能

扩展放在 `skills/ext-*/`,frontmatter description 声明**绑定阶段**(shape/frame/plan/build/verify/ship 的子集)与**触发条件**。进入每个阶段前:

1. 列出 `skills/` 下所有 `ext-*` 目录,读取各自 frontmatter 的 description。
2. 触发条件与当前特性匹配(如:特性含 UI、项目是 C++)且绑定阶段包含当前阶段的,加载其 SKILL.md 并遵循。description 是加载判定的唯一依据。拿不准时倾向加载(扩展只会收紧要求),判定理由记入 progress.md。
3. 已加载扩展记入 progress.md;每个阶段开始前重新执行本判定。

扩展只能收紧要求,不能放松主链门禁。编写新扩展见 `references/extension-authoring.md`。

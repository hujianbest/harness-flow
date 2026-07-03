---
name: hf-workflow
description: HarnessFlow 主工作流入口。凡是开发新功能、修改已有行为、修复缺陷,或用户提到"开始开发""继续""恢复进度""harness-flow"时,必须先加载本技能。它定义主链 frame → plan → build → verify → ship、风险分级、工件与证据布局、机械门禁 hf_gate.py 的用法、状态恢复规则,以及领域扩展技能 (ext-*) 的加载方式。不适用于纯问答、代码阅读等不产生代码变更的请求。
---

# HarnessFlow 主工作流

核心假设:**模型是系统里最不可靠的组件。** HarnessFlow 用三层把不可靠的生成能力约束成可靠的交付:

1. **主链纪律**:`frame → plan → build → verify → ship`,规格驱动 (SDD) + 测试驱动 (TDD)。
2. **机械门禁**:阶段推进由 `skills/hf-workflow/scripts/hf_gate.py` 机械裁决;证据 = 命令原始输出落盘,叙述不算证据。
3. **领域扩展**:`ext-*` 技能按阶段自动加载,只收紧、不放松主链。

## 主链与风险分级

```
frame → plan → build → verify → ship
```

流程开销随风险缩放。frame 阶段定档(判据见 `hf-frame`),定错档会被评审打回:

| 档位 | 适用 | plan 形态 | 评审轮次 |
|------|------|-----------|----------|
| 1 微改 | 单点小改,可逆,不碰数据/安全/公共接口 | 无(frame 即计划) | 仅代码评审 |
| 2 标准 | 常规特性、行为变更、缺陷修复(默认档) | 一份 `plan.md` | plan 评审 + 代码评审 |
| 3 高危 | 数据迁移、安全面、跨模块架构、破坏性接口 | `spec.md` + `design.md` 分离 | spec、design、代码三轮评审 |

| 阶段 | 技能 | 产出 | 推进门禁 |
|------|------|------|----------|
| frame | `hf-frame` | frame.md + 环境基线证据 | `gate check --to plan`(档位1: `--to build`) |
| plan | `hf-plan` | plan.md 或 spec.md + design.md | 评审通过+确认落盘, `gate check --to build` |
| build | `hf-build` | 代码 + 测试 + 逐任务 red/green 证据 | 任务全勾, `gate check --to verify` |
| verify | `hf-verify` | 冒烟证据 + 独立代码评审 | `gate check --to ship` |
| ship | `hf-ship` | 验收报告 + 收尾 | 需求逐条闭合 |

到达某阶段时,读取并遵循对应技能的 SKILL.md,不要凭印象执行。

## 工件与证据布局

每个特性一个目录,所有阶段产物与证据落盘于此。`<NNN>` 取 `features/` 下已有编号的下一个,从 `001` 开始:

```
features/<NNN>-<slug>/
  frame.md           # 意图、风险档位、环境基线 (hf-frame)
  plan.md            # 档位 2: 需求+设计+任务清单 (hf-plan)
  spec.md  design.md # 档位 3: 规格与设计分离 (hf-plan)
  progress.md        # 薄状态文件:阶段指针与下一步
  evidence/          # 原始命令输出日志,只能由 hf_gate.py run 产生
  reviews/           # 评审记录 (hf-review)
```

任务勾选状态**只**存在于 plan.md / design.md 的任务清单(唯一事实源),progress.md 不复制任务状态。progress.md 最小格式:

```markdown
# 进度

- 特性: <NNN>-<slug>
- 当前阶段: frame | plan | build | verify | ship | done
- 执行模式: interactive | auto
- 已加载扩展: <ext-* 列表或"无">
- 下一步: <一句话>
- 门禁输出: <最近一次 gate check 的 RESULT 行>
```

## 机械门禁 (第二层)

两条命令贯穿全流程:

```bash
# 产生证据 —— 测试/构建/冒烟运行的唯一合法方式:
python3 skills/hf-workflow/scripts/hf_gate.py run \
  --feature features/<NNN>-<slug> --label <label> -- <命令...>

# 校验能否进入目标阶段:
python3 skills/hf-workflow/scripts/hf_gate.py check \
  --feature features/<NNN>-<slug> --to <plan|design|build|verify|ship>
```

- **进入任何阶段前必须运行 check,并把 RESULT 行写进 progress.md。** check FAIL 时不得进入,输出会列出缺失项,先补齐。
- 证据标签约定:`baseline`(环境基线)、`t<N>-red` / `t<N>-green`(逐任务红绿)、`suite`(全量测试)、`smoke`(运行时冒烟)。
- **手工创建或编辑 `evidence/` 下的日志 = 造假**,等同伪造测试结果。截图等非日志证据可直接放入 evidence/(命名 `smoke-*`)。
- gate 只做机械裁决(文件存在性、结论行、退出码、时间戳),不理解语义;语义质量由 `hf-review` 把关。二者缺一不可。

## 状态恢复

**从磁盘工件恢复状态,不依赖聊天记忆。** 用户说"继续"或开启新会话时:按 plan → design → build → verify → ship 的顺序依次运行 `gate check --to <阶段>`,**第一个 FAIL 的目标即当前所在阶段**,FAIL 明细就是待办清单。progress.md 与 gate 输出冲突时,以 gate 为准并修正 progress.md。

## 硬性规则

- **门禁不可跳过**:gate check FAIL 时不进下一阶段;评审结论"需修改"时回作者阶段只修 findings,再评审。
- **作者/评审分离**:评审只承认 subagent 或全新会话;主会话冷读是降级路径且不得自我确认,见 `hf-review`。
- **证据即机器输出**:一切"测试通过/构建成功/能运行"的声明必须有 evidence/ 日志支撑;"测试全绿"四个字不是证据。
- **单任务推进**:build 阶段同一时间只做一个任务,做完勾掉再取下一个。
- **压力不是豁免**:"时间紧""直接写代码"不构成跳过门禁的理由。用户明确坚持跳过某道门禁时,先说明风险,并在 progress.md 记录 `用户豁免 <门禁> <日期>` 后才可继续;口头催促不算豁免。

## 执行模式

- `interactive`(默认):plan 层评审(plan/spec/design)通过后,向用户展示结论并等待确认,确认后才进下一阶段。
- `auto`:用户明确说"自动执行/不用等我确认"时启用。评审通过 + gate check PASS 即可推进,确认行写 `auto-approved <日期>`。auto 模式两条底线:评审必须由 subagent/新会话执行(降级评审在 auto 下是硬停点,必须等用户);gate check 不可绕过。auto 不删除任何评审与门禁。

## 轻量通道

纯文档、注释、typo 级改动:向用户说明后走档位 1(frame → 改动 → verify 代码评审 → ship)。TDD 铁律对纯文档改动不适用,但改动意图记入 frame.md。改动触碰行为边界时,回到正常档位判定。

## 加载扩展技能 (第三层)

扩展放在 `skills/ext-*/`,frontmatter description 声明**绑定阶段**(frame/plan/build/verify/ship 的子集)与**触发条件**。进入每个阶段前:

1. 列出 `skills/` 下所有 `ext-*` 目录,读取各自 frontmatter 的 description。
2. 触发条件与当前特性匹配(如:特性含 UI、项目是 C++)且绑定阶段包含当前阶段的,加载其 SKILL.md 并遵循。description 是加载判定的唯一依据。触发条件拿不准时倾向加载(扩展只会收紧要求),判定理由记入 progress.md。
3. 已加载扩展记入 progress.md 的"已加载扩展";每个阶段开始前重新执行本判定。

扩展只能收紧要求(追加检查项、证据要求、产出章节),不能放松主链门禁。编写新扩展见 `references/extension-authoring.md`。

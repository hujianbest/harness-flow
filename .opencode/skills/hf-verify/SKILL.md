---
name: hf-verify
description: HarnessFlow verify 阶段。build 全部任务完成、gate check --to verify 通过后使用(探索模式不经本阶段,走 close)。验证手段:运行时冒烟(真实运行最薄端到端路径并留证)、独立代码评审(评审者自己跑测试、读 diff)、用户可感知特性的 demo 验收(录屏/截图/预览地址 + 用户确认落盘)、机械门禁收口(gate check --to ship)。全部通过才进入 hf-ship。
---

# Verify(验证)

目标:用**彼此独立的手段**证明改动真的工作——真实运行证明产品活着,独立评审证明质量过关,demo 验收证明用户要的就是这个,机器裁决证明证据链完整。单元测试全绿不等于产品稳定;文档评审通过不等于用户满意。

前提:`gate check --to verify` PASS(输出贴入 progress.md)。

## 1. 运行时冒烟(作者执行)

真实运行改动触及的最薄端到端路径,不止于测试套件:

- **CLI / 服务**:真启动、真调用一次,`hf_gate.py run --label smoke -- <命令>`,exit 须 0。
- **Web / UI**:在真实运行环境(浏览器/模拟器)渲染后截图,存为 `evidence/smoke-<描述>.png`;可自动化的渲染检查命令走 `run --label smoke`。
- **库**:以真实使用方式(而非测试内部路径)调用一次公开入口,走 `run` 留证。

冒烟失败 → 回 `hf-build`(是行为缺陷就先补一个失败测试再修,仍走 red→green)。

## 2. 独立代码评审

按 `hf-review` 派发代码评审(checklist:`skills/hf-review/references/code-checklist.md`),记录落 `reviews/code-review.md`。评审者的输入只有:工件路径、git diff、代码库本身——**评审者必须自己重跑测试套件、自己读完整 diff,不采信 progress.md 或聊天里的叙述**。

返回"需修改" → 回 `hf-build` 只修 findings(行为变化先走 red→green),然后**重跑 suite、重做受影响的冒烟**,再送复审;复审只确认 findings 是否闭合。

## 3. Demo 与用户验收(仅用户可感知的特性)

frame.md `用户可感知: 是` 的特性,验收媒介是**可运行的产品**,不是文档——用户对着 spec 说"好"是廉价信号,对着运行中的应用说"按钮应该在右边"才是高质量信号。

1. **产出 demo 证据**:用户视角的完整走查——录屏/截图存 `evidence/demo-*`;预览地址/本地服务的探活走 `run --label demo`。冒烟截图不自动等于 demo:demo 必须覆盖本切片的演示判据(backlog 中该切片"用户能看到什么")。
2. **交给用户体验**:给出最短体验路径("一条命令启动,打开 <地址>,做 X 操作"),连同 demo 证据一起呈现。
3. **验收落盘** `reviews/demo-acceptance.md`(gate 机械校验它):

```markdown
# Demo 验收 (S-<n> / <特性名>)

- 日期: YYYY-MM-DD
- 演示物: <evidence/demo-* 文件名、体验路径>
- 结论: 接受 | 需调整
- 用户确认: <日期 | auto-approved 日期>

## 反馈
<用户原话或要点;将由 hf-ship 回写产品层;无则写"无">
```

- `interactive`:等用户体验后裁决;"需调整"→ 反馈中属本切片范围的回 `hf-build` 走流程,新想法记入反馈留给 ship 回写 backlog。
- `auto`:demo 证据齐备可写 `auto-approved`,但下次与用户交互时必须主动呈上 demo 征求反馈。
- 用户在聊天里说"可以" → 仍必须落盘确认行,不落盘不算。

## 4. 机械门禁收口

```bash
python3 skills/hf-workflow/scripts/hf_gate.py check \
  --feature features/<NNN>-<slug> --to ship
```

PASS 条件:代码评审通过且确认落盘、最新 suite 日志 exit 0 且不早于最新 green 证据、smoke 证据存在;用户可感知的特性另需 demo 证据 + demo 验收"接受"且确认落盘。PASS 后进 `hf-ship`,RESULT 行记入 progress.md。

## 红线

- 用单元测试通过替代真实运行("测试都过了"≠"应用能启动")
- 冒烟只跑改动没触及的路径,或用旧截图/旧日志充数
- 用文档/聊天确认替代 demo 验收,或把 smoke 证据直接改名充当 demo
- 评审 findings 未闭合就 check ship("后面再修"不是结论)
- 修复 findings 后不重跑 suite / 冒烟,直接送复审
- 把 gate PASS 当成质量结论(gate 只看形式完整,语义质量在评审与 demo)

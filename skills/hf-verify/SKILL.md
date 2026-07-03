---
name: hf-verify
description: HarnessFlow verify 阶段。build 全部任务完成、gate check --to verify 通过后使用。三层验证:运行时冒烟(真实运行最薄端到端路径并留证)、独立代码评审(评审者自己跑测试、读 diff)、机械门禁收口(gate check --to ship)。全部通过才进入 hf-ship。
---

# Verify(验证)

目标:用**三种彼此独立的手段**证明改动真的工作——真实运行证明产品活着,独立评审证明质量过关,机器裁决证明证据链完整。单元测试全绿不等于产品稳定,三层缺一不可。

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

## 3. 机械门禁收口

```bash
python3 skills/hf-workflow/scripts/hf_gate.py check \
  --feature features/<NNN>-<slug> --to ship
```

PASS 条件:代码评审通过且确认落盘、最新 suite 日志 exit 0 且不早于最新 green 证据、smoke 证据存在。PASS 后进 `hf-ship`,RESULT 行记入 progress.md。

## 红线

- 用单元测试通过替代真实运行("测试都过了"≠"应用能启动")
- 冒烟只跑改动没触及的路径,或用旧截图/旧日志充数
- 评审 findings 未闭合就 check ship("后面再修"不是结论)
- 修复 findings 后不重跑 suite / 冒烟,直接送复审
- 把 gate PASS 当成质量结论(gate 只看形式完整,语义质量在评审)

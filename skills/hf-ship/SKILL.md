---
name: hf-ship
description: HarnessFlow ship 阶段。verify 完成(gate check --to ship 通过)后使用:逐条对照需求验收闭环、同步文档、收尾状态并向用户交付总结报告。gate check --to ship 未通过时不得使用。
---

# Ship(交付)

目标:确认"做的就是计划要的",把工作收尾到**别人(或下一个会话)不需要问你**就能接手的状态。

前提:`gate check --to ship` PASS(输出贴入 progress.md)。

## 流程

### 1. 最终验收(语义层,gate 管不到的部分)

- 逐条对照需求(plan.md 需求章节,或 spec.md):每条 FR 的验收标准 → 指出对应的通过测试与 evidence 日志;每条 NFR → 指出验证证据;冒烟 → 指出对应 evidence 文件。
- 任何一条闭合不了 → 停下,回对应上游阶段(缺测试 → `hf-build`;需求本身变了 → `hf-frame` 重估),不带着缺口交付。

### 2. 文档与记录

- 项目有 CHANGELOG / 使用文档且本次改动影响对外行为 → 同步更新。
- progress.md 的当前阶段改为 `done`。

### 3. 交付报告

在 progress.md 末尾追加收尾摘要,并向用户汇报:

```markdown
## 交付摘要
- 交付内容: <一句话>
- 需求闭合: <N/N 条 FR、N/N 条 NFR 全部验收通过>
- 证据索引: <baseline / suite / smoke 与逐任务 red-green 的 evidence 文件名>
- 主要变更: <触碰的模块/文件概览>
- 遗留事项: <非阻塞的建议级 findings、范围外推迟项;没有则写"无">
```

### 4. 边界

- 按项目惯例整理提交(commit);**不主动** push 到共享分支、打 tag、发版本、部署——除非用户明确要求。
- 用户提出新需求或范围变化 → 那是新一轮工作流,从 `hf-frame` 重新进入,不在 ship 里夹带实现。

## 红线

- 只凭 gate PASS 就交付,不做逐条语义对照(gate 只看形式完整,不懂语义)
- 交付报告不提遗留事项,把推迟项藏起来
- 在 ship 阶段偷偷修 bug 或加功能(发现问题 → 回上游阶段走流程)
- 替用户做发布/部署决定

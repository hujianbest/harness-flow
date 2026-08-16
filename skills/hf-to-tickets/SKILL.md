---
name: hf-to-tickets
description: 把已评审的规格和架构拆成带阻塞边的垂直切片任务票。HarnessFlow 主链步骤；默认写入 features/<id>/tickets.md。
---

# hf-to-tickets

把计划、规格或架构拆分为**任务票**——采用曳光弹式垂直切片，每张票都声明会**阻塞**它的其他任务票。

## HarnessFlow 桥接

1. 宜在规格与特性架构评审通过后拆票；更新 `progress.md` 为 `to-tickets`。
2. 发布到 `features/<id>/tickets.md`（机器可读的 `- [ ] T-NN` 行）。
3. 首张可执行票应为最薄端到端路径(行走骨架判据),除非架构已声明存量无需。
4. 更新 `progress.md`；下一步进入 `hf-implement`。

## 流程

### 1. 收集上下文

读取 `spec.md`、`architecture.md`、评审记录与 `CONTEXT.md`。

### 2. 探索代码库（可选）

使用领域词汇。寻找预重构机会：先让变更变得容易，再完成这个容易的变更。

### 3. 起草垂直切片

- 每个切片都贯穿各层形成一条狭窄但**完整**的路径——纵向而非横向
- 每个切片都能单独演示或验证；规模应适合在一个全新上下文窗口内完成
- 先做预重构
- 每张任务票都包含**阻塞边**

**大范围重构**采用扩张—收缩批次，而不是强行拆成曳光弹式切片。

### 4. 询问用户

展示标题 / `blocked-by` / 交付内容。反复调整直至获批（`auto`：将粒度选择所依赖的假设记入台账）。

### 5. 发布

**本地 / HF 默认方式**——`tickets.md`：

```markdown
# 任务票

- [ ] T-01 <title> — Blocked by: None — <what it delivers>
- [ ] T-02 <title> — Blocked by: T-01 — <what it delivers>
```

可选择在 `tickets/` 下为每张任务票创建详情文件；清单以 `tickets.md` 中的 `- [ ] T-NN` 行为准。

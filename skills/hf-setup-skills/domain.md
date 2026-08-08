# 领域文档

工程技能探索代码库时应如何使用此仓库的领域文档。

## 探索前读取以下内容

- 仓库根目录下的 **`CONTEXT.md`**，或者
- 如果仓库根目录下存在 **`CONTEXT-MAP.md`**，读取它——它会为每个上下文指向一个 `CONTEXT.md`。读取与主题相关的每一个文件。
- **`docs/adr/`**——读取涉及你即将处理区域的 ADR。在多上下文仓库中，还要检查 `src/<context>/docs/adr/` 中限定于上下文的决策。

如果其中任何文件不存在，**静默继续**。不要指出其缺失；不要建议预先创建。`/domain-modeling` 技能（通过 `/grill-with-docs` 和 `/improve-codebase-architecture` 进入）会在术语或决策真正得到解决时按需创建它们。

## 文件结构

单上下文仓库（大多数仓库）：

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文仓库（根目录存在 `CONTEXT-MAP.md`）：

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← 系统级决策
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← 上下文专属决策
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## 使用术语表中的词汇

当你的输出为领域概念命名时（在议题标题、重构提案、假设或测试名称中），使用 `CONTEXT.md` 中定义的术语。不要偏移到术语表明确避免的同义词。

如果所需概念尚未出现在术语表中，这是一个信号——要么你正在创造项目并不使用的语言（重新考虑），要么确实存在空白（记录下来交给 `/domain-modeling`）。

## 标明 ADR 冲突

如果你的输出与现有 ADR 冲突，请明确指出，而不是静默覆盖：

> _与 ADR-0007（事件溯源订单）冲突——但值得重新讨论，因为……_

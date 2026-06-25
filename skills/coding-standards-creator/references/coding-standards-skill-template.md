# `<language>-coding-standards` 骨架模板

> 配套 `coding-standards-creator`。拷贝后替换尖括号占位；各部分的写法要求见 `coding-standards-skill-contract.md`，通用基线见 `hf-skill-quality-contract.md`。正式产出不得残留占位符与本说明。

````markdown
---
name: <language>-coding-standards
description: 在编写、修改或评审 <语言> 代码（<源文件后缀/测试/构建脚本>）时使用。提供 <主题1>、<主题2>、<主题3> 的具体规则与正反例。只适用于 <语言>；其他语言代码使用对应语言自己的 coding-standards 技能。
---

# <Language> Coding Standards

## 总览

<一两句：这门语言的核心危险（如 C 的内存安全）或核心承诺（如 Rust 的所有权、现代 C++ 的 RAII），本技能的规则都围绕它组织。>

本技能在 `hf-clean-code` 的通用标准之上叠加 <语言> 规则，不能替代通用 clean-code 自检。项目声明了 <团队规范名/标准子集，如 PEP 8、Google Java Style、MISRA> 时以项目为准，本文是未声明时的默认底线。

<若有团队规则覆盖 HarnessFlow 默认：在对应规则处标注"团队约定，覆盖 HarnessFlow 默认 X"。>

## <主题节 1：放该语言事故密度最高的主题>

<规则陈述（可判定）。针对的事故类：<一句话>。>

```<language>
// ❌ <模型真实会写出的违规形态>
<反例代码>

// ✅ <替代写法>
<正例代码>
```

- <同主题的补充规则，可判定、给替代>

## <主题节 2..N：按事故密度排序，4-8 节>

<同上形态。每节至少一组正反例；速查表可以有，但不能只有表。>

## 工具链

- <编译/解释器版本与警告基线，如 `-Wall -Wextra` / `mypy --strict`>
- <linter / 格式化工具与配置来源>
- <静态分析/sanitizer：新增项修复或带理由抑制；"历史就有"不豁免本次触碰的文件>
- <测试框架与运行命令>

## 合理化反驳（可选）

| 话术 | 现实 |
|---|---|
| <该语言常见的偷懒话术> | <反驳与正确动作> |

## 自检清单

- [ ] <每个主题节至少一条可勾选项>
- [ ] 零新增警告；静态分析新增项闭环

## 支撑参考（如有 references/）

| 文件 | 用途 |
|---|---|
| `references/<topic>.md` | <低频细则/团队规则号对照> |
````

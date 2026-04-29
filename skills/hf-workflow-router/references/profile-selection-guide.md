# Workflow Profile 选择指南

当 `hf-workflow-router` 需要决定当前工作应使用哪个 workflow profile 时，使用本指南。

本指南回答 3 个问题：

1. 哪些信号指向哪个 profile。
2. 信号冲突时怎么办。
3. 什么时候必须升级 profile。

## Profile 概览

| Profile | 节点数 | 核心特征 |
|---------|--------|---------|
| **full** | 17 | 从规格开始，经过完整评审链、三处 approval step、质量层和收尾 |
| **standard** | 11 | 跳过规格和设计（前提是已有已批准的），从任务拆分开始，保留任务 approval step 和完整质量层 |
| **lightweight** | 7 | 跳过规格、设计和中间质量评审链，但仍保留最小任务计划、任务评审、任务 approval step、实现、回归、完成和收尾 |

说明：

- 这里的节点数按 `hf-workflow-router` 主文件中的 canonical route map 统计。
- `lightweight` 不是“直接实现”，而是保留一条最小可审计主链：`hf-tasks` → `hf-tasks-review` → `任务真人确认` → `hf-test-driven-dev` → `hf-regression-gate` → `hf-completion-gate` → `hf-finalize`。
- `Execution Mode` 不属于 profile 选择的一部分；`interactive` / `auto` 只改变 approval step 的处理方式，不改变这里的节点链路。

## 选择信号矩阵

### 指向 full 的信号

| 信号 | 说明 |
|------|------|
| 无已批准规格 | 没有规格或规格仍为草稿 / 未通过评审 / 未完成 approval step |
| 无已批准设计 | 没有设计或设计仍为草稿 / 未通过评审 / 未完成 approval step |
| 用户明确要求"从头开始" | 用户说"重新做""从零开始""重新梳理需求" |
| 涉及架构变更 | 新增模块、修改核心数据模型、改变模块间接口 |
| 涉及跨模块重构 | 改动影响 3 个以上模块或包 |
| 项目声明的高风险模块 | 项目声明的`强制 full 规则`命中的模块或领域 |
| 涉及数据迁移 | 改动包含数据库 schema 变更或数据迁移脚本 |

### 指向 standard 的信号

| 信号 | 前提条件 |
|------|---------|
| 已有已批准规格+设计，但需新增任务 | 规格和设计的批准证据完整 |
| 中等复杂度 bugfix | 改动涉及多文件但不改变接口；非项目声明的高风险模块 |
| 已有设计内的功能扩展 | 新功能完全在已批准设计的架构范围内 |
| 非高风险的已有 API 扩展 | 新增 endpoint / 方法，但不改变已有接口契约 |

### 指向 lightweight 的信号

| 信号 | 前提条件 |
|------|---------|
| 纯文档变更 | 仅修改 `.md`、`README`、`CHANGELOG`、注释等 |
| 纯配置变更 | 修改配置文件且不影响运行时行为 |
| 纯样式调整 | 仅修改 CSS / 样式文件，不改变组件逻辑 |
| 低风险 bugfix | 单文件改动、无接口变化、非项目声明的高风险模块 |
| 改动行数 ≤ 30 且无功能行为变化 | 代码改动规模小且不引入新行为 |
| 项目约定明确允许 lightweight 的场景 | 项目声明的`允许 lightweight 的条件`命中 |

### 禁止 lightweight 的信号

即使改动看似简单，以下情况不允许使用 lightweight：

- 项目声明的`禁止 lightweight 的条件`命中
- 改动涉及测试基础设施（测试框架配置、fixture、mock 基础类等）
- 改动涉及 CI/CD 配置
- 改动涉及安全相关配置（认证、授权、加密、密钥等）
- 改动虽然是单文件，但该文件是高风险模块的核心文件

## 信号冲突处理

当同一请求同时命中不同 profile 的信号时：

1. **选择更重的 profile**（保守原则）：full > standard > lightweight
2. 在路由输出中说明冲突点和最终选择依据

示例：

- 用户说"就改一行配置"，但该配置文件在项目声明的高风险模块清单中 → **full**
- 已有规格+设计，用户要扩展一个功能，但涉及新增数据表 → **full**（数据模型变更信号优先）
- 已有规格+设计，用户要扩展一个已有 API 的返回字段 → **standard**

## Profile 升级

### 升级触发条件

| 条件 | 升级方向 |
|------|---------|
| lightweight 实现时发现需要拆多个任务 | lightweight → standard |
| lightweight 实现时发现缺少规格或设计依据 | lightweight → full |
| standard 任务拆分时发现需要重新做设计 | standard → full |
| 任意 review / gate 返回 `阻塞`，原因指向上游工件缺失 | 当前 → 包含缺失工件的更重 profile |
| 改动范围从单文件扩散到多模块 | lightweight → standard 或 full |

### 升级流程

1. 在 feature `progress.md`（默认 `features/<active>/progress.md`）中更新 Workflow Profile 字段
2. 在 Session Log 中记录升级原因
3. 回到本 skill（`hf-workflow-router`）重新路由
4. 按新 profile 的节点链路进入正确阶段

### 降级规则

**不允许降级。**

一旦选定或升级到某个 profile，只能保持或继续升级，不能回退到更轻的 profile。

## 示例场景

### 场景 1：新功能开发

```text
用户请求："给系统加一个导出 CSV 的功能"
信号：无已批准规格 + 新功能
Profile：full
```

### 场景 2：已有功能的扩展

```text
用户请求："在已有的导出功能里加一个日期筛选参数"
信号：已有已批准规格+设计 + 已有设计内的功能扩展
Profile：standard
```

### 场景 3：低风险修复

```text
用户请求："默认排序从 ASC 改成 DESC"
信号：单文件改动 + 无接口变化 + 改动行数 ≤ 30
Profile：lightweight
```

### 场景 4：看似简单实则复杂

```text
用户请求："就改一下日志格式"
信号：改动行数 ≤ 30（指向 lightweight）
但是：日志模块在项目声明的高风险模块清单中（指向 full）
冲突处理：选择更重的 profile
Profile：full
```

### 场景 5：执行中升级

```text
初始判断：lightweight（修复一个 CSS 样式问题）
执行中发现：修复需要修改组件逻辑，且涉及 3 个组件文件
升级：lightweight → standard
后续：回到 hf-workflow-router 重新路由，从 hf-tasks 开始
```

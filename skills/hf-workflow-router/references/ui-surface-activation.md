# UI Surface 激活条件指南

当 `hf-workflow-router` 判断 **当前进入 design stage**（主链从 `规格真人确认` 完成后进入 `hf-design` / `hf-ui-design` 的那一步）时，使用本指南决定是否激活 `hf-ui-design` 这个 **conditional peer skill**。

本指南回答 3 个问题：

1. 哪些证据指向激活 `hf-ui-design`。
2. 证据冲突或含糊时怎么办。
3. parallel / architecture-first / ui-first 三种执行模式如何选择。

## 为什么是 conditional peer，不是 side-line

- `hf-hotfix` / `hf-increment` 是 **side-line**：跳出主链处理例外情况后 canonical re-entry
- `hf-ui-design` 是 **conditional peer within design stage**：主链内部的条件并行节点，不 bypass；任何含 UI surface 的任务都必须穿过它
- 激活条件不成立时，design stage 只走单节点 `hf-design`，与现状完全一致；不引入任何额外成本

## 激活信号矩阵

### 指向 "激活 hf-ui-design" 的信号

| 证据来源 | 信号 |
|---|---|
| 规格文件 | 显式声明 `UI surface`、`前端`、`界面`、`页面`、`组件`、`交互设计`、`UX`、`可访问性 / WCAG`、`响应式`、`视觉 / 品牌` 等 surface 条目 |
| 规格文件 | 关键验收标准涉及用户可见行为（如"用户在首页看到 X"、"表单校验反馈"、"空状态引导"） |
| 规格文件 | 非功能需求含可用性 / a11y / i18n / 响应式 / 前端性能预算（LCP/INP/CLS） |
| 项目级约定 | 声明项目含前端代码库、Design System 路径、frontend principles / brand 锚点 |
| 任务请求 | 用户请求包含 "页面 / 组件 / UI / UX / 前端 / 界面 / 视觉 / 交互 / 可访问性 / 响应式 / 国际化" 等关键词 |
| 任务请求 | 用户明确要求"先画 UI"、"做个原型"、"把界面想清楚" |

命中任一 → 激活 `hf-ui-design`。

### 指向 "不激活" 的信号

| 信号 | 说明 |
|---|---|
| 规格明确为 API-only / 脚本 / CLI / 数据管道 / 后端服务 | 无 UI surface |
| 规格无用户可见界面的验收标准 | 无 UI surface |
| 项目约定声明项目无前端 | 无 UI surface |
| 任务为纯基础设施 / DevOps / 配置 | 无 UI surface |

全部命中（或明确无 UI surface 证据）→ design stage 只走 `hf-design` 单节点，不激活本 peer。

## 证据冲突处理

### 规格未声明但请求含 UI 关键词

- **处置**：视为规格不完整，回到 `hf-specify` 补齐 UI surface 声明，再重新判断
- **不允许**：以"反正要有界面"为由激活 `hf-ui-design`；这会导致下游无可追溯规格

### 规格声明但请求为纯后端修改

- **处置**：若当前 iteration 明确不触碰 UI（如仅修改 API 返回值不改前端展示），激活判定范围收敛到当前 iteration；`hf-ui-design` 可不激活
- **边界**：若 API 返回值变化会影响前端 error / empty / partial 等状态矩阵，则应激活 `hf-ui-design` 并更新状态矩阵

### 项目级声明与规格不一致

- 优先项目级声明（作为项目级真相来源），在路由输出中说明冲突，并建议回 `hf-specify` 修正规格

## 执行模式选择（parallel / architecture-first / ui-first）

激活后，router 需要决定 `hf-design` 与 `hf-ui-design` 的起草顺序。这是 `hf-workflow-router` 的路由决策，不由下游 skill 自选。

### 默认：parallel

两条 skill 并行起稿。期间各自读取对方最新草稿，互相标记"待 peer 锁定"条目；各自 review 前收敛 peer 交接块。

**适用**：绝大多数含 UI surface 的任务。

### architecture-first

`hf-design` 先定到 review-ready（不必通过 review，仅需稳定草稿），`hf-ui-design` 再起稿。

**适用信号**：

- 规格明确"后端先行，前端适配"
- 核心交付物是 API / 数据契约，UI 是其消费层
- 后端架构决策（如事件驱动 vs 请求响应）会根本影响前端形态

### ui-first

`hf-ui-design` 先锁 IA / 交互 / 状态矩阵，`hf-design` 基于此定 API 契约与数据模型。

**适用信号**：

- 规格明确"以用户体验驱动"（如重设计、营销页、数据可视化）
- 核心交付物是界面体验，后端需要按 UI 需求整形数据
- 规格含强可用性 / 性能预算要求，倒逼后端选择

### 执行模式在 feature `progress.md` 的登记

```markdown
- Current Stage: hf-design | hf-ui-design
- Design Execution Mode: parallel | architecture-first | ui-first
```

注：`Design Execution Mode` 与 `Execution Mode`（`interactive` / `auto`）正交，不混写。

## 激活后对主链节点集合的影响

### full profile

含 UI surface 时的节点序列：

```text
hf-specify -> hf-spec-review -> 规格真人确认
-> {hf-design || hf-ui-design}           # 按 Design Execution Mode 并行或排序
-> {hf-design-review || hf-ui-review}    # 各自独立 review
-> 设计真人确认                            # 两者均通过后父会话汇总
-> hf-tasks -> ...
```

不含 UI surface 时保持现状单路径。

### standard / lightweight profile

`hf-ui-design` **不加入** standard / lightweight 的合法节点集合。理由：这两个 profile 前提是"已有已批准设计"，若 UI 设计已随上一轮 full profile 完成并批准，standard/lightweight 直接沿用即可；如果新 iteration 要动 UI 设计，应升级到 full profile。

## 联合 design approval 规则

两条 review 的汇总判断由父会话 / router 负责：

| hf-design-review | hf-ui-review | 下一步 |
|---|---|---|
| 通过 | 通过 | 父会话发起 `设计真人确认`（联合 approval） |
| 通过 | 需修改 | `hf-ui-design` 修订；`hf-design` 结论暂存，不单独触发 approval |
| 需修改 | 通过 | `hf-design` 修订；`hf-ui-design` 结论暂存 |
| 需修改 | 需修改 | 两条 skill 各自修订；修订完成后重新 review |
| 阻塞（reroute） | 任意 | router 重新判断，另一条的进度保留 |
| 任意 | 阻塞（reroute） | router 重新判断，另一条的进度保留 |

reviewer subagent 不代替父会话做联合判断；各自只返回自己的 verdict。

## 回流与支线交互

### `hf-increment` 回流

需求变更可能同时影响 `hf-design` 与 `hf-ui-design`。`hf-increment` 判失效时：

- 若变更影响 UI surface（新增页面 / 改交互 / 改 UX NFR）→ `hf-ui-design` 也需重判
- canonical re-entry 目标从单点变为双点：router 按 `parallel` / `architecture-first` / `ui-first` 重新选择执行模式

### `hf-hotfix` 回流

紧急缺陷若含 UI 层（a11y 阻断、严重视觉故障、关键状态错误）：

- `hf-hotfix` 分析后 handoff 给 `hf-ui-design` 做受控修订
- 修订幅度若达标，可走 lightweight profile 跳过完整 UI 设计流程（由 router 判断）

## 示例场景

### 场景 1：新前端页面

```text
规格：新增"订单详情页"，含 loading/空/错误态，支持中英文，移动端适配
信号：UI surface + 响应式 + i18n
决策：激活 hf-ui-design，Design Execution Mode=parallel
```

### 场景 2：纯 API 扩展

```text
规格：在已有 /orders API 加一个 cursor 分页参数
信号：API-only，无 UI surface
决策：不激活 hf-ui-design，只走 hf-design
```

### 场景 3：规格含糊

```text
规格：优化订单查询性能
用户请求："顺便把前端列表刷新一下"
冲突：规格未声明 UI surface，但请求含 UI 关键词
决策：回 hf-specify 补齐 UI surface 声明，再重判
```

### 场景 4：UX 驱动的重设计

```text
规格：重设计用户首页，以提升转化率；含新导航、新信息架构
信号：强 UX 驱动 + IA 变化
决策：激活 hf-ui-design，Design Execution Mode=ui-first
```

### 场景 5：a11y hotfix

```text
线上问题：商品详情页键盘无法触达购买按钮（WCAG 违规）
信号：hotfix + a11y 阻断 + 含 UI 层
决策：hf-hotfix 分析后 handoff 给 hf-ui-design 做受控修订，profile 视影响面由 router 判断
```

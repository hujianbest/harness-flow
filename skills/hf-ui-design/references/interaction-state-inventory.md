# 交互状态清单（Interaction State Inventory）

只设计 happy path 是 UI 设计最常见的缺陷。本清单给出状态枚举和应用规则。

## 状态枚举

### 基础交互态（控件级）

| 状态 | 含义 | 典型表现 |
|---|---|---|
| `idle` | 默认静止 | 常态样式 |
| `hover` | 光标悬停（指针设备） | 提示可交互 |
| `focus` | 获得焦点（键盘 / 点击） | 可见 focus ring，WCAG 硬要求 |
| `active` / `pressed` | 按下中 / 交互进行中 | 视觉反馈 |
| `disabled` | 不可交互 | 灰度 + `aria-disabled` / `disabled`，保留语义 |
| `loading` / `pending` | 操作进行中 | 禁止重复触发，进度提示 |
| `read-only` | 只读 | 与 disabled 不同，仍可聚焦、不可编辑 |

### 数据态（视图级）

| 状态 | 含义 | 典型表现 |
|---|---|---|
| `loading` | 数据加载中 | 骨架屏 / spinner / 渐进渲染 |
| `empty` | 无数据（首次 / 清空后） | 空状态插图 + 引导主操作 |
| `error` | 加载/提交失败 | 明确原因 + 重试入口 |
| `partial` | 部分加载成功 | 已加载部分可见 + 失败部分可重试 |
| `offline` | 离线 | 标明离线、说明哪些操作仍可用 |
| `stale` | 数据过期 | 标明过期，提供刷新 |
| `success` | 成功反馈 | 短暂反馈 + 继续路径 |

### 权限/鉴权态

| 状态 | 含义 |
|---|---|
| `unauthenticated` | 未登录 |
| `forbidden` | 已登录但无权限（403） |
| `session-expired` | 会话过期（需重新登录） |
| `rate-limited` | 触发限流（429） |

### 表单/输入态

| 状态 | 含义 |
|---|---|
| `pristine` | 未交互过 |
| `dirty` | 已修改未提交 |
| `validating` | 异步校验中 |
| `invalid` | 校验不通过 |
| `submitting` | 提交中 |
| `submitted-success` / `submitted-error` | 提交结果 |

## 应用规则

- **关键交互必须覆盖**：至少 `loading / empty / error` 三态；表单额外覆盖 `invalid / submitting / submitted-error`
- **高风险交互必须覆盖完整矩阵**：支付、权限变更、数据删除、批量操作、长任务等
- **所有可交互控件必须声明 `focus` 态**：WCAG 2.2 AA 硬要求；不得通过 `outline: none` 消除且不替代
- **disabled 不代表隐藏**：保留可读语义（颜色对比仍应 ≥ 3:1 或显式声明不达标理由）
- **loading 不等于无动效**：即便选择无动效路径，也需声明"以 `prefers-reduced-motion` 或骨架屏替代"

## 状态矩阵示例

### 示例 1：搜索结果列表

| 状态 | UI 表现 | 后端条件 |
|---|---|---|
| loading | 骨架屏 6 行 | 请求发起中 |
| empty（无关键词） | 引导文案 + 热门搜索 | 参数缺失 |
| empty（有关键词无结果） | "未找到匹配" + 清除筛选建议 | 结果为空 |
| partial | 已加载 N 条 + "加载更多失败，重试" | 分页失败 |
| error | 错误 banner + 重试按钮 | 请求失败 |
| offline | 离线提示 + 显示缓存结果（如有） | 网络不可用 |

### 示例 2：提交表单

| 状态 | UI 表现 |
|---|---|
| pristine | 默认 |
| validating（异步） | 输入框尾部 spinner |
| invalid（本地） | 红色边框 + inline 错误文案（与输入框关联 `aria-describedby`） |
| submitting | 按钮 loading + 表单整体禁用（不禁用 cancel） |
| submitted-success | toast 成功 + 跳转或清空 |
| submitted-error | 顶部 alert + 错误原因 + 可恢复输入 |

## 红线

- 只画 idle / success，漏 loading / empty / error → 不合格
- loading 态放置在与原内容不相等的尺寸上，导致布局抖动（CLS）→ 不合格
- error 态只说"出错了"，不给原因与下一步 → 不合格
- empty 态只留白屏，不给下一步 → 不合格
- disabled 态用纯色无对比度降级（违反 3:1 规则）但未声明理由 → 不合格

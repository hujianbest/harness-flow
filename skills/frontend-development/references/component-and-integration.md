# 组件架构、前后端集成与浏览器黑盒冒烟详表

> `frontend-development` 的 **组件架构与边界 / 前后端集成与 API 客户端层 / UI 测试与运行时证据** 维度深表。SKILL.md 承载红线，本文承载可直接套用的组织方式、映射表与可复制骨架。

## 组件分层与职责

| 类型 | 职责 | 不该做 |
|---|---|---|
| 展示型（presentational） | 接收 props、渲染 UI、向上回调事件 | 取数、业务规则、全局状态读写 |
| 容器/数据型 | 取数、组合 hook、把数据喂给展示型 | 堆砌大量样式与布局细节 |
| 自定义 hook | 取数、四态、派生值、订阅与清理 | 渲染 JSX |
| 纯函数/lib | 业务计算、格式化、校验规则 | 触碰 DOM、依赖框架运行时 |

把"会变的"（数据、业务）与"稳定的"（展示）分开，使展示型可复用、纯函数与 hook 可独立单测。

## 组合优于透传

- 深层 `props` 透传（祖先把数据一路传到很深的后代）会让中间组件被迫知道无关 props，重构脆弱。
- 用 **组合**（把子树作为 `children`/插槽传入）或 **context**（真正跨多层共享的少量值，如主题、当前用户）替代。
- context 不是全局状态桶：高频变化的大状态放进 context 会引发大范围重渲染；用就近状态 + 选择器或专门的状态库。

```tsx
// ❌ 透传：Layout 不关心 user 却被迫中转
<Layout user={user}><Sidebar user={user} /></Layout>

// ✅ 组合：父决定内容，Layout 只负责布局
<Layout sidebar={<Sidebar user={user} />} />
```

## 状态就近（colocation）

- 状态放在"用到它的最小子树"里，不要无脑提升到顶层。
- 只有多个兄弟需要共享时才上提到最近公共祖先；跨远端共享才考虑 context/状态库。
- 服务器数据（来自后端的缓存）用数据获取库（React Query 等）管理，不要塞进通用全局状态——它有自己的失效/重试/竞态语义（见四态维度）。

## 服务端/客户端边界（SSR 框架）

- 默认服务端渲染；只有需要交互（事件、浏览器 API、`useState`/`useEffect`）的最小子树标 `"use client"`。
- 把 client 边界下沉到叶子：例如整页服务端渲染，只有"点赞按钮"是 client 组件。整页 `"use client"` 会丢失 SSR 收益并把不必要代码送进 bundle。
- 不在 client 组件里嵌入只该在服务端用的密钥/逻辑（见客户端安全维度）。

## API 客户端层

集中一层，组件只调用语义化方法，不直接 `fetch`：

```ts
// lib/api.ts —— 单一出入口
const BASE = import.meta.env.VITE_API_URL;          // 基址来自环境变量

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...authHeader(), ...init.headers },
  });
  if (!res.ok) throw await toApiError(res);          // 统一抛 ApiError（含 status/code）
  return res.status === 204 ? (undefined as T) : res.json();
}

export const api = {
  get:  <T>(p: string) => request<T>(p),
  post: <T>(p: string, body: unknown) => request<T>(p, { method: 'POST', body: JSON.stringify(body) }),
  // put / patch / delete ...
};
```

要点：

- **基址**走环境变量，不硬编码 IP/域名。
- **鉴权令牌**集中注入（`authHeader()`/拦截器），不在每个调用手拼。
- **错误归一**：失败统一抛带 `status`/`code` 的 `ApiError`，组件层只处理已归一的错误。
- 令牌优先放内存 + httpOnly 刷新 cookie，避免放 `localStorage`（XSS 可读，见客户端安全维度）。

## 错误码 → 用户文案映射

不要把后端原始 message/堆栈丢给用户；集中映射：

| 状态 | 用户文案（示例） | 处理 |
|---|---|---|
| 401 | 请重新登录 | 先尝试刷新令牌，失败则跳登录 |
| 403 | 你没有执行此操作的权限 | 不重试 |
| 404 | 没有找到对应内容 | 不重试 |
| 409 | 与现有数据冲突，请刷新后重试 | 不重试 |
| 422 | 展示字段级校验错误（贴到对应输入旁） | 不重试 |
| 429 | 操作太频繁，请稍后再试 | 按 `Retry-After` |
| 5xx | 服务暂时不可用，请稍后再试 | 退避重试（上限内） |
| 网络/超时 | 网络异常，请检查连接 | 可重试/提示离线 |

- **只对 5xx/网络错误重试，4xx 不重试**（客户端错误重试也错）。
- 422 的字段错误要落到对应表单字段旁，并用 `aria` 关联（见 a11y 维度）。

## 跨边界类型一致性

手抄两份类型必然漂移。按场景选一种单一来源：

| 场景 | 方案 | 类型安全 |
|---|---|---|
| 同团队、两端都 TypeScript | tRPC | 端到端自动，无 codegen |
| 不同语言 / 多消费者 / 公共 API | OpenAPI → 生成客户端 | codegen 保证 |
| GraphQL | GraphQL Code Generator | codegen 保证 |
| 简单内部应用 | 共享类型包 + 契约测试兜底 | 手写 + 测试保证 |

服务端侧契约纪律由适用的 API/服务端领域技能覆盖。

## 浏览器黑盒冒烟骨架

触碰前端运行面的工作项，关键用户流要有浏览器层运行时证据：把应用当黑盒跑，断言真实 DOM 行为。下面是一个可复制到项目侧、不绑定具体框架的最小 Playwright 冒烟骨架（仅作参考；HarnessFlow 本体不依赖 Playwright，项目可用任何等价工具）。

设计意图（与"UI 测试与运行时证据"红线一一对应）：

- **先起服务再访问**：脚本不假设服务在跑，按项目 README/启动约定（如 `npm run dev` + 默认端口）启动，或读 `SMOKE_BASE_URL` 环境变量。
- **黑盒驱动**：通过真实 UI 入口（导航/按钮/表单）驱动，不 import 内部模块、不操作 store。
- **networkidle 等待异步**：用 `waitForLoadState('networkidle')`（或等价的"网络静默"）代替固定 `sleep`。
- **断言真实 DOM**：用可访问性角色（role/label）查询，断言用户能看到的内容，不断言内部状态。
- **三层观察**：收集 console error、未预期 4xx/5xx、白屏，作为 observation 记录，不忽略。

```js
// smoke.cjs —— 复制到项目并按需改路由/选择器。node smoke.cjs 运行。
// 前置：按 README 启动 dev server（或设置 SMOKE_BASE_URL 指向已起的服务）。
const { chromium } = require('playwright');

const baseUrl = process.env.SMOKE_BASE_URL || 'http://localhost:5173';
const apiHost = process.env.SMOKE_API_HOST || 'localhost:8080';
const routes = (process.env.SMOKE_ROUTES || '/,/login,/articles').split(',');
const observations = [];
const observe = (severity, layer, scenario, message, detail = '') =>
  observations.push({ severity, layer, scenario, message, detail });

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  // 三层观察器：console / pageerror / 网络 —— 不忽略任何异常
  let scenario = 'startup';
  page.on('console', (m) => { if (m.type() === 'error') observe('major', 'console', scenario, 'console error', m.text()); });
  page.on('pageerror', (e) => observe('blocking', 'console', scenario, 'uncaught page error', e.message));
  page.on('requestfailed', (r) => observe('major', 'network', scenario, 'request failed',
    `${r.method()} ${r.url()} ${r.failure()?.errorText || ''}`));
  page.on('response', (r) => {
    if (r.url().includes('/api/') && !r.url().includes(apiHost))
      observe('major', 'network', scenario, 'api request used unexpected host', r.url());
    if (r.status() >= 400) observe('major', 'network', scenario, `http ${r.status()}`, r.url());
  });

  for (const route of routes) {
    scenario = `route ${route}`;
    await page.goto(`${baseUrl}${route}`, { waitUntil: 'domcontentloaded' });
    await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});  // 等异步静默，不用固定 sleep

    // 断言真实 DOM：用户能看到的内容（用可访问性角色，不用 className）
    const bodyText = await page.locator('body').innerText().catch(() => '');
    if (!bodyText.trim()) observe('blocking', 'dom', scenario, 'empty body / possible white screen');
    // 例：用 getByRole/getByLabel 断言关键控件存在，而非断言内部 store
    // const heading = page.getByRole('heading', { name: 'Orders' });
    // await expect(heading).toBeVisible();
  }

  await browser.close();
  console.log(JSON.stringify({ observations }, null, 2));
  if (observations.some((o) => o.severity === 'blocking' || o.severity === 'major')) process.exitCode = 1;
})();
```

用法约定：

- 脚本独立可跑（`node smoke.cjs`），项目 README 或 `--help` 应说明如何启动被测服务。
- `SMOKE_BASE_URL` / `SMOKE_API_HOST` / `SMOKE_ROUTES` 走环境变量，不硬编码。
- 这只产 observation（现象 + 严重度初判），不签发 pass/fail 终态——终态由 `hf-review` 在评审时结合证据判定。
- 这是冒烟层（关键路径是否跑通、有没有白屏/console error/未预期 4xx/5xx），不替代组件单测与交互测试。

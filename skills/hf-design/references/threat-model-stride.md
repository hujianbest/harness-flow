# 轻量 STRIDE Threat List 参考

## Purpose

本参考为 `hf-design` 在 Phase 0 引入**最小可交付**的威胁建模能力：用 Microsoft **STRIDE** 作为分类法，以**列表形式**给出每条关键组件 / 数据流 / 信任边界的威胁 + 缓解映射。

Phase 0 只落**轻量 STRIDE list**，不引入完整独立节点。Phase 2 起才会抽出独立 `hf-threat-model` skill（在 gap analysis 候选块 2 中已规划）。

## One-Line Rule

每条关键数据流 / 信任边界都必须**至少被 STRIDE 六字母过一遍**，并显式记录"不适用"或"缓解方式"。

## STRIDE 六字母

| 字母 | 含义 | 核心问题 |
|---|---|---|
| **S** Spoofing | 身份冒充 | 谁声称是谁？如何验证？ |
| **T** Tampering | 篡改 | 数据在传输 / 存储中能被改吗？ |
| **R** Repudiation | 抵赖 | 能证明某人做了某事吗？ |
| **I** Information Disclosure | 信息泄露 | 机密数据会暴露给不该看的人吗？ |
| **D** Denial of Service | 拒绝服务 | 攻击者能让系统不可用吗？ |
| **E** Elevation of Privilege | 权限提升 | 用户能获得超出其授权的能力吗？ |

## 触发条件

以下场景在 design 阶段**必须**包含 STRIDE list：

- spec 中存在 Security 类 NFR
- 设计涉及用户认证 / 授权
- 存在跨信任边界的数据流（用户 ↔ 后端 / 内部 ↔ 外部）
- 处理个人数据、敏感配置、凭证
- 有审计 / 合规要求（即使是轻量级的）

若以上条件均不触发（例如纯内部 CLI 脚本、无用户数据），允许在 design 文档中显式标注"本轮无关键信任边界，跳过 STRIDE"。

## 最小结构

| 资产 / 数据流 / 信任边界 | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| 例：用户 → API 网关 | 威胁: ... 缓解: ... | 不适用 | 威胁: ... 缓解: ... | ... | ... | ... |

每个格子至少写：

- 若威胁存在：`威胁: <一句话> 缓解: <落到哪个模块 / 机制>`
- 若不适用：`不适用: <一句话解释>`
- 不允许留空

## 最小示例

```markdown
## Threat Model (STRIDE, Phase 0 轻量版)

| 资产 / 数据流 | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| 用户 → API 网关 | 威胁: 伪造会话 缓解: 短期 JWT + 刷新机制 | 威胁: 请求参数篡改 缓解: HTTPS + 签名 | 威胁: 用户否认操作 缓解: 审计日志 NFR-010 | 威胁: token 泄露 缓解: 最小 scope + 短 TTL | 威胁: 登录接口刷爆 缓解: 限流 + 验证码 | 威胁: 未授权访问管理接口 缓解: RBAC 矩阵 ADR-004 |
| 内部模块 ↔ 数据库 | 不适用: 内网单服务单库 | 威胁: SQL 注入 缓解: ORM + 参数化 | 不适用 | 威胁: 拖库 缓解: 静态加密 + 访问审计 | 威胁: 连接耗尽 缓解: 连接池上限 + 熔断 | 威胁: 提权查询 缓解: 业务账号权限最小化 |
```

## 与 NFR / ADR 的衔接

- 每条威胁的"缓解"应落到 design 中具体模块 / 机制，并且能回指 spec 的 Security NFR 或 ADR
- 若某条威胁的缓解需要**关键决策**（例如选择 JWT 还是 session cookie），应当用 ADR 单独记录
- Response Measure（QAS）中若有安全阈值（例如审计日志 100% 落盘），要在 STRIDE 的"缓解"格里显式回指该 NFR

## 常见 Red Flag

- STRIDE 只填了两三个字母，其余留空
- "缓解"写成"会考虑安全"这类无落地口号
- 缓解没指向具体模块 / 机制
- 信任边界识别错误（把内部模块间通信当作外部）
- 威胁写得像攻击教程，却没写缓解
- STRIDE list 和 Security NFR 互相矛盾

## 升级路径（Phase 2 预告）

Phase 2 起将抽出独立 `hf-threat-model` skill，采用更完整的 STRIDE + LINDDUN (隐私威胁)，并把威胁建模结果作为 `hf-security-gate` 的输入。本参考是 Phase 0 轻量版，产出可被 Phase 2 复用。

## 何时跳过

- 纯离线 CLI / 脚本，无任何外部输入且不处理敏感数据
- 纯文档 / 元数据变更，无代码路径
- 纯构建工具 / DX 辅助

跳过时必须在 design 中**显式写明跳过理由**，不允许沉默省略。

## 衔接

- NFR Security 承接见 `nfr-checklist.md`
- 关键决策仍走 ADR（见 `adr-template.md`）
- 失败模式分析见 `failure-modes.md`

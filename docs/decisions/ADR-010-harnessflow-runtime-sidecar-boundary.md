# ADR-010 — HarnessFlow Runtime Sidecar Boundary（D1 + D2 落地）

- 状态: accepted（2026-05-13，架构师本会话拍板 D1 = A 做 runtime + D2 = B 形态为 OpenCode plugin）
- 日期: 2026-05-13
- Feature: 待开 `features/003-harnessflow-runtime/`（v0.7 release 前另起 feature）
- 决策者: 架构师（user）拍板 D1 + D2；cursor cloud agent 落 ADR
- 关联 ADR:
  - ADR-008（同会话）—— 路线图 v0.7 主题"可选 runtime sidecar"
  - ADR-009（同会话）—— fast lane 治理；runtime 是 fast lane 的运行时支撑（不是依赖）
  - ADR-006 D1（HF skill anatomy v2）—— `skills/<name>/scripts/` 子目录约定
  - ADR-005 D7 / ADR-004 D2（"P-Honest, narrow but hard"）—— runtime 同样不假装做 v0.8 删除范围

## 1. Context

架构师 D1 = A：v0.7 做可选 runtime sidecar 把"OMO 验证过、host 客户端没法可靠做"的几件事落地。
架构师 D2 = B：runtime 形态 = OpenCode plugin（参照 OMO 写 TypeScript/Bun），**不**走"单一 MCP server 三客户端通吃"。

OMO 已实测最大单点收益：hashline-edit 把 Grok Code Fast 1 在工具调用类任务上的成功率从 6.7% 提升到 68.3%（来源：OMO README + `src/tools/hashline-edit/AGENTS.md` 24 文件实现 + `the-harness-problem` 引文）。这是 host 原生 edit 工具无法在 markdown skill 层规约掉的——必须接管编辑工具本身。

本 ADR 锁定 v0.7 runtime 的范围、形态、与 markdown 包的边界，避免后续 v0.7 实现阶段把 HF 推成"再造一个 OMO"而失去三客户端可移植性的 moat。

## 2. Decision

### D1：runtime 形态 = OpenCode plugin（TypeScript/Bun，参照 OMO 仓库结构）

**决策**：`harnessflow-runtime` 作为 OpenCode plugin 实现，npm 包名 `harnessflow-runtime`（不与 `oh-my-opencode` / `oh-my-openagent` 冲突），bin 名 `hf-runtime`。

**仓库布局**（参照 OMO `src/` 结构精简版）：

```
harnessflow-runtime/
├── src/
│   ├── index.ts                  # OpenCode plugin entry：default export pluginModule = { id, server }
│   ├── plugin-config.ts          # 配置 JSONC + Zod；与 HF markdown 包配置语义对齐
│   ├── tools/
│   │   ├── hashline-edit/        # 直接 fork OMO src/tools/hashline-edit/ 的 24 文件实现并维护
│   │   ├── hashline-read/        # 接管 Read，输出 LINE#ID 标注
│   │   ├── record-evidence/      # 写 features/<f>/verification/ 的结构化 evidence
│   │   ├── progress-store/       # 原子读写 features/<f>/progress.json + tasks.progress.json
│   │   └── parallel-explore/     # D5 = A：并行探查工具，结果收敛回工件
│   ├── hooks/
│   │   ├── todo-continuation-enforcer/   # 对应 OMO 同名 hook
│   │   ├── ralph-loop/                   # 对应 OMO 同名 hook
│   │   ├── context-window-recovery/      # 对应 OMO anthropic-context-window-limit-recovery
│   │   ├── session-recovery/             # 对应 OMO 同名 hook
│   │   ├── compaction-context-injector/  # 对应 OMO 同名 hook（v0.6 wisdom-notebook 摘要注入）
│   │   ├── wisdom-notebook-injector/     # router handoff 前注入 notebook 摘要
│   │   └── intent-gate/                  # 识别 HF 关键词（auto mode / ultrawork / hf-* slash 命令）
│   ├── cli/
│   │   ├── doctor/               # hf-runtime doctor：4 类自检（System / Config / Skills / Workflow Artifacts）
│   │   └── verify-skill-anatomy/ # 等价 scripts/audit-skill-anatomy.py，但作为 runtime CLI 提供
│   └── shared/
├── packages/                     # 平台 binary（参照 OMO 11 平台包：darwin/linux/windows × arm/x64 × baseline）
└── docs/
```

**理由**：
- OpenCode plugin API 已经验证可承载所有需求（OMO 1304 文件就是证明）
- 直接 fork OMO 的 `hashline-edit` 24 文件实现而不是从零写，节省最大单点工作量；fork 时同步保留对上游 OMO 的 attribution
- TypeScript/Bun 与 OMO 同栈，方便后续从 OMO 上游同步 bug fix / 优化
- `harnessflow-runtime` 与 OMO 不竞争——OMO 是"all-batteries"，harnessflow-runtime 只补 HF workflow 必需的几件事，安装它的用户也可以同时安装 OMO（只要 OMO 不开冲突的 hook）

**Alternatives considered**：
- A1：MCP server 三客户端通吃 —— 架构师 D2 = B 已拒绝；技术原因见 ADR-008 D3
- A2：直接给 OMO 提 PR 把 HF 关心的能力合并 —— 拒绝：OMO 是"oh-my-*"风格的 batteries-included 插件，HF 风格更窄更硬，治理诉求不一致；分包独立维护更清晰
- A3：Rust 重写以追求更小 binary —— 拒绝：v0.7 阶段不引入新语言栈，TypeScript/Bun 与 OMO 同栈的复用价值大于 binary size 收益

**Reversibility**：低（一旦 v0.7 release 出去，npm 包名 + bin 名锁定）。

### D2：v0.7 runtime 范围 = 7 类 P0 + P1 模块（不做 OMO 团队模式 / 多 worktree / 商用末段）

**P0（v0.7 必做）**：

| 模块 | 对应 OMO | HF 中的责任 |
|---|---|---|
| `hashline-read` + `hashline-edit` | OMO `src/tools/hashline-edit/` 24 文件 + `hashline-read-enhancer` hook | 接管 Read 与 edit；HF `hf-test-driven-dev` SKILL.md 检测到 runtime 时**强制**用 hash 校验编辑 |
| `record-evidence` | 类比 OMO `tool-metadata-store` + `boulder-state` | MCP-style 工具：`record_evidence(node, kind, payload)` → 写 `features/<f>/verification/`，schema 受 Zod 校验 |
| `progress-store` | OMO `boulder-state` | 原子读写 + 文件锁；schema 受 Zod 校验；router 与 fast lane 都通过它消费 step-level 进度 |
| `intent-gate` | OMO `keyword-detector` | 识别 HF 关键词（`auto mode` / `ultrawork` / `/hf` / `/spec` / `/build` 等），做 entry bias 落地 |

**P1（v0.7 应做，可拆出 v0.7.x patch）**：

| 模块 | 对应 OMO | HF 中的责任 |
|---|---|---|
| `todo-continuation-enforcer` + `ralph-loop` | OMO 同名 hook | 实现 ADR-009 D3 的 fast lane Boulder loop 等价物 |
| `context-window-recovery` + `session-recovery` + `compaction-context-injector` | OMO 同名 hook | 在 OpenCode session compaction 时确保 active spec/design/tasks 摘要 + wisdom-notebook 摘要不被压缩丢失 |
| `wisdom-notebook-injector` | 类似 OMO Atlas notepad 注入 | router handoff 前注入 `features/<f>/notepads/*.md` 摘要给下游 prompt |
| `parallel-explore` | OMO `delegate-task` 的 explore/librarian 路径 | 落地 D5 = A：并行探查不动工件，结果回收到调用节点 |
| `hf-runtime doctor` CLI | OMO `src/cli/doctor/` | 4 类自检：System / Config / Skills 完整性 / Workflow Artifacts 一致性 |

**P2（v0.7 不做，列入 v0.7.x 或后续）**：

- comment-checker 二进制 → 用 `scripts/audit-skill-anatomy.py` 同等地位的 stdlib python 脚本替代，纳入 v0.6
- `interactive-bash` / `look_at` / `ast-grep` runtime 接管 → host 已有等价能力，不重复
- 11 平台 binary 自动化 → v0.7 起步只发 darwin-arm64 + linux-x64 两个，其余按需

**P3（v0.7 永远不做）**：

- **Team Mode**（lead + 8 member + mailbox + tasklist + 多 worktree）—— D5 = A 已经禁止并行实现；HF "一个 Current Active Task" 是核心纪律
- **Hephaestus 等价物**（autonomous deep worker）—— ADR-009 已经禁止 fast lane 绕过 Fagan / gate
- **MCP OAuth 2.0 + PKCE + DCR**（OMO `mcp-oauth/` 18 文件）—— 不是 HF workflow 必需
- **OpenClaw 等价物**（Discord/Telegram/HTTP bidirectional）—— 不是 HF workflow 必需
- **任何 v0.8 删除范围内的事**（部署 / 可观测 / 度量 / 事故 / 性能 gate / 安全 hardening / 调试与错误恢复 / 弃用与迁移）

**Reversibility**：中（P0 / P1 模块清单可在 v0.7 design 阶段微调；P3 项需要 v1.0 之后另开 ADR 才能重新评估）。

### D3：runtime 是 *opt-in*，markdown 包必须独立可用

**决策**：v0.6 markdown 包 + 三客户端配置（Cursor / Claude Code / OpenCode）必须 **不依赖** runtime 即可完整使用 HF workflow（含 v0.6 新增的 7 项改动 + `hf-ultrawork`）。

**实现约束**：
- 任何 SKILL.md 不得写 "必须先安装 harnessflow-runtime 才能继续" 或等价语句
- 涉及 runtime 增强的章节必须用 "If `harnessflow-runtime` is detected..." 条件句
- runtime 的检测方式：通过 OpenCode plugin loaded list 或环境变量 `HF_RUNTIME_AVAILABLE=1`；不要求 SKILL.md 知道检测细节，只要在 runtime 不可用时退化到 markdown-only 路径
- Cursor 永远不安装 runtime（OpenCode plugin API 在 Cursor 不可用）；Cursor 用户走纯 markdown 路径，能力差异在 `docs/cursor-setup.md` 明示
- Claude Code 不安装 runtime（OpenCode plugin API 在 Claude Code 不可用）；Claude Code 用户走纯 markdown 路径

**理由**：
- 三客户端可移植性是 HF 的 moat（ADR-003 D1 / D2 / D3 的延续）
- runtime 引入是为 OpenCode 用户加增强能力，**不是**让 HF 蜕化为 OpenCode-only

**Reversibility**：高（任何 SKILL.md 中的 runtime 增强都可以删除而不破坏 markdown-only 路径）。

### D4：runtime 永远不替用户做 verdict

**决策**：runtime 提供的所有 hook / tool / CLI **不得**写任何节点的 review verdict / gate verdict / approval verdict。

具体禁止：
- `record-evidence` 工具只能写 evidence payload，**不能**包含 `verdict` 字段
- `progress-store` 只能写 step status（`pending` / `in_progress` / `done` / `blocked`），**不能**写"this task is approved"
- `todo-continuation-enforcer` 触发 boulder loop 时只能 dispatch 下一个 step，**不能**自动判定"上一个 step 通过"
- `hf-runtime doctor` CLI 只输出诊断结果，**不能**写"compliance: PASS"等价物到任何工件

允许：
- runtime 可以写"这件事 *声称* 已经发生了"（如 `record-evidence({kind: 'red-test-result', payload: {failures: 3}})`）；判定"这是不是 RED 阶段的合法 evidence" 仍由 `hf-test-review` 的 reviewer 节点决定
- runtime 可以写 `progress.json` 的"current step = X"，但下游 review 节点可以 reject 这个 step

**理由**：
- soul.md 第 2 条"HF 不替用户验收自己"——runtime 是 HF 的延伸，必须遵守相同纪律
- ADR-009 D2 已经锁了 fast lane 不能绕过 Fagan / gate；runtime 是 fast lane 的运行时支撑，更不能成为绕过通道

**Reversibility**：低（一旦 runtime 写过 verdict，回滚需要清理所有受影响 feature 的工件）。

### D5：runtime 与 markdown 包的版本对齐

**决策**：runtime 版本号独立演进（`harnessflow-runtime@0.x.y`），但每个 runtime 版本必须声明兼容的 markdown 包版本范围（`compatible_hf_versions: ">=0.7.0,<0.8.0"`）。

**理由**：
- markdown 包通过 ADR-001 ~ ADR-008 的 release ADR 演进，节奏与 runtime 不必同步
- runtime 落后 markdown 包是允许的（OpenCode 用户可以暂时不升级 runtime）；runtime 超前 markdown 包是禁止的（runtime 不能引入未在 markdown 包中定义的 hook / tool 行为）

**Reversibility**：中（版本号语义改变需要 SemVer major bump）。

## 3. Consequences

**好的**：
- OpenCode 用户获得 OMO 已验证的最大单点收益（hashline 6.7% → 68.3%）
- HF workflow 在 OpenCode 上的 step-level recovery + fast lane idle 检测精度提升
- runtime 与 markdown 包解耦演进，markdown 包仍是三客户端通吃

**坏的 / 风险**：
- TypeScript/Bun + 11 平台 binary 是首次进入工程化交付深度；维护成本显著高于纯 markdown
- 直接 fork OMO `hashline-edit` 24 文件意味着要持续 track OMO 上游的 bug fix；建立"OMO upstream sync" 流程是 v0.7 design 阶段必须解决的问题
- runtime 不可用时（Cursor / Claude Code）能力差异需要在文档中反复说明，否则 OpenCode 用户的体验落差容易被误解为"HF 偏向 OpenCode"

**中性**：
- npm 包名 + bin 名锁定后不可变
- runtime 不进 main-chain workflow 节点拓扑，只是 hook / tool / CLI 增强；hf-workflow-router transition map 不变

## 4. Alternatives considered

- **A1：runtime 走 MCP server 三客户端通吃**
  - 拒绝：架构师 D2 = B；hashline 接管 Read 在 MCP server 形态下需要重写客户端 Read tool
- **A2：runtime 由 OMO 内一个 sub-package 提供**
  - 拒绝：治理诉求不一致；OMO 是 batteries-included 风格，HF 是 narrow & hard 风格
- **A3：v0.7 不做 runtime，markdown 包再 patch 几个版本**
  - 拒绝：架构师 D1 = A 已选择做 runtime；hashline 收益太大不能让
- **A4：v0.7 做 runtime 但同时做 v0.8 工程化末段**
  - 拒绝：架构师明确"不做 v0.8"；本 ADR D2 P3 段把这条永久封禁

## 5. Out of Scope

- runtime 的具体 tool schema（每个 tool 的 input/output 字段）→ v0.7 design 阶段决定
- runtime 与 host OpenCode plugin 的具体配置合并语义 → v0.7 design 阶段决定
- runtime 自身的 evals / 测试覆盖率门禁 → v0.7 tasks 阶段决定（参考 OMO 663 test 的覆盖范围作为基线）
- runtime 的 CI/CD pipeline → v0.7 release ADR 决定（不进入 v0.8 删除范围；这里指的是 runtime 自己的发布流程，不是 HF 用户项目的部署）
- 多人协作场景下 runtime 的权限模型 → 与 ADR-009 D5 同：单架构师模型，多人协作不在范围内

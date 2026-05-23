# ADR-012: HarnessFlow v1.0.0 Release Scope — Stable Markdown Workflow + Subagent Roles

- 状态: accepted（2026-05-23，v1.0.0 release pack ready-for-tag）
- 决策人: 用户（架构师角色）
- 工程团队: HF（按 `docs/principles/soul.md` 协作契约）
- 关联文档:
  - `features/release-v1.0.0/release-pack.md`
  - `docs/decisions/ADR-011-release-scope-v0.6.0.md`
  - `docs/decisions/ADR-008-omo-inspired-roadmap-v0.6-onwards.md`
  - `docs/decisions/ADR-010-harnessflow-runtime-sidecar-boundary.md`

## 背景

v0.6.0 已把 OMO-inspired author-side discipline、wisdom-notebook、gap-analyzer、context-mesh、ultrawork fast lane、step-level recovery 等能力纳入 HF markdown 包。随后本次 v1.0.0 切片进一步把 subagent-driven execution 从概念层落到 HF 的稳定契约面：新增 `hf-subagent-driven-dev`，并把 `hf-implementer` / `hf-reviewer` 定义成顶层 `agents/` 运行时资产。

与此同时，Claude Code slash command definitions 从 `.claude/commands/` 抽到顶层 `commands/`，让命令语义不再绑定某个客户端适配目录；Claude plugin manifest 改为指向 `./commands`。

本 ADR 一次性锁定 v1.0.0 的 5 项范围决策。

## 决策

### Decision 1 — v1.0.0 Scope = stable markdown workflow + subagent-driven execution + top-level runtime assets

v1.0.0 纳入：

- `skills/hf-subagent-driven-dev/`：可选 implementation leaf
- `agents/hf-implementer.md`：实现 subagent，必须使用 `hf-test-driven-dev`
- `agents/hf-reviewer.md`：全 review 节点通用 reviewer subagent
- `commands/`：7 个 slash command definitions 的顶层 canonical 目录
- `install.sh` / `uninstall.sh`：同步 vendor / uninstall `agents/`
- README / setup docs / SECURITY / marketplace metadata / CHANGELOG 同步

不新增部署、监控、回滚、事故、性能或安全 hardening workflow 节点。

### Decision 2 — `hf-reviewer` 覆盖所有 `hf-*review` 节点

`hf-reviewer` 不是 TDD 后专用 reviewer。它覆盖：

- `hf-discovery-review`
- `hf-spec-review`
- `hf-design-review`
- `hf-ui-review`
- `hf-tasks-review`
- `hf-test-review`
- `hf-code-review`
- `hf-traceability-review`

Gate 节点仍由各自 gate skill 签发 verdict；`hf-reviewer` 不替代 gate。

### Decision 3 — `commands/` 顶层化，`.claude/commands/` 不再作为命令源

7 个 slash command definitions 的 canonical source 迁移到 `commands/`。`.claude-plugin/plugin.json` 的 `commands` 字段改为 `./commands`。

理由：

- slash command 语义是 HF 入口偏置，不应长期绑定 Claude 适配目录
- 未来客户端扩展可以复用同一命令语义，而不是复制 `.claude/commands/`
- 避免双源维护

### Decision 4 — SemVer major bump 到 v1.0.0，且不勾 pre-release

v1.0.0 是 major bump / first stable release。

理由：

- top-level `agents/` 和 `commands/` 成为稳定 runtime assets
- plugin manifest command path 从 `.claude/commands` 改为 `commands`
- install topology 从只 vendor `skills/` 扩展到 vendor `skills/` + `agents/`
- HF 的稳定承诺面从 pre-release 进入 v1.0.x 支持窗口

### Decision 5 — 继续保持 P-Honest：release 不等于部署

v1.0.0 release pack 只产 tag readiness。仍不自动执行：

- `git tag`
- `git push --tags`
- GitHub Release 创建
- production / staging deploy
- staged rollout
- monitoring / rollback / health check

这些由项目维护者和项目自身 ops 流程承担。

## Tradeoffs

| 决策点 | 备选方案 | 拒绝理由 |
|---|---|---|
| subagent roles 放哪 | 继续只放在 `skills/hf-subagent-driven-dev/references/` | 用户明确要求定义出两个 agent；顶层 `agents/` 更符合运行时资产语义 |
| review agent 范围 | 只覆盖 TDD 后 test/code/traceability | 用户明确要求 `hf-reviewer` 负责所有 review；Fagan 分离也适用于 spec/design/tasks |
| commands 位置 | 保留 `.claude/commands/` | 客户端适配目录会把命令语义绑定 Claude；顶层 `commands/` 更稳定 |
| 版本号 | v0.7.0 / v0.7.1 | 顶层 runtime assets + stable support window 是对外承诺面变化，适合 v1.0.0 |
| 发布动作 | 自动 tag / GitHub Release | hf-release Hard Gates 禁止；tag 由维护者执行 |

## Consequences

正面：

- subagent-driven execution 的实现者 / 评审者角色清晰
- `hf-implementer` 与 `hf-test-driven-dev` 的 TDD 绑定可冷读
- `hf-reviewer` 覆盖所有 review 节点，Fagan 分离更一致
- command definitions 不再依赖 `.claude/commands/` 路径
- install scripts 能把 `agents/` 带入宿主项目

负面 / 风险：

- v1.0.0 对安装拓扑提出新要求：宿主项目应同时携带 `skills/` 与 `agents/`
- 旧文档或外部脚本如果 hardcode `.claude/commands/` 需要同步到 `commands/`
- OpenCode / Cursor 仍不会原生加载 `commands/`，它们继续走自然语言 + entry shell；这是设计选择

## v1.x Roadmap

| 条目 | 来源 | 状态 |
|---|---|---|
| `harnessflow-runtime` OpenCode plugin | ADR-010 | 可选 runtime sidecar，独立版本节奏 |
| Gemini CLI / Windsurf / GitHub Copilot / Kiro | ADR-011 D5 | 延后到后续客户端扩展版本 |
| 部署 / 监控 / 回滚类能力 | ADR-008 D1 | 永久 out-of-scope |

## Implementation 计划（R1–R5）

- **R1（ADR）**：本文件起草并锁定。
- **R2（Skill / Agent）**：新增 `hf-subagent-driven-dev` + `agents/hf-implementer.md` + `agents/hf-reviewer.md`。
- **R3（Commands / Metadata）**：命令定义迁移到 `commands/`；plugin manifest 指向 `./commands`。
- **R4（Install / Docs）**：install/uninstall、README、setup docs、SECURITY、marketplace metadata 同步。
- **R5（Release）**：release-wide regression、release pack、CHANGELOG v1.0.0 段、tag readiness。

## Notes

- 本 ADR 不追溯重写 v0.6.0 的 release pack；v1.0.0 是在当前 branch scope 上锁定稳定承诺面。
- `hf-release` 不自动 tag；维护者合并 PR 后执行 `git tag v1.0.0`。

# ADR-011: HarnessFlow v0.6.0 Release Scope — OMO-Inspired Author-Side + Fast Lane

- 状态: 起草中（2026-05-15 锁定，等 hf-release Final Confirmation 通过后翻 accepted）
- 决策人: 用户（架构师角色）
- 工程团队: HF（按 `docs/principles/soul.md` 协作契约）
- 关联文档:
  - `docs/decisions/ADR-008-omo-inspired-roadmap-v0.6-onwards.md`（v0.6 路线图锚点 + 永久删除 v0.8）
  - `docs/decisions/ADR-009-execution-mode-fast-lane-governance.md`（fast lane D3+D4 reconciliation）
  - `docs/decisions/ADR-010-harnessflow-runtime-sidecar-boundary.md`（v0.7 runtime sidecar 边界，与本版解耦）
  - `docs/decisions/ADR-005-release-scope-v0.5.0.md`（v0.5.0 patch baseline；本版在其上做 minor bump）
  - `features/002-omo-inspired-v0.6/closeout.md`（本版唯一 candidate workflow-closeout feature）
  - `features/release-v0.6.0/release-pack.md`（本版 release pack）

## 背景

v0.5.1（patch on v0.5.0）GA 后，架构师在 2026-05-13 拍板做 **v0.6 OMO-inspired 升级**——参照 [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) 已经验证的 5 类机制（Atlas wisdom-notebook / Metis gap-analysis / Momus 4-dim rubric / Prometheus interview FSM / `/init-deep` hierarchical context）翻译成 HF 体系内可执行范围。这是 HF 自 v0.4.0 引入 `hf-release` 后**首次大规模 author-side discipline 升级**——不是 patch（如 v0.5.1）也不是 reviewer-experience 增强（如 v0.5.0），而是**实质扩展 author 与 reviewer 的工作面**。

架构师在拍板时同时做了两个**永久性**取舍：

1. **D1 = A**：v0.7 runtime sidecar 做（OpenCode plugin 形态，按 ADR-010）
2. **删除 v0.8 工程化末段**：`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-debugging-and-error-recovery` / `hf-deprecation-and-migration` 6 项**永久 out-of-scope**，不再列入 HF 路线图（HF 拒绝假装是部署工具）

D3 + D4 = A 进一步引入 fast lane（"不停"模式 + boulder loop），由 ADR-009 治理为"explicit opt-in + Fagan/gate 不可绕过"。

`features/002-omo-inspired-v0.6/` 是本版唯一 candidate workflow-closeout feature，dogfood 全程使用 v0.6 fast lane（25+ 自动决策 / 0 escape），同时提供 HYP-002 (Blocking) 的 PASS evidence。

本版工作面规模显著大于 v0.5.0 / v0.5.1（4 新 SKILL.md + 7 改 SKILL.md + 1 stdlib python validator + 1 schema reference + 12 测试套件 / 100 unittest cases + 双层 dogfood + docs refresh），按 SemVer 是 **minor bump**（v0.5.1 → v0.6.0），保持 pre-release flag（与 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 / ADR-005 默认沿用）。

本 ADR 一次性锁定 v0.6.0 范围的 8 项决策。

## 决策

### Decision 1 — v0.6.0 Scope = features/002-omo-inspired-v0.6 全部 18 task + 3 ADR (008/009/010) + 1 hotfix merge (PR #55)

`features/002-omo-inspired-v0.6/closeout.md` 是本版**唯一** candidate workflow-closeout feature，状态 `Closeout Type: workflow-closeout` (2026-05-15 closed)。其内含：

- 4 新 SKILL.md：`hf-wisdom-notebook` / `hf-gap-analyzer` / `hf-context-mesh` / `hf-ultrawork`
- 7 改 SKILL.md：`hf-tasks-review` momus / `hf-specify` Interview FSM / `hf-workflow-router` v0.6 段 / `hf-code-review` CR9 ai-slop / `hf-test-driven-dev` FR-002 集成 / `hf-completion-gate` §6.2 / `using-hf-workflow` 步骤 5 +1 行
- 1 stdlib python validator：`skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py` + 4 fixtures + 10 tests
- 1 schema reference：`skills/hf-test-driven-dev/references/tasks-progress-schema.md` + 4 fixtures
- 12 stdlib python 测试套件 / 100 unittest cases / all PASS
- README.md / README.zh-CN.md / docs/principles/soul.md docs refresh（"v0.6+ planned X" → "out-of-scope per ADR-008 D1"）
- CHANGELOG.md `[Unreleased]` 段含完整 v0.6 scope（待本 ADR 通过后翻为 `[0.6.0]`）

外加从主线 merge 的 PR #55（`fix(cursor): make cross-task continuous execution under auto a Hard rule`）—— 与 v0.6 fast lane 治理正交但相关，并入 v0.6.0 release scope。

无其它 candidate feature；`features/001-install-scripts` 已在 v0.5.x 计入；`features/hotfix-cursor-cross-task-continuous` 是 PR #55 已 merged 的产出，工件直接计入。

### Decision 2 — SemVer minor bump v0.5.1 → v0.6.0；保持 pre-release flag

按 SemVer 2.0.0 决策表：

- **新功能**：4 新 skill + 7 改 skill 是 backward-compatible 的能力扩展（既有 24 SKILL.md 中 7 个被修改的均为 surgical 加段，未删除既有功能；4 新 skill 是纯添加）
- **无 breaking change**：`docs/principles/{soul,methodology-coherence,skill-anatomy}.md` 宪法层不变；`install.sh` / `uninstall.sh` / `.cursor/rules/harness-flow.mdc` / `.claude-plugin/marketplace.json` 不变；既有 24 SKILL.md 的 description / Object Contract / Hard Gates / Workflow / Output Contract 字段语义不变（只在指定段添加）
- **bump 类型**：minor（不是 patch 因为 4 新 skill 是新增能力，不是 bug fix）

**Pre-release 标记**：保留 `yes`，沿用 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 / ADR-005 D6 默认——HF 自 v0.1.0 起所有 GitHub Releases 标 pre-release，等 v1.0 才正式去掉。本版 v0.6.0 不破例。

### Decision 3 — 6 项工程化末段 skill 永久从路线图删除（继承 ADR-008 D1）

`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-debugging-and-error-recovery` / `hf-deprecation-and-migration` —— 这 6 项**永远不实现**，从 HF 路线图永久删除。

理由：

- ADR-008 D1 已经锁定（架构师 2026-05-13 拍板"不做 v0.8"）
- 这 6 项属于"代码合并后到上线之间"的工程化层；HF 灵魂文档（`docs/principles/soul.md`）立场是"HF 不假装是部署工具"
- 项目实际需要这些能力时，由项目自身的 ops 流程承担（GitHub Actions / GitLab CI / ArgoCD / Datadog / PagerDuty / 等等）；HF 不重复造轮子
- v0.5.0 之前的"v0.6+ planned" 措辞会给用户错误期望，本版 docs refresh（TASK-016）已统一改为 "out-of-scope per ADR-008 D1"

### Decision 4 — v0.7 runtime sidecar 范围与版本对齐策略

v0.7 runtime（`harnessflow-runtime` OpenCode plugin，按 ADR-010）是**独立 npm 包**，与 markdown 包独立演进：

- markdown 包版本：v0.6.0（本 release）
- runtime 版本：暂未起步；v0.7 release 时另开 `features/release-v0.7.0-runtime/`
- 兼容性约定（按 ADR-010 D5）：runtime 必须声明 `compatible_hf_versions`（如 `">=0.7.0,<0.8.0"`）；runtime 落后 markdown 包允许，超前禁止

本版 v0.6.0 不附带 runtime；OpenCode 用户需要等 v0.7 才能挂 runtime hook。Cursor / Claude Code 用户走纯 markdown 路径（HYP-002 PASS 证明可用）。

### Decision 5 — 4 个剩余客户端扩展继续延后到 v0.7+ / v0.9（ADR-008 D1 + ADR-005 D7 延续）

Gemini CLI / Windsurf / GitHub Copilot / Kiro 4 个客户端扩展按 ADR-008 D1 路线图：

- v0.7 = 不扩客户端（专做 runtime sidecar）
- **v0.9 = 客户端扩展**（4 个剩余客户端官方支持）
- v1.0 = 商用级形态收尾

本版 v0.6.0 仍只支持 Claude Code + OpenCode + Cursor 三客户端（ADR-003 既有范围）。

### Decision 6 — WriteOnce demo evidence trail 不刷新（继承 ADR-005 D8 / ADR-004 D9 / ADR-003 D10）

`examples/writeonce/` 在 v0.6.0 不重跑、不刷新工件、不重新走 hf-* workflow。

理由：

- WriteOnce 的价值是"完整 SDD chain trail 的可读 example"；其 evidence 时间戳本身就是 v0.1.0~v0.5.x 的 dogfood 历史的一部分
- v0.6.0 的 dogfood 由 `features/002-omo-inspired-v0.6/` 自身承担（更具代表性，因为它本身在使用 v0.6 新 skill）
- 强加 WriteOnce 重跑是空洞同步，不带新信息

### Decision 7 — Release-wide regression scope = 12 stdlib python 测试套件 + audit-skill-anatomy.py + install.sh round-trip

按 hf-release SKILL.md §6 协议，release-wide regression scope = `union(各候选 feature 的 affected modules)`。本版唯一 candidate features/002 影响面为：

- 全 29 SKILL.md（25 既有 + 4 新）→ `audit-skill-anatomy.py`
- 12 stdlib python 测试套件（覆盖 4 新 SKILL.md + 7 改 SKILL.md + 1 stdlib python validator + schema reference）
- install.sh / uninstall.sh round-trip（NFR-003 验证 + smoke）

**Fresh evidence 要求**：执行点必须晚于 features/002 closeout 时间（2026-05-15）。本版 release-wide regression 在 2026-05-15 跑过，evidence 落 `features/release-v0.6.0/verification/release-regression.md`。

### Decision 8 — Pre-release 工程级 hygiene 不退化为 ops 项

按 hf-release SKILL.md §8 严格执行 Pre-Release Engineering Checklist 的 4 小节（Code & Evidence / Documentation Sync / Versioning Hygiene / Worktree State）；显式 **不**承担 §8 末尾 "Out of Scope" 段的 6 项 ops 动作（部署 / staged rollout / 监控 / 回滚演练 / health check / 上线后观察）。

`.claude-plugin/plugin.json` 不存在（未启用）；`.claude-plugin/marketplace.json` 存在但 v0.6.0 不修改其 version 字段（marketplace plugin 通过 git tag / commit 拉取，不依赖 manifest 内的 version）。

CHANGELOG `[v0.6.0]` 段由 hf-release 在 Final Confirmation 通过时从 `[Unreleased]` 翻入。

## Tradeoffs

| 取舍 | 选择 | 拒绝的备选 |
|---|---|---|
| v0.6.0 是 minor 还是 major？ | minor（无 breaking change） | major（保留给真正的 breaking 时机；本版 surgical addition 不破坏 backward compat） |
| 是否一并发布 v0.7 runtime？ | 否（runtime 独立 release） | 同 release（会拉长本版 scope；按 D4 解耦） |
| 是否同时扩客户端到 4 个剩余的？ | 否（继承 ADR-005 D7 延后） | 同时扩（v0.6 范围已足够大；客户端扩展放 v0.9） |
| 是否重跑 WriteOnce demo? | 否（继承 ADR-005 D8） | 重跑（空洞同步） |
| pre-release 标记 | 保留 yes（沿用历史默认） | 去掉（v1.0 才合适；v0.6 还在演进中） |
| 永久删除 v0.8 还是再次延后？ | 永久删除（架构师 2026-05-13 D1） | 再次延后到 v0.8/v0.9（违反 soul.md "HF 不假装是部署工具"） |

## Consequences

### 好的

- HF 在 author-side discipline + fast lane + cross-task wisdom accumulation 三个维度上对齐 OMO 已验证的最佳实践
- HYP-002 PASS 证明 markdown-only fast lane 可用，三客户端可移植性的 moat 保住
- 6 项工程化末段 skill 永久删除，HF scope 显式收敛，停止给用户错误期望
- 本版 dogfood（features/002 自身）累计 25+ fast lane decisions / 0 escape，验证了 fast lane 治理的实际可执行性

### 坏的 / 风险

- v0.7 runtime（OpenCode plugin）将首次进入 TypeScript/Bun + 11 平台 binary 工程化交付深度；维护成本显著高于纯 markdown
- v0.6 引入的 4 新 + 7 改 skill 让 SKILL.md 总数升至 29；逼近 anatomy v2 共享 token 预算上限（25000 tokens / ~5 skill），未来如继续扩需评估 skill 拆 / merge
- markdown-only fast lane 精度依赖 host agent 自觉（按 SKILL.md 与 progress.md 工件执行）；OpenCode 用户可在 v0.7 runtime 提升精度，Cursor / Claude Code 用户保持当前精度

### 中性

- 按 SemVer minor bump，v0.6.0 是 backward-compatible 的能力扩展；既有用户升级零摩擦
- WriteOnce demo 不刷新；仍保留 v0.5.x 时点的 evidence trail 作为可读历史

## v0.7+ Roadmap (informational)

- **v0.7**: `harnessflow-runtime` OpenCode plugin（按 ADR-010 P0 + P1 模块；hashline-edit / record-evidence / progress-store / intent-gate / 5 类 hook）
- **v0.9**: 4 个剩余客户端扩展（Gemini CLI / Windsurf / GitHub Copilot / Kiro）
- **v1.0**: 商用级形态收尾（v0.9 全客户端验证 + runtime 自身可观测 + 非 toy `examples/`）
- **永不**: 6 项工程化末段 skill（按 D3 + ADR-008 D1）

## Notes

- 本 ADR 起草中状态会在 hf-release Final Confirmation 通过时翻为 accepted（按 hf-release SKILL.md §8 与 ADR-005 同形态约定）
- 本版 release pack 路径 `features/release-v0.6.0/release-pack.md` 与 v0.5.0 / v0.5.1 同形态（仍是 release-tier 独立目录）
- 本版未自动执行 `git tag` 或 `git push --tags`（按 hf-release Hard Gates）；tag 操作由架构师在合并 PR 后执行

# Pre-Release Engineering Checklist

`hf-release` §8 详细 checklist。**仅工程级 hygiene；显式不含 ops 项**。

## 使用说明

- 默认保存路径：`features/release-vX.Y.Z/verification/pre-release-checklist.md`
- 每条勾选 / 显式 N/A（按 profile 跳过 / 项目未启用 / 本 release 未触发）
- 任一条 FAIL → 不允许进入 §11 Final Confirmation
- 项目级约定可覆盖具体核对命令（例如 `npm test` → `make test`）；不能覆盖核对项本身

## Code & Evidence

| # | 核对项 | 通过条件 | 失败时去哪里 |
|---|---|---|---|
| C1 | release-wide regression 通过 | `features/release-vX.Y.Z/verification/release-regression.md` 存在且结论 PASS，且执行时间晚于所有候选 feature 的最晚 closeout 时间 | 回 `hf-test-driven-dev` 修复对应 feature 的回归 |
| C2 | cross-feature traceability 摘要落盘 | `features/release-vX.Y.Z/verification/release-traceability.md` 存在；任何 missing verdict 的 feature 已显式标 N/A（按 profile 跳过） | 回 `hf-traceability-review` 补单 feature traceability |
| C3 | 候选 feature 全为 `workflow-closeout` 状态 | 每个候选 feature 的 `closeout.md` 第一行 `Closeout Type: workflow-closeout` | 回 `hf-finalize` 把 task-closeout 升级到 workflow-closeout |
| C4 | release base branch 上 lint / type / build 通过 | 项目 CI 入口或本地 `npm run lint && npm run typecheck && npm run build` 等价命令 PASS | 回 `hf-test-driven-dev` 修复 |
| C5 | 无 release-blocking PR 仍 open | 候选 feature 中 worktree disposition = `kept-for-pr` 的 PR 已合并到 release base branch | 先合并 PR 或把该 feature 移出本次 scope |

## Documentation Sync（sync-on-presence 协议内联）

| # | 核对项 | 通过条件 |
|---|---|---|
| D1 | **CHANGELOG.md** 的 `[vX.Y.Z]` 段已写 | 段内含 Added / Changed / Decided / Deferred / Notes（按本版实际有的分类即可，至少 Added + Notes 两段）；段末有 `[X.Y.Z]: <link>` 链接行 |
| D2 | 顶层导航已更新 | 档 0/1：仓库根 `README.md` 中 active feature / 最近 release 行已同步；档 2：`docs/index.md` 已加 vX.Y.Z 入口 |
| D3 | 涉及的 ADR 状态已批量翻转 | 候选 feature 引用的 ADR + 本次 release scope ADR 的状态全部从 `proposed` → `accepted`（在 §11 Final Confirmation 通过时翻转，不提前） |
| D4 | `docs/release-notes/vX.Y.Z.md` 同步 | 仅档 2 启用；含 Highlights / Migration Notes / Known Limitations / Acknowledgements 段 |
| D5 | 架构概述按存在同步 | `docs/architecture.md`（档 1）或 `docs/arc42/`（档 2）；仅本 release 改了架构图景时；二者只能同时存在一份 |
| D6 | `docs/runbooks/` 同步 | 仅目录已存在或本 release 触发首次启用；未触发写 `N/A（项目当前未启用此资产 / 本 release 未触发）` |
| D7 | `docs/slo/` 同步 | 同上 |
| D8 | `docs/diagrams/` 同步 | 同上 |
| D9 | feature closeout `Release / Docs Sync` 字段对账一致 | 任一候选 feature 声称已同步某路径，本次 release 必须能找到对应路径；不一致即视为冲突，停下问用户 |
| D10 | Migration / breaking changes 已写入 release notes 的 `## Migration Notes` | 若本版含任何 breaking change（C1 → §4 SemVer 决策应得 major bump），必须写；否则写 `N/A（无 breaking change）` |
| D11 | Known Limitations 已聚合 | 各 feature closeout 的 `Limits / Open Notes` 字段汇总到 release notes / release pack；含 out-of-scope 能力的承担方说明（项目自身 ops 流程 / 项目自身安全流程 / 等） |

## Versioning Hygiene

| # | 核对项 | 通过条件 |
|---|---|---|
| V1 | scope ADR 已 commit | `docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md` 已 git add / commit；状态字段 = 起草中（§11 通过后翻 accepted） |
| V2 | SemVer + pre-release 标记已写入 release pack | release pack `## Release Summary` 段含 `Version: vX.Y.Z` + `Pre-release: yes/no` + `Bump Type: major/minor/patch` 三字段 |
| V3 | `.claude-plugin/plugin.json` `version` 同步 | 仅在项目本身是 Claude Code 插件时；不存在写 N/A |
| V4 | `.claude-plugin/marketplace.json` 描述同步 | 同上 |
| V5 | `SECURITY.md` Supported Versions 表加 `X.Y.x` 行 | 仅在项目存在 `SECURITY.md` 时；前一版降级（仅 security-only 或 older） |
| V6 | 项目级元数据中的版本号已同步 | `package.json` / `pyproject.toml` / `Cargo.toml` / `Cargo.lock` / `go.mod` / 等存在的所有元数据文件中的版本号字段 |
| V7 | 相关版本链接表 / 链接 update | CHANGELOG 末尾 `[X.Y.Z]: <link>` 行；README 中可能的 "latest version" badge / link |

## Worktree / Branch State

| # | 核对项 | 通过条件 |
|---|---|---|
| W1 | worktree disposition 全部记录 | 每个候选 feature 的 disposition 写入 release pack `## Worktree Disposition` 段，值 = `kept-for-pr` / `cleaned-per-project-rule` / `in-place` |
| W2 | release base branch 状态 | 已是各候选 feature 合并后的状态；HEAD commit 与 release pack `## Tag Readiness` 段的 `Suggested Commit` 一致 |
| W3 | 未自动删除 worktree | 本 skill 不删 worktree；只能记录；如需清理，由项目维护者按项目 worktree-cleanup convention 执行 |

## Out of Scope（显式列出本 skill **不**做的事）

| 动作 | 落到哪 |
|---|---|
| 部署到 production / staging / canary | 项目自身的 ops 流程 |
| Feature flag 0% → 5% → 100% 的 staged rollout | 项目自身的 ops 流程 |
| 监控仪表盘 / 错误上报配置 | 项目自身的 ops 流程 |
| SLO 配置 / 基线监控 | 项目自身的 ops 流程 |
| 回滚 procedure / 回滚演练 | 项目自身的 ops 流程 |
| Health check / CDN / DNS / SSL 配置 | 项目自身的 ops 流程 |
| Rate limiting / 安全 headers 配置 | 项目自身的安全流程 |
| 上线后的观察窗口 | 项目自身的 ops 流程 |
| Staged rollout decision thresholds | 项目自身的 ops 流程 |
| User communication / launch announcement | 项目自身的发布沟通流程 |

以上动作 **不应** 出现在 release pack 或 release notes 的"已完成"清单中；如果项目需要在切版本同时做这些事，请按项目自身的 ops / 安全 / 发布沟通流程独立承担，**不**写进本 skill 的 evidence 中。

## 失败处理流程

任一项 FAIL：

1. 在 release pack `## Status` 字段写 `blocked-on-<check-id>`
2. 在 `## Limits / Open Notes` 段记录失败细节 + 当前状态
3. Next Action 写具体阻塞点（不写回 router）
4. 暂停 §11 Final Confirmation；解决失败项后回到对应 §<step> 重做

## 项目级覆盖

项目可在自家 guidelines / `CONTRIBUTING.md` / 宿主工具链 sidecar 中声明：

- 各核对项的具体命令（例如把 C4 的 lint 命令从 `npm run lint` 改成 `pnpm lint`）
- 是否启用某些 sync-on-presence 资产（D6 / D7 / D8）
- 元数据文件清单（V6）

`hf-release` 优先遵循项目级声明；项目未声明时退回本模板默认。

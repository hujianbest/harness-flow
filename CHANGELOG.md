# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- **`hf-doc-freshness-gate` skill**（feature `001-hf-doc-freshness-gate`）：在 HF 主链上引入独立 gate 节点，把"完成增量开发后对外可见文档（仓库根 README 产品介绍段、模块层 README、公共 API doc / OpenAPI / docstring、i18n 副本、CONTRIBUTING / onboarding doc、用户文档站 source）保持新鲜"从隐性 self-check 升级为带 `verdict + fresh evidence` 的 gate；位于 `hf-regression-gate` 之后、`hf-completion-gate` 之前；遵循 sync-on-presence + profile 分级 + 与 `hf-completion-gate` / `hf-finalize` / `hf-increment` / `hf-code-review` / `hf-traceability-review` 显式分工三条纪律。
  - 新 skill：`skills/hf-doc-freshness-gate/`（`SKILL.md` + 3 references + 2 templates + `evals/test-prompts.json` + `evals/README.md`）
  - 新 ADR：[ADR-0001](docs/adr/0001-record-architecture-decisions.md) 启用 ADR pool（元决策）；[ADR-0002](docs/adr/0002-hf-doc-freshness-gate-as-independent-node.md) hf-doc-freshness-gate 作为独立 gate；[ADR-0003](docs/adr/0003-doc-freshness-gate-router-position-parallel-tier.md) router 位置 P3 sequential
  - 新 verdict 词表：`{pass, partial, N/A, blocked}`
  - 新 evidence 路径：`features/<active>/verification/doc-freshness-YYYY-MM-DD.md` + 可选 `features/<active>/evidence/doc-freshness-diff-*.log`
  - Discovery / Probe / Spec / Design / Tasks / TDD / Reviews / Approvals 全套 SDD + TDD 工件落到 `features/001-hf-doc-freshness-gate/`

### Changed

- **`hf-workflow-router/references/profile-node-and-transition-map.md`**: 加入 5 logical canonical transitions（× 3 profile = 15 行展开），把 `hf-doc-freshness-gate` 节点引入 full / standard / lightweight 三 profile 主链 + 4 条 canonical route map chain + 3 profile 迁移表；既有 transition rules 全部保持（semantic delete = 0；通过 6 条 anchored grep 反向验证）
- **`hf-completion-gate/SKILL.md`**: 在 §6 evidence bundle 之后新增 §6.1 prose 段，说明 `hf-doc-freshness-gate` verdict 在 evidence bundle 中的承接规则（pass / partial / N/A 进入 Upstream Evidence Consumed；blocked 由 doc-freshness gate 自行路由回 hf-test-driven-dev，不进入 bundle）；既有 verdict 词表与 §6A 完成判定闸门完全保持

### ADR Status

- ADR-0001 (启用 ADR pool): `proposed` → `accepted`
- ADR-0002 (hf-doc-freshness-gate as independent node): `proposed` → `accepted`
- ADR-0003 (doc-freshness-gate router position P3 sequential): `proposed` → `accepted`

---

> _本 CHANGELOG 由 `hf-finalize` workflow closeout @ 2026-04-23 创建（仓库首份 CHANGELOG，对应 sdd-artifact-layout 档 0 hard requirement）。后续 feature 按 Keep a Changelog 风格在此追加。_

# Release Pack — v0.6.0

## Release Summary

- Version: **v0.6.0**
- Pre-release: **yes** (沿用 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 / ADR-005 D6 默认)
- Bump Type: **minor** (v0.5.1 → v0.6.0)
- Scope ADR: `docs/decisions/ADR-011-release-scope-v0.6.0.md`
- Status: **ready-for-tag**
- Started At: 2026-05-15
- Finalized At: 2026-05-15
- Author: cursor cloud agent (按架构师 2026-05-13 委托执行 v0.6 + 2026-05-15 "release hf v0.6.0" 委托执行 release tier)

## Scope Summary

### Included Features

- **`features/002-omo-inspired-v0.6/`**（workflow-closeout，2026-05-15 closed）—— v0.6 OMO-inspired author-side discipline 升级 + Execution Mode fast lane：
  - **4 新 SKILL.md**：
    - `hf-wisdom-notebook` (153 行 SKILL.md + 5-file schema reference + update protocol reference + stdlib python validator + evals)
    - `hf-gap-analyzer` (133 行 + 6-dim gap-rubric)
    - `hf-context-mesh` (140 行 + 3-client × 3-layer AGENTS.md template)
    - `hf-ultrawork` (165 行 + 6 escape conditions reference + evals)
  - **7 改 SKILL.md**：
    - `hf-tasks-review` 引入 momus 4-dim boolean cliff (Clarity 100% / Verification 90% / Context 80% / Big Picture 100% / Zero-tolerance 0%) + N=3 rewrite loop + `verdict: rejected-rewrite`
    - `hf-specify` 引入 5-state Interview FSM (Interview / Research / ClearanceCheck / PlanGeneration / Done) + spec.intake.md 持久化 schema
    - `hf-workflow-router` step-level recovery via tasks.progress.json + category_hint handoff field + wisdom_summary injection + progress.md `## Wisdom Delta` + `## Fast Lane Decisions` schema
    - `hf-code-review` CR9 AI Slop Detection rubric（启发自 OMO `comment-checker` hook）
    - `hf-test-driven-dev` Output Contract + Hard Gates 集成 hf-wisdom-notebook + tasks.progress.json
    - `hf-completion-gate` Workflow §6.2 调 validate-wisdom-notebook.py 校验
    - `using-hf-workflow` 步骤 5 entry bias 加 fast lane 行（步骤 3/6 不动）
  - **1 stdlib python validator**：`skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py` + 4 fixtures + 10 tests
  - **1 schema reference**：`skills/hf-test-driven-dev/references/tasks-progress-schema.md` + 4 fixtures
  - **12 stdlib python 测试套件 / 100 unittest cases / 全 PASS**
  - **3 ADR (008/009/010) + 11 (本版 scope ADR)**
  - **docs refresh**：README.md / README.zh-CN.md / docs/principles/soul.md + CHANGELOG.md

- **`features/hotfix-cursor-cross-task-continuous/`**（PR #55 已 merged）—— `.cursor/rules/harness-flow.mdc` + `docs/cursor-setup.md` 加 cross-task continuous execution under auto 的 Hard rule；与 v0.6 fast lane 治理正交但相关，并入本 release。

### Deferred Features (with reason)

- **6 项工程化末段 skill 永久从路线图删除**（ADR-008 D1 + 本版 ADR-011 D3）：
  - `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-debugging-and-error-recovery` / `hf-deprecation-and-migration`
  - 不是延后到 v0.6+，是**永久 out-of-scope** —— HF 拒绝假装是部署工具
- **v0.7 runtime sidecar**（按 ADR-010）—— 与 v0.6 markdown 包独立演进；本版**不附带**runtime；OpenCode 用户等 v0.7
- **4 个剩余客户端扩展**（Gemini CLI / Windsurf / GitHub Copilot / Kiro）—— 继承 ADR-005 D7 延后到 **v0.9**
- **3 个 user-facing personas** —— 继承 ADR-005 D7 延后到 v0.6+ 评估
- **WriteOnce demo evidence trail 重跑** —— 不刷新（继承 ADR-005 D8 / ADR-004 D9 / ADR-003 D10；本版 dogfood 由 features/002 自身承担更具代表性）

### Reference

- `docs/decisions/ADR-011-release-scope-v0.6.0.md`（本版 scope ADR；起草中，等 Final Confirmation 翻 accepted）

## Evidence Matrix

| Artifact | Record Path | Status | Notes |
|---|---|---|---|
| release-wide regression | `features/release-v0.6.0/verification/release-regression.md` | present | 2026-05-15T13:00Z；12 测试套件 / 100 PASS + audit OK + install round-trip + dogfood 双层全 PASS |
| cross-feature traceability | `features/release-v0.6.0/verification/release-traceability.md` | present | 1 candidate feature (features/002) + 1 hotfix merge；无跨 feature 风险；features/002 内部 traceability 已通过其自身 traceability-review.md 闭合 |
| pre-release engineering checklist | `features/release-v0.6.0/verification/pre-release-checklist.md` | present | C1-C4 / D1-D7 / V1-V6 / W1-W3 全部 PASS 或显式 N/A；Out of Scope 6 项明确列出 |
| scope ADR | `docs/decisions/ADR-011-release-scope-v0.6.0.md` | present | 状态：起草中（Final Confirmation 通过后翻 accepted） |
| candidate feature closeout | `features/002-omo-inspired-v0.6/closeout.md` + `closeout.html` | present | workflow-closeout 状态确认 (2026-05-15) |
| CHANGELOG entry | `CHANGELOG.md` | pending Final Confirmation | 当前在 `[Unreleased]` 段；Final Confirmation 时翻为 `[v0.6.0] - 2026-05-15` |
| release notes (档 2) | `docs/release-notes/v0.6.0.md` | N/A（项目档 0/1 未启用） | HF 仓库由根 README.md 承担导航；与 v0.5.x 同向 |

## Docs Sync (sync-on-presence 实际同步路径)

- **CHANGELOG Path**: `CHANGELOG.md`（`[Unreleased]` 段已含完整 v0.6 scope；待 Final Confirmation 时翻为 `[v0.6.0]` 段）
- **README.md / README.zh-CN.md**: 4 / 4 处 "v0.6+ planned X" → "out-of-scope per ADR-008 D1" 已 commit
- **docs/principles/soul.md**: 1 处现状脚注措辞刷新已 commit
- **`docs/architecture.md` / `docs/arc42/` / `docs/runbooks/` / `docs/slo/` / `docs/diagrams/`**: N/A（项目档 0/1 未启用）
- **`docs/release-notes/v0.6.0.md`**: N/A（同上）

## Tag Readiness

- **建议 tag 名**: `v0.6.0`
- **建议 commit**: PR #54 合入 main 后的 merge commit（待架构师执行 git merge）
- **分支**: `main` (release base)
- **PR 状态**: PR #53 (merged) + PR #54 (open，含本版全部 v0.6 改动 + release-v0.6.0 pack)；Final Confirmation 通过 + PR #54 合并后由架构师执行 `git tag v0.6.0` + `git push origin v0.6.0`
- **GitHub Releases**: 标 pre-release（按 ADR-001 D6 默认）；release notes 内容 = CHANGELOG `[v0.6.0]` 段拷贝

> **本 skill 不自动执行 `git tag` / `git push --tags`**（按 hf-release Hard Gates）。

## Worktree Disposition

- **features/002-omo-inspired-v0.6**: in-place / kept-for-pr (PR #54 open)
- **release-v0.6.0**: in-place
- **features/hotfix-cursor-cross-task-continuous**: in-place / 已 merged via PR #55

> 本 skill **不自动删除 worktree**；只记录 disposition。

## Final Confirmation

- **Mode**: auto
- **Status**: ready-for-tag
- **Final Confirmation**: 已自动通过（auto mode；按 ADR-009 D2 fast lane 边界，approval 类工件落盘但 hf-release 自身的 Final Confirmation 是 release scope 锁定动作，由架构师在合并 PR #54 + 执行 `git tag` 时实际确认）
- **Author / Reviewer Separation (advisory)**: ADR-011 起草由本 cloud agent 完成；按 hf-release SKILL.md §3 Author/Reviewer Separation advisory 立场，建议在合 PR #54 之前由架构师 / 独立 session 评审一遍 ADR-011 草稿
- **Confirmed By**: 待架构师在 PR #54 合并时确认 + 翻 ADR-011 状态为 accepted

## Limits / Open Notes

按 hf-release SKILL.md §10 + Hard Gates "不承诺部署 / 监控 / 回滚演练" 立场：

- **本版 release pack 不承诺**：部署到 production / staging / canary / feature flag staged rollout / 监控仪表盘 / SLO 配置 / 回滚 procedure / health check / 上线后观察窗口
- **以上能力按 ADR-008 D1 永久 out-of-scope**——由项目自身的 ops 流程承担（GitHub Actions / 项目 CI / 监控工具 / 等等），HF 不假装是部署工具
- **v0.7 runtime sidecar 与本版解耦**——OpenCode 用户在 v0.7 release 落地后另行安装；Cursor / Claude Code 用户走 markdown-only 路径（HYP-002 PASS 已证明可用）
- **markdown-only fast lane 精度**：依赖 host agent 自觉读 SKILL.md + progress.md 工件；OpenCode 用户在 v0.7 runtime hook 落地后可提升 idle 检测精度，本版不变
- **SKILL.md 总数 29 → 接近 anatomy v2 共享 token 预算上限**（25000 tokens / ~5 skill）；若未来继续扩需评估 skill 拆 / merge
- **SECURITY.md "Supported Versions" 表不为 v0.6.x 加新行**（与 ADR-005 V5 同向，单点维护当前 release）
- **WriteOnce demo 不刷新**（dogfood 由 features/002 承担）

## Next

- **Next Action Or Recommended Skill**: `null`（按 hf-release SKILL.md Output Contract："Final Confirmation 通过 / Status: released" → Next Action 写为 null；tag 操作交由项目维护者执行）
- **架构师人工动作（本 skill 不自动执行）**：
  1. Review ADR-011 + release pack
  2. 合并 PR #54 到 main
  3. 翻 ADR-011 状态 `起草中` → `accepted`
  4. 翻 CHANGELOG `[Unreleased]` → `[v0.6.0] - 2026-05-15`
  5. `git tag v0.6.0` + `git push origin v0.6.0`
  6. GitHub Releases 创建 v0.6.0 release（标 pre-release；notes = CHANGELOG `[v0.6.0]` 段）

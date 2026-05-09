# Finalize Closeout Pack

使用说明：

- 这是 `hf-finalize` 的 closeout pack 模板。
- 用于两种分支：`task-closeout` 与 `workflow-closeout`。
- **默认保存路径：`features/<NNN>-<slug>/closeout.md`**（不再叫 `finalize-closeout-pack.md`）。
- `Release / Docs Sync` 必须显式列出本次 closeout 同步到 `docs/` 的所有路径（arc42、glossary、runbooks、SLO、release notes、CHANGELOG、ADR 状态翻转等），缺失项目应视为 `blocked`。
- 若项目在 项目声明了等价模板或 closeout 路径，优先遵循项目约定。
- **HTML 视觉伴生报告**：写完 `closeout.md` 后必须运行
  `python3 scripts/render-closeout-html.py features/<NNN>-<slug>/`
  生成 `closeout.html`（同目录），作为给 reviewer / 干系人查看的视觉总结。它**渲染**本 closeout pack 的内容，不引入新事实。
- **Coverage 数据**：希望 HTML 报告显示代码覆盖率时，把 vitest/jest/pytest-cov 等工具的 `--coverage --reporter=json-summary` 输出落到 `verification/coverage.json`，或在 `verification/regression-*.md` / `evidence/regression-*.log` 中保留 `Lines:` / `Branches:` / istanbul `All files | …` 行；若不提供则 HTML 自动显示 `未提供`，不阻塞 closeout。

## Closeout Summary

- Closeout Type: `task-closeout` | `workflow-closeout` | `blocked`
- Scope:
- Conclusion:
- Based On Completion Record:
- Based On Regression Record:

## Evidence Matrix

- Artifact:
- Record Path:
- Status: `present` | `N/A (profile skipped)` | `missing`
- Notes:

## State Sync

- Current Stage:
- Current Active Task:
- Workspace Isolation:
- Worktree Path:
- Worktree Branch:
- Worktree Disposition: `kept-for-pr` | `cleaned-per-project-rule` | `in-place`

## Release / Docs Sync

- Release Notes Path:                      # 例：docs/release-notes/v1.5.0.md
- CHANGELOG Path:                          # 例：CHANGELOG.md（v1.5.0 入口）
- Updated Long-Term Assets:                # 显式列出本次同步到 docs/ 的路径
  - `docs/arc42/...`
  - `docs/runbooks/...`
  - `docs/slo/...`
  - `docs/adr/NNNN-...md`（status: proposed → accepted）
- Status Fields Synced:
- Index Updated:                           # docs/index.md 是否已更新

## Handoff

- Remaining Approved Tasks:
- Next Action Or Recommended Skill:
- PR / Branch Status:
- Limits / Open Notes:

## Branch Rules

- `task-closeout`:
  - `Current Stage` 应写回 `hf-workflow-router`
  - `Next Action Or Recommended Skill` 应写 `hf-workflow-router`
  - 不得声称 workflow 已结束

- `workflow-closeout`:
  - `Current Active Task` 应清空或显式关闭
  - `Next Action Or Recommended Skill` 应写 `null` 或项目 null 约定
  - 不得再写回 `hf-workflow-router`

- `blocked`:
  - `Current Stage` 应写回 `hf-workflow-router`
  - `Next Action Or Recommended Skill` 应写 `hf-workflow-router`
  - 不得声称 closeout 已完成

## Final Confirmation

- `workflow-closeout` + `interactive`：
  - Question: 是否确认正式结束本轮 workflow？
  - If confirmed: write `Next Action Or Recommended Skill: null`
  - If not confirmed: return to `hf-workflow-router`

## HTML Companion Report

- Path: `features/<NNN>-<slug>/closeout.html`
- Generator: `python3 scripts/render-closeout-html.py features/<NNN>-<slug>/`
- 必填：写完本 `closeout.md` 后立即生成；HTML 由本 pack + `evidence/*.log` + `verification/*.md`(+ optional `verification/coverage.json`) 渲染，不允许在 HTML 中加入 pack 之外的事实。
- Coverage 数据源（按优先顺序）：`verification/coverage.json` → `verification/*.md` 中的 `Lines:` / `Branches:` 行 → evidence 日志中的 istanbul / vitest 覆盖率表；缺失则 HTML 渲染为 `未提供`。

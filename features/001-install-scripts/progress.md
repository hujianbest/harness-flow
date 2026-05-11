# Task Progress — 001-install-scripts

## Goal

- Goal: 为 HarnessFlow 增加可一键安装到任意宿主仓库的 install/uninstall 脚本，覆盖 Cursor 与 OpenCode 两种官方支持的客户端集成路径
- Owner: cursor agent
- Status: in-progress
- Last Updated: 2026-05-11

## Current Workflow State

- Current Stage: hf-design
- Workflow Profile: full
- Execution Mode: auto
- Current Active Feature: features/001-install-scripts/
- Current Active Task:
- Pending Reviews And Gates: hf-design-review
- Relevant Files:
  - `docs/cursor-setup.md`（现有 Cursor 集成手册——脚本要替代其中"vendor by copying / symlink"段落的手工步骤）
  - `docs/opencode-setup.md`（现有 OpenCode 集成手册——同上）
  - `.cursor/rules/harness-flow.mdc`（Cursor rule，作为 install 时复制目标之一）
  - `.opencode/skills`（OpenCode skills 软链接根，作为 install 时 symlink/copy 目标之一）
  - `skills/`（HF 24 个 hf-* + using-hf-workflow，所有 install 拓扑都要覆盖到）
- Constraints:
  - 现有 ADR-006 D1：HF skill anatomy v2 锁定 4 类子目录（`SKILL.md` / `references/` / `evals/` / `scripts/`）；安装脚本必须把 skill-owned `scripts/` 子目录一起带过去
  - 现有 ADR-005 D9 / ADR-004 D7：HF 不自动执行 `git tag` / 不部署；install 脚本只做"vendor by copy / symlink + rule placement"，不触碰宿主仓库的 git / CI
  - HF 仓库本身的依赖最小化原则：脚本不引入新的运行时依赖（不要求 Node / Python；bash + 标准 unix 工具 + 可选 PowerShell）

## Progress Notes

- What Changed:
  - 创建 feature 目录骨架（README.md / progress.md）
  - 起草 spec.md（含 §3 Success Metrics、§4 Key Hypotheses、§9 NFR QAS）
  - 起草 spec-deferred.md（DEF-001..DEF-007）
  - 完成 hf-spec-review Round 1 + 2，approval 写入 approvals/spec-approval-2026-05-11.md
  - 起草 design.md（21 章；按 full profile 落 Event Storming Snapshot；DDD strategic + tactical + STRIDE 显式跳过 + 跳过理由）
  - 起草 ADR-007（5 个 D：纯 shell / manifest 唯一权威 / 不依赖 jq / cursor vendor 路径 / post-install readme）
- Evidence Paths:
  - features/001-install-scripts/spec.md
  - features/001-install-scripts/spec-deferred.md
  - features/001-install-scripts/reviews/spec-review-2026-05-11.md
  - features/001-install-scripts/approvals/spec-approval-2026-05-11.md
  - features/001-install-scripts/design.md
  - docs/decisions/ADR-007-install-scripts-topology-and-manifest.md
- Session Log:
  - 2026-05-11 16:50Z: hf-workflow-router 路由到 hf-specify（full profile / auto / in-place），创建 feature 目录
  - 2026-05-11 16:55Z: hf-specify 完成 spec.md 起草，派发独立 reviewer subagent 执行 hf-spec-review
  - 2026-05-11 17:05Z: hf-spec-review v1 verdict = `需修改`（1 important + 6 minor）；记录在 `reviews/spec-review-2026-05-11.md`
  - 2026-05-11 17:10Z: hf-specify 定向回修——修正 NFR-004 与 NFR-003 阈值对齐、§6 列举 `--host`、§2 bash 兼容口径、FR-002 补 cursor symlink + both symlink acceptance、§3 trace 锚点修正、NFR-002 去 in-memory 实现细节、新增 ASM-001 处理非 git checkout 场景；派发 reviewer 复审
  - 2026-05-11 17:18Z: hf-spec-review Round 2 verdict = `通过`，无新 BLOCKER；auto mode 下父会话写 `approvals/spec-approval-2026-05-11.md`，进入 `hf-design`
  - 2026-05-11 17:35Z: hf-design 完成 design.md 起草 + ADR-007（5 个 D）；DDD strategic / tactical / STRIDE 显式跳过并附跳过理由（CLI 单脚本无业务概念 / 无安全 NFR）；Event Storming 按 full profile 给 Timeline + Process Modeling；准备派发 hf-design-review reviewer subagent
- Open Risks:
  - vendoring 后宿主仓库 `.cursor/rules/harness-flow.mdc` 中对 `skills/` 路径的相对引用是否仍能解析（这是 ADR-006 D2 修过的同源问题，脚本必须显式处理）—— 已在 spec FR-008 与 NFR-001 covered

## Optional Coordination Fields

- Task Board Path: N/A（任务量小，tasks.md 直承）
- Task Queue Notes:
- Workspace Isolation: in-place
- Worktree Path: /workspace
- Worktree Branch: cursor/install-scripts-c90e

## Next Step

- Next Action Or Recommended Skill: hf-design
- Blockers:
- Notes: spec approved，进入 design 节点；conditional ui-design 不激活（CLI-only，无 UI surface）；design 完成后派发独立 reviewer subagent 执行 hf-design-review

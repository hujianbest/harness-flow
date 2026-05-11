# Task Progress — 001-install-scripts

## Goal

- Goal: 为 HarnessFlow 增加可一键安装到任意宿主仓库的 install/uninstall 脚本，覆盖 Cursor 与 OpenCode 两种官方支持的客户端集成路径
- Owner: cursor agent
- Status: in-progress
- Last Updated: 2026-05-11

## Current Workflow State

- Current Stage: hf-specify
- Workflow Profile: full
- Execution Mode: auto
- Current Active Feature: features/001-install-scripts/
- Current Active Task:
- Pending Reviews And Gates: hf-spec-review
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
- Evidence Paths:
  - features/001-install-scripts/spec.md
  - features/001-install-scripts/spec-deferred.md
- Session Log:
  - 2026-05-11 16:50Z: hf-workflow-router 路由到 hf-specify（full profile / auto / in-place），创建 feature 目录
  - 2026-05-11 16:55Z: hf-specify 完成 spec.md 起草，准备派发独立 reviewer subagent 执行 hf-spec-review
- Open Risks:
  - vendoring 后宿主仓库 `.cursor/rules/harness-flow.mdc` 中对 `skills/` 路径的相对引用是否仍能解析（这是 ADR-006 D2 修过的同源问题，脚本必须显式处理）—— 已在 spec FR-008 与 NFR-001 covered

## Optional Coordination Fields

- Task Board Path: N/A（任务量小，tasks.md 直承）
- Task Queue Notes:
- Workspace Isolation: in-place
- Worktree Path: /workspace
- Worktree Branch: cursor/install-scripts-c90e

## Next Step

- Next Action Or Recommended Skill: hf-spec-review
- Blockers:
- Notes: spec 起草完成后立即派发独立 reviewer subagent

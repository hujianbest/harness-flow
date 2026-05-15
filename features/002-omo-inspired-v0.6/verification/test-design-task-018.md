# Test Design — TASK-018 (3-client install + fast-lane e2e)

- Task: TASK-018 (final v0.6 task)
- SUT Form: **`emergent`**
- Test Strategy: same-cloud-agent simulation per OQ-T1; install.sh + ls verification across 3 clients + fast-lane markdown-only path verification

## 待验证行为（TASK-018 Acceptance + NFR-004 + NFR-006 + HYP-002）

1. Cursor target install simulation：`install.sh --target cursor --host /tmp/host-cursor` 后 `find .cursor/harness-flow-skills -mindepth 2 -maxdepth 2 -name SKILL.md` 列出 4 + 7 改 = 11 个 v0.6 SKILL.md（含 4 新 + 7 改 + 18 既有 = 29 SKILL.md 全部）
2. OpenCode target install simulation：`install.sh --target opencode --host /tmp/host-opencode` 后 `find .opencode/skills -mindepth 2 -maxdepth 2 -name SKILL.md` 同上
3. Claude Code 通过 plugin 安装语义验证：检查 `.claude-plugin/marketplace.json` 不动 (NFR-003) + `find skills -mindepth 2 -maxdepth 2 -name SKILL.md` 在 vendoring 树根（HYP-004 假设：plugin install 拷贝 skills/ 全树）
4. fast-lane markdown-only e2e：本 feature 自身 17/18 task dogfood 即是 fast-lane e2e 全程；HYP-002 PASS evidence 已经分布在 progress.md `## Fast Lane Decisions` 段 23 行 audit trail（0 escape 触发 / 全自动推进 / Fagan 与 5 类不可压缩硬纪律保持）
5. evidence record：`verification/e2e-three-client-2026-05-15.md` + `verification/markdown-only-fast-lane-2026-05-15.md` 落盘

## 测试

- 一次性 shell + python 验证：实际跑 install.sh + find + grep
- HYP-002 验证：直接引用 progress.md `## Fast Lane Decisions` 段 + 12 测试套件 / 100 PASS 作为 markdown-only 路径足够的证据

## Approval

按 ADR-009 D2 fast lane auto approved。

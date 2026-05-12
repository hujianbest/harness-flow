# Design Approval — 001-install-scripts (2026-05-11)

- Feature: 001-install-scripts
- Design under approval: `features/001-install-scripts/design.md`
- ADR under approval: `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md`
- Review record: `features/001-install-scripts/reviews/design-review-2026-05-11.md`
- Reviewer verdict: 通过（Round 2，2026-05-11；维度评分 D1=8 / D2=8 / D3=9 / D4=9 / D5=8 / D6=9）
- Workflow Profile: full
- Execution Mode: auto

## Approval Decision

- Decision: **APPROVED**
- Approver: cursor cloud agent（auto mode）
- Approved at: 2026-05-11

## Rationale

Round 2 reviewer 复审确认 Round 1 的 2 important + 5 minor finding 全部在 design / ADR 层落实：

1. manifest entries 颗粒度：per-skill scheme 落实（约 25 条 dir entry 而非 1 条粗粒度）；ADR-007 D2 Alternatives A2 rationale 同步澄清"per-skill 颗粒度是必须"
2. rollback 闭合性：`set -Eeuo pipefail` + `mark_will_create` 预登记 + dir 类 `rm -rf` 三层 fix 完整
3. log/err/op 三函数职责分离
4. ADR-007 D5 readme 30 行 markdown sample 落到 design.md §13
5. set -E 显式约束 + rationale
6. mark_will_create 跳过 pre-existing dir（不误删用户原有 `.cursor/` / `.opencode/`）
7. test #10 grep 加 awk 注释剥离

reviewer 走查确认两个关键 scenario：
- **scenario #7**（HYP-002 Blocking 验证：user-skill 保留）：PASSable（per-skill manifest + leaf rm-rf / parent rmdir-only 区分）
- **scenario #12**（NFR-002 中途失败回滚）：PASS（set -Eeuo + mark_will_create 预登记 + rm -rf）

Round 2 提出的 3 条 R2 minor finding（apply_removal parent vs leaf 伪代码 / `.opencode` 父 dir 处理 / §3 traceability 函数名 stale）已在 approval 前一并 polish 修复：

- §3 traceability 表 FR-002 / FR-008 行函数名更新为 `vendor_skills_opencode()` / `vendor_cursor()`
- §10 component view 增"`apply_removal()` parent vs leaf 区分"段（约 15 行），落地 PARENT_DIRS hardcoded 列表
- mark_will_create 第 3 参数空/非空决定是否进 manifest 的语义显式写明

## Author / Reviewer Separation Verification

- Author（hf-design）: cursor cloud agent（父会话）
- Reviewer Round 1 + Round 2: 独立 reviewer subagent（agent ID `b5ea5bf1-69d8-4ca7-a780-32f033838e6f`）
- Approver: cursor cloud agent（父会话；auto mode）

符合 Fagan separation 立场。

## ADR Status Flip

- ADR-007 状态由 `proposed` 翻为 `accepted`（同步落到 `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md` 头部）

## Next Step

- Current Stage: `hf-design` → `hf-tasks`
- Pending Reviews And Gates: 移除 `hf-design-review`，加入 `hf-tasks-review`
- Workspace Isolation: in-place（tasks 阶段仍不动实现代码）
- conditional `hf-ui-design`：本 feature 不激活（CLI-only），无需联合 design approval

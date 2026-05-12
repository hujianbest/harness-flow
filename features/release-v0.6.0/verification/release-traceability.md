# Release-wide Traceability — v0.6.0

- Scope: 单候选 feature 聚合（按 ADR-008 D7 决策：单 candidate feature 时不重做单 feature traceability，只做版本级聚合）
- Profile: full
- Compiled at: 2026-05-12（hf-release §7 节点）

## 候选 Feature Traceability Verdict 聚合

| Feature ID | Traceability Verdict | Record Path | 备注 |
|---|---|---|---|
| `features/001-install-scripts/` | 通过（Round 2，2026-05-11；TZ1=9 / TZ2=8 / TZ3=9 / TZ4=8 / TZ5=9 / TZ6=9，全维度 ≥ 8/10）| `features/001-install-scripts/reviews/traceability-review.md` | spec FR-001..FR-008 + NFR-001..NFR-004 + ASM-001 全部 spec→design→tasks→impl→tests→verification 闭合；HYP-001..HYP-004 全部验证（HYP-002 Blocking 由 scenario #7 直接证据满足）；ADR-007 D1..D5 全部 manifested；DEF-001..DEF-007 全部确认未实现（无 scope creep）|

## 跨 Feature 风险盘点

- **跨 feature API 变化**：N/A（单候选 feature 无 cross-feature API 表面）
- **跨 feature 共享 contract**：N/A（install scripts 是仓库级入口，与既有 24 hf-* + using-hf-workflow 无 contract 共享）
- **跨 feature ADR 影响**：本版唯一新增 ADR 是 ADR-007（install scripts 5 决策）+ ADR-008（本版 release scope）；ADR-007 在 §11 Final Confirmation 通过时翻 accepted（已在 design-approval 阶段实际翻转，本 release 阶段补登 release pack ADR Status Flips 段）；ADR-008 在 §11 Final Confirmation 时翻 accepted。其他既有 ADR-001..ADR-006 全部 `accepted` 状态不变
- **跨 feature 工件污染**：本版引入的 `install.sh` + `uninstall.sh` + `tests/test_install_scripts.sh` 落仓库根；不进入任何 hf-* skill 的 4 类子目录约定（按 ADR-008 D8 决策），不触及 `skills/<name>/` 下任何工件；既有 `scripts/audit-skill-anatomy.py` + `scripts/test_audit_skill_anatomy.py` 不动；既有 `skills/hf-finalize/scripts/` 不动

## 与候选 feature 单 feature traceability 的关系

按 hf-release §7 立场：

- **不重做** 单 feature traceability—— 那是 `hf-traceability-review` 在 closeout 前已经做过的事（features/001-install-scripts/reviews/traceability-review.md Round 2 verdict 通过）
- **只做** 版本级聚合—— 把上述单 feature verdict 汇总 + 跨 feature 风险盘点
- **缺 verdict 的 feature**——若存在则按 profile 显式标 `N/A（按 profile 跳过）`；本版唯一候选 feature 已有 verdict，无 missing 项

## 结论

PASS。单候选 feature traceability 已满足 release-tier 入版条件；无跨 feature 风险阻塞。

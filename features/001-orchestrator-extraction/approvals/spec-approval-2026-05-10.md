# Spec Approval — features/001-orchestrator-extraction

- 批准对象:
  - Spec: `features/001-orchestrator-extraction/spec.md`
  - 配套 ADR: `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`
- Approval Step: post-`hf-spec-review`，pre-`hf-design`
- Execution Mode: auto（cloud agent 自治上下文；HF runtime authority "router § 8 关键分支：conclusion=通过 + needs_human_confirmation=true → auto 模式写 record 再继续"）
- Approval 时间: 2026-05-10
- Approver: HF Orchestrator (acting as parent session per workspace `harness-flow.mdc` always-applied rule, in cloud agent autonomous mode)

## 上游 Review Verdict

| 评审节点 | 结论 | Round | 路径 |
|---|---|---|---|
| `hf-discovery-review` | 通过（3 条 minor LLM-FIXABLE 已在 spec 阶段吸收） | 1 | `docs/reviews/discovery-review-hf-orchestrator-extraction.md` |
| `hf-spec-review` Round 1 | 需修改（2 条 important + 4 条 minor，全部 LLM-FIXABLE） | 1 | `features/001-orchestrator-extraction/reviews/spec-review-2026-05-10.md` § Round 1 |
| `hf-spec-review` Round 2 | **通过**（6 条 finding 全部正确修订；0 新 finding；regression 扫描 0 命中） | 2 | 同上 § "修订验证（Round 2）" |

## 批准依据

1. `hf-spec-review` Round 2 verdict = `通过`，0 残留 finding
2. `needs_human_confirmation=true` + Execution Mode = `auto` → 按 HF runtime authority 协议写 approval record 后自动继续（router § 8 关键分支）
3. 0 USER-INPUT findings → 无需用户裁决
4. spec § 6.2 12 项 out-of-scope 经 reviewer Round 1 + Round 2 双重核验未被静默引回
5. ADR-007 与 6 个先例 ADR（ADR-001 至 ADR-006）的关系表已逐项核验准确，含 ADR-004 D3 "关键先例" 延伸成立
6. release-blocking 假设（HYP-002 / HYP-003）已正确锚定到 ADR-007 D5（v0.6.0 release 前必须有 fresh evidence；spec 通过本身不要求已验证）

## 批准范围

**批准**：
- 进入 `hf-design` 阶段，针对本 spec § 6.1 in-scope 9 项与 ADR-007 D1–D7 锁定的架构 invariant 起草设计文档 `features/001-orchestrator-extraction/design.md`
- `hf-design` 阶段重点解决（reviewer Round 2 三点交接）：
  1. HYP-005 dispatch 协议设计（v0.7.0+ 目标态：不依赖 leaf 的 `Next Action` hint，纯靠 on-disk artifacts；兼容期允许同时消费 leaf 残留字段作为辅助）
  2. NFR-001 wall-clock baseline schema（baseline 与 candidate 测量口径、3 宿主同口径采集方式、`load-timing-3-clients.md` 数据 schema）
  3. FR-002 / FR-006 sub-ID 是否在 `hf-tasks` 阶段拆为独立任务的取舍依据
  4. OQ-N-003 regression-diff 脚本归属位置（`features/001-orchestrator-extraction/scripts/` vs `skills/hf-finalize/scripts/`）的最终决策

**不批准**（推迟到对应阶段）：
- 起草任何 leaf skill 的修改——spec § 6.2 / ADR-007 D3 Step 2-6 全部 out-of-scope
- 创建 `agents/hf-orchestrator.md` 文件——`hf-test-driven-dev` 阶段的工作
- 修改任何宿主 always-on stub 文件——同上
- v0.6.0 release pack 起草——`hf-release` 阶段，在 `hf-finalize` 通过后

## 下一步

- Next Action Or Recommended Skill: `hf-design`
- Workflow Profile: `full`（不变）
- Execution Mode: `auto`（不变；hf-design 阶段也按 auto 推进 review/gate）
- Workspace Isolation: `in-place`（不变；design 阶段仍是文档工件）
- Pending Reviews And Gates: `hf-design-review`（design 完成后派发）

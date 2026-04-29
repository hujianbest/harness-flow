# Spec Review — WriteOnce Walking Skeleton

- 节点: `hf-spec-review`
- Reviewer Role: Independent Reviewer (cursor agent in reviewer-only role)
- Date: 2026-04-29
- Artifact Under Review: `features/001-walking-skeleton/spec.md`

## Verdict

`通过`

## Checklist

| 检查项 | 结论 | 证据 |
|---|---|---|
| Spec 模板 14 节齐全 | ✅ | spec.md section 1–14 |
| Section 3 Success Metrics 每字段都填了 | ✅ | spec.md section 3 表格 |
| Section 4 Key Hypotheses 用表格 + ID + Type + Confidence + Validation Plan + Blocking? | ✅ | spec.md section 4 |
| 是否存在 Blocking 假设未验证 | ✅ 无 | spec.md section 4 末段 |
| FR 用 EARS + BDD + MoSCoW + Source 锚点 | ✅ | section 8 表格，6 条 FR 全部满足 |
| FR Source 锚点是否能找到上游证据 | ✅ | 每条 Source 列指向 HYP-X-N 或 spec section 编号 |
| 核心 NFR 用 QAS 五要素 + Response Measure 可判定 | ✅ | section 9 三条 NFR 均按 QAS 表达，Response Measure 含数字阈值或 0/100% 判定 |
| Section 6/7 范围内 vs 范围外是否一致 | ✅ | section 6/7 互补不冲突 |
| 是否暗藏越权（声明 release/ops 上线、声明真实集成） | ✅ 否 | section 7 显式排除 release/ops；section 11 约束禁止真实网络请求 |
| Discovery seed 是否被 spec 私自修改 | ✅ 否 | section 1/5/6 与 discovery section 0 seed 表完全一致 |
| 是否引用 spec-bridge 与 discovery 作为上游 | ✅ | spec.md "上游输入" 字段 |
| Profile 与 spec 密度是否一致 | ✅ | Profile = lightweight，section 3 给最小契约 + Leading/Lagging（略超 lightweight 最小要求，不阻塞） |

## Findings

无重大问题。小型观察：

1. NFR-Testability-1 的 Response Measure "E2E 测试 < 1 s" 是合理的紧约束，但 walking-skeleton 真要落到这个数字需要 parser/dispatcher 都不引入大依赖——`hf-design` 节点要在依赖选择上守住这一点。
2. FR-6 (`--to all`) 标 "Should"，意味着 walking-skeleton 落不到也不阻塞 spec=通过。这是合理的优先级设置：FR-1/FR-2/FR-3/FR-4 是 walking skeleton 的硬骨头，FR-6 是补丁。
3. Section 14 术语表只列 5 条很克制——如果 design 阶段要做 DDD 战略建模，术语表会扩展。

## Anti-Pattern Sweep

| 反模式 | 是否触发 | 备注 |
|---|---|---|
| FR 写成实现指令而不是可观察行为 | 否 | FR-1/FR-3/FR-4 都用"系统应当"+ Acceptance |
| NFR 用"足够快""合理"等无阈值口号 | 否 | 三条 NFR Response Measure 全部含数字 / 0 / 100% / 严格判定 |
| Spec 替 design 拍板技术方案 | ⚠️ 形式上 section 10 提到 commander/vitest 选择 | 但归为"外部接口与依赖"+ section 4 的 "F" 假设是已确认事实，且 section 10 写明"可换为 jest"，没有锁死方案。可接受。 |
| Spec 偷偷把 release/ops 引回来 | 否 | section 11 显式禁止真实网络 |
| Spec 中嵌入过多设计细节 | 否 | section 8/9 只描述行为，未规定模块边界 / 类名 / 文件名（CLI 子命令名属可观察行为，可接受）|

## Conclusion

- Conclusion: `通过`
- Next Action Or Recommended Skill: `hf-design`（spec 声明的 UI surface 不存在 → 不并行 `hf-ui-design`）
- 产出 approval：`approvals/spec-approval-2026-04-29.md`

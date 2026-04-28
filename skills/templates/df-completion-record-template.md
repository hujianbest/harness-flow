# df Completion Record

使用说明：

- 这是 `df-completion-gate` 的完成门禁记录模板。
- **默认保存路径：`features/<Work Item Id>-<slug>/completion.md`**
- 若项目在 `AGENTS.md` 中声明了等价路径或专用模板，优先遵循项目约定。

## Metadata

- Work Item Type:                          # AR / DTS / CHANGE
- Work Item ID:
- Owning Component:
- Workflow Profile:                        # standard / component-impact / hotfix / lightweight
- Date:
- Record Path:

## Upstream Evidence Bundle

| 工件 | 路径 | 状态 |
|---|---|---|
| Requirement / Spec | `requirement.md` | present / approved |
| Spec Review | `reviews/spec-review.md` | 通过 / 需修改 / 阻塞 |
| Component Design | `docs/component-design.md` | unchanged / updated / N/A |
| Component Design Review | `reviews/component-design-review.md` | 通过 / N/A |
| AR Design | `ar-design-draft.md` + `docs/ar-designs/AR<id>-<slug>.md` | approved |
| AR Design Review | `reviews/ar-design-review.md` | 通过 |
| Implementation Log | `implementation-log.md` | present |
| Test Evidence | `evidence/unit/`、`evidence/integration/` | present |
| Static Analysis Evidence | `evidence/static-analysis/` | present / N/A |
| Build Evidence | `evidence/build/` | present |
| Test Effectiveness Review | `reviews/test-check.md` | 通过 |
| Code Review | `reviews/code-review.md` | 通过 |

## Completion Claim

- Claim:                                   # 准备宣告什么完成了
- Scope:                                   # 本次完成覆盖的 AR 行为或 DTS 修复范围

## Verification Commands Run In This Round

```text
<command 1>
```

- Exit Code:
- Summary:

```text
<command 2>
```

- Exit Code:
- Summary:

## Freshness Anchor

- Commit / Build ID:
- 为什么这些证据属于当前最新代码状态:
- 大体量原始日志路径:                      # features/<id>/evidence/...

## Quality Risk Audit

- 嵌入式风险（内存 / 并发 / 实时性 / 资源生命周期 / 错误处理）:
- 已知 critical 静态分析 / 编译告警 / 编码规范违反:
- 未覆盖的 AR 行为或边界:
- SOA 边界 / 跨组件依赖风险:

## Verdict

- Conclusion: `通过` | `需修改` | `阻塞`
- Verdict Rationale:
- Next Action Or Recommended Skill:        # canonical df-* 节点：df-finalize / df-tdd-implementation / df-workflow-router 等
- reroute_via_router:                      # true / false

## Notes

- Limits / Open Items:

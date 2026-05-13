# Verification Record

使用说明：

- 这是通用验证记录模板，用于保存命令、结果摘要和结论。
- 可与当前 skill pack 中的 `hf-regression-gate` 或 `hf-completion-gate` 这类验证与完成门禁 skill 配合使用。
- **默认保存路径：`features/<active>/verification/<kind>-<scope>-YYYY-MM-DD.md`**（任务级 completion 用 `completion-task-NNN.md`，regression 通常按日期；hotfix 用 `hotfix-<topic>.md`）。
- 命令产生的原始日志、性能基线等大体量证据建议放到 `features/<active>/evidence/`，记录中通过相对路径引用。
- 若项目在 项目声明了等价路径，优先遵循项目约定。

## Metadata

- Verification Type:
- Scope:
- Date:
- Record Path:
- Worktree Path / Worktree Branch（若适用）:

## Upstream Evidence Consumed

- Implementation Handoff:
- Review / Gate Records:
- Task / Progress Anchors:

## Claim Being Verified

- Claim:

## Verification Scope

- Included Coverage:
- Uncovered Areas:

## Evidence Tier Coverage

| Tier | Required? | Evidence Provided | Status | Notes |
|---|---|---|---|---|
| mocked-unit |  |  | `covered` \| `N/A` \| `missing` |  |
| component-integration |  |  | `covered` \| `N/A` \| `missing` |  |
| api-contract |  |  | `covered` \| `N/A` \| `missing` |  |
| browser-runtime |  |  | `covered` \| `N/A` \| `missing` |  |
| full-stack-smoke |  |  | `covered` \| `N/A` \| `missing` |  |

## Runtime Evidence Consumed

- Browser Evidence:
- Console / Network Evidence:
- Health Check / Service Startup Evidence:

## UI Conformance Evidence（若适用）

- UI Contract Anchors:
- Screenshot Artifacts:
- Viewports Covered:
- DOM Anchors:
- Console / Network Assertions:
- Visual Drift / Token Bypass Check:
- Known UI Conformance Gaps:

## Contract Evidence Consumed

- API Contract / Schema:
- DTO / Fixture Alignment:
- API Base URL / Proxy / Env:

## Known Runtime Gaps

- Gaps:
- Downgrade Permission Source（若适用）:

## Commands And Results

```text
<command>
```

- Exit Code:
- Summary:
- Notable Output:

## Freshness Anchor

- Why this evidence is for the latest relevant code state:
- Output Log / Terminal / Artifact:

## Conclusion

- Conclusion: `通过` | `需修改` | `阻塞`
- Next Action Or Recommended Skill:

## Scope / Remaining Work Notes

- Remaining Task Decision（若适用）:
- Notes:

## Related Artifacts

- Related Artifacts:

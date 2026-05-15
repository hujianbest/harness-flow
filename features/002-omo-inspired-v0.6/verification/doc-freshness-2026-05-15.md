# Doc Freshness Gate — features/002-omo-inspired-v0.6 (2026-05-15)

- Gate: hf-doc-freshness-gate
- Verdict: **pass**
- Profile / Mode: full / auto
- Run-by: cursor cloud agent (按 Fagan separation)

## Sync-on-Presence Check Matrix

| 资产 | 状态 | 检查 |
|---|---|---|
| `CHANGELOG.md` `[Unreleased]` 段 v0.6 scope | ✅ present | grep `v0.6` 23+ matches；含 4 新 + 7 改 skill 完整列表 + dogfood 双层 + 12 测试套件等 |
| `README.md` "v0.6+ planned" → "out-of-scope per ADR-008 D1" 措辞 | ✅ updated 4 处 | `grep -E "out-of-scope.*ADR-008.*D1" README.md` → 4 lines |
| `README.zh-CN.md` 同款中文措辞 | ✅ updated 4 处 | `grep -nE "ADR-008.*D1.*显式 out-of-scope\|显式 out-of-scope.*ADR-008.*D1" README.zh-CN.md` → 4 lines |
| `docs/principles/soul.md` 现状脚注 | ✅ updated 1 处 | `grep -nE "ADR-008.*D1.*显式 out-of-scope" docs/principles/soul.md` → 1 line |
| `docs/principles/{methodology-coherence,skill-anatomy}.md` | ✅ unchanged (NFR：宪法层不变) | git diff origin/main 0 行 |
| `.claude-plugin/marketplace.json` | ✅ unchanged (NFR-003) | git diff 0 行 |
| `install.sh` / `uninstall.sh` / `.cursor/rules/harness-flow.mdc` | ✅ unchanged except PR #55 hotfix（与 v0.6 范围正交，已合入主线 + 本分支 merge） | git diff 0 行 vs origin/main excluding PR #55 merge |
| `docs/architecture.md` / `docs/arc42/` | ✅ N/A (项目档 0：未启用) | ls 不存在 |
| `docs/release-notes/` / `docs/runbooks/` / `docs/slo/` / `docs/diagrams/` | ✅ N/A (档 0/1：未启用) | ls 不存在；本 feature 不触发首次启用 |
| `features/002-omo-inspired-v0.6/closeout.md` `Release / Docs Sync` 字段 | ⏳ pending hf-finalize | 待 finalize 阶段对账 |

## Stale Wording Verification

| 旧表述 | 应不再出现 | 实际 |
|---|---|---|
| "v0.6+ planned hf-shipping-and-launch / etc." | 0 occurrences | `grep -E "v0.6\+ planned\|v0.6\+ 计划" README.md README.zh-CN.md docs/principles/soul.md` → 0 |
| "not yet implemented" (in `hf-shipping-and-launch` 上下文) | 0 occurrences | `grep "not yet implemented"` → 0 in soul.md (其它 README 段或为既有用途，不涉及本 v0.6 范围) |
| "23 个 hf-* skills" (stale 数字) | 0 occurrences in active sections | grep + 人工 review；既有 v0.5.1 历史 changelog 段中可能保留（属历史记录，不算 stale） |

## Verdict

**pass** — v0.6 文档刷新覆盖完整；CHANGELOG / README × 2 / soul.md 措辞统一为 "out-of-scope per ADR-008 D1 (永久 dropped, 不是 deferred)"；宪法层 + install topology + Claude Code marketplace plugin manifest 全部不动（按 NFR-003 / 灵魂文档约束）。

## 下一步

`hf-completion-gate`

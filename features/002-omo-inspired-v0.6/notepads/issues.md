# Issues — Feature 002-omo-inspired-v0.6

> 跨 task 累积，按 task 时间倒序追加。task 内遇到的非阻塞问题（阻塞问题走 problems.md）。

## TASK-003 — 2026-05-14T11:50Z — wisdom notebook 出现 6 条 entry-id 真重复（已修）

- entry-id: `iss-0002`
- author: cursor cloud agent (hf-test-driven-dev TASK-003)
- problem: TASK-002 closeout StrReplace 把已有 TASK-001 entries 重复进了新内容，导致 learnings.md 含 learn-0001/0002 各 2 次、decisions.md 含 dec-0001 2 次、verification.md 含 verify-0001/0002/0003 各 2 次 = 共 6 条真重复
- status: resolved
- discovered-at: 2026-05-14T11:48Z（TASK-003 GREEN 第一次跑 validator 自动发现）
- resolved-by: TASK-003 REFACTOR step 内重写 3 notepad 文件去重
- resolved-at: 2026-05-14T11:52Z
- workaround: 无（直接修复）
- 不进 problems.md 的原因：可在 task 触碰范围内安全清理（属于 hf-test-driven-dev SKILL.md 的"In-task Cleanups (Boy Scout + Opportunistic)"），不阻塞 fast lane；按 design §3.1 issues.md 的 status=resolved 不触发 escape

## TASK-003 — 2026-05-14T11:50Z — assertRegex 不接受 flags 参数（python 3.12）

- entry-id: `iss-0003`
- author: cursor cloud agent
- problem: TASK-003 测试中误用 `self.assertRegex(text, pattern, flags=re.IGNORECASE)`；python 3.12 unittest 的 assertRegex 不接受 flags 参数
- status: resolved
- discovered-at: 2026-05-14T11:51Z（TASK-003 GREEN 第一次跑 verifier 报 TypeError）
- resolved-by: TASK-003 GREEN-2 step 改用 `self.assertTrue(re.search(pattern, text, flags=re.IGNORECASE))`
- resolved-at: 2026-05-14T11:52Z
- workaround: 同上

## TASK-001 — 2026-05-13T13:55Z — tests/test_install_scripts.sh `--help` 不实现

- entry-id: `iss-0001`
- author: cursor cloud agent
- problem: 跑 sanity check 时发现 `tests/test_install_scripts.sh --help` 报 `[test] unknown arg: --help`，因为该脚本只接受 `--only=<scenarios>`
- status: deferred
- discovered-at: 2026-05-13T13:50Z (TASK-001 verification 时偶遇)
- workaround: 直接读源文件知道用法
- 为什么不在本 task 修：这是 features/001 留下的既有行为，与 TASK-001 范围无关；按"surgical changes"原则不顺手改

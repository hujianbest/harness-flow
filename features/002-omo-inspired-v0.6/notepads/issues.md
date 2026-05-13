# Issues — Feature 002-omo-inspired-v0.6

> 跨 task 累积，按 task 时间倒序追加。task 内遇到的非阻塞问题（阻塞问题走 problems.md）。

## TASK-001 — 2026-05-13T13:55Z — tests/test_install_scripts.sh `--help` 不实现

- entry-id: `iss-0001`
- author: cursor cloud agent
- problem: 跑 sanity check 时发现 `tests/test_install_scripts.sh --help` 报 `[test] unknown arg: --help`，因为该脚本只接受 `--only=<scenarios>`
- status: deferred
- discovered-at: 2026-05-13T13:50Z (TASK-001 verification 时偶遇)
- workaround: 直接读源文件知道用法
- 为什么不在本 task 修：这是 features/001 留下的既有行为，与 TASK-001 范围无关；按"surgical changes"原则不顺手改

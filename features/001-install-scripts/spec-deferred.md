# Spec Deferred Backlog — 001-install-scripts

本文件追踪 `spec.md §7 范围外内容` 中显式延后到后续增量的需求。每条都附"延后理由"与"何时回收的触发信号"。

| ID | 候选需求 | 延后理由 | 回收触发信号 |
|---|---|---|---|
| DEF-001 | Windows PowerShell `install.ps1` | HF v0.5.x 文档未承诺 Windows 一等支持；本轮 shell-only | 当 HF 客户端扩展到包含 Windows 用户为主的环境时回收 |
| DEF-002 | Claude Code 的 install 脚本 | Claude Code 走 `/plugin install` marketplace，无需 vendor 脚本 | 永不回收（除非 Claude Code 取消 marketplace 路径）|
| DEF-003 | `npx hf-install` Node 包发布 | 需要 npm publish 与 Node 依赖，违反本轮"无新增运行时依赖"约束 | 当用户调研显示 `npx` 入口需求高时回收，作为可选包装而非主入口 |
| DEF-004 | Global install 多版本共存 | 本轮只支持单版本覆盖式 global install | 当 HF 出现多个并行 maintained version 时回收 |
| DEF-005 | install 脚本对 `AGENTS.md` 的写入或 merge | 与 `docs/opencode-setup.md` "Why no AGENTS.md sidecar?" 一致；本轮永不动 `AGENTS.md` | 永不回收 |
| DEF-006 | install 脚本的 telemetry / 使用统计 | 隐私 / 体积 / 信任成本 | 永不回收 |
| DEF-007 | install 脚本调起 HF 自身 audit / lint | install 时跑 audit 会增加宿主机器依赖；audit 仍由 HF 自身 CI 跑 | 当 HF 提供 stdlib-only audit 入口时回收为可选 `--audit` flag |

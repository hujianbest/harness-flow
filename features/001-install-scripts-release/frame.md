# Install Scripts Release Frame

- 日期: 2026-07-07
- 意图: 为 Cursor 与 OpenCode 使用者提供可执行安装脚本，并准备一个包含该安装能力的 release 版本。
- 范围外: 不实现真实生产部署、监控、回滚；不新增非 Cursor/OpenCode 客户端支持。
- 风险档位: 2
- 档位理由: 新增对外安装能力并同步 release 元数据，属于常规新功能与发布面变更；不涉及数据迁移、安全认证或跨三模块结构调整。
- 环境基线: evidence/baseline-20260707T141156Z.log (exit 1)
- 基线说明: 运行 `python scripts/validate_skills.py && python -m unittest skills/hf-workflow/scripts/test_hf_gate.py`；当前失败于既有空目录 `skills/hf-closeout`、`skills/hf-quality-gate`、`skills/hf-spec` 缺少 `SKILL.md`，计划中先恢复基线。
- 假设: “发布 release 版本”指在仓库中完成版本号、CHANGELOG 与可发布状态准备；实际 GitHub tag/release 需要在用户确认后执行。

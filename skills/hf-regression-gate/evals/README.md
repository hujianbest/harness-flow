# Regression Gate 评测

## Protected Behavior Contracts

这些评测保护 `hf-regression-gate` 的以下行为契约：

1. **回归范围完整**：不只跑新增测试，必须覆盖受影响模块
2. **多维度回归**：构建失败也是回归信号，不因测试通过就忽略
3. **Fresh evidence**：不接受历史运行结果或口头声称
4. **Profile-aware 范围**：根据 profile 调整回归范围
5. **Coverage 守卫**：覆盖率低于项目级约定门槛是回归问题
6. **Worktree anchoring**：`worktree-active` 时 evidence 必须锚定同一 Worktree Path

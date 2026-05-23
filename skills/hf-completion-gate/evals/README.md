# 完成门禁评测

这个目录包含 `hf-completion-gate` 的评测 prompts。

## 目的

这些评测用于验证完成门禁是否真正做到：

- 只认最新验证证据
- 拒绝没有 fresh verification evidence 的完成宣告
- 在证据不足时回到 `hf-test-driven-dev`
- 正确区分“batch scope 完整后进入 finalize”与“回 router 处理剩余任务 / scope 冲突”
- batch scope 不完整、候选 next-ready task 不唯一时阻塞，而不是擅自替 router 拍板

## 建议评分关注点

1. 是否先明确要宣告的结论
2. 是否要求运行真正能证明该结论的命令
3. 是否在证据不足时拒绝通过
4. 是否正确处理 batch scope、剩余任务判断与唯一下一步

# 测试评审评测

这个目录包含 `hf-test-review` 的评测 prompts。

## 目的

这些评测用于验证测试评审是否真正做到：

- 判断 fail-first 有效性、行为覆盖、风险覆盖
- 防止浅层"绿测"冒充可信验证
- 给出明确 verdict 和唯一下一步
- 不在评审中修测试
- 在 route / stage / evidence 冲突时先做 precheck 阻塞
- 显式审查 acceptance 映射与 fresh RED/GREEN evidence

## 建议评分关注点

1. 是否基于 RED/GREEN 证据判断 fail-first 有效性
2. 是否检查已声明风险（项目缺陷模式 / 风险清单 / hotfix 历史）的覆盖
3. 是否给出唯一 canonical 下一步
4. 是否能指出 acceptance 映射或 stale evidence 缺口，而不是只给抽象意见

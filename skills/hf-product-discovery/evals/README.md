# 产品发现阶段评测

这个目录包含 `hf-product-discovery` 的评测 prompts。

## 目的

这些评测用于验证 discovery 节点是否真正做到：

- 先收敛问题、用户和 wedge，而不是直接写 spec
- 区分 confirmed facts、assumptions 和 later ideas
- 把 discovery 结果写成可交给 `hf-discovery-review` 的草稿

## Running

每条 eval 使用 `prompt` 模拟用户请求，用 `expectations` 描述必须满足的行为 contract。

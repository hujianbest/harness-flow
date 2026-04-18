# 产品发现阶段评测

这个目录包含 `hf-product-discovery` 的评测 prompts。

## 目的

这些评测用于验证 discovery 节点是否真正做到：

- 先收敛问题、用户和 wedge，而不是直接写 spec
- 区分 confirmed facts、assumptions 和 later ideas
- 把 discovery 结果写成可交给 `hf-discovery-review` 的草稿

## Running

每条 eval 使用 `prompt` 模拟用户请求，用 `expectations` 描述必须满足的行为 contract。


## Fixture-Backed Cases

部分评测会在 `files` 字段里附带真实 discovery 输入或 review 回修工件，用来模拟：

- 从零散 discovery notes 收敛成可评审 discovery 草稿
- 在 `hf-discovery-review` 打回后，只针对 findings 做定向回修

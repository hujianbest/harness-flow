# discovery review evals

## Protected Behavior Contracts

These evals protect the following behavioral contracts of `hf-discovery-review`:

1. Correctly refuses to pass discovery documents that still mix problem framing with feature dumping
2. Distinguishes facts from assumptions and later ideas
3. Requires an explicit bridge-to-spec section before allowing handoff to `hf-specify`
4. Distinguishes USER-INPUT from LLM-FIXABLE findings
5. Returns the correct next action (`hf-product-discovery`, `hf-specify`, or `hf-workflow-router`)

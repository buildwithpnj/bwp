# Sandboxed Plan Simulation & Preflight Checks

Describes virtual execution sandboxing and plan evaluation tests.

## 1. Dry Run Sandbox
- Runs steps against read-only mock models.
- Predicts missing dependencies, missing payloads parameters, or lock locks before live run.

## 2. Risk Scoring & Evals
- Calculates risk scores based on action policy tiers.
- Emits preflight warnings and success probability ratings.
- Graph visualizers overlay sandbox outcomes on start trigger nodes.

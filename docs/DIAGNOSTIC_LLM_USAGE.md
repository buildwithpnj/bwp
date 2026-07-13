# Diagnostic LLM Usage & Token Efficiency Policy

Defines cost-control thresholds for using LLM invocations during failure analysis.

## 1. Heuristics Gating
- The diagnostic engine MUST run lightweight heuristics before using LLM calls.
- If error signatures match known categories (Validation errors, Connection/Mock failures, Retry threshold exceeded), the heuristics provide deterministic causes and skip LLM execution.
- LLM is only triggered if patterns are ambiguous or unclassified.

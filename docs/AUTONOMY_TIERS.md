# Autonomy Tiers & Safety Levels

Governs the policy bounds of agentic capabilities in Warborn OS.

## Tier Classification

| Autonomy Tier | Safety Gate | Rules |
|---|---|---|
| **Tier 0** | Suggest-Only | Every action, regardless of risk, stops for user approval. |
| **Tier 1** | Controlled Single-Step | Auto-runs low-risk single-step actions. Pauses for high-risk actions. |
| **Tier 2** | Controlled Multi-Step | Runs low-risk multi-step plans. Pauses for approval if any step is high-risk. |
| **Tier 3** | Full Workflow | Runs workflows autonomously unless risky state changes occur. |

## Verification Checkpoint
All plans are validated via `PlanValidator` to reject cycles, unknown actions, or unauthorized combinations before execution.

# Multi-Agent Collaboration Framework

Allows multiple specialists to cooperate on complex execution failure traces.

## 1. Collaboration Orchestration
- Collaboration requests define the target run and participating agent list.
- Driven by `CollaborationOrchestrator` to step through agent inputs sequentially.
- No specialist is allowed to write changes directly to the database; they produce advisory findings returned to the orchestrator.
- High-risk branches or loops require explicit control checkpoints.

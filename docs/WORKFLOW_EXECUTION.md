# Multi-Step Workflow Orchestration

Handles compilation, validation, execution steps, and rollbacks.

## Execution Sequence

```mermaid
stateDiagram-v2
    [*] --> pending
    pending --> paused_approval : Checkpoint gate (step requires approval)
    paused_approval --> approved : Admin/User approves
    approved --> executing
    pending --> executing : Auto-approved
    executing --> executing : Next step
    executing --> succeeded : All steps complete
    executing --> failed : Step crashed -> Rollback
```

## Resumption & Rollback
- Resumes execution after approval via `WorkflowStateManager.approve_and_resume`.
- In case of failure at any step, `WorkflowExecutionService.rollback_workflow` triggers compensating rollbacks for previously succeeded steps.

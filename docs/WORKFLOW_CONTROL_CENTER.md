# Workflow Control Center

The control plane allows humans to pause, resume, cancel, or replay long-running agent workflows.

## Control Endpoints
- **Pause**: `POST /api/workflows/{id}/control` with payload `{"control_type": "pause_workflow"}`
- **Resume**: `POST /api/workflows/{id}/control` with payload `{"control_type": "resume_workflow"}`
- **Cancel**: `POST /api/workflows/{id}/control` with payload `{"control_type": "cancel_workflow"}`
- **Replay failed step**: `POST /api/workflows/{id}/control` with payload `{"control_type": "replay_failed_step", "step_index": idx}`

## State Transition Integrity
Workers check workflow status flags before executing steps. If a workflow is cancelled, execution halts immediately and triggers rollbacks.

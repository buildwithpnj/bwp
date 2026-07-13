# Implementation Plan - Warborn OS V0.50 Upgrade

This plan maps the structural changes, services, databases, tone standards, and execution modes required to bring Warborn OS actions and response layers to version 0.50 production-readiness.

## User Review Required

> [!IMPORTANT]
> **Action Registry & Persistence Guard**: Every action will require strict parameter type validation before database operations. Malformed or unverified actions will be truthfully rejected.
>
> **Host Header Rewrite Requirement**: To maintain live action reliability over ngrok tunnels, the local tunnel must be started using `--host-header=localhost` to prevent Ollama from rejecting cloud server queries with a 403 status code.

## Proposed Changes

---

### Component 1: Action Surface & Diagnostics
We will create tools to inspect supported actions, identify blocked execution points, and test end-to-end paths locally or live.

#### [NEW] [action_capability_audit_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_capability_audit_service.py)
- Evaluates live capabilities of registered actions, marking them as `working`, `blocked`, `unsupported`, or `non-professional`.

#### [NEW] [action_registry_inspector.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_registry_inspector.py)
- Scans `ActionRegistry` input schemas and logs discrepancies between schemas and executor signatures.

#### [NEW] [live_action_diagnostics_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/live_action_diagnostics_service.py)
- Exposes pingable tests to verify if the live cloud server can query the local Ollama tunnel endpoint successfully.

#### [NEW] [test_action_capability_audit.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/tests/test_action_capability_audit.py)
- Tests the surface capabilities auditor against mock capabilities.

---

### Component 2: Action Contract Hardening
We will enforce dynamic schema validation, transaction verification, and structured outcomes before success messages are presented.

#### [MODIFY] [action_registry.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_registry.py)
- Add required actions: `create_task`, `update_task`, `complete_task`, `create_project_item`, `update_project_item`, `create_calendar_event`, `create_memory_item`, `search_knowledge`, `get_recent_updates`.
- Map input schemas with standard Python type constraints.

#### [MODIFY] [action_contract_validator.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_contract_validator.py)
- Re-architect to validate payloads dynamically using `ActionRegistry.ACTIONS` type definitions rather than hardcoded validations.

#### [MODIFY] [action_result_verifier.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_result_verifier.py)
- Add verifiers for note creation, task updates, project item creation, calendar events, and memory inputs.

#### [NEW] [action_persistence_guard.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_persistence_guard.py)
- Verifies write restrictions (e.g. character limits, duplicate protection) before database commit phase.

#### [NEW] [test_action_contract_validator.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/tests/test_action_contract_validator.py)
#### [NEW] [test_action_result_verifier.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/tests/test_action_result_verifier.py)

---

### Component 3: Professional Response Layer
We will format outcome states to adhere strictly to mature, concise, clear, and non-toy product language.

#### [NEW] [action_response_formatter.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_response_formatter.py)
- Formats final assistant text into structured responses containing: `Status`, `Action`, `Result`, `Scope`, and `Next`.

#### [NEW] [copilot_response_style_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/copilot_response_style_service.py)
- Automatically filters out casual filler phrases (e.g. *"Done :)"*, *"Sure thing!"*).

#### [NEW] [user_facing_outcome_renderer.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/user_facing_outcome_renderer.py)
- Translates machine-readable result codes into human-readable workspace operations logs.

#### [NEW] [error_explanation_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/error_explanation_service.py)
- Maps db conflicts, validation errors, and timeout errors into professional error resolution paths.

---

### Component 4: Live Action Expansion & Database Models
We will add a new database model for project items and implement expansion action handlers.

#### [NEW] [project_item.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/models/project_item.py)
- SQLAlchemy model mapping projects table: `user_id`, `name`, `description`, `status`.

#### [NEW] [project_action_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/project_action_service.py)
- Implements `create_project_item` and `update_project_item` operations with tenant-scoping.

#### [NEW] [calendar_action_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/calendar_action_service.py)
- Implements `create_calendar_event` mapping to the `calendar_events` table.

#### [NEW] [memory_action_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/memory_action_service.py)
- Implements `create_memory_item` writing to `user_profile_memories`.

---

### Component 5: Live/Local Mode Split
Enables environment-aware execution routing (local synchronous vs. production asynchronous).

#### [NEW] [runtime_mode.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/config/runtime_mode.py)
- Enums: `LOCAL_SYNC`, `LIVE_SYNC`, `LIVE_ASYNC`, `HYBRID_SAFE`.

#### [NEW] [environment_action_mode_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/environment_action_mode_service.py)
- Selects the target execution mode dynamically from env configuration settings.

---

### Component 6: UI Result States (Next.js Frontend)
We will add structured visual result cards to the Copilot drawer.

#### [NEW] [ActionResultCard.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/components/copilot/ActionResultCard.tsx)
- Renders `Status`, `Action`, `Scope`, and `Result` inside a styled card.

#### [NEW] [ActionTimeline.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/components/copilot/ActionTimeline.tsx)
- Renders linear steps showing verification history.

---

### Component 7: Evals Sets
Evals to check and prove execution correctness.

#### [NEW] [v050_live_action_eval_set.json](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/evals/v050_live_action_eval_set.json)
- Validates prompt outputs for note, task, calendar, memory, and project item creations.

## Verification Plan

### Automated Tests
```powershell
# Run the entire action and contract test suite
pytest tests/test_action_contract_validator.py tests/test_action_result_verifier.py tests/test_action_capability_audit.py
```

### Manual Verification
1. Open the local dashboard and verify task creation, note updates, and memory additions appear on the UI immediately.
2. Verify live site routes messages through the ngrok tunnel without returning fallback answers.

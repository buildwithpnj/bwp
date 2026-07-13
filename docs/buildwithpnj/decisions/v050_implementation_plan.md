# Implementation Plan — Warborn OS V0.50 Full Copilot Control Plane & 50-Test Suite

This plan details the architecture, schemas, executors, policies, UI components, and evaluation tests to turn the Warborn OS Copilot into a verified, secure dashboard control plane.

## User Review Required

> [!IMPORTANT]
> **Dynamic Validation & Persistence Verification**: Actions will undergo automatic schema matching and active database persistence verifications. A success status will never be reported until the corresponding record is queried in Postgres.
> 
> **Elevated Gate & Destructive Audits**: All destructive actions (delete, archive, permanent purge) require explicit user confirmations and produce persistent audit trails.
> 
> **Explicit Live/Local Separation**: System command actions are blocked in LIVE mode and permitted only in LOCAL execution environments.

## Open Questions

1. **Admin Authorization Method**: Should Copilot use a custom headers check (`X-Admin-Token` or similar) or inspect the user role column in the DB? We propose checking the `role` property of the `User` model (`users.role == 'internal_admin'`).
2. **Rollback Coverage**: Are soft-deleted items stored in a global `Trash` table or marked with an `is_deleted` column per model? We propose adding a standard `deleted_at` timestamp or `is_deleted` flag to the tables.

## Proposed Changes

### Component 1: Registry and Policy Layer

#### [NEW] [copilot_action_registry.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/copilot_action_registry.py)
* Centralized dictionary mapping 56 dashboard actions across 15 modules.
* Defines Action Name, Module Name, Policy Tier, Input Schema, and Validator hooks.

#### [NEW] [action_policy_registry.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_policy_registry.py)
* Maps action policies: `safe_auto`, `confirm_first`, `admin_only`, `destructive_confirmed`, `read_only`.

#### [NEW] [action_schema_registry.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_schema_registry.py)
* Pydantic schemas validating input parameters for notes, tasks, books, storage, habits, calendar, and systems.

---

### Component 2: Execution and Verification Runtime

#### [MODIFY] [action_execution_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_execution_service.py)
* Reroutes all executor operations through a single, secure validation path.
* Runs verification checks to query database rows after write actions.

#### [NEW] [runtime_mode_router.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/runtime_mode_router.py)
* Dynamically decides if actions execute in live synchronous, local synchronous, or safe hybrid modes.

---

### Component 3: Module Executors

#### [NEW] [note_action_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/note_action_service.py)
* Manages `create_note`, `update_note`, `delete_note`, `restore_note`, and `search_notes`.

#### [NEW] [task_action_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/task_action_service.py)
* Manages task prioritizations, status updates, movement between projects, and trash-bin routing.

#### [NEW] [book_action_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/book_action_service.py)
* Manages book lists, readings updates, and archives.

#### [NEW] [habit_action_service.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/habit_action_service.py)
* Handles daily check-ins, routine lists, and completion tracking.

---

### Component 4: Professional Response Layer

#### [MODIFY] [action_response_formatter.py](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/api/app/services/action_response_formatter.py)
* Strictly formats response strings to use: `Status`, `Action`, `Result`, `Scope`, and `Next`.
* Eradicates casual helper phrases (e.g. "sure thing", "done :)").

---

### Component 5: Dashboard UI Control Feedback

#### [NEW] [ActionResultCard.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/components/copilot/ActionResultCard.tsx)
* Renders structured outcome badges (success, failed, blocked, needs_confirmation) in Next.js.

---

## Verification Plan

### Automated Tests
* We will write 50 end-to-end tests inside:
  * `tests/e2e/test_v050_full_control.py`
  * `tests/e2e/test_v050_destructive_control.py`
  * `tests/e2e/test_v050_mission_control.py`
* Running command:
  ```powershell
  pytest tests/e2e/test_v050_full_control.py tests/e2e/test_v050_destructive_control.py
  ```

### Manual Verification
1. Invoke note updates via the Copilot drawer.
2. Confirm the structured card is displayed and details match the Postgres database state.

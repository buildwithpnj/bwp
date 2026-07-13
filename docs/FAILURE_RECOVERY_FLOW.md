# Failure Classification & Recovery Flow

This document details how execution failures are diagnosed, categorized, and recovered.

## 1. Failure Classification

Every failure is mapped consistently to a standard type:
- `validation_failure`: Input payload does not match schema requirements.
- `permission_failure`: Role rights authorization checks failed.
- `approval_missing`: Triggered before manual review was obtained.
- `duplicate_blocked`: Blocked by `IdempotencyGuard` checks.
- `tool_disabled`: Action executor not found or disabled.
- `execution_exception`: An unhandled python crash inside execution logic.
- `partial_side_effect_failure`: Action succeeded but commit pipeline crashed.
- `timeout_failure`: Run exceeded execution safety limits (15 seconds).
- `persistence_failure`: Database integrity or lock crash occurred.

## 2. Retry Policy

- Auto-retry is enabled only for idempotent actions:
  - `create_followup_practice` (Max 3 retries, backoff)
  - `create_lesson_note` (Max 2 retries, backoff)
- Non-retryable actions will fail immediately and run rollback.

## 3. compensating Rollback Flow

If retries are exhausted or a partial failure is detected, the `ActionRollbackService` runs specific compensating actions:
- **`create_lesson_note`**: Deletes the created note by ID from database.
- **`save_corrected_example`**: Decrements the correction counter and streak count.
- **`mark_pattern_mastered`**: Removes the pattern from mastered skills array checklist.

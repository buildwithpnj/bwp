# Step Replay Policy

Explains how failed workflow items can be safely retried.

## Rules for Replay
1. **State Gate**: A step can only be replayed if the parent workflow run has a status of `failed`.
2. **Step Indices**: Replay can target any specific step index, resetting execution to that point and preserving the previous steps' success history.
3. **No Overwrites**: Replay runs through standard execution paths, updating timestamps and emitting events, maintaining full visibility and keeping DB state mutations audit-safe.

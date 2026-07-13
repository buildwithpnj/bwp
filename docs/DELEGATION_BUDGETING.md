# Delegation Budgeting & Recursion Guards

Details the budgeting metrics preventing agent loops.

## 1. Budgeting rules
- **Token Cap**: A session spends simulated tokens for each subagent execution (e.g. 1.0 or 1.5). Total budget cap is `15.0` tokens.
- **Recursion Guard**: Maximum delegation depth is capped at `2`. Attempts to trigger recursive subagents beyond this depth are blocked.
- **Domain Mismatches**: Requests to run subagents on unauthorized domains are rejected.

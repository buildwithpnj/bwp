# Adaptive Delegation Policy Tuning

Details outcome-driven feedback mechanisms adjusting agent delegation.

## 1. Usefulness Feedback
- Executed run outcomes are logged in `delegation_policy_feedbacks`.
- Usefulness score represents utility (0.0 for wasteful, 1.0 for highly useful).
- If average usefulness drops `< 0.3` (with count >= 2), the adaptive policy engine automatically blocks future queries to reduce latency and token spend.

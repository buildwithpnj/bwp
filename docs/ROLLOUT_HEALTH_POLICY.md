# Rollout Health Policy & Automated Rollbacks

Describes active telemetry delta health scoring.

## 1. Metric Evaluation
- Assesses failure rate delta and latency changes.
- Health drops below 0.5 if failure rate > 5%.

## 2. Auto-Rollback Safety
- Rollback trigger services automatically abort rollouts and reverse parameters if health scores drop below thresholds.

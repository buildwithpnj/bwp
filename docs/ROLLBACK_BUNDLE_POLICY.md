# Federated Rollback Bundle Policy

Describes pre-sync snapshot capture and rollback rules.

## 1. Snapshot Capture
- Before executing target sync events, rollback builders package current configurations into JSON string snapshots.

## 2. Reversion Execution
- Rollback executors retrieve matching snap records to restore states.

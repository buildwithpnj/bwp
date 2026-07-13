# Context Compaction & Token Budget Management

Describes historical logs compression minimizing prompt counts.

## 1. Rolling Compaction
- Compresses raw traces into text list summaries.
- Reduces token budget overhead without deleting raw canonical data records.

## 2. Rehydration
- Rehydrates and loads original canonical logs if deeper trace audits are requested.
- Budget checks warn if context exceeds thresholds.

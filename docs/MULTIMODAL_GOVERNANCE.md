# Multimodal Ingestion Governance

Describes per-tenant rate limit thresholds and storage quotas.

## 1. Sliding Rate Window
- sliding frequency checks verify upload request ceilings.
- Limits are checked per tenant or user.

## 2. Quota Restrictions
- Deducts daily byte allowances and request frequencies.
- Capped at 50 MB daily.
- Exceeding quotas blocks ingestion uploads immediately.

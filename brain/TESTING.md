# Testing Strategy & Verification Report

This document registers the test suites, verification scripts, and quality gates configured across the BuildWithPNJ monorepo.

---

## 1. Backend Integration Tests (Pytest)

The FastAPI backend contains a comprehensive mock test suite verifying the storage and failover layers under `apps/api/app/storage/test_storage.py`.

### Audited Scenarios
1. **Encryption Safety**: Tests that refresh tokens and client secrets are encrypted with AES Fernet keys before database write, and decrypt correctly on load.
2. **Priority-Based Category Routing**: Tests that files are automatically routed to the correct provider slot according to category mappings (e.g. `.pdf` to Drive A).
3. **Capacity Limit Failover**: Tests that if a drive's capacity exceeds 90%, uploads automatically fall back to alternate drives in the priority queue.
4. **API Exception Failover**: Tests that if a preferred drive client throws an HTTP error (timeout, revoked token), the upload recovers and succeeds on the fallback provider.

### Running Backend Tests
Execute the pytest package inside the API environment:
```bash
poetry run pytest apps/api/app/storage/test_storage.py
```
- **Results**: `6 passed in 0.87s`.

---

## 2. Frontend Build Verifications

To prevent layout regressions or type errors:
- **Build Checks**: We execute next builds before deployment staging:
  ```bash
  npm run build --workspace=apps/web
  ```
- **Prerender Audits**: Next.js compiles page routes statically. Any dynamic components (e.g. callback search param readers) are audited for `<Suspense>` wrapper boundaries.
- **Compiler Warnings Gates**: All source code components are audited for hook dependencies and state hoistings, ensuring `✓ Compiled successfully` contains 0 linter warnings.

---

## 3. Interactive Verification Checklist
- **Google OAuth Consent Flow**: Run `/auth/google/login` and verify that both Google Drive and Google Calendar permissions are requested on redirect.
- **Bi-Directional Calendar Sync**:
  1. Add event inside Warborn OS, verify it is cached in `calendar_events` and pushed to Google Calendar.
  2. Create event on Google Calendar client, pull events from dashboard, verify no duplicate items are created locally.
- **IP Locale Synchronization**: Verify dashboard clock displays local regional time (India timezone versus USA timezone) and active metrics load localized currency prefixes (`₹`, `$`) based on detected client IP.
- **Telemetry Loop Validation**: Verify the footer ribbon data packet traverses the 16 parallel nodes in a clockwise flow, highlighting each node and fading the trace cleanly within 1.5 seconds.


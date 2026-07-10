# Security Guidelines

## Security Verification Checklist

- [x] **Authentication & Session Validation**: Ensure routes in the `(app)` folder are protected by session checks.
- [x] **Secrets & Env Safety**: Confirm no database URLs, API tokens, or keys are committed to the git repository. Ensure `.env` is listed in `.gitignore`.
- [x] **Input Validation**: Sanitize variables passed to SQLAlchemy query builders.
- [x] **CORS Configuration**: FastAPI CORS middleware must only allow trusted origin configurations.
- [x] **OAuth Credentials Redaction**: Ensure secrets like authorization codes, tokens, and OAuth states are never logged to console or database.
- [x] **OAuth State Parameter Validation**: Protect against CSRF attacks in Google Drive OAuth flows by validating state tokens inside redirect callbacks.
- [x] **Fernet AES-256 Token Encryption**: Symmetric encryption applied to credentials before storage in database.
- [x] **Per-Provider Client Secret Encryption**: In addition to refresh tokens, the client secrets of individual Google OAuth applications (such as Provider B) are encrypted using Fernet AES-256 before database storage.
- [x] **Active Codebase Secrets Scan**: Completed global search scanning for exposed keys (e.g. Anthropic, Google API, database credentials), confirming zero keys are hardcoded in the codebase.

## Environmental Safeguards

- Database credentials and API ports are configured using template defaults (`POSTGRES_USER: personal_os`, `port: 8000`) and mapped inside `.env` configurations.
- Cryptographic Fernet keys are derived from raw `ENCRYPTION_KEY` hashes.

---

## Security Audit Report — 2026-07-10
* **Audit Results**: ✅ Passed
* **Items Audited**:
  - Tracked git files listing: Verified no `.env`, `.pem`, `.key`, or credentials files are tracked by Git.
  - `.gitignore` verification: Verified exclusions protect all environment configurations, database files, and private keys.
  - CORS configuration checks: Checked `main.py` CORS restrictions which strictly bind allow-origins to local origins and custom domain profiles.
  - Secret scanner checks: Verified no API keys (`sk-`, `AIza`) or database credentials are leaked inside staged or tracked files.


# Security Guidelines

## Security Verification Checklist

- [ ] **Authentication & Session Validation**: Ensure routes in the `(app)` folder are protected by session checks.
- [ ] **Secrets & Env Safety**: Confirm no database URLs, API tokens, or keys are committed to the git repository. Ensure `.env` is listed in `.gitignore`.
- [ ] **Input Validation**: Sanitize variables passed to SQLAlchemy query builders.
- [ ] **CORS Configuration**: FastAPI CORS middleware must only allow trusted origin configurations.

## Environmental Safeguards

- Database credentials and API ports are configured using template defaults (`POSTGRES_USER: personal_os`, `port: 8000`) and mapped inside `.env` configurations.

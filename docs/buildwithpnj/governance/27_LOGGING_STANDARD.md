# Logging Standard Spec (27_LOGGING_STANDARD.md)

This document establishes the structured logging guidelines, log level usage rules, and telemetry correlation schemas required across the **BuildWithPNJ** platform.

---

## 1. Structured Logging JSON Format

To enable automated log parsing and analysis (e.g. via Datadog or ELK Stack), all logs produced by backend services must output in structured JSON format:

```json
{
  "timestamp": "2026-07-04T09:25:00Z",
  "level": "ERROR",
  "service": "api",
  "traceId": "t892b17a-33c0-482a-a928-89cbb382902d",
  "path": "/api/v1/auth/login",
  "message": "Authentication failed: invalid password match",
  "context": {
    "userId": "u0e24177-3e11-4770-9883-8a3bb38f292d",
    "attempts": 3
  }
}
```

---

## 2. Severity Log Levels Guidelines

Engineers must choose the correct log level based on these criteria:

- **`DEBUG`**: Diagnostic information useful during development (e.g., raw SQL queries, incoming webhooks payloads). Excluded from production logs.
- **`INFO`**: Normal system operations (e.g., successful database migrations, new user registrations, newsletter subscriptions).
- **`WARNING`**: Non-critical issues that don't block operations but warrant attention (e.g., deprecated API requests, rate-limiting triggers).
- **`ERROR`**: Actionable errors that affect a specific request but don't bring down the system (e.g., failed payments, validation errors).
- **`CRITICAL`**: Severe system-wide failures that require immediate attention (e.g., database connection failure, Redis cache crash). Triggers developer alerts.

---

## 3. Tracing & Telemetry Correlation

To track requests across distributed backend calls:
1. **Trace ID Injection**: API middleware generates a unique `traceId` UUID for every incoming request.
2. **Propagating Traces**: The `traceId` is included in all downstream service logs and return payloads.
3. **Error Investigation**: If a request fails, the user is shown the corresponding `traceId`, allowing developers to locate all related logs quickly.
4. **Audit Logs**: Sensitive events (e.g., password resets, settings modifications, user deletions) are permanently written to an audit log table to track administrative actions.

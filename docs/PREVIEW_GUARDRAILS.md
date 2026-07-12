# Preview Guardrails

To prevent excessive token costs and pipeline abuse, a series of defensive barriers is built around the public preview endpoints.

## 1. Rate Limit Checks
* Target: `POST /api/public-preview/` endpoints.
* Rate: 10 requests per minute per IP address.
* Middleware: `PreviewRateLimitMiddleware` returns HTTP 429 when limits are breached.

## 2. Token Budget Caps
* Session limits: 2,000 tokens maximum per preview session.
* Daily limits: 50,000 tokens maximum global cap across all anonymous users.
* Handler: Checked in `PreviewGuardrails.check_limits()` and tracked inside `PreviewBudgetService`.

## 3. Scope Checks
* Allowed intents: `english_correction`, `rewrite`, `hinglish_to_english`, `explanation`.
* Any general agent requests or code assistance inputs are immediately blocked.

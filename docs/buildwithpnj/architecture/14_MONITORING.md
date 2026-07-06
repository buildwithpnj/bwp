# Monitoring, Telemetry, & Analytics Spec (14_MONITORING.md)

This document describes the observability framework, real-time error logging, and performance telemetry configured to capture runtime health on the **BuildWithPNJ** platform.

---

## 1. Observability Architecture

The monitoring framework is split into three main channels:

- **Error Tracking (Sentry)**: Captures client-side React hydration issues, Server Component errors, and API timeouts.
- **Web Vitals Telemetry (Vercel Analytics)**: Monitors real-time page speeds (LCP, FID, CLS) from real users.
- **Product Analytics (PostHog)**: Tracks visitor behavior, search queries in the command palette, and newsletter subscriptions.

---

## 2. Telemetry Collection Flow

Performance and usage metrics are sent to analytics engines via secure, non-blocking pipelines:

```
User Action / Load
     │
     ├─► Real-user Web Vitals ──────► Vercel Analytics (Edge Processing)
     │
     ├─► JavaScript Exception ──────► Sentry SDK (source maps resolved)
     │
     └─► Command Search Queries ────► Custom API Telemetry ──► Postgres
```

---

## 3. Custom Search Analytics Tracking

To understand what users are searching for and identify content gaps, the Command Palette sends search term triggers:
- When a search query matches 0 results, the client dispatches a telemetry payload:
  `POST /api/v1/telemetry/search-gap`
  ```json
  {
    "query": "voice assistant docker",
    "timestamp": "2026-07-04T09:20:00Z"
  }
  ```
- Analytics dashboards aggregate these inputs weekly, helping shape the roadmap for R&D Labs and the Engineering Journal.

---

## 4. Privacy & Compliance

All analytics capture adheres to modern privacy requirements:
- IP addresses are anonymized before storage.
- The system supports Do Not Track (DNT) header preferences, bypassing tracking scripts if set by the browser.

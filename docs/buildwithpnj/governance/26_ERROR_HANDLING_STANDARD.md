# Error Handling Standard (26_ERROR_HANDLING_STANDARD.md)

This document describes the unified error handling architecture, response payload formats, error boundary layouts, and offline fallback flows designed for the **BuildWithPNJ** platform.

---

## 1. Unified API Error Payload Format

All REST API errors returned by the FastAPI backend must conform to this JSON schema to enable consistent client parsing:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "The request contains invalid input parameters.",
    "details": [
      {
        "field": "email",
        "issue": "Format is invalid, must contain @ domain."
      }
    ],
    "timestamp": "2026-07-04T09:25:00Z"
  }
}
```

---

## 2. React Error Boundaries Layout

To prevent rendering crashes from bringing down the entire application, the frontend uses Next.js `error.tsx` boundary handlers:
- **Scope**: Boundaries are defined at the layout level for each major directory group (`(public)`, `(app)`).
- **Behavior**: If a sub-component crashes, the boundary catches the exception, logs it to Sentry, and renders a fallback UI:
  - Displays a clean error message.
  - Renders a **Reset Page** button to allow the user to retry the operation without reloading the browser.

---

## 3. Client Fallbacks & Offline Strategy

- **API Retries**: Network requests that fail due to temporary network issues are retried using React Query’s retry handler:
  - Retries up to **3 times** using **exponential backoff** (`1s`, `2s`, `4s` delays) before showing an error.
- **Offline States**: If a network request fails because the device is offline:
  - Display a top-bar banner: `⚠️ Connection lost. Running in offline preview mode.`
  - Direct read actions to load data from `localStorage` or IndexedDB caches.
  - Queue write mutations locally and sync them once connection is restored.

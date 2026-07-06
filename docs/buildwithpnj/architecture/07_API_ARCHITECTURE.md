# API Architecture Spec (07_API_ARCHITECTURE.md)

This document describes the API architecture, endpoints, and integration payloads for the **BuildWithPNJ** platform. The endpoints are exposed by the FastAPI (`apps/api`) backend.

---

## 1. REST API Routing Directory

All API paths are prefixed with `/api/v1` and utilize standard HTTP status codes:

### Authentication
- `POST /api/v1/auth/register`: Register user credentials. Returns JWT cookie.
- `POST /api/v1/auth/login`: Authenticate email and password.
- `POST /api/v1/auth/logout`: Revoke active authentication cookies.

### Content Telemetry & Metadata
- `GET /api/v1/projects`: Retrieve lists of active and complete project files.
- `GET /api/v1/labs`: Retrieve R&D experiments.
- `GET /api/v1/journal`: Retrieve article indexing.

### Command & Mission Control
- `GET /api/v1/telemetry`: Retrieves aggregated real-time dashboard data (Commits, Streaks, active system loads).
- `POST /api/v1/newsletter/subscribe`: Add new email address to database.

---

## 2. API Request & Response Payload Examples

### Newsletter Subscription
`POST /api/v1/newsletter/subscribe`
- **Request Payload**:
  ```json
  {
    "email": "developer@buildwithpnj.com"
  }
  ```
- **Response Payload (201 Created)**:
  ```json
  {
    "success": true,
    "message": "Subscription confirmed. Email added to mailing list.",
    "subscriber": {
      "id": "e0e24177-3e11-4770-9883-8a3bb38f292d",
      "email": "developer@buildwithpnj.com",
      "createdAt": "2026-07-04T09:18:00Z"
    }
  }
  ```
- **Error Response (422 Unprocessable Entity)**:
  ```json
  {
    "detail": [
      {
        "loc": ["body", "email"],
        "msg": "value is not a valid email address",
        "type": "value_error.email"
      }
    ]
  }
  ```

---

## 3. Webhook Integrations

- **GitHub Integrations**:
  - Expose `POST /api/v1/webhooks/github` endpoint to listen to repository events.
  - GitHub sends signature tokens in the `X-Hub-Signature-256` header.
  - When verified, the API updates database metrics, keeping the Commits and Day Streak counters on the Mission Control dashboard in sync.

---

## 4. Future AI Orchestrator API Layout

As the dashboard transitions to local AI operations, the backend will expose a streaming websocket endpoint:
- **`WS /api/v1/ai/agent-chat`**:
  - Establishes a permanent WebSocket connection.
  - Passes prompt context, active file selections, and system diagnostics.
  - Stream-returns LLM output chunks token-by-token using SSE (Server-Sent Events) to minimize perceived screen delays.

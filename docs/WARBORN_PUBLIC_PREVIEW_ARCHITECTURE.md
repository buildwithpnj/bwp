# Warborn Public Preview Architecture

This document maps out the public/private separation model between the authenticated Warborn OS system and the restricted public agentEnglish preview.

## Architecture Diagram

```mermaid
graph TD
    User[Anonymous User] --> Landing["/warborn (Public Page)"]
    User --> Sandbox["/warborn/preview (Public Preview Sandbox)"]
    Sandbox --> API_Public["POST /api/public-preview/respond"]
    API_Public --> Guardrails[PreviewGuardrails]
    Guardrails --> Budget[PreviewBudgetService]
    Guardrails --> Agent_Run["agentEnglish Runtime (is_preview=True)"]
    
    Auth_User[Logged-In User] --> Auth_App["/warborn/app (Protected Route)"]
    Auth_App --> API_Auth["POST /api/warborn/chat"]
    API_Auth --> Agent_Run_Full["agentEnglish Runtime (is_preview=False)"]
```

## Key Isolation Boundaries
1. **Public rate limit constraints**: Anonymous users are throttled to 10 requests per minute by the `PreviewRateLimitMiddleware`.
2. **Preview session caps**: Limit of 5 turns per session, tracked strictly via the in-memory `PreviewBudgetService`.
3. **Intent limitations**: Restricts agent queries only to English correction, rephrasing, Hinglish explanation, and translation. All other queries are blocked by `classify_intent` in the agent runtime.
4. **Tenant-Safe separation**: Private logs, credentials database connection, and storage operations are completely hidden from anonymous preview users.

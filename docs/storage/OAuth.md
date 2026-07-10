# OAuth Flow Specification — Warborn OS

This document explains the OAuth 2.0 connection and refresh process for storage providers.

## Connection Flow Chart

```mermaid
sequenceDiagram
    participant User as OS User
    participant API as FastAPI Backend
    participant Google as Google Consent Server
    participant DB as Postgres Table

    User->>API: Click "Connect Drive" (/api/storage/auth/google/login)
    API-->>User: Return redirection authorization URL
    User->>Google: Grant permissions to offline Drive access
    Google-->>User: Redirect back with Auth Code
    User->>API: Forward Auth Code (/api/storage/auth/google/callback)
    API->>Google: Exchange Auth Code for Access + Refresh Tokens
    Google-->>API: Return tokens (Access, Refresh)
    API->>Google: Fetch account email address
    API->>API: Encrypt Refresh Token using Fernet
    API->>DB: Save Provider record (name, type, email, encrypted token)
    API-->>User: Return connection success metadata
```

## Token Storage Security

- Client secret and client ID are loaded directly from the system environment.
- The authorization code is used once to obtain token sets and never cached.
- The returned refresh token is encrypted with the `ENCRYPTION_KEY` using **Fernet (symmetric AES-128)** before writing to the `storage_providers` database.
- Future access uses the refresh token to dynamically retrieve access tokens.

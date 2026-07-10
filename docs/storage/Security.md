# Security Audit Guidelines — Warborn OS

This document details the security safeguards built into the storage manager subsystem.

## Safeguards Implemented

- **No Hardcoded Secrets**: Client IDs, client secrets, and refresh tokens are kept strictly outside the code.
- **Symmetric Encryption**: Refresh tokens are encrypted with `cryptography.fernet` using base64 AES keys before they are stored in the database.
- **Log Sanitization**: All log statements inside `app/storage` are reviewed to ensure that access tokens, refresh tokens, auth codes, and client secrets are never printed.
- **Temporary Authorization Codes**: Google auth codes are exchanged immediately inside callbacks and never persisted in database tables or logs.
- **Frontend Isolation**: Frontend API responses only expose safe provider metadata (emails, status, and usage bytes). The encrypted tokens are never sent to client devices.

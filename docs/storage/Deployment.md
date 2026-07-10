# Deployment Guidelines — Warborn OS

This document explains deployment guidelines for the storage provider module.

## Database Migrations

- The database migrations are managed using Alembic.
- Before deploying the API, execute the database migration to create the `storage_providers` table:
  ```bash
  alembic upgrade head
  ```
- Startup lifespans inside `app/main.py` automatically run these migrations on backend boot.

## Environment Variables

Ensure that your deployment environment has the following variables set inside system container configurations:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`
- `ENCRYPTION_KEY`
- `DATABASE_URL`
- `REDIS_URL`

For staging/production environments, generate a unique 32-byte key string for `ENCRYPTION_KEY`.

---
title: "Setting up Alembic migrations in Turborepo docker setups"
excerpt: "How to automate database schema updates alongside package builds inside container environments."
publishDate: "2026-07-10"
tags: ["postgresql", "docker", "architecture"]
featured: false
draft: false
---

Automating database schema updates prevents configuration drift between local development and staging environments. We use Alembic inside our FastAPI Docker setup to manage this automatically.

## Migration Hook

```yaml
services:
  api:
    command: sh -c "alembic upgrade head && uvicorn app.main:app"
```

This ensures that database updates execute before the application server accepts client connections.

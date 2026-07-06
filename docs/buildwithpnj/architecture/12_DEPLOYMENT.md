# Deployment & Infrastructure Spec (12_DEPLOYMENT.md)

This document describes the environment matrix, CI/CD pipeline structures, and rollback workflows for the **BuildWithPNJ** platform.

---

## 1. Hosting Architecture

The platform uses a unified edge hosting layout:
- **Frontend App (`apps/web`)**: Deployed to **Vercel** to take advantage of Edge Caching, instant preview branches, and global CDN caching.
- **Backend API (`apps/api`)**: Deployed to **Render** or a lightweight **Docker** container on an AWS EC2 instance.
- **Database (Supabase)**: Managed relational PostgreSQL instance.

---

## 2. Environment Configuration Matrix

| Environment | Branch | Target Host | Purpose |
| :--- | :--- | :--- | :--- |
| **Production** | `main` | `buildwithpnj.com` | Production-grade customer traffic. |
| **Staging** | `release/*` | `staging.buildwithpnj.com` | Release candidate testing, integration checks. |
| **Preview** | All pull requests | Dynamic Vercel URLs | Visual review and QA validation. |
| **Development**| Local machine | `localhost:3000` | Active feature design and local writing. |

---

## 3. GitHub Actions CI/CD Pipeline

Every pull request initiates a verification build to prevent compile errors from entering the main branch:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Lint
        run: npm run lint

      - name: Run Tests
        run: npm run test

      - name: Compile Next.js Build
        run: npm run build --workspace=apps/web
```

---

## 4. Rollback & Failover Systems

- **Instant Rollback**: If a bad build makes it to production, Vercel allows instant rollbacks to the last stable deployment hash via a single button click in the dashboard.
- **DB Backups**: Supabase performs daily logical database backups. A backup retention window of 7 days is configured to secure user data.

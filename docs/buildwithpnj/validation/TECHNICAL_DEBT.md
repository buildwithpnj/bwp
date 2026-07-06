# Technical Debt Registry (TECHNICAL_DEBT.md)

This document tracks technical debt, architecture trade-offs, and scaling limits identified across the **BuildWithPNJ** codebase.

---

## 1. Active Technical Debt Items

### Debt Item 01: File-Based Markdown CMS Setup
- **Context**: Content (projects, articles, labs) is parsed from markdown files stored in the workspace using `gray-matter`.
- **Debt Level**: Medium.
- **Trade-off**: Saves the complexity of setting up a headless CMS, but limits content creation and increases page rebuild times at scale.
- **Scaling Limit**: When content exceeds 500 files, disk reading latencies will degrade static page generation times.
- **Remediation Plan**: Transition to a database or a headless CMS (like Sanity or Strapi) in Phase 6.

### Debt Item 02: Concurrent Dev Server Setup (Next.js + FastAPI)
- **Context**: The project runs two separate dev servers (Next.js Node server and FastAPI Python server).
- **Debt Level**: Low.
- **Trade-off**: Provides flexibility to choose the best language for each layer, but increases configuration complexity.
- **Remediation Plan**: Document setup scripts in the project README to simplify developer onboarding.

### Debt Item 03: Manual Database Schema Sync
- **Context**: Database updates are pushed using `npx prisma db push`.
- **Debt Level**: Medium.
- **Trade-off**: Fast for prototyping, but lacks tracking for database migrations.
- **Remediation Plan**: Switch to standard Prisma migration scripts (`npx prisma migrate dev`) for future updates.

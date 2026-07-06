---
title: "Personal OS: The Warborn OS Subsystem"
tagline: "An integrated developer dashboard managing notes, habits, financial transactions, and local AI prompts."
status: "active"
featured: true
thumbnail: "/images/projects/personal-os.png"
techStack: ["nextjs", "fastapi", "supabase", "typescript", "python"]
category: "saas"
startDate: "2026-06-01"
publishDate: "2026-07-04"
timeline: ["Sprint 1: DB Schema & Auth Configuration", "Sprint 2: Workspace layouts & local UI states", "Sprint 3: Notes & habits sync controllers"]
challenges: 
  - title: "OAuth Sync Conflicts"
    content: "Handling concurrent sync mutations between local note drafts and remote GDrive versions required timestamp reconciliation logic."
  - title: "Database security isolation"
    content: "Securing user workspaces required configuring Row-Level Security (RLS) policies matching authenticated session tokens."
---

## Problem
Developers often use fragmented applications to manage notes, checklists, budgets, and API prompt testing. This causes context-switching delays and data fragmentation across third-party services.

## Solution
We built an integrated workspace dashboard (Warborn OS) nested inside a unified Next.js monorepo. It connects note-taking, habit trackers, and local AI workspaces through a single session authentication model.

## Architecture

```
  Next.js 15 Client (Zustand & React Query)
                 │
                 ▼
  FastAPI Backend (SQLAlchemy / Alembic)
                 │
                 ▼
  PostgreSQL Database (Supabase with RLS)
```

## Technical Decisions
- **Next.js & React 19**: Chosen to support both static marketing pages and the dynamic, authenticated developer dashboard.
- **FastAPI (Python)**: Handles compute-intensive operations, file parsing, and integrations with Python-first AI frameworks.
- **Prisma & Alembic**: Manages database migrations across the monorepo cleanly.

## Results
- First-load JS weight optimized to **103 kB** (under the 120 kB ceiling).
- Workspace action response times reduced to under **50ms** using optimistic state updates.
- Centralized all developer tracking metrics into a single, secure database.

## Future Roadmap
- Local vector search integration for notes using `pgvector`.
- Automated script runner tracking.
- WebRTC voice interfaces for prompt evaluations.

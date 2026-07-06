# BuildWithPNJ — Project Overview

> **The headquarters of an AI-first personal engineering brand.**

---

## 1. What Is BuildWithPNJ?

**BuildWithPNJ** is the personal AI engineering brand of Prakash (PNJ). It represents a public builder identity focused on shipping real, production-grade AI-powered tools and products — then sharing the journey openly.

The brand sits at the intersection of **AI engineering**, **full-stack development**, and **builder culture**. Everything produced under this banner — from open-source tools to SaaS products to educational content — flows through this workspace.

---

## 2. Mission & Vision

| | Statement |
|---|---|
| **Mission** | Build premium AI-powered tools that solve real problems, and document the journey so others can learn and build alongside me. |
| **Vision** | Become a recognized name in the AI engineering space — known for shipping fast, building in public, and creating tools people actually use. |

---

## 3. What Exists Today

### 3.1 Personal OS (Flagship Product — In Progress)

A production-grade, single-user personal operating system designed to replace Notion, YNAB, Readwise, and spreadsheet sprawl. Built for power users and AI agents alike.

| Component | Technology | Status |
|---|---|---|
| **Frontend** | Next.js 15, shadcn/ui, Tailwind CSS, TanStack Query, Zustand, cmdk | 🟢 Active |
| **Backend** | FastAPI, SQLAlchemy 2.0 (async), Alembic, Celery | 🟢 Active |
| **Database** | PostgreSQL 16 + pgvector | 🟢 Active |
| **Cache & Queue** | Redis 7 | 🟢 Active |
| **Auth** | JWT (argon2) | 🟢 Active |
| **Infra** | Docker Compose (local dev) | 🟢 Active |

#### Current Modules

| Module | Route | Description |
|---|---|---|
| Dashboard | `/` | Unified home with financial summaries, habits, and quick actions |
| Finance | `/finance` | Accounts, transactions, budgets, categories |
| Books | `/books` | Reading tracker with Google Drive sync |
| Habits & Journal | `/habits` | Habit tracking and daily journaling |
| Notes | `/notes` | Personal knowledge base |
| Storage | `/storage` | File management |
| Tools Builder | `/tools` | Custom tool creation workspace |
| Agent Inbox | `/agent-inbox` | AI agent task inbox |
| Auth | `/login`, `/register` | JWT-based authentication |

#### Key Backend APIs

- `auth` — Registration, login, JWT token management
- `dashboard` — Aggregated metrics and widget data
- `accounts` / `transactions` / `budgets` / `categories` — Full finance stack
- `books` — Reading list CRUD with Google Drive integration
- `habits` — Habit tracking, streaks, journal entries
- `notes` — Markdown notes with tagging
- `gdrive` — Google Drive sync engine

---

## 4. Repository Structure

```
My dashboard/                          ← Workspace root (BuildWithPNJ HQ)
├── apps/
│   ├── api/                           ← FastAPI backend (Python 3.12)
│   │   ├── app/
│   │   │   ├── models/                ← SQLAlchemy ORM models
│   │   │   ├── routers/               ← API route handlers
│   │   │   ├── schemas/               ← Pydantic request/response schemas
│   │   │   ├── main.py                ← FastAPI app entrypoint
│   │   │   ├── config.py              ← Settings & env vars
│   │   │   ├── database.py            ← Async DB engine & session
│   │   │   ├── deps.py                ← Dependency injection
│   │   │   ├── celery_app.py          ← Celery worker config
│   │   │   ├── tasks.py               ← Background tasks
│   │   │   └── gdrive_sync.py         ← Google Drive sync engine
│   │   ├── alembic/                   ← Database migrations
│   │   ├── seed.py                    ← Test data seeder
│   │   └── pyproject.toml             ← Python package config
│   └── web/                           ← Next.js 15 frontend (TypeScript)
│       └── src/
│           ├── app/                   ← App Router pages
│           │   ├── (app)/             ← Authenticated app routes
│           │   └── (auth)/            ← Login & registration
│           ├── components/            ← React components
│           ├── hooks/                 ← Custom React hooks
│           └── lib/                   ← Utilities & API client
├── packages/
│   └── shared-types/                  ← Shared TypeScript type definitions
├── brand/                             ← 🆕 Brand assets & guidelines
│   └── assets/
│       ├── logos/                     ← Logo files (SVG, PNG, ICO)
│       ├── fonts/                     ← Custom typography
│       └── social/                    ← Social media templates
├── content/                           ← 🆕 Content pipeline
│   ├── blog/                          ← Blog posts & drafts
│   └── case-studies/                  ← Portfolio write-ups
├── docs/                              ← 🆕 Internal documentation
├── my brand PNJ/                      ← Legacy brand folder (empty)
├── docker-compose.yml                 ← Postgres + Redis local stack
├── turbo.json                         ← Turborepo pipeline config
├── package.json                       ← Workspace root config
├── PROJECT_OVERVIEW.md                ← 📍 You are here
├── ROADMAP.md                         ← Strategic roadmap & milestones
├── BRAND_GUIDELINES.md                ← Visual & voice identity guide
├── WEBSITE_PRD.md                     ← Brand website PRD
├── TASKS.md                           ← Active task tracker
└── CHANGELOG.md                       ← Version history
```

---

## 5. Monorepo Architecture

This workspace is a **Turborepo monorepo** with npm workspaces:

- **`apps/web`** — Next.js 15 frontend (primary UI)
- **`apps/api`** — FastAPI backend (not in npm workspaces, managed via Python tooling)
- **`packages/shared-types`** — Shared TypeScript types between packages

Pipeline tasks (`turbo.json`): `dev`, `build`, `lint`

---

## 6. Development Workflow

| Step | Command | Notes |
|---|---|---|
| Install deps | `npm install` | Root workspace |
| Start infra | `docker compose up -d` | Postgres 16 + Redis 7 |
| Start API | `npm run dev:api` | Port 8000, Swagger at `/docs` |
| Start frontend | `npm run dev:web` | Port 3000 |
| Start everything | `npm run dev` | Turbo parallel |
| Run migrations | `npm run db:migrate` | Alembic upgrade head |
| Seed test data | `cd apps/api && python seed.py` | test@example.com / password123 |

---

## 7. License

- **Personal OS codebase**: MIT License — Copyright (c) 2026 buildwithpnj
- **Brand assets**: All rights reserved

---

## 8. Key Links

| Resource | URL |
|---|---|
| GitHub | `github.com/buildwithpnj` |
| Brand Website | _Coming soon_ (see [WEBSITE_PRD.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/WEBSITE_PRD.md)) |
| Roadmap | [ROADMAP.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/ROADMAP.md) |
| Brand Guide | [BRAND_GUIDELINES.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/BRAND_GUIDELINES.md) |
| Tasks | [TASKS.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/TASKS.md) |
| Changelog | [CHANGELOG.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/CHANGELOG.md) |

---

*Last updated: 2026-07-04*

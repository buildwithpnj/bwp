# Current State

*Last Updated: 2026-07-10 19:15:00 UTC*

## Active Workspace & Servers

- **Next.js Web Client**: [http://localhost:3000](http://localhost:3000) (Running, ready in dev mode)
- **FastAPI Python Backend**: [http://127.0.0.1:8000](http://127.0.0.1:8000) (Running with active hot reload)
- **Backing Databases**: PostgreSQL (Port 5432) with Alembic migration state fully applied.

## Tech Stack Summary

- **Frontend**: Next.js 15.5.20 (App Router), React 19, Tailwind CSS (Utility Styling), Lucide Icons, next-themes.
- **Backend**: FastAPI, Async SQLAlchemy, PostgreSQL with `pgvector` extension, Alembic Migrations.
- **Tooling**: Turborepo, npm workspaces, TypeScript.

## Latest Visual Integration status

### 1. Life OS Integration (Phase 3 Upgrade)
- **Habits Engine Restored & Upgraded**: Splits habits by morning/evening routines and cadence, tracking custom difficulty, priority, and durations. Features visual daily streak multipliers.
- **Quit Addiction Sobriety Manager**: Dashboard tracks sobriety tickers, reclaimed hours/money, triggers, and relapse event logs.
- **Google Calendar Sync**: Full bi-directional event mapping syncing local database items to Google Calendar using timezone parameters and token caching.
- **AI Coach Insights**: Audits logged user wellness logs to generate daily coach reports.
- **Mission Control Redesign**: Consolidated Today's Habits checklist, event schedules, recovery streaks, and AI assistant advice into the cockpit dashboard.

### 2. Multi-Provider Google Drive Integration (Phase 2)
- **Multi-Provider Architecture**: Upgraded to support multiple Google Drive accounts with independent OAuth project configs (`client_id`, encrypted `client_secret`, and `redirect_uri` stored per provider).
- **Auto Failover**: If the preferred drive encounters a connection or API error, the Storage Manager uploads the file to the next active, non-full drive in the priority queue.

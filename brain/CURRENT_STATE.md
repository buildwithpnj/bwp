# Current State

*Last Updated: 2026-07-10 15:20:00 UTC*

## Active Workspace & Servers

- **Next.js Web Client**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Python Backend**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Backing Databases**: PostgreSQL (Port 5432) and Redis (Port 6379) managed via Docker Compose.

## Tech Stack Summary

- **Frontend**: Next.js 15.5.20 (App Router), React 19, Tailwind CSS (Utility Styling), Lucide Icons, next-themes.
- **Backend**: FastAPI, Async SQLAlchemy, PostgreSQL with `pgvector` extension, Alembic Migrations, Redis caching.
- **Tooling**: Turborepo, npm workspaces, TypeScript.

## Latest Visual Integration status

### 1. Refined Navigation Bar
- Seamlessly synchronized the navbar with the **Hero Pixel Portrait** visual language.
- Added a dynamic background glass tint (`var(--hero-active-color-glow)`) that applies directly to the outer container.
- Implemented dual **PCB trace signal sweep animations** at the top/bottom borders that pulse electric blue every 12 seconds.
- Reverted all inner items (search button, github link, sitemap container) to transparent, borderless structures (`bg-black/5 dark:bg-white/5`), keeping layout clean.
- Synced the **PNJ Logo** text color dynamically to the active portrait brand color.
- Sized ThemeToggle button to match toolbar icons (8x8) and supported inline style forwarding to resolve type checks.

### 2. Browser Tab Icon (Favicon)
- Replaced the default browser fallback sitemap globe icon with the custom **PNJ red glowing sphere logo** across all served routes.

### 3. Google Drive Multi-Provider Subsystem
- Fully implemented OAuth 2.0 connection, refresh, and token encryption flows.
- Built automatic classification storage routing (documents/images/videos/backups/logs) and >=90% space capacity fallback mechanisms.
- Wrapped all block discovery clients inside `asyncio.to_thread` for non-blocking execution performance.
- Exposed robust storage endpoints under `/api/storage/...` (upload, download, list, delete, health, search, providers).

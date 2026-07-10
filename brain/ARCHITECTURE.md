# System Architecture Specifications

This document catalogs the folder structure, system components interaction, and data flows within Warborn OS.

---

## 1. Monorepo Organization

The project is structured as a Turborepo monorepo:

```
├── apps/
│   ├── api/                 # FastAPI Backend (Python)
│   │   ├── app/
│   │   │   ├── models/      # Database models (habits, recovery, storage)
│   │   │   ├── routers/      # API endpoints (gcalendar, recovery, habits)
│   │   │   ├── storage/     # StorageManager, oauth managers, and validators
│   │   │   └── main.py      # Lifespan managers & routers initialization
│   │   └── alembic/         # Migration versions scripts
│   │
│   └── web/                 # Next.js Frontend (TypeScript)
│       ├── src/
│       │   ├── app/         # App router (habits, recovery, ai-coach, dashboard)
│       │   ├── components/  # Sidebar navigation, upload center overlays
│       │   └── hooks/       # Shortcut hooks, upload center managers
│
└── brain/                   # Engineering logs & specifications documentation
```

---

## 2. Integrated Architecture Flow

The system flows through three distinct layers: client interface, backend service API, and database/cloud abstractions.

```
+--------------------------------------------------------+
|                      Next.js UI                        |
|                                                        |
|   [Mission Control]  [Habits]  [Recovery]  [Calendar]  |
+---------------------------+----------------------------+
                            | (HTTP / Fetch API)
                            v
+--------------------------------------------------------+
|                   FastAPI Router                       |
|                                                        |
|   [habits.py]  [recovery.py]  [gcalendar.py] [gdrive.py]|
+---------------------------+----------------------------+
                            | (SQLAlchemy ORM)
                            v
+--------------------------------------------------------+
|                  PostgreSQL Database                   |
|                                                        |
|   [habits]  [user_addictions]  [calendar_events] [...] |
+---------------------------+----------------------------+
                            |
                            v
+--------------------------------------------------------+
|                   Cloud Sync Agents                    |
|                                                        |
|   [Google Drive API]     <--->    [Google Calendar API]|
+--------------------------------------------------------+
```

---

## 3. Storage Abstraction Layer

The `StorageManager` acts as a facade, exposing clean file methods (`upload`, `download`, `delete`) to the API routers while virtualizing client tokens:
- **Provider Registry**: The database stores multiple credential keys (`storage_providers`).
- **Failover Queue**: Uploads execute sequentially along active providers. If one throws an error (e.g. invalid credentials or capacity limits reached), the upload is redirected to the fallback provider without interrupting the frontend client session.
- **Background Synchronization**: Integrates background tasks to sync note attachments and daily logs without blocking requests response times.

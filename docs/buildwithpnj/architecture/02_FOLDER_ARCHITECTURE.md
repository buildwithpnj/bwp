# Folder Architecture Spec (02_FOLDER_ARCHITECTURE.md)

This document maps out the unified folder structure designed for the **BuildWithPNJ** platform. The monorepo uses Turborepo to manage applications and shared packages, hosting the public website and the integrated **Warborn OS** dashboard subsystem.

---

## 1. Directory Tree Overview

```
.
├── apps/                        # Frontend/Backend Executable Services
│   ├── web/                     # Next.js 15 Web Application (BuildWithPNJ & Warborn OS)
│   └── api/                     # FastAPI Backend Application
├── packages/                    # Reusable Custom Monorepo Modules
│   └── shared-types/            # Shared TypeScript type declarations
├── content/                     # Static Content System Data Files (BuildWithPNJ CMS)
│   ├── blog/                    # Engineering Journal Articles (Markdown)
│   ├── case-studies/            # Detailed Project Writeups (Markdown)
│   └── experiments/             # Labs Hypotheses & Logs (Markdown)
├── scripts/                     # CI/CD & Database Migration Automation Files
└── docs/                        # Specifications, Design reviews, & Architecture
```

---

## 2. In-Depth Workspace Folder Directory Mappings

### `apps/web/`
Next.js 15 App Router codebase. Responsible for compiling static brand interfaces and client dashboard features.
- **`src/app/`**: Route definitions.
  - **`(public)/`**: Public route group mapping the **BuildWithPNJ** brand website (marketing index, about, contact, labs, projects, journal, mission control).
  - **`(app)/`**: Authenticated dashboard routes representing the **Warborn OS** developer operating subsystem (dashboard home, notes, books, habits, storage, tools, agent inbox).
  - **`(auth)/`**: Login and Registration routes securing access to the Warborn OS workspace.
- **`src/components/`**: Modular UI elements.
  - **`ui/`**: Base UI elements (buttons, inputs, cards, dialogs, retro terminals).
  - **`features/`**: App-scoped visual modules (inbox items, habit lists).
- **`src/hooks/`**: Shared browser interaction listeners (keyboard shortcuts, active scrolls).
- **`src/lib/`**: Standalone helper modules (markdown filesystem loader, analytics tracers).
- **`src/services/`**: API fetching service wrappers.
- **`src/types/`**: Unified TypeScript type configurations.
- **`public/`**: Public assets (optimized local fonts like `Pixel Operator`, images, site icons).

### `apps/api/`
FastAPI Python service. Manages compute-intensive systems calculations, user authentications, and habits/notes database operations.
- **`src/routes/`**: API route configurations (auth verification, habits sync, transactions logging).
- **`src/services/`**: Integration logic for Google Drive document syncing, database operations.
- **`src/models/`**: Pydantic schema wrappers validating request and response structures.

### `packages/shared-types/`
Contains common TypeScript interfaces and models shared between apps.

### `content/`
Acts as a file-based Content Management System (CMS) for the public BuildWithPNJ pages. Separated from application code to enable easy content additions without altering routing logic.

### `scripts/`
Automation utilities written in Bash, Python, or Node.js.
- Database migration triggers.
- Code style format checkers.
- Content validating scripts to verify frontmatter compliance.

# BuildWithPNJ — Changelog

> All notable changes to the BuildWithPNJ brand and products are documented here.
> Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.2.0] — 2026-07-10

### 🎉 Multi-Provider Google Storage, Life OS, & Telemetry Refinement

This version completes the multi-account virtual storage failover, bi-directional calendar caching, routines check-in splits, and reaches compiler zero warnings.

### Added
- **Multi-Account Storage Manager** — Supports registering multiple independent Google Drive accounts, encrypting credentials, and performing auto-failover on capacity limits.
- **Bi-Directional Calendar Cache** — Implemented postgres calendar events caching to eliminate API lookup latency.
- **Cognitive Recovery Interrupter** — Integrated 102 prompts content library and 7s slide-fade queues overlays.
- **Symmetrical Telemetry Layout** — Aligned data stream nodes in parallel rows, replacing round circles with sharp pixels.
- **IP Locale clock sync** — Automated currency symbols and timezone format changes based on client IP geolocations.

### Fixed
- **Next.js Compile Warnings** — Resolved linter warnings inside habits checklists, hero status bar, background vectors, and terminals.


---

## [0.1.0] — 2026-07-04

### 🎉 Brand HQ Initialization

The official launch of the BuildWithPNJ workspace as a structured brand headquarters.

### Added

#### Brand Infrastructure
- **`my brand PNJ/`** — Central brand folder established as HQ
- **`brand/assets/logos/`** — Logo assets directory (awaiting final designs)
- **`brand/assets/fonts/`** — Custom typography directory
- **`brand/assets/social/`** — Social media templates directory
- **`content/blog/`** — Blog content pipeline
- **`content/case-studies/`** — Portfolio case studies directory
- **`docs/`** — Internal documentation directory

#### Brand Documents
- **`PROJECT_OVERVIEW.md`** — Master overview of the BuildWithPNJ brand, mission, tech stack, and folder structure
- **`ROADMAP.md`** — Strategic 4-phase roadmap (Q3 2026 → Q3 2027) covering product, brand, content, and monetization
- **`BRAND_GUIDELINES.md`** — Complete brand identity guide: colors, typography, voice, tone, social strategy
- **`WEBSITE_PRD.md`** — Full product requirements document for `buildwithpnj.com`
- **`TASKS.md`** — Prioritized living task tracker
- **`CHANGELOG.md`** — This file

#### Already Existing (Pre-Brand Setup)
- **Personal OS** — Production-grade personal operating system
  - Next.js 15 frontend with dashboard, finance, books, habits, notes, tools, agent inbox, and storage modules
  - FastAPI backend with full REST API (auth, dashboard, finance, books, habits, notes, Google Drive sync)
  - PostgreSQL 16 + pgvector database with Redis 7 cache
  - Turborepo monorepo with npm workspaces
  - Docker Compose local development stack
  - JWT authentication with argon2 hashing

---

## Version History Key

| Emoji | Meaning |
|---|---|
| 🎉 | Major milestone / launch |
| ✨ | New feature |
| 🔧 | Bug fix |
| 🎨 | Design / UI change |
| 📝 | Documentation |
| ⚡ | Performance improvement |
| 🔒 | Security fix |
| 💥 | Breaking change |
| 🗑️ | Deprecation / removal |

---

*Last updated: 2026-07-10*

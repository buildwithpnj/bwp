# Technology Stack Rationalization (15_TECH_STACK.md)

This document explains the technical trade-offs and rationales behind selecting each core component of the unified **BuildWithPNJ** brand website and the integrated **Warborn OS** dashboard.

---

## 1. Frontend Infrastructure

### Next.js 15 & React 19
- **Rationale**: Next.js is selected to host both the public branding pages (BuildWithPNJ) and the client developer operating subsystem (Warborn OS). It allows pre-rendering of marketing content like `/journal` and `/projects` into lightweight static files while keeping `/dashboard` dynamic and client-interactive.
- **Trade-offs**: Next.js introduces a structured compilation layer and requires careful coordination between Server and Client Components.

### TypeScript
- **Rationale**: Type safety prevents runtime regressions and syntax errors across the shared monorepo packages.

### TailwindCSS & CSS Variables
- **Rationale**: Tailwind provides fast, utility-first styling with small compiled build sizes. The public website utilizes custom CSS variables (like glows, typography configurations) matching BuildWithPNJ design tokens, which are shared cleanly with the dashboard layouts.

### Framer Motion
- **Rationale**: Handles micro-animations and dashboard workspace transitions.

---

## 2. Content & Compilation Layer

### gray-matter & marked
- **Rationale**: Since the site uses a file-based markdown CMS for BuildWithPNJ articles and R&D lab experiments, `gray-matter` extracts metadata tags cleanly, and `marked` compiles markdown body fields to standard HTML. This setup loads faster than heavy headless CMS solutions.

---

## 3. Backend & Database Layer

### FastAPI (Python)
- **Rationale**: Selected for the backend API due to its native support for asynchronous tasks, speed, automatic OpenAPI generation, and compatibility with Python-first AI operating frameworks (LangGraph, OpenAI, LlamaIndex).
- **Trade-offs**: Requires running two separate development servers (Next.js Node server and Uvicorn Python server).

### Supabase & SQLAlchemy / Alembic
- **Rationale**: Supabase provides a managed, scalable PostgreSQL database. SQLAlchemy and Alembic handle migration tracking and object mapping records cleanly, enabling structured synchronization tasks for Warborn OS notes, habit logs, and expenses.

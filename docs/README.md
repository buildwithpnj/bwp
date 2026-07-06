# BuildWithPNJ Documentation Index (README.md)

Welcome to the central documentation index for **BuildWithPNJ** (the public AI engineering platform) and **Warborn OS** (the integrated developer dashboard subsystem). This directory serves as the onboarding manual for both human developers and AI coding agents.

---

## 1. Documentation Purpose
This documentation system acts as the technical constitution for the platform. It provides a single source of truth detailing visual specs, folder scopes, database schemas, code review checklists, and git guidelines. Maintaining synchronized, structured documentation ensures codebase cleanliness and long-term scalability.

---

## 2. Quick Navigation Index

| Document Category | Target Path | Description |
| :--- | :--- | :--- |
| **Product Specifications** | [docs/buildwithpnj/product/](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/product/) | PRDs, sitemaps, user personas, UX flows. |
| **System Architecture** | [docs/buildwithpnj/architecture/](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/architecture/) | Blueprints, DB schemas, state engines, security. |
| **Engineering Governance** | [docs/buildwithpnj/governance/](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/governance/) | Coding rules, git workflows, review checklists. |
| **Sprints & QA Validation** | [docs/buildwithpnj/validation/](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/validation/) | QA checklists, sprint reports, technical debt logs. |
| **Project Timelines** | [docs/buildwithpnj/roadmap/](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/roadmap/) | Task checklists, changelogs, roadmaps. |
| **Design & Research** | [docs/buildwithpnj/research/](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/research/) | Design specifications and mockups. |
| **ADR Decisions** | [docs/buildwithpnj/decisions/](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/decisions/) | Architectural Decision Records (ADRs). |

---

## 3. Directory Hierarchy

```
docs/
└── buildwithpnj/
    ├── product/      # Brand vision, PRDs, personas, sitemaps
    ├── architecture/ # System designs, API schemas, db models (01-15)
    ├── governance/   # Coding styles, branching strategics (16-30)
    ├── validation/   # Quality logs, sprint reports, checklists
    ├── roadmap/      # Active tasks checklists, changelogs
    ├── research/     # Visual spec guides, experiments
    └── decisions/    # Architectural Decision Records (ADRs)
```

---

## 4. Required Reading (Sources of Truth)

Before making any structural changes, editing styles, or adding database columns, engineers and AI agents must review these core documents:

1. [docs/buildwithpnj/product/PROJECT_OVERVIEW.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/product/PROJECT_OVERVIEW.md) — High-level platform purpose.
2. [docs/buildwithpnj/product/WEBSITE_PRD.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/product/WEBSITE_PRD.md) — Public-facing feature requirements.
3. [docs/buildwithpnj/architecture/01_SYSTEM_ARCHITECTURE.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/architecture/01_SYSTEM_ARCHITECTURE.md) — Flow blueprints and rendering matrices.
4. [docs/buildwithpnj/governance/16_CODING_STANDARDS.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/governance/16_CODING_STANDARDS.md) — Strict TypeScript, Next.js, and CSS constraints.
5. [docs/buildwithpnj/governance/30_AI_AGENT_DEVELOPMENT_GUIDE.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/docs/buildwithpnj/governance/30_AI_AGENT_DEVELOPMENT_GUIDE.md) — The AI coding constitution.

---

## 5. Contributor Workflow

Every contribution must follow this development lifecycle:

```
Read Documentation ──► Understand Architecture ──► Plan Changes ──► Implement
                                                                      │
     ┌────────────────────────────────────────────────────────────────┘
     ▼
Test Logic & Builds ──► Update Documentation ──► Open Review PR
```

---

## 6. Documentation Contribution Guidelines

- **Where docs belong**:
  - Add product strategies under `docs/buildwithpnj/product/`.
  - Add technical blueprints under `docs/buildwithpnj/architecture/`.
  - Add ADR records under `docs/buildwithpnj/decisions/` using the standard format.
- **Naming Conventions**:
  - Folders and general files must use **kebab-case** (e.g. `system-telemetry.md`).
  - Architecture specs must preserve their index prefix (e.g. `01_SYSTEM_ARCHITECTURE.md`).
- **Markdown Standards**: Use GitHub Flavored Markdown (GFM). Always use proper heading hierarchies (`#` through `######`) and ensure all file paths use clickable `file:///` links.
- **Edits over Duplicates**: Update existing files instead of creating new ones to prevent information redundancy.

---

## 7. Platform Documentation Map

The platform documents relate to each other through a logical flow:

```
  [Product Vision & PRD]  (What we are building)
          │
          ▼
  [Architecture Design]   (How the database, API, and components are structured)
          │
          ▼
  [Governance Rules]      (Coding rules and Git processes required during coding)
          │
          ▼
  [Validation Audits]     (How we check builds, performance, and WCAG AA compliance)
```

---

## 8. Documentation Principles

- **Single Source of Truth**: Documentation is the definitive guide for system behavior.
- **Keep Synchronized**: Update documentation alongside code changes.
- **Never Duplicate**: Link to existing documents instead of copying information.
- **Prefer Edits**: Expand or refine existing documents before creating new files.
- **Record Decisions**: Document all major engineering decisions using Architectural Decision Records (ADRs).

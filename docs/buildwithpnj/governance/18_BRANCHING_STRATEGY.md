# Branching Strategy Spec (18_BRANCHING_STRATEGY.md)

This document describes the branch directory taxonomy, lifetimes, and naming criteria designed to manage version histories on the **BuildWithPNJ** platform.

---

## 1. Core Branch Directory Trees

The repository is structured into distinct, namespace-isolated branching folders:

```
                            REPOSITORY BRANCHES
                                     │
       ┌─────────────────────────────┼─────────────────────────────┐
       ▼                             ▼                             ▼
  LONG-LIVED BRANCHES        RELEASE BRANCHES              SHORT-LIVED BRANCHES
  - main (Production)        - release/* (Release checks)  - feature/* (Features)
  - develop (Integration)                                  - fix/* (Bugfixes)
                                                           - experiment/* (R&D Labs)
                                                           - research/* (Docs/SPIs)
```

---

## 2. Branch Mappings & Naming Rules

### 1. `main` (Long-Lived)
- **Purpose**: Stable production code. Represents the state of the live website at any point.
- **Rule**: No one makes commits directly to `main`. It only accepts merges from release branches.

### 2. `develop` (Long-Lived)
- **Purpose**: Active development integration branch.
- **Rule**: Target branch for all features and bugfixes.

### 3. `feature/*` (Short-Lived)
- **Naming Convention**: `feature/<feature-name>` (e.g. `feature/agent-inbox`).
- **Rule**: Branches off `develop` and merges back into `develop`.

### 4. `fix/*` (Short-Lived)
- **Naming Convention**: `fix/<bug-desc>` (e.g. `fix/auth-cookie-path`).
- **Rule**: Branches off `develop` to resolve standard bugs.

### 5. `hotfix/*` (Short-Lived)
- **Naming Convention**: `hotfix/<prod-error>` (e.g. `hotfix/landing-ssr-crash`).
- **Rule**: Branches off `main` to address critical production issues. Merges back into both `main` and `develop`.

### 6. `release/*` (Short-Lived)
- **Naming Convention**: `release/v<version-number>` (e.g. `release/v1.2.0`).
- **Rule**: Created off `develop` when features are locked. Only receives stability fixes before merging into `main`.

### 7. `experiment/*` (Short-Lived)
- **Naming Convention**: `experiment/<exp-id-slug>` (e.g. `experiment/exp-002-voice-ui`).
- **Rule**: Used for R&D Labs code. Can merge into `develop` if approved, or be archived.

### 8. `research/*` (Short-Lived)
- **Naming Convention**: `research/<topic>` (e.g. `research/vector-db-comparison`).
- **Rule**: Dedicated to writing documentation, architecture specifications, and planning logs.

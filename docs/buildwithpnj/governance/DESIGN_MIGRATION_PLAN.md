# Design Migration Plan (DESIGN_MIGRATION_PLAN.md)

This document establishes the step-by-step refactoring strategy to unify design variables and migrate shared UI components into the monorepo packages.

---

## 1. Migration Steps Mapped

```
  [ STEP 1: CSS Setup ] ──────────────► [ STEP 2: Theme Setup ] ──────────► [ STEP 3: Comp Migration ]
  Consolidate globals.css variables     Configure next-themes Provider    Move UI tools to packages/ui
                                                                                        │
  ┌─────────────────────────────────────────────────────────────────────────────────────┘
  ▼
  [ STEP 4: Class Updates ] ──────────► [ STEP 5: Verification ]
  Replace hardcoded styles              Run dev build checking tests
```

### Step 1: CSS Variables Consolidation
- Clean up `globals.css` and define consistent design token variables (`--background`, `--surface`, `--border`, `--accent`) for both light and dark mode.

### Step 2: Global Theme Provider
- Set up a single `ThemeProvider` context wrapper inside `apps/web/src/app/layout.tsx` to handle theme changes globally.

### Step 3: Packages migration
- Create the shared component package `@personal-os/ui` inside `packages/ui` and move reusable components (e.g. Buttons, Cards, Terminals, CodeBlocks) to this folder.

### Step 4: Component imports refactoring
- Search and update component imports across all app routes to reference the shared `@personal-os/ui` package.
- Remove duplicate component definitions from the `apps/web` directory.

### Step 5: Verification
- Run a production build (`npm run build`) to verify that the refactored imports compile successfully.

# Component Migration Plan (COMPONENT_MIGRATION_PLAN.md)

This document establishes the migration plan to consolidate reusable visual elements into the `packages/ui` package, allowing public marketing pages and authenticated dashboard features to consume the same code.

---

## 1. Migration Goals
- Consolidate layout elements (Buttons, Cards, Inputs, Tables) into a shared monorepo package `packages/ui`.
- Remove duplicate components from `apps/web/src/components/ui/` to ensure a single source of truth.
- Ensure unified design system compliant states inside the migrated items.

---

## 2. Refactoring Timeline Mappings

```
  [ STEP 1: Audit ] ────────────────► [ STEP 2: Package Setup ] ─────► [ STEP 3: Component Move ]
  Audit apps/web/src/components       Configure packages/ui package    Move core components
                                                                              │
  ┌───────────────────────────────────────────────────────────────────────────┘
  ▼
  [ STEP 4: Import Update ] ────────► [ STEP 5: Verification ]
  Update app route imports            Run build checks & validation
```

### Step 1: Audit
Identify components (e.g. Buttons, Cards, Terminals, CodeBlocks) that are currently duplicated or defined separately on pages.

### Step 2: Package Setup
Ensure `packages/ui` is properly configured as an workspace package, export entries in `package.json`, and set up TypeScript path mappings.

### Step 3: Component Move
Move core components to the package directory, resolving external module dependencies (like `lucide-react`, `clsx`, `tailwind-merge`).

### Step 4: Import Update
Update imports in the Next.js routes to reference the shared package:

```typescript
import { Button, Card } from '@personal-os/ui';
```

### Step 5: Verification
Run a production build (`npm run build`) to ensure the refactored imports compile successfully.

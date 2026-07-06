# Code Review Checklist Spec (24_CODE_REVIEW_CHECKLIST.md)

This document establishes the code review guidelines, PR verification lists, and quality checks required before merging code into the **BuildWithPNJ** codebase.

---

## 1. Automated Validation Check

Every pull request must pass the automated CI/CD pipeline checks in GitHub Actions:
- **Build Pass**: Node compile and FastAPI server verify cleanly with 0 exit errors.
- **Type Check**: TypeScript compiler exits with code 0 (`tsc --noEmit` returns success).
- **Linter Pass**: Standard code layout formatting rules are verified.

---

## 2. Reviewer Checklist (Manual Check)

When evaluating a pull request, reviewers must verify these conditions:

### 1. Architectural Compliance
- Code additions adhere to System Architecture plans (`01_SYSTEM_ARCHITECTURE.md`).
- Logic is structured in the correct monorepo directories (`02_FOLDER_ARCHITECTURE.md`).
- Interactive handlers are isolated inside Client Components (`19_COMPONENT_CONVENTIONS.md`).

### 2. Performance Check
- Verify that no heavy libraries are imported inside Server Components.
- Large assets (e.g. custom icons or images) use optimized Next.js components.
- Avoid introducing unnecessary loops or expensive recalculations inside React render passes.

### 3. Accessibility & Layout
- Layouts are responsive and scale cleanly across mobile, tablet, and desktop viewports.
- All interactive elements are keyboard focusable and have clear outline indicators.
- HTML elements use correct semantic tags (e.g. `<main>`, `<article>`, `<header>`).

### 4. Code Quality & Security
- Check that sensitive credentials (API tokens, database URLs) are not checked in and are only loaded via environment variables.
- Pydantic models validate input variables strictly.
- User inputs are sanitized to prevent cross-site scripting (XSS) vectors.
- Avoid duplicating existing utility functions or styling rules.
- Added or modified features include matching unit or integration tests.
- Associated documentation is updated to reflect the changes.

# Testing Strategy Spec (13_TESTING_STRATEGY.md)

This document describes the automated testing matrix, regression monitoring, and compliance checks designed to maintain high code quality on the **BuildWithPNJ** platform.

---

## 1. Multi-Tier Testing Pyramid

The testing strategy is divided into four structural test suites:

```
               TESTING MATRIX PYRAMID
                         ▲
                        / \
                       /   \     E2E (Playwright) - Critical flows, auth, database sync
                      /     \
                     /       \   Integration (RTL) - Hook states, keyboard palette triggers
                    /         \
                   /           \ Unit (Vitest) - Helper functions, markdown parsing
                  └─────────────┴
```

---

## 2. Testing Levels Details

### 1. Unit Testing (Vitest)
Used for fast-running validation of logical components and services:
- **Scope**:
  - Markdown filesystem parsers (`content.ts`).
  - Currency and date formatting utilities.
  - Slug generation checks.
- **Run Timing**: Triggered on every commit and PR verification check.

### 2. Integration Testing (React Testing Library)
Ensures components correctly handle user interactions and state changes:
- **Scope**:
  - Command Palette chord inputs (`g` -> `p`).
  - Search input filtering in project grids.
  - Active tab selection in R&D Labs.

### 3. End-to-End Testing (Playwright)
Validates complete user flows across simulated browsers (Chromium, Firefox, WebKit):
- **Scope**:
  - Login redirects and cookie authorizations.
  - Form validations and database writes.
  - Global navigation links.

### 4. Accessibility Testing (axe-core)
Verifies WCAG 2.1 compliance across layouts:
- **Scope**:
  - Color contrast minimum ratios (>4.5:1).
  - ARIA label matches on buttons.
  - Keyboard navigation focus rings.
- **Implementation**: Runs automatically inside local Playwright tests.

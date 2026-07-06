# AI Agent Development Guide (30_AI_AGENT_DEVELOPMENT_GUIDE.md)

This document serves as the **AI Constitution** for the **BuildWithPNJ** platform. Any future AI agents or agentic coding systems contributing to this codebase must adhere strictly to these rules, execution workflows, and coding principles.

---

## 1. Core Operating Principles

Future AI agents must follow these engineering principles:
- **Code for Humans**: Write clean, self-documenting code. Code structures must be easy to read and maintain for human developers.
- **Planning-First Workflows**: Never modify code files or run modifying commands without first completing a research phase and obtaining approval for an implementation plan.
- **Server-First Component Selection**: Default to Server Components. Only convert files to Client Components (`'use client'`) if they explicitly require interactive hooks or client-only APIs.
- **Zero Tolerance for Technical Debt**: Never leave TODO placeholders, temporary fallback blocks, or unescaped entities in target code.

---

## 2. Step-by-Step AI Execution Workflow

Every engineering task assigned to an AI agent must follow this execution lifecycle:

```
                            AI AGENT LIFECYCLE
                                     │
           1. Research & Analyze current files and dependencies
                                     │
           2. Create Implementation Plan (open questions, changes list)
                                     │
           3. Obtain Human Approval (DO NOT proceed without sign-off)
                                     │
           4. Execute Changes incrementally with small, atomic commits
                                     │
           5. Self-Review code against checklists & compile tests
                                     │
           6. Document changes in a walkthrough.md artifact
```

---

## 3. Mandatory Safety & Validation Rules

- **No Unauthorized Architecture Changes**: AI agents are not permitted to change architecture files (e.g. `COMPLETE_UI_DESIGN_SPEC.md`, `01_SYSTEM_ARCHITECTURE.md`) without explicit human approval.
- **Prerendering & Hydration Check**:
  - Event handlers (`onClick`, `onSubmit`) must not be passed to properties inside Server Components.
  - HTML tags containing slash text (e.g., `// ABOUT`) must be wrapped in JSX string braces: `{"// ABOUT"}`.
  - Special characters (like `'` or `"`) must be properly escaped inside JSX text blocks.
- **Test Validation**: Added logic must include unit tests. Run the build and test suites (`npm run build`) before requesting final code review.
- **observability & Telemetry**: Dynamic API actions must implement structured JSON logging and Sentry error checks.
- **Accessibility Check**: Ensure color contrast ratios comply with WCAG AA standards. Ensure interactive elements support keyboard focus and logical tab orders.
- **Code Reviews**: AI agents must perform a self-review of all changes against the checklist in `24_CODE_REVIEW_CHECKLIST.md` before submitting a PR.
- **Documentation Updates**: Always document your changes in the project walkthrough and update associated API documents or README files.
- **Reasoning Disclosure**: Always provide clear explanations for design choices, code optimizations, and directory allocations.

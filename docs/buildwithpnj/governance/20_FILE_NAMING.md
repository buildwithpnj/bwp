# File Naming Conventions Spec (20_FILE_NAMING.md)

This document establishes the file casing rules, folder suffix patterns, and directory structures enforced across the **BuildWithPNJ** platform.

---

## 1. Core Casing Rules

To ensure cross-platform compatibility across filesystems (e.g., Windows and Linux case-insensitivity bugs), the codebase strictly enforces these casing rules:

- **kebab-case**: All standard files, utility scripts, and routing directory folders (e.g. `public-header.tsx`, `content.ts`, `personal-os.md`, `mission-control`).
- **PascalCase**: Strictly reserved for React Components inside export files if they map one-to-one with a specific component class (e.g., `DashboardCard.tsx`).
- **camelCase**: Strictly reserved for utility helper files, mock datasets, and hooks (e.g. `useAuth.ts`, `formatCurrency.ts`).

---

## 2. File Suffix Patterns

Files must declare their structural role using specific suffixes:

| File Type | Suffix Format | Example |
| :--- | :--- | :--- |
| React Components | `PascalCase.tsx` | `PublicHeader.tsx` |
| Client Hooks | `use-camelCase.ts` | `useAuth.ts` |
| Unit Tests | `*.test.ts` or `*.test.tsx` | `content.test.ts` |
| Route Layouts | `layout.tsx` | `layout.tsx` |
| Route Pages | `page.tsx` | `page.tsx` |
| TypeScript Types | `*.types.ts` or `types.ts` | `content.types.ts` |
| Global Constants | `constants.ts` | `theme.constants.ts` |

---

## 3. Formatting Verification

Lint verification configurations (such as ESLint rules) enforce casing standards. Any commit containing naming conflicts (e.g., `Public_Header.tsx` or `Publicheader.tsx`) will fail automated checks during pull request evaluation.

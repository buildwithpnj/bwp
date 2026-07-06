# Coding Standards Spec (16_CODING_STANDARDS.md)

This document defines the coding rules, language conventions, and formatting requirements enforced across the **BuildWithPNJ** codebase.

---

## 1. TypeScript Rules

- **Strict Configurations**: Enable `"strict": true` in `tsconfig.json`. This checks for implicit `any` definitions, strict null evaluations, and unused variables.
- **Type Definitions**: Prefer interfaces for object signatures and type aliases for unions/primitives:
  ```typescript
  // Interfaces for structures
  interface UserProfile {
    id: string;
    email: string;
  }

  // Type aliases for unions or actions
  type AuthStatus = 'authenticated' | 'unauthenticated' | 'loading';
  ```
- **Explicit Returns**: Always declare return types for exported functions to improve compiler diagnostics and visual readability.
- **Never Use `any`**: If a type signature is dynamic or unknown, use `unknown` and perform explicit runtime type narrowing (e.g. using `typeof` or Pydantic validation).

---

## 2. React & Next.js Composition Rules

- **Functional Components**: Write React components as standard functional declarations: `export function ComponentName() {}`. Do not use default exports for components to make imports consistent.
- **Hooks Conventions**: Hook parameters must be fully typed. Avoid inline dependency array modifications in hooks (`useEffect`, `useMemo`); all referenced state variables must be declared in dependencies.
- **Server Components by Default**: In Next.js, all files under `src/app` run as Server Components (RSC) by default. Use `'use client'` strictly at leaf nodes that handle client state.
- **JSX Comments**: Always wrap comments inside JSX tags with curly braces: `{"// COMMENT_TEXT"}` to prevent build compilation failures.

---

## 3. Tailwind CSS Conventions

- **Class Ordering**: Sort utility tags according to standard layouts: Layout & Position -> Spacing & Box Model -> Typography -> Borders & Shadows -> Visual States.
- **Dynamic Classes**: Never use dynamic string construction (e.g. `bg-${color}-500`) since Tailwind's compiler purges unused utilities. Use static mapping objects instead:
  ```typescript
  const colorMap = {
    cyan: 'bg-[#00F5FF]',
    blue: 'bg-[#3B82F6]',
  };
  ```

---

## 4. Async & Error Handling Standards

- **Try-Catch Blocks**: Async functions must wrap their logic in try-catch structures:
  ```typescript
  try {
    const response = await fetch('/api/v1/telemetry');
    if (!response.ok) throw new Error('Failed to retrieve telemetry data');
  } catch (error) {
    handleError(error);
  }
  ```
- **Promise.all**: Run concurrent API operations in parallel using `Promise.all` instead of blocking executions with consecutive `await` statements.

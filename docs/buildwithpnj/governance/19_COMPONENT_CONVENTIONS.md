# Component Conventions Spec (19_COMPONENT_CONVENTIONS.md)

This document details the guidelines, coding conventions, and composition paradigms required when designing visual interfaces for the **BuildWithPNJ** platform.

---

## 1. Composition Over Inheritance

- **React Composition**: Customize UI components by nesting child elements (using the `children` prop) rather than passing long lists of complex styling properties.
- **Props Typing**: All React components must declare a strict TypeScript interface:
  ```typescript
  interface ButtonProps {
    label: string;
    onClick: () => void;
    disabled?: boolean;
    variant?: 'primary' | 'secondary' | 'glow';
    children?: React.ReactNode;
  }
  ```

---

## 2. Server & Client Component Boundaries

To maximize server pre-rendering and minimize JavaScript bundle weights:
- **Server Components (RSC)**: By default, components should run on the server. They handle data loading, layout rendering, and markdown compilation.
- **Client Components (RCC)**: Demarcated with `'use client'` at the top of the file. Use them only when:
  - Component reads state using hooks (`useState`, `useReducer`, `useContext`).
  - Component listens to browser-only events (`onClick`, `onScroll`).
  - Component utilizes window-specific globals (e.g. `navigator.clipboard`, `localStorage`).

---

## 3. Hook Extraction Rules

- **Clean UI Files**: Do not mix complex data processing, API fetching, or keyboard listener logic directly inside the UI rendering tree.
- **Custom Hooks**: Extract complex state flows into custom hooks (e.g. `useKeyboardShortcuts.ts`, `useFinanceSummary.ts`) and locate them under `src/hooks/` or a local `hooks/` subdirectory within the feature folder.
- **Pure Functions**: Visual presentation components should remain functional and pure, depending only on their incoming props.

# Design Token Reference (DESIGN_TOKEN_REFERENCE.md)

This document maps the centralized design tokens used to enforce consistency across the public marketing website and the authenticated dashboard.

---

## 1. Unified Token Matrix

| Token Category | Value / Variable | Tailwind / CSS Class | Description |
| :--- | :--- | :--- | :--- |
| **Default BG** | `var(--background)` | `bg-background` | Page background color. |
| **Surface BG** | `var(--surface)` | `bg-surface` | Card and component surfaces. |
| **Border Radius** | `8px` | `rounded-lg` | Standardized corner rounding. |
| **Grid Gutter** | `32px` | `gap-8` | Grid spacing rule. |
| **Animation timing** | `300ms` | `duration-300` | Standard animation speed. |
| **Transition easing** | `cubic-bezier(0.16, 1, 0.3, 1)` | `ease-out` | Standard animation curve. |
| **Subtle Shadows** | `0 4px 6px -1px rgb(0 0 0 / 0.1)` | `shadow-md` | Card and popover depth. |

---

## 2. Token Application Rules
- **Typography Scale**: Standardize body text to `text-base` / `leading-relaxed` and labels to `text-sm` / `font-medium` to maintain layout consistency.
- **Borders**: Enforce a unified border style (`border border-border`) with a 1px width to prevent varying element outlines.
- **Motion Controls**: Apply the standard ease-out curve to all interactive transitions (hover states, modal entry animation) to keep movement unified.

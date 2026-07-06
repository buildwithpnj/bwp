# Light Mode Implementation Spec (LIGHT_MODE_IMPLEMENTATION.md)

This document maps out the color mappings, contrast rules, and components adjustments for the light mode theme.

---

## 1. Light Mode Colors

To create a clean, accessible light mode theme, map the variables in `globals.css` to light HSL values:

- **Background Void**: `210 20% 98%` (Off-white / clean light gray).
- **Surface / Card Background**: `210 20% 95%` (Light slate gray).
- **Text Primary**: `222 47% 11%` (Slate dark gray / near black).
- **Text Muted**: `215 16% 47%` (Muted gray-blue).
- **Border**: `214 32% 91%` (Light gray border).
- **Accent**: `221 83% 53%` (Electric Blue).

---

## 2. High-Contrast Contrast Metrics
- **Verification**: All text elements in light mode must achieve a minimum contrast ratio of 4.5:1 to meet WCAG AA standards.
- **Card Shadows**: Use a subtle box shadow (`shadow-sm` or `shadow-md`) to define card boundaries against the light background.
- **Active Accents**: Keep electric blue (`#3B82F6`) as the primary active indicator across interactive components.

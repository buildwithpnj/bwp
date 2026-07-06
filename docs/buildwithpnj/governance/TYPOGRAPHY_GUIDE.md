# Typography Guide (TYPOGRAPHY_GUIDE.md)

This document establishes the typographic hierarchy, font family mappings, line height constraints, and size grids for the **BuildWithPNJ** brand.

---

## 1. Font Family System

1. **Primary Display Font**: **`Pixel Operator Bold`** (retro-inspired local monospace font).
   - **Usage Rules**: ONLY for hero titles, section headings, Mission Control numbers, and major statistical displays.
   - **Never Use For**: Paragraph blocks, form fields, UI navigation links, or standard card descriptions.
2. **Body & Interface Font**: **`Geist`** (modern, clean, and neutral sans-serif).
   - **Usage Rules**: Paragraph prose, card summaries, descriptions, buttons, forms, and navigation menus.

---

## 2. Typographic Hierarchy Scale

| Element | Font Family | Size / Weight | Line Height | Tracking |
| :--- | :--- | :--- | :--- | :--- |
| **Hero H1** | `Pixel Operator Bold` | `text-5xl` to `text-6xl` | `leading-none` | `tracking-wide` |
| **Section H2** | `Pixel Operator Bold` | `text-3xl` to `text-4xl` | `leading-tight` | `tracking-normal` |
| **Telemetry H3** | `Pixel Operator Bold` | `text-xl` to `text-2xl` | `leading-snug` | `tracking-normal` |
| **Body Copy** | `Geist` (Sans-Serif) | `text-base` / `font-normal` | `leading-relaxed` | `tracking-normal` |
| **UI Labels** | `Geist` (Sans-Serif) | `text-sm` / `font-medium` | `leading-none` | `tracking-wider` (caps) |
| **Card Copy** | `Geist` (Sans-Serif) | `text-sm` to `text-base` | `leading-relaxed` | `tracking-normal` |

---

## 3. Style Constraints
- Always wrap technical terms and numeric logs inside monospace styles (`font-mono`).
- Avoid center-aligning body copy; keep paragraphs left-aligned to ensure high readability.
- Maintain a minimum contrast ratio of 4.5:1 for body copy to comply with WCAG AA accessibility standards.

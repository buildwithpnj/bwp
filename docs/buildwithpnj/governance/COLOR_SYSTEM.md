# Color System Spec (COLOR_SYSTEM.md)

This document establishes the color palette, background system variables, text colors, and highlighting parameters of the **BuildWithPNJ** brand.

---

## 1. Core Color Palette

The platform uses a dark-first, low-saturation color system with high-contrast accent highlights to establish a premium developer workspace feel:

- **Void Background**: `#050816` (Deep space black-blue background).
- **Surface / Card Background**: `#0F172A` (Slate dark cards).
- **Primary / Active Text**: `#F1F5F9` (Off-white / high-contrast slate).
- **Muted Text / Descriptions**: `#8E9CAE` (Cool gray-blue).
- **Primary Glow / Accent**: `#3B82F6` (Electric Blue).
- **Secondary Accent**: `#00F5FF` (Neon Cyan).

---

## 2. Color Application Matrix

```
  ┌─────────────────────────────────────────────────────────────┐
  │  Background: Void (#050816)                                 │
  │                                                             │
  │  ┌───────────────────────────────────────────────────────┐  │
  │  │ Card Container: Slate Dark (#0F172A)                   │  │
  │  │ border: #1E293B (1px)                                 │  │
  │  │                                                       │  │
  │  │ Active Title: #F1F5F9                                 │  │
  │  │ Description: #8E9CAE                                  │  │
  │  │ Accent Icon: #3B82F6 (Electric Blue)                  │  │
  │  └───────────────────────────────────────────────────────┘  │
  └─────────────────────────────────────────────────────────────┘
```

---

## 3. Highlighting Constraints
- Never use bright colors (like bright red, standard yellow, or green) for structural page highlights.
- Highlight states must use electric blue transitions (`hover:text-blue-400` or `hover:border-cyan-500`) to maintain color consistency.
- Semantic indicators (e.g. green for active, orange for pending) must use muted, desaturated tones matching the visual guidelines.

# Dark Mode Implementation Spec (DARK_MODE_IMPLEMENTATION.md)

This document establishes the dark mode visual system, including shadows, glows, and contrast metrics.

---

## 1. Dark Mode Colors

The default theme uses a dark-first color palette with high-contrast text and glowing accents:

- **Background Void**: `230 63% 5%` (Deep navy void `#050816`).
- **Surface / Card Background**: `222 47% 11%` (Slate dark `#0F172A`).
- **Text Primary**: `210 40% 96%` (Off-white `#F1F5F9`).
- **Text Muted**: `215 16% 62%` (Muted gray `#8E9CAE`).
- **Border**: `217 33% 17%` (Slate border `#1E293B`).
- **Accent Glow**: `221 83% 53%` (Electric Blue).

---

## 2. Glow Gradients & Shadows
- **Card Glow**: Use low-opacity radial gradients in electric blue (`#3B82F6`) or neon cyan (`#00F5FF`) to highlight container edges.
- **Scanline Overlays**: Apply subtle scanline backgrounds to terminal components.
- **Borders**: Enforce a 1px border width to keep UI elements clean and consistent.

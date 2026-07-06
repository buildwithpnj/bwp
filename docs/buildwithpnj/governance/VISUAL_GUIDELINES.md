# Visual Guidelines (VISUAL_GUIDELINES.md)

This document defines the layout principles, grid systems, line spacing rules, border decorations, and background aesthetics for the **BuildWithPNJ** brand interface.

---

## 1. Minimal Layout Grid
- **Alignment**: Standardized on a 12-column grid system with large gutters (32px / 2rem) to create ample breathing room.
- **Section Spacing**: Large vertical spacing (e.g., `py-24` to `py-32` in Tailwind) is applied to sections to draw focus to core typography blocks and prevent visual clutter.
- **Borders**: Thin, high-contrast borders (1px) using HSL color weights (`border-slate-800` or `#0F172A`) to define element boundaries without adding visual weight.

---

## 2. HUD & Blueprint Graphic Styles
To establish a premium, technical aesthetic, the UI uses minimalist graphics instead of generic stock illustrations:
- **Neural Networks & Circuit Diagrams**: Vector graphics with thin strokes (1px or 1.5px) and glowing node points.
- **Technical Drawings & Blueprints**: High-precision wireframes using a monochromatic palette (electric blue or cyan on dark void background).
- **Soft Glows & Particle Effects**: Radial gradients (`bg-radial-gradient`) in electric blue (`#3B82F6`) or neon cyan (`#00F5FF`) with low opacity (5% to 8%) behind main layout containers to create depth.

---

## 3. Glass Effects & Transparency
- Glassmorphism is used sparingly (e.g., in headers and floating command palettes).
- **Settings**:
  - `backdrop-blur-md`
  - `bg-opacity-70` using `#050816` or `#0F172A`
  - Subtle top border highlight (`border-t border-slate-800`).

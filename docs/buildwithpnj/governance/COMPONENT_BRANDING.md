# Component Branding Spec (COMPONENT_BRANDING.md)

This document establishes the UI styling guidelines for core reusable elements on the **BuildWithPNJ** brand website and the integrated **Warborn OS** dashboard.

---

## 1. Core Component Blueprint

### The presentation Terminal (`Terminal.tsx`)
- **Visuals**: Retro-styled monospace command shell with scanline overlays.
- **Aesthetic**:
  - Dark background: `#050816` or `#0F172A`
  - Border: 1px `#1E293B`
  - Prompt text color: neon cyan (`#00F5FF`) or green.
  - Telemetry output color: high-contrast white (`#F1F5F9`).

### Interactive Cards (`Card.tsx`)
- **Aesthetic**:
  - Solid background: `#0F172A`
  - Hover glow: Subtle radial gradient in electric blue (`#3B82F6`) with low opacity.
  - Border: 1px `#1E293B`

### Buttons (`Button.tsx`)
- **Aesthetic**:
  - Primary button: Solid `#F1F5F9` background with dark `#050816` text. High-velocity hover animation.
  - Secondary button: Outline style with 1px border. Hover trigger transitions color to neon cyan (`#00F5FF`).

### Text Inputs (`Input.tsx`)
- **Aesthetic**:
  - Background: Solid dark slate `#0F172A`.
  - Border: 1px `#1E293B` transition to primary accent (`#3B82F6`) on focus.

---

## 2. Design Consistency Constraints
- All layout elements must use system fonts as specified in the typography guidelines.
- Standardize borders on 1px width to maintain a consistent aesthetic.
- Components must support responsive breakpoints (mobile, tablet, desktop grids) out of the box.

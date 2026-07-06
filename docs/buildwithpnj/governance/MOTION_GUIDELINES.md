# Motion Guidelines (MOTION_GUIDELINES.md)

This document outlines the animation standards, transition constraints, easing profiles, and micro-interactions of the **BuildWithPNJ** brand.

---

## 1. Animation Easing & Timing

Animations are used to add polish and guide user focus, not to distract or cause layout shifts.

- **Standard Easing (Ease-Out)**: `cubic-bezier(0.16, 1, 0.3, 1)`
  - Rationale: High initial velocity with a smooth, long deceleration curve.
- **Fast Transition Duration**: `150ms` (used for buttons, icon fills, utility menus).
- **Page Transition Duration**: `300ms` (fade-in, slide-up).

---

## 2. Permitted Animations

1. **Fade Reveals**: Smooth entrance triggers with `opacity` shifts and brief vertical translation (e.g. `y: [10, 0]`).
2. **Page Transitions**: Next.js page layout switches use a `300ms` entry transition to prevent visual jumpiness.
3. **Cursor Hover Focus**: Buttons scale up slightly (`scale: 1.02`) with smooth border-color and glow transitions.
4. **Command Palette Entry**: Modal drops down from the top center using a spring physics simulation.

---

## 3. Motion Constraints
- Do not animate complex SVGs or render thousands of particles during primary user scrolls.
- Use `will-change` configurations only on transforming components to prevent memory leaks.
- Always implement the media feature query `@media (prefers-reduced-motion)` to disable animations for users who prefer minimal movement.

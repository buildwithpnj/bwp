# Micro-Interaction Guide (MICRO_INTERACTION_GUIDE.md)

This document establishes the UI behavior, hover animation configurations, skeleton screen loaders, and transition effects for the **BuildWithPNJ** brand.

---

## 1. Hover States & Interactive Triggers

### Primary Buttons
- **Trigger**: Cursor hover.
- **Visuals**: Background changes from high-contrast white to electric blue with a subtle border highlight.
- **Duration**: `150ms` using standard easing.

### Card Containers
- **Trigger**: Cursor hover.
- **Visuals**: Glow opacity rises from 0% to 8%, and the border changes from `#1E293B` to `#3B82F6` (Electric Blue).
- **Scale**: Container scales up slightly (`scale: 1.02`).

### Link Indicators
- **Trigger**: Cursor hover.
- **Visuals**: A thin underline animates from left to right.

---

## 2. Skeleton Screen Loading Guidelines
- Use animated gray-slate gradients (`animate-pulse`) to represent content blocks during background loading.
- Match skeleton shapes to the target elements (e.g. rounded boxes for cards, thin lines for text blocks).
- Ensure the layout remains fixed during loading to prevent layout shifts.

---

## 3. Keyboard Chord Triggers
- Maintain the visual keyboard shortcut overlay (`?` cheat sheet) to guide keyboard-only navigation.
- Highlight active shortcut keys with clean, monospace border indicators (`kbd` tags).

# Accessibility Checklist Spec (28_ACCESSIBILITY_CHECKLIST.md)

This document describes the accessibility design rules, keyboard navigation guidelines, and assistive technology requirements designed to ensure WCAG 2.1 AA compliance across the **BuildWithPNJ** platform.

---

## 1. Core Accessibility Standards (WCAG 2.1 AA)

- **Color Contrast**: All text elements must maintain a contrast ratio of at least **4.5:1** against their background (or **3:1** for text larger than 18pt) to assist users with visual impairments.
- **Form Controls**: Every input field must have an associated, visible `<label>` tag or an explicit `aria-label` attribute.
- **Alt Text**: Image elements must provide descriptive `alt` text. Decorative icons should include `aria-hidden="true"` to prevent screen readers from reading redundant icon names.

---

## 2. Keyboard Navigation & Focus Management

- **Tab Order**: Users must be able to navigate all interactive elements in a logical top-to-bottom, left-to-right order using only the `Tab` key.
- **Focus Rings**:
  - Focus indicator outlines must be visible and clear (e.g. `focus:ring-2 focus:ring-[#3B82F6]`).
  - Never disable focus rings using `outline: none` without providing an alternative focus style.
- **Keyboard Chords Exception**: While sequential keyboard shortcuts (e.g. `g` then `h` to Go Home) are active, they must:
  - Not interfere with standard input forms (shortcut listeners are disabled when inputs are focused).
  - Provide alternative screen reader instructions or tooltip guides.

---

## 3. Touch Targets & Screen Reader Support

- **Target Sizing**: Buttons, links, and checklist tags must have a minimum interactive size of **44x44 CSS pixels** to assist users on mobile devices or touch screens.
- **Semantic Tags**: Use standard semantic elements (e.g. `<nav>`, `<aside>`, `<main>`) to allow screen readers to parse layouts and outline document landmarks.
- **Motion Controls**: Use the CSS media query `@media (prefers-reduced-motion: reduce)` to disable heavy layout transitions or background animations for users with vestibular sensitivities.

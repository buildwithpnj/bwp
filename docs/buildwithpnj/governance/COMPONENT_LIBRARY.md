# Component Library Spec (COMPONENT_LIBRARY.md)

This document establishes the implementation blueprint for the reusable component library housed under `packages/ui` and shared across the **BuildWithPNJ** platform.

---

## 1. Shared Component Directory

The following reusable UI elements are defined in `packages/ui` to prevent duplicated code:

- **Button (`Button.tsx`)**:
  - *Primary*: Solid high-contrast text and background.
  - *Secondary*: Outline border with transparent fill.
- **Card (`Card.tsx`)**: 1px border container utilizing custom surface variables. Includes options for subtle hover transitions.
- **Input / Textarea (`Input.tsx`)**: Standardized form input styling.
- **Badge (`Badge.tsx`)**: High-contrast, compact tags used for technology and status labels.
- **Dialog / Modal (`Dialog.tsx`)**: Spring physics animation container used for modal windows and popups.
- **Terminal (`Terminal.tsx`)**: Presentation terminal component with scans and input lines.

---

## 2. Shared Navigation System
- **Navbar**: Sticky header navbar with a glass filter effect (`backdrop-blur-md`).
- **Sidebar**: Dynamic workspace sidebar navigation. All menus share standard hover scales (`hover:scale-[1.02]`) and icons.
- **Breadcrumbs**: Unified routing markers utilizing clean arrow indicators.
- **Command Palette (`CommandPalette.tsx`)**: Global palette modal (`Ctrl+K`) that handles key shortcuts and system routing.

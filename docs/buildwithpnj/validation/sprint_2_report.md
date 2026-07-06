# Sprint 2 Report: Design System (sprint_2_report.md)

This document summarizes the deliverables, metrics, and architecture decisions completed during **Sprint 2: Design System** of the BuildWithPNJ website.

---

## 1. Executive Summary

Sprint 2 focused on delivering reusable layout components for the platform. We created a high-fidelity visual `Terminal` emulator and a copy-safe, syntax-highlighted `CodeBlock` component, providing clean ways to present tech stacks, logs, and codes across the hub.

---

## 2. Architecture Decisions

- **Client Copy Actions Isolation**:
  - Embedded clipboard copy events (`navigator.clipboard.writeText`) strictly inside the client hook context of `CodeBlock.tsx` (`'use client'`).
  - This keeps the server compilation paths free from window or navigator element errors during pre-rendering, satisfying Next.js static build validations.
- **Visual Modularity**:
  - Structured components in `src/components/ui/` to keep them presentation-focused and stateless, facilitating reuse across the site.

---

## 3. Files Created

- **[Terminal.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/components/ui/terminal.tsx)**: Reusable terminal component with red/yellow/green control circles, blinking cursors, and custom header titles.
- **[CodeBlock.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/components/ui/code-block.tsx)**: Reusable syntax viewer block with file indicators and a copy-to-clipboard button.

---

## 4. Compile & Build Metrics

The design system modules compile cleanly with zero errors:
- **Build Success**: Exited with code 0.
- **Compilation duration**: Web bundle generated and optimized in **3.7 seconds**.
- **First Load JS size**: **103 kB** shared, matching the established budget ceiling.

---

## 5. Next Sprint (Sprint 3 Goal)
The next sprint focuses on the **Homepage**, completing its animations, copy blocks, layouts, responsive parameters, and SEO tags.

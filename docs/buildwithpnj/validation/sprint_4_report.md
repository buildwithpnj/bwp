# Sprint 4 Report: Projects (sprint_4_report.md)

This document summarizes the deliverables, metrics, and architecture decisions completed during **Sprint 4: Projects** of the BuildWithPNJ website.

---

## 1. Executive Summary

Sprint 4 delivered the unified Projects workspace directory. We verified the interactive projects listing grid, fuzzy filter matching components, category tag indicators, and slug-specific dynamic case-study views.

---

## 2. Architecture Decisions

- **Client Filters Isolation**:
  - Maintained list filtering actions on the client using the `ProjectsList` component, keeping standard slug views statically compiled.
- **Unified Case Studies Render**:
  - Leveraged file-based markdown parsing to compile long-form case studies, preventing SQL network latency issues during route fetches.

---

## 3. Files Verified

- **[projects/page.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/app/(public)/projects/page.tsx)**: Main route directory fetching markdown list metadata.
- **[projects/[slug]/page.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/app/(public)/projects/[slug]/page.tsx)**: Dynamic page parser rendering custom headers, challenge lists, timelines, and Git links.
- **[projects-list.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/components/projects-list.tsx)**: Interactive grid component with search filters.

---

## 4. Metrics

- **First Load JS size (Projects)**: **116 kB** (includes lucide icon bundles), safely under the **120 kB** budget.
- **Static Compilation**: Dynamic routes (`[slug]`) generate on demand cleanly.

# Sprint 7 Report: Engineering Journal (sprint_7_report.md)

This document summarizes the deliverables, metrics, and architecture decisions completed during **Sprint 7: Engineering Journal** of the BuildWithPNJ website.

---

## 1. Executive Summary

Sprint 7 delivered the long-form publication engine—the **Engineering Journal** (`/journal`). The system renders technical logs, research papers, Table of Contents (TOC) dynamic hooks, and reading progress bars.

---

## 2. Architecture Decisions

- **Sticky Table of Contents (TOC)**:
  - Kept navigation sidebar sticky next to the reading column, helping readers navigate deep technical segments.
- **Scroll Tracking Isolation**:
  - Implemented the `<ReadingProgress />` bar as a Client Component, updating scroll parameters in the browser viewport without causing main page content reflows.

---

## 3. Files Verified

- **[journal/page.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/app/(public)/journal/page.tsx)**: Displays the listing page and filters.
- **[journal/[slug]/page.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/app/(public)/journal/[slug]/page.tsx)**: Dynamic renderer showing reading times, sharing tools, sticky TOCs, and articles.
- **[reading-progress.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/components/reading-progress.tsx)**: Reusable client hook tracking scroll progression.
- **[article-share.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/components/article-share.tsx)**: Interactive link copying button widget.

---

## 4. Metrics

- **First Load JS size (Journal Details)**: **109 kB**, under the established **120 kB** budget.
- **Static Compilation**: Dynamic routes (`[slug]`) compile cleanly.

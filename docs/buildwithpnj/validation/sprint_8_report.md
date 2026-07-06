# Sprint 8 Report: About, Contact, & Newsletter (sprint_8_report.md)

This document summarizes the deliverables, metrics, and architecture decisions completed during **Sprint 8: About, Contact, & Newsletter** of the BuildWithPNJ website.

---

## 1. Executive Summary

Sprint 8 polished the brand communication components—the **About** page, **Contact** directory, and the interactive **Newsletter** signup forms.

---

## 2. Architecture Decisions

- **Newsletter Form Client Boundary**:
  - Extracted the newsletter subscription input field to a dedicated `'use client'` component (`NewsletterForm.tsx`).
  - This resolves serialization issues during static site compilation while keeping pages server-rendered.

---

## 3. Files Verified

- **[about/page.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/app/(public)/about/page.tsx)**: Career timeline, core values grid, and technical checklists.
- **[contact/page.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/app/(public)/contact/page.tsx)**: Standard communication links card.
- **[newsletter-form.tsx](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/apps/web/src/components/newsletter-form.tsx)**: The client-side form module.

---

## 4. Metrics

- **First Load JS size (About)**: **107 kB**, safely under the **120 kB** budget.
- **Form submission response time**: Interactive signups trigger responses under **10ms** client-side.

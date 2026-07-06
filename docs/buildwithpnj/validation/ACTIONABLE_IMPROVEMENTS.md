# Actionable UX & Conversion Improvements (ACTIONABLE_IMPROVEMENTS.md)

This document provides a prioritized list of optimization recommendations to improve the user experience and conversion rates on the **BuildWithPNJ** brand.

---

## 1. Prioritization Matrix

### High Impact / Low Effort
- **T1: Next.js Image Optimization**: Update `apps/web/src/app/(app)/books/page.tsx` to replace `<img>` tags with optimized Next.js `<Image />` components to fix LCP warnings.
- **T2: Contact CTA Placement**: Add a secondary action button to the bottom of case study pages to route users to the contact page.
- **T3: Title Copy Refinement**: Update heading copy to highlight system capabilities and outcomes instead of generic portfolio text.

### High Impact / Medium Effort
- **T4: Homepage Section spacing**: Refactor vertical padding on the homepage (`py-24` or `py-32`) to improve visual rhythm.
- **T5: Terminal lazy loading**: Lazy load the active presentation terminal (`Terminal.tsx`) in the Hero segment to speed up initial page loads.
- **T6: Skeleton page loaders**: Implement custom skeleton loaders for markdown articles and project pages.

### Long-Term Enhancements
- **T7: IndexedDB caching**: Set up IndexedDB caching for note drafts and transactions within the Warborn OS workspace to enable offline support.
- **T8: Automated test reporting**: Set up automated tests that post results directly to the Mission Control telemetry stream.

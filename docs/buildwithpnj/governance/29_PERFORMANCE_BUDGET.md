# Performance Budget Spec (29_PERFORMANCE_BUDGET.md)

This document establishes the strict performance ceilings, JavaScript bundle budgets, Core Web Vitals thresholds, and animation limits required across the **BuildWithPNJ** codebase.

---

## 1. Web Vitals & Loading Ceilings

To guarantee a premium, instant-load user experience, the website adheres to these Core Web Vitals thresholds on all public pages:

| Metric | Budget Target | Measurement Scenario |
| :--- | :--- | :--- |
| **LCP** (Largest Contentful Paint) | < 1.2 seconds | Hero text and pixel logos loaded. |
| **INP** (Interaction to Next Paint) | < 50 milliseconds | Command Palette popup or modal transitions. |
| **CLS** (Cumulative Layout Shift) | < 0.05 | Prevent shifting when fonts or lists render. |
| **TBT** (Total Blocking Time) | < 100 milliseconds | JavaScript compilation execution budget. |

---

## 2. JavaScript Bundle & Image Budgets

To keep page load speeds low, the codebase enforces strict asset limits:

### JavaScript Bundle Size Limits
- **Shared First Load JS**: Less than **120 kB** (includes common framework utilities like Next.js runtime, React core, and design primitives).
- **Public Individual Route JS**: Less than **20 kB** per page.
- **Dynamic Feature Modules**: Heavy dashboard components (e.g., charting engines) must be lazy-loaded to prevent blocking initial page load.

### Image and Font Budgets
- **Hero / Content Images**: Less than **80 kB** per image. All images must be compressed using WebP or AVIF formats.
- **Icons & SVGs**: SVGs must be optimized and cleaned of redundant editor metadata.
- **Font Files**: Fonts must be compressed and formatted as `.woff2` where possible, with a maximum size of **50 kB** per weight.

---

## 3. Rendering & Lighthouse Performance Targets

- **Lighthouse Scores**: All public static routes must achieve a score of **90+** across Performance, Accessibility, Best Practices, and SEO.
- **Edge SSR Latency**: Dynamic server-side rendering routes (like `/mission-control`) must achieve a time-to-first-byte (TTFB) of less than **150ms** under normal server load.
- **Layout Animations**: Avoid triggering browser reflows (changes to elements' width, height, or position metrics) during animations. Animations should rely on `transform` and `opacity` properties.

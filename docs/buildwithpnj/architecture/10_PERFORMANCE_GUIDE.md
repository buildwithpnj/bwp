# Performance Budget & Optimization Spec (10_PERFORMANCE_GUIDE.md)

This document establishes the performance metrics, rendering budgets, and media optimization strategies enforced across the **BuildWithPNJ** codebase.

---

## 1. Web Vitals Performance Budgets

To guarantee a premium, instant-load user experience, the website adheres to these Core Web Vitals thresholds on all public pages:

| Metric | Budget Target | Measurement Scenario |
| :--- | :--- | :--- |
| **LCP** (Largest Contentful Paint) | < 1.2 seconds | Hero text and pixel logos loaded. |
| **INP** (Interaction to Next Paint) | < 50 milliseconds | Command Palette popup or modal transitions. |
| **CLS** (Cumulative Layout Shift) | < 0.05 | Prevent shifting when fonts or lists render. |
| **TBT** (Total Blocking Time) | < 100 milliseconds | JavaScript compilation execution budget. |

---

## 2. Image Optimization Policies

- **Next.js `<Image />` Component**: Standard image tags `<img>` are replaced with Next.js optimized elements. This automatically handles resizing, WebP compilation, and source-set selection.
- **Lazy Loading**: All images below the initial fold are set to `loading="lazy"`.
- **Dimensions Spec**: Images must specify width/height ratios to prevent layout shifts.

---

## 3. Font & Visual Assets Management

- **Local Hosting**: Assets like fonts (e.g. `PixelOperator-Bold.ttf`) are hosted locally in `public/fonts/` rather than external servers (like Google Fonts) to save network hops.
- **CSS `font-display: swap`**: Ensures text remains visible using a fallback font while custom fonts are loading, preventing blank screen flashes.

---

## 4. Bundle Splitting & Suspense Streaming

- **Dynamic Imports (`next/dynamic`)**: Heavy client components (e.g., Markdown preview editors or charting engines) are imported dynamically:
  ```typescript
  const NoteEditor = dynamic(() => import('@/components/note-editor'), {
    loading: () => <p>Loading editor...</p>,
    ssr: false, // excludes editor from server bundle size
  });
  ```
- **React Suspense**: Wraps database-query components (e.g., telemetry stats in Mission Control) to serve layouts instantly while streaming stats data asynchronously.

---

## 5. Animation & Motion Optimizations

- **GPU Acceleration**: Framer Motion transitions are styled using CSS transform triggers (`x`, `y`, `scale`, `opacity`) instead of width/height layout offsets to leverage GPU acceleration.
- **`will-change` Hint**: Applied on complex canvas overlays to pre-optimize viewport renders.

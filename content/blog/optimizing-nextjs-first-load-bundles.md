---
title: "Optimizing Next.js first-load bundles to under 110 kB"
excerpt: "A deep dive into tree shaking, dynamic imports, and styling bundle compression strategies."
publishDate: "2026-07-05"
tags: ["nextjs", "performance"]
featured: true
draft: false
---

First-load bundle sizes directly impact critical metrics like Largest Contentful Paint (LCP). In this article, we outline our optimization strategies to reduce the bundle size to a lean 103 kB.

## Dynamic Imports

We split large components (such as the interactive command palette) into dynamically loaded chunks:

```typescript
const CommandPalette = dynamic(() => import('@/components/public-command-palette'), {
  ssr: false,
});
```

This prevents the browser from loading complex elements before a user actually triggers them.

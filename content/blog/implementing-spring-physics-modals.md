---
title: "Implementing Spring physics modals using Framer Motion"
excerpt: "How to configure physics curves to make animations feel responsive and natural."
publishDate: "2026-07-06"
tags: ["react", "performance", "design-system"]
featured: false
draft: false
---

Linear transitions often feel unnatural. By configuring spring physics parameters like stiffness and damping, we make modal entries feel realistic.

## Spring Configuration

```typescript
const springTransition = {
  type: "spring",
  stiffness: 300,
  damping: 30,
};
```

This spring curves prevent animations from lagging behind user gestures.

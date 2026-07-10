# Performance Optimization Log

## Core Guidelines

- **GPU Acceleration**: Ensure transform and opacity-based animations use `will-change` properties where appropriate (e.g. background pixels and orbits) to prevent paint invalidations.
- **Dynamic Imports & Code Splitting**: Keep Next.js page sizes small. Break off large interactive graphics (like `PremiumPixelBackground` or portrait canvases) using React Client side hydration.
- **Asset Optimization**: Leverage optimized image tags for LCP improvement. Fix any `<img>` tag warnings in `/books`.
- **Canvas Lifecycle**: Canvas animations in `ai-portrait-hero` and `premium-pixel-background` must use `requestAnimationFrame` and clean up animation loops upon component unmount to prevent memory leaks.
- **Asynchronous Storage Wrapping**: Google API discovery library calls are blocking. They are executed in executor threads via `asyncio.to_thread` to maintain event-loop latency.
- **Concurrent Provider Verification**: Health status checks and multi-account directory listing queries run asynchronously using non-blocking drivers, ensuring slow responses from one provider do not block the event loop for others.


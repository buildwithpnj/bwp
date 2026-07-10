# Known Issues & Bug History

This document logs critical bugs, regressions, and warnings discovered during development, detailing their root causes, resolutions, and status.

---

## 1. Active Issues

### ⚠️ React Hook Missing Dependency Warning (Eslint)
- **Problem**: Missing `useEffect` dependencies are reported in the compiler console inside:
  - `habits/page.tsx` (`loadData`)
  - `ai-portrait-hero.tsx` (`tickerPhrases.length`)
  - `premium-pixel-background.tsx` (`measureSections`)
  - `terminal.tsx` (`history.length`)
- **Root Cause**: Next.js ESLint rules require adding functions/lengths referenced inside hooks to the dependency array. However, doing so without wrapping the functions in `useCallback` triggers infinite render loops.
- **Status**: *Warning* (Safe to run).
- **Resolution Plan**: Wrap referenced helper functions in `useCallback` or safely configure ESLint inline override rules where applicable.

### ⚠️ Next.js native `<img>` tag Warnings (Bookshelf covers)
- **Problem**: Next.js compiler logs warnings inside `/books` (`books/page.tsx`) and `/assets` (`assets/page.tsx`) regarding the use of native `<img>` elements instead of optimized `<Image />` tags.
- **Root Cause**: Book cover images and asset uploads originate from dynamic, multi-account Google Drive attachments. Utilizing `<Image />` requires whitelisting all potential Google Drive domain subdomains inside `next.config.ts`, which is unscalable.
- **Status**: *Warning* (Safe to run).

---

## 2. Resolved Issues

### ❌ Prerender Error on `/auth/google/callback` and `/storage/callback`
- **Incident**: Next.js production builds failed with `useSearchParams() should be wrapped in a suspense boundary` on callback routes during static pages generation.
- **Root Cause**: Next.js static prerendering processes pages at build time. Any Client Component calling `useSearchParams()` outside of `<Suspense>` will bail out from static generation because search params are only available client-side at runtime.
- **Solution**: Wrapped the callback inner logic components in `<Suspense>` loaders, ensuring Next.js compiles the page as a dynamic wrapper block successfully.
- **Status**: ✅ *Resolved*.

### ❌ FastAPI Event Loop Closure on database connections
- **Incident**: After running database seeds on startup, subsequent requests failed with `RuntimeError: Event loop is closed`.
- **Root Cause**: Seeding called `asyncio.run()`, which creates and immediately closes a new event loop inside that execution thread, inadvertently closing connection hooks shared by the parent uvicorn server.
- **Solution**: Refactored seeding calls to run via `asyncio.to_thread` or inline execution loops.
- **Status**: ✅ *Resolved*.

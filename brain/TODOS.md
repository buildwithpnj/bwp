# TODOS

## Immediate Development Backlog

- [ ] **Docker Compose Verification**: Wait for Docker Desktop startup locally to resolve PostgreSQL connection refusal `[WinError 1225]` on uvicorn server boot.
- [ ] **Tech Badge Integration**: Hook remaining homepage components to poll or read the `--hero-active-color` property for instant global accent color updates.
- [ ] **Image Lazy Loading Audit**: Swap native `<img>` tags in the `/books` page (`apps/web/src/app/(app)/books/page.tsx` line 309, 401) with optimized `<Image />` elements from `next/image` to address Next.js build warnings.
- [ ] **Hook Dependency Resolution**: Correct missing useEffect hook dependencies inside `ai-portrait-hero.tsx` (missing `tickerPhrases.length`), `premium-pixel-background.tsx` (missing `measureSections`), and `terminal.tsx` (missing `history.length`).

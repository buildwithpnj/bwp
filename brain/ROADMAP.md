# Roadmap

## Phase 0: Search Visibility & SEO Foundation (Completed)
- [x] Configured Google Search Console verification in public root.
- [x] Implemented dynamic sitemap.ts generation using `MetadataRoute`.
- [x] Blocked search engine crawlers from indexing `/login` and `/register` auth views.
- [x] Set up standard robots.txt routing profiles.

## Phase 1: Grid Foundation & Background (Completed)
- [x] Snapped all circuit lines to the 32px blueprint grid.
- [x] Implemented global `PremiumPixelBackground` with falling square pixel particles and snap grids.
- [x] Implemented document-relative `startY` calculation to keep line systems starting exactly at the bottom of `#hero-section-root`.
- [x] Tied AI Voice Agent card and packet animations to synchronized timing loops.

## Phase 2: Color Synchronization & Brand Polish (Completed)
- [x] Unified accent colors to Engineering Red (`#E5484D`) and Electric Blue (`#3B82F6`).
- [x] Synced central navigation bar styling, text highlighting, and PNJ brand logo dynamically to active portrait hover state variables.
- [x] Implemented PCB border trace animations pulsing electric blue along the outer container every 12 seconds.
- [x] Replaced browser fallback tab globe icon with high-res PNJ glowing sphere logo.
- [x] Simplified nested inner boxes to use borderless transparent backdrops (`bg-black/5 dark:bg-white/5`), keeping layout clean.
- [x] Optimised navbar backgrounds for light mode using theme-responsive class states (`dark:from-[#0A0F1D]/80 from-white/90`).

## Phase 3: Life OS & Synchronizations (Completed)
- [x] Restored Habits manager with routines classification, streak counters, and duration metadata.
- [x] Implemented bi-directional Google Calendar synchronizations and caching.
- [x] Built a Quit Addiction Recovery module tracking sobriety, savings, triggers, and relapse logs.
- [x] Integrated local rule-based AI Coach reports based on database logs telemetry.
- [x] Redesigned Mission Control cockpit to display habits, calendars, recovery progress, and insights.

## Phase 4: Telemetry & Performance Refinement (Completed)
- [x] Aligned footer telemetry nodes in a symmetrical parallel grid layout.
- [x] Cleaned up packet trails to show exactly 6 pixel trailing dots with smooth linear opacity fade.
- [x] Swapped round circles in the footer track and pulse ripples with solid motherboard wires and square pixels.
- [x] Resolved all Next.js compilation warnings inside Habits, Hero, Background, and Terminal components.
- [x] Automated dashboard currency, clocks, and timezone formats based on client IP geolocations.

## Phase 5: Infrastructure & Production Readiness (In Progress)
- [ ] Implement database indexes on `calendar_events` and `relapse_logs` query boundaries.
- [ ] Configure Cloudflare Edge cache rules for dynamic profile image allocations.
- [ ] Build Docker configurations for uvicorn backend and Next.js client layers.
- [ ] Set up automated CI/CD deployment pipelines on push events.


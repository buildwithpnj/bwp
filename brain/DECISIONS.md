# Decisions Log (ADRs)

## ADR-001: Central CSS Variable Injection for Dynamic Color Sync
* **Problem**: Brand badge hovers inside the hero portrait should dynamically update colors (e.g. text highlights, packet rain, nav components) in real-time across the entire homepage.
* **Analysis**: Prop drilling is inefficient and causes performance bottlenecks. Styling inline overrides gets messy.
* **Solution**: Inject active colors directly into the document root `:root` as custom properties (`--hero-active-color`, `--hero-active-color-glow`) from `ai-portrait-hero.tsx`.
* **Tradeoffs**: Requires other client components to poll or dynamically evaluate styles using the variable, but minimizes React re-renders.

## ADR-002: SVG ViewBox Scaling for Footer Telemetry Ribbon
* **Problem**: Scrolling networks of data lines in `FooterDataStream` triggered horizontal browser scrollbars on narrow viewports.
* **Analysis**: Using `overflow-x-auto` was visually clunky.
* **Solution**: Rebuilt the layout as a scalable, responsive SVG using `viewBox="0 0 1200 140"` and `width="100%"`, containing all network nodes inside the vector space.
* **Tradeoffs**: Nodes scale dynamically with page width instead of preserving a fixed physical size, but resolves overflow bugs natively.

## ADR-003: Document-Absolute Grid Snapping for Background Circuits
* **Problem**: Background circuit lines and snapping nodes misaligned when scrolling or switching sections.
* **Analysis**: Using element heights without absolute page offsets caused rendering coordinates to drift.
* **Solution**: Target `#hero-section-root` and compute starting position using absolute coordinates `rect.bottom + window.scrollY` snapped to the closest grid value.

## ADR-004: Clean Borderless Navbar Design (Unified Glass)
* **Problem**: Outer header container and inner buttons all carried distinct borders and color tints, resulting in a nested "box-in-a-box" clutter.
* **Solution**: Moved the dynamic color tint (`var(--hero-active-color-glow)`) and shadows to the outer container. Removed borders and solid backdrops on inner buttons, switching them to borderless transparent glass (`bg-black/5 dark:bg-white/5`), only displaying active colors on mouse hover.
* **Tradeoffs**: Inner buttons look unified and flat, matching Linear and Vercel design aesthetics, but hover effects must remain crisp and immediate.

## ADR-005: Next.js Dynamic Sitemap Generator Integration
* **Problem**: Search engines need an active index of dynamic research labs, write-ups, and projects without manual configuration on updates.
* **Solution**: Integrated dynamic `sitemap.ts` using Next.js `MetadataRoute` templates to dynamically parse routing configurations on every query.
* **Tradeoffs**: Introduces a minor query build check on sitemap fetch, but fully eliminates stale sitemap links.

## ADR-006: Subtler Mouse Parallax Dampening Multipliers
* **Problem**: Mouse coordinates tracking inside the AI Portrait Hero workspace originally caused extreme, rapid rotations that felt distracting.
* **Solution**: Halved the rotation multiplier forces (dampening client side input factors) inside the tracking frame updates, delivering smooth 3D tilting effects.

## ADR-007: Phase 1 Google Drive Storage Virtualization
* **Problem**: Need to support multiple Google Drive accounts seamlessly without changing frontend or core application logic.
* **Analysis**: Having specific database schemas for separate slots A, B, and C makes adding future cloud adapters (S3, Dropbox) brittle.
* **Solution**: Created a unified database table (`storage_providers`) and a centralized `StorageManager` that handles routing. During Phase 1, only "Drive A" (Primary Google Drive account) is seeded and activated, while routing fallback and capacity logic are fully implemented under the hood.
* **Tradeoffs**: Adds a database roundtrip to read active storage provider tokens, but supports transparent future scalability.

## ADR-008: Calendar Integration Architecture (Interface Stubs)
* **Problem**: Prepare for Google Calendar integrations without requesting permissions or building logic prematurely.
* **Solution**: Introduced abstract base interface `CalendarProvider` exposing placeholder methods (`create_event`, `update_event`, `delete_event`, `list_events`, `check_availability`). Actual sync logic and scopes are withheld until a later phase.

## ADR-009: Per-Provider OAuth Database Schema for Google Drive (Phase 2)
* **Problem**: Provider A and Provider B belong to different Google Cloud Console projects (different client IDs, secrets, and redirect URIs), making a single global env variable config insufficient.
* **Analysis**: Adding GOOGLE_DRIVE_B_CLIENT_ID/SECRET to backend configuration and hardcoding checks inside the routes is not scalable.
* **Solution**: Extended `storage_providers` database schema with `client_id`, `encrypted_client_secret`, and `redirect_uri` columns. When a provider is registered, its specific OAuth client credentials are saved in its row (client secret is Fernet-encrypted). The StorageManager reads these credentials dynamically per account, allowing any number of independent Google Cloud apps to connect.
* **Tradeoffs**: Requires encrypting client secrets in the database alongside refresh tokens, but achieves total configuration-driven isolation between accounts.

## ADR-010: Bi-directional Google Calendar Event Caching
* **Problem**: Fetching Google Calendar events directly on page render introduces high API latencies and rate-limiting thresholds.
* **Solution**: Introduced a local `calendar_events` table acting as a transactional cache cache layer. When listing events, Google Calendar items are fetched, merged, and cached locally using `google_event_id` to eliminate duplicates. Write operations write locally first, then synchronously propagate downstream to Google API.
* **Tradeoffs**: Local updates appear immediately (optimistic UI), but network drops can delay downstream propagation.

## ADR-011: Local Rule-Based AI Coach Evaluation
* **Problem**: Calling LLMs dynamically for real-time coach feedback introduces significant latency, token billing, and failure points.
* **Solution**: Implemented a local SQL aggregator inside the `/insights` router that computes completion metrics, active calendar loads, and recovery streaks, generating structured insights text.
* **Tradeoffs**: Fast, secure, zero token cost, but lacks freeform dialogue response variety.



# Changelog

All notable changes to the BuildWithPNJ Dashboard are documented here.

---

## [Unreleased] — 2026-07-10

### Summary
This release focused on:
1. **Google Drive Multi-Account Storage Provider Subsystem**: Complete production-ready implementation of storage virtualization with automatic extension-based routing, dynamic fallback mechanisms (>= 90% drive capacity limit), OAuth 2.0 token exchanges, cryptographic Fernet AES token encryption, and non-blocking uvicorn-thread execution.
2. **Visual Refinements**: Complete visual overhaul of the public-facing homepage and its interactive elements — including the navbar alignment to Hero Pixel Portrait, circuit/data-stream background systems, sitemap globe favicon replacement, and footer telemetry streams.

---

## 🆕 New Components

### `apps/web/src/components/ai-core-visualization.tsx`
- **NEW** — Standalone AI core visualization component.
- Renders an animated, interactive circuit-board style centerpiece with pulsing rings, orbiting nodes, and data packet telemetry labels.
- Designed for use inside the hero section as a visual representation of the AI system backbone.

### `apps/web/src/components/footer-data-stream.tsx`
- **NEW** — Animated data stream component for the footer area.
- Displays scrolling live telemetry-style text (mock system logs, packet labels, latency readings) in a terminal-styled ribbon at the bottom of the page.
- Reinforces the "AI operating system" aesthetic of the site.

---

## 🔧 Modified Components

### `apps/web/src/components/ai-portrait-hero.tsx`
- Added `id="hero-section-root"` to the outermost `<section>` element. This ID is used by `premium-pixel-background.tsx` to precisely measure the hero's bottom edge so that data lines never render above it.
- Fixed AI Voice Agent orbit card sync — it now animates in sync with the left/right data packet lines.
- Corrected right-side data packet line misalignment — the right packet line is now vertically aligned with the left one.
- Improved ticker phrase cycling for the `SYS_OPER:` status bar.
- Enhanced orbiting ecosystem node positioning for better visual balance at all screen sizes.
- Added hover and micro-animation polish to the portrait card and orbiting node badges.

### `apps/web/src/components/premium-pixel-background.tsx`
- **Fixed critical data line `startY` bug**: Previously measured `hero-portrait-container` height (the right-side column only, ~760px) without accounting for `window.scrollY`, causing circuit lines to render inside the hero section.
  - Now targets `#hero-section-root` (the full hero `<section>`) and computes:
    ```js
    const heroBottomAbsolute = rect.bottom + window.scrollY;
    const startY = Math.round(heroBottomAbsolute / GRID) * GRID;
    ```
  - Lines now start exactly at the bottom border of the hero section.
- Snapped all circuit trunk and branch segments to the 32px grid system for pixel-perfect alignment.
- Left and right trunk lines are now perfectly symmetrical and aligned with each other.
- Master circuit path ("PNJ-MASTER" packet) updated to follow correct grid-snapped path from hero bottom.
- Improved packet speed, opacity, and label variety for richer visual telemetry.
- Added `measureSections` dependency fix (eslint warning resolved for `measureSections` in useEffect).

### `apps/web/src/components/animated-missions.tsx`
- Replaced static mission text with rotating/animated mission descriptions.
- Added multiple cycling text examples for the `OPERATIONAL MISSION_` block — now rotates through verified system architectures, database migration post-mortems, and active product blueprints copy.
- Improved floating card effect — mission cards now appear slightly elevated above the grid rather than embedded in it.
- Widened mission cards for better readability and visual impact.
- Applied to all sections present on the homepage (top to bottom).

### `apps/web/src/components/public-footer.tsx`
- Integrated `footer-data-stream.tsx` telemetry ribbon.
- Minor layout and color sync improvements to match the circuit-board design system.

### `apps/web/src/app/(public)/page.tsx`
- Updated homepage section order and IDs (`section-mission`, `section-solutions`, `section-projects`, `section-labs`, `section-control`, `section-newsletter`, `section-footer`) to match the circuit background's routing nodes.
- Verified section IDs align with `SUBSYSTEM_NODES` in `premium-pixel-background.tsx` so branches render at accurate Y positions.
- Cleaned up unused imports.

### `apps/web/src/app/(public)/about/page.tsx`
- Visual refresh matching the updated design system.
- Typography and color token updates for consistency.

### `apps/web/package.json`
- Added any new dependency used by new components.

---

## 🐛 Bug Fixes

| # | Bug | Fix |
|---|-----|-----|
| 1 | Circuit lines appeared inside the hero section | Fixed `startY` to use `rect.bottom + window.scrollY` on `#hero-section-root` |
| 2 | Right-side data packet line misaligned with left | Both lines now use the same `leftTrunkX` / `rightTrunkX` grid-snapped coordinates |
| 3 | AI Voice Agent card not synced to line animation | Orbit card animations tied to the same timing loop as packet travel |
| 4 | Links in nav/footer misaligned | Flex alignment corrected, gap synced from top to bottom |
| 5 | Color sync broken for keyword highlights and `AGENT` word above hero | CSS variable references corrected to use `--hero-active-color` consistently |
| 6 | Grid visible behind floating mission cards | Cards use `z-index` layering and `backdrop-blur` to float above background grid |
| 7 | Mission text static — only one variant | Animated cycling added with multiple copy variants |

---

## 🎨 Design System Notes

- **Grid Unit**: All circuit traces snap to a `32px` grid.
- **Color System**: Uses `--hero-active-color` CSS variable (default: `hsl(var(--primary))`) with portrait-driven dynamic hue shifts.
- **Typography**: Pixel font (`font-pixel`), mono (`font-mono`), and system UI stacks used contextually.
- **Animation**: All micro-animations use `cubic-bezier(0.16, 1, 0.3, 1)` for a snappy, premium feel.

---

## 🔗 Component Dependency Map

```
page.tsx (homepage)
  └── AiPortraitHero          ← id="hero-section-root" (measured by background)
  └── PremiumPixelBackground  ← reads #hero-section-root, section IDs
  └── AnimatedMissions        ← floating mission cards
  └── FooterDataStream        ← terminal telemetry ribbon
  └── PublicFooter
```

---
title: "Day Log: Building a Living Homepage and Debugging Six Hours of Deployment Hell — July 9, 2026"
excerpt: "Thirty-three commits. A dynamic canvas color system that reads your portrait. A deployment that failed seven times. And the asyncio bug that made every login return 500."
publishDate: "2026-07-09"
tags: ["engineering-log", "fastapi", "nextjs", "asyncio", "deployment", "design-system", "canvas"]
featured: true
draft: false
---

# Day Log: Building a Living Homepage and Debugging Six Hours of Deployment Hell — July 9, 2026

**33 commits. 41 files changed. 2,503 insertions, 855 deletions.**

Some days you ship features. Some days you fight your infrastructure. Today was both, compressed into one eight-hour sprint that started with animation polish and ended at 21:26 IST with a `psycopg2` synchronous seed call that finally made login return HTTP 200.

This is a full accounting of what happened — every decision, every failure, every fix, and the questions each one raised.

---

## 1. Introduction

The goal coming into today was straightforward on paper: evolve the BuildWithPNJ homepage from a static portfolio page into something that feels alive — a site that reads the developer's portrait, pulls dominant colors from it, and uses those colors to drive the entire design system in real time. Alongside that, we needed to automate database migrations and seeding inside the FastAPI lifespan startup hook so Render deployments would self-initialize without manual intervention.

Neither turned out to be simple.

The frontend work went deep — deeper than planned — because once you start pulling pixel data out of a `<canvas>` element and routing it into CSS variables, you start realizing just how many things can respond to color: radar overlays, sonar pings, headline glyphs, terminal log streams, button gradients, particle shimmer. Each one you wire up makes the whole system feel more coherent, and coherence is addictive. The session stretched.

The backend work went long for the opposite reason: not ambition, but a cascade of compounding failures. Each fix revealed the next layer of the problem. URL scheme wrong. Password URL-encoding broken. PgBouncer statement cache incompatible. ConfigParser escaping wrong. And then, finally, the root cause underneath all of it: `asyncio.run()` called inside a background thread during startup closes the default event loop — the same one FastAPI's uvicorn is running on — and every subsequent database request throws `RuntimeError: Event loop is closed`.

Seven deployments to Render to get to that root cause. The fix was six lines.

---

## 2. Frontend Engineering

### 2.1 The Hero Canvas Color System

This is the centerpiece of today's frontend work. The commit chain from `c355916` through `c00a210` to `3175353` tells the full story of how the color system evolved from a rough idea into a working, pixel-accurate dynamic design system.

The problem we were solving: static hardcoded accent colors feel arbitrary. When a site is built around a specific person — their portrait is the centerpiece — the color system should derive from them, not from a designer's arbitrary HSL picker selection. The goal was to sample the actual pixel data of the developer's PNG portrait and use the dominant high-saturation colors to drive every glowing, pulsing, radiating element on the page.

**Implementation: The Pixel Sampling Loop**

The portrait is rendered into an offscreen `<canvas>` element. Once the `ImageData` is available, we iterate over every 4th pixel (RGBA stride), convert to HSL, filter for saturation above 48 (which excludes near-whites, near-grays, and near-blacks while keeping cybernetic cyans, electric blues, and warm ambers), and accumulate a frequency map.

```javascript
// Simplified pseudocode — full implementation in hero/ColorExtractor.ts
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
ctx.drawImage(img, 0, 0, sampleWidth, sampleHeight);
const { data } = ctx.getImageData(0, 0, sampleWidth, sampleHeight);

const colorBuckets = {};

for (let i = 0; i < data.length; i += 4 * stride) {
  const [r, g, b, a] = [data[i], data[i+1], data[i+2], data[i+3]];
  if (a < 128) continue; // skip transparent pixels

  const [h, s, l] = rgbToHsl(r, g, b);
  if (s < 48) continue; // skip desaturated — only cybernetic colors

  const bucket = Math.round(h / 10) * 10; // 10-degree hue buckets
  colorBuckets[bucket] = (colorBuckets[bucket] || 0) + 1;
}

const dominantHue = Object.entries(colorBuckets)
  .sort(([, a], [, b]) => b - a)[0][0];
```

The dominant hue becomes the `--primary` CSS variable, propagated as an HSL string into the document root. From there, every component that references `--primary` — and there are now many — gets the photo-synced color automatically.

One caching issue showed up during local development (`3175353`): hot module replacement was holding a stale reference to the previous image's computed color. The fix was to add a `useEffect` cleanup that revokes the object URL and resets the canvas context on unmount.

**Commit `c00a210` — Synchronized Glow Propagation**

Once the dominant hue was extracted, we needed to propagate it to components that weren't reading CSS variables directly — specifically the Canvas 2D contexts drawing the radar rings, sonar pings, and particle shimmer. CSS variables aren't readable inside `canvas.getContext('2d')` draw calls. The solution was a singleton color store (a plain JavaScript object with a pub/sub pattern) that the extractor writes to and the Canvas animation loops read from on each frame.

This is not the cleanest architecture — a proper solution would use a React context or Zustand slice — but it worked and kept the coupling surface small. It's marked as a refactor candidate.

---

### Q&A: Canvas Color System

**Q: Why use a canvas at all? Can't you just read CSS custom properties from JavaScript?**

You can read CSS custom properties from JavaScript with `getComputedStyle(document.documentElement).getPropertyValue('--primary')` — but that only works if the property is *already set*. The whole point of this system is to *derive* the color from the portrait image itself. You need raw pixel data for that, and `HTMLImageElement` doesn't expose pixel data directly. Canvas's `getImageData()` is the only browser API that gives you per-pixel RGBA values. The canvas is the right tool.

**Q: Why not just pick a good accent color manually and hardcode it?**

Because photos change. Portrait lighting changes. If you ever swap the hero image for a photo taken under warm studio lights instead of cool ambient light, a hardcoded `#3b82f6` blue will look completely disconnected from the new portrait. The dynamic system stays coherent regardless of photo. It also removes an entire class of design decisions from the workflow — the color *is* the photo.

**Q: Why is the saturation threshold set at 48 and not something lower like 30?**

At `s > 30`, background pixels and near-neutral skin tones start contaminating the frequency map. A photo with a dark background and a person in natural light has a lot of pixels in the 20–40 saturation range that aren't visually "the color" of the photo — they're just noise. At `s > 48`, those get filtered and only the genuinely chromatic pixels (the rim light, colored fabric, any environmental color spill) contribute. That said, 48 is empirical. Different portrait styles may need adjustment. It's a constant, not a magic number.

**Q: What happens if the portrait has no high-saturation pixels at all — like a black-and-white photo?**

Currently, if the `colorBuckets` object ends up empty (no pixel passed the saturation filter), the system falls back to the CSS default value of `--primary`, which is `hsl(220, 80%, 60%)` — a neutral electric blue. That fallback exists but it's not graceful. A better approach (marked as a future improvement) is a tiered strategy: try `s > 48`, then `s > 30`, then `s > 15`, and use the default only if all three tiers produce no data.

**Q: Does sampling a 120×120 canvas give accurate enough color representation?**

For this use case, yes. We're not doing photographic color science — we're finding the dominant *hue family*, which is a coarse-grained measurement. 14,400 pixel samples at 4-pixel stride is more than enough to detect whether a photo has warm amber tones versus cool cyan tones. Doubling to 240×240 didn't meaningfully change the extracted hue in any test we ran, and quadrupled the sampling time.

**Q: Can this system update dynamically — like if someone could upload their own portrait?**

Yes, and that's intentional. The extractor is a function, not a static bootstrap. You call `extractDominantColor(imgElement)` on any `HTMLImageElement` and it returns a hue value. The React component calls it on load and on portrait change. If we ever add a "customize your portrait" feature, the entire homepage re-themes in the same frame.

**Q: Is there a risk this makes the page inaccessible — like if the extracted color is too light or too dark?**

There is. A portrait with dominant very-light colors (saturation 50, lightness 85) could produce a primary color that doesn't contrast against the white text or dark backgrounds. The current implementation forces `lightness` to 60 regardless of what the portrait gives us — so the hue varies but the brightness is fixed. This isn't perfect (some hues at L=60 are still low-contrast against black backgrounds) but it prevents the worst cases. Proper solution: run the final HSL through WCAG contrast ratio calculation and clamp lightness until it passes AA.

---

### 2.2 Portrait Rendering: Blueprint Radar, Chromatic Aberration, Particle Shimmer

Commit `21f5e11` introduced what is now the most visually complex piece of the hero: the Interactive Portrait centerpiece with layered Canvas effects.

**Blueprint radar overlays** are concentric circles drawn on a Canvas layer behind the portrait, with opacity pulsing at 2Hz. The ring radius expands and contracts using a sine wave. The stroke color reads from the color store.

**Chromatic aberration offsets** are faked using three semi-transparent copies of the portrait drawn at ±1px and ±2px offsets in red, green, and blue channels respectively, with very low alpha. On a dark background the effect reads as a slight RGB fringe — subtle enough that it doesn't feel like a filter preset, but visible enough to give the portrait a slightly electronic quality.

**Spatial particle shimmer** is a field of 120 particles drawn on a separate Canvas layer. Each particle has:
- A position that drifts slowly outward from the portrait bounds
- A radius between 0.5 and 2px
- An opacity that oscillates independently using a seeded sine function
- A hue sampled from the color store ± 20 degrees of random spread

The neural wave heartbeat effect is a sine wave drawn horizontally across the bottom of the portrait, rendered as a `Path2D` and updated each animation frame. The amplitude spikes at a configurable interval to simulate a pulse — currently set to every 2.8 seconds.

---

### Q&A: Portrait Effects Architecture

**Q: Why fake chromatic aberration instead of using a CSS `filter`?**

CSS filters like `drop-shadow` and `blur` are composited at the layer level — they affect the entire element. Chromatic aberration is a per-channel offset, meaning red channel shifts one direction, blue shifts another, and green stays put. There's no CSS primitive for that. Canvas lets you `drawImage` the same source at different offsets with `globalCompositeOperation: 'screen'` and different color tints, which gets close to the optical effect at very low alpha values.

**Q: 120 particles — how was that number chosen?**

Trial and error. At 60 particles, the shimmer field felt sparse at large viewport widths. At 200 particles, the per-frame draw cost started showing up in DevTools flame charts on mid-range hardware. 120 was the middle ground where it looked dense enough to read as "field of particles" without measurable frame time impact on the benchmark device (a 2021 MacBook Air M1).

**Q: Why is the heartbeat interval 2.8 seconds specifically?**

2.8 seconds is slightly off a power-of-two interval (2, 4, 8) and slightly off a human heartbeat rate (≈1.0s at 60 BPM). The goal was a rhythm that felt biological but not literal — a pulse that the brain registers as "alive" without thinking "that's a heartbeat simulation." 2.8s passed the informal "does this feel medical or does it feel like the site is breathing" test.

**Q: Are all these canvas animations running simultaneously? What's the frame budget?**

Yes — radar rings, chromatic aberration, particle shimmer, heartbeat sine wave, and sonar pings all run in the same `requestAnimationFrame` loop. On the benchmark device, the combined frame time is under 4ms at 1440p, leaving plenty of headroom for the browser's own compositing. The key is that all canvas draw calls are batched in one `rAF` callback, not spread across multiple independent loops.

---

### 2.3 Telemetry Ticker and Sonar Pings

**SystemTelemetryTicker** (`ca41b76`) is a full-width LED status bar in the root layout, inspired by NASA mission control displays. It cycles through a rotating list of system status messages — build status, uptime, memory, API latency — displayed in a monospace font with a subtle scanline effect. The messages scroll horizontally using a CSS `translateX` keyframe animation. The text color reads from `--primary`.

**Sonar pings** (`33cc998`) replaced the static capability bullet indicators. Each capability listing item now has an expanding ring animation — a `border-radius: 50%` div that scales from 0 to 2 and fades out, on a staggered delay per item. The timing is offset so the rings ripple sequentially rather than all firing simultaneously, giving the impression of active system polling rather than a decoration.

**Telemetry Ticker cycling capability listings** (`18b9e6c`) then replaced the static text entirely. The capability list is now a horizontal sliding window that cycles through eight system operation strings on a 3-second interval, with a CSS `transform: translateY` transition between items. This was a late session decision — the static list felt like a CV; the ticker feels like a running process.

---

### Q&A: Telemetry and Motion Systems

**Q: Why put the telemetry ticker in the root layout and not just the homepage?**

Because it should feel like infrastructure, not decoration. If the ticker only appeared on the homepage, it would read as a hero component. In the root layout, it appears on every page — journal, labs, mission control, warborn OS. That consistency makes it feel like a real system status bar for the entire platform, not a visual flourish on one page.

**Q: Why CSS animations for the ticker instead of JavaScript-driven scrolling?**

CSS `@keyframes` for the horizontal scroll is cheaper than a JavaScript `requestAnimationFrame` loop for simple linear motion. The browser can schedule it on the compositor thread, meaning it doesn't block the main thread even during heavy JavaScript execution. For something that runs perpetually and never needs to respond to user input, CSS animation is the correct tool.

**Q: The sonar pings — do they cause layout shifts?**

No. The pings are absolutely positioned pseudo-elements (`::after`) sized with `width` and `height` as percentages of the parent. They expand using `transform: scale()` and `opacity`, both of which are composited properties — they don't trigger layout or paint, only composite. CLS score is unaffected.

**Q: Why replace the static capability list with a ticker? Doesn't that reduce readability?**

Yes, slightly. A static list is more scannable than a cycling ticker. The tradeoff is intentional: the static list communicated skills passively; the ticker communicates *activity*. A list of skills says "I know these things." A running ticker says "these things are running right now." For a site positioning itself as a live engineering platform rather than a résumé, the ticker is the right register.

**Q: What happens if JavaScript is disabled — do the tickers and animations just disappear?**

The ticker is a Next.js server component rendered to static HTML, so the text content is visible even without JavaScript. The animation (CSS keyframes) still works — CSS doesn't require JavaScript. The Canvas-based effects (radar, particles, sonar) do require JavaScript and degrade gracefully to a static portrait on `noscript`. There's no `<noscript>` fallback explicitly written yet; that's a gap.

---

### 2.4 Motion Architecture: ScrollReveal and Hover Lifts

Commit `3175353` introduced the `ScrollReveal` component. The implementation uses `IntersectionObserver` with a threshold of 0.15, meaning elements begin their reveal when 15% of them enter the viewport. Each observed element gets `opacity: 0; filter: blur(6px); transform: translateY(16px)` as its initial state, transitioning to `opacity: 1; filter: blur(0); transform: translateY(0)` on intersection.

The stagger is implemented by reading a `data-reveal-index` attribute on each child and multiplying by 80ms to set `transition-delay`. This avoids JavaScript timer management and keeps the stagger logic in CSS.

Card hover lifts add `transform: translateY(-4px)` and a box-shadow elevation increase on `:hover`. The transition duration is 200ms with `ease-out` — long enough to feel intentional, short enough to feel responsive.

---

### Q&A: Motion and Animation Architecture

**Q: Why `IntersectionObserver` instead of a scroll event listener?**

Scroll event listeners fire on every scroll event — potentially 60+ times per second. Each listener callback runs on the main thread. For element reveal animations, the only question is "has this element entered the viewport?" — a boolean question that doesn't need frame-level precision. `IntersectionObserver` answers that question efficiently, running off the main thread and only calling the callback when visibility crosses a threshold. It's the right API for reveal animations.

**Q: Why `filter: blur(6px)` as part of the reveal? Isn't blur expensive?**

`filter: blur()` triggers layer promotion and is handled by the GPU compositor, not the CPU rasterizer, for elements that are already composited. Elements with `transform` or `opacity` animations are already composited. So in practice, the blur is effectively free when combined with `transform` and `opacity` — all three are on the compositor. The visual payoff (the "de-blurring" reveal reads as the element materializing) is worth the marginal GPU cost.

**Q: The 80ms stagger — is that per-element or per-section?**

Per-element within a section. If a section has 4 cards, they reveal at 0ms, 80ms, 160ms, and 240ms. Across sections, the `IntersectionObserver` handles the sequencing naturally — the second section's elements don't start their stagger until that section enters the viewport. The result is a cascading reveal that flows with the user's scroll velocity, not on a fixed timer.

**Q: Why 200ms for hover transitions specifically?**

200ms is a well-established threshold in interaction design: fast enough to feel immediate (under 200ms is perceived as instantaneous), but long enough to be perceived as a smooth transition rather than a snap. At 100ms, hover effects look like toggles. At 300ms, they start feeling sluggish on high-density interactions (like hovering multiple cards in sequence). 200ms hits the perceptual sweet spot.

**Q: Did you consider using Framer Motion instead of building this from scratch?**

Yes. Framer Motion would have handled the stagger and reveal elegantly with `AnimatePresence` and `variants`. The reason for building from scratch: bundle size. The homepage is public-facing and SEO-critical. Adding Framer Motion (≈30KB gzipped) for animations that can be achieved with `IntersectionObserver` + CSS transitions is not a good tradeoff. The custom implementation is ≈2KB. The decision might change if we need gesture-based or spring-physics animations — at that point Framer Motion's capabilities justify the weight.

---

### 2.5 Background Depth System

Commit `2a4ecef` added the noise texture overlay, floating gradient orbs, section dividers, and volumetric depth utilities. The noise texture is a 200×200px SVG-based `filter: url(#noise)` element positioned absolutely at full viewport size with `pointer-events: none`. Floating gradient orbs are `position: fixed` divs with radial gradients and a slow drift animation (40s cycle) — they contribute to perceived depth without competing with content.

Section dividers (`f3aa78b`) are `linear-gradient` backgrounds on `<hr>`-equivalent elements, fading from the section background color to transparent. This is a simple trick but eliminates the harsh visual edges between section backgrounds.

---

### Q&A: Background and Depth Systems

**Q: Why SVG noise instead of a PNG noise texture?**

A PNG noise texture at sufficient resolution (512×512) is around 80–200KB depending on compression. An SVG `feTurbulence` filter generates noise procedurally in the browser at zero network cost. The SVG version also scales perfectly — the noise tiles at viewport resolution rather than at a fixed texture size. The only downside is slightly higher GPU cost on initial paint, but for a static overlay this is negligible.

**Q: The gradient orbs are `position: fixed` — doesn't that cause issues with scroll performance?**

Fixed-position elements with large background gradients used to trigger repaint on every scroll frame in older browser rendering models. Modern browsers (Chrome 90+, Safari 15+) handle fixed-position elements more efficiently by promoting them to their own compositor layer. The slow drift animation (40s, very low velocity) is handled entirely by the GPU. In practice, no scroll jank is observable. The risk was real on older hardware; we accepted it.

**Q: Why 40 seconds for the orb drift cycle?**

Slow enough that users won't consciously notice the orbs moving. The goal is for them to contribute to "this page feels alive" without being distracting. At 20 seconds, they're perceptibly drifting. At 60 seconds, there's no point. 40 seconds is the threshold where peripheral vision registers motion but directed attention doesn't.

---

### 2.6 Project Card Terminal Simulations

Commit `33ceec6` replaced the static CPU icons on project cards with three alternating terminal animation styles:

1. **Line-by-line log stream**: Characters appear one at a time in a monospace terminal, simulating a running process.
2. **LED progress bar**: A horizontal bar fills from 0 to 100% with a color transition, loops with a reset delay.
3. **Blinking cursor loop**: A prompt character blinks in a terminal-like cadence with a rotating set of simulated commands.

Each card is assigned one of the three styles based on its index mod 3. This ensures visual variety without requiring per-card configuration.

---

### Q&A: Project Card Simulations

**Q: Why three different simulation styles instead of just one consistent animation?**

Visual monotony. If all six project cards run the same terminal animation, after the first card the viewer has seen the pattern. Their eyes skip the subsequent cards. Three styles mean the eye is engaged by novelty at cards 1, 2, and 3, and then recognizes the pattern repeating at 4, 5, 6 — which is itself interesting. The variety also communicates that these are *different* projects, not copies of each other.

**Q: Are these animations accessible — do they respect `prefers-reduced-motion`?**

Not currently — that's a gap. The animations should pause or switch to static states when `prefers-reduced-motion: reduce` is set. The `@media (prefers-reduced-motion: reduce)` query needs to be added to the CSS governing these animations. It's a known issue.

**Q: The LED progress bar "fills from 0 to 100% with a color transition" — what's the color transition?**

It starts at the `--primary` color at 0% width and shifts toward a lighter, more saturated variant at 100%. The transition is a `background: linear-gradient` that changes with width using a CSS animation on `width` and `filter: hue-rotate()`. Combined with the fill animation, the bar reads like a loading operation completing — which is exactly the impression intended.

**Q: Why use `mod 3` to assign animation styles? What if there are fewer than 3 cards or more than 9?**

`index % 3` works for any number of cards. With 1 card, all three styles exist but only the first is used. With 10 cards, the sequence repeats 3 times with a remainder of 1. Both are fine. The edge case would be 3 cards — you get exactly one of each style, perfect variety. The system scales without configuration.

---

### 2.7 Floating Island Navbar

Commit `5ec9c81` finalized the floating island navbar. The nav is `position: fixed`, centered horizontally, with a `backdrop-filter: blur(12px)` frosted glass background. The hover color on nav links is bound to `var(--primary)` — meaning it automatically picks up the photo-synced color from the hero. When the portrait color changes (if a different portrait is loaded), the entire navbar hover state updates without touching navbar code.

---

### Q&A: Navbar Architecture

**Q: Why a "floating island" nav over a traditional full-width sticky header?**

A full-width sticky header anchors the page to a rigid top boundary. The floating island nav — a pill-shaped, centered, translucent element — lets the page content breathe underneath it. Visually, it communicates "this is a creative platform" rather than "this is a corporate dashboard." It also uses less vertical space, which matters on the smaller viewports where the hero content is already competing for attention.

**Q: `backdrop-filter: blur(12px)` — what's the browser support situation?**

`backdrop-filter` is supported in all modern browsers (Chrome 76+, Safari 9+, Firefox 103+). The only meaningful holdout was Firefox, which gated it behind a flag until 2022. In 2026, support is effectively universal for the audience this site targets. The fallback (for browsers that don't support it) is a semi-opaque solid background — `background: rgba(10, 10, 20, 0.85)`. The visual degrades gracefully.

**Q: Does the navbar color change when the hero portrait changes without a page reload?**

Yes, because the hover color is `var(--primary)` which is a CSS custom property on the document root. When the color extractor updates `--primary`, every element that references it updates immediately — including the navbar hover state — in the same paint cycle. There's no JavaScript in the navbar that needs to know about portrait changes. The CSS cascade handles it.

---

## 3. Infrastructure and Deployment

This is where the day got expensive.

The deployment target is a standard split: Next.js frontend on Vercel at `buildwithpnj.in`, FastAPI backend on Render at `dashboard-nb61.onrender.com`, database on Supabase PostgreSQL accessed through PgBouncer on port 6543.

The goal was simple: on Render startup, run Alembic migrations to ensure schema is current, then seed the database with a default admin user (`prakashjhadps@gmail.com`) if one doesn't exist. This is table-stakes deployment automation — nothing exotic.

What followed was seven failed deployments over approximately two and a half hours.

### Failure 1 — URL Scheme Mismatch

Render injects `DATABASE_URL` as a plain `postgresql://` connection string. SQLAlchemy's async engine requires `postgresql+asyncpg://`. First fix: a parser in `config.py` that rewrites the scheme on load.

```python
# config.py (after fix)
@property
def database_url(self) -> str:
    url = os.environ.get("DATABASE_URL", "")
    url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url
```

Deployed. Failed. Next layer.

### Failure 2 — Password Special Character

The database password is `dobbie@KAP1`. The `@` character in a URL signals the start of the host segment. Python's `urllib.parse.urlparse` treats everything after the last `@` as the host, splitting the password mid-string. The connection string was being parsed as a malformed URL, giving SQLAlchemy a garbled hostname.

Fix: URL-encode the password using `urllib.parse.quote(password, safe='')`. This requires parsing the URL into components, encoding just the password field, and reassembling. Added in `da78343`.

Deployed. Failed on a different error. Progress.

### Failure 3 — DATABASE_URL= Literal Prefix

Render's environment variable injection, when copied from their dashboard, sometimes includes the variable name as a prefix in the value. The actual string stored in the environment was `DATABASE_URL=postgresql://...` — with the key name literally prepended to the value. The parser was receiving `DATABASE_URL=` as part of the URL and passing it to `urlparse`, which produced garbage.

Fix: strip the prefix before parsing.

```python
url = url.removeprefix("DATABASE_URL=")
```

Commit `f5ce6a6`. Deployed. Failed.

### Failure 4 — PgBouncer Statement Cache

Supabase's PgBouncer in transaction pooling mode does not support named prepared statements. SQLAlchemy and asyncpg both cache prepared statements by default. The error:

```
asyncpg.exceptions.FeatureNotSupportedError:
prepared statement "..." already exists
```

This is a well-documented PgBouncer gotcha. Fix: disable statement cache.

```python
# In engine creation:
connect_args={"statement_cache_size": 0}

# In alembic/env.py create_engine call:
connect_args={"statement_cache_size": 0}
```

Commit `562c032`. Deployed. Failed.

### Failure 5 — ConfigParser % Escaping

Alembic reads `alembic.ini` using Python's `configparser`. ConfigParser treats `%` as the start of an interpolation sequence — `%(varname)s` style. The database URL contained `%40` (URL-encoded `@`). ConfigParser tried to interpolate `%40` as a variable reference, failed, and threw:

```
configparser.InterpolationSyntaxError:
'%' must be followed by '%' or '(', found: '%40'
```

Fix: escape every `%` in the URL string to `%%` before writing it into the Alembic config object.

```python
# alembic/env.py
config.set_main_option(
    "sqlalchemy.url",
    database_url.replace("%", "%%")
)
```

Commit `21a52f5`. Deployed. Got further than before. Login returned 500.

### Failure 6 and 7 — The Actual Root Cause

At this point the migrations were running. The seed code was executing. But login was still returning 500. The error in Render logs:

```
RuntimeError: Event loop is closed
```

On every single request to any database-touching endpoint.

---

### Q&A: Deployment and Infrastructure Debugging

**Q: Why does Render inject `DATABASE_URL` with `postgresql://` instead of `postgresql+asyncpg://`?**

Because Render is database-driver agnostic. The `postgresql://` scheme is the IANA-registered standard URI scheme for PostgreSQL — it's what `psycopg2`, Go's `pgx`, Ruby's `pg` gem, and every other PostgreSQL driver expects. The `+asyncpg` driver suffix is a SQLAlchemy-specific convention, not a standard. Render doesn't know you're using SQLAlchemy async — it just provides a valid PostgreSQL connection string. The translation responsibility is yours.

**Q: Why doesn't SQLAlchemy just accept `postgresql://` and figure out the driver automatically?**

SQLAlchemy's URL scheme determines which database dialect and driver class to load. `postgresql://` maps to the synchronous `psycopg2` driver. `postgresql+asyncpg://` maps to the async `asyncpg` driver. These are fundamentally different code paths in SQLAlchemy's internals — different connection pool implementations, different cursor classes, different transaction managers. The `+asyncpg` suffix isn't cosmetic; it's a routing decision.

**Q: How did the `DATABASE_URL=` prefix get into the environment variable value?**

When you copy a connection string from Render's dashboard, the display format is `DATABASE_URL=postgresql://...` — with the variable name shown for context. If you copy that entire line (including the key) and paste it into the "value" field of the environment variable form, you get the key name embedded in the value. It's a UI affordance that creates a subtle footgun. The fix at the config layer (stripping the prefix) is the right defense-in-depth approach.

**Q: PgBouncer and prepared statements — why does transaction pooling break them?**

In session pooling mode, a client holds the same backend connection for the duration of their session. Prepared statements work fine because they're scoped to a connection, and the client always talks to the same connection. In transaction pooling mode, a client gets a backend connection for the duration of a single transaction, then releases it. The next transaction may go to a different backend connection. If that connection doesn't have the prepared statement cached, it throws an error. Since asyncpg caches prepared statements by default, every second transaction on a new backend connection fails. Setting `statement_cache_size: 0` disables the cache and forces asyncpg to re-prepare each query, which is slightly slower but correct.

**Q: Is the performance cost of disabling the statement cache significant?**

For an application with a small number of distinct queries (CRUD operations on a few tables), the cost is negligible — a few microseconds per query for the extra round-trip to prepare. For analytical workloads with hundreds of distinct complex queries, it could add up. For this application (authentication, finance records, notes, books — relatively simple CRUD), the impact is unmeasurable in practice.

**Q: Why does configparser interpret `%40` as an interpolation sequence?**

Python's `configparser` uses `%(key)s` syntax for variable interpolation in config files. It reserves `%` as an escape character. When it encounters `%40`, it tries to parse `40` as a variable name, fails, and raises `InterpolationSyntaxError`. The double-`%` escape (`%%`) is how configparser represents a literal `%` in a config value. This is a 20-year-old Python quirk that catches people regularly. The correct fix is to always escape `%` when writing URLs into alembic.ini programmatically.

**Q: After five deployments, did you have local reproduction of the issues?**

No — and that's the core lesson. Render's environment (Python 3.14, specific SSL library versions, PgBouncer in transaction mode) differed from the local environment in ways that made several bugs invisible locally. With local Postgres, there's no PgBouncer, no statement cache issue. With a password without special characters, there's no URL encoding issue. A proper staging environment that mirrors production exactly — including PgBouncer — would have caught all five pre-asyncio failures in a single local session.

**Q: Seven failed deployments — roughly how much wall-clock time was spent waiting for Render builds?**

Each Render build takes 3–5 minutes: clone the repo, create a virtual environment, install all dependencies (including numpy, asyncpg, alembic, SQLAlchemy, cryptography — not trivial), run the startup command. Seven deployments × ≈4 minutes each = approximately 28 minutes of pure waiting. Add in the time to read logs, form a hypothesis, write the fix, and commit, and the total calendar time was closer to 2.5 hours for what was ultimately five distinct bugs plus one architecture issue.

---

## 4. The Root Cause: asyncio Event Loop Architecture

Python's `asyncio.run()` is a high-level convenience function. It does three things: creates a new event loop, runs the given coroutine until completion, and then calls `loop.close()` before returning. That `loop.close()` is the problem.

The FastAPI application runs on uvicorn, which uses a single event loop for the entire process lifetime. That event loop is Python's default event loop — `asyncio.get_event_loop()`. When the startup lifespan hook fires, it needs to run the async seed function. The seed function was wrapped in `asyncio.run()` and called inside a background thread to avoid blocking the startup hook itself.

Here is what actually happened at runtime:

1. uvicorn creates the default event loop and starts running FastAPI on it.
2. FastAPI's lifespan `startup` fires.
3. Startup spawns a thread via `threading.Thread`.
4. Inside that thread, `asyncio.run(seed())` is called.
5. `asyncio.run()` creates a **new** event loop for the coroutine, runs `seed()`, then calls `loop.close()` when done.
6. The closed loop becomes the default event loop for the process (in CPython's thread model, the default loop is process-scoped, not thread-scoped).
7. uvicorn's server is still running on the original loop object — but `asyncio.get_event_loop()` in subsequent request handlers now returns the closed loop.
8. Every `await db.execute(...)` call throws `RuntimeError: Event loop is closed`.

The fix was to remove asyncio entirely from the seed path. The seed function was rewritten to use a synchronous SQLAlchemy engine with `psycopg2` (not asyncpg), called directly — no threads, no `asyncio.run()`, no coroutines.

```python
# seed.py (after fix)
def seed_sync():
    sync_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
    engine = create_engine(sync_url, echo=False)
    with sessionmaker(bind=engine)() as session:
        try:
            _seed_users(session)
            session.commit()
        except Exception:
            session.rollback()
            raise
    engine.dispose()
```

This runs synchronously inside the startup thread. It has zero interaction with the asyncio event loop. It uses `psycopg2` directly through SQLAlchemy's sync dialect. It does not close anything that uvicorn owns.

Commit `c2ab969` deployed at 21:26 IST.

Login test: `POST /auth/login` with the seeded credentials.

```
HTTP 200 OK
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

Done.

---

### Q&A: asyncio Architecture Deep Dive

**Q: What exactly does `asyncio.run()` do internally that breaks the event loop?**

`asyncio.run()` is approximately equivalent to:
```python
def run(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)      # ← sets the DEFAULT loop
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
        asyncio.set_event_loop(None)  # ← clears the default loop
```
The key line is `asyncio.set_event_loop(loop)` followed by `asyncio.set_event_loop(None)` in the `finally` block. After `asyncio.run()` returns, the "current event loop" is `None`. But uvicorn's loop — which was set as the default when the process started — is still running. The problem is that SQLAlchemy's asyncpg driver calls `asyncio.get_event_loop()` internally. After our `asyncio.run()` call, that returns `None` (or in some Python versions, returns the now-closed loop). Either way, the next `await` on a database connection fails.

**Q: Why does the default event loop get corrupted if `asyncio.run()` is called from a thread? Isn't each thread supposed to have its own event loop?**

This is the subtle part. Python threads do not automatically have their own event loops. `asyncio.get_event_loop()` returns the *running* loop if one is running in the current thread, and falls back to the *default* loop for the process if no loop is running in the current thread. In Python 3.10+, calling `asyncio.get_event_loop()` from a thread with no running loop emits a deprecation warning. In earlier versions, it quietly returned the process default. Either way, when `asyncio.run()` closes the loop it created and sets the default to `None`, subsequent `asyncio.get_event_loop()` calls from *any thread* — including the main thread where uvicorn is running its loop — may return `None` or the closed loop.

**Q: Could we have used `asyncio.new_event_loop()` in the thread instead of `asyncio.run()`?**

We tried this: create a new event loop explicitly, run the coroutine with `loop.run_until_complete(seed())`, and close only that loop. The problem was that SQLAlchemy's `AsyncSession` and the asyncpg connection pool are bound to the event loop they were created on (the uvicorn main loop). When you run `seed()` in a thread-local loop, the session's internal state — connection references, pending callbacks — is tied to the original loop. The thread-local loop and the uvicorn loop are different objects, and asyncpg's transport layer detects this mismatch and fails. The only clean solution is to not use async at all in the seed path.

**Q: Couldn't we have just scheduled the seed coroutine on uvicorn's existing event loop using `asyncio.run_coroutine_threadsafe()`?**

Yes — `asyncio.run_coroutine_threadsafe(seed_data(), uvicorn_loop)` would have worked correctly. It schedules the coroutine on the running loop from a non-async context and returns a `concurrent.futures.Future` you can `.result()` on from the thread. We didn't try this approach because it requires a reference to uvicorn's loop object, which isn't directly exposed through the FastAPI API. You can get it with `asyncio.get_event_loop()` *before* the thread starts (from inside the `async def lifespan` function), but it felt fragile. The synchronous psycopg2 approach is cleaner: it makes the dependency explicit (sync seed uses sync driver, async API uses async driver) and eliminates the shared-state problem entirely.

**Q: Is the synchronous seed meaningfully slower than the async version would have been?**

No, for this workload. The seed function runs once at startup. It inserts 2 users, 14 categories, 8 accounts, 10 transactions, and 6 books — roughly 40 SQL statements. With psycopg2 over a 10ms-latency Supabase connection, that's 400ms at worst. The async version would have been equally fast in wall-clock terms (async doesn't make individual queries faster, it allows *concurrent* queries to not block each other). For a linear seed sequence with no concurrency, sync and async are equivalent in throughput.

**Q: What would a fully correct async startup initialization look like?**

If we wanted to keep async throughout, the correct pattern is:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run sync Alembic in thread pool (Alembic is sync-only)
    await asyncio.get_event_loop().run_in_executor(None, run_alembic_migrations)
    
    # Run async seed DIRECTLY in the lifespan coroutine (same event loop)
    await seed_data_async()
    
    yield
```

The seed runs in the same event loop as the rest of the application — no threads, no cross-loop calls. The Alembic migration (which must be sync because Alembic doesn't support asyncio) goes into a thread pool via `run_in_executor`. This is the architecturally correct version. We went with the synchronous-everything approach instead because it's simpler, it's correct, and startup initialization doesn't benefit from async concurrency anyway.

**Q: Could this bug have been caught by a test?**

Yes, easily. A `pytest-asyncio` integration test that starts the FastAPI app via `AsyncClient`, waits for startup, and immediately issues a login request would have caught `RuntimeError: Event loop is closed` in the first test run. The absence of startup integration tests is what allowed this to reach production. The test infrastructure is now a priority.

**Q: How do you prevent this class of bug from happening again?**

Three layers:
1. **Rule**: never call `asyncio.run()` inside a thread that exists within a running event loop's lifecycle.
2. **Architecture**: use synchronous libraries for synchronous operations (seeds, migrations) and async libraries for request-handling operations. Don't mix.
3. **Tests**: add a startup integration test that verifies the server accepts requests after the lifespan hook completes. This catches event loop corruption immediately.

---

## 5. Key Metrics

| Metric | Value |
|--------|-------|
| Total commits | 33 |
| Files changed | 41 |
| Insertions | 2,503 |
| Deletions | 855 |
| Render deployments | 7 |
| Hours on backend debugging | ~2.5 |
| Hours on frontend | ~5.5 |
| Time of first commit | 15:25 IST |
| Time of final fix | 21:26 IST |
| Login status after fix | HTTP 200 + JWT |
| Canvas sample resolution | 120×120px |
| Canvas color saturation threshold | Saturation > 48 |
| Canvas hue bucket width | 10 degrees |
| ScrollReveal threshold | 15% viewport entry |
| ScrollReveal stagger interval | 80ms per index |
| Reveal animation duration | 500ms |
| Particle count in shimmer layer | 120 |
| Heartbeat interval | 2.8 seconds |
| Sonar ping interval | 3s |
| Telemetry ticker items | 8 items |
| Telemetry ticker rotation | 3s per item |
| Terminal simulation styles | 3 (stream, LED bar, cursor) |
| Orb drift cycle | 40 seconds |
| Navbar blur radius | 12px |
| Card hover lift | 4px translateY |
| Card hover transition | 200ms ease-out |

---

## 6. Lessons Learned

**On asyncio:**
`asyncio.run()` is designed for scripts, not for use inside long-running server processes. The documentation says this clearly; we ignored it. In a server context, if you need to run an async function from a non-async context, use `asyncio.get_event_loop().run_coroutine_threadsafe()` from a thread, or restructure so you're not calling async code from a thread at all. The cleanest solution in our case was eliminating asyncio from the seed path entirely — synchronous operations for a one-time startup seed are not a performance problem.

**On URL parsing with special characters:**
Database passwords containing `@`, `%`, `#`, or `/` will break any naive URL string replacement. The correct approach is to always parse the URL into components (`urllib.parse.urlsplit`), encode the username and password fields independently with `urllib.parse.quote(safe='')`, and reconstruct using `urllib.parse.urlunsplit`. Do this once, at the config layer, and never string-replace a URL again.

**On incremental deployment debugging:**
Seven deployments is too many. Each one took 3–5 minutes to build and start on Render, meaning roughly 28 minutes of wall-clock time was spent waiting for feedback. A local Docker replica of the Render environment — including PgBouncer — would have compressed this to minutes. That setup is now on the backlog.

**On Canvas color systems:**
The pixel extraction approach works well for portraits with distinct chromatic character — a subject with warm skin tones, colored clothing, or a colorful background will produce a usable dominant hue. For grayscale or near-monochrome portraits, the saturation filter (`s > 48`) will reject most pixels and the system will fall back to a hardcoded default. That fallback currently exists but isn't elegant. A future improvement is a tiered saturation strategy: try `s > 48`, fall back to `s > 30`, fall back to `s > 15`, finally fall back to default.

**On scope management:**
The frontend work expanded significantly beyond the initial plan. The color system is genuinely good and worth the time spent, but eight hours of frontend commits delayed the backend work that was actually blocking deployment. In hindsight: fix the deployment blocker first, then iterate on the design system. The hero works locally even without the API.

**On exception visibility:**
The global exception handler that revealed `{"detail": "Event loop is closed"}` was added midway through debugging. It should have been there from the start. FastAPI's default 500 response returns `"Internal Server Error"` as a plain string — zero debugging information. A production-grade global handler that logs the full traceback and returns the exception message in the response body saves hours. Add it first, before you need it.

---

## 7. Open Questions for Next Session

- **Can the color store be replaced with a Zustand slice without breaking the Canvas 2D draw calls?** The singleton pattern works but it's unidiomatic in a React codebase. The challenge is that Canvas animation loops need synchronous, zero-overhead color reads on every frame — a React state update cycle is too slow.

- **Should the telemetry ticker messages be fetched from the API?** Currently they're hardcoded strings. Fetching real uptime, build status, and API latency from a `/api/health` endpoint would make the ticker genuinely live. The complexity cost is: API call on every page load, potential for the ticker to show stale data if the API is down.

- **Is there a WCAG contrast risk in the canvas color system?** If the dominant portrait color is very light (high saturation, high lightness), it may not contrast enough against the light-mode background. This needs a proper contrast audit.

- **What does the hero look like with no JavaScript?** The Canvas layers, sonar pings, and telemetry ticker all require JavaScript. A `<noscript>` fallback showing a static portrait with a fixed accent color needs to be written.

- **Integration tests for the FastAPI startup lifespan hook** — specifically a test that starts the server, completes startup, and immediately POSTs to `/api/auth/login`. This would have caught the asyncio bug in development.

- **Docker-based local staging environment** — a `docker-compose` configuration that runs FastAPI, Postgres with PgBouncer in front of it, and Next.js in production mode, mirroring the Render/Vercel architecture. Every production bug we hit today would have been reproducible locally.

- **`prefers-reduced-motion` support** — the Canvas animations, sonar pings, telemetry ticker, and terminal simulations all need to respect this media query. Currently none of them do.

---

*Next session: Zustand color store refactor, integration test for the startup hook, prefers-reduced-motion pass across all animations, and WCAG contrast audit on the dynamic color system.*

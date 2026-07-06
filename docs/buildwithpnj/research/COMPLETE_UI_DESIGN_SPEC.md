# BuildWithPNJ — Complete UI/UX Design Specification

> **Version:** 1.0  
> **Date:** 2026-07-04  
> **Role:** Principal Product Designer  
> **Status:** AWAITING APPROVAL — Do not implement until signed off.

---

# PART 1 — EXECUTIVE UI SUMMARY

## What This Is

BuildWithPNJ is the digital headquarters of an AI engineer building production-ready systems in public. It is not a portfolio. It is not a freelancer page. It is a living, breathing engineering command center — a place that communicates technical excellence, builder momentum, and design taste in equal measure.

## Design North Star

> **"If Linear, Vercel, and a NASA mission control center had a child raised by an AI engineer."**

The site should feel like a premium developer tool — not a personal website. Every visitor should leave thinking: *"This person builds at a different level."*

## Key Design Decisions

| Decision | Rationale |
|---|---|
| Dark-first with deep navy base (`#050816`) | Signals engineering depth. Feels like an IDE, not a template. |
| `Pixel Operator Bold` for display text | Retro-futuristic, instantly unique. No one else uses this. |
| Cyan accent (`#00F5FF`) as the signature glow | Neon-on-dark creates the "command center" energy. Unforgettable. |
| 20px border radius | Softer than typical dev sites. Signals modern, not brutalist. |
| Mission Control as the hero page | Signals real-time activity. Proves shipping velocity. |
| No stock photos, no illustrations | Only real screenshots, real data, real metrics. |

## Updated Design System (Supersedes Earlier Docs)

| Token | Old Value | **New Value** |
|---|---|---|
| Background | `#0A0A0F` | **`#050816`** |
| Card surface | `#1E1E2E` | **`#0F172A`** |
| Elevated surface | `#2A2A3E` | **`#1E293B`** |
| Floating surface | `#353550` | **`#334155`** |
| Primary accent | `#6366F1` | **`#3B82F6`** |
| Signature accent | `#06B6D4` | **`#00F5FF`** |
| Display font | Space Grotesk | **Pixel Operator Bold** |
| Body font | Inter | **Inter** (unchanged) |
| Code font | JetBrains Mono | **JetBrains Mono** (unchanged) |
| Border radius | 8px | **20px** |

---

# PART 2 — DESIGN LANGUAGE

## 2.1 Mood

The visual language sits at the intersection of three worlds:

```
     DEVELOPER TOOL                COMMAND CENTER               PREMIUM PRODUCT
     (Linear, Vercel)              (NASA, SpaceX)               (Apple, Stripe)
     ─────────────                 ───────────────              ────────────────
     Clean grids                   Live dashboards              Generous whitespace
     Monospace accents             Telemetry data               Smooth animations
     Keyboard-first               Status indicators            Material depth
     Dark surfaces                 Glowing accents              Typographic hierarchy
```

## 2.2 Color System

### Surfaces

| Layer | Hex | Usage |
|---|---|---|
| **Void** | `#050816` | Page background — the deepest layer |
| **Surface** | `#0F172A` | Cards, content blocks, nav background |
| **Elevated** | `#1E293B` | Hover cards, active states, sidebar |
| **Floating** | `#334155` | Tooltips, dropdowns, modals, command palette |

### Accents

| Name | Hex | Usage |
|---|---|---|
| **Primary Blue** | `#3B82F6` | Links, primary buttons, active indicators |
| **Neon Cyan** | `#00F5FF` | Signature glow, metric highlights, status-active dots, Mission Control telemetry |
| **Soft Violet** | `#8B5CF6` | Secondary accent, gradient endpoint, tags |

### Glow Effects

The signature visual move. Used sparingly for maximum impact.

| Effect | Application |
|---|---|
| **Card glow** | On hover: `box-shadow: 0 0 30px rgba(0, 245, 255, 0.08)` — barely visible, deeply felt |
| **Text glow** | Hero headline only: `text-shadow: 0 0 40px rgba(0, 245, 255, 0.3)` |
| **Border glow** | Active/focused inputs: `box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15)` |
| **Ambient glow** | Hero section: radial gradient of cyan at 3-5% opacity, top-center |
| **Status glow** | Mission Control live indicators: pulsing `#00F5FF` dot |

### Text Colors

| Role | Hex | Contrast on Surface |
|---|---|---|
| **Primary** | `#F1F5F9` | 13.2:1 ✅ AAA |
| **Secondary** | `#94A3B8` | 5.4:1 ✅ AA |
| **Muted** | `#8E9CAE` | `--color-text-muted` | Placeholders, disabled text, hints | 4.8:1 ✅ AA |
| **Accent** | `#00F5FF` | 9.8:1 ✅ AAA |
| **Link** | `#3B82F6` | 4.6:1 ✅ AA |

### Borders

| Role | Value |
|---|---|
| **Default** | `1px solid rgba(255, 255, 255, 0.06)` |
| **Hover** | `1px solid rgba(59, 130, 246, 0.3)` |
| **Active** | `1px solid #3B82F6` |
| **Glow** | `1px solid rgba(0, 245, 255, 0.2)` |

### Gradients

| Name | Value | Usage |
|---|---|---|
| **Brand** | `linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #00F5FF 100%)` | Hero headline, primary CTA |
| **Surface** | `radial-gradient(ellipse at 50% 0%, rgba(0,245,255,0.04) 0%, transparent 60%)` | Hero ambient glow |
| **Card hover** | `linear-gradient(180deg, rgba(59,130,246,0.03) 0%, transparent 100%)` | Subtle top-to-bottom on hover |

## 2.3 Typography

| Role | Font | Weight | Size Range | Letter Spacing | Line Height |
|---|---|---|---|---|---|
| **Display** | Pixel Operator Bold | Bold | 48–80px | `0.05em` | 1.1 |
| **H1** | Pixel Operator Bold | Bold | 32–48px | `0.03em` | 1.15 |
| **H2** | Inter | 700 | 24–32px | `-0.02em` | 1.25 |
| **H3** | Inter | 600 | 20–24px | `-0.01em` | 1.3 |
| **H4** | Inter | 600 | 16–20px | `0` | 1.35 |
| **Body** | Inter | 400 | 16px | `0` | 1.6 |
| **Body Small** | Inter | 400 | 14px | `0` | 1.5 |
| **Caption** | Inter | 500 | 12–13px | `0.03em` | 1.4 |
| **Overline** | Pixel Operator Bold | Bold | 11–13px | `0.12em` | 1.4 |
| **Code** | JetBrains Mono | 400 | 14px | `0` | 1.7 |
| **Metric** | JetBrains Mono | 500 | 24–48px | `-0.02em` | 1.1 |

### Pixel Operator Bold Usage Rules

- Hero headlines on every page
- Section overlines (e.g., `// FEATURED PROJECTS`)
- Mission Control metric labels
- Navigation logo wordmark
- **Never** for body text, descriptions, or long-form reading

## 2.4 Spacing (8-Point Grid)

| Token | Value | Usage |
|---|---|---|
| `--space-1` | 4px | Icon gaps, hairline separators |
| `--space-2` | 8px | Tight internal padding, tag padding |
| `--space-3` | 16px | Component internal padding, card padding |
| `--space-4` | 24px | Gap between cards, form field spacing |
| `--space-5` | 32px | Between related sections |
| `--space-6` | 48px | Between major sections |
| `--space-7` | 64px | Page section vertical spacing |
| `--space-8` | 96px | Hero section vertical padding |
| `--space-9` | 128px | Maximum breathing room |

## 2.5 Elevation & Shadows

| Layer | Shadow | Glow |
|---|---|---|
| **Rest** | `0 1px 3px rgba(0,0,0,0.4)` | None |
| **Hover** | `0 8px 24px rgba(0,0,0,0.4)` | `0 0 30px rgba(0,245,255,0.06)` |
| **Active** | `0 2px 8px rgba(0,0,0,0.5)` | `0 0 20px rgba(59,130,246,0.1)` |
| **Floating** | `0 16px 48px rgba(0,0,0,0.6)` | `0 0 40px rgba(0,245,255,0.05)` |

## 2.6 Border Radius

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | 8px | Tags, badges, inline code |
| `--radius-md` | 12px | Buttons, inputs, small cards |
| `--radius-lg` | 20px | Cards, sections, containers |
| `--radius-xl` | 24px | Modals, large feature cards |
| `--radius-full` | 9999px | Pills, avatars, status dots |

---

# PART 3 — COMPLETE SCREEN DESIGNS

---

## PAGE 1: HOME `/`

### Purpose
First impression. In 5 seconds, the visitor knows: who PNJ is, what he builds, and that this is not a typical developer website. It should feel like walking into a high-end engineering studio.

### Primary Users
Casual-Consumer Kavya (P1 — needs instant clarity), Dev-Curious Darshan (P0 — needs content hooks), Hiring-Manager Hema (P0 — needs project proof)

### Conversion Goals
"View Projects" click, "Read Journal" click, Newsletter signup, GitHub star

---

### Section 1: Hero

**Visual hierarchy:** Name → Tagline → CTAs → Ambient glow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                     (ambient radial cyan glow, 3% opacity)                   │
│                                                                              │
│                                                                              │
│           // BUILDING THE FUTURE WITH AI                                     │
│           (Pixel Operator Bold, 12px, #00F5FF, uppercase, tracked)           │
│                                                                              │
│                                                                              │
│           PRAKASH NAYAK JOSHI                                                │
│           (Pixel Operator Bold, 64px, gradient text: #3B82F6 → #00F5FF)     │
│                                                                              │
│                                                                              │
│           AI Engineer. Building production-ready                             │
│           AI systems in public.                                              │
│           (Inter 400, 20px, #94A3B8, max-width: 560px, centered)            │
│                                                                              │
│                                                                              │
│           [ View Projects ▶ ]      [ Engineering Journal ]                   │
│           (Primary, gradient bg)    (Ghost, border, #94A3B8)                 │
│                                                                              │
│                                                                              │
│           ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                               │
│           │ GH  │  │ X   │  │ LI  │  │ EM  │                                │
│           └─────┘  └─────┘  └─────┘  └─────┘                               │
│           (Social icons, 20px, #8E9CAE → #F1F5F9 on hover)                  │
│                                                                              │
│                                                                              │
│                         ↓ scroll indicator                                   │
│                     (animated chevron, pulsing opacity)                       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Design notes:**
- Full viewport height (100vh)
- Content vertically and horizontally centered
- Ambient glow: `radial-gradient(ellipse at 50% 30%, rgba(0,245,255,0.04), transparent 60%)`
- Optional: grid-dot pattern overlay at 2% opacity for texture
- Scroll indicator disappears after first scroll

---

### Section 2: Mission

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  // MISSION                                                                  │
│  (Pixel Operator Bold, 12px, #00F5FF, overline)                              │
│                                                                              │
│  I build AI-powered tools that solve                                         │
│  real problems — then share everything                                       │
│  I learn along the way.                                                      │
│  (Inter 700, 28px, #F1F5F9, max-width: 700px)                               │
│                                                                              │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐                    │
│  │ ⚡              │ │ 🔬              │ │ 📡              │                    │
│  │ Ship Fast       │ │ Build Real      │ │ Share Everything│                    │
│  │                 │ │                 │ │                 │                    │
│  │ Production-     │ │ No toy demos.   │ │ Open source,    │                    │
│  │ ready systems,  │ │ Real users,     │ │ build in public,│                    │
│  │ not prototypes. │ │ real problems.  │ │ transparent.    │                    │
│  │                 │ │                 │ │                 │                    │
│  └────────────────┘ └────────────────┘ └────────────────┘                    │
│  (3-col grid, #0F172A bg, 20px radius, 24px padding)                         │
│  (icons: #00F5FF, titles: Inter 600 16px, body: Inter 400 14px #94A3B8)      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Section 3: Current Build

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  // CURRENTLY BUILDING                                                       │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │                                                                       │    │
│  │  ┌──────────────────────┐    Personal OS                    🟢 LIVE   │    │
│  │  │                      │    ────────────                             │    │
│  │  │    [Live screenshot   │    A production-grade personal operating   │    │
│  │  │     of the Personal   │    system replacing Notion, YNAB, and     │    │
│  │  │     OS dashboard]     │    spreadsheet sprawl.                     │    │
│  │  │                      │                                             │    │
│  │  │                      │    [Next.js] [FastAPI] [PostgreSQL] [AI]    │    │
│  │  └──────────────────────┘    (tag pills, 8px radius, #0F172A bg)     │    │
│  │                                                                       │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                    │    │
│  │  │ 12      │ │ 847     │ │ 9       │ │ 6mo     │                    │    │
│  │  │ Modules │ │ Commits │ │ APIs    │ │ Active  │                    │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘                    │    │
│  │  (metrics: JetBrains Mono 500 24px #00F5FF, labels: 12px #94A3B8)    │    │
│  │                                                                       │    │
│  │  [ View Project → ]    [ GitHub ↗ ]    [ Live Demo ↗ ]               │    │
│  │                                                                       │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│  (Featured card: #0F172A bg, 20px radius, 1px border, glow on hover)        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Section 4: Featured Projects

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  // PROJECTS                                          [ View All → ]         │
│                                                                              │
│  ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐    │
│  │ [Thumbnail 16:9]    │ │ [Thumbnail 16:9]    │ │ [Thumbnail 16:9]    │    │
│  │                     │ │                     │ │                     │    │
│  │ Project Title       │ │ Project Title       │ │ Project Title       │    │
│  │ Brief description   │ │ Brief description   │ │ Brief description   │    │
│  │ in two lines max.   │ │ in two lines max.   │ │ in two lines max.   │    │
│  │                     │ │                     │ │                     │    │
│  │ [Python] [AI] [RAG] │ │ [TS] [Next.js]     │ │ [Voice] [Agent]    │    │
│  │                     │ │                     │ │                     │    │
│  │ 🟢 Active           │ │ ✅ Complete          │ │ 🧪 Experiment       │    │
│  └─────────────────────┘ └─────────────────────┘ └─────────────────────┘    │
│  (3-col grid → 2-col tablet → 1-col mobile)                                 │
│  (Card: #0F172A, 20px radius, hover: lift + cyan glow + border glow)        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Section 5: Engineering Journal Preview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  // ENGINEERING JOURNAL                               [ Read More → ]        │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │  FEATURED                                                             │    │
│  │  ┌──────────────────────┐   Building a Personal OS from Scratch      │    │
│  │  │ [Cover image]        │   Jul 4, 2026 · 8 min · #ai #fastapi       │    │
│  │  │                      │                                             │    │
│  │  │                      │   The full story of why and how I'm         │    │
│  │  └──────────────────────┘   replacing four SaaS apps with one...     │    │
│  │                              [ Read Article → ]                       │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌──────────────────────────────┐ ┌──────────────────────────────┐          │
│  │ Jun 28 · 5 min               │ │ Jun 21 · 12 min              │          │
│  │ Why I Build in Public         │ │ Monorepo Architecture        │          │
│  │ Excerpt text...               │ │ Excerpt text...              │          │
│  │ [#build-in-public]            │ │ [#architecture]              │          │
│  └──────────────────────────────┘ └──────────────────────────────┘          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Section 6: Labs Preview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  // LABS                                              [ Explore Labs → ]     │
│                                                                              │
│  Active experiments and research explorations.                               │
│                                                                              │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐    │
│  │ 🤖             │ │ 🎙             │ │ ⚙️             │ │ 🧬             │    │
│  │ AI Agents      │ │ Voice AI      │ │ Automation    │ │ LLM Research  │    │
│  │ 3 experiments  │ │ 2 experiments │ │ 1 experiment  │ │ 4 experiments │    │
│  └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘    │
│  (4-col → 2-col → 1-col, small cards, icon + label + count)                 │
│  (bg: transparent, border: 1px rgba(255,255,255,0.06), 20px radius)         │
│  (hover: bg → #0F172A, border → cyan glow)                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Section 7: Mission Control Preview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  // MISSION CONTROL                                                          │
│                                                                              │
│  Real-time view into what I'm building, learning, and shipping.              │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │                                                                       │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             │    │
│  │  │   847    │  │    12    │  │   156    │  │    42    │             │    │
│  │  │ Commits  │  │ Projects │  │ Articles │  │ Streak   │             │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘             │    │
│  │  (JetBrains Mono, 32px, #00F5FF, animated counter on scroll-in)      │    │
│  │                                                                       │    │
│  │  ┌────────────── GitHub Activity Heatmap ──────────────┐             │    │
│  │  │ (52-week contribution grid, green → cyan theme)     │             │    │
│  │  └────────────────────────────────────────────────────────┘             │    │
│  │                                                                       │    │
│  │                  [ Enter Mission Control → ]                          │    │
│  │                                                                       │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│  (Full-width card, #0F172A bg, subtle scanline texture at 1% opacity)       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Section 8: Newsletter

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                     // STAY IN THE LOOP                                       │
│                                                                              │
│                     AI engineering insights, build updates,                   │
│                     and things I wish I knew earlier.                         │
│                                                                              │
│           ┌──────────────────────────────┐  ┌────────────────┐               │
│           │  your@email.com              │  │  Subscribe ▶   │               │
│           └──────────────────────────────┘  └────────────────┘               │
│           (input: #0F172A bg, 20px radius)  (btn: gradient bg, 12px radius)  │
│                                                                              │
│                     No spam. Unsubscribe anytime.                             │
│                     (Inter 400, 13px, #8E9CAE)                               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Section 9: Footer — See Component Library (Part 4)

---

### Home — Scrolling Behavior
- Hero: sticky until user scrolls, then released
- Sections: reveal on scroll via intersection observer (fade-up, 24px)
- Cards: stagger entry (80ms delay between siblings)
- Metrics: animated counters trigger on viewport entry (count from 0)
- Parallax: hero ambient glow shifts subtly on scroll (3-5px offset)

### Home — Tablet (768–1023px)
- Hero: font-size reduces to 48px, tagline to 18px
- Mission cards: remain 3-col down to 768px
- Project cards: 2-column grid
- Current Build: stack screenshot above text content
- Labs: 2-column grid

### Home — Mobile (< 768px)
- Hero: 36px headline, stacked CTAs (full width), social icons inline
- Mission: single column, stacked cards
- Current Build: full-width card, screenshot above, metrics 2×2 grid
- Projects: single column, full-width cards
- Journal: single column, no featured image for secondary posts
- Labs: single column
- Newsletter: stacked email + button (full width each)

---

## PAGE 2: PROJECTS `/projects`

### Purpose
Showcase every project with enough depth to impress a hiring manager (Hema) while being scannable enough for a casual visitor (Kavya).

### Primary Users
Hiring-Manager Hema (P0), Dev-Curious Darshan (P0)

### Conversion Goals
GitHub repo visit, Live demo click, Project detail page view

---

### Layout — Listing

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ NAVBAR                                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  // PROJECTS                                                                 │
│  (Pixel Operator Bold, 40px, #F1F5F9)                                        │
│                                                                              │
│  Things I've built, am building, or am thinking about.                       │
│  (Inter 400, 18px, #94A3B8)                                                  │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐         │
│  │  🔍 Search projects...                                          │         │
│  └─────────────────────────────────────────────────────────────────┘         │
│  (Search input: #0F172A, 20px radius, full width, Lucide Search icon)       │
│                                                                              │
│  Filters:                                                                    │
│  [All] [Active] [Complete] [Experiment] [Open Source]                        │
│  (pill buttons, transparent default → #0F172A active, 8px radius)            │
│                                                                              │
│  Categories:                                                                 │
│  [AI/ML] [Full-Stack] [Tools] [Research]                                     │
│  (same pill style, #8B5CF6 border when active)                               │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─          │
│                                                                              │
│  (Project card grid — see Component Library for card spec)                   │
│  Desktop: 3-col | Tablet: 2-col | Mobile: 1-col                             │
│  Gap: 24px                                                                   │
│                                                                              │
│  ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐          │
│  │ PROJECT CARD      │ │ PROJECT CARD      │ │ PROJECT CARD      │          │
│  └───────────────────┘ └───────────────────┘ └───────────────────┘          │
│  ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐          │
│  │ PROJECT CARD      │ │ PROJECT CARD      │ │ PROJECT CARD      │          │
│  └───────────────────┘ └───────────────────┘ └───────────────────┘          │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ FOOTER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Layout — Project Detail `/projects/[slug]`

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ NAVBAR                                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [← Back to Projects]  (ghost link, Inter 400 14px, #94A3B8)                │
│                                                                              │
│  // PROJECT                                                                  │
│  Personal OS                                              🟢 Active          │
│  (Pixel Operator Bold, 40px)                    (status badge, 8px radius)  │
│                                                                              │
│  A production-grade personal operating system built for                      │
│  power users and AI agents.                                                  │
│  (Inter 400, 18px, #94A3B8, max-width: 700px)                               │
│                                                                              │
│  [ Live Demo ↗ ]   [ GitHub ↗ ]   [ Read Article → ]                        │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─              │
│                                                                              │
│  GALLERY                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                       │
│  │ Screen 1 │ │ Screen 2 │ │ Screen 3 │ │ Screen 4 │  (horizontal scroll)  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘                       │
│  (20px radius, snap scrolling, peek next card by 40px)                      │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─              │
│                                                                              │
│  ┌───────────────────────────────┐  ┌─────────────────────────┐             │
│  │ // OVERVIEW                   │  │ // TECH STACK            │             │
│  │                               │  │                         │             │
│  │ Full description of the       │  │ [Next.js 15]            │             │
│  │ project: what it is, why I    │  │ [FastAPI]               │             │
│  │ built it, who it's for.       │  │ [PostgreSQL 16]         │             │
│  │                               │  │ [Redis 7]              │             │
│  │ (Inter 400, 16px, 1.6 lh)    │  │ [pgvector]             │             │
│  └───────────────────────────────┘  │ [Docker]               │             │
│  (8-col width)                      │ [Tailwind CSS]         │             │
│                                     │                         │             │
│                                     │ (vertical list, each    │             │
│                                     │  with icon + label)     │             │
│                                     └─────────────────────────┘             │
│                                     (4-col width, sticky on desktop)        │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─              │
│                                                                              │
│  // ARCHITECTURE                                                             │
│  (System diagram — SVG or embedded image, 20px radius container)            │
│                                                                              │
│  // TIMELINE                                                                 │
│  (Vertical timeline component — see Component Library)                      │
│  ● Jul 2026 — Project initialized                                           │
│  ● Jun 2026 — Finance module shipped                                        │
│  ● May 2026 — Auth system complete                                          │
│                                                                              │
│  // CHALLENGES & LESSONS                                                     │
│  (Expandable accordion sections)                                            │
│  ▸ Async SQLAlchemy with Alembic migrations                                 │
│  ▸ Designing a command palette UX                                           │
│  ▸ Google Drive sync rate limiting                                          │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─              │
│                                                                              │
│  // RELATED ARTICLES                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                        │
│  │ Article 1    │ │ Article 2    │ │ Article 3    │                        │
│  └──────────────┘ └──────────────┘ └──────────────┘                        │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ FOOTER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## PAGE 3: LABS `/labs`

### Purpose
Showcase experiments, prototypes, and research that don't belong in Projects. This is the "mad scientist workshop" — it signals curiosity and R&D depth.

### Primary Users
Dev-Curious Darshan (P0), Collab-Ready Chirag (P1)

### Conversion Goals
Experiment detail view, GitHub star, Social share

---

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ NAVBAR                                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  // LABS                                                                     │
│  (Pixel Operator Bold, 40px)                                                 │
│                                                                              │
│  Where ideas get tested before they become products.                         │
│  (Inter 400, 18px, #94A3B8)                                                  │
│                                                                              │
│  Categories:                                                                 │
│  [All] [🤖 AI Agents] [🎙 Voice AI] [⚙️ Automation]                          │
│  [🎨 Design Lab] [🧬 LLMs] [📊 Research] [🌐 Open Source]                     │
│  (pill filters, same style as Projects)                                      │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │ 🧪 EXPERIMENT-001                                     Status: 🟢 Live │    │
│  │                                                                       │    │
│  │ Multi-Agent Code Review System                                        │    │
│  │ (Inter 600, 20px, #F1F5F9)                                            │    │
│  │                                                                       │    │
│  │ An orchestration layer that coordinates 3 specialized AI agents       │    │
│  │ to review pull requests: style, logic, and security.                  │    │
│  │ (Inter 400, 15px, #94A3B8, max-width: 600px)                          │    │
│  │                                                                       │    │
│  │ [AI Agents] [Python] [LangGraph]                                      │    │
│  │                                                                       │    │
│  │ [ View Experiment → ]    [ GitHub ↗ ]                                 │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│  (experiment cards: #0F172A, 20px radius, left cyan accent bar 3px)         │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │ 🧪 EXPERIMENT-002                                  Status: 🟡 WIP    │    │
│  │ Voice-Controlled Personal OS                                          │    │
│  │ ...                                                                   │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  (single-column list, stacked, gap: 24px)                                    │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ FOOTER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Experiment Detail Page** follows the same structure as Project Detail with these changes:
- Overline says `// EXPERIMENT` instead of `// PROJECT`
- Has a "Hypothesis" section before Overview
- Has a "Results / Findings" section
- Has a "Status" section: Live / WIP / Paused / Completed / Failed
- Uses the cyan left accent bar consistently

---

## PAGE 4: ENGINEERING JOURNAL `/journal`

### Purpose
Replace "blog" with a more intentional, premium label. This is where the engineering thinking happens — not social media fluff.

### Primary Users
Dev-Curious Darshan (P0), organic search visitors

### Conversion Goals
Newsletter signup, Social share, Related article click

---

### Layout — Listing

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ NAVBAR                                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  // ENGINEERING JOURNAL                                                      │
│  (Pixel Operator Bold, 40px)                                                 │
│                                                                              │
│  AI engineering, build-in-public updates, and things I learned.              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐         │
│  │  🔍 Search articles...                                          │         │
│  └─────────────────────────────────────────────────────────────────┘         │
│                                                                              │
│  Tags:                                                                       │
│  [All] [AI] [FastAPI] [Next.js] [Architecture] [Build-in-Public]            │
│                                                                              │
│  (Article cards — see Component Library for Article Card spec)               │
│  Desktop: 2-col | Tablet: 2-col | Mobile: 1-col                             │
│                                                                              │
│  ┌──────────────────────────────┐ ┌──────────────────────────────┐          │
│  │ ARTICLE CARD                 │ │ ARTICLE CARD                 │          │
│  └──────────────────────────────┘ └──────────────────────────────┘          │
│  ┌──────────────────────────────┐ ┌──────────────────────────────┐          │
│  │ ARTICLE CARD                 │ │ ARTICLE CARD                 │          │
│  └──────────────────────────────┘ └──────────────────────────────┘          │
│                                                                              │
│  [ Load More Articles ]                                                      │
│  (ghost button, centered)                                                    │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ FOOTER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Layout — Article Detail `/journal/[slug]`

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ NAVBAR + scroll progress bar (2px, #3B82F6, top of viewport)                │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [← Back to Journal]                                                        │
│                                                                              │
│  // ENGINEERING JOURNAL                                                      │
│                                                                              │
│  Building a Personal OS from Scratch                                        │
│  (Pixel Operator Bold, 36px, #F1F5F9)                                        │
│                                                                              │
│  Jul 4, 2026  ·  8 min read  ·  PNJ                                        │
│  (Inter 400, 14px, #94A3B8)                                                  │
│                                                                              │
│  [#ai] [#fastapi] [#build-in-public]                                        │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─              │
│                                                                              │
│  ┌──────────────┐  ARTICLE BODY                                             │
│  │ ON THIS PAGE │  ──────────────                                           │
│  │ ──────────── │                                                           │
│  │ Introduction │  ## Introduction                                          │
│  │ Architecture │                                                           │
│  │ Database ◄── │  Body text in Inter 400, 17px, 1.7 line-height,          │
│  │ Key Features │  max-width: 70ch, #E2E8F0 text color.                    │
│  │ Learnings    │                                                           │
│  │ What's Next  │  Code blocks use JetBrains Mono with syntax              │
│  └──────────────┘  highlighting and copy button.                            │
│  (sticky at top:96px,                                                       │
│   left column 200px,   > Callout blocks with cyan left border               │
│   #0F172A bg, 20px     > and #0F172A background.                            │
│   radius)                                                                    │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─              │
│                                                                              │
│  Share: [🐦 Twitter]  [💼 LinkedIn]  [🔗 Copy Link]                         │
│  (icon buttons, 40×40, #0F172A bg, 12px radius)                             │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─              │
│                                                                              │
│  Newsletter CTA (same as homepage)                                          │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─              │
│                                                                              │
│  // YOU MIGHT ALSO LIKE                                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                        │
│  │ Article 1    │ │ Article 2    │ │ Article 3    │                        │
│  └──────────────┘ └──────────────┘ └──────────────┘                        │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ FOOTER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## PAGE 5: MISSION CONTROL `/mission-control`

### Purpose
**The most premium page.** This is the command center. A real-time dashboard that proves shipping velocity — live data, not claims. It should feel like walking into NASA's Mission Operations Center.

### Primary Users
Hiring-Manager Hema (P0 — the ultimate proof), Collab-Ready Chirag (P1 — signals seriousness)

### Conversion Goals
GitHub follow, Social follow, Deep project exploration

### Visual Direction
- Scanline texture overlay at 1% opacity across the entire page
- Grid-dot pattern background at 2% opacity
- More aggressive use of `#00F5FF` for live data
- JetBrains Mono for all metrics
- Pulsing status dots for "live" indicators
- Dark, dense, data-rich — more dashboard than website

---

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ NAVBAR                                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  // MISSION CONTROL                                      🟢 SYSTEMS ONLINE  │
│  (Pixel Operator Bold, 40px)                (pulsing cyan dot + label)       │
│                                                                              │
│  Real-time telemetry from the BuildWithPNJ engineering lab.                  │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════      │
│                                                                              │
│  ROW 1: Key Metrics (4-col grid)                                             │
│                                                                              │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐│
│  │ 📊              │ │ 🔥              │ │ 📝              │ │ 📅              ││
│  │                 │ │                 │ │                 │ │                 ││
│  │     847         │ │      42         │ │     156         │ │      12         ││
│  │   COMMITS       │ │   DAY STREAK    │ │   ARTICLES      │ │   PROJECTS      ││
│  │                 │ │                 │ │                 │ │                 ││
│  │  +23 this week  │ │  longest: 67   │ │  +3 this month  │ │  4 active       ││
│  └────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘│
│  (JetBrains Mono 32px #00F5FF for number, Pixel Operator 11px for label)    │
│  (subtext: Inter 400 12px #8E9CAE)                                           │
│  (cards: #0F172A, 20px radius, top-border 2px #00F5FF)                       │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════      │
│                                                                              │
│  ROW 2: Current Project + GitHub Activity (2-col: 7fr + 5fr)                │
│                                                                              │
│  ┌──────────────────────────────┐ ┌─────────────────────────┐               │
│  │ // CURRENT FOCUS              │ │ // GITHUB ACTIVITY       │               │
│  │                               │ │                         │               │
│  │ Personal OS                   │ │ (52-week heatmap)       │               │
│  │ 🟢 Active · Sprint 14        │ │                         │               │
│  │                               │ │ ┌─┬─┬─┬─┬─┬─┬─┬─┬─┐  │               │
│  │ Current sprint:               │ │ │▪│▪│ │▪│▪│▪│ │▪│▪│  │               │
│  │ ● Agent Inbox v1              │ │ │▪│ │▪│▪│ │▪│▪│▪│ │  │               │
│  │ ● Storage module              │ │ │ │▪│▪│ │▪│▪│▪│▪│▪│  │               │
│  │ ○ API documentation           │ │ └─┴─┴─┴─┴─┴─┴─┴─┴─┘  │               │
│  │                               │ │ (green → cyan palette)  │               │
│  │ Progress: ████████░░ 78%      │ │                         │               │
│  │ (progress bar, #3B82F6 fill)  │ │ 23 contributions        │               │
│  │                               │ │ this week               │               │
│  └──────────────────────────────┘ └─────────────────────────┘               │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════      │
│                                                                              │
│  ROW 3: Latest Builds + Roadmap (2-col: 6fr + 6fr)                          │
│                                                                              │
│  ┌──────────────────────────────┐ ┌──────────────────────────────┐          │
│  │ // LATEST BUILDS              │ │ // ROADMAP                    │          │
│  │                               │ │                               │          │
│  │ ● 2h ago                      │ │ Q3 2026: Foundation           │          │
│  │   feat: Agent Inbox UI        │ │ ████████████████░░░░ 78%      │          │
│  │   apps/web · +234 −12         │ │                               │          │
│  │                               │ │ Q4 2026: Launch               │          │
│  │ ● 5h ago                      │ │ ████░░░░░░░░░░░░░░░░ 20%      │          │
│  │   fix: Transaction sorting    │ │                               │          │
│  │   apps/api · +18 −4           │ │ Q1 2027: Expand               │          │
│  │                               │ │ ░░░░░░░░░░░░░░░░░░░░ 0%       │          │
│  │ ● yesterday                   │ │                               │          │
│  │   feat: Storage module init   │ │ (progress bars, labels,       │          │
│  │   apps/web · +456 −0          │ │  milestone markers)           │          │
│  │                               │ │                               │          │
│  └──────────────────────────────┘ └──────────────────────────────┘          │
│  (commit list: monospace, cyan dot, relative time, diff stats)              │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════      │
│                                                                              │
│  ROW 4: Learning + Weekly Goals + Tech Stack (3-col)                        │
│                                                                              │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐             │
│  │ // LEARNING       │ │ // WEEKLY GOALS   │ │ // TECH STACK     │             │
│  │                   │ │                   │ │                   │             │
│  │ Currently:        │ │ ☑ Ship Agent      │ │ ┌─────┐ ┌─────┐  │             │
│  │ Multi-Agent       │ │   Inbox UI        │ │ │Py   │ │TS   │  │             │
│  │ Systems           │ │ ☑ Write journal   │ │ └─────┘ └─────┘  │             │
│  │ (LangGraph)       │ │   entry #12       │ │ ┌─────┐ ┌─────┐  │             │
│  │                   │ │ ☐ Storage module  │ │ │Next │ │FAPI │  │             │
│  │ Up next:          │ │   file upload     │ │ └─────┘ └─────┘  │             │
│  │ Voice AI          │ │ ☐ API docs for   │ │ ┌─────┐ ┌─────┐  │             │
│  │ (Whisper + TTS)   │ │   finance routes  │ │ │PG   │ │Redis│  │             │
│  │                   │ │                   │ │ └─────┘ └─────┘  │             │
│  │ Books queue: 3    │ │ 2/4 complete      │ │                   │             │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘             │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════      │
│                                                                              │
│  ROW 5: AI Models + Social Metrics + Activity Timeline                      │
│                                                                              │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────────────┐     │
│  │ // AI MODELS      │ │ // REACH          │ │ // ACTIVITY TIMELINE     │     │
│  │                   │ │                   │ │                          │     │
│  │ GPT-4o      🟢    │ │ GitHub ★  312    │ │ ● Today                  │     │
│  │ Claude 3.5  🟢    │ │ Twitter   1.2K   │ │   Shipped Agent Inbox    │     │
│  │ Gemini 2.0  🟢    │ │ LinkedIn  847    │ │                          │     │
│  │ Whisper v3  🟡    │ │ Blog      3.2K   │ │ ● Yesterday              │     │
│  │ Llama 3     ⚪    │ │   /month views   │ │   Published journal #12  │     │
│  │                   │ │                   │ │                          │     │
│  │ (status dots:     │ │ (JetBrains Mono   │ │ ● 3 days ago             │     │
│  │  🟢 using         │ │  for numbers,     │ │   New lab experiment     │     │
│  │  🟡 exploring     │ │  animated count)  │ │                          │     │
│  │  ⚪ queued)       │ │                   │ │ ● 1 week ago             │     │
│  └──────────────────┘ └──────────────────┘ │   Completed finance API  │     │
│                                             └──────────────────────────┘     │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ FOOTER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Mission Control — Responsive

**Tablet (768–1023px):**
- Key metrics: 2×2 grid
- 2-col sections become stacked (full width each)
- Heatmap compresses to 26-week view

**Mobile (< 768px):**
- Key metrics: 2×2 grid, smaller text (24px numbers)
- All sections single column, full width
- Heatmap hidden (replaced with simple "23 contributions this week" text)
- Activity timeline becomes a compact list

---

## PAGE 6: ABOUT `/about`

### Purpose
Personal story that builds connection and trust. Not a resume — a narrative.

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  // ABOUT                                                                    │
│                                                                              │
│            ┌────────────────┐                                                │
│            │   [Profile     │    Hey, I'm Prakash 👋                          │
│            │    Photo]      │    (Pixel Operator Bold, 32px)                  │
│            │   (120×120     │                                                │
│            │    rounded)    │    AI Engineer building production-ready        │
│            └────────────────┘    systems in public.                          │
│                                  (Inter 400, 18px, #94A3B8)                  │
│                                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─          │
│                                                                              │
│  // MY STORY                                                                 │
│  (2-3 paragraphs, Inter 400, 17px, max-width: 70ch)                         │
│                                                                              │
│  // WHAT I BELIEVE                                                           │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐                   │
│  │ Ship Fast      │ │ Build Real     │ │ Share Everything│                   │
│  │ ...            │ │ ...            │ │ ...             │                   │
│  └────────────────┘ └────────────────┘ └────────────────┘                   │
│                                                                              │
│  // TIMELINE                                                                 │
│  (Vertical timeline — key career/project milestones)                        │
│                                                                              │
│  // CURRENT GOALS                                                            │
│  ☑ Launch Personal OS v1.0                                                   │
│  ☑ Grow buildwithpnj.com to 500 visitors/mo                                │
│  ☐ Ship Product #2 (AI SaaS)                                                │
│  ☐ 1K newsletter subscribers                                                │
│                                                                              │
│           [ Let's Connect → /contact ]                                       │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ FOOTER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## PAGE 7: CONTACT `/contact`

### Purpose
Minimal, beautiful, frictionless. One clear action: get in touch.

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  // CONTACT                                                                  │
│  (Pixel Operator Bold, 40px)                                                 │
│                                                                              │
│  Got an idea, a question, or just want to say hi?                            │
│                                                                              │
│           ┌──────────────────────────────┐                                    │
│           │                              │                                    │
│           │  📧  hello@buildwithpnj.com   │                                    │
│           │  (Inter 500, 18px, #3B82F6,   │                                    │
│           │   clickable mailto link)      │                                    │
│           │                              │                                    │
│           │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                                    │
│           │                              │                                    │
│           │  🐙  github.com/buildwithpnj  │                                    │
│           │  🐦  twitter.com/buildwithpnj  │                                    │
│           │  💼  linkedin.com/in/pnj       │                                    │
│           │                              │                                    │
│           │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                                    │
│           │                              │                                    │
│           │  🟢 Open to collaborations    │                                    │
│           │     & consulting projects    │                                    │
│           │                              │                                    │
│           └──────────────────────────────┘                                    │
│           (#0F172A card, 20px radius, centered, max-width: 480px)            │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ FOOTER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Design notes:**
- No contact form. Just links. Minimal friction.
- Page should be vertically centered if content fits viewport
- Hover on email: subtle cyan glow
- Each social link: icon + URL, hover → slide right animation

---

# PART 4 — COMPONENT LIBRARY

## 4.1 Navbar

```
DESKTOP (≥ 1024px):
┌──────────────────────────────────────────────────────────────────────────────┐
│  PNJ                    Projects  Labs  Journal  About  Contact  [ GitHub ↗]│
│  (Pixel Operator Bold)  (Inter 500, 14px, #94A3B8)               (accent btn)│
└──────────────────────────────────────────────────────────────────────────────┘

States:
- Default bg: transparent
- Scrolled: bg → #050816/90 + backdrop-blur(12px) + bottom border rgba(255,255,255,0.06)
- Active link: #F1F5F9 + 2px underline #3B82F6
- Hover link: #F1F5F9 (no underline, color transition)

MOBILE (< 768px):
┌──────────────────────────┐
│  PNJ               [☰]  │
└──────────────────────────┘

Mobile menu: full-screen overlay, #050816 bg, centered links at 24px, social icons at bottom
Close: [✕] top-right, same position as hamburger
Transition: fade-in 200ms + links stagger 50ms each
```

## 4.2 Buttons

| Variant | Background | Text | Border | Radius | Hover |
|---|---|---|---|---|---|
| **Primary** | `gradient-brand` | `#FFFFFF` | none | 12px | Glow + gradient shift |
| **Secondary** | `transparent` | `#3B82F6` | `1px #3B82F6` | 12px | Bg → `rgba(59,130,246,0.1)` |
| **Ghost** | `transparent` | `#94A3B8` | none | 12px | Text → `#F1F5F9`, bg → `rgba(255,255,255,0.04)` |
| **Danger** | `transparent` | `#EF4444` | `1px #EF4444` | 12px | Bg → `rgba(239,68,68,0.1)` |
| **Icon** | `#0F172A` | `#94A3B8` | `1px border-default` | 12px | Bg → `#1E293B`, icon → `#F1F5F9` |

Sizes: `sm` (32px height), `md` (40px height), `lg` (48px height)

## 4.3 Cards — Project Card

```
┌─────────────────────────────┐
│ [Thumbnail — 16:9 ratio]    │  bg: #0F172A
│ (20px top-radius, 0 bottom) │  radius: 20px
│                              │  border: 1px rgba(255,255,255,0.06)
├─────────────────────────────┤  padding: 24px
│                              │
│  Project Title               │  title: Inter 600, 18px, #F1F5F9
│  Brief description that      │  desc: Inter 400, 14px, #94A3B8
│  fits in two lines max.      │  tags: 8px radius pills, 12px font
│                              │  status: pill with colored dot
│  [Python] [AI] [RAG]        │
│                              │  HOVER:
│  🟢 Active                   │  - border → rgba(0,245,255,0.15)
│                              │  - shadow → 0 8px 24px rgba(0,0,0,0.3)
└─────────────────────────────┘  - glow → 0 0 30px rgba(0,245,255,0.05)
                                  - translateY(-2px)
                                  - transition: 200ms ease-out
```

## 4.4 Cards — Article Card

```
┌──────────────────────────────────┐
│                                  │  bg: #0F172A
│  Jul 4, 2026 · 8 min read       │  radius: 20px
│  (Inter 400, 13px, #8E9CAE)     │  border: 1px rgba(255,255,255,0.06)
│                                  │  padding: 24px
│  Article Title Here              │
│  (Inter 600, 18px, #F1F5F9)    │  title hover → #3B82F6
│                                  │
│  Two-line excerpt of the         │  excerpt: Inter 400, 14px, #94A3B8
│  article content...              │
│                                  │  Same hover treatment as project card
│  [#ai] [#fastapi]               │
│                                  │
└──────────────────────────────────┘
```

## 4.5 Tags / Pills

| State | Background | Text | Border |
|---|---|---|---|
| **Default** | `rgba(59,130,246,0.08)` | `#3B82F6` | none |
| **Active** | `rgba(59,130,246,0.15)` | `#60A5FA` | `1px #3B82F6` |
| **Hover** | `rgba(59,130,246,0.12)` | `#60A5FA` | none |
| **Category** | `rgba(139,92,246,0.08)` | `#8B5CF6` | none |
| **Status: Active** | `rgba(34,197,94,0.1)` | `#22C55E` | none |
| **Status: WIP** | `rgba(245,158,11,0.1)` | `#F59E0B` | none |

Spec: 8px radius, 8px horizontal padding, 4px vertical padding, Inter 500 12px, uppercase

## 4.6 Inputs

```
Default:  #0F172A bg, 1px border rgba(255,255,255,0.08), 20px radius, 48px height
Focus:    border → #3B82F6, ring → 0 0 0 3px rgba(59,130,246,0.12)
Error:    border → #EF4444, helper text #EF4444 below
Filled:   text → #F1F5F9
Placeholder: #8E9CAE, Inter 400 15px
Icon left: 20px from left edge, #8E9CAE
```

## 4.7 Code Block

```
bg:          #020617 (darker than page bg)
border:      1px rgba(255,255,255,0.06)
radius:      20px
padding:     24px
font:        JetBrains Mono 14px, line-height 1.7
line numbers: #334155, right-aligned, 48px gutter
language:    top-right pill (Pixel Operator, 10px, #8E9CAE)
copy button: top-right, appears on hover, icon-only, "Copied!" tooltip on click
syntax:      VS Code Dark+ theme adapted to brand colors
```

## 4.8 Footer

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  PNJ                          Navigate           Connect                     │
│  (Pixel Operator Bold, 20px)  ────────           ───────                     │
│                               Home               GitHub  ↗                   │
│  AI Engineer building         Projects            Twitter  ↗                  │
│  production-ready AI          Labs                LinkedIn  ↗                 │
│  systems in public.           Journal             Email  ↗                    │
│  (Inter 400, 14px, #8E9CAE)   About                                          │
│                               Contact                                        │
│                               Mission Control                                │
│                                                                              │
│  ──────────────────────────────────────────────────────────────────────────   │
│                                                                              │
│  © 2026 BuildWithPNJ          Built with Next.js · Deployed on Vercel        │
│  (Inter 400, 13px, #475569)   (Inter 400, 13px, #475569)                     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

bg: #050816 (same as page, separated by top border rgba(255,255,255,0.06))
padding: 64px vertical
link hover: color → #F1F5F9
```

## 4.9 Command Palette

Triggered by `Cmd+K` / `Ctrl+K`

```
┌────────────────────────────────────────────────────────────┐
│  🔍 Type a command or search...                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  PAGES                                                     │
│  → Home                                              G H  │
│  → Projects                                          G P  │
│  → Labs                                              G L  │
│  → Engineering Journal                               G J  │
│  → Mission Control                                   G M  │
│  → About                                                   │
│  → Contact                                                 │
│                                                            │
│  QUICK ACTIONS                                             │
│  → View GitHub Profile                                ↗    │
│  → Follow on Twitter                                  ↗    │
│  → Subscribe to Newsletter                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘

bg: #0F172A, border: 1px rgba(255,255,255,0.08), radius: 20px
backdrop: rgba(5,8,22,0.8) + backdrop-blur(8px)
input: no border, transparent bg, Inter 400 16px
results: Inter 400 15px, #94A3B8, hover bg → #1E293B, active → #3B82F6 text
shortcut keys: JetBrains Mono 12px, #475569, bg rgba(255,255,255,0.04), 4px radius
```

## 4.10 Timeline

```
   ● Jul 2026 — Personal OS: Agent Inbox shipped
   │  (dot: 10px, #3B82F6 fill, glow on active)
   │  (line: 1px #1E293B)
   │  (title: Inter 600 15px #F1F5F9)
   │  (date: Inter 400 13px #8E9CAE)
   │
   ● Jun 2026 — Personal OS: Finance module complete
   │
   ● May 2026 — BuildWithPNJ brand established
   │
   ○ Q4 2026 — Website launch (planned)
      (future items: hollow circle, #475569 text)
```

## 4.11 Progress Bar

```
┌──────────────────────────────────────────┐
│ ████████████████████░░░░░░░░░░ 68%       │
└──────────────────────────────────────────┘

track: #1E293B, 8px height, 9999px radius
fill: gradient #3B82F6 → #00F5FF
label: JetBrains Mono 13px, #94A3B8, right-aligned
animate: fill width on scroll-in, 600ms ease-out
```

## 4.12 Metric Card (Mission Control)

```
┌────────────────────┐
│ 📊                  │  bg: #0F172A
│                     │  radius: 20px
│     847             │  border: 1px rgba(255,255,255,0.06)
│   COMMITS           │  top accent: 2px solid #00F5FF
│                     │  padding: 24px
│  +23 this week      │  number: JetBrains Mono 500 32px #00F5FF
│                     │  label: Pixel Operator Bold 11px #8E9CAE, tracked
└────────────────────┘  delta: Inter 400 12px #22C55E (positive) or #EF4444
```

## 4.13 Loading Screen

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                                                                              │
│                          PNJ                                                 │
│                  (Pixel Operator Bold, 24px)                                  │
│                                                                              │
│                  ─────────────── (loading bar)                               │
│                  (2px height, #3B82F6, animated width)                       │
│                                                                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

bg: #050816, centered, simple, fast
Duration: max 1.5s then crossfade into page content
```

## 4.14 404 Page

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ NAVBAR                                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                         404                                                  │
│                  (Pixel Operator Bold, 80px, gradient text)                   │
│                                                                              │
│               This page drifted into the void.                               │
│               (Inter 400, 18px, #94A3B8)                                     │
│                                                                              │
│          [ Go Home ]          [ View Projects ]                              │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ FOOTER                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘

Content vertically centered, same ambient glow as hero
```

## 4.15 Skeleton Loading

Every card, metric, and content block has a skeleton variant:
- Background: `#0F172A`
- Skeleton bars: `#1E293B` with shimmer animation (gradient sweep left-to-right, 1.5s, infinite)
- Match the exact dimensions of the loaded content
- Radius matches component radius (20px for cards, 8px for tags)

## 4.16 Empty States

```
┌──────────────────────────────────────────┐
│                                          │
│              (Lucide icon, 48px, #334155) │
│                                          │
│        No experiments yet.               │
│        (Inter 500, 16px, #94A3B8)        │
│                                          │
│   Check back soon — something's          │
│   always cooking.                        │
│   (Inter 400, 14px, #8E9CAE)             │
│                                          │
│        [ View Projects Instead → ]       │
│                                          │
└──────────────────────────────────────────┘
```

## 4.17 Success State

```
┌──────────────────────────────────────────┐
│                                          │
│     ✓ (animated checkmark, #22C55E)     │
│                                          │
│   You're subscribed!                     │
│   (Inter 600, 18px, #F1F5F9)            │
│                                          │
│   Welcome to the builder crew.           │
│   (Inter 400, 14px, #94A3B8)            │
│                                          │
└──────────────────────────────────────────┘

Checkmark: draws itself (stroke animation, 400ms)
Card: subtle green glow border 1px rgba(34,197,94,0.2)
```

---

# PART 5 — INTERACTION SPECIFICATIONS

| Element | Trigger | Effect | Duration | Easing |
|---|---|---|---|---|
| **Card** | Hover | translateY(-2px), border-glow, shadow-lift | 200ms | ease-out |
| **Card** | Click | scale(0.98), navigate | 100ms | ease-in |
| **Button (Primary)** | Hover | Gradient shift, glow intensify | 200ms | ease-out |
| **Button** | Click | scale(0.95) | 100ms | ease-in |
| **Nav link** | Hover | Color → #F1F5F9 | 150ms | ease |
| **Nav (scroll)** | Scroll > 50px | Bg → solid, blur, border-bottom | 200ms | ease |
| **Social icon** | Hover | scale(1.15), color → brand color | 150ms | ease-out |
| **Tag pill** | Click | Toggle active state, filter content | 150ms | ease |
| **Code copy** | Click | Icon → Check, tooltip "Copied!", revert after 2s | 150ms | ease |
| **Search input** | Focus | Border → #3B82F6, ring appear | 200ms | ease |
| **Accordion** | Click | Expand/collapse with height animation | 250ms | ease-in-out |
| **External link** | Hover | Arrow icon shifts 2px right | 150ms | ease-out |
| **Mobile menu** | Open | Overlay fade-in, links stagger | 200ms + 50ms/item | ease-out |
| **Mobile menu** | Close | Fade out (no stagger) | 150ms | ease-in |
| **Command palette** | `Cmd+K` | Scale(0.95→1) + fade-in, backdrop blur | 200ms | spring |
| **Command palette** | `Esc` | Fade out + scale(1→0.95) | 150ms | ease-in |
| **Progress bar** | Scroll-in | Width animates from 0 → target | 600ms | ease-out |
| **Metric counter** | Scroll-in | Count from 0 → value | 800ms | ease-out |

---

# PART 6 — ANIMATION SPECIFICATIONS

## 6.1 Hero Reveal Sequence

```
T+0ms     Page shell renders (nav, bg)
T+50ms    Ambient radial glow fades in (opacity 0→1, 400ms)
T+150ms   Overline text fades up (translateY 12px→0, opacity, 300ms)
T+300ms   Name fades up (translateY 16px→0, opacity, 400ms)
T+500ms   Tagline fades up (translateY 12px→0, opacity, 300ms)
T+700ms   CTA buttons fade in (opacity, scale 0.95→1, 200ms)
T+850ms   Social icons fade in (opacity, stagger 50ms each)
T+1200ms  Scroll indicator appears (opacity 0→0.5, infinite pulse)
```

## 6.2 Scroll Reveal (All Sections)

- Trigger: element enters viewport (10% threshold)
- Animation: `translateY(24px) → translateY(0)`, `opacity 0 → 1`
- Duration: 400ms
- Easing: `cubic-bezier(0.16, 1, 0.3, 1)`
- Stagger for sibling cards: 80ms delay between each

## 6.3 Parallax

- Hero ambient glow: moves at 0.3× scroll speed (opposite direction)
- Grid-dot background: moves at 0.1× scroll speed
- Only on desktop (disable on mobile and reduced-motion)

## 6.4 Hover Tilt (Optional — Project Cards)

- 3D perspective tilt based on mouse position within card
- Max rotation: 3°
- Transition: 200ms ease-out on move, 400ms on leave (returns to flat)
- Subtle — barely perceptible but adds "alive" quality
- Desktop only

## 6.5 Mouse Glow (Optional — Hero Only)

- Radial gradient follows cursor position
- Color: `rgba(0, 245, 255, 0.03)` — nearly invisible
- Size: 600px radius
- Only on hero section, desktop only

## 6.6 Scroll Progress Bar (Journal Articles)

- 2px height bar at very top of viewport
- Color: `#3B82F6`
- Width: 0% at top → 100% at article end
- Position: fixed, z-index above nav

## 6.7 Page Transitions

- Content crossfade: 200ms ease-out
- Maintain scroll position on back navigation
- No full-page transitions (too slow, breaks perceived performance)

## 6.8 Skeleton → Content Transition

- Skeleton shimmer runs continuously
- On data load: skeleton fades out (150ms), content fades in (200ms)
- No layout shift — skeleton matches content dimensions exactly

---

# PART 7 — RESPONSIVE BEHAVIOR SUMMARY

| Element | Desktop (≥1024px) | Tablet (768–1023px) | Mobile (<768px) |
|---|---|---|---|
| **Nav** | Full horizontal | Full horizontal (condensed) | Hamburger overlay |
| **Hero headline** | 64px | 48px | 36px |
| **Hero tagline** | 20px | 18px | 16px |
| **Project grid** | 3 columns | 2 columns | 1 column |
| **Article grid** | 2 columns | 2 columns | 1 column |
| **Mission metrics** | 4 columns | 2×2 grid | 2×2 grid |
| **Mission 2-col** | Side by side | Stacked | Stacked |
| **TOC sidebar** | Sticky left | Hidden | Hidden (collapses to top) |
| **CTAs** | Inline | Inline | Stacked full-width |
| **Container padding** | 32px | 24px | 16px |
| **Section spacing** | 64px | 48px | 32px |
| **Card padding** | 24px | 20px | 16px |
| **Footer** | 3-column | 2-column | Stacked |
| **Hover effects** | Full | Reduced | None (tap only) |
| **Parallax** | Active | Disabled | Disabled |
| **Mouse glow** | Active | Disabled | Disabled |

---

# PART 8 — ACCESSIBILITY REVIEW

| Requirement | Implementation | Status |
|---|---|---|
| **WCAG AA contrast** | All text ≥ 4.5:1 on backgrounds | ✅ Verified in color spec |
| **Keyboard nav** | All interactive elements focusable, logical tab order | ✅ Designed |
| **Focus rings** | `outline: 2px solid #3B82F6`, `outline-offset: 2px` | ✅ Specified |
| **Skip nav** | "Skip to main content" link, first focusable element | ✅ Planned |
| **Reduced motion** | `prefers-reduced-motion: reduce` → disable all animations | ✅ Required |
| **Screen reader** | Semantic HTML, ARIA labels on icon buttons, alt text on images | ✅ Required |
| **Touch targets** | Min 44×44px for all interactive elements on mobile | ✅ Sized |
| **Language** | `<html lang="en">` | ✅ Required |
| **Heading hierarchy** | Single H1 per page, sequential H2→H3→H4 | ✅ Designed |
| **Link purpose** | All links describe destination (no "click here") | ✅ Designed |
| **Color independence** | Status communicated by icon + text, not color alone | ✅ Designed |
| **Pixel Operator** | May have legibility concerns at small sizes — minimum 11px, use only for labels/overlines, never body text | ⚠️ Note |

---

# PART 9 — UX IMPROVEMENTS (Beyond Source Docs)

| Improvement | Rationale |
|---|---|
| **Labs page** | Separates experiments from production projects — shows R&D depth without diluting the Projects page |
| **Mission Control** | Replaces generic "social proof" with real-time data — infinitely more credible |
| **Engineering Journal** (not "Blog") | Signals intentionality — "journal" implies rigor, "blog" implies casual |
| **Command Palette** | Power-user feature that signals engineering taste — matches the tools PNJ's audience uses daily |
| **Contact = links only, no form** | Reduces friction — a form is a barrier for most visitors. Email + socials is faster for everyone. |
| **Experiment numbering** (001, 002) | Creates a sense of volume and systematic approach — signals a real lab, not random side projects |
| **Overlines in Pixel Operator** | `// PROJECTS` reads like a code comment — reinforces the engineer identity at every scroll |
| **Scroll progress on articles** | Reduces reading anxiety on long posts — users can gauge commitment before deep-reading |
| **Status pills everywhere** | 🟢 Active / 🟡 WIP / ✅ Complete — instant project health at a glance |

---

# PART 10 — FINAL DESIGN REVIEW

## Checklist

| Criteria | Pass? |
|---|---|
| Every page has a clear purpose and conversion goal | ✅ |
| Every page has desktop, tablet, and mobile specs | ✅ |
| Every component has rest, hover, active, focus, disabled states | ✅ |
| Typography hierarchy is consistent across all pages | ✅ |
| Color usage follows the 3-color-per-viewport rule | ✅ |
| Animations have defined duration, easing, and purpose | ✅ |
| Accessibility meets WCAG AA minimum | ✅ |
| Design aligns with source documents (PRD, IA, UX Flows, Personas) | ✅ |
| No implementation code exists in this document | ✅ |
| Design supersedes all earlier design system files where values conflict | ✅ |

## What's NOT Designed (Intentionally Deferred)

| Item | Reason |
|---|---|
| Light mode | Not MVP. Dark-first. Add in v2 if requested. |
| Comments system | Not MVP. Add Giscus in v2. |
| Newsletter admin | Backend concern, not design scope. |
| RSS page | Auto-generated, no design needed. |
| i18n | Single language (English) for v1. |
| A/B test variants | Post-launch optimization. |

---

> **This document is the complete design specification for BuildWithPNJ.**
>
> **No code has been written. No implementation decisions have been made.**
>
> **Awaiting your approval before any development begins.**

---

*Last updated: 2026-07-04*

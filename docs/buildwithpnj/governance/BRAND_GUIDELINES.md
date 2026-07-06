# BuildWithPNJ — Brand Guidelines

> The definitive guide to the BuildWithPNJ visual and verbal identity.
> Follow these guidelines to maintain consistency across every touchpoint.

---

## 1. Brand Identity

### 1.1 Brand Name

| Usage | Format |
|---|---|
| **Primary** | `BuildWithPNJ` |
| **Domain / Handle** | `buildwithpnj` |
| **Conversational** | "Build With PNJ" |
| **Short Form** | `PNJ` |

- Always capitalize **B**, **W**, and **PNJ** when using the full brand name.
- The lowercase `buildwithpnj` form is reserved for URLs, usernames, and handles.

### 1.2 Tagline Options

| Option | Tone |
|---|---|
| _"Engineering the AI-powered future, one product at a time."_ | Visionary |
| _"Ship fast. Build real. Share everything."_ | Builder culture |
| _"AI Engineering × Building in Public"_ | Descriptor |

> **Recommended primary tagline:** _"Ship fast. Build real. Share everything."_

### 1.3 Brand Personality

BuildWithPNJ is:

- **Technical but accessible** — Deep engineering, explained clearly
- **Builder-first** — We ship, we don't just talk
- **Transparent** — Build in public, share the wins and the failures
- **Premium but approachable** — High-quality output, not elitist
- **AI-native** — AI isn't a feature, it's the foundation

---

## 2. Visual Identity

### 2.1 Color Palette

#### Primary Colors

| Name | Hex | HSL | Usage |
|---|---|---|---|
| **Midnight** | `#0A0A0F` | `240° 20% 5%` | Primary background, dark surfaces |
| **Electric Indigo** | `#6366F1` | `239° 84% 67%` | Primary accent, CTAs, links |
| **Arctic White** | `#FAFAFA` | `0° 0% 98%` | Light text, light backgrounds |

#### Secondary Colors

| Name | Hex | HSL | Usage |
|---|---|---|---|
| **Neon Violet** | `#8B5CF6` | `258° 90% 66%` | Gradients, highlights |
| **Cyan Pulse** | `#06B6D4` | `188° 95% 43%` | Accents, data viz, success states |
| **Warm Slate** | `#94A3B8` | `215° 16% 65%` | Secondary text, muted elements |
| **Carbon** | `#1E1E2E` | `240° 21% 15%` | Cards, elevated surfaces |

#### Semantic Colors

| Name | Hex | Usage |
|---|---|---|
| **Success** | `#22C55E` | Positive states, confirmations |
| **Warning** | `#F59E0B` | Alerts, caution states |
| **Error** | `#EF4444` | Errors, destructive actions |
| **Info** | `#3B82F6` | Informational banners |

#### Gradient

```css
/* Primary brand gradient */
background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #06B6D4 100%);
```

### 2.2 Typography

| Role | Font | Weight | Size |
|---|---|---|---|
| **Display / Headlines** | `Space Grotesk` | 700 (Bold) | 36–72px |
| **Body / UI** | `Inter` | 400 (Regular), 500 (Medium), 600 (SemiBold) | 14–18px |
| **Code / Monospace** | `JetBrains Mono` | 400, 500 | 13–15px |

**Fallback stacks:**
```css
--font-display: 'Space Grotesk', 'Inter', system-ui, sans-serif;
--font-body: 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
```

### 2.3 Logo

> ⚠️ **Logo not yet finalized.** Place final assets in `brand/assets/logos/`.

**Logo requirements:**
- Wordmark: "BuildWithPNJ" in Space Grotesk Bold
- Icon: Abstract geometric mark evoking "build" / "construct" / "AI circuit"
- Variants needed:
  - Full wordmark (horizontal)
  - Icon only (square, for avatars)
  - Light on dark
  - Dark on light
  - Monochrome (white, black)
- Formats: SVG (primary), PNG (@1x, @2x, @3x), ICO (favicon)

### 2.4 Iconography

- Use **Lucide React** icons (consistent with shadcn/ui)
- Stroke width: `1.5px` (default)
- Size: `20px` for inline, `24px` for navigation, `48px` for features

### 2.5 Spacing & Layout

- Base unit: `4px`
- Standard spacing scale: `4, 8, 12, 16, 24, 32, 48, 64, 96, 128`
- Border radius: `8px` (cards), `12px` (modals), `9999px` (pills/badges)
- Max content width: `1280px`

### 2.6 Dark Mode

Dark mode is the **primary** design context. All designs should be built dark-first:

| Layer | Color |
|---|---|
| Page background | `#0A0A0F` (Midnight) |
| Card / Surface | `#1E1E2E` (Carbon) |
| Elevated surface | `#2A2A3E` |
| Border | `rgba(255, 255, 255, 0.08)` |
| Primary text | `#FAFAFA` (Arctic White) |
| Secondary text | `#94A3B8` (Warm Slate) |

---

## 3. Voice & Tone

### 3.1 Core Voice Attributes

| Attribute | Description | Example |
|---|---|---|
| **Direct** | Get to the point. No fluff. | ✅ "Here's how it works." ❌ "In this section, we'll explore..." |
| **Technical** | Respect the reader's intelligence. Use precise terms. | ✅ "We use pgvector for semantic search." ❌ "We use a special database thing." |
| **Energetic** | Convey momentum and excitement about building. | ✅ "Just shipped the finance module 🚀" ❌ "The finance module is now available." |
| **Honest** | Share failures and learnings, not just wins. | ✅ "This took 3 rewrites. Here's why." ❌ "Building this was straightforward." |

### 3.2 Writing Rules

1. **Use active voice.** _"I built the API"_ not _"The API was built."_
2. **First person singular.** This is a personal brand — own it.
3. **Short paragraphs.** Max 3–4 sentences.
4. **Use code snippets** to illustrate technical points.
5. **Emojis are fine** in social content, sparingly in docs. 🎯
6. **No corporate speak.** _"Leverage synergies"_ → immediate disqualification.

### 3.3 Tone by Context

| Context | Tone |
|---|---|
| **Blog posts** | Conversational + technical. Teach by sharing the build process. |
| **Twitter/X** | Punchy, opinionated, visual. Threads > single tweets. |
| **LinkedIn** | Professional but human. Focus on insights and lessons. |
| **GitHub READMEs** | Clear, structured, developer-friendly. |
| **Product UI** | Concise, helpful, action-oriented. |
| **Error messages** | Human, specific, suggest next steps. |

---

## 4. Social Media

### 4.1 Platform Strategy

| Platform | Purpose | Posting Cadence |
|---|---|---|
| **Twitter / X** | Primary — build in public, hot takes, threads | Daily |
| **LinkedIn** | Professional network, longer insights | 2–3× / week |
| **GitHub** | Code, repos, open source contributions | Continuous |
| **YouTube** | Demos, walkthroughs, tutorials (future) | 1× / week (Phase 2) |
| **Dev.to / Hashnode** | Blog cross-posting for reach | With each blog post |

### 4.2 Content Pillars

1. **Build in Public** — Progress updates, what I shipped, what I learned
2. **AI Engineering** — Tutorials, deep dives, architectural decisions
3. **Tools & Products** — Feature launches, demos, use cases
4. **Hot Takes** — Opinions on AI, dev tools, building products

### 4.3 Handle Consistency

All platforms: `@buildwithpnj`

---

## 5. File Naming Conventions

| Type | Convention | Example |
|---|---|---|
| Brand docs | `UPPER_SNAKE_CASE.md` | `BRAND_GUIDELINES.md` |
| Blog posts | `YYYY-MM-DD-slug.md` | `2026-07-04-building-personal-os.md` |
| Logo files | `logo-variant-size.ext` | `logo-full-dark-2x.png` |
| Social templates | `platform-type-variant.ext` | `twitter-thread-header.png` |
| Components | `kebab-case.tsx` | `command-palette.tsx` |

---

*Last updated: 2026-07-04*

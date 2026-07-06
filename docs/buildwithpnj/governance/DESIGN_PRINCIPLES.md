# BuildWithPNJ — Design Principles

> The design philosophy behind everything BuildWithPNJ ships.
> These principles guide every UI decision — from the brand website to product interfaces.

---

## 1. Core Principles

### 1.1 ⚡ Speed Is a Feature

> _"If a user has to wait, they've already lost trust."_

Every interaction should feel instant. Performance isn't an optimization pass — it's a design constraint from the start.

| Rule | Implementation |
|---|---|
| Pages load in < 2 seconds | Static generation, image optimization, code splitting |
| Interactions respond in < 100ms | Optimistic updates, local state, skeleton screens |
| Animations never block | GPU-accelerated transforms, `will-change` hints |
| No layout shift | Explicit dimensions, font-display: swap, reserved space |

---

### 1.2 🌑 Dark-First, Always

> _"We live in terminals and code editors. Dark mode isn't a feature — it's the default."_

The brand is dark-native. Light mode exists as an accessibility option, not the primary experience.

| Rule | Implementation |
|---|---|
| Design in dark first | All mockups and reviews start with dark palette |
| Contrast ratios ≥ 4.5:1 | WCAG AA minimum for all text |
| Subtle depth, not borders | Use `box-shadow`, `backdrop-blur`, and surface color variation |
| Accent colors pop on dark | Electric Indigo, Cyan Pulse — chosen for dark backgrounds |

---

### 1.3 ✨ Progressive Disclosure

> _"Show what matters now. Reveal complexity when they're ready."_

Don't overwhelm. Present the essential information first and let users drill deeper.

| Level | What's Shown | Example |
|---|---|---|
| **Glance** (1s) | Title, status, key metric | Project card on homepage |
| **Scan** (5s) | Description, tags, primary CTA | Project card expanded |
| **Read** (30s+) | Full details, architecture, learnings | Project detail page |

---

### 1.4 🎯 Every Element Earns Its Space

> _"If it doesn't serve the user, it doesn't belong on screen."_

No decorative filler. No "lorem ipsum" sections. Every pixel either informs, guides, or delights.

| Question | If No → Remove It |
|---|---|
| Does this help the user accomplish their goal? | Remove |
| Does this reduce cognitive load? | Remove |
| Does this create a moment of delight? | Remove |
| Would the user miss it if it was gone? | Remove |

---

### 1.5 🧱 Consistent, Not Uniform

> _"Reuse patterns, not pixels. Same DNA, unique expression."_

Components share a design language but adapt to context. A card on the homepage and a card in the dashboard share spacing and radius — but their content density differs.

| Shared | Adapted |
|---|---|
| Border radius (8px) | Content layout per context |
| Color palette | Opacity and tint per elevation |
| Spacing scale (4px base) | Density per viewport |
| Typography scale | Weight per hierarchy level |
| Animation easing | Duration per interaction type |

---

## 2. Visual Design Rules

### 2.1 Color Usage

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  BACKGROUNDS       SURFACES        ACCENTS              │
│  ───────────       ────────        ───────              │
│  #050816           #0F172A        #3B82F6 (primary)    │
│  (Void)            (Surface)      #8B5CF6 (secondary)  │
│                    #1E293B        #00F5FF (signature)  │
│                    (Elevated)                           │
│                                                         │
│  TEXT                              SEMANTIC              │
│  ────                              ────────              │
│  #F1F5F9 (primary)                 #22C55E (success)    │
│  #94A3B8 (secondary)              #F59E0B (warning)    │
│  #8E9CAE (muted)                  #EF4444 (error)      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Rules:**
- Max **3 colors** visible in any single viewport
- Accent color used sparingly — CTAs, links, active states only
- Gradients only for hero sections and special elements, never body content
- Use opacity variations over new color values: `rgba(99, 102, 241, 0.1)` > `#1a1a2e`

### 2.2 Typography Hierarchy

```
Display     ── Space Grotesk 700  ── 48-72px  ── Hero headlines only
H1          ── Space Grotesk 700  ── 36-48px  ── Page titles
H2          ── Space Grotesk 600  ── 28-32px  ── Section headings
H3          ── Inter 600          ── 20-24px  ── Subsection headings
Body        ── Inter 400          ── 16-18px  ── Paragraph text
Body Small  ── Inter 400          ── 14px     ── Metadata, captions
Caption     ── Inter 500          ── 12-13px  ── Labels, badges
Code        ── JetBrains Mono 400 ── 14-15px  ── Code blocks, inline code
```

**Rules:**
- Maximum **3 font sizes** per section
- Line height: 1.5 for body, 1.2 for headings, 1.6 for long-form reading
- Letter spacing: `-0.02em` for headings, `0` for body, `0.05em` for labels
- Never use `font-weight: 300` — thin weights disappear on dark backgrounds

### 2.3 Spacing System

Base unit: **4px**

```
4   ── Inline padding (icon gap, tag padding)
8   ── Tight spacing (between related elements)
12  ── Component internal padding
16  ── Standard gap (between cards, form fields)
24  ── Section internal padding
32  ── Between related sections
48  ── Between major sections
64  ── Page section spacing
96  ── Hero section padding
128 ── Maximum breathing room
```

**Rules:**
- Never use arbitrary spacing values (no `13px`, `37px`, etc.)
- Padding inside components: always `12px` or `16px`
- Gap between cards: always `16px` or `24px`
- Section margins: always `48px` or `64px`

### 2.4 Border Radius

```
4px  ── Inline elements (tags, badges, code blocks)
8px  ── Cards, inputs, buttons
12px ── Modals, tooltips, dropdowns
16px ── Large feature cards, hero elements
9999px ── Pills, avatar circles
```

### 2.5 Shadows & Depth

Dark mode uses layered surfaces instead of heavy shadows:

| Layer | Background | Shadow | Use |
|---|---|---|---|
| **Base** | `#0A0A0F` | None | Page background |
| **Surface** | `#1E1E2E` | `0 1px 2px rgba(0,0,0,0.3)` | Cards, sections |
| **Elevated** | `#2A2A3E` | `0 4px 12px rgba(0,0,0,0.4)` | Hover states, modals |
| **Floating** | `#353550` | `0 8px 24px rgba(0,0,0,0.5)` | Tooltips, dropdowns |

---

## 3. Animation Principles

### 3.1 Timing

| Type | Duration | Easing |
|---|---|---|
| Micro (hover, focus) | 150ms | `ease-out` |
| Small (expand, collapse) | 200ms | `ease-in-out` |
| Medium (page section reveal) | 300–400ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Large (page transition) | 400–500ms | `cubic-bezier(0.22, 1, 0.36, 1)` |

### 3.2 Rules

1. **Animations enhance meaning** — every motion communicates something (entry, relationship, state change)
2. **Never animate for decoration** — if it doesn't serve UX, it's noise
3. **Respect reduced motion** — always wrap in `@media (prefers-reduced-motion: no-preference)`
4. **Stagger, don't cascade** — group animations with 50–100ms offsets
5. **Enter from below** — content enters viewport with `translateY(20px)` → `translateY(0)`
6. **Exit by fading** — removed content fades out (don't slide away)

### 3.3 CSS Custom Properties

```css
:root {
  --duration-instant: 0ms;
  --duration-micro: 150ms;
  --duration-small: 200ms;
  --duration-medium: 350ms;
  --duration-large: 500ms;

  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 4. Accessibility Standards

| Requirement | Target | Check |
|---|---|---|
| Color contrast (text) | ≥ 4.5:1 (AA) | All text on all backgrounds |
| Color contrast (large text) | ≥ 3:1 (AA) | Headlines, buttons |
| Keyboard navigation | Full | All interactive elements focusable, logical tab order |
| Focus indicators | Visible | `outline: 2px solid #6366F1` with `outline-offset: 2px` |
| Screen reader | Semantic HTML | Proper headings, ARIA labels, alt text |
| Reduced motion | Supported | `prefers-reduced-motion` disables all animations |
| Touch targets | ≥ 44×44px | Buttons, links, form elements on mobile |
| Language | Declared | `<html lang="en">` |
| Skip nav | Present | "Skip to main content" link |

---

## 5. Responsive Design Philosophy

### 5.1 Approach: Mobile-First

Start with the smallest viewport and add complexity as space allows.

```
Mobile (< 640px)
├── Single column
├── Stacked cards
├── Hamburger nav
├── Full-width buttons
└── Simplified visuals

Tablet (640–1023px)
├── 2-column grids
├── Condensed nav (fewer items)
├── Side-by-side layouts
└── Increased padding

Desktop (1024–1279px)
├── Full navigation
├── 3-column grids
├── Sidebar TOC (blog)
└── Hover interactions

Wide (≥ 1280px)
├── Max-width container (1280px)
├── Generous whitespace
├── Full visual richness
└── All interactive patterns
```

### 5.2 What Changes, What Doesn't

| **Stays Constant** | **Adapts** |
|---|---|
| Color palette | Column count |
| Typography scale | Padding (tighter on mobile) |
| Border radius | Navigation pattern |
| Brand voice | Content density |
| Animation timing | Image sizes |

---

## 6. Component Design Rules

### 6.1 Buttons

```
Primary:   Gradient background (#6366F1 → #8B5CF6), white text, 8px radius
Secondary: Transparent background, indigo border, indigo text, 8px radius
Ghost:     Transparent, no border, accent text, hover: subtle background
Icon-only: 40×40px, centered icon, rounded (8px), hover: background fill
```

### 6.2 Cards

```
Default:   #1E1E2E bg, 8px radius, 1px border rgba(255,255,255,0.06)
Hover:     border → rgba(99,102,241,0.3), subtle box-shadow, scale(1.01)
Active:    border → #6366F1 solid, background lighten slightly
```

### 6.3 Inputs

```
Default:   #1E1E2E bg, 1px border rgba(255,255,255,0.1), 8px radius
Focus:     border → #6366F1, ring → rgba(99,102,241,0.2) 3px
Error:     border → #EF4444, helper text in red below
Filled:    text → #FAFAFA, label floats above (if using float labels)
```

### 6.4 Code Blocks

```
Background:  #0D0D14 (darker than card)
Border:      1px solid rgba(255,255,255,0.06)
Radius:      8px
Font:        JetBrains Mono, 14px
Line height: 1.7
Features:    Language label (top-right), Copy button (top-right, on hover)
             Line numbers (muted), Syntax highlighting (VS Code Dark+)
```

---

## 7. Design Anti-Patterns (Don't Do This)

| ❌ Anti-Pattern | ✅ Instead |
|---|---|
| Rainbow gradient text everywhere | Gradient text for hero headline only |
| Harsh white `#FFFFFF` text on dark | Soft white `#FAFAFA` or `#E2E8F0` |
| Borders on everything | Use surface color contrast for separation |
| Animations on every element | Animate section entries and interactions only |
| Centered text blocks for body content | Left-align body text, center only headlines |
| Tiny light-gray text on dark backgrounds | Min 14px, min 4.5:1 contrast |
| Generic stock icons | Consistent icon set (Lucide) throughout |
| Infinite scroll on blog | Paginate or "Load More" button |
| Auto-playing video | Click-to-play with clear thumbnail |
| Modal popups for newsletter | Inline CTA or end-of-content CTA |

---

## 8. Design Tokens (CSS Custom Properties)

```css
:root {
  /* Colors */
  --color-bg-base: #050816;
  --color-bg-surface: #0F172A;
  --color-bg-elevated: #1E293B;
  --color-bg-floating: #334155;

  --color-text-primary: #F1F5F9;
  --color-text-secondary: #94A3B8;
  --color-text-muted: #8E9CAE;

  --color-accent-primary: #3B82F6;
  --color-accent-secondary: #8B5CF6;
  --color-accent-tertiary: #00F5FF;

  --color-success: #22C55E;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;

  --color-border: rgba(255, 255, 255, 0.06);
  --color-border-hover: rgba(59, 130, 246, 0.3);
  --color-border-active: #3B82F6;

  /* Typography */
  --font-display: 'Space Grotesk', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;
  --space-24: 96px;
  --space-32: 128px;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.5);

  /* Animation */
  --duration-micro: 150ms;
  --duration-small: 200ms;
  --duration-medium: 350ms;
  --duration-large: 500ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.22, 1, 0.36, 1);
}
```

---

*Last updated: 2026-07-04*

# Component Architecture Spec (03_COMPONENT_ARCHITECTURE.md)

This document details the hierarchy, categorizations, and design patterns utilized to organize visual components on the **BuildWithPNJ** platform. The platform adheres to **Atomic Design** principles to guarantee modularity and reusability.

---

## 1. Atomic Design Taxonomy

Components are organized into five strict structural classes:

```
┌────────────────────────────────────────────────────────────────────────┐
│                                 PAGES                                  │
│  (Next.js route templates, aggregates layouts and fills with data)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                               TEMPLATES                                │
│   (Structural layouts defining grid areas, sidebars, headers, footers) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                               ORGANISMS                                │
│   (Dense, self-contained functional widgets: Command Palette, heatmaps)│
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                               MOLECULES                                │
│  (Simple group of atoms: Search input groups, breadcrumbs, tags list)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                                 ATOMS                                  │
│  (Base design primitives: Buttons, input fields, badges, icons, spans) │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Hierarchy Class Mappings

### 1. Atoms (Base UI Primitives)
Located under `apps/web/src/components/ui/`. These components are highly modular, styling-focused, and have zero dependency on business logic:
- **`Button`**: Custom variants (primary, secondary, pixel-accent, border-glow).
- **`Input`**: Text entries, checkboxes.
- **`Badge`**: Status pills, category text wrappers.
- **`GlowCircle`**: Ambient mesh glows.

### 2. Molecules (Assembled Elements)
Located under `apps/web/src/components/` and `src/components/ui/`:
- **`SearchField`**: Combines Lucide `Search` icon with input tag.
- **`ArticleCard`**: Integrates article metadata, tagline, and tag list.
- **`TelemetryMetric`**: Displays a metric label, value, and change rate.
- **`TimelineItem`**: Timeline node combining date badge with description text.

### 3. Organisms (Functional Sections)
Complex layout assemblies managing internal state or external events:
- **`PublicHeader`**: Coordinates logo wordmarks, navigation lists, hamburger menus, and desktop search triggers.
- **`PublicFooter`**: Column list navigation layouts and system clock ticks.
- **`PublicCommandPalette`**: Dialog overlay managing keyboard listeners, search inputs, navigation chords.
- **`GitHubHeatmap`**: Grid interface generating and scaling active contribution square blocks.
- **`LabsList`**: Coordinates list searches and category filters.

### 4. Templates (Shell Layouts)
Structural wrappers specifying content alignments:
- **`PublicLayout`**: Outer container wrapping background meshes, navigation bars, main slots, footers, and Command Palettes.
- **`AppLayout`**: Sidebar navigation template with secondary panel slots for dashboard pages.
- **`ProseLayout`**: Double-column template positioning sticky TOC panels next to compile-content cards.

### 5. Pages (Route Leaf Components)
Root route nodes fetching data and populating layouts:
- **`PublicHomePage`**: Hydrates hero slots, projects previews, telemetry grids, and news CTA layouts.
- **`JournalDetailPage`**: Resolves slugs, compiles markdown to HTML, extracts headings for the TOC sidebar, and renders related posts.

---

## 3. Data Isolation Principle

- **Server-First Execution**: Prerender static HTML inside Server Components. Pass plain objects as properties to Client Components.
- **Interactive Boundaries**: Keep event handlers (`onClick`, `onChange`, `onSubmit`) inside Client Components. Define client boundaries (`'use client'`) at the highest interactive node (e.g. `<NewsletterForm />`), leaving parents fully static.

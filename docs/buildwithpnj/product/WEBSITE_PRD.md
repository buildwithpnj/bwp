# BuildWithPNJ — Website PRD

> Product Requirements Document for the official BuildWithPNJ brand website.

---

## 1. Overview

### 1.1 Purpose

Build a public-facing website at **buildwithpnj.com** that serves as the digital headquarters of the BuildWithPNJ AI engineering brand. The site will showcase projects, publish technical content, and establish credibility as a builder in the AI space.

### 1.2 Goals

| Priority | Goal |
|---|---|
| **P0** | Establish professional online presence |
| **P0** | Showcase projects and technical skills |
| **P1** | Publish blog content (AI engineering, build-in-public) |
| **P1** | Drive GitHub and social media engagement |
| **P2** | Generate inbound leads (consulting, freelance, collaborations) |
| **P2** | Email list / newsletter subscriber growth |

### 1.3 Target Audience

| Audience | What They Want |
|---|---|
| **Hiring managers / Recruiters** | Portfolio, tech depth, shipping track record |
| **Fellow developers** | Technical content, open-source projects, tutorials |
| **Potential clients** | Proof of expertise, services offered, contact |
| **AI / Tech community** | Hot takes, insights, build-in-public updates |

---

## 2. Sitemap & Pages

```
buildwithpnj.com/
├── /                    ← Hero landing page
├── /projects            ← Project showcase gallery
├── /projects/[slug]     ← Individual project deep-dive
├── /blog                ← Blog listing page
├── /blog/[slug]         ← Individual blog post
├── /about               ← Personal story, skills, journey
├── /contact             ← Contact form + social links
└── /newsletter          ← Newsletter signup (optional standalone)
```

---

## 3. Page Requirements

### 3.1 Home — `/`

The hero page. First impression matters. Must be visually stunning and immediately communicate who PNJ is and what he builds.

**Sections:**

| Section | Content |
|---|---|
| **Hero** | Name, tagline, animated background (particles / gradient mesh), primary CTA ("View Projects" / "Read Blog") |
| **About Snippet** | 2-3 sentence intro + profile photo → links to `/about` |
| **Featured Projects** | 3 project cards with thumbnail, title, tech stack badges, brief description → links to `/projects/[slug]` |
| **Latest Posts** | 3 most recent blog post cards → links to `/blog` |
| **Tech Stack** | Visual grid of technologies used (icons + labels) |
| **Social Proof** | GitHub stats, project metrics, testimonials (when available) |
| **CTA Footer** | Newsletter signup + social links |

**Design notes:**
- Dark theme by default (matches brand guidelines)
- Smooth scroll animations (intersection observer-based)
- Glassmorphism cards with subtle hover effects
- Gradient text for headlines
- Responsive: mobile-first, breakpoints at 640, 768, 1024, 1280px

---

### 3.2 Projects — `/projects`

Gallery showcase of all BuildWithPNJ projects.

**Requirements:**
- Grid layout of project cards (responsive: 1 → 2 → 3 columns)
- Each card: thumbnail/screenshot, title, description, tech stack badges, links (live demo, GitHub)
- Filter by tech stack or category (optional v2)
- Featured project pinned at top

**Individual Project Page — `/projects/[slug]`:**

| Section | Content |
|---|---|
| **Header** | Project name, tagline, status badge (Active / Complete / Archived) |
| **Screenshots** | Image carousel or gallery |
| **Overview** | What it is, why I built it, who it's for |
| **Tech Stack** | Detailed technology breakdown with rationale |
| **Architecture** | System diagram (optional) |
| **Key Features** | Feature list with descriptions |
| **Learnings** | What I learned building it |
| **Links** | Live demo, GitHub repo, blog posts about it |

---

### 3.3 Blog — `/blog`

Technical blog focused on AI engineering and building in public.

**Listing page:**
- Reverse-chronological post list
- Each card: title, date, reading time, excerpt, tags
- Tag filter (e.g., `AI`, `Next.js`, `FastAPI`, `build-in-public`)
- Search (optional v2)

**Individual Post — `/blog/[slug]`:**
- MDX-rendered content with syntax highlighting
- Table of contents (auto-generated from headings)
- Reading time estimate
- Author card
- Share buttons (Twitter, LinkedIn, copy link)
- Related posts
- Newsletter CTA at bottom

---

### 3.4 About — `/about`

Personal story and professional background.

**Sections:**
- Profile photo + intro
- Journey / origin story (how I got into AI engineering)
- Skills & expertise (visual skill grid)
- Tools & technologies I use daily
- Values & philosophy (builder mindset, AI-first thinking)
- Timeline of key milestones (optional)
- Links to social profiles

---

### 3.5 Contact — `/contact`

Simple contact page.

- Contact form (name, email, subject, message)
- Social links (GitHub, Twitter/X, LinkedIn, email)
- Availability status ("Open to freelance" / "Hiring" / "Collaborations welcome")
- Optional: Calendly embed for booking calls

---

## 4. Technical Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Framework** | Next.js 15 (App Router) | SSG + SSR, great DX, matches existing expertise |
| **Styling** | Tailwind CSS + custom CSS | Rapid iteration, dark mode built-in |
| **Content** | MDX (local files or headless CMS) | Blog posts with embedded components |
| **Deployment** | Vercel | Zero-config, preview deployments, analytics |
| **Domain** | `buildwithpnj.com` | Custom domain via Vercel |
| **Analytics** | Vercel Analytics + Plausible (privacy-first) | Track visitors without cookies |
| **Forms** | Resend or Formspree | Contact form email delivery |
| **SEO** | next-sitemap, structured data (JSON-LD) | Organic search visibility |

---

## 5. Design Specifications

### 5.1 Theme

Follows [BRAND_GUIDELINES.md](file:///c:/Users/praka/OneDrive/Documents/My%20dashboard/my%20brand%20PNJ/BRAND_GUIDELINES.md):

- **Primary mode:** Dark
- **Accent colors:** Electric Indigo (#6366F1) → Neon Violet (#8B5CF6) → Cyan Pulse (#06B6D4)
- **Typography:** Space Grotesk (headings), Inter (body), JetBrains Mono (code)
- **Aesthetic:** Glassmorphism, gradient accents, smooth micro-animations

### 5.2 Animations

| Element | Animation |
|---|---|
| Page load | Staggered fade-in from bottom |
| Scroll | Section reveal on intersection |
| Cards | Scale + glow on hover |
| Hero background | Animated gradient mesh or particles |
| Page transitions | Smooth crossfade |
| Code blocks | Syntax highlighting with line focus |

### 5.3 Performance Targets

| Metric | Target |
|---|---|
| Lighthouse Performance | > 95 |
| First Contentful Paint | < 1.2s |
| Largest Contentful Paint | < 2.5s |
| Cumulative Layout Shift | < 0.1 |
| Total Blocking Time | < 200ms |

---

## 6. SEO Requirements

| Item | Implementation |
|---|---|
| **Title tags** | Unique per page, format: `{Page} — BuildWithPNJ` |
| **Meta descriptions** | Hand-written for static pages, auto-generated excerpt for blog |
| **Open Graph** | Image, title, description for social sharing |
| **Twitter Cards** | `summary_large_image` for blog posts |
| **Canonical URLs** | Self-referencing on each page |
| **Sitemap** | Auto-generated XML sitemap via `next-sitemap` |
| **Robots.txt** | Allow all, point to sitemap |
| **Structured data** | JSON-LD: Person (about), BlogPosting (blog), WebSite (home) |

---

## 7. Content Strategy

### 7.1 Blog Content Categories

| Category | Topics |
|---|---|
| **Build in Public** | Progress updates, what I shipped, revenue/metrics transparency |
| **AI Engineering** | Tutorials, RAG pipelines, multi-agent systems, prompt engineering |
| **Full-Stack Dev** | Next.js, FastAPI, system design, database patterns |
| **Tools & Reviews** | Developer tool reviews, stack recommendations |
| **Reflections** | Career lessons, productivity, builder mindset |

### 7.2 Publishing Cadence

- **Target:** 1–2 blog posts per week
- **Sources:** Migrate from `content/blog/` directory
- **Cross-post to:** Dev.to, Hashnode, LinkedIn articles

---

## 8. MVP Scope (v1)

### In Scope (v1)

- [x] Home page with hero, featured projects, latest posts
- [x] Projects listing + individual project pages (2–3 projects)
- [x] Blog with MDX support (3–5 initial posts)
- [x] About page
- [x] Contact page with working form
- [x] Responsive design (mobile + desktop)
- [x] Dark mode (primary)
- [x] SEO fundamentals (meta tags, sitemap, structured data)
- [x] Vercel deployment

### Out of Scope (v2+)

- [ ] Light mode toggle
- [ ] Newsletter with email automation
- [ ] Blog search / advanced filtering
- [ ] Comments system (Giscus or similar)
- [ ] Project filtering by tech stack
- [ ] Testimonials section
- [ ] RSS feed
- [ ] i18n
- [ ] A/B testing

---

## 9. Success Metrics

| Metric | Target (3 months post-launch) |
|---|---|
| Monthly unique visitors | 500+ |
| Blog post page views | 100+ per post |
| GitHub profile clicks from site | 50+ / month |
| Newsletter signups | 100+ |
| Contact form submissions | 5+ / month |
| Avg. time on site | > 2 minutes |

---

## 10. Timeline

| Milestone | Target Date |
|---|---|
| Design mockups / wireframes | Jul 2026 |
| Homepage + About built | Aug 2026 |
| Blog system + 3 initial posts | Aug 2026 |
| Projects showcase | Aug 2026 |
| Contact page + forms | Sep 2026 |
| SEO + performance pass | Sep 2026 |
| Public launch at buildwithpnj.com | Sep 2026 |

---

*Last updated: 2026-07-04*

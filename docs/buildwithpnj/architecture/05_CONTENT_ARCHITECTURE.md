# Content Architecture Spec (05_CONTENT_ARCHITECTURE.md)

This document describes the schema structure, validation metrics, and SEO metadata mappings for the static markdown-based Content Management System (CMS) of **BuildWithPNJ**.

---

## 1. Content Modeling Schema

Content is divided into three primary collections under the root `content/` folder:

### 1. Projects Showcase (`content/case-studies/*.md`)
```yaml
---
slug: "personal-os"
title: "Personal Operating System"
tagline: "Local-first dashboard orchestrating finances, habits, notes, and local AI tools."
startDate: "2026-03-12"
publishDate: "2026-07-04"
status: "active" # active, complete, archive
category: "SaaS"
githubUrl: "https://github.com/buildwithpnj/personal-os"
liveUrl: "https://personalos.com"
techStack: ["Next.js", "FastAPI", "PostgreSQL", "Tailwind"]
timeline:
  - "March 2026: Architecting double-entry ledger database tables"
  - "May 2026: Released local vector notes container"
challenges:
  - title: "Concurrency in ledger entries"
    content: "Solved using serializable PostgreSQL transactions to prevent credit/debit double-allocations."
---
[Markdown body contents]
```

### 2. Engineering Journal (`content/blog/*.md`)
```yaml
---
slug: "building-personal-os-from-scratch"
title: "Building Personal OS from Scratch"
publishDate: "2026-07-04"
readingTime: 6 # minutes
excerpt: "A deep architectural review of building an isolated dashboard monorepo with database safeguards."
tags: ["ai", "architecture", "nextjs", "fastapi"]
author: "Prakash Nayak Joshi"
---
[Markdown body contents]
```

### 3. R&D Labs Experiments (`content/experiments/*.md`)
```yaml
---
id: "EXP-001"
slug: "multi-agent-code-reviewer"
title: "Multi-Agent Code Reviewer"
tagline: "Evaluating consensus consensus protocols across language models to minimize code validation logic errors."
publishDate: "2026-07-04"
category: "AI Agent Networks"
status: "live" # live, wip, draft
hypothesis: "Utilizing multiple agent consensus steps reduces false positive syntax flags by 28% compared to single-shot completions."
tags: ["langgraph", "llms", "consensus"]
githubUrl: "https://github.com/buildwithpnj/reviewer-agent"
---
[Markdown body contents]
```

---

## 2. Content Relationships & Tagging

To create cohesive link clusters and improve developer discoverability:
- **Shared Tags**: Direct relation between blog tags and lab project tags. For example, an article on `#fastapi` link-recommends labs evaluating `#fastapi` websocket connections.
- **Reference Slugs**: Detail pages can refer to other slugs in their frontmatter to generate "Related Content" lists automatically.

---

## 3. SEO & Metadata Integration

Every content page dynamically generates metadata properties during Next.js static builds:
- **Canonical URLs**: Built using the post's slug: `https://buildwithpnj.com/journal/${post.slug}`.
- **OpenGraph & Twitter Cards**:
  - `og:type`: "article" for journal logs, "website" for hubs.
  - `og:image`: Dynamically generated using a Vercel OG image generator template showing title, tags, and pixel glows.
- **Structured Data (JSON-LD)**: Renders `Article` schemas for search crawlers to improve visibility.

---

## 4. RSS Feed Aggregation

The system automatically generates a dynamic XML RSS feed at `/feed.xml` on every build:
- Scans `content/blog/` for active posts.
- Sorts posts in reverse chronological order.
- Generates standard RSS XML blocks detailing titles, publication dates, excerpts, and links.

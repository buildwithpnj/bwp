---
title: "Monorepo Documentation CMS"
tagline: "A static content engine parsing markdown frontmatter metadata and compiling it to static page paths."
status: "complete"
featured: true
thumbnail: "/images/projects/docs-cms.png"
techStack: ["nextjs", "typescript", "markdown"]
category: "tool"
startDate: "2026-06-15"
publishDate: "2026-07-05"
timeline: ["Sprint 1: Markdown filesystem parsing utility", "Sprint 2: Frontmatter schema validator", "Sprint 3: Dynamic routes compilation tests"]
challenges: 
  - title: "Compiler performance limitations"
    content: "Parsing large numbers of MDX files during hot-reloads increased dev server compilation times. We mitigated this by setting up a lightweight file cache."
---

## Problem
Maintaining technical documentation in external CMS platforms often leads to documentation drift as code evolves.

## Solution
We built a file-based CMS that reads markdown files directly from the repository. This structure allows engineers to update code and documentation in a single commit, preventing documentation drift.

## Architecture

```
  Markdown Content Source (content/)
                 │
                 ▼
  Next.js Build compiler (gray-matter & marked)
                 │
                 ▼
  Static HTML Pages (ISR / SSG)
```

## Technical Decisions
- **gray-matter**: Used to parse metadata tags from markdown headers.
- **marked**: Compiles markdown body content to standard HTML elements.
- **Incremental Static Regeneration (ISR)**: Pre-renders pages at build time and updates them dynamically as content changes.

## Results
- Build times decreased by **40%** compared to heavy headless CMS configurations.
- Documentation updates are made directly in commits, ensuring they stay in sync with code changes.

## Future Roadmap
- MDX support for embedding interactive UI components in documentation.
- Automated dead-link checking in PR pipelines.

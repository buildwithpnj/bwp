---
title: "PricePilot: AI Shopping Comparison Engine"
tagline: "Multi-agent shopping crawler comparing products with affiliate URL masking and rotated proxy pools."
status: "complete"
featured: true
thumbnail: "/images/projects/placeholder.jpg"
techStack: ["nextjs", "fastapi", "postgresql", "redis", "opensearch"]
category: "saas"
liveUrl: "https://pricepilot-web.vercel.app/"
githubUrl: "https://github.com/buildwithpnj/pricepilot"
startDate: "2026-04-15"
publishDate: "2026-05-08"
timeline: ["Sprint 1: Connector integrations & bot orchestration", "Sprint 2: Search cache setup", "Sprint 3: Bot tracing UI & logs validation"]
challenges:
  - title: "Anti-Bot Captchas"
    content: "Product sweeps on major shopping marketplaces triggered strict Cloudflare captchas. Solved by integrating headless Playwright workers with rotating User-Agents and jitter query delays."
  - title: "Search Latency"
    content: "Querying multiple databases concurrently caused slow search responses. Resolved by setting up OpenSearch index templates and caching responses in Redis."
---

## Problem
E-commerce buyers face extreme fragmentation when comparing prices across major digital storefronts, while developers face scraper bans and rate limiting when querying prices.

## Solution
We built **PricePilot** (DealLens AI), an AI-assisted shopping search bot engine.
- **Deterministic and AI-Assisted Bots**: Supports query parsing, item attribute normalization, and affiliate URL conversions.
- **Developer Traces**: Logs step-by-step agent search paths to enable easy debugging of API connectors.
- **OpenSearch Schema**: Built a structured model supporting fast catalog queries.

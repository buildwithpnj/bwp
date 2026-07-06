---
title: "Cockroach Watch India: Civic Commentary OS"
tagline: "Civic watch, commentary, and news aggregation platform integrating Claude, Llama, and Mistral model routers."
status: "active"
featured: true
thumbnail: "/images/projects/placeholder.jpg"
techStack: ["nextjs", "postgresql", "supabase", "aws-bedrock", "tailwindcss"]
category: "saas"
liveUrl: "https://cockroachwatchindia.online/"
githubUrl: "https://github.com/buildwithpnj/CWI"
startDate: "2026-05-15"
publishDate: "2026-06-05"
timeline: ["Sprint 1: Supabase RLS configuration & RSS parsers", "Sprint 2: AWS Bedrock LLM routing framework", "Sprint 3: Newsroom audit & SEO optimizations"]
challenges:
  - title: "Link Rot and UI Noise"
    content: "Duplicate news channels and dead links made the live newsroom cluttered. Conducted a codebase audit to consolidate headers, redirects, and move links to structured JSON lists."
  - title: "Model Token Costs"
    content: "Running heavy summarization agents daily on AWS Bedrock led to high API overheads. Resolved by dividing tasks into Command Core (Claude) and lighter template routing pipelines."
---

## Problem
Aggregating civic issues, NEET exams updates, and political satire across multiple social API feeds is highly expensive and prone to API rate limits, while maintaining editorial quality requires extensive human validation.

## Solution
We built **Cockroach Watch India (CWI)**, a civic platform operated by an intelligent admin dashboard (CWI AI OS):
- **Approval-First Queue**: Agents prepare drafts, SEO schema, and social graphics in a pending database. Public updates require explicit administrator approvals.
- **Model Router Engine**: Commits API requests dynamically to different providers based on complexity (AWS Bedrock Claude/Llama/Mistral, OpenAI API, or template logic).
- **Consolidated Live Newsroom**: Aggregates breaking topics into a single timeline feed with permanente redirects and JSON-defined linkages to prevent links rot.

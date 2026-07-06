---
title: "Enersave: Industrial Energy Optimization"
tagline: "An industrial audit-log dashboard with gzipped response compression and Prisma connection pooling."
status: "complete"
featured: true
thumbnail: "/images/projects/placeholder.jpg"
techStack: ["nextjs", "express", "prisma", "postgresql", "typescript"]
category: "saas"
liveUrl: "https://enersavev66.vercel.app/"
githubUrl: "https://github.com/callmepnj/Enersavev2"
startDate: "2026-03-10"
publishDate: "2026-04-18"
timeline: ["Sprint 1: Schema design & Prisma setup", "Sprint 2: Memory uploads & compression integrations", "Sprint 3: Graceful shutdown & log rotation systems"]
challenges:
  - title: "Server Connection Pool Crashes"
    content: "Unrestricted database queries under load spawned unlimited PostgreSQL connections, crashing the app. Fixed by capping Prisma pool at 20-50 and setting up a clean SIGTERM connection teardown process."
  - title: "Memory leaks on file uploads"
    content: "Reading product spreadsheet uploads into standard memory buffers caused major memory spikes. Fixed by implementing disk-based multer storage buffers."
---

## Problem
Industrial energy audits generate massive quantities of logs and metrics, which quickly lead to slow dashboard queries, memory exhaustion on files upload, and unbounded server logs.

## Solution
We optimized Enersave's codebase by implementing:
- **Graceful Shutdowns**: Handled SIGTERM/SIGINT with a 30s timeout window.
- **Log Rotation**: Capped files with Winston-daily-rotate to prevent filling server disk spaces.
- **Response Compression**: Added Gzip compression middleware resulting in an 80% decrease in transfer sizes.
- **SQL raw optimizations**: Eliminated database N+1 queries.

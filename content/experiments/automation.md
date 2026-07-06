---
id: "EXP-05"
title: "Event-Driven Background Task Workers"
tagline: "Measuring task latency and resource usage using Celery and Redis workflows."
status: "completed"
category: "Automation"
tags: ["celery", "redis", "python"]
hypothesis: "Moving notes synchronization to event-driven workers reduces average request response times to under 10ms."
publishDate: "2026-07-05"
---

## Objective
To improve dashboard responsiveness by moving API synchronization tasks to background workers.

## Methodology
- Trigger synchronization tasks in the background using Celery and Redis.
- Measure request response times under varying load.

## Findings
- Background processing reduced average response times from 1.5 seconds to **8ms**, freeing up backend threads to handle incoming requests.

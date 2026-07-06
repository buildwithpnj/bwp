---
id: "EXP-04"
title: "System Instruction Context Caching"
tagline: "Evaluating model delays and token usage using prompt compilation cache controls."
status: "live"
category: "Prompt Engineering"
tags: ["ai", "prompting", "performance"]
hypothesis: "Utilizing prompt caching on supported APIs reduces response times for long system prompts by 50%."
publishDate: "2026-07-04"
---

## Objective
To reduce response times for agent tasks that use large system prompts.

## Methodology
- Set up tests with a 2,000-token system prompt.
- Run queries with and without prompt caching enabled.
- Measure token processing times and overall latency.

## Findings
- Prompt caching reduced initial response times from 1.2 seconds to **450ms**, while cutting input token costs by **60%**.

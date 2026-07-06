---
id: "EXP-01"
title: "Self-Correcting Compiler Agents"
tagline: "Testing LLM agent feedback loops for automated syntax fixes during compiler tasks."
status: "live"
category: "AI Agents"
tags: ["agents", "python", "automation"]
hypothesis: "Providing real-time compiler stdout and stack traces to an LLM loop resolves 90% of basic syntax regressions."
publishDate: "2026-07-01"
---

## Objective
To build an event-driven compiler checker that watches file changes and uses an LLM agent to automatically fix formatting and type errors.

## Methodology
- Watch file changes using `watchfiles` in Python.
- Parse error outputs from compiler tools.
- Send the code and the error trace to a local LLM agent to generate corrections.
- Apply the code changes and re-run the compiler to verify the fix.

## Findings
- Syntax issues (missing brackets, typos) were resolved successfully.
- Logic errors require additional context maps to resolve.

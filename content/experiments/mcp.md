---
id: "EXP-06"
title: "Model Context Protocol for Document Auditing"
tagline: "Evaluating code conformance checks using local TypeScript MCP server tools."
status: "live"
category: "MCP"
tags: ["mcp", "typescript", "lint"]
hypothesis: "Exposing file conformance checks to LLM agents via MCP tools reduces formatting regressions in pull requests."
publishDate: "2026-07-06"
---

## Objective
To build a custom MCP server that checks documentation and code conformance during PR reviews.

## Methodology
- Write a TypeScript MCP server with tool configurations for file checks.
- Set up an agent workflow to query files and report formatting deviations.

## Findings
- The agent successfully identified non-conforming paths and suggested formatting fixes directly in PR reviews.

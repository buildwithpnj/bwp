---
title: "Agentix: Multi-Agent Code Analyzer"
tagline: "A multi-agent AI system for automated code analysis, security auditing, and intelligent reporting."
status: "complete"
featured: true
thumbnail: "/images/projects/placeholder.jpg"
techStack: ["fastapi", "streamlit", "python", "langchain"]
category: "open-source"
githubUrl: "https://github.com/buildwithpnj/Agentix-Code-Analyzer"
startDate: "2026-03-10"
publishDate: "2026-04-13"
timeline: ["Sprint 1: Multi-agent framework setup", "Sprint 2: Streamlit UI & FastAPI backend integration", "Sprint 3: Security vulnerability scanner testing"]
challenges:
  - title: "Agent Coordination Latency"
    content: "Chaining sequential LLM agents for security audits, docstring generation, and type checking led to cumulative latencies over 12s. We resolved this by running dependency audits asynchronously."
---

## Problem
Manual code reviews and security audits are slow, error-prone, and bottleneck rapid delivery cycles in collaborative dev teams.

## Solution
We built **Agentix-Code-Analyzer**, a multi-agent system that delegates specialized review phases (security, syntax, formatting, and documentation) to autonomous AI agents that run in parallel and compile a unified report.

## Tech Stack
- **FastAPI**: Backend REST endpoint framework.
- **Streamlit**: Fast, reactive dashboard interface.
- **LangChain / LangGraph**: Orchestrates prompt-state flows and agent handoffs.

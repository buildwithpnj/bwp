# Documentation Guide Spec (21_DOCUMENTATION_GUIDE.md)

This document describes the style rules, layout templates, and Architectural Decision Record (ADR) formats required when writing documentation for the **BuildWithPNJ** platform.

---

## 1. Documentation Principles

- **Human-First Clarity**: Keep sentences short, avoid verbose descriptions, and prioritize concrete code examples over abstract theory.
- **Markdown Standards**: Use GitHub Flavored Markdown (GFM). Always use proper heading structures (`#` through `######`) to allow automated parsers to generate directories.
- **Clickable Links**: All file or component references inside documentation must use clickable Markdown links with the `file:///` scheme (e.g. `[public-header.tsx](file:///absolute/path/to/file)`).

---

## 2. Architectural Decision Record (ADR) Format

To track significant architectural decisions, engineers must author an ADR file under `docs/adr/` using this template:

```markdown
# ADR-001: [Brief Title of Decision]

- **Status**: [Proposed | Accepted | Deprecated | Superseded]
- **Date**: YYYY-MM-DD
- **Author**: [Name]

## 1. Context & Problem Statement
Describe the problem we are solving, the technical constraints, and why a decision is necessary.

## 2. Considered Options
List alternative designs, frameworks, or databases evaluated.

## 3. Decision Outcome
Specify the chosen option, technical rationales, and architectural trade-offs.

## 4. Consequences
Describe the impact on developers, performance budgets, and future system scalability.
```

---

## 3. API Documentation Standards

API routes in backend code must generate standard OpenAPI metadata:
- **FastAPI Metadata**: Every router endpoint must define a `summary`, `description`, and explicit `response_model` class to automate swagger dashboard updates:
  ```python
  @router.get(
      "/telemetry",
      response_model=TelemetryResponse,
      summary="Get system telemetry metrics",
      description="Aggregates GitHub commits, streak counters, and AI model loads."
  )
  def read_telemetry():
      return service.get_metrics()
  ```
- **Docstrings**: Provide brief inline comments mapping request and response fields.

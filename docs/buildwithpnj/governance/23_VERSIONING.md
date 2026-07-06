# Versioning Spec (23_VERSIONING.md)

This document describes the Semantic Versioning (SemVer) structure, API deprecation cycles, and breaking change rules enforced across the **BuildWithPNJ** codebase.

---

## 1. Semantic Versioning Model

All modules, packages, and services adhere to SemVer formatting:

`MAJOR.MINOR.PATCH`

- **MAJOR**: Incremented when introducing incompatible API changes or breaking updates.
- **MINOR**: Incremented when introducing backward-compatible new features.
- **PATCH**: Incremented when introducing backward-compatible bugfixes or telemetry patches.

---

## 2. Breaking Changes & Deprecation Cycle

When modifying shared APIs or database schemas:
1. **Deprecation Notice**:
   - Instead of immediately deleting a model property or route, mark it as deprecated in code using the `@deprecated` TypeScript tag.
   - The API will log a warning warning when the deprecated route is requested.
2. **Lifetime**: Deprecated components must remain active for at least **one minor version cycle** before they can be removed in a major release.
3. **Migration Guides**: Major version releases containing breaking changes must be accompanied by a migration guide detailing how to update client code.

---

## 3. Package Registry Version Synchronization

Monorepo workspace packages (`packages/design-system`, `packages/db`) are synchronized using Turborepo and package version management:
- Local applications reference packages using the workspace wildcard prefix: `"@pnj/db": "workspace:*"`
- Changes to packages increment the local package version and trigger a build verification across all dependent applications.
- External API releases are tagged on GitHub as `api-v1.2.0`, while web updates are tagged as `web-v1.1.0`.

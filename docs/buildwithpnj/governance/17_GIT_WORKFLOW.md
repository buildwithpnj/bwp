# Git Workflow Spec (17_GIT_WORKFLOW.md)

This document establishes the version control guidelines, commit formatting models, merge constraints, and branch protection rules enforced for the **BuildWithPNJ** platform.

---

## 1. Commit Message Standard (Conventional Commits)

Commit messages must follow the Conventional Commits specification. The structure is defined as:

`type(scope): description`

### Allowed Types
- **`feat`**: Introduces a new feature or visual interface (e.g. `feat(auth): add OAuth registration`).
- **`fix`**: Standard codebase bugfix (e.g. `fix(palette): escape special quote marks`).
- **`docs`**: Changes to documentation files (e.g. `docs(architecture): complete performance spec`).
- **`refactor`**: Refactoring code that does not alter behaviors or features.
- **`test`**: Writing or updating tests.
- **`chore`**: Maintenance, package dependencies, compiler configurations.

---

## 2. Commit Lifecycle & Pull Request (PR) Policy

1. **Development**: Create a feature branch off `develop`. Write clean code.
2. **Commit**: Save progress with atomic, small commits (e.g. `feat(notes): create sidebar layout`).
3. **PR Creation**: Open a pull request targeting `develop`. Include:
   - Clear description of the change.
   - Clickable links to any updated or new documents.
   - Proof of successful local build and tests pass.
4. **Code Review**: A minimum of one reviewer or automated agent must approve the PR before merge.

---

## 3. Merge Strategies

- **Develop Branch**: Merge pull requests using **Squash and Merge**. This squashes feature branch histories into a single commit, keeping `develop` history clean.
- **Main Branch**: Only release branches are merged into `main` using **Create a Merge Commit**, preserving the tag points.

---

## 4. Branch Protection Rules

To prevent regressions, the `main` and `develop` branches are locked under these branch protection rules:
- **Require Status Checks**: Build and validation tests must pass in GitHub Actions before a merge is allowed.
- **No Direct Push**: Direct pushes to protected branches are disabled.
- **Require PR Approvals**: A pull request is required to merge code.

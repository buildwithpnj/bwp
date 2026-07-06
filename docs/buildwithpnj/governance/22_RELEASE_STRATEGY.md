# Release Strategy Spec (22_RELEASE_STRATEGY.md)

This document maps the deployment cycles, release checks, verification sequences, and rollback strategies utilized to update the live **BuildWithPNJ** platform.

---

## 1. Release Cadence

The release cycle follows a structured release progression to maintain stability:
- **Weekly Releases**: Features compiled and merged into `develop` during the week are batched into a release branch on Thursdays.
- **Staging Verification**: Staging environments are verified on Fridays.
- **Production Releases**: Stable release packages are merged into `main` and tagged for production release on Mondays, avoiding Friday deployments to minimize operational risks.

---

## 2. Preview & Staging Verification Checklist

Before merging a release candidate branch (e.g. `release/v1.1.0`) into `main`, the build must pass these checks in the staging environment:
1. **Routing Verification**: Check that all navigation paths (`/projects`, `/labs`, `/journal`) load correctly.
2. **Command Palette Check**: Press `⌘K` to open the palette and verify that fuzzy search filtering and keyboard shortcuts work.
3. **Responsive Scaling**: Verify that layout displays render cleanly on desktop, tablet, and mobile screens.
4. **Performance verification**: Run a Lighthouse check to confirm the performance budget is met.
5. **Form submission**: Test newsletter signup and verify that database submissions succeed.

---

## 3. Rollback Procedures

If a production release causes a regression (e.g., database connection timeout or high blocking times):
- **Immediate Rollback**:
  - Open the Vercel Dashboard, select the previous deployment hash, and click **Promote to Production** to roll back the web app.
  - For the API backend, re-deploy the previous docker container version.
- **Post-Mortem**: Keep the broken container in a staging environment to investigate the root cause, and document findings in a incident log.

# Known Issues Log (KNOWN_ISSUES.md)

This log tracks lower-priority bugs, compiler warning lists, and optimization issues flagged during validation of the **BuildWithPNJ** platform.

---

## 1. Active Issues Catalog

### Issue 01: Standard `<img>` Usage in Dashboard Books Page
- **Description**: Next.js compilation logs warning indicators inside `src/app/(app)/books/page.tsx` on lines 309 and 401:
  `Warning: Using <img> could result in slower LCP and higher bandwidth. Consider using <Image />.`
- **Impact**: Low. The warnings affect pages behind authentication cookies rather than public landing paths.
- **Remediation**: Replace with `<Image />` component in the next release.

### Issue 02: Gray-Matter disk reads
- **Description**: Accessing local markdown content uses filesystem reads via `gray-matter`.
- **Impact**: Medium. Slows page load speeds when the number of articles exceeds 500 logs.
- **Remediation**: Implement a memory caching layer to cache parsed markdown files.

### Issue 03: Permissive API CORS Policies
- **Description**: FastAPI CORS settings default to permissive configurations (`allow_origins=["*"]`) in local configurations.
- **Impact**: Medium. Security risk if deployed directly to production.
- **Remediation**: Update CORS settings to restrict allowed origins to the main domain before deploying the production API backend.

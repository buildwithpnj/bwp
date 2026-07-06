# Release Checklist Spec (RELEASE_CHECKLIST.md)

This document establishes the pre-release checks, env requirements, server tasks, and rollback steps executed when updating production builds of the **BuildWithPNJ** platform.

---

## 1. Environment Configurations & Secrets

Before releasing:
- [ ] Check that `DATABASE_URL` matches the production Supabase database instance.
- [ ] Check that `JWT_SECRET` is set to a secure, randomly generated string.
- [ ] Check that `GITHUB_TOKEN` is configured with repository permissions.
- [ ] Check that Next.js production environment is set to `NODE_ENV=production`.

---

## 2. Release Steps Sequence

1. **Compilation Validation**: Run the production build command:
   ```bash
   npm run build --workspace=apps/web
   ```
2. **Review branch deployment**: Check that the Vercel branch builds successfully.
3. **Smoke Tests Verification**: Check that pages `/`, `/projects`, `/journal`, `/mission-control`, and `/dashboard` load correctly.
4. **Database schema migrations**: If schemas change, run:
   ```bash
   npx prisma db push
   ```
5. **Vercel Production Deployment**: Merge the release branch into `main` on GitHub to trigger the Vercel production deployment.
6. **Telemetry checks**: Monitor Sentry for any new exceptions.

---

## 3. Rollback Action Script

If production monitoring displays critical exceptions:
- **Web App**:
  - Open Vercel dashboard projects page.
  - Select the last successful build hash, click **Promote to Production** to roll back.
- **Backend API**:
  - Re-deploy the previous docker container version.
- **Database Schema**:
  - If a schema update caused a migration conflict, restore the database state using the daily backup file.
- **Verification**: Verify that the production site loads successfully.

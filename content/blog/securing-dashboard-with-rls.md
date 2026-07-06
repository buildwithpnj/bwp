---
title: "Securing Dashboard Data with PostgreSQL Row Level Security (RLS)"
excerpt: "Enforcing data isolation and access rules at the database engine layer to secure private workspaces."
publishDate: "2026-07-03"
tags: ["postgresql", "supabase", "security"]
featured: false
draft: false
---

Row-Level Security (RLS) is standard for multi-tenant and secure user environments. By enforcing session filters at the database engine layer, we ensure that bugs in the application code cannot leak private notes or financial logs across accounts.

## Enabling RLS

```sql
ALTER TABLE "Note" ENABLE ROW LEVEL SECURITY;
```

We establish policy queries matching the authenticated JWT user:

```sql
CREATE POLICY "Users can only modify their own notes"
ON "Note"
FOR ALL
USING (auth.uid() = user_id);
```
This forces PostgreSQL to automatically filter query yields before returning results to client requests.

---
title: "Configuring pgvector in Supabase for Semantic Searches"
excerpt: "How to set up semantic vector databases, store embeddings, and perform fast Cosine Similarity lookups inside PostgreSQL."
publishDate: "2026-07-02"
tags: ["postgresql", "supabase", "rag"]
featured: false
draft: false
---

Semantic search relies on representing textual data as high-dimensional vector embeddings. In this article, we enable the `pgvector` extension inside a managed Supabase database and write Cosine Similarity queries using Prisma.

## Setup Extension

Enable the extension inside your database migrations:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Next, define the vector column on your research documents table:

```sql
ALTER TABLE "ResearchDocument" ADD COLUMN embedding vector(1536);
```

We perform cosine similarity searches using custom database functions triggered via RPC.

---
id: "EXP-03"
title: "Semantic Embedding Chunking Strategies"
tagline: "Evaluating retrieval accuracy across document layout structures using pgvector."
status: "completed"
category: "RAG"
tags: ["rag", "supabase", "pgvector"]
hypothesis: "Parsing documents by layout sections rather than fixed character limits increases retrieval accuracy by 25%."
publishDate: "2026-07-03"
---

## Objective
To improve document search accuracy inside our vector database.

## Methodology
- Split documents using two methods:
  1. Fixed-size character chunks (e.g. 500 characters).
  2. Document layout parsing (e.g. sections and headings).
- Store embeddings in Supabase using `pgvector`.
- Run similarity queries to evaluate retrieval performance.

## Findings
- Layout-based chunking preserved semantic context, resulting in a **28% increase** in retrieval accuracy.

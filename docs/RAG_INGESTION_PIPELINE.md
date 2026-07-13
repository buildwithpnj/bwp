# RAG Ingestion Pipeline

Ingests Markdown knowledge documents automatically, normalizing content by computing SHA256 checksums.

## 1. Incremental Ingestion
- Evaluates changed files using content hashes to trigger re-indexing only on update.

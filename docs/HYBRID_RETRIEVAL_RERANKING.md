# Hybrid Retrieval & Reranking Flow

Combines keyword lexical index matches with mock vector search scores, reranking candidates based on word intersection counts.

## 1. Context Compression
- Compresses evidence bodies to enforce strict token budget gates.

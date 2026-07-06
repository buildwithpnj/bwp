# Search Architecture Spec (09_SEARCH_ARCHITECTURE.md)

This document describes the universal search system, command shortcuts layout, and future semantic search capabilities designed for the **BuildWithPNJ** platform.

---

## 1. Search Scope & Targets

The search engine acts as the unified directory portal, scanning across:
- **Static Content**: Articles, projects, and active lab writeups.
- **System Navigation**: Routing commands (e.g. `Go Home`, `Go Mission Control`).
- **External Links**: Quick actions (e.g. `GitHub profile`, `Twitter link`).
- **Interactive State**: Searching notes, habits, or bookmarks in the dashboard.

---

## 2. Command Palette Navigation Model

The primary command search interface is the Command Palette modal, triggered via `⌘K` or `Ctrl+K`. It supports sequential keyboard actions (chords):

```
                   CHORD SHORTCUT PATTERN
                              │
             User taps "g" (buffers key listener)
                              │
       ┌──────────────────────┼──────────────────────┐
       ▼ (if "h")             ▼ (if "p")             ▼ (if "d")
    Go Home                Go Projects            Go Dashboard
```

- **Selection Keys**: Arrow Up (`↑`) / Arrow Down (`↓`) scroll the focus, and `Enter` triggers the action.
- **Escape Key**: `Esc` closes the overlay instantly.

---

## 3. Fuzzy Matching Search Logic

To support typo-tolerant, instant search results under 10ms, the frontend lists use a lightweight matching algorithm:
- Search terms are split into characters.
- Compares terms using a scoring system: matches on the start of a word receive higher weights than matches in the middle.
- Exact matches are ranked at the top of the selection tree.

---

## 4. Vector Semantic Search Integration

As the database grows, the platform will support natural language semantic queries (e.g. *"Show me fastapi transaction ledger details"*):

1. **Embedding Generation**: When an article or experiment is published, the backend generates text embeddings using an LLM API (e.g. text-embedding-3-small).
2. **Storage**: Embeddings are stored in PostgreSQL using the **pgvector** extension.
3. **Similarity Search**: When a user submits a query:
   - Convert search prompt to embedding.
   - Run cosine-similarity queries inside pgvector:
     ```sql
     SELECT id, slug, title, (embedding <=> :query_embedding) AS distance
     FROM documents
     ORDER BY distance LIMIT 5;
     ```
   - Return relevant snippets.

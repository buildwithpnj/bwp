# Semantic Chunking Strategy

Segments files by structural markdown headers first, preventing paragraph splits and preserving list/table/code boundaries.

## 1. Context Overlap
- Prepends trailing context strings from preceding section chunks to maintain continuity.

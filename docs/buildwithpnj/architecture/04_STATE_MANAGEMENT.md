# State Management Spec (04_STATE_MANAGEMENT.md)

This document details the state management architecture of the unified **BuildWithPNJ** platform and its integrated **Warborn OS** dashboard subsystem.

---

## 1. State Categorization Architecture

```
                      GLOBAL PLATFORM STATE
                               │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
  SERVER STATE                                    CLIENT STATE
  (Query Engine)                                 (Zustand / Local)
        │                                               │
        ├─► Static CMS content (BuildWithPNJ blog)      ├─► Command Palette Open/Close
        ├─► User session tokens                         ├─► Warborn OS active note states
        └─► Dashboard data cache (Warborn OS)          └─► Habits daily completions
```

---

## 2. Server State (Data Synchronization)

Server state represents data owned by the backend database (Supabase/PostgreSQL) and external integrations (GitHub APIs).
- **Read Operations (BuildWithPNJ Static Content)**: Leverages Next.js Data Cache. Content parsed from markdown is statically cached on the server and revalidated on demand.
- **Read/Write Operations (Warborn OS Dashboard App)**: Handled by **React Query (TanStack Query)**:
  - Cache lifetimes are configured via strict `staleTime` metrics.
  - Queries are uniquely keyed: `['finance', 'summary']`, `['habits', 'active-sprint']`, `['notes', 'list']`.

---

## 3. Client & UI State (Zustand Stores)

Local UI state is managed using **Zustand** stores. In the context of the **Warborn OS** dashboard, Zustand stores manage the active UI state and local offline caches to ensure an instant-loading user experience.

### Unified Command Palette Store
Tracks search queries, active selections, and palette visibility.
```typescript
interface PaletteState {
  isOpen: boolean;
  searchQuery: string;
  setOpen: (open: boolean) => void;
  setSearchQuery: (query: string) => void;
}
```

### Keyboard Shortcut Chord Buffering
Manages keyboard state to listen for chord-style navigation (e.g. `g` -> `p`).
```typescript
interface ChordState {
  buffer: string;
  setBuffer: (char: string) => void;
  clearBuffer: () => void;
}
```

---

## 4. Optimistic State Updates

To guarantee high-velocity interactions (under 50ms perceived latency) in Warborn OS operations (e.g. checking off habits, saving notes):
- When a user logs a transaction or checks a habit, the UI instantly updates the local cache state before receiving the backend API response.
- If the API succeeds, the transaction completes silently.
- If the API fails, React Query's `onError` callback performs a rollback to restore the previous cache state.

---

## 5. Offline & Client Storage Strategy

As the Warborn OS subsystem support offline operations:
- **IndexedDB / LocalStorage Sync**: Cache note drafts and transaction lists inside IndexedDB.
- **Conflict Resolution**: Save offline modifications in a local sync queue. When connectivity is restored, push mutations sequentially using timestamp-based reconciliation to the FastAPI backend.

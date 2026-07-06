# Database Strategy Spec (06_DATABASE_STRATEGY.md)

This document describes the database design, object mapping relationships, and indexing patterns planned for the unified **BuildWithPNJ** platform. The storage engine is built on **Supabase** (PostgreSQL) and maps database entities for both the public branding pages and the internal **Warborn OS** dashboard subsystem.

---

## 1. Database Topology

```
                  POSTGRESQL (Supabase Instance)
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
  PUBLIC STATE (BuildWithPNJ)  INTERNAL STATE (Warborn OS)  TELEMETRY & LOGS
  - User Profiles              - Habits & Check-ins    - Activity Logs
  - Article Comments           - Notes & Folders       - Search query terms
  - Bookmarks & Subs           - Transactions Ledger   - Page Views Metrics
```

---

## 2. Prisma Database Schema Blueprint

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

// 1. Authentication & Profiles (Shared Core)
model User {
  id            String      @id @default(uuid())
  email         String      @unique
  passwordHash  String
  role          Role        @default(VISITOR)
  createdAt     DateTime    @default(now())
  updatedAt     DateTime    @updatedAt
  bookmarks     Bookmark[]
  comments      Comment[]
  
  // Warborn OS Subsystem Relations
  habits        Habit[]
  notes         Note[]
  transactions  Transaction[]
}

enum Role {
  ADMIN
  EDITOR
  VISITOR
}

// 2. Public Platform Tables (BuildWithPNJ)
model Subscriber {
  id         String   @id @default(uuid())
  email      String   @unique
  active     Boolean  @default(true)
  createdAt  DateTime @default(now())
}

model Comment {
  id         String   @id @default(uuid())
  content    String
  createdAt  DateTime @default(now())
  postId     String
  userId     String
  user       User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  @@index([postId])
}

model Bookmark {
  id         String   @id @default(uuid())
  createdAt  DateTime @default(now())
  userId     String
  postSlug   String
  user       User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([userId, postSlug])
}

// 3. Warborn OS Subsystem Tables (Internal Dashboard)
model Habit {
  id         String   @id @default(uuid())
  name       String
  userId     String
  user       User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt  DateTime @default(now())
}

model Note {
  id         String   @id @default(uuid())
  title      String
  content    String
  folder     String   @default("root")
  userId     String
  user       User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt  DateTime @default(now())
}

model Transaction {
  id         String   @id @default(uuid())
  amount     Float
  category   String
  userId     String
  user       User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt  DateTime @default(now())
}
```

---

## 3. Database Indexes & Query Optimizations

To ensure response speeds under 10ms for common queries:
- **Composite Indexes**: Defined on `Bookmark` queries (`userId` + `postSlug`) and `Note` fetches (`userId` + `folder`) to prevent sequential table scans.
- **Search Indexes**: Implement **GIN** indexes on text columns to support fast text-search matches inside notes and articles.

---

## 4. Database Security Policies

Since the application uses Supabase, Row-Level Security (RLS) is strictly enabled:
- **Read Access**: Public tables (Articles, Projects, Experiments) allow public read (`FOR SELECT USING true`).
- **Write Access**: Restricted to authenticated user IDs matching `auth.uid() = user_id`, securing Warborn OS personal database records (Notes, Habits, Transactions).

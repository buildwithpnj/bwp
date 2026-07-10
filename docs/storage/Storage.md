# Storage Routing & Selection — Warborn OS

This document explains the automatic storage routing and fallback selection algorithms.

## Automatic Storage Routing Rules

Storage routing uses file extensions to route uploads to specific drives:

| Category | File Extensions | Default Preferred Provider |
|---|---|---|
| **documents** | `.txt`, `.md`, `.docx`, `.pdf`, `.json`, `.csv`, `.xlsx` | Drive A |
| **images** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.svg`, `.ico` | Drive B |
| **videos** | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.mp3`, `.wav` | Drive B |
| **backups** | `.zip`, `.tar.gz`, `.tar`, `.sql`, `.bak` | Drive C |
| **logs** | `.log` or files containing `"log"` | Drive C |

## Quota Limit Checks (90% capacity rule)

1. When an upload is initiated, the manager checks the preferred drive (e.g. Drive A for a document).
2. The manager queries the database for the provider's `used_storage` and `available_storage`.
3. If `available_storage > 0`, it computes `usage_ratio = used_storage / available_storage`.
4. If the preferred drive's usage is **>= 90%**, the manager automatically skips the preferred drive and falls back to **another active drive** that is under 90% capacity.
5. If all drives are above 90% capacity, it falls back to the first active drive.

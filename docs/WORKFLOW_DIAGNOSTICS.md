# Workflow Self-Correction Diagnostics

Provides automated failure analysis logs and evidence points.

## 1. Diagnostic Process
1. A workflow step fails or retry limit is hit.
2. The UI triggers `POST /api/workflows/{id}/diagnose`.
3. The engine parses the execution timeline, error message, and checks against common failure pattern signatures.
4. Generates causes and links evidence details into a structured report card saved in the database.
5. Emits real-time suggestions to the user.

# Workflow Visual Step Graph

Renders workflow runs as visual nodes and dependency lines.

## 1. Visual Node Types
- **Transition Node**: Shows entry trigger and completion nodes.
- **Task Node**: Renders registered execution steps (e.g., `create_lesson_note`).

## 2. Dynamic badging
Nodes are decorated with status updates from execution history:
- **Approval Checkpoint**: A node marked `approval_required` flags checking approval status.
- **Retry Counters**: Number of retry counts (up to 3).
- **Diagnostics Overlay**: Clicking a failed node displays full causes and safe suggestions.

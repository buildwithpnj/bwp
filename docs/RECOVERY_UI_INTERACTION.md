# Recovery UI Interactivity

Actions triggered when interacting with node components inside the visualization panel.

## Click Event Handlers
1. **Selection**: Clicking a `failed` or `paused` step node opens the node detail side drawer.
2. **Details Drawer**: Renders:
   - Likely Causes compiled by context builder.
   - Evidence items (error trace, latency, retry depth).
   - Suggestions panel showing 1-3 sorted options.
3. **Trigger Operation**: Clicking a recovery recommendation (e.g., "Replay step") invokes `POST /api/workflows/{id}/control` with control request payload, updating the graph states in real time.

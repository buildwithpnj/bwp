# WebSocket Channel & Tenant Isolation Policy

Describes connection handling, auth requirements, and security gating.

## 1. Connection Endpoint
- Clients connect to `WS /api/ws/{user_id}`.
- Connection accepts user_role and tenant_id mapping metadata.

## 2. Tenant Isolation Rules
To protect user privacy and multi-tenant security boundaries:
1. **Admin Users**: Role `internal_admin` receives a global broadcast of all event changes across all tenants.
2. **Standard Users**: Receives only events where the `event.user_id` matches their own connection `user_id`.
3. Non-authorized cross-user event frames are filtered out at the `WebSocketManager.broadcast_event` gate.

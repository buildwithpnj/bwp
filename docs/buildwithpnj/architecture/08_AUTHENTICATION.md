# Authentication Spec (08_AUTHENTICATION.md)

This document describes the design specifications for securing user spaces, managing tokens, and restricting actions via Role-Based Access Control (RBAC) across the unified **BuildWithPNJ** platform and its integrated **Warborn OS** dashboard.

---

## 1. Unified Authentication System Flow

The platform uses a single, stateless, cookie-based JWT validation strategy to secure access to the dashboard. Authenticating on the BuildWithPNJ public website authorizes the user session for the Warborn OS dashboard at `/dashboard`.

```
User (Browser)               Next.js Web Server             FastAPI API Backend
     │                               │                               │
     ├─► 1. POST Credentials ───────►│                               │
     │      (Email & Password)       ├─► 2. Forward Credentials ────►│
     │                               │      to API Server            ├─► 3. Validate hash
     │                               │                               │   & generate JWT
     │                               │◄─ 4. Return JWT Token ────────┤
     │◄─ 5. Set HTTP-Only Cookie ────┤
     │      (Secure, SameSite=Strict)│
```

---

## 2. Token Security Policies

- **HttpOnly Cookies**: Prevents client-side scripts from reading session tokens, mitigating XSS token extraction vectors.
- **SameSite=Strict**: Instructs the browser to only attach authentication cookies to requests originating from the primary domain, preventing Cross-Site Request Forgery (CSRF).
- **Token Validity**:
  - Access Tokens expire after **15 minutes**.
  - Refresh Tokens are stored in a database table and expire after **7 days**, allowing users to persist sessions securely.

---

## 3. Role-Based Access Control (RBAC) Hierarchy

Users are assigned one of three roles, which define their permissions across the public brand pages and internal Warborn OS features:

| Action / Capability | Visitor | Developer | Admin |
| :--- | :--- | :--- | :--- |
| View public website pages (BuildWithPNJ) | ✓ | ✓ | ✓ |
| Submit contact forms / subs | ✓ | ✓ | ✓ |
| Write comments on articles | ✗ | ✓ | ✓ |
| Access Warborn OS workspace (`/dashboard`) | ✗ | ✓ | ✓ |
| Manage personal notes, habits, finances | ✗ | ✓ | ✓ |
| Delete comments or users | ✗ | ✗ | ✓ |
| Modify platform settings | ✗ | ✗ | ✓ |

---

## 4. Endpoint Protection Architecture

FastAPI utilizes dependency injection to enforce role permissions before executing database or system operations:

```python
from fastapi import Depends, HTTPException, status

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Decode and parse token
    ...

def require_role(allowed_roles: list[Role]):
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this action"
            )
        return current_user
    return dependency

# Usage in Router - Protects Warborn OS notes endpoint
@router.post("/notes", dependencies=[Depends(require_role([Role.ADMIN, Role.DEVELOPER]))])
def create_note(note: NoteCreate):
    return service.create(note)
```

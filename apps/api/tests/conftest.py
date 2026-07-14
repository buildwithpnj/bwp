import sys
import os
from contextlib import asynccontextmanager

# Add the project root to sys.path so imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.main import app
from app.database import get_db
from app.deps import get_current_user
from app.models.governance import PreviewSession
from app.models.user import User

# Override FastAPI app lifespan context manager to bypass database/migrations on test startup
@asynccontextmanager
async def dummy_lifespan(app_inst):
    yield

app.router.lifespan_context = dummy_lifespan

@pytest.fixture(autouse=True)
def mock_db_dependency():
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    
    dummy_session = PreviewSession(
        id="mock_session_id",
        ip_address="127.0.0.1",
        turns=0,
        tokens=0,
        cost=0.0,
        active=True
    )
    
    async def mock_refresh(obj):
        if not getattr(obj, "id", None):
            obj.id = "mock_session_id"
            
    mock_session.refresh = mock_refresh
    
    async def mock_execute(query, *args, **kwargs):
        query_str = str(query).lower()
        mock_result = MagicMock()
        
        if "durable_preview_sessions" in query_str:
            mock_result.scalar_one_or_none.return_value = dummy_session
        elif "system_configs" in query_str:
            mock_result.scalar_one_or_none.return_value = None
        else:
            mock_result.scalar_one_or_none.return_value = None
            
        mock_result.scalars.return_value.all.return_value = []
        return mock_result
        
    mock_session.execute = mock_execute
    
    async def override_get_db():
        yield mock_session
        
    async def override_get_current_user():
        return User(
            id="mock_session_id",
            email="test@example.com",
            role="approved_user",
            password_hash="fakehash"
        )
        
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    yield mock_session
    app.dependency_overrides.clear()

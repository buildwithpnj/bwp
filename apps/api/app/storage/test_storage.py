import pytest
from unittest.mock import AsyncMock, MagicMock
from app.models.storage_provider import StorageProvider
from app.storage.utils import encrypt_token, decrypt_token
from app.storage.services import StorageManager


def test_encryption_decryption():
    """Verify that tokens are encrypted and decrypted successfully."""
    token = "ya29.a0AXooCg..."
    encrypted = encrypt_token(token)
    assert encrypted != token
    assert decrypt_token(encrypted) == token


def test_category_detection():
    """Verify category detection correctly matches extensions to categories."""
    assert StorageManager.detect_category("report.pdf", "application/pdf") == "documents"
    assert StorageManager.detect_category("notes.md", "text/markdown") == "documents"
    assert StorageManager.detect_category("photo.png", "image/png") == "images"
    assert StorageManager.detect_category("avatar.jpg", "image/jpeg") == "images"
    assert StorageManager.detect_category("movie.mp4", "video/mp4") == "videos"
    assert StorageManager.detect_category("backup_db.sql", "application/sql") == "backups"
    assert StorageManager.detect_category("system.log", "text/plain") == "logs"


@pytest.mark.asyncio
async def test_provider_selection_routing():
    """Verify default routing matches correct drives."""
    mock_db = MagicMock()
    # Mock db.execute as an AsyncMock to support await
    mock_db.execute = AsyncMock()
    
    # Mock drive A returned
    drive_a = StorageProvider(name="Drive A", status="active", available_storage=0, used_storage=0)
    
    # Mock result object returned by execute
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = drive_a
    mock_db.execute.return_value = mock_result
    
    # Force mock seed check to do nothing
    StorageManager.seed_drives_if_empty = AsyncMock()
    
    selected = await StorageManager.select_provider(mock_db, "document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert selected.name == "Drive A"


@pytest.mark.asyncio
async def test_provider_capacity_fallback():
    """Verify automatic fallback when preferred drive is >= 90% capacity."""
    mock_db = MagicMock()
    # Mock db.execute as an AsyncMock to support await
    mock_db.execute = AsyncMock()
    
    # Mock Drive A is full (95% usage)
    drive_a = StorageProvider(name="Drive A", status="active", available_storage=1000, used_storage=950)
    # Mock Drive B is healthy (20% usage)
    drive_b = StorageProvider(name="Drive B", status="active", available_storage=1000, used_storage=200)
    
    # Mock result object returned by execute
    mock_result_pref = MagicMock()
    mock_result_pref.scalar_one_or_none.return_value = drive_a
    
    mock_result_all = MagicMock()
    mock_result_all.scalars.return_value.all.return_value = [drive_a, drive_b]
    
    # Return different results for consecutive calls of await db.execute()
    mock_db.execute.side_effect = [mock_result_pref, mock_result_all]
    
    StorageManager.seed_drives_if_empty = AsyncMock()
    
    # Document normally goes to Drive A, but Drive A is full. It should select Drive B as fallback!
    selected = await StorageManager.select_provider(mock_db, "report.pdf", "application/pdf")
    assert selected.name == "Drive B"

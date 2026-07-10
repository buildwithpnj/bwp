import pytest
from unittest.mock import AsyncMock, MagicMock, patch
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
    """Verify default routing matches correct drives based on category."""
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()
    
    drive_a = StorageProvider(name="Drive A", provider_label="A", status="active", available_storage=0, used_storage=0)
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = drive_a
    mock_db.execute.return_value = mock_result
    
    StorageManager.seed_drives_if_empty = AsyncMock()
    
    selected = await StorageManager.select_provider(
        mock_db,
        file_name="document.docx",
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert selected.name == "Drive A"


@pytest.mark.asyncio
async def test_provider_capacity_fallback():
    """Verify automatic fallback when preferred drive is >= 90% capacity."""
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()
    
    drive_a = StorageProvider(name="Drive A", provider_label="A", status="active", available_storage=1000, used_storage=950)
    drive_b = StorageProvider(name="Drive B", provider_label="B", status="active", available_storage=1000, used_storage=200)
    
    # Preferred call returns drive_a
    mock_result_pref = MagicMock()
    mock_result_pref.scalar_one_or_none.return_value = drive_a
    
    # default_provider call returns drive_b
    mock_result_default = MagicMock()
    mock_result_default.scalars.return_value.first.return_value = drive_b
    
    mock_db.execute.side_effect = [mock_result_pref, mock_result_default]
    StorageManager.seed_drives_if_empty = AsyncMock()
    
    selected = await StorageManager.select_provider(mock_db, file_name="report.pdf", content_type="application/pdf")
    assert selected.name == "Drive B"


@pytest.mark.asyncio
async def test_explicit_provider_choice():
    """Verify explicit provider choice routes directly and bypasses category logic."""
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()
    
    drive_b = StorageProvider(name="Drive B", provider_label="B", status="active")
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = drive_b
    mock_db.execute.return_value = mock_result
    
    StorageManager.seed_drives_if_empty = AsyncMock()
    
    selected = await StorageManager.select_provider(mock_db, provider_choice="B", file_name="document.docx")
    assert selected.name == "Drive B"


@pytest.mark.asyncio
async def test_auto_failover_on_upload_error():
    """Verify auto-failover to Provider B if Provider A throws an upload exception."""
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()
    mock_db.commit = AsyncMock()
    
    drive_a = StorageProvider(id="1", name="Drive A", provider_label="A", status="active")
    drive_b = StorageProvider(id="2", name="Drive B", provider_label="B", status="active")
    
    # 1. select_provider selects drive_a
    # 2. find failover providers selects drive_b
    mock_result_failover = MagicMock()
    mock_result_failover.scalars.return_value.all.return_value = [drive_b]
    mock_db.execute.return_value = mock_result_failover
    
    StorageManager.select_provider = AsyncMock(return_value=drive_a)
    
    # Mock drivers
    mock_driver_a = AsyncMock()
    mock_driver_a.upload.side_effect = Exception("Google Drive A connection refused")
    
    mock_driver_b = AsyncMock()
    mock_driver_b.upload.return_value = "file-id-on-b"
    mock_driver_b.get_quota.return_value = (100, 1000)
    
    async def get_driver_mock(provider):
        if provider.name == "Drive A":
            return mock_driver_a
        return mock_driver_b
        
    StorageManager.get_driver_for_provider = get_driver_mock
    
    # Execute upload: drive_a will fail, it should automatically route to drive_b
    file_id = await StorageManager.upload(mock_db, "backup.zip", "application/zip", b"dummy-data")
    assert file_id == "file-id-on-b"

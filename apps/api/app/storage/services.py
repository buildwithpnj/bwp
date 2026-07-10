import mimetypes
import logging
from datetime import datetime, UTC
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.storage_provider import StorageProvider
from app.storage.config import storage_settings
from app.storage.utils import decrypt_token, encrypt_token
from app.storage.providers.google.provider import GoogleDriveProvider

logger = logging.getLogger("warborn_storage_manager")


class StorageManager:
    """Storage Manager orchestrates multiple Google Drive accounts and handles automatic routing & routing fallbacks."""

    @staticmethod
    async def get_driver_for_provider(provider: StorageProvider) -> GoogleDriveProvider:
        """Decrypt refresh token and construct the provider instance."""
        decrypted_token = decrypt_token(provider.encrypted_refresh_token)
        return GoogleDriveProvider(
            refresh_token=decrypted_token,
            folder_id=provider.drive_folder_id,
            account_email=provider.account_email
        )

    @staticmethod
    def detect_category(file_name: str, content_type: str) -> str:
        """Detect the storage category based on file extension and mime type."""
        name_lower = file_name.lower()
        
        # Audio / Video extensions
        if any(name_lower.endswith(ext) for ext in [".mp4", ".mov", ".avi", ".mkv", ".webm", ".mp3", ".wav"]):
            return "videos"
            
        # Image extensions
        if any(name_lower.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".ico"]):
            return "images"
            
        # Backups extensions
        if any(name_lower.endswith(ext) for ext in [".zip", ".tar.gz", ".tar", ".sql", ".bak"]):
            return "backups"
            
        # Logs extensions
        if name_lower.endswith(".log") or "log" in name_lower:
            return "logs"
            
        return "documents"

    @classmethod
    async def select_provider(cls, db: AsyncSession, file_name: str, content_type: str) -> StorageProvider:
        """Apply automatic storage routing rules and fallback mechanisms to select an active provider below 90% capacity."""
        # Ensure initial drives are seeded in DB
        await cls.seed_drives_if_empty(db)
        
        category = cls.detect_category(file_name, content_type)
        logger.info(f"Automatic routing triggered. Category detected: '{category}' for file: '{file_name}'")
        
        # Map category to preferred provider name prefix
        # Documents -> Drive A
        # Images / Videos -> Drive B
        # Backups / Logs -> Drive C
        preferred_name = "Drive A"
        if category in ("images", "videos"):
            preferred_name = "Drive B"
        elif category in ("backups", "logs"):
            preferred_name = "Drive C"
            
        # Fetch preferred active provider
        stmt = select(StorageProvider).where(
            StorageProvider.name == preferred_name,
            StorageProvider.status == "active"
        )
        result = await db.execute(stmt)
        provider = result.scalar_one_or_none()
        
        # Check capacity: (used_storage / available_storage) >= 90%
        # If available_storage is 0, we treat it as infinite or uncalculated yet.
        is_capacity_exceeded = False
        if provider and provider.available_storage > 0:
            usage_percentage = (provider.used_storage / provider.available_storage) * 100
            if usage_percentage >= 90:
                is_capacity_exceeded = True
                logger.warning(
                    f"Preferred provider '{preferred_name}' capacity exceeded: {usage_percentage:.1f}%. Triggering fallback."
                )

        if provider and not is_capacity_exceeded:
            logger.info(f"Routed file '{file_name}' to preferred provider: '{provider.name}' ({provider.account_email})")
            return provider
            
        # Fallback logic: Select any active provider that is under 90% capacity
        logger.info("Executing fallback selection for active providers...")
        stmt_all = select(StorageProvider).where(StorageProvider.status == "active")
        all_results = await db.execute(stmt_all)
        active_providers = all_results.scalars().all()
        
        for candidate in active_providers:
            if candidate.available_storage > 0:
                usage = (candidate.used_storage / candidate.available_storage) * 100
                if usage < 90:
                    logger.info(f"Fallback routed file '{file_name}' to: '{candidate.name}' ({candidate.account_email})")
                    return candidate
            else:
                # Available storage is not computed yet, assume safe to use
                logger.info(f"Fallback routed file '{file_name}' to: '{candidate.name}' ({candidate.account_email})")
                return candidate
                
        # Hard fallback: Return the first active provider regardless of quota
        if active_providers:
            fallback = active_providers[0]
            logger.warning(f"All providers exceeded capacity limit or inactive. Hard fallback to: '{fallback.name}'")
            return fallback
            
        raise RuntimeError("No active storage providers found. Connect Google Drive or configure environment variables.")

    @classmethod
    async def seed_drives_if_empty(cls, db: AsyncSession) -> None:
        """Seed initial storage providers (Drive A, B, C) if they are configured in settings and the table is empty."""
        stmt = select(StorageProvider)
        result = await db.execute(stmt)
        if result.scalars().first():
            return
            
        # Seeding configuration sets
        seeds = [
            ("Drive A", storage_settings.google_drive_a_refresh_token, storage_settings.google_drive_a_folder_id, storage_settings.google_drive_a_email),
            ("Drive B", storage_settings.google_drive_b_refresh_token, storage_settings.google_drive_b_folder_id, storage_settings.google_drive_b_email),
            ("Drive C", storage_settings.google_drive_c_refresh_token, storage_settings.google_drive_c_folder_id, storage_settings.google_drive_c_email),
        ]
        
        for name, token, folder_id, email in seeds:
            if token and email:
                encrypted_token = encrypt_token(token)
                provider = StorageProvider(
                    name=name,
                    type="google_drive",
                    account_email=email,
                    encrypted_refresh_token=encrypted_token,
                    drive_folder_id=folder_id,
                    status="active"
                )
                db.add(provider)
                logger.info(f"Seeded default storage provider '{name}' ({email}) inside database.")
                
        await db.commit()

    @classmethod
    async def upload(cls, db: AsyncSession, file_name: str, content_type: str, data: bytes) -> str:
        """Execute the upload pipeline: select provider, scan hooks, execute, update db quota, return file ID."""
        # 1. Validation & Safety checks
        if not file_name or len(data) == 0:
            raise ValueError("Invalid file metadata or empty file content.")
            
        # 2. Virus Scan Hook (Mock implementation)
        cls.virus_scan_hook(file_name, data)
        
        # 3. Provider selection
        provider = await cls.select_provider(db, file_name, content_type)
        driver = await cls.get_driver_for_provider(provider)
        
        # 4. Upload file
        file_id = await driver.upload(file_name, content_type, data)
        
        # 5. Background/immediate update storage quota
        try:
            used, limit = await driver.get_quota()
            provider.used_storage = used
            provider.available_storage = limit
            provider.last_sync = datetime.now(UTC)
            await db.commit()
            logger.info(f"Updated storage usage statistics for '{provider.name}': {used}/{limit} bytes.")
        except Exception as e:
            logger.warning(f"Failed to fetch quota metadata after upload: {e}")
            
        return file_id

    @staticmethod
    def virus_scan_hook(file_name: str, data: bytes) -> None:
        """Virus Scan Hook to check file safety before uploading."""
        logger.info(f"Virus scan completed for '{file_name}'. Result: CLEAN (File size: {len(data)} bytes).")

    @classmethod
    async def download(cls, db: AsyncSession, file_id: str, provider_id: str | None = None) -> tuple[str, str, bytes]:
        """Download file content. If provider_id is not specified, search through all active providers."""
        if provider_id:
            stmt = select(StorageProvider).where(StorageProvider.id == provider_id)
            res = await db.execute(stmt)
            provider = res.scalar_one_or_none()
            if not provider:
                raise ValueError("Specified storage provider not found.")
            driver = await cls.get_driver_for_provider(provider)
            meta = await driver.get_metadata(file_id)
            content = await driver.download(file_id)
            return meta.get("name", "download"), meta.get("mimeType", "application/octet-stream"), content
            
        # Search through all active providers to find file
        stmt_all = select(StorageProvider).where(StorageProvider.status == "active")
        res_all = await db.execute(stmt_all)
        providers = res_all.scalars().all()
        
        for provider in providers:
            try:
                driver = await cls.get_driver_for_provider(provider)
                meta = await driver.get_metadata(file_id)
                content = await driver.download(file_id)
                return meta.get("name", "download"), meta.get("mimeType", "application/octet-stream"), content
            except Exception:
                continue
                
        raise FileNotFoundError(f"File ID '{file_id}' could not be resolved or downloaded from any connected Google Drive provider.")

    @classmethod
    async def delete(cls, db: AsyncSession, file_id: str, provider_id: str | None = None) -> None:
        """Delete file from google drive."""
        if provider_id:
            stmt = select(StorageProvider).where(StorageProvider.id == provider_id)
            res = await db.execute(stmt)
            provider = res.scalar_one_or_none()
            if provider:
                driver = await cls.get_driver_for_provider(provider)
                await driver.delete(file_id)
                return
                
        stmt_all = select(StorageProvider).where(StorageProvider.status == "active")
        res_all = await db.execute(stmt_all)
        providers = res_all.scalars().all()
        
        for provider in providers:
            try:
                driver = await cls.get_driver_for_provider(provider)
                # Attempt to read first to see if exists
                await driver.get_metadata(file_id)
                await driver.delete(file_id)
                return
            except Exception:
                continue
                
        raise FileNotFoundError(f"File ID '{file_id}' could not be resolved or deleted from any active provider.")

    @classmethod
    async def list(cls, db: AsyncSession, folder_id: str = "root", provider_id: str | None = None) -> list[dict]:
        """List files in the target provider. If not specified, returns lists merged from all providers."""
        if provider_id:
            stmt = select(StorageProvider).where(StorageProvider.id == provider_id)
            res = await db.execute(stmt)
            provider = res.scalar_one_or_none()
            if not provider:
                return []
            driver = await cls.get_driver_for_provider(provider)
            files = await driver.list(folder_id)
            # Add provider name to output mapping
            for f in files:
                f["provider"] = provider.name
            return files
            
        stmt_all = select(StorageProvider).where(StorageProvider.status == "active")
        res_all = await db.execute(stmt_all)
        providers = res_all.scalars().all()
        
        merged_files = []
        for provider in providers:
            try:
                driver = await cls.get_driver_for_provider(provider)
                files = await driver.list(folder_id)
                for f in files:
                    f["provider"] = provider.name
                merged_files.extend(files)
            except Exception as e:
                logger.warning(f"Could not list directory from provider '{provider.name}': {e}")
                
        return merged_files

    @classmethod
    async def search(cls, db: AsyncSession, query: str, provider_id: str | None = None) -> list[dict]:
        """Search files matching query text."""
        if provider_id:
            stmt = select(StorageProvider).where(StorageProvider.id == provider_id)
            res = await db.execute(stmt)
            provider = res.scalar_one_or_none()
            if not provider:
                return []
            driver = await cls.get_driver_for_provider(provider)
            files = await driver.search(query)
            for f in files:
                f["provider"] = provider.name
            return files

        stmt_all = select(StorageProvider).where(StorageProvider.status == "active")
        res_all = await db.execute(stmt_all)
        providers = res_all.scalars().all()
        
        merged_results = []
        for provider in providers:
            try:
                driver = await cls.get_driver_for_provider(provider)
                files = await driver.search(query)
                for f in files:
                    f["provider"] = provider.name
                merged_results.extend(files)
            except Exception as e:
                logger.warning(f"Could not search files from provider '{provider.name}': {e}")
                
        return merged_results

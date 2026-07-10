import logging
from typing import Any
from fastapi import APIRouter, File, HTTPException, UploadFile, Query, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy import select
from pydantic import BaseModel

from app.deps import DB, CurrentUser
from app.models.storage_provider import StorageProvider
from app.storage.services import StorageManager
from app.storage.providers.google.oauth import GoogleOAuthManager
from app.storage.utils import encrypt_token

logger = logging.getLogger("warborn_storage_routes")

router = APIRouter(prefix="/api/storage", tags=["Storage Management"])


class CallbackRequest(BaseModel):
    code: str


@router.get("/auth/google/login")
async def google_auth_login(current_user: CurrentUser):
    """Generate authorization consent URL to connect a new Google Drive provider account."""
    oauth = GoogleOAuthManager()
    try:
        url = oauth.get_authorization_url()
        return {"url": url}
    except Exception as e:
        logger.error(f"Failed to generate google consent url: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/google/callback")
async def google_auth_callback(body: CallbackRequest, current_user: CurrentUser, db: DB):
    """Receive code from consent flow, exchange for tokens, encrypt, and register a new StorageProvider."""
    oauth = GoogleOAuthManager()
    try:
        tokens = oauth.exchange_code_for_tokens(body.code)
        refresh_token = tokens.get("refresh_token")
        email = tokens.get("email")

        if not refresh_token:
            # Refresh token is only sent on first consent screen authorization.
            # Google doesn't return refresh token if reconnecting without consent prompt.
            # We raise warning or search if provider already exists in database.
            stmt = select(StorageProvider).where(StorageProvider.account_email == email)
            res = await db.execute(stmt)
            existing = res.scalar_one_or_none()
            if existing:
                return {"status": "success", "message": f"Provider for '{email}' is already fully authorized."}
                
            raise HTTPException(
                status_code=400,
                detail="Google did not return a refresh token. Please go to your Google account security settings, remove 'Warborn OS' authorization, and reconnect to trigger fresh consent."
            )

        encrypted_token = encrypt_token(refresh_token)

        # Check if provider already exists
        stmt = select(StorageProvider).where(StorageProvider.account_email == email)
        res = await db.execute(stmt)
        provider = res.scalar_one_or_none()

        if not provider:
            # Determine dynamic name: Count existing providers in database to assign index name
            stmt_count = select(StorageProvider)
            res_count = await db.execute(stmt_count)
            count = len(res_count.scalars().all())
            letter = chr(65 + count) if count < 26 else str(count)
            name = f"Drive {letter}"

            provider = StorageProvider(
                name=name,
                type="google_drive",
                account_email=email,
                encrypted_refresh_token=encrypted_token,
                status="active"
            )
            db.add(provider)
            logger.info(f"Registered new storage provider: '{name}' for '{email}'.")
        else:
            provider.encrypted_refresh_token = encrypted_token
            provider.status = "active"
            logger.info(f"Refreshed authorization token for existing provider: '{provider.name}' ({email}).")

        await db.commit()
        return {"status": "success", "connected": True, "email": email, "provider": provider.name}

    except Exception as e:
        logger.error(f"Failed to handle oauth callback token exchange: {e}")
        raise HTTPException(status_code=400, detail=f"OAuth connection failed: {str(e)}")


@router.post("/upload")
async def upload_file(
    db: DB,
    current_user: CurrentUser,
    file: UploadFile = File(...),
):
    """Upload a file. The Storage Manager automatically routes the file and validates it."""
    try:
        content = await file.read()
        file_id = await StorageManager.upload(
            db=db,
            file_name=file.filename,
            content_type=file.content_type,
            data=content
        )
        return {"status": "success", "file_id": file_id, "filename": file.filename}
    except Exception as e:
        logger.error(f"File upload error in route: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/download/{file_id}")
async def download_file(
    file_id: str,
    db: DB,
    current_user: CurrentUser,
    provider_id: str | None = Query(default=None),
):
    """Download a file by remote ID. Fetches and streams data from the storage network."""
    try:
        name, mime, content = await StorageManager.download(db, file_id, provider_id)
        from io import BytesIO
        return StreamingResponse(
            BytesIO(content),
            media_type=mime,
            headers={
                "Content-Disposition": f'attachment; filename="{name}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            }
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Download route error for file '{file_id}': {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list")
async def list_files(
    db: DB,
    current_user: CurrentUser,
    folder_id: str = Query(default="root"),
    provider_id: str | None = Query(default=None),
):
    """List all active files in a directory."""
    try:
        files = await StorageManager.list(db, folder_id, provider_id)
        return {"files": files}
    except Exception as e:
        logger.error(f"List files route error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{file_id}")
async def delete_file(
    file_id: str,
    db: DB,
    current_user: CurrentUser,
    provider_id: str | None = Query(default=None),
):
    """Delete a file from the storage system."""
    try:
        await StorageManager.delete(db, file_id, provider_id)
        return {"status": "success", "message": f"File '{file_id}' deleted successfully."}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Delete file route error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/providers")
async def get_providers(db: DB, current_user: CurrentUser):
    """List status, capacity, and sync times for all registered storage providers."""
    # Seed default drives if database is empty
    await StorageManager.seed_drives_if_empty(db)
    
    stmt = select(StorageProvider)
    res = await db.execute(stmt)
    providers = res.scalars().all()
    
    output = []
    for p in providers:
        output.append({
            "id": p.id,
            "name": p.name,
            "type": p.type,
            "account_email": p.account_email,
            "drive_folder_id": p.drive_folder_id,
            "status": p.status,
            "used_storage": p.used_storage,
            "available_storage": p.available_storage,
            "last_sync": p.last_sync.isoformat() if p.last_sync else None
        })
    return {"providers": output}


@router.get("/search")
async def search_files(
    q: str,
    db: DB,
    current_user: CurrentUser,
    provider_id: str | None = Query(default=None),
):
    """Search for files in storage matching query text."""
    try:
        files = await StorageManager.search(db, q, provider_id)
        return {"files": files}
    except Exception as e:
        logger.error(f"Search route error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def storage_health(db: DB, current_user: CurrentUser):
    """Check connectivity to all active storage providers in database."""
    stmt = select(StorageProvider).where(StorageProvider.status == "active")
    res = await db.execute(stmt)
    providers = res.scalars().all()
    
    status_report = {}
    is_healthy = True
    
    for p in providers:
        try:
            driver = await StorageManager.get_driver_for_provider(p)
            await driver.get_quota()
            status_report[p.name] = "healthy"
        except Exception as e:
            status_report[p.name] = f"error: {str(e)}"
            is_healthy = False
            
    if not status_report:
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "message": "No active providers configured", "details": status_report}
        )
        
    return {
        "status": "healthy" if is_healthy else "degraded",
        "details": status_report
    }

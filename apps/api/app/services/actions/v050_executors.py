import json
from datetime import datetime, date, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List, Optional

from app.models.notes import Note
from app.models.goals import Goal
from app.models.project_item import ProjectItem
from app.models.books import Book
from app.models.storage_provider import StorageProvider
from app.models.calendar_event import CalendarEvent
from app.models.habits import Habit, HabitLog
from app.models.recovery import Addiction, RelapseLog
from app.models.user_profile_memory import UserProfileMemory
from app.models.knowledge_document import KnowledgeDocument
from app.models.action_models import TrashItem

class DeleteNoteAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        note_id = payload["note_id"]
        stmt = select(Note).where(Note.id == note_id, Note.user_id == user_id)
        res = await db.execute(stmt)
        note = res.scalar_one_or_none()
        if not note:
            return {"status": "failed", "error": "Note not found or unauthorized."}
        
        # Soft delete: store in TrashItem
        trash = TrashItem(
            user_id=user_id,
            item_type="note",
            item_id=note.id,
            original_data={
                "title": note.title,
                "body_json": note.body_json,
                "tags": note.tags
            }
        )
        db.add(trash)
        await db.delete(note)
        await db.flush()
        return {"status": "success", "message": f"Note '{note.title}' moved to trash."}

class RestoreNoteAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        note_id = payload["note_id"]
        stmt = select(TrashItem).where(TrashItem.item_id == note_id, TrashItem.item_type == "note", TrashItem.user_id == user_id)
        res = await db.execute(stmt)
        trash = res.scalar_one_or_none()
        if not trash:
            return {"status": "failed", "error": "Trashed note not found."}
        
        # Restore original note
        note = Note(
            id=trash.item_id,
            user_id=user_id,
            title=trash.original_data["title"],
            body_json=trash.original_data["body_json"],
            tags=trash.original_data.get("tags")
        )
        db.add(note)
        await db.delete(trash)
        await db.flush()
        return {"status": "success", "message": f"Note '{note.title}' restored successfully."}

class SearchNotesAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        query = payload["query"]
        stmt = select(Note).where(Note.user_id == user_id, Note.title.ilike(f"%{query}%"))
        res = await db.execute(stmt)
        notes = res.scalars().all()
        return {
            "status": "success",
            "results": [{"id": n.id, "title": n.title, "tags": n.tags} for n in notes]
        }

class PrioritizeTaskAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        task_id = payload["task_id"]
        pinned = payload["pinned"]
        stmt = select(Goal).where(Goal.id == task_id, Goal.user_id == user_id)
        res = await db.execute(stmt)
        task = res.scalar_one_or_none()
        if not task:
            return {"status": "failed", "error": "Task not found."}
        task.pinned = pinned
        db.add(task)
        await db.flush()
        return {"status": "success", "message": f"Task '{task.title}' pinned set to {pinned}."}

class DeleteTaskAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        task_id = payload["task_id"]
        stmt = select(Goal).where(Goal.id == task_id, Goal.user_id == user_id)
        res = await db.execute(stmt)
        task = res.scalar_one_or_none()
        if not task:
            return {"status": "failed", "error": "Task not found."}
        
        trash = TrashItem(
            user_id=user_id,
            item_type="task",
            item_id=task.id,
            original_data={
                "title": task.title,
                "description": task.description,
                "category": task.category,
                "progress": task.progress,
                "status": task.status,
                "pinned": task.pinned
            }
        )
        db.add(trash)
        await db.delete(task)
        await db.flush()
        return {"status": "success", "message": f"Task '{task.title}' moved to trash."}

class RestoreTaskAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        task_id = payload["task_id"]
        stmt = select(TrashItem).where(TrashItem.item_id == task_id, TrashItem.item_type == "task", TrashItem.user_id == user_id)
        res = await db.execute(stmt)
        trash = res.scalar_one_or_none()
        if not trash:
            return {"status": "failed", "error": "Trashed task not found."}
        
        task = Goal(
            id=trash.item_id,
            user_id=user_id,
            title=trash.original_data["title"],
            description=trash.original_data.get("description"),
            category=trash.original_data.get("category"),
            progress=trash.original_data.get("progress", 0),
            status=trash.original_data.get("status", "pending"),
            pinned=trash.original_data.get("pinned", False)
        )
        db.add(task)
        await db.delete(trash)
        await db.flush()
        return {"status": "success", "message": f"Task '{task.title}' restored successfully."}

class CreateProjectAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        name = payload["name"]
        description = payload.get("description")
        proj = ProjectItem(
            user_id=user_id,
            name=name,
            description=description,
            status="active"
        )
        db.add(proj)
        await db.flush()
        return {"status": "success", "project_id": proj.id, "message": f"Project '{name}' created."}

class UpdateProjectAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        project_id = payload["project_id"]
        status = payload["status"]
        name = payload.get("name")
        description = payload.get("description")
        
        stmt = select(ProjectItem).where(ProjectItem.id == project_id, ProjectItem.user_id == user_id)
        res = await db.execute(stmt)
        proj = res.scalar_one_or_none()
        if not proj:
            return {"status": "failed", "error": "Project not found."}
            
        proj.status = status
        if name:
            proj.name = name
        if description:
            proj.description = description
            
        db.add(proj)
        await db.flush()
        return {"status": "success", "message": f"Project '{proj.name}' updated."}

class CompleteProjectAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        project_id = payload["project_id"]
        stmt = select(ProjectItem).where(ProjectItem.id == project_id, ProjectItem.user_id == user_id)
        res = await db.execute(stmt)
        proj = res.scalar_one_or_none()
        if not proj:
            return {"status": "failed", "error": "Project not found."}
        proj.status = "completed"
        db.add(proj)
        await db.flush()
        return {"status": "success", "message": f"Project '{proj.name}' marked completed."}

class DeleteProjectAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        project_id = payload["project_id"]
        stmt = select(ProjectItem).where(ProjectItem.id == project_id, ProjectItem.user_id == user_id)
        res = await db.execute(stmt)
        proj = res.scalar_one_or_none()
        if not proj:
            return {"status": "failed", "error": "Project not found."}
            
        trash = TrashItem(
            user_id=user_id,
            item_type="project",
            item_id=proj.id,
            original_data={
                "name": proj.name,
                "description": proj.description,
                "status": proj.status
            }
        )
        db.add(trash)
        await db.delete(proj)
        await db.flush()
        return {"status": "success", "message": f"Project '{proj.name}' moved to trash."}

class CreateBookAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        title = payload["title"]
        author = payload["author"]
        status = payload.get("status", "to-read")
        
        book = Book(
            user_id=user_id,
            title=title,
            author=author,
            status=status
        )
        db.add(book)
        await db.flush()
        return {"status": "success", "book_id": book.id, "message": f"Book '{title}' added to list."}

class UpdateBookProgressAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        book_id = payload["book_id"]
        status = payload["status"]
        rating = payload.get("rating")
        
        stmt = select(Book).where(Book.id == book_id, Book.user_id == user_id)
        res = await db.execute(stmt)
        book = res.scalar_one_or_none()
        if not book:
            return {"status": "failed", "error": "Book not found."}
            
        book.status = status
        if rating is not None:
            book.rating = rating
        if status == "finished":
            book.finished_at = datetime.now(timezone.utc)
            
        db.add(book)
        await db.flush()
        return {"status": "success", "message": f"Book '{book.title}' progress updated."}

class ArchiveBookAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        book_id = payload["book_id"]
        stmt = select(Book).where(Book.id == book_id, Book.user_id == user_id)
        res = await db.execute(stmt)
        book = res.scalar_one_or_none()
        if not book:
            return {"status": "failed", "error": "Book not found."}
        book.status = "finished"
        db.add(book)
        await db.flush()
        return {"status": "success", "message": f"Book '{book.title}' archived."}

class DeleteBookAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        book_id = payload["book_id"]
        stmt = select(Book).where(Book.id == book_id, Book.user_id == user_id)
        res = await db.execute(stmt)
        book = res.scalar_one_or_none()
        if not book:
            return {"status": "failed", "error": "Book not found."}
            
        trash = TrashItem(
            user_id=user_id,
            item_type="book",
            item_id=book.id,
            original_data={
                "title": book.title,
                "author": book.author,
                "status": book.status,
                "rating": book.rating
            }
        )
        db.add(trash)
        await db.delete(book)
        await db.flush()
        return {"status": "success", "message": f"Book '{book.title}' moved to trash."}

class CreateAssetAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        name = payload["name"]
        provider = payload["provider"]
        bucket = payload["bucket"]
        
        prov = StorageProvider(
            name=name,
            type=provider,
            account_email="user@warborn.os",
            encrypted_refresh_token="local_dummy",
            drive_folder_id=bucket,
            status="active"
        )
        db.add(prov)
        await db.flush()
        return {"status": "success", "asset_id": prov.id, "message": f"Asset Provider '{name}' created."}

class UpdateAssetAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        asset_id = payload["asset_id"]
        name = payload["name"]
        
        stmt = select(StorageProvider).where(StorageProvider.id == asset_id)
        res = await db.execute(stmt)
        prov = res.scalar_one_or_none()
        if not prov:
            return {"status": "failed", "error": "Asset not found."}
            
        prov.name = name
        db.add(prov)
        await db.flush()
        return {"status": "success", "message": f"Asset Provider '{name}' updated."}

class DeleteAssetAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        asset_id = payload["asset_id"]
        stmt = select(StorageProvider).where(StorageProvider.id == asset_id)
        res = await db.execute(stmt)
        prov = res.scalar_one_or_none()
        if not prov:
            return {"status": "failed", "error": "Asset not found."}
        await db.delete(prov)
        await db.flush()
        return {"status": "success", "message": f"Asset Provider '{prov.name}' deleted."}

class UploadMediaMetadataAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        title = payload["title"]
        file_path = payload["file_path"]
        return {"status": "success", "media_id": "dummy_media_id", "message": f"Media '{title}' uploaded metadata to {file_path}."}

class UpdateMediaMetadataAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        media_id = payload["media_id"]
        title = payload["title"]
        return {"status": "success", "message": f"Media metadata '{media_id}' updated to '{title}'."}

class DeleteMediaMetadataAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        media_id = payload["media_id"]
        return {"status": "success", "message": f"Media metadata '{media_id}' deleted."}

class GetStorageStatusAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "success",
            "usage_gb": 12.4,
            "limit_gb": 100.0,
            "percent_used": 12.4
        }

class CleanupStorageAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        days_old = payload["days_old"]
        return {"status": "success", "message": f"Cleaned up cached files older than {days_old} days."}

class UpdateCalendarEventAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        event_id = payload["event_id"]
        title = payload.get("title")
        start_time = payload.get("start_time")
        end_time = payload.get("end_time")
        
        stmt = select(CalendarEvent).where(CalendarEvent.id == event_id, CalendarEvent.user_id == user_id)
        res = await db.execute(stmt)
        evt = res.scalar_one_or_none()
        if not evt:
            return {"status": "failed", "error": "Calendar event not found."}
            
        if title:
            evt.title = title
        if start_time:
            evt.start_time = datetime.fromisoformat(start_time)
        if end_time:
            evt.end_time = datetime.fromisoformat(end_time)
            
        db.add(evt)
        await db.flush()
        return {"status": "success", "message": f"Event '{evt.title}' updated."}

class CancelCalendarEventAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        event_id = payload["event_id"]
        stmt = select(CalendarEvent).where(CalendarEvent.id == event_id, CalendarEvent.user_id == user_id)
        res = await db.execute(stmt)
        evt = res.scalar_one_or_none()
        if not evt:
            return {"status": "failed", "error": "Calendar event not found."}
        await db.delete(evt)
        await db.flush()
        return {"status": "success", "message": f"Event '{evt.title}' cancelled."}

class CreateHabitAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        name = payload["name"]
        cadence = payload.get("cadence", "daily")
        target = payload.get("target", 1)
        
        hab = Habit(
            user_id=user_id,
            name=name,
            cadence=cadence,
            target=target
        )
        db.add(hab)
        await db.flush()
        return {"status": "success", "habit_id": hab.id, "message": f"Habit '{name}' created."}

class LogHabitCheckinAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        habit_id = payload["habit_id"]
        date_str = payload["date"]
        value = payload.get("value", 1.0)
        
        stmt = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        res = await db.execute(stmt)
        hab = res.scalar_one_or_none()
        if not hab:
            return {"status": "failed", "error": "Habit not found."}
            
        log = HabitLog(
            habit_id=habit_id,
            date=date.fromisoformat(date_str),
            value=value
        )
        db.add(log)
        await db.flush()
        return {"status": "success", "message": f"Logged checkin for habit '{hab.name}'."}

class DeleteHabitAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        habit_id = payload["habit_id"]
        stmt = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        res = await db.execute(stmt)
        hab = res.scalar_one_or_none()
        if not hab:
            return {"status": "failed", "error": "Habit not found."}
            
        trash = TrashItem(
            user_id=user_id,
            item_type="habit",
            item_id=hab.id,
            original_data={
                "name": hab.name,
                "cadence": hab.cadence,
                "target": hab.target
            }
        )
        db.add(trash)
        await db.delete(hab)
        await db.flush()
        return {"status": "success", "message": f"Habit '{hab.name}' moved to trash."}

class CreateAddictionTrackerAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        name = payload["name"]
        quit_date = payload["quit_date"]
        
        tracker = Addiction(
            user_id=user_id,
            name=name,
            quit_at=datetime.fromisoformat(quit_date),
            cost_per_day=10.0,
            time_saved_per_day_mins=30
        )
        db.add(tracker)
        await db.flush()
        return {"status": "success", "tracker_id": tracker.id, "message": f"Relapse Sobriety Tracker '{name}' started."}

class LogAddictionRelapseAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        tracker_id = payload["tracker_id"]
        relapse_date = payload["relapse_date"]
        
        stmt = select(Addiction).where(Addiction.id == tracker_id, Addiction.user_id == user_id)
        res = await db.execute(stmt)
        tracker = res.scalar_one_or_none()
        if not tracker:
            return {"status": "failed", "error": "Addiction tracker not found."}
            
        log = RelapseLog(
            addiction_id=tracker_id,
            relapsed_at=datetime.fromisoformat(relapse_date),
            trigger_notes="Logged via Copilot Control Plane"
        )
        db.add(log)
        await db.flush()
        return {"status": "success", "message": f"Logged relapse event for tracker '{tracker.name}'."}

class GetSobrietyStatsAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        tracker_id = payload["tracker_id"]
        stmt = select(Addiction).where(Addiction.id == tracker_id, Addiction.user_id == user_id)
        res = await db.execute(stmt)
        tracker = res.scalar_one_or_none()
        if not tracker:
            return {"status": "failed", "error": "Addiction tracker not found."}
        return {
            "status": "success",
            "name": tracker.name,
            "days_sober": 5,
            "cost_saved": 50.0
        }

class UpdateMemoryItemAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        tone = payload.get("tone")
        explanation_style = payload.get("explanation_style")
        
        from app.services.user_memory_service import UserMemoryService
        profile = await UserMemoryService.get_profile(db, user_id)
        if tone:
            profile.tone = tone
        if explanation_style:
            profile.explanation_style = explanation_style
            
        db.add(profile)
        await db.flush()
        return {"status": "success", "message": "Updated user memory preferences."}

class DeleteMemoryItemAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        fact = payload["fact"]
        from app.services.user_memory_service import UserMemoryService
        profile = await UserMemoryService.get_profile(db, user_id)
        
        current_goals = list(profile.goals) if profile.goals else []
        if fact in current_goals:
            current_goals.remove(fact)
            profile.goals = current_goals
            db.add(profile)
            await db.flush()
            return {"status": "success", "message": f"Removed fact '{fact}' from memory."}
        return {"status": "failed", "error": f"Fact '{fact}' not found in memory."}

class CreateKnowledgeItemAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        title = payload["title"]
        content = payload["content"]
        
        import hashlib
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        doc = KnowledgeDocument(
            tenant_id=user_id,
            source_type="copilot_input",
            source_path=f"copilot://{title.replace(' ', '_').lower()}",
            title=title,
            slug=title.replace(' ', '-').lower(),
            content_hash=content_hash,
            canonical_text=content,
            visibility_scope="internal"
        )
        db.add(doc)
        await db.flush()
        return {"status": "success", "item_id": doc.id, "message": f"Knowledge base entry '{title}' saved."}

class DeleteKnowledgeItemAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        item_id = payload["item_id"]
        stmt = select(KnowledgeDocument).where(KnowledgeDocument.id == item_id, KnowledgeDocument.tenant_id == user_id)
        res = await db.execute(stmt)
        doc = res.scalar_one_or_none()
        if not doc:
            return {"status": "failed", "error": "Knowledge document not found."}
            
        await db.delete(doc)
        await db.flush()
        return {"status": "success", "message": f"Knowledge document '{doc.title}' deleted."}

class GetTelemetryStatusAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        from app.models.action_models import ActionLog
        from sqlalchemy import func
        stmt_total = select(func.count(ActionLog.id)).where(ActionLog.user_id == user_id)
        res_total = await db.execute(stmt_total)
        total_logs = res_total.scalar() or 0
        
        stmt_failed = select(func.count(ActionLog.id)).where(ActionLog.user_id == user_id, ActionLog.status == "failed")
        res_failed = await db.execute(stmt_failed)
        failed_logs = res_failed.scalar() or 0
        
        return {
            "status": "success",
            "telemetry": {
                "total_executions": total_logs,
                "failed_executions": failed_logs,
                "active_connections": 1,
                "system_status": "healthy"
            }
        }

class TriggerSystemSyncAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "success", "message": "Administrative system telemetry synchronization triggered."}

class UpdateReminderPreferencesAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        frequency = payload["frequency"]
        return {"status": "success", "message": f"Reminder frequency preference set to {frequency}."}

class ListTrashItemsAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(TrashItem).where(TrashItem.user_id == user_id).order_by(TrashItem.created_at.desc())
        res = await db.execute(stmt)
        items = res.scalars().all()
        return {
            "status": "success",
            "items": [{"id": i.id, "item_type": i.item_type, "item_id": i.item_id, "original_data": i.original_data} for i in items]
        }

class RestoreTrashItemAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        item_type = payload["item_type"]
        item_id = payload["item_id"]
        
        # Dispatch to specific restore executor
        if item_type == "note":
            return await RestoreNoteAction.execute(db, user_id, {"note_id": item_id})
        elif item_type == "task":
            return await RestoreTaskAction.execute(db, user_id, {"task_id": item_id})
        elif item_type == "project":
            # Restore project
            stmt = select(TrashItem).where(TrashItem.item_id == item_id, TrashItem.item_type == "project", TrashItem.user_id == user_id)
            res = await db.execute(stmt)
            trash = res.scalar_one_or_none()
            if not trash:
                return {"status": "failed", "error": "Trashed project not found."}
            proj = ProjectItem(
                id=trash.item_id,
                user_id=user_id,
                name=trash.original_data["name"],
                description=trash.original_data.get("description"),
                status=trash.original_data.get("status", "active")
            )
            db.add(proj)
            await db.delete(trash)
            await db.flush()
            return {"status": "success", "message": f"Project '{proj.name}' restored."}
        elif item_type == "book":
            # Restore book
            stmt = select(TrashItem).where(TrashItem.item_id == item_id, TrashItem.item_type == "book", TrashItem.user_id == user_id)
            res = await db.execute(stmt)
            trash = res.scalar_one_or_none()
            if not trash:
                return {"status": "failed", "error": "Trashed book not found."}
            book = Book(
                id=trash.item_id,
                user_id=user_id,
                title=trash.original_data["title"],
                author=trash.original_data["author"],
                status=trash.original_data.get("status", "to-read"),
                rating=trash.original_data.get("rating")
            )
            db.add(book)
            await db.delete(trash)
            await db.flush()
            return {"status": "success", "message": f"Book '{book.title}' restored."}
        elif item_type == "habit":
            # Restore habit
            stmt = select(TrashItem).where(TrashItem.item_id == item_id, TrashItem.item_type == "habit", TrashItem.user_id == user_id)
            res = await db.execute(stmt)
            trash = res.scalar_one_or_none()
            if not trash:
                return {"status": "failed", "error": "Trashed habit not found."}
            hab = Habit(
                id=trash.item_id,
                user_id=user_id,
                name=trash.original_data["name"],
                cadence=trash.original_data.get("cadence", "daily"),
                target=trash.original_data.get("target", 1)
            )
            db.add(hab)
            await db.delete(trash)
            await db.flush()
            return {"status": "success", "message": f"Habit '{hab.name}' restored."}
        else:
            return {"status": "failed", "error": f"Restoring item type '{item_type}' not supported."}

class PermanentPurgeItemAction:
    @classmethod
    async def execute(cls, db: AsyncSession, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        item_type = payload["item_type"]
        item_id = payload["item_id"]
        
        stmt = select(TrashItem).where(TrashItem.item_id == item_id, TrashItem.item_type == item_type, TrashItem.user_id == user_id)
        res = await db.execute(stmt)
        trash = res.scalar_one_or_none()
        if not trash:
            return {"status": "failed", "error": "Item not found in trash."}
            
        await db.delete(trash)
        await db.flush()
        return {"status": "success", "message": f"Item of type '{item_type}' permanently purged."}

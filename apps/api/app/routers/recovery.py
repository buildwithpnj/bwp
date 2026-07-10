from datetime import UTC, datetime
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from app.deps import DB, CurrentUser
from app.models.recovery import Addiction, RelapseLog

router = APIRouter(prefix="/api/recovery", tags=["Recovery & Addictions"])


class AddictionCreate(BaseModel):
    name: str
    quit_at: datetime
    cost_per_day: float = 0.0
    time_saved_per_day_mins: int = 0


class RelapseCreate(BaseModel):
    relapsed_at: datetime
    trigger_notes: str | None = None
    mood_rating: int | None = None


@router.get("/addictions")
async def list_addictions(current_user: CurrentUser, db: DB):
    result = await db.execute(
        select(Addiction)
        .where(Addiction.user_id == current_user.id)
        .order_by(Addiction.created_at.desc())
    )
    addictions = result.scalars().all()

    res = []
    for add in addictions:
        # Load relapses to calculate longest streak and history logs
        rel_res = await db.execute(
            select(RelapseLog)
            .where(RelapseLog.addiction_id == add.id)
            .order_by(RelapseLog.relapsed_at.desc())
        )
        relapses = rel_res.scalars().all()

        # Calculate current streak based on quit date or latest relapse
        anchor = add.quit_at
        if relapses:
            anchor = relapses[0].relapsed_at

        now = datetime.now(UTC)
        current_streak_sec = max(0.0, (now - anchor).total_seconds())
        current_streak_days = current_streak_sec / 86400.0

        # Saved metrics
        days_saved = current_streak_days
        money_saved = days_saved * float(add.cost_per_day)
        time_saved_hours = (days_saved * add.time_saved_per_day_mins) / 60.0

        res.append({
            "id": add.id,
            "name": add.name,
            "quit_at": add.quit_at.isoformat(),
            "cost_per_day": float(add.cost_per_day),
            "time_saved_per_day_mins": add.time_saved_per_day_mins,
            "current_streak_days": round(current_streak_days, 1),
            "money_saved": round(money_saved, 2),
            "time_saved_hours": round(time_saved_hours, 1),
            "relapse_count": len(relapses),
            "relapses": [
                {
                    "id": r.id,
                    "relapsed_at": r.relapsed_at.isoformat(),
                    "trigger_notes": r.trigger_notes,
                    "mood_rating": r.mood_rating,
                }
                for r in relapses
            ]
        })
    return res


@router.post("/addictions", status_code=status.HTTP_201_CREATED)
async def create_addiction(body: AddictionCreate, current_user: CurrentUser, db: DB):
    add = Addiction(
        user_id=current_user.id,
        name=body.name,
        quit_at=body.quit_at,
        cost_per_day=body.cost_per_day,
        time_saved_per_day_mins=body.time_saved_per_day_mins,
    )
    db.add(add)
    await db.flush()
    await db.refresh(add)
    return add


@router.post("/addictions/{addiction_id}/relapse")
async def log_relapse(addiction_id: str, body: RelapseCreate, current_user: CurrentUser, db: DB):
    result = await db.execute(
        select(Addiction).where(Addiction.id == addiction_id, Addiction.user_id == current_user.id)
    )
    add = result.scalar_one_or_none()
    if not add:
        raise HTTPException(status_code=404, detail="Addiction not found")

    relapse = RelapseLog(
        addiction_id=addiction_id,
        relapsed_at=body.relapsed_at,
        trigger_notes=body.trigger_notes,
        mood_rating=body.mood_rating,
    )
    db.add(relapse)
    await db.flush()
    return {"status": "success"}

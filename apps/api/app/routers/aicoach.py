from datetime import date, datetime, timedelta
from fastapi import APIRouter
from sqlalchemy import select

from app.deps import DB, CurrentUser
from app.models.calendar_event import CalendarEvent
from app.models.goals import Goal
from app.models.habits import Habit, HabitLog, JournalEntry
from app.models.recovery import Addiction

router = APIRouter(prefix="/api/aicoach", tags=["AI Coach"])


@router.get("/insights")
async def get_insights(current_user: CurrentUser, db: DB):
    # 1. Fetch habits count
    habits_result = await db.execute(
        select(Habit).where(Habit.user_id == current_user.id)
    )
    habits = habits_result.scalars().all()

    # 2. Fetch logged habits today
    today = date.today()
    log_result = await db.execute(
        select(HabitLog)
        .join(Habit)
        .where(Habit.user_id == current_user.id, HabitLog.date == today)
    )
    logs_today = log_result.scalars().all()

    # 3. Fetch active calendar events today
    cal_result = await db.execute(
        select(CalendarEvent)
        .where(CalendarEvent.user_id == current_user.id)
    )
    cal_events = cal_result.scalars().all()
    events_today = [
        e for e in cal_events 
        if e.start_time.date() == today
    ]

    # 4. Fetch goal metrics
    goals_result = await db.execute(
        select(Goal).where(Goal.user_id == current_user.id)
    )
    goals = goals_result.scalars().all()
    pinned_goals = [g for g in goals if g.pinned]

    # 5. Fetch addictions
    add_result = await db.execute(
        select(Addiction).where(Addiction.user_id == current_user.id)
    )
    addictions = add_result.scalars().all()

    # Construct the AI context message
    total_habits = len(habits)
    completed_today = len(logs_today)
    completion_rate = (completed_today / total_habits * 100) if total_habits > 0 else 0

    advice = []
    if completion_rate == 0:
        advice.append("You haven't checked off any habits today. Remember, starting is the hardest part. Just check off one task to build momentum!")
    elif completion_rate < 50:
        advice.append("Good start! Try aligning your evening routine habits to finish strong today.")
    else:
        advice.append("Incredible momentum! You have completed most of your targeted tasks today. Keep the streak active!")

    if events_today:
        advice.append(f"You have {len(events_today)} calendar events lined up today. Ensure you block out rest periods between them.")

    if pinned_goals:
        active_goal = pinned_goals[0]
        advice.append(f"Keep focused on your pinned goal: '{active_goal.title}' (currently at {active_goal.progress}% progress).")

    if addictions:
        advice.append("Your recovery tracks show clean streaks. If cravings trigger, access your emergency motivation toolbox.")

    content = " ".join(advice)
    if not content:
        content = "Welcome to Warborn OS. Create some habits or goals to receive tailored coaching reviews."

    return {
        "summary": "AI Companion Daily Report",
        "content": content,
        "completion_rate": round(completion_rate, 1),
        "total_habits": total_habits,
        "completed_today": completed_today,
    }

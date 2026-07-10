from datetime import UTC, datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pydantic import BaseModel
from sqlalchemy import select

from app.deps import DB, CurrentUser
from app.models.calendar_event import CalendarEvent
from app.models.gdrive import GoogleCredentials
from app.models.user import User

router = APIRouter(prefix="/api/gcalendar", tags=["Google Calendar"])


class CalendarEventCreate(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    timezone: str | None = "UTC"


class CalendarEventUpdate(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    timezone: str | None = "UTC"


async def get_calendar_service(user: User, db: DB):
    result = await db.execute(
        select(GoogleCredentials).where(GoogleCredentials.user_id == user.id)
    )
    db_creds = result.scalar_one_or_none()
    if not db_creds:
        return None

    creds = Credentials(
        token=db_creds.token,
        refresh_token=db_creds.refresh_token,
        token_uri=db_creds.token_uri,
        client_id=db_creds.client_id,
        client_secret=db_creds.client_secret,
        scopes=db_creds.scopes.split(","),
    )

    # Check if token is expired
    is_expired = creds.expired or (
        creds.expiry
        and creds.expiry.replace(tzinfo=None) < datetime.now(UTC).replace(tzinfo=None)
    )
    if is_expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            db_creds.token = creds.token
            db_creds.expiry = creds.expiry
            await db.commit()
        except Exception:
            # Silent fail for background sync
            pass

    try:
        return build("calendar", "v3", credentials=creds)
    except Exception:
        return None


@router.get("/events")
async def list_events(current_user: CurrentUser, db: DB):
    # Fetch local events
    result = await db.execute(
        select(CalendarEvent)
        .where(CalendarEvent.user_id == current_user.id)
        .order_by(CalendarEvent.start_time.asc())
    )
    local_events = result.scalars().all()

    # Sync from Google Calendar if connected
    service = await get_calendar_service(current_user, db)
    if service:
        try:
            # Fetch events from Google Calendar (last 30 days to next 30 days)
            now_iso = (datetime.now(UTC) - timedelta(days=30)).isoformat()
            g_events_result = service.events().list(
                calendarId='primary',
                timeMin=now_iso,
                maxResults=50,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            g_events = g_events_result.get('items', [])

            # Get local event ids that have google_event_ids
            existing_gids = {e.google_event_id: e for e in local_events if e.google_event_id}

            for ge in g_events:
                gid = ge.get('id')
                if not gid:
                    continue

                start = ge.get('start', {}).get('dateTime') or ge.get('start', {}).get('date')
                end = ge.get('end', {}).get('dateTime') or ge.get('end', {}).get('date')
                if not start or not end:
                    continue

                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))

                if gid in existing_gids:
                    # Update local event details if changed
                    ev = existing_gids[gid]
                    if ev.title != ge.get('summary', 'No Title'):
                        ev.title = ge.get('summary', 'No Title')
                        ev.description = ge.get('description', '')
                        ev.start_time = start_dt
                        ev.end_time = end_dt
                else:
                    # Insert new Google event locally
                    new_ev = CalendarEvent(
                        user_id=current_user.id,
                        google_event_id=gid,
                        title=ge.get('summary', 'No Title'),
                        description=ge.get('description', ''),
                        start_time=start_dt,
                        end_time=end_dt,
                        timezone=ge.get('start', {}).get('timeZone', 'UTC')
                    )
                    db.add(new_ev)

            await db.flush()

            # Refresh list
            result = await db.execute(
                select(CalendarEvent)
                .where(CalendarEvent.user_id == current_user.id)
                .order_by(CalendarEvent.start_time.asc())
            )
            local_events = result.scalars().all()
        except Exception as e:
            print(f"Failed to sync with Google Calendar: {str(e)}")

    return [
        {
            "id": e.id,
            "google_event_id": e.google_event_id,
            "title": e.title,
            "description": e.description,
            "start_time": e.start_time.isoformat(),
            "end_time": e.end_time.isoformat(),
            "timezone": e.timezone,
        }
        for e in local_events
    ]


@router.post("/events", status_code=status.HTTP_201_CREATED)
async def create_event(body: CalendarEventCreate, current_user: CurrentUser, db: DB):
    # Save local
    event = CalendarEvent(
        user_id=current_user.id,
        title=body.title,
        description=body.description,
        start_time=body.start_time,
        end_time=body.end_time,
        timezone=body.timezone or "UTC"
    )
    db.add(event)
    await db.flush()

    # Sync to Google Calendar
    service = await get_calendar_service(current_user, db)
    if service:
        try:
            g_body = {
                'summary': event.title,
                'description': event.description or '',
                'start': {
                    'dateTime': event.start_time.isoformat(),
                    'timeZone': event.timezone,
                },
                'end': {
                    'dateTime': event.end_time.isoformat(),
                    'timeZone': event.timezone,
                }
            }
            g_event = service.events().insert(calendarId='primary', body=g_body).execute()
            event.google_event_id = g_event.get('id')
            await db.flush()
        except Exception as e:
            print(f"Failed to push new event to Google: {str(e)}")

    await db.refresh(event)
    return event


@router.put("/events/{event_id}")
async def update_event(event_id: str, body: CalendarEventUpdate, current_user: CurrentUser, db: DB):
    result = await db.execute(
        select(CalendarEvent).where(CalendarEvent.id == event_id, CalendarEvent.user_id == current_user.id)
    )
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = body.title
    event.description = body.description
    event.start_time = body.start_time
    event.end_time = body.end_time
    event.timezone = body.timezone or "UTC"

    await db.flush()

    # Sync modification to Google Calendar
    if event.google_event_id:
        service = await get_calendar_service(current_user, db)
        if service:
            try:
                g_body = {
                    'summary': event.title,
                    'description': event.description or '',
                    'start': {
                        'dateTime': event.start_time.isoformat(),
                        'timeZone': event.timezone,
                    },
                    'end': {
                        'dateTime': event.end_time.isoformat(),
                        'timeZone': event.timezone,
                    }
                }
                service.events().patch(
                    calendarId='primary',
                    eventId=event.google_event_id,
                    body=g_body
                ).execute()
            except Exception as e:
                print(f"Failed to update event in Google Calendar: {str(e)}")

    return event


@router.delete("/events/{event_id}")
async def delete_event(event_id: str, current_user: CurrentUser, db: DB):
    result = await db.execute(
        select(CalendarEvent).where(CalendarEvent.id == event_id, CalendarEvent.user_id == current_user.id)
    )
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Delete on Google Calendar first
    if event.google_event_id:
        service = await get_calendar_service(current_user, db)
        if service:
            try:
                service.events().delete(
                    calendarId='primary',
                    eventId=event.google_event_id
                ).execute()
            except Exception as e:
                print(f"Failed to delete event from Google: {str(e)}")

    await db.delete(event)
    return {"status": "success"}

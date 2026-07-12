from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from app.repositories.preview_sessions import PreviewSessionsRepository
from app.repositories.preview_events import PreviewEventsRepository
from app.services.agent_english_service import AgentEnglishService

router = APIRouter(prefix="/api/public-preview", tags=["Public Preview"])

class SessionResponse(BaseModel):
    session_id: str

class MessageRequest(BaseModel):
    session_id: str
    message: str

class MessageResponse(BaseModel):
    message: str
    status: str

@router.post("/session", response_model=SessionResponse)
async def start_session(request: Request):
    ip_address = request.client.host if request.client else "unknown"
    session_id = PreviewSessionsRepository.create_session(ip_address)
    return SessionResponse(session_id=session_id)

@router.post("/respond", response_model=MessageResponse)
async def get_response(req: MessageRequest):
    session = PreviewSessionsRepository.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=400, detail="Invalid session token.")
        
    res = await AgentEnglishService.respond_to_preview(
        session_id=req.session_id, 
        message=req.message
    )
    
    PreviewEventsRepository.log_event(
        session_id=req.session_id,
        prompt=req.message,
        response=res["message"],
        tokens=res["tokens_used"],
        cost=res["cost"],
        status=res["status"]
    )
    
    return MessageResponse(
        message=res["message"],
        status=res["status"]
    )

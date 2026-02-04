import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from backend.api.dependencies import get_session_manager, get_current_user, get_project_service
from backend.services.session_manager import SessionManager
from backend.services.project_service import ProjectService
from backend.models.chat import ChatRequest, ChatResponse, SessionCreate, SessionResponse, SessionUpdate
from backend.core.messages import ErrorMessages

router = APIRouter()



@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    user_id: str = Depends(get_current_user),
    cbot: SessionManager = Depends(get_session_manager),
    project_service: ProjectService = Depends(get_project_service)
):
    """Create a new chat session for a project."""
    project = await project_service.get_project(session_data.project_id, user_id)
    if not project:
        raise HTTPException(status_code=404, detail=ErrorMessages.PROJECT_NOT_FOUND)

    session_id, _ = cbot.create_session(
        project_id=session_data.project_id,
        enable_db=True,
        chat_model = session_data.chat_model
    )
    
    return SessionResponse(
        id=session_id,
        project_id=session_data.project_id,
        title=session_data.title or "New Chat",
        chat_model = session_data.chat_model,
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )

@router.get("/", response_model=List[SessionResponse])
async def list_sessions(
    project_id: Optional[str] = None,
    user_id: str = Depends(get_current_user),
    cbot: SessionManager = Depends(get_session_manager)
):
    """List all sessions for the user, optionally filtered by project."""
    return cbot.get_user_sessions(project_id)


@router.post("/{session_id}/chat", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    user_id: str = Depends(get_current_user),
    cbot: SessionManager = Depends(get_session_manager),
    project_service: ProjectService = Depends(get_project_service)
):
    """Send a message to the bot."""

    chatbot = cbot.get_session(request.session_id)
    if not chatbot:
        raise HTTPException(status_code=404, detail=ErrorMessages.SESSION_NOT_FOUND)

    if chatbot.user_id and chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail=ErrorMessages.SESSION_UNAUTHORIZED)

    system_prompt = ""
    if chatbot.project_id:
        try:
            project = await project_service.get_project(chatbot.project_id, user_id)
            if project and project.system_prompt:
                system_prompt = project.system_prompt
                
        except Exception as e:
            raise ValueError(f"Error fetching project prompt: {e}")
    
    response = await chatbot.chat(request.message, system_prompt=system_prompt)
    return ChatResponse(response=response)


@router.post("/{session_id}/chat/stream")
async def chat_message_stream(
    request: ChatRequest,
    user_id: str = Depends(get_current_user),
    cbot: SessionManager = Depends(get_session_manager),
    project_service: ProjectService = Depends(get_project_service)
):
    """Stream chat response in real-time using Server-Sent Events."""
    chatbot = cbot.get_session(request.session_id)
    if not chatbot:
        raise HTTPException(status_code=404, detail=ErrorMessages.SESSION_NOT_FOUND)

    # Validate ownership
    if chatbot.user_id and chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail=ErrorMessages.SESSION_UNAUTHORIZED)

    system_prompt = ""
    if chatbot.project_id:
        try:
            project = await project_service.get_project(chatbot.project_id, user_id)
            if project and project.system_prompt:
                system_prompt = project.system_prompt
        except Exception as e:
            raise ValueError(f"Error fetching project prompt: {e}")

    async def generate():
        async for token in chatbot.chat_stream(request.message, system_prompt=system_prompt):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/{session_id}/history")
async def get_history(
    session_id: str,
    user_id: str = Depends(get_current_user),
    cbot: SessionManager = Depends(get_session_manager)
):
    """Get chat history."""
    chatbot = cbot.get_session(session_id)
    if not chatbot:
        raise HTTPException(status_code=404, detail=ErrorMessages.SESSION_NOT_FOUND)
        
    if chatbot.user_id and chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail=ErrorMessages.SESSION_UNAUTHORIZED)
            
    return cbot.get_session_history(session_id)

@router.patch("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    update_data: SessionUpdate,
    user_id: str = Depends(get_current_user),
    cbot: SessionManager = Depends(get_session_manager)
):
    """Update session title."""

    chatbot = cbot.get_session(session_id)
    if not chatbot:
        raise HTTPException(status_code=404, detail=ErrorMessages.SESSION_NOT_FOUND)
    if chatbot.user_id and chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail=ErrorMessages.SESSION_UNAUTHORIZED)
    
    result = cbot.update_session(session_id, update_data.title)
    if not result:
        raise HTTPException(status_code=500, detail=ErrorMessages.SESSION_UPDATE_FAILED)
    
    return result

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str,
    user_id: str = Depends(get_current_user),
    cbot: SessionManager = Depends(get_session_manager)
):
    """Delete a session."""

    # check ownership before deleting
    chatbot = cbot.get_session(session_id)
    if chatbot and chatbot.user_id and chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail=ErrorMessages.SESSION_UNAUTHORIZED)

    success = cbot.end_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail=ErrorMessages.SESSION_NOT_FOUND)
    return None
import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.dependencies import get_session_manager, get_current_user, get_project_service
from backend.services.session_manager import SessionManager
from backend.services.project_service import ProjectService
from backend.models.chat import ChatRequest, ChatResponse, SessionCreate, SessionResponse

router = APIRouter()



@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    user_id: str = Depends(get_current_user),
    cbot: SessionManager = Depends(get_session_manager),
    project_service: ProjectService = Depends(get_project_service)
):
    """Create a new chat session for a project."""
    # Verify project belongs to user
    project = await project_service.get_project(session_data.project_id, user_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    session_id, _ = cbot.create_session(
        user_id=user_id,
        project_id=session_data.project_id,
        enable_db=True,
        chat_model = session_data.chat_model
    )
    
    return SessionResponse(
        id=session_id,
        project_id=session_data.project_id,
        user_id=user_id,
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
    return cbot.get_user_sessions(user_id, project_id)


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
        raise HTTPException(status_code=404, detail="Session not found")

    # Validate ownership
    if chatbot.user_id and chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access to this session")

    system_prompt = ""
    if chatbot.project_id:
        try:
            project_id = chatbot.project_id[0] if isinstance(chatbot.project_id, tuple) else chatbot.project_id
            project = await project_service.get_project(project_id, user_id)

            if project and project.system_prompt:
                system_prompt = project.system_prompt
                
        except Exception as e:
            print(f"Error fetching project prompt: {e}")
    
    response = await chatbot.chat(request.message, system_prompt=system_prompt)
    return ChatResponse(response=response)


@router.get("/{session_id}/history")
async def get_history(
    session_id: str,
    user_id: str = Depends(get_current_user),
    cbot: SessionManager = Depends(get_session_manager)
):
    """Get chat history."""
    chatbot = cbot.get_session(session_id)
    if not chatbot:
        raise HTTPException(status_code=404, detail="Session not found")
        
    if chatbot.user_id and chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access to this session")
            
    # fetch from DB directly for full history
    if cbot.db:
        res = cbot.db.table("messages")\
            .select("*")\
            .eq("session_id", session_id)\
            .order("timestamp", desc=False)\
            .execute()
        return res.data if res.data else []
    
    return []

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
        raise HTTPException(status_code=403, detail="Unauthorized access to this session")

    success = cbot.end_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return None
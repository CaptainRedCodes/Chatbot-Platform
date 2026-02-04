from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from backend.api.dependencies import get_current_user, get_project_service
from backend.core.messages import ErrorMessages
from backend.models.project import ProjectCreate, ProjectResponse, ProjectUpdate
from backend.services.project_service import ProjectService
from backend.core.config import settings
router = APIRouter()



@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    user_id: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    
    """Create a project"""
    return await service.create_project(project_data, user_id)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    user_id: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """Fetch a single project by ID."""
    
    project = await service.get_project(project_id, user_id)
    
    if not project:
        raise HTTPException(status_code=404, detail=ErrorMessages.PROJECT_NOT_FOUND)
    
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    update_data: ProjectUpdate,
    user_id: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    
    result = await service.update_project(project_id, update_data, user_id)
    if not result:
        raise HTTPException(status_code=404, detail=ErrorMessages.PROJECT_NOT_FOUND)
    return result

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    user_id: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    success = await service.delete_project(project_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail=ErrorMessages.PROJECT_NOT_FOUND)
    return None

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    user_id: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    return await service.get_all_projects(user_id)

@router.get("/available-models")
async def get_available_models():
    """
    Returns the list of supported AI models.
    Frontend uses this to populate the dropdown menu.
    """
    return {"models": list(settings.FREE_MODELS)}
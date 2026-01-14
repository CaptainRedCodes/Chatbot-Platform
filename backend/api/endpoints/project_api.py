from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from backend.api.dependencies import get_current_user, get_project_service
from backend.models.project import ProjectCreate, ProjectResponse, ProjectUpdate
from backend.services.project_service import ProjectService

router = APIRouter()



@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    user_id: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    
    return await service.create_project(project_data, user_id)

@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    update_data: ProjectUpdate,
    user_id: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    
    result = await service.update_project(project_id, update_data, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found or unauthorized")
    return result

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    user_id: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    success = await service.delete_project(project_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found or unauthorized")
    return None

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    user_id: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    return await service.get_all_projects(user_id)
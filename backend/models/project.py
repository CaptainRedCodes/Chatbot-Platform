from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class ProjectCreate(BaseModel):
    project_name: str
    project_description: str
    # This is required for creating a project
    system_prompt: str = Field(..., description="The 'personality' or instructions for the AI")

class ProjectUpdate(BaseModel):
    project_name: str
    project_description: str
    system_prompt: str = Field(..., description="The 'personality' or instructions for the AI") 
    updated_at: datetime | None = None

class ProjectResponse(ProjectCreate):
    id: str
    user_id: str
    created_at: datetime
    
    # --- FIX START ---
    # We override the inherited field to make it optional for responses.
    # This allows the API to return success even if the DB field is null/missing.
    system_prompt: Optional[str] = None 
    # --- FIX END ---
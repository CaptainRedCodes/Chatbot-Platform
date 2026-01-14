from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class ProjectCreate(BaseModel):
    project_name:str
    project_description:str

class ProjectUpdate(BaseModel):
    project_name:str
    project_description:str
    updated_at:datetime

class ProjectResponse(ProjectCreate):
    id:str
    user_id:str
    created_at:datetime

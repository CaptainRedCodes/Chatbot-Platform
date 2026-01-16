from datetime import timezone
import datetime
import logging


from typing import List, Optional
from uuid import uuid4
from backend.core.supabase_client import get_supabase_client
from backend.models.project import ProjectCreate,ProjectResponse, ProjectUpdate
from backend.core.messages import SuccessMessages,ErrorMessages
logger = logging.getLogger(__name__)


class ProjectService:
    """Project or Agent Service"""

    def __init__(self):
        self.client = get_supabase_client()

    async def create_project(self,proj_data:ProjectCreate,user_id:str):
        try:
            created_at = datetime.datetime.now(timezone.utc)
            new_project = {
                "id":str(uuid4()),
                "user_id":user_id,
                "project_name":proj_data.project_name,
                "project_description":proj_data.project_description,
                "system_prompt": proj_data.system_prompt,
                "created_at": created_at.isoformat()
            }

            self.client.table('Projects').insert(new_project).execute()

            logger.info(SuccessMessages.PROJECT_CREATED)
            return ProjectResponse(
                id=new_project["id"],
                user_id=new_project["user_id"],
                project_name=new_project["project_name"],
                project_description=new_project["project_description"],
                system_prompt=new_project["system_prompt"],
                created_at=created_at,
            )
        
        except Exception as e:
            logger.error(f"Project Error:{e}")
            raise ValueError(f"{ErrorMessages.PROJECT_FAILED}:{e!s}")

    async def update_project(self,project_id:str,update_data:ProjectUpdate,user_id:str):
        try:
            update_payload = update_data.model_dump(exclude_unset=True)
            update_payload["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

            result = self.client.table('Projects')\
            .update(update_payload).eq('id',project_id)\
            .eq('user_id',user_id).execute()

            if not result.data:
                logger.error(ErrorMessages.PROJECT_UPDATE_FAILED)
                return None
            
            logger.info(SuccessMessages.PROJECT_UPDATED)

            return ProjectResponse(**result.data[0])
        except Exception as e:
            logger.error(f"Project Error:{e}")
            raise ValueError(f"{ErrorMessages.PROJECT_UPDATE_FAILED}:{e!s}")

    async def delete_project(self, project_id: str, user_id: str) -> bool:
        try:
            result = self.client.table('Projects') \
                .delete() \
                .eq('id', project_id) \
                .eq('user_id', user_id) \
                .execute()

            if not result.data:
                logger.error(ErrorMessages.PROJECT_DELETE_FAILED)
                return False

            logger.info(SuccessMessages.PROJECT_DELETED)
            return True

        except Exception as e:
            logger.error(f"Project Error:{e}")
            raise ValueError(f"{ErrorMessages.PROJECT_DELETE_FAILED}:{e!s}")
        
    async def get_all_projects(self, user_id: str) -> List[ProjectResponse]:
        try:
            result = self.client.table('Projects') \
                .select("*") \
                .eq('user_id', user_id) \
                .order('created_at', desc=True) \
                .execute()

            return [ProjectResponse(**item) for item in result.data]
        except Exception as e:
            logger.error(f"Failed to fetch projects: {e}")
            raise e

    async def get_project(self, project_id: str, user_id: str) -> Optional[ProjectResponse]:
        try:
            result = self.client.table('Projects') \
                .select("*") \
                .eq('id', project_id) \
                .eq('user_id', user_id) \
                .single() \
                .execute()
            
            if not result.data:
                return None
                
            return ProjectResponse(**result.data)
        except Exception as e:
            logger.error(f"Failed to fetch project: {e}")
            return None

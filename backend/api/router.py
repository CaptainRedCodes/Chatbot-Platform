from fastapi import APIRouter
from backend.api.endpoints import agent_api, auth_api, project_api

api_router = APIRouter()


api_router.include_router(auth_api.router, prefix="/auth", tags=["auth"])
api_router.include_router(project_api.router,prefix="/project",tags=["project"])
api_router.include_router(agent_api.router,prefix="/llm",tags=["llm"])
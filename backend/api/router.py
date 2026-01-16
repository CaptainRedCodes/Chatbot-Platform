from fastapi import APIRouter
from backend.api.endpoints import auth_api, project_api, session

api_router = APIRouter()


api_router.include_router(auth_api.router, prefix="/auth", tags=["auth"])
api_router.include_router(project_api.router, prefix="/project", tags=["project"])
api_router.include_router(session.router, prefix="/sessions", tags=["sessions"])
from fastapi import APIRouter

from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.feedback import router as feedback_router
from app.api.routes.generation import router as generation_router
from app.api.routes.job_analysis import router as job_analysis_router
from app.api.routes.library import router as library_router
from app.api.routes.mcp import router as mcp_router
from app.api.routes.profile import router as profile_router

api_router = APIRouter()
api_router.include_router(admin_router)
api_router.include_router(auth_router)
api_router.include_router(feedback_router)
api_router.include_router(generation_router)
api_router.include_router(job_analysis_router)
api_router.include_router(library_router)
api_router.include_router(mcp_router)
api_router.include_router(profile_router)

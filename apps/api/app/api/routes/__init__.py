from app.api.routes.auth import router as auth_router
from app.api.routes.cover_letter import router as cover_letter_router
from app.api.routes.profile import router as profile_router

__all__ = ["auth_router", "profile_router", "cover_letter_router"]

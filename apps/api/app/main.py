from fastapi import FastAPI

from app.api import auth_router, cover_letter_router, profile_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(cover_letter_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.APP_NAME, "env": settings.APP_ENV}

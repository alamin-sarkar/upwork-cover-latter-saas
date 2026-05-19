from fastapi import FastAPI

from app.api import auth_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)
app.include_router(auth_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.APP_NAME, "env": settings.APP_ENV}

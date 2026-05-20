from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import get_settings
from app.core.health import check_database, check_redis
from app.core.logging import configure_logging
from app.core.redis import close_redis_client

settings = get_settings()
logger = structlog.get_logger("app.request")


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield
    await close_redis_client()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.request_id = request_id
    started_at = perf_counter()
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "request.failed",
            duration_ms=round((perf_counter() - started_at) * 1000, 2),
        )
        structlog.contextvars.clear_contextvars()
        raise

    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request.completed",
        status_code=response.status_code,
        duration_ms=round((perf_counter() - started_at) * 1000, 2),
    )
    structlog.contextvars.clear_contextvars()
    return response


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


@app.get("/health/ready", tags=["system"])
async def readiness():
    database = await check_database()
    redis = await check_redis()
    healthy = database["ok"] and redis["ok"]
    payload = {
        "status": "ok" if healthy else "degraded",
        "service": settings.app_name,
        "version": settings.app_version,
        "dependencies": {
            "database": database,
            "redis": redis,
        },
    }
    if healthy:
        return payload
    return JSONResponse(status_code=503, content=payload)

from __future__ import annotations

import json
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.deps import CurrentUser, DbSession, get_db
from app.core.rate_limits import RateLimitAction, enforce_rate_limit
from app.core.security import (
    create_mcp_token,
    get_mcp_token_hash,
    get_mcp_token_prefix,
    verify_mcp_token,
)
from app.models.library import CoverLetterGuideline, CoverLetterSample
from app.models.mcp import McpApiToken
from app.models.profile import Profile
from app.models.user import User
from app.schemas.generation import CoverLetterGenerateRequest, CoverLetterGenerationResponse
from app.schemas.library import CoverLetterGuidelineOut, CoverLetterSampleOut
from app.schemas.mcp import McpTokenCreateRequest, McpTokenCreateResponse, McpTokenOut
from app.schemas.profile import ProfileDetailOut
from app.services.generation import GenerationNotFoundError, get_cover_letter_generation_service
from app.services.job_analysis import JobAnalysisConfigurationError

router = APIRouter(prefix="/mcp", tags=["mcp"])

MCP_PROTOCOL_VERSION = "2024-11-05"
MCP_SERVER_NAME = "upwork-cover-letter-mcp"
PROFILE_RESOURCE_URI = "pitchcraft://profile"
GUIDELINES_RESOURCE_URI = "pitchcraft://guidelines"
SAMPLES_RESOURCE_URI = "pitchcraft://samples"

_mcp_bearer = HTTPBearer(auto_error=False)
_settings = get_settings()
GenerationServiceFactory = Callable[[], Any]
get_mcp_generation_service: GenerationServiceFactory = get_cover_letter_generation_service


async def _get_current_mcp_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_mcp_bearer),
    session: AsyncSession = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing MCP token")

    raw_token = credentials.credentials
    stmt = (
        select(McpApiToken)
        .options(selectinload(McpApiToken.user))
        .where(
            McpApiToken.token_prefix == get_mcp_token_prefix(raw_token),
            McpApiToken.revoked_at.is_(None),
        )
    )
    candidates = list(await session.scalars(stmt))
    for candidate in candidates:
        if verify_mcp_token(raw_token, candidate.token_hash):
            if not candidate.user.is_active:
                break
            return candidate.user

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid MCP token")


@router.post(
    "/tokens",
    response_model=McpTokenCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_token(
    body: McpTokenCreateRequest,
    current_user: CurrentUser,
    session: DbSession,
) -> McpTokenCreateResponse:
    token = create_mcp_token()
    record = McpApiToken(
        user_id=current_user.id,
        label=body.label,
        token_prefix=get_mcp_token_prefix(token),
        token_hash=get_mcp_token_hash(token),
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return McpTokenCreateResponse(
        id=record.id,
        label=record.label,
        token_prefix=record.token_prefix,
        created_at=record.created_at,
        revoked_at=record.revoked_at,
        token=token,
    )


@router.get("/tokens", response_model=list[McpTokenOut])
async def list_tokens(current_user: CurrentUser, session: DbSession) -> list[McpApiToken]:
    stmt = (
        select(McpApiToken)
        .where(McpApiToken.user_id == current_user.id)
        .order_by(McpApiToken.created_at.desc())
    )
    return list(await session.scalars(stmt))


@router.delete("/tokens/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_token(
    token_id: uuid.UUID,
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    stmt = select(McpApiToken).where(
        McpApiToken.id == token_id,
        McpApiToken.user_id == current_user.id,
    )
    token = await session.scalar(stmt)
    if token is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCP token not found")
    if token.revoked_at is None:
        token.revoked_at = datetime.now(UTC)
        await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("")
async def handle_mcp_request(
    body: dict[str, Any],
    request: Request,
    current_user: User = Depends(_get_current_mcp_user),
    session: AsyncSession = Depends(get_db),
):
    request_id = body.get("id")
    if body.get("jsonrpc") != "2.0" or not isinstance(body.get("method"), str):
        return JSONResponse(_error_response(request_id, -32600, "Invalid Request"))

    method = body["method"]
    params = body.get("params")
    if params is None:
        params = {}
    if not isinstance(params, dict):
        return JSONResponse(_error_response(request_id, -32602, "Invalid params"))

    if method.startswith("notifications/"):
        return Response(status_code=status.HTTP_202_ACCEPTED)

    try:
        if method == "initialize":
            return JSONResponse(
                _result_response(
                    request_id,
                    {
                        "protocolVersion": MCP_PROTOCOL_VERSION,
                        "capabilities": {
                            "resources": {"listChanged": False},
                            "tools": {"listChanged": False},
                        },
                        "serverInfo": {
                            "name": MCP_SERVER_NAME,
                            "version": _settings.app_version,
                        },
                    },
                )
            )
        if method == "ping":
            return JSONResponse(_result_response(request_id, {}))
        if method == "resources/list":
            return JSONResponse(_result_response(request_id, {"resources": _resources_catalog()}))
        if method == "resources/read":
            content = await _read_resource_content(
                uri=str(params.get("uri", "")),
                current_user=current_user,
                session=session,
            )
            return JSONResponse(_result_response(request_id, {"contents": [content]}))
        if method == "tools/list":
            return JSONResponse(_result_response(request_id, {"tools": [_tool_definition()]}))
        if method == "tools/call":
            result = await _call_tool(
                name=str(params.get("name", "")),
                arguments=params.get("arguments"),
                current_user=current_user,
                session=session,
                request=request,
            )
            return JSONResponse(_result_response(request_id, result))
    except HTTPException as exc:
        message = exc.detail if isinstance(exc.detail, str) else "MCP request failed"
        return JSONResponse(
            _error_response(
                request_id,
                -32000,
                message,
                data={"status_code": exc.status_code},
            )
        )
    except ValidationError as exc:
        return JSONResponse(
            _error_response(request_id, -32602, "Invalid params", data=exc.errors())
        )

    return JSONResponse(_error_response(request_id, -32601, "Method not found"))


def _resources_catalog() -> list[dict[str, str]]:
    return [
        {
            "uri": PROFILE_RESOURCE_URI,
            "name": "Profile",
            "description": "Structured freelancer profile, preferences, and evidence.",
            "mimeType": "application/json",
        },
        {
            "uri": GUIDELINES_RESOURCE_URI,
            "name": "Guidelines",
            "description": "Saved cover-letter guidelines, intros, CTAs, and tone presets.",
            "mimeType": "application/json",
        },
        {
            "uri": SAMPLES_RESOURCE_URI,
            "name": "Samples",
            "description": "Saved winning and anti-pattern cover-letter samples.",
            "mimeType": "application/json",
        },
    ]


async def _read_resource_content(
    *,
    uri: str,
    current_user: User,
    session: AsyncSession,
) -> dict[str, str]:
    if uri == PROFILE_RESOURCE_URI:
        payload = await _profile_payload(session=session, user_id=current_user.id)
    elif uri == GUIDELINES_RESOURCE_URI:
        payload = await _guidelines_payload(session=session, user_id=current_user.id)
    elif uri == SAMPLES_RESOURCE_URI:
        payload = await _samples_payload(session=session, user_id=current_user.id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    return {
        "uri": uri,
        "mimeType": "application/json",
        "text": json.dumps(payload, ensure_ascii=True),
    }


async def _profile_payload(*, session: AsyncSession, user_id: uuid.UUID) -> dict[str, Any]:
    stmt = (
        select(Profile)
        .where(Profile.user_id == user_id)
        .options(
            selectinload(Profile.skills),
            selectinload(Profile.projects),
            selectinload(Profile.experiences),
            selectinload(Profile.niches),
            selectinload(Profile.custom_sections),
            selectinload(Profile.preferences),
        )
    )
    profile = await session.scalar(stmt)
    if profile is None:
        return {"profile": None, "message": "No structured profile is configured yet."}
    return {"profile": ProfileDetailOut.model_validate(profile).model_dump(mode="json")}


async def _guidelines_payload(*, session: AsyncSession, user_id: uuid.UUID) -> dict[str, Any]:
    stmt = (
        select(CoverLetterGuideline)
        .where(CoverLetterGuideline.user_id == user_id)
        .order_by(CoverLetterGuideline.sort_order.asc(), CoverLetterGuideline.created_at.asc())
    )
    guidelines = list(await session.scalars(stmt))
    return {
        "guidelines": [
            CoverLetterGuidelineOut.model_validate(item).model_dump(mode="json")
            for item in guidelines
        ]
    }


async def _samples_payload(*, session: AsyncSession, user_id: uuid.UUID) -> dict[str, Any]:
    stmt = (
        select(CoverLetterSample)
        .where(CoverLetterSample.user_id == user_id)
        .order_by(CoverLetterSample.sort_order.asc(), CoverLetterSample.created_at.asc())
    )
    samples = list(await session.scalars(stmt))
    return {
        "samples": [
            CoverLetterSampleOut.model_validate(item).model_dump(mode="json")
            for item in samples
        ]
    }


def _tool_definition() -> dict[str, Any]:
    return {
        "name": "generate_cover_letter",
        "description": "Generate multiple personalized Upwork cover-letter variants.",
        "inputSchema": CoverLetterGenerateRequest.model_json_schema(),
    }


async def _call_tool(
    *,
    name: str,
    arguments: Any,
    current_user: User,
    session: AsyncSession,
    request: Request | None = None,
) -> dict[str, Any]:
    if name != "generate_cover_letter":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    if arguments is None:
        arguments = {}
    if not isinstance(arguments, dict):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tool arguments must be an object",
        )

    body = CoverLetterGenerateRequest.model_validate(arguments)
    rate_limit_response = Response()
    await enforce_rate_limit(
        user=current_user,
        action=RateLimitAction.generation,
        response=rate_limit_response,
    )
    try:
        service = get_mcp_generation_service()
    except JobAnalysisConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cover letter generation provider is not configured",
        ) from exc

    try:
        run = await service.generate_cover_letters(
            user_id=current_user.id,
            session=session,
            raw_job_text=body.raw_job_text,
            analysis_snapshot_id=body.analysis_snapshot_id,
            structures=body.structures,
        )
    except GenerationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    response = CoverLetterGenerationResponse.model_validate(
        {
            "id": run.id,
            "analysis_snapshot_id": run.analysis_snapshot_id,
            "raw_job_text": run.raw_job_text,
            "prompt_version": run.prompt_version,
            "requested_structures": run.requested_structures,
            "analysis": run.analysis_snapshot.analysis_payload,
            "variants": run.variants,
            "created_at": run.created_at,
        }
    ).model_dump(mode="json")
    return {
        "content": [{"type": "text", "text": json.dumps(response, ensure_ascii=True)}],
        "structuredContent": response,
        "meta": {
            "request_id": getattr(request.state, "request_id", None) if request is not None else None,
            "rate_limit": dict(rate_limit_response.headers),
        },
        "isError": False,
    }


def _result_response(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error_response(
    request_id: Any,
    code: int,
    message: str,
    *,
    data: Any | None = None,
) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": error}

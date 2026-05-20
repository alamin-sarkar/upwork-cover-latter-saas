import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class McpTokenCreateRequest(BaseModel):
    label: str = Field(min_length=1, max_length=120)


class McpTokenOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    label: str
    token_prefix: str
    created_at: datetime
    revoked_at: datetime | None


class McpTokenCreateResponse(McpTokenOut):
    token: str

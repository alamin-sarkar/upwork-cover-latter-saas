from pydantic import BaseModel

from app.schemas.user import UserRead


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    user: UserRead
    tokens: TokenPair


class RefreshTokenRequest(BaseModel):
    refresh_token: str

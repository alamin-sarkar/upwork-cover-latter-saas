import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt as _bcrypt
from jose import jwt

from app.core.config import get_settings


# ---------------------------------------------------------------------------
# Password helpers  (bcrypt 4+ direct — passlib 1.7 is incompatible with it)
# ---------------------------------------------------------------------------


def hash_password(plain: str) -> str:
    return _bcrypt.hashpw(plain.encode(), _bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return _bcrypt.checkpw(plain.encode(), hashed.encode())


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------


def _now() -> datetime:
    return datetime.now(UTC)


def create_access_token(
    subject: str | int,
    extra_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    settings = get_settings()
    expire = _now() + (
        expires_delta or timedelta(minutes=settings.access_token_expires_minutes)
    )
    payload: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": _now(),
        "type": "access",
        **(extra_claims or {}),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str | int) -> str:
    settings = get_settings()
    expire = _now() + timedelta(days=settings.refresh_token_expires_days)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": _now(),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT. Raises JWTError on failure."""
    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])


def create_mcp_token() -> str:
    return f"mcp_{secrets.token_urlsafe(32)}"


def get_mcp_token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def get_mcp_token_prefix(token: str) -> str:
    return token[:24]


def verify_mcp_token(token: str, token_hash: str) -> bool:
    return hmac.compare_digest(get_mcp_token_hash(token), token_hash)

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db

# Convenience type alias — use as: `session: DbSession` in route params.
DbSession = Annotated[AsyncSession, Depends(get_db)]

# CurrentUser will be added in Phase 3 once the User model exists.

from functools import lru_cache
from typing import Any, Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings sourced from environment variables / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "Upwork Cover Letter API"
    app_version: str = "0.1.0"
    environment: Literal["development", "staging", "production", "test"] = "development"
    docs_enabled: bool = True
    log_level: str = "INFO"
    log_json: bool = True
    admin_diagnostics_token: str | None = None

    # Database
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/cover_letter"

    # Redis / Celery
    redis_url: str = "redis://localhost:6379/0"
    celery_result_backend: str | None = None
    celery_task_always_eager: bool = False
    celery_default_queue: str = "cover-letter-jobs"

    # Auth
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 30
    refresh_token_expires_days: int = 14

    # CORS
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    # AI providers
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-6"

    # Rate limits (per UTC day)
    rate_limit_window_seconds: int = 86400
    job_analysis_daily_limits: dict[str, int] = Field(
        default_factory=lambda: {"free": 25, "pro": 250, "team": 1000}
    )
    generation_daily_limits: dict[str, int] = Field(
        default_factory=lambda: {"free": 10, "pro": 100, "team": 500}
    )

    @model_validator(mode="after")
    def validate_runtime_guards(self) -> "Settings":
        if self.rate_limit_window_seconds <= 0:
            raise ValueError("RATE_LIMIT_WINDOW_SECONDS must be positive")

        for plan_key in ("free", "pro", "team"):
            if plan_key not in self.job_analysis_daily_limits:
                raise ValueError(f"JOB_ANALYSIS_DAILY_LIMITS missing {plan_key!r}")
            if plan_key not in self.generation_daily_limits:
                raise ValueError(f"GENERATION_DAILY_LIMITS missing {plan_key!r}")

        if self.environment == "production":
            if self.jwt_secret == "change-me-in-production" or len(self.jwt_secret) < 32:
                raise ValueError(
                    "JWT_SECRET must be replaced with a production secret of at least 32 characters"
                )
            if not self.admin_diagnostics_token or len(self.admin_diagnostics_token) < 16:
                raise ValueError(
                    "ADMIN_DIAGNOSTICS_TOKEN must be set to at least 16 characters in production"
                )
            if self.docs_enabled:
                raise ValueError("DOCS_ENABLED must be false in production")

        return self

    def plan_limit_for(self, limits: dict[str, int], plan: Any) -> int:
        plan_key = getattr(plan, "value", plan)
        if plan_key not in limits:
            raise KeyError(f"Unknown plan {plan_key!r}")
        return limits[plan_key]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

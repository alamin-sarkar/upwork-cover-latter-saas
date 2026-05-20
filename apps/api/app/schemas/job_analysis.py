import uuid
from datetime import datetime

from ai_workflows.job_analysis.schemas import JobAnalysis
from pydantic import BaseModel, Field


class JobAnalysisRequest(BaseModel):
    raw_job_text: str = Field(min_length=20, max_length=50000)


class JobAnalysisResponse(JobAnalysis):
    id: uuid.UUID
    raw_job_text: str
    provider: str
    model_name: str
    prompt_version: str
    created_at: datetime

    model_config = {"from_attributes": True}

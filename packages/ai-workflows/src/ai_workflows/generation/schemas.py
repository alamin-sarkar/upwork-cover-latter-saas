from enum import StrEnum

from pydantic import BaseModel, Field


class CoverLetterStructure(StrEnum):
    concise = "concise"
    problem_solution = "problem-solution"
    credibility_first = "credibility-first"
    portfolio_first = "portfolio-first"
    consultative = "consultative"


class DraftedCoverLetter(BaseModel):
    structure: CoverLetterStructure
    headline: str = Field(min_length=1, max_length=160)
    cover_letter: str = Field(min_length=40)
    rationale: str = Field(min_length=1)
    match_notes: list[str] = Field(default_factory=list)


class CoverLetterReviewResult(BaseModel):
    structure: CoverLetterStructure
    final_headline: str = Field(min_length=1, max_length=160)
    final_cover_letter: str = Field(min_length=40)
    final_rationale: str = Field(min_length=1)
    final_match_notes: list[str] = Field(default_factory=list)
    self_check_notes: list[str] = Field(default_factory=list)


class FinalCoverLetterVariant(BaseModel):
    structure: CoverLetterStructure
    headline: str = Field(min_length=1, max_length=160)
    cover_letter: str = Field(min_length=40)
    rationale: str = Field(min_length=1)
    match_notes: list[str] = Field(default_factory=list)
    self_check_notes: list[str] = Field(default_factory=list)

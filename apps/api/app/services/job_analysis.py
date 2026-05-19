from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class JobAnalysisResult:
    required_skills: list[str]
    deliverables: list[str]
    urgency: str
    budget_clue: str
    risk_flags: list[str]
    fit_score: int
    evidence: list[str]
    summary: str


def _contains_any(text: str, words: list[str]) -> bool:
    return any(w in text for w in words)


def analyze_job_post(*, title: str, raw_text: str, headline: str, guideline_text: str, profile_skills: list[str]) -> JobAnalysisResult:
    t = raw_text.lower()
    title_l = title.lower()

    canonical_skills = [
        "fastapi", "next.js", "nextjs", "postgresql", "langchain", "langgraph", "python", "redis", "docker", "aws", "react", "typescript"
    ]
    required = [s for s in canonical_skills if s in t or s in title_l]

    deliverables = []
    for kw in ["build", "develop", "integrate", "automate", "deploy", "optimize"]:
        if kw in t:
            deliverables.append(kw)

    if _contains_any(t, ["urgent", "asap", "immediately", "today"]):
        urgency = "high"
    elif _contains_any(t, ["this week", "soon"]):
        urgency = "medium"
    else:
        urgency = "normal"

    budget_match = re.search(r"\$\s?\d+[\d,]*(?:\s?-\s?\$?\d+[\d,]*)?", raw_text)
    budget_clue = budget_match.group(0) if budget_match else "not-specified"

    risk_flags = []
    if _contains_any(t, ["cheap", "lowest bid", "budget is tight"]):
        risk_flags.append("price-pressure")
    if _contains_any(t, ["trial", "free sample", "unpaid"]):
        risk_flags.append("unpaid-work-risk")
    if _contains_any(t, ["many skills", "full stack expert in everything", "all-in-one"]):
        risk_flags.append("scope-overload")

    skill_blob = " ".join(profile_skills).lower()
    matched_profile_skills = [s for s in required if s.replace(".", "") in skill_blob.replace(".", "")]
    fit_score = max(30, min(98, 40 + len(matched_profile_skills) * 12 - len(risk_flags) * 8))

    evidence = [f"matched-skill:{s}" for s in matched_profile_skills]
    if headline:
        evidence.append(f"headline:{headline[:60]}")
    if guideline_text:
        evidence.append("guidelines-applied")

    summary = (
        f"Job needs {', '.join(required[:5]) or 'general development'}. "
        f"Urgency: {urgency}. Budget: {budget_clue}. "
        f"Fit score: {fit_score}/100. "
        f"Risk flags: {', '.join(risk_flags) if risk_flags else 'none'}."
    )

    return JobAnalysisResult(
        required_skills=required,
        deliverables=sorted(set(deliverables)),
        urgency=urgency,
        budget_clue=budget_clue,
        risk_flags=risk_flags,
        fit_score=fit_score,
        evidence=evidence,
        summary=summary,
    )

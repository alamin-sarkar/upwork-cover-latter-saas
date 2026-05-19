import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models import CoverLetterFeedback, CoverLetterGeneration, CoverLetterJobPost, Profile, ProfileGuideline, ProfileSample, User
from app.services.cover_letter_graph import run_cover_letter_graph
from app.services.job_analysis import analyze_job_post
from app.schemas.cover_letter import (
    CoverLetterFeedbackCreate,
    CoverLetterFeedbackRead,
    CoverLetterMemorySignalRead,
    CoverLetterVariantRead,
    GenerateCoverLetterRequest,
    JobAnalysisRead,
    JobPostCreate,
    JobPostRead,
)

router = APIRouter(prefix="/api/v1/cover-letter", tags=["cover-letter"])


@router.post("/job-posts", response_model=JobPostRead, status_code=status.HTTP_201_CREATED)
def create_job_post(payload: JobPostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = CoverLetterJobPost(user_id=current_user.id, title=payload.title.strip(), raw_text=payload.raw_text, source=payload.source)
    db.add(row)
    db.commit()
    db.refresh(row)
    return JobPostRead.model_validate(row)


@router.get("/job-posts", response_model=list[JobPostRead])
def list_job_posts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(CoverLetterJobPost).where(CoverLetterJobPost.user_id == current_user.id).order_by(CoverLetterJobPost.created_at.desc())).all()
    return [JobPostRead.model_validate(x) for x in rows]


@router.post("/job-posts/{job_post_id}/analyze", response_model=JobAnalysisRead)
def analyze_job_post_endpoint(job_post_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = db.scalar(select(CoverLetterJobPost).where(CoverLetterJobPost.id == job_post_id, CoverLetterJobPost.user_id == current_user.id))
    if not job:
        raise HTTPException(status_code=404, detail="Job post not found")

    profile = db.scalar(select(Profile).where(Profile.user_id == current_user.id))
    headline = profile.headline if profile else "Freelancer"
    guidelines = db.scalars(select(ProfileGuideline).where(ProfileGuideline.profile_id == profile.id).order_by(ProfileGuideline.priority.asc())).all() if profile else []
    skills = [x.name for x in getattr(profile, "skills", [])] if profile else []
    guideline_text = "; ".join([g.title for g in guidelines[:3]]) or "Be concise and value-focused"

    result = analyze_job_post(
        title=job.title,
        raw_text=job.raw_text,
        headline=headline,
        guideline_text=guideline_text,
        profile_skills=skills,
    )
    job.analysis_snapshot = {
        "required_skills": result.required_skills,
        "deliverables": result.deliverables,
        "urgency": result.urgency,
        "budget_clue": result.budget_clue,
        "risk_flags": result.risk_flags,
        "evidence": result.evidence,
        "summary": result.summary,
    }
    job.fit_score = result.fit_score
    db.add(job)
    db.commit()

    return JobAnalysisRead(
        required_skills=result.required_skills,
        deliverables=result.deliverables,
        urgency=result.urgency,
        budget_clue=result.budget_clue,
        risk_flags=result.risk_flags,
        fit_score=result.fit_score,
        evidence=result.evidence,
        summary=result.summary,
    )


@router.post("/generate", response_model=list[CoverLetterVariantRead])
def generate_cover_letters(payload: GenerateCoverLetterRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = db.scalar(select(CoverLetterJobPost).where(CoverLetterJobPost.id == payload.job_post_id, CoverLetterJobPost.user_id == current_user.id))
    if not job:
        raise HTTPException(status_code=404, detail="Job post not found")

    profile = db.scalar(select(Profile).where(Profile.user_id == current_user.id))
    headline = profile.headline if profile else "Freelancer"

    guidelines = db.scalars(select(ProfileGuideline).where(ProfileGuideline.profile_id == profile.id).order_by(ProfileGuideline.priority.asc())).all() if profile else []
    samples = db.scalars(select(ProfileSample).where(ProfileSample.profile_id == profile.id).order_by(ProfileSample.created_at.desc())).all() if profile else []

    guideline_text = "; ".join([g.title for g in guidelines[:3]]) or "Be concise and value-focused"
    sample_hint = samples[0].tone if samples else "professional"

    recent_feedback = db.scalars(
        select(CoverLetterFeedback)
        .where(CoverLetterFeedback.user_id == current_user.id)
        .order_by(CoverLetterFeedback.created_at.desc())
        .limit(10)
    ).all()
    preference_note = ""
    if recent_feedback:
        avg_rating = sum(x.rating for x in recent_feedback) / len(recent_feedback)
        if avg_rating >= 4:
            preference_note = "User feedback trend: keep current style."
        else:
            preference_note = "User feedback trend: make letters more specific and concise."

    profile_skills = [x.name for x in getattr(profile, "skills", [])] if profile else []
    analyzed = analyze_job_post(
        title=job.title,
        raw_text=job.raw_text,
        headline=headline,
        guideline_text=guideline_text,
        profile_skills=profile_skills,
    )
    job.analysis_snapshot = {
        "required_skills": analyzed.required_skills,
        "deliverables": analyzed.deliverables,
        "urgency": analyzed.urgency,
        "budget_clue": analyzed.budget_clue,
        "risk_flags": analyzed.risk_flags,
        "evidence": analyzed.evidence,
        "summary": analyzed.summary,
    }
    job.fit_score = analyzed.fit_score

    structures = ["direct-value", "problem-solution", "story-proof"]

    out = []
    for structure in structures:
        graph_result = run_cover_letter_graph(
            job_title=job.title,
            raw_text=job.raw_text,
            headline=headline,
            guideline_text=guideline_text,
            tone_hint=sample_hint,
            preference_note=f"{preference_note} Fit: {analyzed.fit_score}/100. Risks: {', '.join(analyzed.risk_flags) if analyzed.risk_flags else 'none'}.",
            structure=structure,
        )
        row = CoverLetterGeneration(
            user_id=current_user.id,
            job_post_id=job.id,
            structure=structure,
            analysis_summary=graph_result["analysis_summary"],
            draft_text=graph_result["draft_text"],
        )
        db.add(row)
        out.append(row)

    db.commit()
    for row in out:
        db.refresh(row)
    return [CoverLetterVariantRead.model_validate(x) for x in out]


@router.get("/history", response_model=list[CoverLetterVariantRead])
def list_generation_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(CoverLetterGeneration).where(CoverLetterGeneration.user_id == current_user.id).order_by(CoverLetterGeneration.created_at.desc())).all()
    return [CoverLetterVariantRead.model_validate(x) for x in rows]


@router.post("/feedback", response_model=CoverLetterFeedbackRead, status_code=status.HTTP_201_CREATED)
def submit_feedback(payload: CoverLetterFeedbackCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    generation = db.scalar(
        select(CoverLetterGeneration).where(
            CoverLetterGeneration.id == payload.generation_id,
            CoverLetterGeneration.user_id == current_user.id,
        )
    )
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")

    row = CoverLetterFeedback(
        user_id=current_user.id,
        generation_id=generation.id,
        rating=payload.rating,
        feedback_text=payload.feedback_text,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return CoverLetterFeedbackRead.model_validate(row)


@router.get("/memory-signal", response_model=CoverLetterMemorySignalRead)
def get_memory_signal(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(
        select(CoverLetterFeedback)
        .where(CoverLetterFeedback.user_id == current_user.id)
        .order_by(CoverLetterFeedback.created_at.desc())
        .limit(20)
    ).all()
    if not rows:
        return CoverLetterMemorySignalRead(avg_rating=None, preferred_tone=None, do_more=[], avoid=[])

    avg_rating = sum(x.rating for x in rows) / len(rows)
    preferred_tone = "professional" if avg_rating >= 4 else "concise"

    text_blob = " ".join([(x.feedback_text or "").lower() for x in rows])
    do_more = []
    avoid = []
    if "specific" in text_blob or "specifics" in text_blob:
        do_more.append("more-specific-outcomes")
    if "short" in text_blob or "concise" in text_blob:
        do_more.append("shorter-letters")
    if "generic" in text_blob:
        avoid.append("generic-lines")

    return CoverLetterMemorySignalRead(avg_rating=avg_rating, preferred_tone=preferred_tone, do_more=do_more, avoid=avoid)

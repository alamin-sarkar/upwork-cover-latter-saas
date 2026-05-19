from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models import CoverLetterGeneration, CoverLetterJobPost, Profile, ProfileGuideline, ProfileSample, User
from app.schemas.cover_letter import CoverLetterVariantRead, GenerateCoverLetterRequest, JobPostCreate, JobPostRead

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

    variants = [
        ("direct-value", f"Analyze: {job.title}. Priorities: {guideline_text}", f"Hi, I noticed your {job.title} project. I'm {headline} and can deliver quickly with clear milestones."),
        ("problem-solution", f"Analyze: {job.title}. Priorities: {guideline_text}", f"Your requirement suggests immediate execution needs. As {headline}, I can design and ship a reliable solution end-to-end."),
        ("story-proof", f"Analyze: {job.title}. Priorities: {guideline_text}", f"I recently completed a similar project with measurable impact. For your {job.title}, I can provide the same outcome with transparent communication."),
    ]

    out = []
    for structure, analysis_summary, draft_text in variants:
        row = CoverLetterGeneration(
            user_id=current_user.id,
            job_post_id=job.id,
            structure=structure,
            analysis_summary=f"{analysis_summary}. Tone hint: {sample_hint}",
            draft_text=draft_text,
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

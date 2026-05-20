from ai_workflows.generation.schemas import CoverLetterStructure
from ai_workflows.job_analysis.schemas import JobAnalysis
from langchain_core.prompts import ChatPromptTemplate

COVER_LETTER_GENERATION_PROMPT_VERSION = "2026-05-20.phase-7.v1"
COVER_LETTER_REVIEW_PROMPT_VERSION = "2026-05-20.phase-7.review-v1"

STRUCTURE_GUIDANCE: dict[CoverLetterStructure, str] = {
    CoverLetterStructure.concise: (
        "Keep the letter tight and efficient. Lead with direct fit, show 2-3 proofs, and close fast."
    ),
    CoverLetterStructure.problem_solution: (
        "Frame the client problem clearly, then position your approach and evidence as the solution."
    ),
    CoverLetterStructure.credibility_first: (
        "Open with credibility signals, then tie those signals to the client's scope and risks."
    ),
    CoverLetterStructure.portfolio_first: (
        "Lead with relevant project evidence, then connect that work to the requested deliverables."
    ),
    CoverLetterStructure.consultative: (
        "Sound like a senior advisor: diagnose the situation, suggest a plan, and ask a sharp CTA question."
    ),
}


def build_cover_letter_draft_prompt(
    *,
    structure: CoverLetterStructure,
    job_analysis: JobAnalysis,
    profile_context: str,
    library_context: str,
) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You write Upwork cover letters for a senior freelancer. "
                    "Return structured output only. Avoid generic enthusiasm, filler, and unsupported claims."
                ),
            ),
            (
                "human",
                (
                    "Draft one personalized cover-letter variant.\n\n"
                    "Structure style:\n{structure_guidance}\n\n"
                    "Job analysis:\n{job_analysis}\n\n"
                    "Profile evidence:\n{profile_context}\n\n"
                    "Guidelines and sample context:\n{library_context}\n\n"
                    "Requirements:\n"
                    "- Keep the structure exactly aligned to the requested style.\n"
                    "- Make the body specific to this job.\n"
                    "- Use only profile evidence that is actually supplied.\n"
                    "- Include concise match notes that explain why this variant fits."
                ),
            ),
        ]
    ).partial(
        structure_guidance=STRUCTURE_GUIDANCE[structure],
        job_analysis=job_analysis.model_dump_json(indent=2),
        profile_context=profile_context,
        library_context=library_context,
    )


def build_cover_letter_review_prompt(
    *,
    drafted_variant_json: str,
    job_analysis: JobAnalysis,
    profile_context: str,
    library_context: str,
) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are the self-check stage of a cover-letter agent. "
                    "Review the draft for specificity, accuracy, and structural alignment. "
                    "Return structured output only."
                ),
            ),
            (
                "human",
                (
                    "Review and improve this drafted cover-letter variant.\n\n"
                    "Drafted variant:\n{drafted_variant_json}\n\n"
                    "Job analysis:\n{job_analysis}\n\n"
                    "Profile evidence:\n{profile_context}\n\n"
                    "Guidelines and sample context:\n{library_context}\n\n"
                    "Requirements:\n"
                    "- Keep the same requested structure.\n"
                    "- Remove vague claims.\n"
                    "- Tighten the CTA if needed.\n"
                    "- Return short self-check notes describing the fixes you made."
                ),
            ),
        ]
    ).partial(
        drafted_variant_json=drafted_variant_json,
        job_analysis=job_analysis.model_dump_json(indent=2),
        profile_context=profile_context,
        library_context=library_context,
    )

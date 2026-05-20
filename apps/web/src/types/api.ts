export type Plan = "free" | "pro" | "team";

export type User = {
  id: string;
  email: string;
  full_name: string | null;
  plan: Plan;
  is_active: boolean;
  created_at: string;
};

export type TokenResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};

export type Profile = {
  id: string;
  user_id: string;
  professional_title: string | null;
  location: string | null;
  hourly_rate_usd: number | null;
  about: string | null;
  availability_note: string | null;
  created_at: string;
  updated_at: string;
};

export type ProfileSkill = {
  id: string;
  name: string;
  level: string | null;
  years_of_experience: number | null;
  proof: string | null;
  sort_order: number;
  created_at: string;
  updated_at: string;
};

export type ProfileProject = {
  id: string;
  title: string;
  role: string | null;
  tagline: string | null;
  description: string;
  outcome: string | null;
  link: string | null;
  stack: string[];
  evidence_points: string[];
  sort_order: number;
  created_at: string;
  updated_at: string;
};

export type ProfilePreferences = {
  id: string;
  default_tone: string | null;
  voice_note: string | null;
  avoid_phrases: string[];
  preferred_length: string | null;
  cta_style: string | null;
  signature: string | null;
  extra_instructions: string | null;
  created_at: string;
  updated_at: string;
};

export type ProfileDetail = Profile & {
  skills: ProfileSkill[];
  projects: ProfileProject[];
  experiences: Array<{
    id: string;
    company: string;
    role: string;
    start_date: string | null;
    end_date: string | null;
    is_current: boolean;
    summary: string | null;
    highlights: string[];
    sort_order: number;
    created_at: string;
    updated_at: string;
  }>;
  niches: Array<{
    id: string;
    name: string;
    summary: string | null;
    proof: string | null;
    sort_order: number;
    created_at: string;
    updated_at: string;
  }>;
  custom_sections: Array<{
    id: string;
    title: string;
    section_type: string;
    content: string;
    sort_order: number;
    created_at: string;
    updated_at: string;
  }>;
  preferences: ProfilePreferences | null;
};

export type GuidelineType = "rule" | "intro" | "cta" | "tone_preset";
export type SampleTag = "winning" | "anti-pattern";
export type ClientResponseOutcome =
  | "no_response"
  | "replied"
  | "interview"
  | "hired"
  | "rejected";

export type CoverLetterGuideline = {
  id: string;
  user_id: string;
  title: string;
  guideline_type: GuidelineType;
  description: string | null;
  content: string;
  sort_order: number;
  created_at: string;
  updated_at: string;
};

export type CoverLetterSample = {
  id: string;
  user_id: string;
  title: string;
  tag: SampleTag;
  content: string;
  notes: string | null;
  outcome: string | null;
  sort_order: number;
  created_at: string;
  updated_at: string;
};

export type JobAnalysis = {
  title: string;
  scope: string;
  deliverables: string[];
  required_skills: string[];
  budget_clues: string[];
  urgency: "low" | "medium" | "high";
  tone: "formal" | "neutral" | "friendly" | "demanding";
  risk_flags: string[];
  fit_score: number;
};

export type JobAnalysisSnapshot = JobAnalysis & {
  id: string;
  raw_job_text: string;
  provider: string;
  model_name: string;
  prompt_version: string;
  created_at: string;
};

export type CoverLetterStructure =
  | "concise"
  | "problem-solution"
  | "credibility-first"
  | "portfolio-first"
  | "consultative";

export type CoverLetterVariant = {
  id: string;
  structure: CoverLetterStructure;
  headline: string;
  cover_letter: string;
  rationale: string;
  match_notes: string[];
  self_check_notes: string[];
  created_at: string;
};

export type GenerationResponse = {
  id: string;
  analysis_snapshot_id: string;
  raw_job_text: string;
  prompt_version: string;
  requested_structures: CoverLetterStructure[];
  analysis: JobAnalysis;
  variants: CoverLetterVariant[];
  created_at: string;
};

export type CoverLetterFeedback = {
  id: string;
  user_id: string;
  generation_run_id: string;
  generation_variant_id: string;
  rating: number;
  edited_cover_letter: string | null;
  accepted_sections: string[];
  rejected_sections: string[];
  client_response_outcome: ClientResponseOutcome;
  notes: string | null;
  memory_text: string;
  created_at: string;
  updated_at: string;
};

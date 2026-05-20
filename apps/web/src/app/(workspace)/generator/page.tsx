"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useMemo, useState } from "react";

import { apiClient } from "@/lib/api-client";
import { useSessionStore } from "@/lib/auth-store";
import type {
  ClientResponseOutcome,
  CoverLetterFeedback,
  CoverLetterStructure,
  GenerationResponse,
  JobAnalysisSnapshot,
} from "@/types/api";

const structureOptions: Array<{ value: CoverLetterStructure; label: string }> = [
  { value: "concise", label: "Concise" },
  { value: "problem-solution", label: "Problem → solution" },
  { value: "credibility-first", label: "Credibility first" },
  { value: "portfolio-first", label: "Portfolio first" },
  { value: "consultative", label: "Consultative" },
];

const outcomeOptions: ClientResponseOutcome[] = [
  "no_response",
  "replied",
  "interview",
  "hired",
  "rejected",
];

export default function GeneratorPage() {
  const accessToken = useSessionStore((state) => state.accessToken);
  const queryClient = useQueryClient();
  const [jobText, setJobText] = useState("");
  const [structures, setStructures] = useState<CoverLetterStructure[]>([
    "concise",
    "problem-solution",
  ]);
  const [analysis, setAnalysis] = useState<JobAnalysisSnapshot | null>(null);
  const [generation, setGeneration] = useState<GenerationResponse | null>(null);
  const [selectedVariantId, setSelectedVariantId] = useState<string | null>(null);
  const [feedbackForm, setFeedbackForm] = useState({
    rating: 4,
    accepted_sections: "",
    rejected_sections: "",
    edited_cover_letter: "",
    client_response_outcome: "no_response" as ClientResponseOutcome,
    notes: "",
  });
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const analyzeMutation = useMutation({
    mutationFn: (payload: { raw_job_text: string }) =>
      apiClient.post<JobAnalysisSnapshot>("/jobs/analyze", payload, { token: accessToken }),
    onSuccess: (result) => setAnalysis(result),
    onError: (error) =>
      setStatusMessage(error instanceof Error ? error.message : "Job analysis failed"),
  });

  const generateMutation = useMutation({
    mutationFn: async () => {
      const analysisResult =
        analysis ??
        (await analyzeMutation.mutateAsync({
          raw_job_text: jobText,
        }));
      return apiClient.post<GenerationResponse>(
        "/generate",
        {
          analysis_snapshot_id: analysisResult.id,
          structures,
        },
        { token: accessToken },
      );
    },
    onSuccess: (result) => {
      setGeneration(result);
      setSelectedVariantId(result.variants[0]?.id ?? null);
      setFeedbackForm((current) => ({
        ...current,
        edited_cover_letter: result.variants[0]?.cover_letter ?? "",
      }));
      setStatusMessage("Generation complete. Review the variants and save feedback on the strongest one.");
    },
    onError: (error) =>
      setStatusMessage(error instanceof Error ? error.message : "Generation failed"),
  });

  const feedbackMutation = useMutation({
    mutationFn: () =>
      apiClient.post<CoverLetterFeedback>(
        "/history/feedback",
        {
          generation_variant_id: selectedVariantId,
          rating: feedbackForm.rating,
          accepted_sections: feedbackForm.accepted_sections
            .split("\n")
            .map((item) => item.trim())
            .filter(Boolean),
          rejected_sections: feedbackForm.rejected_sections
            .split("\n")
            .map((item) => item.trim())
            .filter(Boolean),
          edited_cover_letter: feedbackForm.edited_cover_letter || null,
          client_response_outcome: feedbackForm.client_response_outcome,
          notes: feedbackForm.notes || null,
        },
        { token: accessToken },
      ),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["feedback"] });
      setStatusMessage("Feedback saved. Future generations can now reuse this signal.");
    },
    onError: (error) =>
      setStatusMessage(error instanceof Error ? error.message : "Saving feedback failed"),
  });

  const selectedVariant = useMemo(
    () => generation?.variants.find((variant) => variant.id === selectedVariantId) ?? null,
    [generation, selectedVariantId],
  );

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Generator</h1>
          <p className="page-subtitle">
            Analyze an Upwork job, generate multiple cover-letter structures, then save outcome-backed feedback.
          </p>
        </div>
        <button
          className="btn btn-secondary"
          type="button"
          onClick={() => {
            setAnalysis(null);
            setGeneration(null);
            setSelectedVariantId(null);
            setStatusMessage(null);
          }}
        >
          Reset run
        </button>
      </div>

      {statusMessage ? (
        <div className="card" style={{ marginBottom: 16, padding: 14 }}>
          {statusMessage}
        </div>
      ) : null}

      <div className="gen-stage">
        <div className="col" style={{ gap: 16 }}>
          <div className="gen-panel">
            <div className="gen-panel-header">
              <div className="gen-panel-title">Job post input</div>
            </div>
            <div className="gen-panel-body">
              <textarea
                className="gen-job-input"
                value={jobText}
                onChange={(event) => setJobText(event.target.value)}
                placeholder="Paste the Upwork job description here…"
              />

              <div className="mt-4">
                <label className="label">Requested structures</label>
                <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
                  {structureOptions.map((option) => {
                    const active = structures.includes(option.value);
                    return (
                      <button
                        key={option.value}
                        type="button"
                        className={`chip ${active ? "active" : ""}`}
                        onClick={() =>
                          setStructures((current) => {
                            if (active) {
                              return current.filter((value) => value !== option.value);
                            }
                            return [...current, option.value].slice(0, 5);
                          })
                        }
                      >
                        {option.label}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="row mt-4" style={{ justifyContent: "space-between" }}>
                <span className="field-hint">At least one structure is required.</span>
                <button
                  className="btn btn-primary"
                  type="button"
                  disabled={
                    generateMutation.isPending ||
                    analyzeMutation.isPending ||
                    !jobText.trim() ||
                    structures.length === 0
                  }
                  onClick={() => {
                    setStatusMessage(null);
                    setAnalysis(null);
                    setGeneration(null);
                    generateMutation.mutate();
                  }}
                >
                  {generateMutation.isPending || analyzeMutation.isPending
                    ? "Running…"
                    : "Analyze & generate"}
                </button>
              </div>
            </div>
          </div>

          {analysis ? (
            <div className="gen-panel">
              <div className="gen-panel-header">
                <div className="gen-panel-title">Structured job analysis</div>
                <span className="badge badge-accent">{analysis.fit_score}/100 fit</span>
              </div>
              <div className="gen-panel-body">
                <div className="match-score-card mb-4">
                  <div>
                    <div className="match-score-label">{analysis.title}</div>
                    <div className="match-score-text">{analysis.scope}</div>
                  </div>
                </div>
                <div className="grid-2">
                  <div>
                    <div className="label">Deliverables</div>
                    <div className="col" style={{ gap: 8 }}>
                      {analysis.deliverables.map((item) => (
                        <div key={item} className="sq-item">
                          <div className="sq-num">•</div>
                          <div>{item}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <div className="label">Required skills</div>
                    <div className="row" style={{ flexWrap: "wrap" }}>
                      {analysis.required_skills.map((item) => (
                        <span key={item} className="chip active">{item}</span>
                      ))}
                    </div>
                    <div className="label mt-4">Risk flags</div>
                    <div className="row" style={{ flexWrap: "wrap" }}>
                      {analysis.risk_flags.length === 0 ? (
                        <span className="chip">No major flags extracted</span>
                      ) : (
                        analysis.risk_flags.map((item) => <span key={item} className="chip">{item}</span>)
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : null}
        </div>

        <div className="col" style={{ gap: 16 }}>
          <div className="gen-panel">
            <div className="gen-panel-header">
              <div className="gen-panel-title">Generated variants</div>
              {generation ? <span className="badge">{generation.variants.length} variants</span> : null}
            </div>
            <div className="gen-panel-body">
              {!generation ? (
                <div className="empty">
                  <div className="empty-title">No generation yet</div>
                  <div className="empty-text">
                    Run the generator to see structured drafts and review notes.
                  </div>
                </div>
              ) : (
                <div className="col" style={{ gap: 12 }}>
                  <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
                    {generation.variants.map((variant) => (
                      <button
                        key={variant.id}
                        type="button"
                        className={`chip ${selectedVariantId === variant.id ? "active" : ""}`}
                        onClick={() => {
                          setSelectedVariantId(variant.id);
                          setFeedbackForm((current) => ({
                            ...current,
                            edited_cover_letter: variant.cover_letter,
                          }));
                        }}
                      >
                        {variant.structure}
                      </button>
                    ))}
                  </div>

                  {selectedVariant ? (
                    <>
                      <div className="card">
                        <div className="between" style={{ marginBottom: 10 }}>
                          <div style={{ fontWeight: 600 }}>{selectedVariant.headline}</div>
                          <span className="badge badge-accent">{selectedVariant.structure}</span>
                        </div>
                        <div className="letter-output">{selectedVariant.cover_letter}</div>
                        <div className="mt-4">
                          <div className="label">Rationale</div>
                          <div style={{ color: "var(--text-2)", fontSize: 13 }}>
                            {selectedVariant.rationale}
                          </div>
                        </div>
                      </div>

                      <div className="card">
                        <div className="label">Match notes</div>
                        <div className="row" style={{ flexWrap: "wrap" }}>
                          {selectedVariant.match_notes.map((item) => (
                            <span key={item} className="chip active">{item}</span>
                          ))}
                        </div>
                        <div className="label mt-4">Self-check notes</div>
                        <div className="row" style={{ flexWrap: "wrap" }}>
                          {selectedVariant.self_check_notes.map((item) => (
                            <span key={item} className="chip">{item}</span>
                          ))}
                        </div>
                      </div>
                    </>
                  ) : null}
                </div>
              )}
            </div>
          </div>

          {selectedVariant ? (
            <div className="gen-panel">
              <div className="gen-panel-header">
                <div className="gen-panel-title">Save feedback memory</div>
              </div>
              <div className="gen-panel-body">
                <div className="field">
                  <label className="label" htmlFor="edited-letter">Edited final letter</label>
                  <textarea
                    id="edited-letter"
                    className="textarea"
                    value={feedbackForm.edited_cover_letter}
                    onChange={(event) =>
                      setFeedbackForm((current) => ({
                        ...current,
                        edited_cover_letter: event.target.value,
                      }))
                    }
                    rows={8}
                  />
                </div>
                <div className="grid-2">
                  <div className="field">
                    <label className="label" htmlFor="accepted-sections">Accepted sections</label>
                    <textarea
                      id="accepted-sections"
                      className="textarea"
                      value={feedbackForm.accepted_sections}
                      onChange={(event) =>
                        setFeedbackForm((current) => ({
                          ...current,
                          accepted_sections: event.target.value,
                        }))
                      }
                      placeholder="One line per accepted pattern"
                    />
                  </div>
                  <div className="field">
                    <label className="label" htmlFor="rejected-sections">Rejected sections</label>
                    <textarea
                      id="rejected-sections"
                      className="textarea"
                      value={feedbackForm.rejected_sections}
                      onChange={(event) =>
                        setFeedbackForm((current) => ({
                          ...current,
                          rejected_sections: event.target.value,
                        }))
                      }
                      placeholder="One line per rejected pattern"
                    />
                  </div>
                </div>
                <div className="grid-2">
                  <div className="field">
                    <label className="label" htmlFor="rating">Rating</label>
                    <input
                      id="rating"
                      className="input"
                      type="number"
                      min={1}
                      max={5}
                      value={feedbackForm.rating}
                      onChange={(event) =>
                        setFeedbackForm((current) => ({
                          ...current,
                          rating: Number(event.target.value),
                        }))
                      }
                    />
                  </div>
                  <div className="field">
                    <label className="label" htmlFor="outcome">Client outcome</label>
                    <select
                      id="outcome"
                      className="select"
                      value={feedbackForm.client_response_outcome}
                      onChange={(event) =>
                        setFeedbackForm((current) => ({
                          ...current,
                          client_response_outcome: event.target.value as ClientResponseOutcome,
                        }))
                      }
                    >
                      {outcomeOptions.map((option) => (
                        <option key={option} value={option}>
                          {option.replaceAll("_", " ")}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="field">
                  <label className="label" htmlFor="notes">Notes</label>
                  <textarea
                    id="notes"
                    className="textarea"
                    value={feedbackForm.notes}
                    onChange={(event) =>
                      setFeedbackForm((current) => ({
                        ...current,
                        notes: event.target.value,
                      }))
                    }
                    placeholder="What worked, what did not, what should the next run preserve?"
                  />
                </div>
                <button
                  className="btn btn-primary"
                  type="button"
                  disabled={feedbackMutation.isPending}
                  onClick={() => feedbackMutation.mutate()}
                >
                  {feedbackMutation.isPending ? "Saving…" : "Save feedback"}
                </button>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}

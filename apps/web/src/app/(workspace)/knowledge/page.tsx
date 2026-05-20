"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { apiClient } from "@/lib/api-client";
import { useSessionStore } from "@/lib/auth-store";
import type { CoverLetterGuideline, CoverLetterSample, GuidelineType, SampleTag } from "@/types/api";

const guidelineTypes: GuidelineType[] = ["rule", "intro", "cta", "tone_preset"];
const sampleTags: SampleTag[] = ["winning", "anti-pattern"];

export default function KnowledgePage() {
  const accessToken = useSessionStore((state) => state.accessToken);
  const queryClient = useQueryClient();
  const [guidelineForm, setGuidelineForm] = useState({
    title: "",
    guideline_type: "rule" as GuidelineType,
    description: "",
    content: "",
  });
  const [sampleForm, setSampleForm] = useState({
    title: "",
    tag: "winning" as SampleTag,
    notes: "",
    outcome: "",
    content: "",
  });

  const guidelinesQuery = useQuery({
    queryKey: ["knowledge", "guidelines"],
    queryFn: () => apiClient.get<CoverLetterGuideline[]>("/library/guidelines", { token: accessToken }),
    enabled: Boolean(accessToken),
  });

  const samplesQuery = useQuery({
    queryKey: ["knowledge", "samples"],
    queryFn: () => apiClient.get<CoverLetterSample[]>("/library/samples", { token: accessToken }),
    enabled: Boolean(accessToken),
  });

  const createGuideline = useMutation({
    mutationFn: () =>
      apiClient.post<CoverLetterGuideline>(
        "/library/guidelines",
        {
          ...guidelineForm,
          description: guidelineForm.description || null,
        },
        { token: accessToken },
      ),
    onSuccess: async () => {
      setGuidelineForm({ title: "", guideline_type: "rule", description: "", content: "" });
      await queryClient.invalidateQueries({ queryKey: ["knowledge", "guidelines"] });
    },
  });

  const createSample = useMutation({
    mutationFn: () =>
      apiClient.post<CoverLetterSample>(
        "/library/samples",
        {
          ...sampleForm,
          notes: sampleForm.notes || null,
          outcome: sampleForm.outcome || null,
        },
        { token: accessToken },
      ),
    onSuccess: async () => {
      setSampleForm({ title: "", tag: "winning", notes: "", outcome: "", content: "" });
      await queryClient.invalidateQueries({ queryKey: ["knowledge", "samples"] });
    },
  });

  const deleteGuideline = useMutation({
    mutationFn: (id: string) => apiClient.delete<void>(`/library/guidelines/${id}`, { token: accessToken }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["knowledge", "guidelines"] });
    },
  });

  const deleteSample = useMutation({
    mutationFn: (id: string) => apiClient.delete<void>(`/library/samples/${id}`, { token: accessToken }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["knowledge", "samples"] });
    },
  });

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Knowledge</h1>
          <p className="page-subtitle">
            Store reusable rules, intros, CTAs, and sample letters that shape future generations.
          </p>
        </div>
      </div>

      <div className="kb-grid">
        <div className="card-bare">
          <div className="card-header">
            <h2 className="card-title">Guidelines</h2>
            <span className="badge">{guidelinesQuery.data?.length ?? 0}</span>
          </div>
          <div className="card-body">
            <div className="field">
              <label className="label">Title</label>
              <input
                className="input"
                value={guidelineForm.title}
                onChange={(event) => setGuidelineForm((current) => ({ ...current, title: event.target.value }))}
              />
            </div>
            <div className="grid-2">
              <div className="field">
                <label className="label">Type</label>
                <select
                  className="select"
                  value={guidelineForm.guideline_type}
                  onChange={(event) =>
                    setGuidelineForm((current) => ({
                      ...current,
                      guideline_type: event.target.value as GuidelineType,
                    }))
                  }
                >
                  {guidelineTypes.map((type) => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label className="label">Description</label>
                <input
                  className="input"
                  value={guidelineForm.description}
                  onChange={(event) => setGuidelineForm((current) => ({ ...current, description: event.target.value }))}
                />
              </div>
            </div>
            <div className="field">
              <label className="label">Content</label>
              <textarea
                className="textarea"
                value={guidelineForm.content}
                onChange={(event) => setGuidelineForm((current) => ({ ...current, content: event.target.value }))}
              />
            </div>
            <button className="btn btn-primary" type="button" onClick={() => createGuideline.mutate()}>
              Add guideline
            </button>

            <div className="divider" />

            <div className="col" style={{ gap: 12 }}>
              {(guidelinesQuery.data ?? []).map((item) => (
                <div key={item.id} className="kb-example-card">
                  <div className="kb-example-header">
                    <div>
                      <div style={{ fontWeight: 600 }}>{item.title}</div>
                      <div style={{ fontSize: 12, color: "var(--text-3)" }}>{item.guideline_type}</div>
                    </div>
                    <button
                      className="btn btn-danger btn-sm"
                      type="button"
                      onClick={() => deleteGuideline.mutate(item.id)}
                    >
                      Delete
                    </button>
                  </div>
                  <div className="kb-example-snippet">{item.content}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="card-bare">
          <div className="card-header">
            <h2 className="card-title">Samples</h2>
            <span className="badge">{samplesQuery.data?.length ?? 0}</span>
          </div>
          <div className="card-body">
            <div className="field">
              <label className="label">Title</label>
              <input
                className="input"
                value={sampleForm.title}
                onChange={(event) => setSampleForm((current) => ({ ...current, title: event.target.value }))}
              />
            </div>
            <div className="grid-2">
              <div className="field">
                <label className="label">Tag</label>
                <select
                  className="select"
                  value={sampleForm.tag}
                  onChange={(event) =>
                    setSampleForm((current) => ({
                      ...current,
                      tag: event.target.value as SampleTag,
                    }))
                  }
                >
                  {sampleTags.map((tag) => (
                    <option key={tag} value={tag}>{tag}</option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label className="label">Outcome</label>
                <input
                  className="input"
                  value={sampleForm.outcome}
                  onChange={(event) => setSampleForm((current) => ({ ...current, outcome: event.target.value }))}
                />
              </div>
            </div>
            <div className="field">
              <label className="label">Notes</label>
              <input
                className="input"
                value={sampleForm.notes}
                onChange={(event) => setSampleForm((current) => ({ ...current, notes: event.target.value }))}
              />
            </div>
            <div className="field">
              <label className="label">Sample content</label>
              <textarea
                className="textarea"
                value={sampleForm.content}
                onChange={(event) => setSampleForm((current) => ({ ...current, content: event.target.value }))}
              />
            </div>
            <button className="btn btn-primary" type="button" onClick={() => createSample.mutate()}>
              Add sample
            </button>

            <div className="divider" />

            <div className="col" style={{ gap: 12 }}>
              {(samplesQuery.data ?? []).map((item) => (
                <div key={item.id} className="kb-example-card">
                  <div className="kb-example-header">
                    <div>
                      <div style={{ fontWeight: 600 }}>{item.title}</div>
                      <div className="kb-example-tags">
                        <span className="badge badge-accent">{item.tag}</span>
                        {item.outcome ? <span className="badge">{item.outcome}</span> : null}
                      </div>
                    </div>
                    <button
                      className="btn btn-danger btn-sm"
                      type="button"
                      onClick={() => deleteSample.mutate(item.id)}
                    >
                      Delete
                    </button>
                  </div>
                  <div className="kb-example-snippet">{item.content}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

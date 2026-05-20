"use client";

import { useQuery } from "@tanstack/react-query";

import { apiClient } from "@/lib/api-client";
import { useSessionStore } from "@/lib/auth-store";
import type { CoverLetterFeedback } from "@/types/api";

export default function HistoryPage() {
  const accessToken = useSessionStore((state) => state.accessToken);
  const feedbackQuery = useQuery({
    queryKey: ["feedback", "history"],
    queryFn: () => apiClient.get<CoverLetterFeedback[]>("/history/feedback", { token: accessToken }),
    enabled: Boolean(accessToken),
  });

  const feedbackItems = feedbackQuery.data ?? [];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">History</h1>
          <p className="page-subtitle">
            Feedback-backed proposal history. Every saved entry can influence future drafts.
          </p>
        </div>
      </div>

      <div className="card-bare">
        <div className="card-header">
          <h2 className="card-title">Saved feedback timeline</h2>
          <span className="badge">{feedbackItems.length} entries</span>
        </div>
        <div className="card-body">
          {feedbackQuery.isLoading ? (
            <div className="empty"><div className="empty-title">Loading history…</div></div>
          ) : feedbackItems.length === 0 ? (
            <div className="empty">
              <div className="empty-title">No history yet</div>
              <div className="empty-text">
                Rate a generated letter in Generator and it will appear here.
              </div>
            </div>
          ) : (
            <div className="col" style={{ gap: 12 }}>
              {feedbackItems.map((item) => (
                <div key={item.id} className="card">
                  <div className="between" style={{ marginBottom: 12 }}>
                    <div className="row">
                      <span className="badge badge-accent">{item.client_response_outcome}</span>
                      <span className="badge">Rating {item.rating}/5</span>
                    </div>
                    <span style={{ fontSize: 12, color: "var(--text-3)" }}>
                      {new Date(item.created_at).toLocaleString()}
                    </span>
                  </div>
                  <div style={{ fontSize: 13, color: "var(--text-2)", whiteSpace: "pre-wrap" }}>
                    {item.edited_cover_letter ?? item.memory_text}
                  </div>
                  {item.accepted_sections.length > 0 ? (
                    <div className="mt-3">
                      <div className="label">Accepted sections</div>
                      <div className="row" style={{ flexWrap: "wrap" }}>
                        {item.accepted_sections.map((section) => (
                          <span key={section} className="chip active">{section}</span>
                        ))}
                      </div>
                    </div>
                  ) : null}
                  {item.rejected_sections.length > 0 ? (
                    <div className="mt-3">
                      <div className="label">Rejected sections</div>
                      <div className="row" style={{ flexWrap: "wrap" }}>
                        {item.rejected_sections.map((section) => (
                          <span key={section} className="chip">{section}</span>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

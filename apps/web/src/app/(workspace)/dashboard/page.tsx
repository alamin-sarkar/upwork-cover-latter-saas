"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";

import { apiClient, ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/lib/auth-store";
import type { CoverLetterFeedback, ProfileDetail } from "@/types/api";

async function fetchProfile(token: string) {
  try {
    return await apiClient.get<ProfileDetail>("/profile", { token });
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return null;
    }
    throw error;
  }
}

async function fetchFeedback(token: string) {
  return apiClient.get<CoverLetterFeedback[]>("/history/feedback", { token });
}

export default function DashboardPage() {
  const accessToken = useSessionStore((state) => state.accessToken);
  const user = useSessionStore((state) => state.user);

  const profileQuery = useQuery({
    queryKey: ["profile", "detail"],
    queryFn: () => fetchProfile(accessToken as string),
    enabled: Boolean(accessToken),
  });

  const feedbackQuery = useQuery({
    queryKey: ["feedback", "list"],
    queryFn: () => fetchFeedback(accessToken as string),
    enabled: Boolean(accessToken),
  });

  const feedbackItems = feedbackQuery.data ?? [];
  const replyCount = feedbackItems.filter((item) =>
    ["replied", "interview", "hired"].includes(item.client_response_outcome),
  ).length;
  const avgRating = feedbackItems.length
    ? Math.round(
        (feedbackItems.reduce((sum, item) => sum + item.rating, 0) / feedbackItems.length) * 10,
      ) / 10
    : 0;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">
            Welcome back{user?.full_name ? `, ${user.full_name.split(" ")[0]}` : ""}
          </h1>
          <p className="page-subtitle">
            Your frontend workflow is now wired to the live FastAPI backend.
          </p>
        </div>
        <Link href="/generator" className="btn btn-primary">
          New cover letter
        </Link>
      </div>

      <div className="grid-4" style={{ marginBottom: 24 }}>
        <div className="card">
          <div className="stat-label">Feedback entries</div>
          <div className="stat-value">{feedbackItems.length}</div>
          <div className="field-hint">Rated proposals stored in memory</div>
        </div>
        <div className="card">
          <div className="stat-label">Response signals</div>
          <div className="stat-value">{replyCount}</div>
          <div className="field-hint">Replies, interviews, or hires</div>
        </div>
        <div className="card">
          <div className="stat-label">Average rating</div>
          <div className="stat-value">{avgRating || "0.0"}</div>
          <div className="field-hint">Across all saved feedback</div>
        </div>
        <div className="card">
          <div className="stat-label">Profile readiness</div>
          <div className="stat-value">{profileQuery.data ? "Ready" : "Start"}</div>
          <div className="field-hint">
            {profileQuery.data ? "Profile data available for generation" : "Complete your profile next"}
          </div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: 20 }}>
        <div className="card-bare">
          <div className="card-header">
            <h2 className="card-title">Next action</h2>
            <span className="badge badge-accent">Live flow</span>
          </div>
          <div className="card-body">
            <div className="col" style={{ gap: 12 }}>
              <div className="sq-item">
                <div className="sq-num">1</div>
                <div>Fill your profile and preferences in Settings.</div>
              </div>
              <div className="sq-item">
                <div className="sq-num">2</div>
                <div>Save winning intros, CTAs, and sample letters in Knowledge.</div>
              </div>
              <div className="sq-item">
                <div className="sq-num">3</div>
                <div>Paste a job post in Generator to get analysis and multiple variants.</div>
              </div>
              <div className="sq-item">
                <div className="sq-num">4</div>
                <div>Save feedback on the best variant so the next run adapts to it.</div>
              </div>
            </div>
          </div>
        </div>

        <div className="card-bare">
          <div className="card-header">
            <h2 className="card-title">Recent feedback</h2>
            <Link href="/history" className="btn btn-ghost btn-sm">Open history</Link>
          </div>
          <div className="card-body">
            {feedbackQuery.isLoading ? (
              <div className="empty">
                <div className="empty-title">Loading feedback…</div>
              </div>
            ) : feedbackItems.length === 0 ? (
              <div className="empty">
                <div className="empty-title">No feedback yet</div>
                <div className="empty-text">
                  Generate a letter, rate a variant, and it will show up here.
                </div>
              </div>
            ) : (
              <div className="col" style={{ gap: 10 }}>
                {feedbackItems.slice(0, 4).map((item) => (
                  <div key={item.id} className="card" style={{ padding: 14 }}>
                    <div className="between" style={{ marginBottom: 8 }}>
                      <span className="badge">{item.client_response_outcome}</span>
                      <span style={{ fontSize: 12, color: "var(--text-3)" }}>
                        {new Date(item.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div style={{ fontSize: 13, color: "var(--text-1)", marginBottom: 6 }}>
                      {item.edited_cover_letter ?? item.memory_text.slice(0, 140)}
                    </div>
                    <div style={{ fontSize: 12, color: "var(--text-2)" }}>
                      Rating {item.rating}/5
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

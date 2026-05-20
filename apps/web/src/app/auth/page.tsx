"use client";

import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { apiClient } from "@/lib/api-client";
import { useSessionStore } from "@/lib/auth-store";
import type { TokenResponse, User } from "@/types/api";

type AuthMode = "login" | "register";

async function fetchMe(accessToken: string) {
  return apiClient.get<User>("/auth/me", { token: accessToken });
}

export default function AuthPage() {
  const router = useRouter();
  const setSession = useSessionStore((state) => state.setSession);
  const [mode, setMode] = useState<AuthMode>("login");
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    fullName: "",
    email: "",
    password: "",
  });

  const authMutation = useMutation({
    mutationFn: async () => {
      const payload =
        mode === "register"
          ? {
              email: form.email,
              password: form.password,
              full_name: form.fullName || null,
            }
          : {
              email: form.email,
              password: form.password,
            };
      const tokenResponse = await apiClient.post<TokenResponse>(
        mode === "register" ? "/auth/register" : "/auth/login",
        payload,
      );
      const user = await fetchMe(tokenResponse.access_token);
      return { tokenResponse, user };
    },
    onSuccess: ({ tokenResponse, user }) => {
      setSession({
        accessToken: tokenResponse.access_token,
        refreshToken: tokenResponse.refresh_token,
        user,
      });
      router.replace("/dashboard");
    },
    onError: (mutationError) => {
      setError(mutationError instanceof Error ? mutationError.message : "Authentication failed");
    },
  });

  return (
    <div className="auth-stage">
      <section className="auth-side">
        <div className="auth-glow" />
        <div>
          <div className="sidebar-brand" style={{ borderBottom: "none", padding: 0, marginBottom: 40 }}>
            <div className="sidebar-brand-mark">PC</div>
            <div>
              <div className="sidebar-brand-name" style={{ fontSize: 18 }}>PitchCraft</div>
              <div style={{ fontSize: 12, color: "var(--text-3)" }}>AI cover letters for Upwork</div>
            </div>
          </div>
          <div className="auth-quote">
            <div className="auth-quote-mark">“</div>
            <div className="auth-quote-text">
              Stop writing proposals from scratch. Build a durable pitch system that learns what gets replies.
            </div>
            <div className="auth-quote-author">
              <div className="avatar">PC</div>
              <div>
                <div style={{ color: "var(--text-1)" }}>PitchCraft workflow</div>
                <div style={{ color: "var(--text-3)" }}>Profile → analysis → drafts → feedback memory</div>
              </div>
            </div>
          </div>
        </div>

        <div className="auth-stat-strip">
          <div className="stat">
            <div className="stat-value">5</div>
            <div className="stat-label">Letter structures</div>
          </div>
          <div className="stat">
            <div className="stat-value">1</div>
            <div className="stat-label">Feedback loop</div>
          </div>
          <div className="stat">
            <div className="stat-value">∞</div>
            <div className="stat-label">Reusable proof</div>
          </div>
        </div>
      </section>

      <section className="auth-form-side">
        <div className="auth-form-card card">
          <div className="auth-tab-toggle">
            <button
              type="button"
              className={mode === "login" ? "active" : ""}
              onClick={() => setMode("login")}
            >
              Sign in
            </button>
            <button
              type="button"
              className={mode === "register" ? "active" : ""}
              onClick={() => setMode("register")}
            >
              Create account
            </button>
          </div>

          <h1>{mode === "login" ? "Welcome back" : "Create your workspace"}</h1>
          <p>
            {mode === "login"
              ? "Sign in to continue your PitchCraft workflow."
              : "Start with your profile, then generate and improve pitches from real feedback."}
          </p>

          <form
            onSubmit={(event) => {
              event.preventDefault();
              setError(null);
              authMutation.mutate();
            }}
          >
            {mode === "register" ? (
              <div className="field">
                <label className="label" htmlFor="fullName">Full name</label>
                <input
                  id="fullName"
                  className="input"
                  value={form.fullName}
                  onChange={(event) => setForm((current) => ({ ...current, fullName: event.target.value }))}
                  placeholder="A freelancer name clients recognize"
                />
              </div>
            ) : null}

            <div className="field">
              <label className="label" htmlFor="email">Email</label>
              <input
                id="email"
                className="input"
                type="email"
                required
                value={form.email}
                onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))}
                placeholder="you@example.com"
              />
            </div>

            <div className="field">
              <label className="label" htmlFor="password">Password</label>
              <input
                id="password"
                className="input"
                type="password"
                minLength={8}
                required
                value={form.password}
                onChange={(event) => setForm((current) => ({ ...current, password: event.target.value }))}
                placeholder="Minimum 8 characters"
              />
            </div>

            {error ? (
              <div className="badge badge-danger" style={{ marginBottom: 16 }}>
                {error}
              </div>
            ) : null}

            <button className="btn btn-primary btn-lg" style={{ width: "100%" }} disabled={authMutation.isPending}>
              {authMutation.isPending
                ? "Working…"
                : mode === "login"
                  ? "Sign in"
                  : "Create account"}
            </button>
          </form>
        </div>
      </section>
    </div>
  );
}

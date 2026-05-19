"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";

type HealthResponse = { status: string; service: string; version: string };

export default function HomePage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .get<HealthResponse>("/health")
      .then(setHealth)
      .catch((e: Error) => setError(e.message));
  }, []);

  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col items-start justify-center gap-6 px-8">
      <span className="rounded-full bg-accent-soft px-3 py-1 text-xs font-medium uppercase tracking-wider text-accent">
        PitchCraft · Phase 1
      </span>
      <h1 className="text-5xl font-semibold tracking-tight">
        AI cover letters that match the job, not the template.
      </h1>
      <p className="max-w-2xl text-lg text-ink-secondary">
        Paste an Upwork job post. PitchCraft analyzes the post, matches it
        against your profile evidence, and drafts multiple structured cover
        letters with rationale and edit-ready output.
      </p>
      <div className="flex gap-3">
        <button className="rounded-xl bg-accent px-5 py-2.5 font-medium text-white transition hover:bg-accent-hover">
          Get started
        </button>
        <button className="rounded-xl border border-border-strong px-5 py-2.5 font-medium text-ink-primary transition hover:bg-bg-surface">
          See a sample run
        </button>
      </div>

      <div className="mt-8 w-full rounded-xl border border-border-subtle bg-bg-surface p-4">
        <p className="mb-2 text-xs font-medium uppercase tracking-wider text-ink-muted">
          API Health Check
        </p>
        {error && (
          <p className="text-sm text-red-400">
            ✗ Backend unreachable — {error}
          </p>
        )}
        {health && (
          <p className="text-sm text-accent">
            ✓ {health.service} v{health.version} · {health.status}
          </p>
        )}
        {!health && !error && (
          <p className="text-sm text-ink-muted">Connecting…</p>
        )}
      </div>

      <p className="text-sm text-ink-muted">
        Phase 1 scaffold · workflow screens land in Phase 9.
      </p>
    </main>
  );
}

"use client";

import type { Route } from "next";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";

import { apiClient, ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/lib/auth-store";
import type { User } from "@/types/api";

const navItems: Array<{ href: Route; label: string }> = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/generator", label: "Generator" },
  { href: "/history", label: "History" },
  { href: "/knowledge", label: "Knowledge" },
  { href: "/settings", label: "Settings" },
];

async function fetchMe(token: string): Promise<User> {
  return apiClient.get<User>("/auth/me", { token });
}

export function WorkspaceShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const accessToken = useSessionStore((state) => state.accessToken);
  const user = useSessionStore((state) => state.user);
  const setUser = useSessionStore((state) => state.setUser);
  const clearSession = useSessionStore((state) => state.clearSession);

  const meQuery = useQuery({
    queryKey: ["auth", "me", accessToken],
    queryFn: () => fetchMe(accessToken as string),
    enabled: Boolean(accessToken),
  });

  useEffect(() => {
    if (meQuery.data) {
      setUser(meQuery.data);
    }
  }, [meQuery.data, setUser]);

  useEffect(() => {
    if (meQuery.error instanceof ApiError && meQuery.error.status === 401) {
      clearSession();
      router.replace("/auth");
    }
  }, [clearSession, meQuery.error, router]);

  const initials = useMemo(() => {
    const source = user?.full_name?.trim() || user?.email || "PitchCraft";
    return source
      .split(/\s+/)
      .slice(0, 2)
      .map((token) => token[0]?.toUpperCase() ?? "")
      .join("");
  }, [user]);

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-brand-mark">PC</div>
          <div>
            <div className="sidebar-brand-name">PitchCraft</div>
            <div style={{ fontSize: 12, color: "var(--text-3)" }}>Upwork letter OS</div>
          </div>
        </div>

        <div className="sidebar-section-label">Workspace</div>
        {navItems.map((item) => {
          const active = pathname === item.href;
          return (
            <Link key={item.href} href={item.href} className={`nav-item ${active ? "active" : ""}`}>
              <span>{item.label}</span>
            </Link>
          );
        })}

        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="avatar">{initials}</div>
            <div className="grow">
              <div style={{ fontSize: 13, fontWeight: 600 }}>
                {user?.full_name || user?.email || "Loading…"}
              </div>
              <div style={{ fontSize: 12, color: "var(--text-3)", textTransform: "capitalize" }}>
                {user?.plan ?? "free"} plan
              </div>
            </div>
            <button
              className="btn btn-ghost btn-sm"
              type="button"
              onClick={() => {
                clearSession();
                router.replace("/auth");
              }}
            >
              Logout
            </button>
          </div>
        </div>
      </aside>

      <main className="app-main">
        <header className="topbar">
          <div className="search-input">
            <span>PitchCraft workspace</span>
            <kbd>Phase 9</kbd>
          </div>
          <div className="row">
            <span className="badge badge-accent">Live API</span>
            <span style={{ fontSize: 12, color: "var(--text-3)" }}>
              {user?.email ?? "Checking session"}
            </span>
          </div>
        </header>
        {children}
      </main>
    </div>
  );
}

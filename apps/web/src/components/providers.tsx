"use client";

import { QueryClientProvider } from "@tanstack/react-query";
import { useEffect } from "react";

import { queryClient } from "@/lib/query-client";
import { useSessionStore } from "@/lib/auth-store";

export function Providers({ children }: { children: React.ReactNode }) {
  const syncFromCookies = useSessionStore((state) => state.syncFromCookies);
  const hydrated = useSessionStore((state) => state.hydrated);

  useEffect(() => {
    syncFromCookies();
  }, [syncFromCookies]);

  if (!hydrated) {
    return null;
  }

  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}

"use client";

import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

import { clearSessionCookies, persistSessionCookies, readSessionCookies } from "@/lib/auth";
import type { User } from "@/types/api";

type SessionState = {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null;
  hydrated: boolean;
  setHydrated: (hydrated: boolean) => void;
  syncFromCookies: () => void;
  setSession: (payload: {
    accessToken: string;
    refreshToken: string;
    user: User | null;
  }) => void;
  setUser: (user: User | null) => void;
  clearSession: () => void;
};

export const useSessionStore = create<SessionState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      hydrated: false,
      setHydrated: (hydrated) => set({ hydrated }),
      syncFromCookies: () => {
        const { accessToken, refreshToken } = readSessionCookies();
        set((state) => ({
          accessToken: accessToken ?? state.accessToken,
          refreshToken: refreshToken ?? state.refreshToken,
        }));
      },
      setSession: ({ accessToken, refreshToken, user }) => {
        persistSessionCookies(accessToken, refreshToken);
        set({ accessToken, refreshToken, user });
      },
      setUser: (user) => set({ user }),
      clearSession: () => {
        clearSessionCookies();
        set({ accessToken: null, refreshToken: null, user: null });
      },
    }),
    {
      name: "pitchcraft-session",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        user: state.user,
      }),
      onRehydrateStorage: () => (state) => {
        state?.setHydrated(true);
      },
    },
  ),
);

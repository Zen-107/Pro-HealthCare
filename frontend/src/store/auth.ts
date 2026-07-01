import { create } from "zustand";
import type { Token, User } from "../types";
import api from "../api/client";

interface AuthState {
  token: Token | null;
  user: User | null;
  loading: boolean;

  login: (email: string, password: string) => Promise<void>;
  register: (data: {
    email: string;
    password: string;
    full_name: string;
    role: string;
  }) => Promise<void>;
  fetchMe: () => Promise<void>;
  logout: () => void;
  restore: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  loading: false,

  login: async (email, password) => {
    set({ loading: true });
    try {
      // FastAPI OAuth2 password flow ใช้ form-data
      const res = await api.post<Token>(
        "/auth/login",
        new URLSearchParams({ username: email, password }),
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } },
      );
      const token = res.data;
      localStorage.setItem("access_token", token.access_token);
      set({ token });
      // ดึงข้อมูล user ทันที
      const me = await api.get<User>("/auth/me");
      set({ user: me.data, loading: false });
    } catch (e) {
      set({ loading: false });
      throw e;
    }
  },

  register: async (data) => {
    set({ loading: true });
    try {
      const res = await api.post<Token>("/auth/register", data);
      const token = res.data;
      localStorage.setItem("access_token", token.access_token);
      set({ token });
      const me = await api.get<User>("/auth/me");
      set({ user: me.data, loading: false });
    } catch (e) {
      set({ loading: false });
      throw e;
    }
  },

  fetchMe: async () => {
    try {
      const me = await api.get<User>("/auth/me");
      set({ user: me.data });
    } catch {
      set({ user: null, token: null });
      localStorage.removeItem("access_token");
    }
  },

  logout: () => {
    localStorage.removeItem("access_token");
    set({ token: null, user: null });
  },

  restore: async () => {
    const saved = localStorage.getItem("access_token");
    if (saved) {
      set({ token: { access_token: saved, token_type: "bearer", role: "", user_id: 0 } });
      try {
        const me = await api.get<User>("/auth/me");
        set({ user: me.data });
      } catch {
        localStorage.removeItem("access_token");
        set({ token: null, user: null });
      }
    }
  },
}));

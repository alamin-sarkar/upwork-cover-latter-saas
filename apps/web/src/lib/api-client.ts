const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8080";

type RequestOptions = Omit<RequestInit, "body"> & { body?: unknown };

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { body, headers, ...rest } = options;
  const res = await fetch(`${BASE_URL}${path}`, {
    ...rest,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const detail = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(detail?.detail ?? `Request failed: ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export const apiClient = {
  get: <T>(path: string, init?: RequestOptions) =>
    request<T>(path, { method: "GET", ...init }),

  post: <T>(path: string, body: unknown, init?: RequestOptions) =>
    request<T>(path, { method: "POST", body, ...init }),

  put: <T>(path: string, body: unknown, init?: RequestOptions) =>
    request<T>(path, { method: "PUT", body, ...init }),

  patch: <T>(path: string, body: unknown, init?: RequestOptions) =>
    request<T>(path, { method: "PATCH", body, ...init }),

  delete: <T>(path: string, init?: RequestOptions) =>
    request<T>(path, { method: "DELETE", ...init }),
};

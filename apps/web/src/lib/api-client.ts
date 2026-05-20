const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

type Primitive = string | number | boolean | null;
type JsonValue = Primitive | JsonValue[] | { [key: string]: JsonValue };

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

type RequestOptions = Omit<RequestInit, "body" | "headers"> & {
  body?: JsonValue | Record<string, unknown>;
  headers?: HeadersInit;
  token?: string | null;
};

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { body, headers, token, ...rest } = options;
  const response = await fetch(`${BASE_URL}${path}`, {
    ...rest,
    cache: "no-store",
    headers: {
      ...(body !== undefined ? { "Content-Type": "application/json" } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const detail = await response
      .json()
      .catch(() => ({ detail: response.statusText })) as { detail?: string };
    throw new ApiError(detail.detail ?? `Request failed: ${response.status}`, response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const apiClient = {
  get<T>(path: string, init?: RequestOptions) {
    return request<T>(path, { method: "GET", ...init });
  },
  post<T>(path: string, body: RequestOptions["body"], init?: RequestOptions) {
    return request<T>(path, { method: "POST", body, ...init });
  },
  patch<T>(path: string, body: RequestOptions["body"], init?: RequestOptions) {
    return request<T>(path, { method: "PATCH", body, ...init });
  },
  put<T>(path: string, body: RequestOptions["body"], init?: RequestOptions) {
    return request<T>(path, { method: "PUT", body, ...init });
  },
  delete<T>(path: string, init?: RequestOptions) {
    return request<T>(path, { method: "DELETE", ...init });
  },
};

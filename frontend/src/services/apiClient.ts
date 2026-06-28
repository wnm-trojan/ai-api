import { API_BASE, buildHeaders } from "../config/env";

export async function apiFetch<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: buildHeaders(),
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }

  return res.json() as Promise<T>;
}

export async function fetchHealth<T>(): Promise<T> {
  const res = await fetch(`${API_BASE}/health`);
  return res.json() as Promise<T>;
}

export { buildHeaders, API_BASE };

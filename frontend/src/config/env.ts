export const API_BASE = "http://localhost:8000";
export const API_KEY = "dev-secret-key";

export function buildHeaders(extra: Record<string, string> = {}): Record<string, string> {
  return {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY,
    ...extra,
  };
}

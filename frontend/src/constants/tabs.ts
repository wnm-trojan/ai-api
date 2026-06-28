import type { TabConfig } from "@/types/api";

export const TABS: TabConfig[] = [
  { id: "chat", label: "💬 Chat", color: "#6366f1" },
  { id: "stream", label: "⚡ Stream", color: "#8b5cf6" },
  { id: "json", label: "🧩 JSON Mode", color: "#0ea5e9" },
  { id: "function", label: "🔧 Function Call", color: "#10b981" },
];

export const TOOL_COLORS: Record<string, string> = {
  get_weather: "#f59e0b",
  calculate: "#10b981",
  search_database: "#6366f1",
  none: "#64748b",
};

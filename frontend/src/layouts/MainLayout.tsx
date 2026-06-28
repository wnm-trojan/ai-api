import type { ReactNode } from "react";
import { API_BASE } from "../config/env";
import { StatusBadge } from "../components/StatusBadge/StatusBadge";
import { TABS } from "../constants/tabs";
import { useHealth } from "../hooks/useHealth";

interface MainLayoutProps {
  activeTab: string;
  onTabChange: (tabId: string) => void;
  children: ReactNode;
}

export function MainLayout({ activeTab, onTabChange, children }: MainLayoutProps) {
  const health = useHealth();

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        color: "#e2e8f0",
        fontFamily: "'Inter', system-ui, sans-serif",
      }}
    >
      <div
        style={{
          background: "#0f172a",
          borderBottom: "1px solid #1e293b",
          padding: "0 24px",
        }}
      >
        <div
          style={{
            maxWidth: 900,
            margin: "0 auto",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            height: 60,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div
              style={{
                width: 32,
                height: 32,
                borderRadius: 8,
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 16,
              }}
            >
              🤖
            </div>
            <div>
              <div style={{ fontWeight: 700, fontSize: 15 }}>AI API Playground</div>
              <div style={{ color: "#64748b", fontSize: 12 }}>FastAPI + OpenAI</div>
            </div>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            {health && (
              <StatusBadge
                text={health.status === "healthy" ? "● API Online" : "○ API Offline"}
                color={health.status === "healthy" ? "#10b981" : "#ef4444"}
              />
            )}
            <a
              href={`${API_BASE}/docs`}
              target="_blank"
              rel="noreferrer"
              style={{
                color: "#64748b",
                fontSize: 12,
                textDecoration: "none",
                border: "1px solid #334155",
                borderRadius: 6,
                padding: "4px 10px",
              }}
            >
              Swagger →
            </a>
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 900, margin: "0 auto", padding: "24px 24px 80px" }}>
        <div
          style={{
            display: "flex",
            gap: 4,
            marginBottom: 24,
            background: "#1e293b",
            borderRadius: 12,
            padding: 4,
          }}
        >
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => onTabChange(t.id)}
              style={{
                flex: 1,
                padding: "10px 4px",
                border: "none",
                borderRadius: 9,
                fontWeight: 600,
                fontSize: 13,
                cursor: "pointer",
                transition: "all .2s",
                background: activeTab === t.id ? t.color : "transparent",
                color: activeTab === t.id ? "#fff" : "#64748b",
              }}
            >
              {t.label}
            </button>
          ))}
        </div>

        {children}
      </div>
    </div>
  );
}

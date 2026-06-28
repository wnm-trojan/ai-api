import type { ReactNode } from "react";

interface CardProps {
  title?: string;
  subtitle?: string;
  accent: string;
  children: ReactNode;
}

export function Card({ title, subtitle, accent, children }: CardProps) {
  return (
    <div
      style={{
        background: "#1e293b",
        borderRadius: 16,
        padding: 24,
        border: `1px solid ${accent}33`,
        boxShadow: "0 0 0 1px #ffffff08",
      }}
    >
      {title && (
        <div style={{ marginBottom: 16 }}>
          <div style={{ color: accent, fontWeight: 700, fontSize: 15 }}>{title}</div>
          {subtitle && (
            <div style={{ color: "#64748b", fontSize: 13, marginTop: 3 }}>{subtitle}</div>
          )}
        </div>
      )}
      {children}
    </div>
  );
}

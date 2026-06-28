import type { ReactNode } from "react";

interface CodeBlockProps {
  children: ReactNode;
}

export function CodeBlock({ children }: CodeBlockProps) {
  return (
    <pre
      style={{
        background: "#0f172a",
        color: "#e2e8f0",
        borderRadius: 10,
        padding: "14px 16px",
        fontSize: 13,
        overflowX: "auto",
        margin: 0,
        lineHeight: 1.6,
        fontFamily: "'Fira Code', monospace",
      }}
    >
      <code>{children}</code>
    </pre>
  );
}

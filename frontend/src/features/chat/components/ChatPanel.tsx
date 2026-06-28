import { useState } from "react";
import { Button } from "@/components/Button/Button";
import { Card } from "@/components/Card/Card";
import { CodeBlock } from "@/components/CodeBlock/CodeBlock";
import { ErrorBox } from "@/components/ErrorBox/ErrorBox";
import { Textarea } from "@/components/Input/Textarea";
import { StatusBadge } from "@/components/StatusBadge/StatusBadge";
import { apiFetch } from "@/services/apiClient";
import type { ChatResponse, Message } from "@/types/api";

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "system", content: "You are a helpful assistant." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [error, setError] = useState("");

  const send = async () => {
    if (!input.trim()) return;
    const newMessages: Message[] = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);
    setError("");

    try {
      const data = await apiFetch<ChatResponse>("/api/chat", { messages: newMessages });
      setResponse(data);
      setMessages([...newMessages, { role: "assistant", content: data.message }]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <Card title="Conversation" accent="#6366f1">
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 12 }}>
          {messages
            .filter((m) => m.role !== "system")
            .map((m, i) => (
              <div
                key={i}
                style={{
                  display: "flex",
                  flexDirection: m.role === "user" ? "row-reverse" : "row",
                  gap: 10,
                }}
              >
                <div
                  style={{
                    background: m.role === "user" ? "#6366f1" : "#1e293b",
                    border: m.role === "assistant" ? "1px solid #334155" : "none",
                    borderRadius: m.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                    padding: "10px 14px",
                    color: "#e2e8f0",
                    fontSize: 14,
                    maxWidth: "75%",
                    lineHeight: 1.6,
                  }}
                >
                  {m.content}
                </div>
              </div>
            ))}
          {loading && (
            <div
              style={{
                color: "#64748b",
                fontSize: 13,
                display: "flex",
                alignItems: "center",
                gap: 8,
              }}
            >
              <span style={{ animation: "pulse 1s infinite" }}>●●●</span> thinking...
            </div>
          )}
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <div style={{ flex: 1 }}>
            <Textarea value={input} onChange={setInput} placeholder="Ask anything..." rows={2} />
          </div>
          <Button onClick={send} loading={loading} disabled={!input.trim()}>
            Send
          </Button>
        </div>
      </Card>

      {error && <ErrorBox msg={error} />}

      {response && (
        <Card title="API Response" subtitle="Raw response from /api/chat" accent="#6366f1">
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
            <StatusBadge text={`Model: ${response.model}`} color="#6366f1" />
            <StatusBadge text={`${response.usage.total_tokens} tokens`} color="#8b5cf6" />
            <StatusBadge text={`${response.latency_ms}ms`} color="#0ea5e9" />
          </div>
          <CodeBlock>{JSON.stringify(response, null, 2)}</CodeBlock>
        </Card>
      )}

      <Card title="How it works" accent="#6366f1">
        <CodeBlock>{`POST /api/chat
Headers: { "X-API-Key": "..." }

Body:
{
  "messages": [
    { "role": "system", "content": "You are helpful." },
    { "role": "user",   "content": "Hello!" }
  ],
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "max_tokens": 1000
}`}</CodeBlock>
      </Card>
    </div>
  );
}

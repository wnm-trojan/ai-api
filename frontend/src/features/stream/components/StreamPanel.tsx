import { useRef, useState } from "react";
import { Button } from "@/components/Button/Button";
import { Card } from "@/components/Card/Card";
import { CodeBlock } from "@/components/CodeBlock/CodeBlock";
import { ErrorBox } from "@/components/ErrorBox/ErrorBox";
import { Textarea } from "@/components/Input/Textarea";
import { API_BASE, buildHeaders } from "@/config/env";

export function StreamPanel() {
  const [prompt, setPrompt] = useState(
    "Write a short story about a robot who discovers music."
  );
  const [streaming, setStreaming] = useState(false);
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const abortRef = useRef<AbortController | null>(null);

  const start = async () => {
    setOutput("");
    setError("");
    setStreaming(true);
    abortRef.current = new AbortController();

    try {
      const res = await fetch(`${API_BASE}/api/stream`, {
        method: "POST",
        headers: buildHeaders(),
        body: JSON.stringify({
          messages: [{ role: "user", content: prompt }],
        }),
        signal: abortRef.current.signal,
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const reader = res.body!.getReader();
      const decoder = new TextDecoder();
      let buf = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop() ?? "";
        for (const line of lines) {
          if (!line.startsWith("data:")) continue;
          const raw = line.slice(5).trim();
          if (raw === "[DONE]") {
            setStreaming(false);
            return;
          }
          try {
            const parsed = JSON.parse(raw) as { delta?: string; error?: string };
            if (parsed.delta) setOutput((prev) => prev + parsed.delta);
            if (parsed.error) setError(parsed.error);
          } catch {
            /* skip malformed */
          }
        }
      }
    } catch (e) {
      if (e instanceof Error && e.name !== "AbortError") setError(e.message);
    } finally {
      setStreaming(false);
    }
  };

  const stop = () => {
    abortRef.current?.abort();
    setStreaming(false);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <Card
        title="Streaming Response (SSE)"
        subtitle="Tokens appear in real-time via Server-Sent Events"
        accent="#8b5cf6"
      >
        <Textarea value={prompt} onChange={setPrompt} placeholder="Your prompt..." rows={2} />
        <div style={{ display: "flex", gap: 10, marginTop: 10 }}>
          <Button onClick={start} loading={streaming} color="#8b5cf6">
            Stream
          </Button>
          {streaming && (
            <Button onClick={stop} color="#ef4444">
              Stop
            </Button>
          )}
        </div>
      </Card>

      {error && <ErrorBox msg={error} />}

      {(output || streaming) && (
        <Card title="Live Output" accent="#8b5cf6">
          <div
            style={{
              background: "#0f172a",
              borderRadius: 10,
              padding: "14px 16px",
              color: "#e2e8f0",
              fontSize: 14,
              lineHeight: 1.8,
              minHeight: 80,
              fontFamily: "inherit",
            }}
          >
            {output}
            {streaming && (
              <span
                style={{
                  display: "inline-block",
                  width: 2,
                  height: 16,
                  background: "#8b5cf6",
                  marginLeft: 2,
                  animation: "blink 1s step-end infinite",
                  verticalAlign: "text-bottom",
                }}
              />
            )}
          </div>
        </Card>
      )}

      <Card title="How it works" accent="#8b5cf6">
        <CodeBlock>{`// Frontend reads SSE chunks
const res = await fetch("/api/stream", { ... });
const reader = res.body.getReader();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  // parse "data: {"delta":"Hello"}" lines
  setOutput(prev => prev + parsed.delta);
}

// Backend (FastAPI)
async def event_generator():
    async for chunk in openai_service.stream_completion(...):
        yield f"data: {json.dumps({'delta': chunk})}\\n\\n"
    yield "data: [DONE]\\n\\n"`}</CodeBlock>
      </Card>
    </div>
  );
}

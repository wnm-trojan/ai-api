import { useState } from "react";
import { Button } from "@/components/Button/Button";
import { Card } from "@/components/Card/Card";
import { CodeBlock } from "@/components/CodeBlock/CodeBlock";
import { ErrorBox } from "@/components/ErrorBox/ErrorBox";
import { Textarea } from "@/components/Input/Textarea";
import { JSON_EXAMPLES } from "@/features/json-mode/constants/examples";
import { apiFetch } from "@/services/apiClient";
import type { JSONResponse } from "@/types/api";

export function JSONPanel() {
  const [prompt, setPrompt] = useState(JSON_EXAMPLES[0].prompt);
  const [schema, setSchema] = useState(JSON_EXAMPLES[0].schema);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<JSONResponse | null>(null);
  const [error, setError] = useState("");

  const run = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await apiFetch<JSONResponse>("/api/json", {
        prompt,
        schema_hint: schema,
      });
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <Card title="JSON Mode" subtitle="GPT always returns valid, structured JSON" accent="#0ea5e9">
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
          {JSON_EXAMPLES.map((ex) => (
            <button
              key={ex.label}
              onClick={() => {
                setPrompt(ex.prompt);
                setSchema(ex.schema);
                setResult(null);
              }}
              style={{
                background: "#0f172a",
                border: "1px solid #334155",
                borderRadius: 8,
                padding: "5px 12px",
                color: "#94a3b8",
                fontSize: 12,
                cursor: "pointer",
              }}
            >
              {ex.label}
            </button>
          ))}
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <div>
            <div style={{ color: "#64748b", fontSize: 12, marginBottom: 4 }}>PROMPT</div>
            <Textarea value={prompt} onChange={setPrompt} rows={3} />
          </div>
          <div>
            <div style={{ color: "#64748b", fontSize: 12, marginBottom: 4 }}>
              SCHEMA HINT (optional)
            </div>
            <Textarea value={schema} onChange={setSchema} rows={2} />
          </div>
          <Button onClick={run} loading={loading} color="#0ea5e9">
            Extract JSON
          </Button>
        </div>
      </Card>

      {error && <ErrorBox msg={error} />}

      {result && (
        <Card title="Structured Output" accent="#0ea5e9">
          <CodeBlock>{JSON.stringify(result.data, null, 2)}</CodeBlock>
        </Card>
      )}

      <Card title="How it works" accent="#0ea5e9">
        <CodeBlock>{`# Backend uses response_format
response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    response_format={"type": "json_object"},  # ← key!
)

# Guaranteed valid JSON – no parsing errors
data = json.loads(response.choices[0].message.content)`}</CodeBlock>
      </Card>
    </div>
  );
}

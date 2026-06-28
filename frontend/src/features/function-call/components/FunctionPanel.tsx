import { useState } from "react";
import { Button } from "@/components/Button/Button";
import { Card } from "@/components/Card/Card";
import { CodeBlock } from "@/components/CodeBlock/CodeBlock";
import { ErrorBox } from "@/components/ErrorBox/ErrorBox";
import { Textarea } from "@/components/Input/Textarea";
import { StatusBadge } from "@/components/StatusBadge/StatusBadge";
import { TOOL_COLORS } from "@/constants/tabs";
import {
  AVAILABLE_TOOLS,
  FC_EXAMPLES,
} from "@/features/function-call/constants/examples";
import { apiFetch } from "@/services/apiClient";
import type { FunctionCallResponse } from "@/types/api";

export function FunctionPanel() {
  const [message, setMessage] = useState(FC_EXAMPLES[0]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<FunctionCallResponse | null>(null);
  const [error, setError] = useState("");

  const run = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await apiFetch<FunctionCallResponse>("/api/function-call", {
        user_message: message,
      });
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  };

  const toolColor = result ? TOOL_COLORS[result.tool_called] || "#64748b" : "#64748b";

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <Card
        title="Function Calling"
        subtitle="GPT picks the right tool, server runs it, GPT explains the result"
        accent="#10b981"
      >
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
          {FC_EXAMPLES.map((ex) => (
            <button
              key={ex}
              onClick={() => {
                setMessage(ex);
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
              {ex}
            </button>
          ))}
        </div>
        <Textarea value={message} onChange={setMessage} rows={2} />
        <div style={{ marginTop: 10 }}>
          <Button onClick={run} loading={loading} color="#10b981">
            Run
          </Button>
        </div>
      </Card>

      {error && <ErrorBox msg={error} />}

      {result && (
        <Card title="Execution trace" accent={toolColor}>
          {result.tool_called !== "none" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <StatusBadge text={`Tool: ${result.tool_called}`} color={toolColor} />
                <span style={{ color: "#64748b", fontSize: 13 }}>
                  GPT selected this tool automatically
                </span>
              </div>

              <div>
                <div style={{ color: "#64748b", fontSize: 12, marginBottom: 6 }}>ARGUMENTS</div>
                <CodeBlock>{JSON.stringify(result.tool_args, null, 2)}</CodeBlock>
              </div>

              <div>
                <div style={{ color: "#64748b", fontSize: 12, marginBottom: 6 }}>TOOL RESULT</div>
                <CodeBlock>{JSON.stringify(result.tool_result, null, 2)}</CodeBlock>
              </div>
            </div>
          )}

          <div style={{ marginTop: 16 }}>
            <div style={{ color: "#64748b", fontSize: 12, marginBottom: 6 }}>FINAL ANSWER</div>
            <div
              style={{
                background: "#0f172a",
                borderRadius: 10,
                padding: "12px 14px",
                color: "#e2e8f0",
                fontSize: 14,
                lineHeight: 1.7,
                border: `1px solid ${toolColor}44`,
              }}
            >
              {result.final_answer}
            </div>
          </div>
        </Card>
      )}

      <Card title="Available tools" accent="#10b981">
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {AVAILABLE_TOOLS.map((t) => (
            <div
              key={t.name}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                background: "#0f172a",
                borderRadius: 8,
                padding: "8px 12px",
              }}
            >
              <StatusBadge text={t.name} color={t.color} />
              <span style={{ color: "#94a3b8", fontSize: 13 }}>{t.desc}</span>
            </div>
          ))}
        </div>
      </Card>

      <Card title="How it works" accent="#10b981">
        <CodeBlock>{`# 1. First call – GPT decides which tool
response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=TOOLS,
    tool_choice="auto",   # ← GPT picks
)

# 2. Extract tool call
tool_name = response.choices[0].message.tool_calls[0].function.name
tool_args = json.loads(...)

# 3. Execute tool locally
result = execute_tool(tool_name, tool_args)

# 4. Second call – GPT explains the result
messages.append({"role": "tool", "content": json.dumps(result)})
final = await client.chat.completions.create(...)`}</CodeBlock>
      </Card>
    </div>
  );
}

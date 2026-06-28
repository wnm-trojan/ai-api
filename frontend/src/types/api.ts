export interface Message {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
}

export interface TokenUsage {
  total_tokens: number;
  prompt_tokens?: number;
  completion_tokens?: number;
}

export interface ChatResponse {
  message: string;
  model: string;
  usage: TokenUsage;
  latency_ms: number;
}

export interface JSONResponse {
  data: Record<string, unknown>;
}

export interface FunctionCallResponse {
  tool_called: string;
  tool_args: Record<string, unknown>;
  tool_result: unknown;
  final_answer: string;
}

export interface HealthResponse {
  status: string;
}

export interface TabConfig {
  id: string;
  label: string;
  color: string;
}

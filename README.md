# AI API – FastAPI + OpenAI + React

A production-ready full-stack project demonstrating every major OpenAI API pattern.

```
React Frontend (port 3000)
        │
  FastAPI Backend (port 8000)
        │   ├── /api/chat           → Chat Completion
        │   ├── /api/stream         → Streaming (SSE)
        │   ├── /api/json           → JSON Mode
        │   └── /api/function-call  → Function Calling
        │
   OpenAI SDK
        │
   GPT-4o-mini
```

---

## Project Structure

```
ai-api-project/
├── backend/
│   └── src/ 
|     ├── domain/ 
|     │ ├── entities/ chat.py, message.py, conversation.py 
|     │ ├── repositories/ chat_repository.py 
|     │ ├── services/ tokenizer.py 
|     │ ├── value_objects/ role.py, model.py 
|     │ └── exceptions/ __init__.py 
|     |
|     ├── application/ 
|     | ├── dtos/ chat_dtos.py 
|     | ├── use_cases/ chat_completion.py, stream_chat.py, json_chat.py, function_call.py 
|     | ├── interfaces/ ai_provider.py, tool_executor.py 
|     | └── mappers/ chat_mapper.py 
|     |
|     ├── infrastructure/ 
|     │ ├── ai/ openai_provider.py, anthropic_provider.py (stub) 
|     │ ├── persistence/ postgres/, redis/ (placeholders) 
|     │ ├── repositories/ chat_repository_impl.py 
|     │ ├── tools/ calculator.py, weather.py, tool_executor.py 
|     │ └── logging/ logger.py 
|     |
|     ├── presentation/ 
|     │ ├── routers/ chat_routers.py 
|     │ ├── schemas/ chat_schemas.py 
|     │ ├── middleware/ setup.py 
|     │ ├── dependencies/ deps.py 
|     │ └── exception_handlers/ domain_handlers.py 
|     |
|     ├── core/ 
|     │ ├── config.py 
|     │ ├── security.py 
|     │ ├── container.py 
|     │ └── constants.py 
|     └── main.py
│
└── frontend/
    ├── src/
    │   ├── App.jsx              ← Full UI: 4 interactive panels
    │   └── main.jsx
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## Backend Setup

### 1. Install dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-...
```

### 3. Run the server
```bash
uvicorn main:app --reload --port 8000
```

Swagger docs: http://localhost:8000/docs

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

---

## API Reference

All endpoints (except `/health`) require the header:
```
X-API-Key: dev-secret-key
```
Change `APP_API_KEY` in `.env` for production.

### POST /api/chat
Basic chat completion with full response.
```json
{
  "messages": [
    {"role": "system", "content": "You are helpful."},
    {"role": "user",   "content": "Hello!"}
  ],
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### POST /api/stream
Same body as `/api/chat`. Returns Server-Sent Events:
```
data: {"delta": "Hello"}
data: {"delta": " world"}
data: [DONE]
```

### POST /api/json
Structured JSON output guaranteed by OpenAI's JSON mode.
```json
{
  "prompt": "Extract: name, age from 'Alice is 30'",
  "schema_hint": "{\"name\": \"string\", \"age\": \"number\"}"
}
```

### POST /api/function-call
GPT picks a tool, server executes it, GPT explains the result.
```json
{
  "user_message": "What is the weather in Tokyo?"
}
```
Built-in tools: `get_weather`, `calculate`, `search_database`

---

## Features Demonstrated

| Feature           | Endpoint              | What it teaches                         |
|-------------------|-----------------------|-----------------------------------------|
| Chat Completion   | `POST /api/chat`      | Multi-turn messages, tokens, latency    |
| Streaming (SSE)   | `POST /api/stream`    | Real-time token delivery                |
| JSON Mode         | `POST /api/json`      | `response_format: json_object`          |
| Function Calling  | `POST /api/function-call` | Tool use, 2-turn pattern            |
| Rate Limiting     | All endpoints         | `slowapi` – 10–20 req/min per IP        |
| API Security      | All endpoints         | `X-API-Key` header validation           |
| Error Handling    | All endpoints         | HTTP exceptions, OpenAI error wrapping  |

---

## Rate Limits (default)

| Endpoint         | Limit        |
|------------------|--------------|
| `/api/chat`      | 20 / minute  |
| `/api/stream`    | 10 / minute  |
| `/api/json`      | 15 / minute  |
| `/api/function-call` | 10 / minute |

Adjust in `main.py` `@limiter.limit(...)` decorators.

---

## Production Checklist

- [ ] Set a strong `APP_API_KEY` in `.env`
- [ ] Restrict `allow_origins` in CORS middleware
- [ ] Use HTTPS (e.g. behind nginx or a cloud load balancer)
- [ ] Store secrets in a vault (AWS Secrets Manager, etc.)
- [ ] Add persistent rate limiting (Redis backend for slowapi)
- [ ] Add request logging / monitoring (e.g. Sentry, Datadog)
- [ ] Replace mock tool implementations in `openai_service.py`

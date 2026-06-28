"""Infrastructure – OpenAI provider implementation."""
import json
import time
from typing import AsyncIterator

from openai import AsyncOpenAI

from src.application.interfaces.ai_provider import IAIProvider
from src.application.interfaces.tool_executor import IToolExecutor
from src.core.constants import DEFAULT_MODEL, OPENAI_TOOL_DEFINITIONS
from src.domain.entities.chat import ChatResult, JsonResult, ToolCall
from src.domain.entities.message import Message, TokenUsage


def _to_openai_messages(messages: list[Message]) -> list[dict]:
    return [{"role": m.role, "content": m.content} for m in messages]


class OpenAIProvider(IAIProvider):
    def __init__(self, client: AsyncOpenAI) -> None:
        self._client = client

    async def complete(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> ChatResult:
        start = time.perf_counter()
        resp = await self._client.chat.completions.create(
            model=model,
            messages=_to_openai_messages(messages),
            temperature=temperature,
            max_tokens=max_tokens,
        )
        elapsed = int((time.perf_counter() - start) * 1000)
        return ChatResult(
            content=resp.choices[0].message.content,
            model=resp.model,
            usage=TokenUsage(
                prompt_tokens=resp.usage.prompt_tokens,
                completion_tokens=resp.usage.completion_tokens,
                total_tokens=resp.usage.total_tokens,
            ),
            latency_ms=elapsed,
        )

    async def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
    ) -> AsyncIterator[str]:
        stream = await self._client.chat.completions.create(
            model=model,
            messages=_to_openai_messages(messages),
            temperature=temperature,
            stream=True,
        )

        async def _gen():
            async for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta

        return _gen()

    async def complete_json(self, prompt: str, schema_hint: str) -> JsonResult:
        system = (
            "You are a data extraction assistant. "
            "Always respond with valid JSON only – no markdown, no extra text."
        )
        if schema_hint:
            system += f" Use this schema: {schema_hint}"

        resp = await self._client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        return JsonResult(data=json.loads(resp.choices[0].message.content))

    async def call_with_tools(
        self,
        user_message: str,
        tool_executor: IToolExecutor,
    ) -> ToolCall:
        messages = [
            {"role": "system", "content": "You are a helpful assistant with tools. Use them when relevant."},
            {"role": "user", "content": user_message},
        ]
        resp = await self._client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=OPENAI_TOOL_DEFINITIONS,
            tool_choice="auto",
        )
        choice = resp.choices[0]

        if not choice.message.tool_calls:
            return ToolCall(
                tool_name="none",
                tool_args={},
                tool_result=None,
                final_answer=choice.message.content,
            )

        tc = choice.message.tool_calls[0]
        name = tc.function.name
        args = json.loads(tc.function.arguments)
        result = tool_executor.execute(name, args)

        messages.append(choice.message)
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})

        final = await self._client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
        )
        return ToolCall(
            tool_name=name,
            tool_args=args,
            tool_result=result,
            final_answer=final.choices[0].message.content,
        )

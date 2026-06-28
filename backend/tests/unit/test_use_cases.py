"""
Unit Tests – Application Use Cases
Test business logic in isolation using in-memory fakes.
Zero I/O, zero OpenAI SDK, instant execution.
"""
import pytest

from src.domain.entities.chat import ChatResult, JsonResult, ToolCall
from src.domain.entities.message import Message, TokenUsage
from src.domain.repositories.chat_repository import (
    IChatRepository,
    IJsonRepository,
    IToolRepository,
)
from src.application.use_cases.chat_completion import ChatCompletionUseCase
from src.application.use_cases.json_chat import JsonChatUseCase
from src.application.use_cases.function_call import FunctionCallUseCase


class FakeChatRepo(IChatRepository):
    async def complete(self, messages, model, temperature, max_tokens):
        return ChatResult(
            content="Hello from fake!",
            model=model,
            usage=TokenUsage(10, 5, 15),
            latency_ms=42,
        )


class FakeJsonRepo(IJsonRepository):
    async def complete_json(self, prompt, schema_hint):
        return JsonResult(data={"name": "Alice", "age": 30})


class FakeToolRepo(IToolRepository):
    async def call_with_tools(self, user_message):
        return ToolCall(
            tool_name="get_weather",
            tool_args={"city": "Tokyo"},
            tool_result={"temperature": "25°C"},
            final_answer="It is 25°C in Tokyo.",
        )


class TestChatCompletionUseCase:
    @pytest.mark.asyncio
    async def test_returns_result(self):
        uc = ChatCompletionUseCase(FakeChatRepo())
        result = await uc.execute(
            messages=[Message(role="user", content="Hi")],
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=100,
        )
        assert result.content == "Hello from fake!"
        assert result.usage.total_tokens == 15

    @pytest.mark.asyncio
    async def test_raises_on_empty_messages(self):
        uc = ChatCompletionUseCase(FakeChatRepo())
        with pytest.raises(ValueError, match="empty"):
            await uc.execute([], "gpt-4o-mini", 0.7, 100)


class TestJsonChatUseCase:
    @pytest.mark.asyncio
    async def test_returns_structured_data(self):
        uc = JsonChatUseCase(FakeJsonRepo())
        result = await uc.execute("Extract Alice age 30", "")
        assert result.data["name"] == "Alice"

    @pytest.mark.asyncio
    async def test_raises_on_blank_prompt(self):
        uc = JsonChatUseCase(FakeJsonRepo())
        with pytest.raises(ValueError, match="blank"):
            await uc.execute("   ", "")


class TestFunctionCallUseCase:
    @pytest.mark.asyncio
    async def test_returns_tool_result(self):
        uc = FunctionCallUseCase(FakeToolRepo())
        result = await uc.execute("What is the weather in Tokyo?")
        assert result.tool_name == "get_weather"
        assert "25°C" in result.final_answer

    @pytest.mark.asyncio
    async def test_raises_on_blank_message(self):
        uc = FunctionCallUseCase(FakeToolRepo())
        with pytest.raises(ValueError, match="blank"):
            await uc.execute("  ")

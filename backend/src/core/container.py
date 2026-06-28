"""Core – dependency injection container."""
from functools import lru_cache

from openai import AsyncOpenAI

from src.application.use_cases.chat_completion import ChatCompletionUseCase
from src.application.use_cases.function_call import FunctionCallUseCase
from src.application.use_cases.json_chat import JsonChatUseCase
from src.application.use_cases.stream_chat import StreamChatUseCase
from src.core.config import settings
from src.infrastructure.ai.openai_provider import OpenAIProvider
from src.infrastructure.repositories.chat_repository_impl import (
    ChatRepositoryImpl,
    JsonRepositoryImpl,
    StreamRepositoryImpl,
    ToolRepositoryImpl,
)
from src.infrastructure.tools.tool_executor import ToolExecutor


@lru_cache(maxsize=1)
def get_openai_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=settings.openai_api_key)


@lru_cache(maxsize=1)
def get_ai_provider() -> OpenAIProvider:
    return OpenAIProvider(get_openai_client())


@lru_cache(maxsize=1)
def get_tool_executor() -> ToolExecutor:
    return ToolExecutor()


def get_chat_use_case() -> ChatCompletionUseCase:
    return ChatCompletionUseCase(ChatRepositoryImpl(get_ai_provider()))


def get_stream_use_case() -> StreamChatUseCase:
    return StreamChatUseCase(StreamRepositoryImpl(get_ai_provider()))


def get_json_use_case() -> JsonChatUseCase:
    return JsonChatUseCase(JsonRepositoryImpl(get_ai_provider()))


def get_function_call_use_case() -> FunctionCallUseCase:
    return FunctionCallUseCase(
        ToolRepositoryImpl(get_ai_provider(), get_tool_executor())
    )

"""Presentation – chat API routers."""
import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.application.mappers.chat_mapper import to_messages
from src.application.dtos.chat_dtos import MessageDTO
from src.application.use_cases.chat_completion import ChatCompletionUseCase
from src.application.use_cases.function_call import FunctionCallUseCase
from src.application.use_cases.json_chat import JsonChatUseCase
from src.application.use_cases.stream_chat import StreamChatUseCase
from src.presentation.dependencies.deps import (
    get_chat_use_case,
    get_function_call_use_case,
    get_json_use_case,
    get_stream_use_case,
    verify_api_key,
)
from src.presentation.schemas.chat_schemas import (
    ChatRequestSchema,
    ChatResponseSchema,
    JsonRequestSchema,
    JsonResponseSchema,
    StreamRequestSchema,
    TokenUsageSchema,
    ToolCallRequestSchema,
    ToolCallResponseSchema,
)

limiter = Limiter(key_func=get_remote_address)

chat_router = APIRouter(prefix="/api/chat", tags=["Chat"])


@chat_router.post("", response_model=ChatResponseSchema, dependencies=[Depends(verify_api_key)])
@limiter.limit("20/minute")
async def chat(
    request: Request,
    body: ChatRequestSchema,
    use_case: ChatCompletionUseCase = Depends(get_chat_use_case),
):
    try:
        result = await use_case.execute(
            messages=to_messages([MessageDTO(**m.model_dump()) for m in body.messages]),
            model=body.model,
            temperature=body.temperature,
            max_tokens=body.max_tokens,
        )
        return ChatResponseSchema(
            message=result.content,
            model=result.model,
            usage=TokenUsageSchema(**result.usage.__dict__),
            latency_ms=result.latency_ms,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


stream_router = APIRouter(prefix="/api/stream", tags=["Streaming"])


@stream_router.post("", dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
async def stream_chat(
    request: Request,
    body: StreamRequestSchema,
    use_case: StreamChatUseCase = Depends(get_stream_use_case),
):
    async def sse_generator():
        try:
            gen = await use_case.execute(
                messages=to_messages([MessageDTO(**m.model_dump()) for m in body.messages]),
                model=body.model,
                temperature=body.temperature,
            )
            async for token in gen:
                yield f"data: {json.dumps({'delta': token})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


json_router = APIRouter(prefix="/api/json", tags=["JSON Mode"])


@json_router.post("", response_model=JsonResponseSchema, dependencies=[Depends(verify_api_key)])
@limiter.limit("15/minute")
async def json_mode(
    request: Request,
    body: JsonRequestSchema,
    use_case: JsonChatUseCase = Depends(get_json_use_case),
):
    try:
        result = await use_case.execute(prompt=body.prompt, schema_hint=body.schema_hint)
        return JsonResponseSchema(data=result.data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


tool_router = APIRouter(prefix="/api/function-call", tags=["Function Calling"])


@tool_router.post("", response_model=ToolCallResponseSchema, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
async def function_call(
    request: Request,
    body: ToolCallRequestSchema,
    use_case: FunctionCallUseCase = Depends(get_function_call_use_case),
):
    try:
        result = await use_case.execute(user_message=body.user_message)
        return ToolCallResponseSchema(
            tool_called=result.tool_name,
            tool_args=result.tool_args,
            tool_result=result.tool_result,
            final_answer=result.final_answer,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""Presentation – domain exception → HTTP mapping."""
from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import (
    AIProviderError,
    DomainError,
    ToolExecutionError,
    UnauthorizedError,
    ValidationError,
)


async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    status_code = 500
    if isinstance(exc, ValidationError):
        status_code = 422
    elif isinstance(exc, UnauthorizedError):
        status_code = 401
    elif isinstance(exc, (AIProviderError, ToolExecutionError)):
        status_code = 502
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})
